"""Issue #15: original 7x3 agenda within the existing grammar_fill quiz.

No time-mode, new route, screenshot/PDF content, or DB migration.
Exercises: 21 schedule-time, 7 day, 7 calendar date, 7 spoken time.
"""
from collections import Counter
from pathlib import Path
import random
import tempfile

import agenda_cards
import clock_cards
import cloze_meanings
import grammar2_cards
import server

days=agenda_cards.DAYS
cards=agenda_cards.CARDS
langs=agenda_cards.LANGS
assert len(days)==7 and all(len(day["events"])==3 for day in days)
assert len({e["time"] for d in days for e in d["events"]})==21
assert len(clock_cards.CARDS)==144 and server.CLOCK_COUNT==144
assert len(cards)==42 and len(grammar2_cards.CARDS)>=301  # added duration cards preserve schedule IDs
assert [c["id"] for c in grammar2_cards.CARDS[:259]]==[
    f"g2261021_{i:03d}" for i in range(1,260)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(260,302)
}
assert Counter(c["skill"] for c in cards)=={
    "time":21,"day":7,"date":7,"spoken":7
}
assert len({c["prompt"] for c in cards})==42
assert all(c["chapter"]==7 and c["curriculum_ready_unit"]==7 for c in cards)
assert all(c["kind"]=="grammar" and c["group"]=="schedule" for c in cards)
assert all(c["prompt"].count("___")==1 and c["prompt"].count("\n")>=3 for c in cards)
assert all("2026" in c["prompt"] for c in cards if c["skill"]!="spoken")
assert all(c["typedAnswer"]==(c["skill"] in ("time","spoken")) for c in cards)
assert all(len(c["options"])==len(set(c["options"]))==4 for c in cards)
assert len(server.vocab.VOCAB)==1700

# Clock/schedule are different questions in pre-existing modes. The
# 12-hour clock cannot by itself tell AM from PM; schedule cards always do.
assert clock_cards.expression(8,45)=="Είναι εννέα παρά τέταρτο."
at_one=[c for c in cards if c["eventTime"]=="13:00"]
assert at_one and any(c["skill"]=="time" and
    "στη μία το μεσημέρι" in c["acceptedForms"] for c in at_one)
assert any(c["correct"]=="στη μία το μεσημέρι" for c in cards)
assert all("στις μία" not in c.get("acceptedForms",[]) for c in cards)
assert all(c["correct"].startswith("στις ") or c["correct"].startswith("στη ")
           for c in cards if c["typedAnswer"])
# Explicit early-stage syllabus retains no new learner mode or kind.
assert all(c["id"] in server.GRAMMAR2_BY_ID for c in cards)
assert not any(c["kind"]=="agenda" for c in server.PRACTICE_ALL)

js=Path(__file__).with_name("app.js").read_text(encoding="utf-8")
css=Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
assert 'q.kind==="grammar"&&q.grammarGroup==="schedule"' in js
assert '#question-prompt.schedule-agenda' in css
assert 'white-space: pre-line' in css and 'overflow-wrap: anywhere' in css
assert '@media (max-width: 360px)' in css

with tempfile.TemporaryDirectory(prefix="lexi-agenda-") as tmp:
    old_db=server.DB
    old_pepper=server.auth.SECRET_FILE
    server.DB=str(Path(tmp)/"agenda.sqlite3")
    server.auth.SECRET_FILE=Path(tmp)/"login-pepper"
    try:
        server.init_db()
        attempts=0
        variants=0
        for card in cards:
            for lang in langs:
                question=server.format_question(card,"grammar_fill",lang)
                assert question["id"]==card["id"] and question["kind"]=="grammar"
                assert question["grammarGroup"]=="schedule"
                assert question["note"]==card[lang]
                assert question["prompt"]==card["prompt"]
                assert question["sourcePageVerified"] is False
                assert not any(key in question for key in (
                    "correct","acceptedForms","fullTranslations","grammarTip"))
                assert len(question["choices"])==(0 if card["typedAnswer"] else 4)
                if card["typedAnswer"]:
                    assert question["typedAnswer"] is True
                else:
                    assert set(question["choices"])==set(card["options"])
                user="ag-"+card["id"]+"-"+lang
                right=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                attempts+=1
                assert right["correct"] and right["answer"]==card["correct"]
                assert right["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                assert right["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert right["clozeTranslation"]==card["fullTranslations"][lang]
                assert right["clozeTranslationLang"]==lang
                wrong=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["options"][1]
                })
                attempts+=1
                assert not wrong["correct"] and wrong["missDebt"]==2
                assert wrong["answer"]==card["correct"] and wrong["explanation"]
                if card.get("acceptedForms") and len(card["acceptedForms"])>1:
                    for variant in card["acceptedForms"][1:]:
                        alt=server.mark(user,{
                            "id":card["id"],"direction":"grammar_fill",
                            "lang":lang,"selected":variant
                        })
                        attempts+=1
                        variants+=1
                        assert alt["correct"] and alt["acceptedVariant"]
                        assert variant in alt["clozeGreek"]

        # The old standalone chapter-6 clock is not changed.
        clock=clock_cards.CARDS[5]
        assert server.mark("clock-user",{
            "id":clock["id"],"direction":"read",
            "lang":"ru","selected":clock["gr"]
        })["correct"]
        attempts+=1
        # Typed time with only a 12h hour is ambiguous; 13:00 needs noon.
        one=next(c for c in cards if c["skill"]=="time" and c["eventTime"]=="13:00")
        bad=server.mark("ambiguous",{
            "id":one["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"στη μία"
        })
        assert not bad["correct"] and bad["missDebt"]==2
        attempts+=1
        sample=next(c for c in cards if c["skill"]=="time")
        wrong=server.mark("review-user",{
            "id":sample["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"στις 00:00"
        })
        attempts+=1
        assert not wrong["correct"] and wrong["missDebt"]==2
        weak=server.make_quiz("review-user",{
            "scope":["chapters"],"chapters":["7"],"types":["grammar"],
            "mode":["weak"],"count":["60"],"lang":["ru"]
        })
        assert any(c["id"]==sample["id"] for c in weak["questions"])
        random.seed(123)
        quiz=server.make_quiz("new",{
            "scope":["chapters"],"chapters":["7"],"types":["grammar"],
            "count":["60"],"lang":["ru"]
        })
        assert quiz["count"]==60 and quiz["available"]>=42
        # This chapter now includes independent weather, duration and core
        # verbs. A 60-question random sample cannot promise any fixed count
        # of schedule prompts. Test their *full availability* separately.
        wanted={c["id"] for c in cards}
        excluded=",".join(c["id"] for c in server.GRAMMAR2_ALL
                          if c["chapter"]==7 and c["id"] not in wanted)
        schedule_only=server.make_quiz("agenda-full-coverage",{
            "scope":["chapters"],"chapters":["7"],"types":["grammar"],
            "count":["60"],"lang":["ru"],"exclude":[excluded]
        })
        assert schedule_only["available"]==len(wanted)==42
        assert wanted.issubset({q["id"] for q in schedule_only["questions"]})
        assert not server.make_quiz("not-ready",{
            "scope":["chapters"],"chapters":["6"],"types":["grammar"],
            "lang":["ru"],"count":["60"]
        })["questions"] or all(c["chapter"]==6 for c in server.make_quiz("not-ready",{
            "scope":["chapters"],"chapters":["6"],"types":["grammar"],
            "lang":["ru"],"count":["60"]
        })["questions"])
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==attempts
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_pepper
print(f"PASS 7 days x 3 events, 42 agenda cards (21/7/7/7), six locales, {variants} curated typed time forms")
print("PASS chapter 7 progression, 24h/12h with daypart, singular στη μία, weak/SRS and old 144 clock IDs")
print("PASS 320px agenda vertical CSS contract; 259 old grammar IDs and 1700 vocabulary immutable")
