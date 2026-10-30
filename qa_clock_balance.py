"""Regression: mixed chapter selection must not drown students in clocks."""
import collections
import random
import tempfile
from pathlib import Path
import server
from quiz_clock_balance import balance

ALL_KINDS="word,number,phrase,sentence,dialogue,accent,article,order,grammar,clock"

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/"test.sqlite3")
    server.init_db()

    def quiz(user,seed,chapters,types=ALL_KINDS,scope="chapters",**extra):
        random.seed(seed)
        query={
            "scope":[scope],
            "chapters":[chapters],
            "types":[types],
            "lang":["ru"],
            "count":["60"],
            **{k:[str(v)] for k,v in extra.items()}
        }
        return server.make_quiz(user,query)

    for chapters in ("1,2,3,4,5,6","6"):
        counts=[]
        for seed in range(15):
            result=quiz("new",seed,chapters)
            cards=result["questions"]
            n=sum(c["kind"]=="clock" for c in cards)
            counts.append(n)
            assert len(cards)==60,(chapters,seed,len(cards))
            if chapters=="1,2,3,4,5,6":
                assert n==6,(chapters,seed,n)
            else:
                # One chapter has too few distinct non-clock semantic targets
                # to supply sixty unique questions; filling is intentional.
                assert 6<=n<=25,(chapters,seed,n)
            assert result["available"]>60,(chapters,result["available"])
            assert len({c["semanticId"] for c in cards})==60
            assert all(c["chapter"] in set(map(int,chapters.split(","))) for c in cards)
        assert any(n>0 for n in counts),(chapters,counts)
        print("MIXED",chapters,"clock counts",counts)

    for seed in range(4):
        cards=quiz("new",seed,"6","clock")["questions"]
        assert len(cards)==60 and all(c["kind"]=="clock" for c in cards)
        cards=quiz("new",seed,"1,2,3,4,5","clock")["questions"]
        assert not cards
        cards=quiz("new",seed,"6","word,dialogue,article,grammar")["questions"]
        assert cards and all(c["kind"]!="clock" for c in cards)
        random.seed(seed)
        pages=server.make_quiz("new",{"scope":["pages"],"from":["1"],"to":["79"],
            "types":[ALL_KINDS],"lang":["ru"],"count":["60"]})["questions"]
        assert len(pages)==60 and sum(c["kind"]=="clock" for c in pages)<=6

    # If a small selected range cannot supply enough non-clock questions,
    # do not shorten the session just to respect the soft 10% quota.
    fake=lambda kind,n:[(dict(id=f"{kind}{i}",kind=kind),"read",0) for i in range(n)]
    picked=balance(fake("word",2)+fake("clock",30),20)
    assert len(picked)==20 and sum(c["kind"]=="clock" for c,_,_ in picked)==18
    assert len(balance(fake("clock",40),20))==20
    assert not balance([],20)
    assert len(balance(fake("word",20),20))==20

    # Weak review: a learner who failed many clocks should see the due
    # questions, not lose them to a cap intended for regular mixed lessons.
    uid="weak_clock_learner"
    for card in server.CLOCK_ALL[:12]:
        server.mark(uid,{"id":card["id"],"direction":"read","selected":"wrong","lang":"ru"})
    weak=quiz(uid,9,"6","clock,word",mode="weak")["questions"]
    assert len(weak)==12 and all(x["kind"]=="clock" for x in weak)
    with server.conn() as db:
        assert db.execute("pragma quick_check").fetchone()[0]=="ok"

print("PASS: 10% maximum clocks in full mixed batch, 100% clock-only, no lost weak cards")
