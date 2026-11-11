"""Issue #14: original duration-context tasks in EXISTING Lexi grammar_fill.

No time-mode, route, DB changes, scans or source-text reproduction.
Tests short event vs ongoing period, units/numeral inflection, 8 time lines,
approved numeric typed variants, six locales, weak/SRS and immutable old IDs.
"""
from collections import Counter
from pathlib import Path
import tempfile

import cloze_meanings
import clock_cards
import duration_cards
import grammar2_cards
import server

cards=duration_cards.CARDS
assert len(cards)==38 and len(grammar2_cards.CARDS)>=339  # later weather cards append, preserve original IDs
assert [c["id"] for c in grammar2_cards.CARDS[:301]]==[
    f"g2261021_{i:03d}" for i in range(1,302)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(302,340)
}
assert Counter(c["skill"] for c in cards)=={
    "contrast":8,"unit":10,"timeline":8,"typed":8,"preposition":4
}
assert Counter(c["chapter"] for c in cards)=={7:25,11:7,13:6}
assert Counter(c["contextType"] for c in cards if c["skill"]=="contrast")=={
    "event":4,"ongoing":4
}
assert len({c["prompt"] for c in cards})==len(cards)
assert Counter(c["correct"] for c in cards if c["skill"]=="preposition")=={"από":2,"για":2}
assert all(c["kind"]=="grammar" and c["group"]=="duration" for c in cards)
assert all(c["curriculum_ready_unit"]<=c["chapter"] for c in cards)
assert all(c["id"] in server.GRAMMAR2_BY_ID for c in cards)
assert len(clock_cards.CARDS)==server.CLOCK_COUNT==144
assert len(server.vocab.VOCAB)==1700
assert len([c for c in server.GRAMMAR2_ALL if c["group"]=="schedule"])==42
assert all(c["typedAnswer"]==(c["skill"]=="typed") for c in cards)
assert all(len(c["options"])==len(set(c["options"]))==4 for c in cards)
assert all(c["correct"]==c["options"][0] for c in cards)
assert {c["durationUnit"] for c in cards if c["skill"]=="unit"}=={
    "λεπτό","λεπτά","ώρα","ώρες","εβδομάδα","εβδομάδες",
    "μήνα","μήνες","χρόνο","χρόνια"
}
assert all("Τι ώρα" not in c.get("acceptedForms",[]) for c in cards)
for c in cards:
    if c["skill"]=="contrast":
        assert c["correct"]==(
            "Πόση ώρα" if c["contextType"]=="event" else "Πόσο καιρό"
        )
        assert "Τι ώρα" in c["options"] and "Πότε" in c["options"]
    if c["skill"]=="timeline":
        start_h,start_m=map(int,c["startTime"].split(":"))
        end_h,end_m=map(int,c["endTime"].split(":"))
        assert (start_h*60+start_m+c["minutes"])%1440==end_h*60+end_m
        assert c["correct"]=="στις "+c["endTime"]
    if c["skill"]=="typed":
        assert c["acceptedForms"][0]==c["correct"]
        assert len(c["acceptedForms"])>1

client=Path(__file__).with_name("app.js").read_text(encoding="utf-8")
css=Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
assert 'q.kind==="grammar"&&q.grammarGroup==="duration"' in client
assert "#question-prompt.schedule-agenda" in css
assert "white-space: pre-line" in css and "overflow-wrap: anywhere" in css

with tempfile.TemporaryDirectory(prefix="lexi-duration-") as temp:
    old_db=server.DB
    old_secret=server.auth.SECRET_FILE
    server.DB=str(Path(temp)/"student.sqlite3")
    server.auth.SECRET_FILE=Path(temp)/"login-pepper"
    try:
        server.init_db()
        attempts=0
        approved=0
        for card in cards:
            for lang in duration_cards.LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["kind"]=="grammar" and q["grammarGroup"]=="duration"
                assert q["id"]==card["id"] and q["prompt"]==card["prompt"]
                assert q["note"]==card[lang]
                assert "correct" not in q and "fullTranslations" not in q
                assert "grammarTip" not in q and "acceptedForms" not in q
                assert len(q["choices"])==(0 if card["typedAnswer"] else 4)
                if card["typedAnswer"]:
                    assert q["typedAnswer"] is True
                else:
                    assert set(q["choices"])==set(card["options"])
                uid=f"dur-{card['id']}-{lang}"
                yes=server.mark(uid,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                attempts+=1
                assert yes["correct"] and yes["answer"]==card["correct"]
                assert yes["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert yes["clozeTranslation"]==card["fullTranslations"][lang]
                assert yes["clozeTranslationLang"]==lang
                assert yes["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                no=server.mark(uid,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["options"][1]
                })
                attempts+=1
                assert not no["correct"] and no["answer"]==card["correct"]
                assert no["missDebt"]==2 and no["explanation"]
                if card.get("acceptedForms"):
                    for variant in card["acceptedForms"][1:]:
                        yes_alt=server.mark(uid,{
                            "id":card["id"],"direction":"grammar_fill",
                            "lang":lang,"selected":variant
                        })
                        attempts+=1
                        approved+=1
                        assert yes_alt["correct"] and yes_alt["acceptedVariant"]
                        assert variant in yes_alt["clozeGreek"]

        # A time-of-day question is NOT a duration question.
        sample=next(c for c in cards if c["skill"]=="contrast")
        try:
            server.mark("invalid-choice",{
                "id":sample["id"],"direction":"grammar_fill",
                "lang":"ru","selected":"πόσες ώρες"
            })
            raise AssertionError("Invalid multiple-choice selection was accepted")
        except ValueError:pass
        # Only curated full-answer digit spellings are accepted.
        text=next(c for c in cards if c["skill"]=="typed" and c["correct"]=="μία ώρα")
        response=server.mark("stress",{
            "id":text["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"μια ωρα"
        })
        attempts+=1
        assert not response["correct"]
        # Existing weak review must preserve the precise grammar card.
        wrong_user=server.mark("weak-duration",{
            "id":sample["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"Πότε"
        })
        attempts+=1
        assert not wrong_user["correct"] and wrong_user["missDebt"]==2
        weak=server.make_quiz("weak-duration",{
            "scope":["chapters"],"chapters":[str(sample["chapter"])],
            "types":["grammar"],"mode":["weak"],"count":["60"],"lang":["ru"]
        })
        assert any(c["id"]==sample["id"] for c in weak["questions"])
        # Isolate this batch within each stage: the ordinary session cap is 60
        # and cannot show every existing grammar item in a heavily populated unit.
        for chapter in (7,11,13):
            wanted={c["id"] for c in cards if c["chapter"]==chapter}
            excluded=",".join(c["id"] for c in server.GRAMMAR2_ALL
                              if c["chapter"]==chapter and c["id"] not in wanted)
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(chapter)],
                "types":["grammar"],"count":["60"],"lang":["en"],
                "exclude":[excluded]
            })
            assert wanted.issubset({q["id"] for q in quiz["questions"]}),chapter
        assert not any(c["chapter"]<7 for c in cards)
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==attempts
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_secret

print(f"PASS 38 authored duration cards x six locales, {approved} explicitly approved typed variants")
print("PASS 8 contrast scenes, 10 morphology units, 8 timelines, 8 typed answers, 4 από/για distinctions")
print("PASS existing grammar/SRS, 301 old grammar IDs, 144 clock cards and 1700 vocab immutable")
