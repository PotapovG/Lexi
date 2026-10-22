"""Isolated integrity/security/regression suite for personalized and Greek dialogues."""
import tempfile,sqlite3,collections
from pathlib import Path
import server, vocab_lessons as vocab, personalized, dialogues
def qs(uid,scope="pages",study="textbook",types="word,dialogue",**extra):
    parms=dict(scope=[scope],study=[study],types=[types],lang=["ru"],count=["60"],**{"from":["1"],"to":["56"]})
    for k,v in extra.items():parms[k]=[str(v)]
    return server.make_quiz(uid,parms)["questions"]

with tempfile.TemporaryDirectory() as d:
    server.DB=str(Path(d)/"test.sqlite3")
    server.init_db()
    u1,u2="isotest_user1","isotest_user2"
    initial=qs(u1,types="word")
    assert initial and all(not c["id"].startswith("personal_") for c in initial)
    with server.conn() as db:
        assert personalized.progress_summary(db,u1)["learned"]==0
    candidate=next(w for w in vocab.VOCAB if w["id"].startswith("vx") and w["level"]=="A2" and w["gr"] not in {c["gr"] for c in server.ALL if c["kind"]=="word"})
    cid="personal_"+candidate["id"]
    with server.conn() as db:
        assert not personalized.is_learned(db,u1,candidate["id"])
    try:
        server.mark(u1,{"id":cid,"direction":"ru-gr","selected":candidate["gr"],"lang":"ru"})
        raise AssertionError("Unlearned personal word accepted")
    except ValueError:pass
    with server.conn() as db:
        # First correct answer in vocab course unlocks word for this account only.
        right=vocab.answer(db,u1,{"id":candidate["id"],"direction":"target-gr","selected":candidate["gr"],"lang":"ru"})
        assert right["correct"]
        assert personalized.progress_summary(db,u1)["learned"]==1
        assert personalized.progress_summary(db,u2)["learned"]==0
    personalized_q=qs(u1,study="personalized")
    assert any(x["id"]==cid for x in personalized_q), "learned word must get guaranteed quota"
    assert not any(x["id"]==cid for x in qs(u2,study="personalized")), "account isolation"
    assert not any(x["id"]==cid for x in qs(u1,study="textbook")), "textbook isolation"
    assert server.mark(u1,{"id":cid,"direction":"ru-gr","selected":candidate["gr"],"lang":"ru"})["correct"]
    try:
        server.mark(u2,{"id":cid,"direction":"ru-gr","selected":candidate["gr"],"lang":"ru"})
        raise AssertionError("Account bypass")
    except ValueError:pass
    # Missed word is removed from personalized until sufficient vocab-course corrections.
    with server.conn() as db:
        bad=vocab.answer(db,u1,{"id":candidate["id"],"direction":"target-gr","selected":"WRONG","lang":"ru"})
        assert not bad["correct"] and bad["missDebt"]>0
        assert personalized.progress_summary(db,u1)["needsReview"]==1
    assert not any(x["id"]==cid for x in qs(u1,study="personalized"))
    with server.conn() as db:
        for _ in range(2):
            vocab.answer(db,u1,{"id":candidate["id"],"direction":"target-gr","selected":candidate["gr"],"lang":"ru"})
    assert any(x["id"]==cid for x in qs(u1,study="personalized"))
    # Dialogue cards are all Greek: 1 to 3 gaps, 8 unique answers, rest distractors.
    import dialogues_extra
    assert len(dialogues.CARDS)==20 and len(dialogues_extra.CARDS)==80
    for card in dialogues.CARDS+dialogues_extra.CARDS:
        assert len(card["bank"])==8 and len(set(card["bank"]))==8
        assert 1<=len(card["gaps"])<=3
        assert all(g in card["bank"] for g in card["gaps"])
    dialogue=next(q for q in qs(u1,types="dialogue") if q["kind"]=="dialogue" and len(q["dialogueGaps"])==2)
    assert dialogue["gapIndices"]==[0,1] and len(dialogue["choices"])==8
    assert all(not key in dialogue for key in ("choicesEn","promptEn"))
    original=server.BY_ID[dialogue["id"]]
    assert server.mark(u1,{"id":dialogue["id"],"direction":"gap0","selected":original["gaps"][0],"lang":"ru"})["correct"]
    assert not server.mark(u1,{"id":dialogue["id"],"direction":"gap1","selected":"λάθος","lang":"ru"})["correct"]
    weak=qs(u1,types="dialogue",mode="weak")
    matching=[q for q in weak if q["id"]==dialogue["id"]]
    assert len(matching)==1 and matching[0]["gapIndices"]==[1],matching
    # Language invariant: dialogue answers stay raw Greek in every language, graded without language suffix.
    for lang in ("ru","en","zh","ar","es","pt"):
        question=server.make_quiz(u1,{"scope":["pages"],"types":["dialogue"],"from":["1"],"to":["56"],"lang":[lang],"count":["20"]})["questions"][0]
        assert question["choices"] and question["dialogueLines"] and "choicesEn" not in question
        book=server.make_quiz(u1,{"scope":["pages"],"types":["word"],"from":["1"],"to":["56"],"lang":[lang],"count":["20"]})["questions"]
        assert book
        if lang!="en":
            assert any(q.get("promptEn") for q in book if q["direction"]=="ru-gr")
            assert all(len(q["choicesEn"])==8 for q in book if q["direction"]=="gr-ru")
        else:
            assert all("promptEn" not in q and "choicesEn" not in q for q in book)
        verbs=server.make_quiz(u1,{"scope":["verbs"],"types":["verb"],"lang":[lang],"count":["25"]})["questions"]
        assert all(len(q["choices"])==8 and len(q["phraseChoices"])==len(q["phraseChoicesEn"])==8 for q in verbs)
    # Past stats, answer raw values, and SQLite DB records all still work.
    with server.conn() as db:
        assert db.execute("pragma quick_check").fetchone()[0]=="ok"
        attempts=db.execute("SELECT COUNT(*) FROM attempts WHERE user_id=?",(u1,)).fetchone()[0]
        assert attempts>=3
    print("PASS: personalized unique learned words, per-account authorization, unfinished weak exclusion and recovery")
    print("PASS: 100 Greek-only 1–3 gap dialogues, eight Greek choices, gap-level persistence and weak review")
    print("PASS: RU/EN/ZH/AR/ES/PT textbook hints metadata, 8-choice verbs, user isolation, existing stats")
    print("PASS: isolated SQLite quick_check and prior API semantics")
