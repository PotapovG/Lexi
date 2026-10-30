"""Greek Life curriculum scope, learner personalization and typed explanations."""
import sqlite3
import tempfile
from pathlib import Path
import server
import greek_life as life
import study_tracks
import practice_games

assert life.validate()==11
assert all(any(x["chapter"]==n for x in life.SCENES) for n in (1,2,3,4,6,7,8,9,11,14,16))

with tempfile.TemporaryDirectory() as directory:
    server.DB=str(Path(directory)/"progress.sqlite3")
    server.init_db()

    def overview(uid="alice",lang="ru"):
        with server.conn() as db:return life.current_settings(db,uid,lang)
    def configure(level,uid="alice",lang="ru"):
        state=overview(uid,lang)
        with server.conn() as db:
            return life.update_settings(db,uid,lang,{
                "revision":state["revision"],"maxChapter":level})
    def scene(sid,uid="alice",lang="ru"):
        with server.conn() as db:return life.scene_get(db,uid,lang,sid)
    def answer(sid,phrase,uid="alice",lang="ru"):
        data=scene(sid,uid,lang)
        with server.conn() as db:
            return life.scene_answer(db,uid,lang,{
                "id":sid,"answer":phrase,"revision":data["revision"]})

    first=overview()
    assert first["maxChapter"]==6
    assert {x["id"] for x in first["available"] if x["type"]=="activity"}=={"route"}
    assert {x["id"] for x in first["available"] if x["type"]=="roleplay"}=={
        "meet","home_city","family","languages","ticket"}
    assert first["observations"]==0
    assert scene("ticket")["hint"] is not None
    for cid in ("groceries","clothes","cafe","plans"):
        try:
            scene(cid)
            raise AssertionError("future chapter exposed "+cid)
        except ValueError as err:assert str(err)=="chapter_not_unlocked"

    with server.conn() as db:
        try:
            life.ensure(db,"alice","ru","periptero")
            raise AssertionError("market unlocked before chapter8")
        except ValueError as err:assert str(err)=="chapter_not_unlocked"
        try:
            life.ensure(db,"alice","ru","likes")
            raise AssertionError("subjunctive before chapter16")
        except ValueError as err:assert str(err)=="chapter_not_unlocked"

    wrong=answer("home_city","Μένω Λευκωσία")
    assert not wrong["correct"] and "артикль" in wrong["explanation"]
    assert wrong["answer"]=="Μένω στη Λευκωσία."
    correct=answer("home_city","μένω στην λευκωσία")
    assert correct["correct"] and correct["translation"]=="Я живу в Никосии."
    assert overview()["available"][1]["attempts"]==2
    assert scene("home_city")["hint"] is None
    assert answer("meet","Είμαι η Μαρία")["correct"]
    assert answer("ticket","Ένα εισιτήριο για τη Λεμεσό")["correct"]

    configure(1)
    assert {x["id"] for x in overview()["available"]}=={"meet"}
    configure(8)
    scenarios={x["id"] for x in overview()["available"]}
    assert "periptero" in scenarios and "groceries" in scenarios
    assert "likes" not in scenarios and "cafe" not in scenarios
    with server.conn() as db:
        stage=life.ensure(db,"alice","ru","periptero")
        assert stage==8
        assert "beef" not in [x["id"] for x in practice_games.store_get(db,"alice","ru",stage)["items"]]
        assert set(x["name"] for x in study_tracks.route_get(db,"alice","ru",stage)["stops"]).issubset(
            {"Σχολείο","Κέντρο","Πανεπιστήμιο","Σπίτι","Τράπεζα"})
    configure(14)
    assert "cafe" in {x["id"] for x in overview()["available"]}
    assert "likes" not in {x["id"] for x in overview()["available"]}
    assert answer("cafe","Θα ήθελα έναν καφέ, παρακαλώ")["correct"]
    configure(16)
    assert {"plans","likes"}.issubset({x["id"] for x in overview()["available"]})
    miss=answer("plans","Μου αρέσει περπατάω")
    assert not miss["correct"] and "να" in miss["explanation"]
    assert answer("plans","Μου αρέσει να περπατάω")["correct"]
    with server.conn() as db:
        assert life.ensure(db,"alice","ru","likes")==16
        assert "beef" in [x["id"] for x in practice_games.store_get(db,"alice","ru",16)["items"]]

    # Existing main-quiz evidence and authored vocabulary course results adapt
    # the same scene from guided to independent, but never unlock beyond scope.
    with server.conn() as db:
        for _ in range(12):
            db.execute("""INSERT INTO attempts(user_id,card_key,kind,unit,correct,created_at)
                VALUES(?,?,?,?,?,?)""",("bob","w001:gr-ru","word",2,1,"2026-10-30"))
    assert scene("home_city","bob")["difficulty"]=="independent"
    assert scene("home_city","bob")["hint"] is None
    assert overview("bob")["maxChapter"]==6
    assert overview("alice","en")["maxChapter"]==6
    with server.conn() as db:
        assert db.execute("pragma quick_check").fetchone()[0]=="ok"
print("PASS: staged chapters 1-20, no beyond-syllabus scenes or market items")
print("PASS: 11 roleplays + 3 gated activities, per-account skill and error explanations")
