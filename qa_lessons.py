"""Account-owned eight-lesson rounds, exact stats, weak backlog and safe v1 migration."""
import datetime as dt
import tempfile
from pathlib import Path

import board_course as board
import server
import study_tracks as tracks

assert board.PER_CHAPTER==8 and len(board.FAMILIES)==8
assert board.MAX_CHAPTER==20

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/"test.sqlite3")
    server.init_db()
    args=(server.PRACTICE_ALL+server.LISTEN_CARDS,server.vocab.VOCAB,
          server.format_question,server._grammar_guard.milestone,
          server.LISTENING_ENABLED,lambda gr:server._word_audio.lookup(gr,server.listening))

    def get(uid="player",lang="ru"):
        with server.conn() as db:return board.board_get(db,uid,lang)
    def action(message,uid="player",lang="ru"):
        with server.conn() as db:
            return board.board_action(db,uid,lang,message,server.mark,args)
    def correct(q):
        if q["type"]=="life":return server._life.BY_ID[q["id"]]["accepted"][0]
        if q["type"]=="lexicon":return server.vocab.VOCAB_BY_ID[q["id"]][q["lang"]]
        return server.shape(server.book_or_audio_card(q["id"]),q["direction"],q["lang"])[1]

    initial=get()
    assert initial["schema"]==2 and initial["round"]==1
    assert initial["chapterLimit"]==6
    assert len(initial["nodes"])==8 and initial["nodes"][0]["state"]=="current"
    assert all(x["state"]=="locked" and "name" not in x and "family" not in x
               for x in initial["nodes"][1:])
    assert initial["lesson"] is None and initial["roundStats"]["attempts"]==0
    assert initial["backlog"]["due"]==0
    assert get("other")["position"]==0

    # New users can explicitly start with the last studied chapter without
    # claiming every skipped chapter is mastered.
    other=get("other")
    moved=action(dict(action="jump",revision=other["revision"],chapter=3),uid="other")
    assert moved["position"]==16 and moved["totals"]["lessons"]==0
    assert moved["round"]==3 and moved["nodes"][0]["state"]=="current"
    assert moved["canJump"] is False

    started=action(dict(action="lesson_start",revision=initial["revision"]))
    assert started["lesson"]["count"]>=10 and started["lesson"]["at"]==0
    assert started["lesson"]["question"]["kind"] in ("word","phrase","number","sentence")
    assert "answer" not in started["lesson"]["question"]
    assert all(x["state"]=="locked" and "name" not in x
               for x in started["nodes"][1:])
    assert get()["lesson"]["question"]==started["lesson"]["question"]

    # The FIRST submitted answer is final. A wrong answer advances
    # immediately, remains wrong in stats and enters the long-term backlog.
    q=started["lesson"]["question"]
    wrong=next(o for o in q["choices"] if o!=correct(q))
    failed=action(dict(action="answer",revision=started["revision"],
                       lessonIndex=0,questionId=q["id"],selected=wrong))
    assert failed["feedback"]["correct"] is False
    assert failed["lesson"]["at"]==1 and failed["lesson"]["errors"]==1
    assert failed["lesson"]["attempts"]==1
    assert failed["backlog"]["due"]==1 and failed["backlog"]["items"][0]["errors"]==1
    assert failed["roundStats"]["lessonsCompleted"]==0
    assert get()["lesson"]["question"]["id"]!=q["id"]
    # Revealed correct answer cannot be resubmitted for free credit,
    # even with the new revision: the current question id changed.
    try:
        action(dict(action="answer",revision=failed["revision"],
                    lessonIndex=0,questionId=q["id"],selected=correct(q)))
        raise AssertionError("revealed correct option accepted")
    except ValueError as ex:assert str(ex)=="stale_track"
    try:
        action(dict(action="answer",revision=started["revision"],
                    lessonIndex=0,questionId=q["id"],selected=correct(q)))
        raise AssertionError("replayed answer accepted")
    except ValueError as ex:assert str(ex)=="stale_track"
    with server.conn() as db:
        saved,_,_=board._load(db,"player")
        saved["active"]["lastAt"]=(dt.datetime.now(dt.timezone.utc)-dt.timedelta(seconds=50)).isoformat(timespec="seconds")
        tracks._save(db,"player","board","shared",saved,failed["revision"])
    failed=get()
    next_q=failed["lesson"]["question"]
    passed=action(dict(action="answer",revision=failed["revision"],
                       lessonIndex=0,questionId=next_q["id"],selected=correct(next_q)))
    assert passed["lesson"]["at"]==2 and passed["lesson"]["activeSeconds"]>=45
    assert passed["backlog"]["due"]==1 # review scheduled in later lesson

    # Pause, resume and complete all eight full lessons in the first round.
    paused=action(dict(action="pause",revision=passed["revision"]))
    assert paused["lesson"]["paused"] is True
    saved=get()
    assert saved["lesson"]["paused"]
    assert saved["lesson"]["at"]==2
    resumed=action(dict(action="lesson_start",revision=saved["revision"]))
    assert not resumed["lesson"]["paused"]

    attempts=2
    completed_lengths=[]
    while True:
        state=get()
        if state["roundReady"] or state["finished"]:break
        if state["lesson"] is None:
            state=action(dict(action="lesson_start",revision=state["revision"]))
        lesson=state["lesson"];q=lesson["question"]
        assert lesson["count"]>=10
        assert lesson["index"]==state["position"]
        # The final question of lesson 1 is intentionally wrong: it must
        # *still* finalize that lesson and expose Finish lesson in the UI.
        fail_final=(lesson["index"]==0 and lesson["at"]==lesson["count"]-1)
        selected=(next(x for x in q["choices"] if x!=correct(q))
                  if fail_final else correct(q))
        result=action(dict(action="answer",revision=state["revision"],
                  lessonIndex=lesson["index"],questionId=q["id"],selected=selected))
        assert result["feedback"]["correct"] is (not fail_final),(lesson["index"],q["id"],result["feedback"])
        if result["feedback"].get("lessonComplete"):
            completed_lengths.append(result["feedback"]["lessonComplete"]["total"])
            if fail_final:
                assert result["lesson"] is None and result["position"]==1
        attempts+=1
        assert attempts<160
    assert len(completed_lengths)==8,completed_lengths
    assert sum(completed_lengths)>=90,completed_lengths
    assert state["position"]==8 and state["roundReady"]
    assert state["roundStats"]["chapter"]==1
    assert state["roundStats"]["finished"]
    assert state["roundStats"]["lessonsCompleted"]==8
    assert state["roundStats"]["errors"]==2
    assert state["roundStats"]["attempts"]==sum(completed_lengths)
    assert state["roundStats"]["activeSeconds"]>=45
    assert len(state["roundStats"]["lessons"])==8
    assert state["nodes"][-1]["state"]=="completed"
    assert state["backlog"]["due"]<=1  # reviewed errors may have been resolved
    try:
        action(dict(action="lesson_start",revision=state["revision"]))
        raise AssertionError("round report bypassed")
    except ValueError as ex:assert str(ex)=="round_report_not_seen"
    next_round=action(dict(action="continue_round",revision=state["revision"]))
    assert not next_round["roundReady"] and next_round["round"]==2
    assert next_round["nodes"][0]["state"]=="current"
    assert all(x["state"]=="locked" and "name" not in x for x in next_round["nodes"][1:])
    assert next_round["totals"]["lessons"]==8
    assert next_round["totals"]["errors"]==2

    # V1 1-question cell progress is archived, not magically converted into
    # lessons. Old account and legacy scorer records remain unchanged.
    with server.conn() as db:
        old=dict(position=19,wins=17,misses=2,skips=1,chapterLimit=6,
                 hasStarted=True,pending=dict(question=dict(id="w014",lang="ru")))
        tracks._save(db,"v1","board","shared",old,0)
    migrated=get("v1")
    assert migrated["position"]==16
    assert migrated["totals"]["lessons"]==0 and migrated["nodes"][0]["state"]=="current"
    with server.conn() as db:
        record,_,_=board._load(db,"v1")
        assert record["legacyBoard"]==old and record["schema"]==2
        assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"

print("PASS eight 10–14-question lessons per round, locked titles, server-timed statistics")
print("PASS final wrong answer advances once; delayed review backlog, pause/resume, round report")
print("PASS progression gates, replay resistance, optional honest jump, v1 archive migration")
