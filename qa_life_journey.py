"""Greek Life one-button adventure: ordering, scope, safe skip, adaptive activities."""
import tempfile
from pathlib import Path
import server
import greek_life as life
import study_tracks as tracks
import practice_games as games

with tempfile.TemporaryDirectory() as tmp:
    server.DB=str(Path(tmp)/"test.sqlite3")
    server.init_db()
    uid="adventure-user"
    with server.conn() as db:
        home=life.current_settings(db,uid,"ru")
        assert home["maxChapter"]==6
        assert home["recommended"]=="meet"
        assert home["totalExperiences"]==6 and home["completedExperiences"]==0
        # A different unconstrained sentence is not a demonstrably wrong
        # Greek construction; no false penalty.
        phrase=life.scene_get(db,uid,"ru","meet")
        data=life.scene_answer(db,uid,"ru",{"id":"meet","answer":"Ονομάζομαι Μαρία.",
                        "revision":phrase["revision"]})
        db.commit()
        assert not data["correct"] and data["unverified"] and data["attempts"]==1
        assert life.current_settings(db,uid,"ru")["available"][0]["errors"]==0
        skipped=life.skip_scene(db,uid,"ru",{
            "id":"meet","revision":data["revision"]})
        db.commit()
        assert skipped["recommended"]=="home_city"
        assert skipped["completedExperiences"]==0
        assert life.scene_get(db,uid,"ru","meet")["attempts"]==1
        # All new scenes stay inside the chosen chapter and retry only
        # validated errors; the next experience is not chosen by the user.
        scene=life.scene_get(db,uid,"ru","home_city")
        bad=life.scene_answer(db,uid,"ru",{
            "id":"home_city","revision":scene["revision"],"answer":"Μένω Λευκωσία."})
        db.commit()
        assert not bad["correct"] and not bad["unverified"]
        assert "артикль" in bad["explanation"]
        assert life.current_settings(db,uid,"ru")["recommended"]=="home_city"
        correct=life.scene_answer(db,uid,"ru",{
            "id":"home_city","revision":bad["revision"],"answer":"Μένω στη Λευκωσία."})
        db.commit()
        assert correct["correct"]
        assert life.current_settings(db,uid,"ru")["completedExperiences"]==1
        assert life.current_settings(db,uid,"ru")["recommended"]!="home_city"

        cfg=life.current_settings(db,uid,"ru")
        cfg=life.update_settings(db,uid,"ru",{
            "revision":cfg["revision"],"maxChapter":8})
        db.commit()
        assert cfg["maxChapter"]==8 and "periptero" in [x["id"] for x in cfg["available"]]
        stage=life.ensure(db,uid,"ru","periptero")
        scene=games.store_get(db,uid,"ru",stage)
        bought=games.store_action(db,uid,"ru",{
            "revision":scene["revision"],"action":"buy","productId":"apple",
            "phrase":"Θέλω ένα μήλο, παρακαλώ."},stage)
        db.commit()
        assert bought["feedback"]["correct"] and bought["bought"]==["apple"]
        assert life.current_settings(db,uid,"ru")["recommended"]=="periptero"
        # Reopening on another device must land in the unfinished basket.
        assert games.store_get(db,uid,"ru",stage)["bought"]==["apple"]
        # Changing level doesn't let subsequent API calls bypass unit 8.
        cfg=life.current_settings(db,uid,"ru")
        life.update_settings(db,uid,"ru",{"revision":cfg["revision"],"maxChapter":6})
        db.commit()
        try:
            life.ensure(db,uid,"ru","periptero")
            raise AssertionError("market bypassed the chapter gate")
        except ValueError as e:assert str(e)=="chapter_not_unlocked"
        assert games.store_get(db,uid,"ru",8)["bought"]==["apple"]
        cfg=life.current_settings(db,uid,"ru")
        life.update_settings(db,uid,"ru",{"revision":cfg["revision"],"maxChapter":8})
        db.commit()
        assert life.current_settings(db,uid,"ru")["recommended"]=="periptero"
    print("PASS guided automatic one-tap journey, real progress-based next, unfinished basket")
    print("PASS no false penalty for unverified answers, skip is safe, chapter server gates")
