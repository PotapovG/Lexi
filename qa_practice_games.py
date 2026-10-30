"""Validated likes grammar and Periptero ordering as isolated user-owned tracks."""
import tempfile
from pathlib import Path
import server
import study_tracks as base
import practice_games as games

assert games.validate()==(280,12)
assert games._like_scene(1)["expected"]=="Δεν μου αρέσει να διαβάζω."
assert games._like_scene(2)["expected"]=="σου αρέσει να διαβάζεις."
assert games._like_scene(4)["expected"]=="του αρέσει να διαβάζει."
assert games._like_scene(6)["expected"]=="της αρέσει να διαβάζει."
assert games._like_scene(8)["expected"]=="μας αρέσει να διαβάζουμε."
assert games._like_scene(10)["expected"]=="σας αρέσει να διαβάζετε."
assert games._like_scene(12)["expected"]=="τους αρέσει να διαβάζουν."

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/"test.sqlite3")
    server.init_db()
    def likes_get(uid="alice",lang="ru"):
        with server.conn() as db:return games.likes_get(db,uid,lang)
    def likes_action(uid,lang,body):
        with server.conn() as db:return games.likes_action(db,uid,lang,body)
    def shop_get(uid="alice",lang="ru"):
        with server.conn() as db:return games.store_get(db,uid,lang)
    def shop_action(uid,lang,body):
        with server.conn() as db:return games.store_action(db,uid,lang,body)

    s=likes_get()
    assert s["step"]==1 and "expected" not in s and s["lemma"]=="διαβάζω"
    wrong=likes_action("alice","ru",dict(revision=s["revision"],action="submit",answer="Δεν του αρέσει να διαβάζω"))
    assert not wrong["feedback"]["correct"] and wrong["step"]==1 and wrong["misses"]==1
    assert "expected" in wrong["feedback"]
    assert likes_get()["revision"]==wrong["revision"]
    try:
        likes_action("alice","ru",dict(revision=s["revision"],action="submit",answer="μου αρέσει να διαβάζω"))
        raise AssertionError("stale grammar state accepted")
    except ValueError as e:assert str(e)=="stale_track"
    for index in range(280):
        expected=games._like_scene(index)["expected"]
        saved=likes_get()
        assert saved["step"]==index+1
        reply=likes_action("alice","ru",dict(revision=saved["revision"],action="submit",
             answer=base._normalized(expected)))
        assert reply["feedback"]["correct"],(index,reply)
    assert likes_get()["completed"] is True
    try:
        likes_action("alice","ru",dict(revision=likes_get()["revision"],action="submit",
                                answer="μου αρέσει να διαβάζω"))
        raise AssertionError("grammar completion gate failed")
    except ValueError as e:assert str(e)=="already_finished"
    reset=likes_action("alice","ru",dict(revision=likes_get()["revision"],action="restart"))
    assert reset["step"]==1
    assert likes_get("bob")["step"]==1 and likes_get("alice","en")["step"]==1

    scene=shop_get()
    assert len(scene["items"])==4 and scene["bought"]==[]
    assert [p["id"] for p in scene["items"]]==["apple","milk","water","beef"]
    assert "expected" not in str(scene)
    for item in games._shopping_scene(0):
        current=shop_get()
        incorrect=shop_action("alice","ru",dict(revision=current["revision"],action="buy",
            productId=item[0],phrase="Θα ήθελα ένα βιβλίο"))
        assert not incorrect["feedback"]["correct"]
        assert item[0] not in incorrect["bought"]
        correct=shop_action("alice","ru",dict(revision=incorrect["revision"],action="buy",
            productId=item[0],phrase="Μπορώ να έχω "+base._normalized(item[3])+" παρακαλώ"))
        assert correct["feedback"]["correct"] and item[0] in correct["bought"]
        assert correct["feedback"]["expected"]=="Θα ήθελα "+item[3]+", παρακαλώ."
        assert correct["feedback"]["productId"]==item[0]
    complete=shop_get()
    assert complete["stage"]=="complete" and len(complete["bought"])==4
    try:
        shop_action("alice","ru",dict(revision=complete["revision"],action="buy",
            productId="apple",phrase="Θα ήθελα ένα μήλο"))
        raise AssertionError("re-buy accepted after checkout")
    except ValueError as e:assert str(e)=="already_finished"
    next_round=shop_action("alice","ru",dict(revision=complete["revision"],action="next"))
    assert next_round["round"]==2 and next_round["bought"]==[]
    assert shop_get("bob")["round"]==1
    assert shop_get("alice","en")["round"]==1
    with server.conn() as db:assert db.execute("pragma quick_check").fetchone()[0]=="ok"

print("PASS likes 280 positive/negative verb/noun constructions and seven pronoun forms")
print("PASS Periptero basket of four, errors cannot buy, restart and account/device persistence")
