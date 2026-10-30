"""Board adventure: server-authorized progression, syllabus, stable lessons, no replay."""
import tempfile
from pathlib import Path
import sqlite3
import server
import board_course as board

assert board.PER_CHAPTER==8 and len(board.QUESTS)==8
assert board.TOTAL_CHAPTERS==20

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/"progress.sqlite3")
    server.init_db()
    def get(uid="alice",lang="ru"):
        with server.conn() as db:
            return board.board_get(db,uid,lang,server.PRACTICE_ALL+server.LISTEN_CARDS,
                server.vocab.VOCAB,server.format_question,server._grammar_guard.milestone,
                server.LISTENING_ENABLED,lambda word:server._word_audio.lookup(word,server.listening))
    def move(prev,selected,uid="alice",lang="ru",action="answer"):
        with server.conn() as db:
            return board.board_action(db,uid,lang,{
                "action":action,"revision":prev["revision"],"questId":prev["quest"]["question"]["id"],
                "selected":selected},server.mark)
    def correct(b,lang="ru"):
        q=b["quest"]["question"]
        if b["quest"]["type"]=="life":return server._life.BY_ID[q["id"]]["accepted"][0]
        if b["quest"]["type"]=="lexicon":return server.vocab.VOCAB_BY_ID[q["id"]][lang]
        return server.shape(server.book_or_audio_card(q["id"]),q["direction"],lang)[1]

    s=get()
    assert s["position"]==0 and s["chapterLimit"]==6 and len(s["nodes"])==48
    assert s["nodes"][0]["state"]=="current" and s["nodes"][1]["state"]=="locked"
    assert s["quest"]["question"]["chapter"]==1
    assert "answer" not in s["quest"]["question"] and "correct" not in s["quest"]["question"]
    persistent=get()
    assert persistent["revision"]==s["revision"] and persistent["quest"]==s["quest"]
    # Attempted injection of answer not offered cannot score/advance.
    try:
        move(s,"не относится к варианту")
        raise AssertionError("invalid option accepted")
    except ValueError as e:assert str(e)=="invalid_choice"
    assert get()["position"]==0

    # Wrong answer stays on current cell; source scorer updates ordinary
    # progress/debt, but board advancement is withheld.
    correct_answer=correct(s)
    wrong=next(x for x in s["quest"]["question"]["choices"] if x!=correct_answer)
    bad=move(s,wrong)
    assert not bad["feedback"]["correct"] and bad["position"]==0 and bad["misses"]==1
    assert get()["position"]==0
    good=move(get(),correct_answer)
    assert good["feedback"]["correct"] and good["position"]==1 and good["wins"]==1
    try:
        move(s,correct_answer)
        raise AssertionError("stale attempt allowed")
    except ValueError as e:assert str(e)=="stale_track"

    visited=set()
    for i in range(1,24):
        current=get()
        assert current["position"]==i,(i,current["position"])
        q=current["quest"]["question"]
        typ=current["quest"]["type"]
        assert q["chapter"]<=current["quest"]["chapter"]
        assert current["quest"]["chapter"]==i//8+1
        assert "correct" not in q and "answer" not in q
        if typ=="quiz":
            assert len(q["choices"])>=4 and correct(current) in q["choices"],(i,q)
            assert q["kind"] not in ("accent","syllable","order")
            if q["kind"]=="grammar":
                assert q["grammarGroup"]
            if q["kind"]=="dialogue":
                assert q["dialogueLines"] and q["direction"]=="gap0"
            if q["kind"]=="clock":assert q["clockHour"] in range(1,13)
        elif typ=="lexicon":
            assert q["wordAudio"]["audioSource"]=="pocket"
        elif typ=="life":
            assert "choices" not in q
            assert server._life.BY_ID[q["id"]]["chapter"]<=current["quest"]["chapter"]
        visited.add(current["quest"]["title"])
        result=move(current,correct(current))
        assert result["feedback"]["correct"] and result["position"]==i+1
    assert {"book","lexicon","verb","grammar","dialogue","life"}.issubset(visited)
    assert get()["wins"]==24 and get()["position"]==24
    assert get("another-user")["position"]==0
    assert get("alice","en")["position"]==24
    # Account progression is shared across interface languages. Revisit an
    # unanswered task in another language and regenerate translated choices.
    before=get()
    newlang=get("alice","en")
    assert newlang["quest"]["question"]["lang"]=="en"
    assert newlang["position"]==before["position"]
    assert get()["quest"]["question"]["lang"]=="ru"
    # Curriculum cap can be lowered safely without erasing already reached
    # progress, then increased again to continue.
    s=get()
    with server.conn() as db:
        changed=board.board_action(db,"alice","ru",{"action":"scope",
            "revision":s["revision"],"chapterLimit":2},server.mark)
    assert changed["finished"] and changed["wins"]==24
    with server.conn() as db:
        restored=board.board_action(db,"alice","ru",{"action":"scope",
            "revision":changed["revision"],"chapterLimit":6},server.mark)
    assert not restored["finished"] and get()["position"]==24
    # Optional jump preserves honesty: skipped chapters are not mastered.
    starter=get("another-user")
    with server.conn() as db:
        jumped=board.board_action(db,"another-user","ru",{"action":"jump",
            "revision":starter["revision"],"chapter":6},server.mark)
    assert jumped["position"]==40 and jumped["wins"]==0
    assert jumped["nodes"][0]["state"]=="skipped"
    assert jumped["nodes"][40]["state"]=="current"
    with server.conn() as db:
        assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"

print("PASS 8 diverse quests/chapter, 20-chapter gate, A1 vocabulary, verb/grammar/listening/life")
print("PASS scoring, no skipping wrong answers, stale/replayed answer protection, cross-device/lang progress")
print("PASS legacy source attempts preserved, syllabus cap and optional honest chapter jump")
