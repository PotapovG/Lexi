"""End-to-end state machine regressions for new independent learning tracks."""
import os
import sqlite3
import tempfile

import server
import study_tracks as tracks

assert tracks.validate()>500
mix={k:sum(tracks._word_class(w)==k for w in tracks.WORDS[:30])
     for k in ("noun","verb","adjective","other")}
assert all(n>=4 for n in mix.values()),mix
assert tracks._word_class({"gr":"εγώ","en":"I"})=="other"
assert tracks._word_class({"gr":"αντίο","en":"goodbye"})=="other"
assert tracks._word_class({"gr":"καλημέρα","en":"good morning"})=="other"

with tempfile.TemporaryDirectory() as folder:
    server.DB=os.path.join(folder,"test.sqlite3")
    server.init_db()
    def get(user="first",lang="ru"):
        with server.conn() as db:return tracks.anki_get(db,user,lang)
    def act(s,action,**kwargs):
        with server.conn() as db:
            return tracks.anki_action(db,"first","ru",{
                "revision":s["revision"],"action":action,**kwargs})
    s=get()
    assert s["phase"]=="preview" and s["at"]==1 and s["card"]["translation"]
    assert "options" not in s
    first_card=s["card"]["id"]
    for i in range(30):
        assert s["phase"]=="preview",s
        s=act(s,"advance")
    assert s["phase"]=="quiz" and s["target"]==30
    assert "translation" not in s["card"]
    assert "options" in s and len(set(s["options"]))==4
    assert first_card in tracks.WORD_IDS[:30]
    assert get()["revision"]==s["revision"]

    try:
        act({**s,"revision":s["revision"]-1},"answer",
            cardId=s["card"]["id"],selected=s["options"][0])
        raise AssertionError("stale answers were allowed")
    except ValueError as e:
        assert str(e)=="stale_track"

    # Fail the first item deliberately, then solve every requeued item;
    # the cohort must not advance before all thirty are correct.
    target=tracks.BY_ID[s["card"]["id"]]["ru"]
    bad=next(x for x in s["options"] if tracks._normalized(x)!=tracks._normalized(target))
    s=act(s,"answer",cardId=s["card"]["id"],selected=bad)
    assert s["feedback"]["correct"] is False and s["misses"]==1 and s["phase"]=="quiz"
    # Simulate reload after an incorrect answer; queue must persist.
    assert get()["revision"]==s["revision"]
    while s["phase"]=="quiz":
        source=tracks.BY_ID[s["card"]["id"]]
        selected=next(x for x in s["options"] if tracks._normalized(x)==tracks._normalized(source["ru"]))
        s=act(s,"answer",cardId=s["card"]["id"],selected=selected)
        assert s["feedback"]["correct"]
    assert s["phase"]=="milestone" and s["learned"]==30 and s["nextPhase"]=="preview"
    s=act(s,"continue")
    assert s["phase"]=="preview" and s["batch"]==2 and s["card"]["id"]!=first_card
    for i in range(30):s=act(s,"advance")
    assert s["phase"]=="quiz"
    while s["phase"]=="quiz":
        source=tracks.BY_ID[s["card"]["id"]]
        selected=next(x for x in s["options"] if tracks._normalized(x)==tracks._normalized(source["ru"]))
        s=act(s,"answer",cardId=s["card"]["id"],selected=selected)
    assert s["phase"]=="milestone" and s["learned"]==60 and s["nextPhase"]=="review"
    s=act(s,"continue")
    assert s["phase"]=="review" and s["target"]==60 and s["round"]==1
    review_seen=set()
    while s["phase"]=="review":
        review_seen.add(s["card"]["id"])
        source=tracks.BY_ID[s["card"]["id"]]
        selected=next(x for x in s["options"] if tracks._normalized(x)==tracks._normalized(source["ru"]))
        s=act(s,"answer",cardId=s["card"]["id"],selected=selected)
    assert len(review_seen)==60 and s["phase"]=="milestone" and s["learned"]==60
    s=act(s,"continue")
    assert s["phase"]=="preview" and s["batch"]==3 and s["at"]==1
    assert get("second")["phase"]=="preview" and get("second")["learned"]==0
    assert get("first","en")["phase"]=="preview" and get("first","en")["learned"]==0

    with server.conn() as db:
        first_route=tracks.route_get(db,"first","ru")
        scene=tracks._scene(0)
        assert first_route["bus"]==scene["bus"] and "expected" not in first_route
        wrong=tracks.route_action(db,"first","ru",{
            "revision":first_route["revision"],"answers":{k:"not greek" for k in first_route["fields"]}})
        assert not wrong["feedback"]["correct"] and wrong["completed"]==0
        assert all(not x for x in wrong["feedback"]["fields"].values())
        db.commit()
        # Greek user input without tonos is still accepted, including bus number words.
        expected=scene["expected"]
        answer={k:tracks._normalized(v) for k,v in expected.items()}
        correct=tracks.route_action(db,"first","ru",{
            "revision":wrong["revision"],"answers":answer})
        assert correct["feedback"]["correct"] and correct["completed"]==1
        assert correct["feedback"]["translationLang"]=="ru"
        db.commit()
        assert correct["bus"]!=first_route["bus"]
        try:
            tracks.route_action(db,"first","ru",{"revision":wrong["revision"],"answers":answer})
            raise AssertionError("stale route revision accepted")
        except ValueError as e:assert str(e)=="stale_track"
        assert tracks.route_get(db,"second","ru")["completed"]==0
        assert db.execute("pragma quick_check").fetchone()[0]=="ok"
    print("PASS mastery 30/30 gate, next 30, surprise cumulative 60, missed replay")
    print("PASS persisted revision/queue, independent account/lang, route typing and validation")
