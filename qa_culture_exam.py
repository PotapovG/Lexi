"""CULT-06 secure mock-exam tests using existing server and temporary SQLite.

Synthetic cards test the sealed session only: no private or official exam text.
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import tempfile
import uuid
from pathlib import Path

import answer_idempotency
import culture_adapter
import culture_exam
import server

UTC=dt.timezone.utc
ROOT=Path(__file__).parent
AT=dt.datetime(2026,11,14,10,0,0,tzinfo=UTC)


def rid():
    return str(uuid.uuid4())


def corpus():
    fixture=json.loads((ROOT/"tests/fixtures/culture/sample_corpus.json").read_text(encoding="utf-8"))
    cards={}
    for i in range(30):
        q=copy.deepcopy(fixture["questions"][i%4])
        f=copy.deepcopy(fixture["facts"][i%4])
        q["id"]=f"cyq_geo_{i+5000:04d}"
        f["id"]=f"cyf_geo_{i+5000:04d}"
        q["fact_id"]=f["id"]
        q["topic"]=["GEO","GOV","HIS","NEWS"][i%4]
        f["topic"]=q["topic"]
        if q["freshness"]=="current":
            q["review_due"]=f["review_due"]="2027-01-01"
            q["valid_until"]=f["valid_until"]="2027-02-01"
        cards[q["id"]]=culture_adapter.to_card(q,f)
    # One more formulation of an existing fact: still only 30 unique facts.
    alt=dict(cards["cyq_geo_5000"])
    alt["id"]="cyq_geo_9000"
    cards[alt["id"]]=alt
    return cards


def test_server_profile():
    original_db=server.DB
    original_cards=dict(server.CULTURE_BY_ID)
    original_pepper=server.auth.SECRET_FILE
    try:
        with tempfile.TemporaryDirectory(prefix="lexi-cyprus-exam-") as scratch:
            server.DB=str(Path(scratch)/"student.sqlite3")
            server.auth.SECRET_FILE=Path(scratch)/"pepper"
            server.CULTURE_BY_ID.clear()
            server.CULTURE_BY_ID.update(corpus())
            server.init_db()
            with server.conn() as db:
                schemas={r[0] for r in db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'")}
                assert "culture_exam_sessions" in schemas
                assert "progress" in schemas and "attempts" in schemas and "srs_schedule" in schemas
                assert not any(x.startswith("culture_exam_answers") for x in schemas)

            uid="mock-exam-user"
            start_key=rid()
            with server.conn() as db:
                assert not culture_exam.get(db,uid,now=AT)["exists"]
            with server.conn() as db:
                started=culture_exam.action(db,uid,
                    {"action":"start","requestId":start_key,"goal":"citizenship","lang":"ru"},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT)
            assert started["status"]=="active"
            assert started["durationMinutes"]==45 and started["total"]==25
            assert started["answered"]==0 and started["revision"]==0
            assert len(started["questions"])==25
            ids={x["id"] for x in started["questions"]}
            facts={server.CULTURE_BY_ID[x["id"]]["factId"] for x in started["questions"]}
            assert len(ids)==len(facts)==25
            for row in started["questions"]:
                assert set(row)=={"id","topic","cultureFormat","prompt","choices","selectedIndex","flagged"}
                assert len(row["choices"])==4
            raw=json.dumps(started,ensure_ascii=False)
            for secret in ("correctIndex","correct_index","correctChoice",
                           "optionTranslations","explanation","source","truth",
                           "translations","answerIndex"):
                assert f'"{secret}"' not in raw,secret
            assert started["deadlineAt"]=="2026-11-14T10:45:00+00:00"

            # First start and same idempotency key return the same server snapshot.
            with server.conn() as db:
                again=culture_exam.action(db,uid,
                    {"action":"start","requestId":start_key,"goal":"citizenship","lang":"ru"},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT)
                assert again["sessionId"]==started["sessionId"]
            with server.conn() as db:
                concurrent=culture_exam.action(db,uid,
                    {"action":"start","requestId":rid(),"lang":"en"},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT)
                assert concurrent["sessionId"]==started["sessionId"]

            with server.conn() as db:
                assert culture_exam.has_live_exam(db,uid,AT)
                assert not culture_exam.get(db,"another-user",started["sessionId"],now=AT)["exists"]
            try:
                with server.conn() as db:
                    culture_exam.action(db,"another-user",
                        {"action":"finish","sessionId":started["sessionId"],"revision":0},
                        server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT)
            except ValueError as exc:
                assert "unknown_exam_session" in str(exc)
            else:
                raise AssertionError("cross-account exam read")

            # Ordinary study quiz and direct grading cannot reveal the active exam's answers.
            try:
                server.make_quiz(uid,{"scope":["culture"],"mode":["all"],"lang":["ru"],"count":["25"]})
            except ValueError as exc:
                assert str(exc)=="active_culture_exam"
            else:
                raise AssertionError("study quiz open during exam")
            card_id=started["questions"][0]["id"]
            raw_card=server.CULTURE_BY_ID[card_id]
            try:
                server.mark(uid,{"id":card_id,"direction":"culture_select","lang":"ru",
                                 "selected":raw_card["options"][0]})
            except ValueError as exc:
                assert str(exc)=="active_culture_exam"
            else:
                raise AssertionError("study scoring open during exam")

            # Answer is saved without immediate score; retry is idempotent.
            req=rid()
            selected=3
            selection={"action":"answer","sessionId":started["sessionId"],
                       "questionId":card_id,"selectedIndex":selected,
                       "revision":0,"requestId":req}
            with server.conn() as db:
                saved=culture_exam.action(db,uid,selection,
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(seconds=2))
            assert saved["revision"]==1 and saved["answered"]==1
            assert next(q for q in saved["questions"] if q["id"]==card_id)["selectedIndex"]==selected
            assert "correctIndex" not in json.dumps(saved)
            with server.conn() as db:
                replay=culture_exam.action(db,uid,selection,
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(seconds=2))
            assert replay["revision"]==1
            try:
                with server.conn() as db:
                    culture_exam.action(db,uid,{**selection,"selectedIndex":1},
                        server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(seconds=3))
            except ValueError as exc:
                assert "reused" in str(exc)
            else:
                raise AssertionError("reused request ID accepted altered choice")
            try:
                with server.conn() as db:
                    culture_exam.action(db,uid,{**selection,"requestId":rid(),"revision":0},
                        server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(seconds=3))
            except ValueError as exc:
                assert str(exc)=="stale_exam_revision"
            else:
                raise AssertionError("stale concurrent answer accepted")

            # Marked for return: same question, existing session/revision.
            with server.conn() as db:
                flagged=culture_exam.action(db,uid,
                    {"action":"flag","sessionId":started["sessionId"],"questionId":card_id,
                     "flagged":True,"revision":1,"requestId":rid()},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(seconds=4))
            assert flagged["revision"]==2
            assert next(q for q in flagged["questions"] if q["id"]==card_id)["flagged"]

            # Review is available only after explicit completion, immutable thereafter.
            with server.conn() as db:
                done=culture_exam.action(db,uid,{"action":"finish",
                    "sessionId":started["sessionId"],"revision":2},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(minutes=5))
            assert done["status"]=="finished" and done["answered"]==1
            assert done["score"] in (0,1) and done["passingScore"]==15
            assert done["passed"] is False and done["reason"]=="submitted"
            assert all("correctIndex" in q and "optionTranslations" in q
                       and "explanation" in q and "source" in q
                       for q in done["questions"])
            with server.conn() as db:
                assert not culture_exam.has_live_exam(db,uid,AT+dt.timedelta(minutes=6))
                completed_again=culture_exam.action(db,uid,{"action":"finish",
                    "sessionId":started["sessionId"],"revision":2},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(minutes=7))
                assert completed_again["score"]==done["score"]
            with server.conn() as db:
                assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==0
                assert db.execute("SELECT COUNT(*) FROM progress").fetchone()[0]==0
                assert db.execute("SELECT COUNT(*) FROM srs_schedule").fetchone()[0]==0

            # New exam uses new immutable question snapshot and own deadline.
            with server.conn() as db:
                restarted=culture_exam.action(db,uid,{"action":"start",
                    "requestId":rid(),"lang":"en","goal":"citizenship"},
                    server.CULTURE_BY_ID,server.CULTURE_CONFIG,now=AT+dt.timedelta(minutes=8))
            with server.conn() as db:
                expired=culture_exam.get(db,uid,restarted["sessionId"],now=AT+dt.timedelta(minutes=55))
            assert expired["status"]=="finished" and expired["reason"]=="time_expired"
            assert expired["answered"]==0 and expired["score"]==0
            assert expired["deadlineAt"]=="2026-11-14T10:53:00+00:00"

            # Fewer than 25 different facts must not create a misleading "mock exam".
            smaller={key:val for key,val in list(server.CULTURE_BY_ID.items())[:24]}
            try:
                with server.conn() as db:
                    culture_exam.action(db,"new-student",{"action":"start","requestId":rid()},
                        smaller,server.CULTURE_CONFIG,now=AT)
            except ValueError as exc:
                assert str(exc)=="not_enough_reviewed_culture_facts"
            else:
                raise AssertionError("insufficient published bank accepted")
    finally:
        server.DB=original_db
        server.auth.SECRET_FILE=original_pepper
        server.CULTURE_BY_ID.clear()
        server.CULTURE_BY_ID.update(original_cards)


def test_receipt_replay_guard():
    # Used by the HTTP /api/answer validator: pre-check Culture before replay
    # of an old stored answer receipt, under the same write transaction.
    with tempfile.TemporaryDirectory(prefix="lexi-culture-side-channel-") as scratch:
        import sqlite3
        dbpath=Path(scratch)/"receipts.sqlite3"
        def connect():
            c=sqlite3.connect(dbpath)
            c.row_factory=sqlite3.Row
            return c
        with connect() as db:
            answer_idempotency.schema(db)
        uid="receipt-test"
        request=rid()
        body={"id":"cyq_geo_9999","direction":"culture_select",
              "selected":"A","lang":"ru","requestId":request}
        calls=[]
        def grader(user_id,body,injected_db=None):
            calls.append(body)
            return {"correct":True,"answer":"A"}
        def permitted(db,uid,body):
            return
        result=answer_idempotency.score_once(connect,grader,uid,body,validate_attempt=permitted)
        assert result["answer"]=="A"
        def forbidden(db,uid,body):
            raise ValueError("active_culture_exam")
        try:
            answer_idempotency.score_once(connect,grader,uid,body,validate_attempt=forbidden)
        except ValueError as exc:
            assert str(exc)=="active_culture_exam"
        else:
            raise AssertionError("stored receipt revealed a correct answer during exam")
        assert len(calls)==1


if __name__=="__main__":
    test_server_profile()
    test_receipt_replay_guard()
    print("PASS CULT-06 server-authoritative 25×45 sealed exam, recovery, ownership, idempotency, side-door guard")
