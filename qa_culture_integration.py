#!/usr/bin/env python3
"""CULT-03 shared-engine contract: synthetic fixtures, isolated temporary SQLite.

Draft fixtures are NEVER copied to live content or published as Cyprus facts.
"""
import copy
import json
import tempfile
import uuid
from pathlib import Path

import answer_idempotency
import culture_adapter
import server

ROOT=Path(__file__).parent


def test_shared_ledger():
    fixture=json.loads((ROOT/"tests/fixtures/culture/sample_corpus.json").read_text(encoding="utf-8"))
    q=fixture["questions"][0]
    f=fixture["facts"][0]
    card=culture_adapter.to_card(q,f)
    key=card["id"]+":"+culture_adapter.CULTURE_DIRECTION
    old_db=server.DB
    old_pepper=server.auth.SECRET_FILE
    old_cards=dict(server.CULTURE_BY_ID)
    try:
        with tempfile.TemporaryDirectory(prefix="lexi-culture-integration-") as tmp:
            server.DB=str(Path(tmp)/"data.sqlite3")
            server.auth.SECRET_FILE=Path(tmp)/"login-pepper"
            server.CULTURE_BY_ID.clear()
            server.CULTURE_BY_ID[card["id"]]=card
            server.init_db()
            uid="culture-integration-user"
            # Same quiz endpoint/renderer contract: four Greek choices,
            # no translations, correct index, explanations or source before answer.
            params={"scope":["culture"],"lang":["ru"],"mode":["all"],"count":["25"]}
            batch=server.make_quiz(uid,params)
            assert batch["scope"]=="culture" and batch["count"]==1
            assert batch["available"]==1
            shown=batch["questions"][0]
            assert shown["kind"]=="culture" and shown["direction"]=="culture_select"
            assert shown["factId"]==card["factId"]
            assert set(shown["choices"])==set(q["options_el"]) and len(shown["choices"])==4
            for private in ("answerIndex","correct_index","options_el","translations","explanations",
                            "explanation","source","correct","answer"):
                assert private not in shown,(private,shown)
            assert server.make_quiz(uid,{**params,"topics":["GOV"]})["count"]==0
            assert server.make_quiz(uid,{**params,"lang":["en"]})["count"]==1
            try:server.make_quiz(uid,{**params,"lang":["ar"]})
            except ValueError:pass
            else:raise AssertionError("unsupported locale was silently substituted")

            # A wrong answer uses the existing progress/weak+SRS tables.
            wrong={"id":card["id"],"direction":"culture_select","lang":"ru",
                   "selected":q["options_el"][1],"srsOptIn":True,
                   "requestId":str(uuid.uuid4())}
            outcome=answer_idempotency.score_once(server.conn,server.mark,uid,wrong)
            assert not outcome["correct"] and outcome["answer"]==q["options_el"][0]
            assert "translationChoices" in outcome and outcome["explanation"]
            again=answer_idempotency.score_once(server.conn,server.mark,uid,wrong)
            assert again==outcome,"idempotent retry must replay the receipt"
            assert server.make_quiz(uid,{**params,"mode":["weak"]})["count"]==1
            assert server.make_quiz(uid,{**params,"mode":["srs_due"]})["count"]==0
            with server.conn() as db:
                db.execute("UPDATE srs_schedule SET due_at='2020-01-01T00:00:00+00:00' WHERE user_id=?",
                           (uid,))
            assert server.make_quiz(uid,{**params,"mode":["srs_due"]})["count"]==1
            assert server.stats(uid)["attempts"]==0, "A1/A2 stats polluted"
            assert server.stats(uid)["weak"]==0, "Culture weak surfaced in Greek study"
            assert server.stats(uid,scope="culture")["attempts"]==1
            assert server.stats(uid,scope="culture")["weak"]==1

            # Assisted correct answers must not clear weak debt or count as independent mastery.
            helped={**wrong,"selected":q["options_el"][0],"assisted":True,
                    "requestId":str(uuid.uuid4())}
            helped_result=answer_idempotency.score_once(server.conn,server.mark,uid,helped)
            assert helped_result["correct"] and helped_result["assisted"]
            assert not helped_result["independentCorrect"]
            with server.conn() as db:
                row=db.execute("SELECT attempts,correct,miss_debt FROM progress WHERE user_id=? AND card_key=?",
                               (uid,key)).fetchone()
                assert (row["attempts"],row["correct"],row["miss_debt"])==(2,0,2),dict(row)
                receipts=db.execute("SELECT COUNT(*) FROM answer_receipts").fetchone()[0]
                assert receipts==2
                srs=db.execute("SELECT COUNT(*) FROM srs_schedule").fetchone()[0]
                assert srs==1,"assisted must not create or advance SRS entries"

            independent={**helped,"assisted":False,"requestId":str(uuid.uuid4())}
            independent_result=answer_idempotency.score_once(server.conn,server.mark,uid,independent)
            assert independent_result["independentCorrect"]
            with server.conn() as db:
                row=db.execute("SELECT attempts,correct,miss_debt FROM progress WHERE user_id=? AND card_key=?",
                               (uid,key)).fetchone()
                assert (row["attempts"],row["correct"],row["miss_debt"])==(3,1,1),dict(row)
                attempts=db.execute("SELECT kind,correct,assisted FROM attempts WHERE user_id=? ORDER BY id",
                                    (uid,)).fetchall()
                assert [tuple(x) for x in attempts]==[
                    ("culture",0,0),("culture",1,1),("culture",1,0)]
                srs_culture=server.learning_engine.status(db,uid,scope="culture")
                srs_book=server.learning_engine.status(db,uid,scope="book")
                assert srs_culture["scheduled"]==1 and srs_book["scheduled"]==0

            summary=server.stats(uid,scope="culture")
            assert summary["assisted"]==1 and summary["masteredFacts"]==1
            assert summary["topics"]["GEO"]["independentCorrect"]==1
            assert server.stats(uid)["attempts"]==0
            try:
                answer_idempotency.score_once(server.conn,server.mark,uid,
                    {**independent,"assisted":True})
            except ValueError:pass
            else:raise AssertionError("reusing receipt with different assisted flag was accepted")
            try:
                server.mark(uid,{**wrong,"selected":"не вариант","requestId":str(uuid.uuid4())})
            except ValueError:pass
            else:raise AssertionError("out-of-pool culture answer was accepted")
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_pepper
        server.CULTURE_BY_ID.clear()
        server.CULTURE_BY_ID.update(old_cards)


if __name__=="__main__":
    test_shared_ledger()
    print("PASS CULT-03: 4-choice safe payload, shared quiz/score/weak/SRS, assisted, "
          "idempotency, RU/EN, chapter stats isolation, all in temporary SQLite")
