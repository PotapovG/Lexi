"""Issue #17: ten linked A1 practical scenarios in the EXISTING Lexi quiz.

Ten authorial scenes of five sequential productive/choice tasks with full
six-locale meanings and explanations, curriculum gates 1..7, no new mode.
Normal 10–60 minute/Quick session gets one full story first; weak/SRS review
continues to target only the individual failed cards.  Old IDs/SRS untouched.
"""
from collections import Counter
from pathlib import Path
import random
import tempfile
import unicodedata

import cloze_meanings
import grammar2_cards
import mixed_review_cards as review
import mixed_review_selection as selector
import server

cards=review.CARDS
assert len(cards)==50 and len(review.SCENARIOS)==10
assert len(grammar2_cards.CARDS)==543
assert [c["id"] for c in grammar2_cards.CARDS[:493]]==[
    f"g2261021_{i:03d}" for i in range(1,494)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(494,544)
}
assert Counter(c["chapter"] for c in cards)=={1:10,2:5,3:5,4:5,6:10,7:15}
assert all(c["kind"]=="grammar" and c["group"]=="review_scenario" for c in cards)
assert all(c["scenarioStep"] in range(1,6) and c["scenarioTotal"]==5 for c in cards)
assert all(c["curriculum_ready_unit"]<=c["chapter"]<=7 for c in cards)
assert len({c["prompt"] for c in cards})==50
assert sum(c["typedAnswer"] for c in cards)>=20
assert sum(not c["typedAnswer"] for c in cards)>=20
assert len(set(c["reviewSkill"] for c in cards))>=8
assert len(server.vocab.VOCAB)==1700 and server.CLOCK_COUNT==144
assert len(server.SYLLABLE_ALL)==35
assert not any(c["kind"]=="review_scenario" for c in server.PRACTICE_ALL)
assert all(c["source"].startswith("independent_") and not c["book_page_verified"] for c in cards)
assert all(len(c["options"])==len(set(c["options"]))==4 for c in cards)
assert all(c["correct"]==c["options"][0] for c in cards)
assert all(c["scenarioId"] in review.SCENARIOS and c["id"] in server.GRAMMAR2_BY_ID for c in cards)
assert all("θα " not in c["prompt"] and "χθες" not in c["prompt"] for c in cards)

# Pure deterministic scene-packing coverage. A partial scene never forces
# a block; normal mode still sees other previously ranked learning cards.
all_entries=[(c,"grammar_fill",5) for c in cards]
selected,remainder=selector.select_block(all_entries,60,random.Random(17))
assert len(selected)==5 and len(remainder)==0
assert len({x[0]["scenarioId"] for x in selected})==1
assert [x[0]["scenarioStep"] for x in selected]==[1,2,3,4,5]
assert selector.select_block(all_entries[:4],60,random.Random(17))==([],[])
assert selector.select_block(all_entries,4,random.Random(17))==([],[])
# A partially eligible scene must be discarded in normal practice; the
# existing ordinary grammar item survives both chapter and short caps.
ordinary_example=(grammar2_cards.CARDS[0],"grammar_fill",3)
part=all_entries[:4]+[ordinary_example]
assert selector.select_block(part,60,random.Random(17))==([],[ordinary_example])
assert selector.select_block(part,4,random.Random(17))==([],[ordinary_example])

js=Path(__file__).with_name("app.js").read_text("utf-8")
html=Path(__file__).with_name("index.html").read_text("utf-8")
css=Path(__file__).with_name("styles.css").read_text("utf-8")
assert 'q.grammarGroup==="review_scenario"' in js
assert '["phonetic","consonant","review_scenario"].includes(q.grammarGroup)' in js
assert 'id="finish-skills"' in html
assert '.finish-skill-row' in css and '@media (max-width: 360px)' in css
assert 'sessionSkills:state.sessionSkills' in js
assert 'state.sessionSkills=(saved.sessionSkills' in js
assert 'renderSessionSkills();' in js
assert 'const SESSION_SKILLS=' in js and 'weakSession' in js

with tempfile.TemporaryDirectory(prefix="lexi-mixed-a1-") as folder:
    old_db=server.DB
    old_secret=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"learner.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"pepper"
    try:
        server.init_db()
        attempts=0
        variants=0
        for card in cards:
            for lang in review.LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["id"]==card["id"]
                assert q["kind"]=="grammar" and q["grammarGroup"]=="review_scenario"
                assert q["scenarioId"]==card["scenarioId"]
                assert q["scenarioStep"]==card["scenarioStep"] and q["scenarioTotal"]==5
                assert q["scenarioTitle"]==card["scenarioTitles"][lang]
                assert q["reviewSkill"]==card["reviewSkill"]
                assert q["note"]==card[lang] and q["prompt"]==card["prompt"]
                assert q["sourcePageVerified"] is False
                assert all(k not in q for k in (
                    "correct","acceptedForms","fullTranslations","fullTips","grammarTip"
                ))
                assert len(q["choices"])==(0 if card["typedAnswer"] else 4)
                if card["typedAnswer"]:
                    assert q["typedAnswer"] is True
                else:
                    assert set(q["choices"])==set(card["options"])
                if card.get("phoneticWord"):
                    audio=q.get("wordAudio")
                    assert audio and audio["speechText"]==card["phoneticWord"]
                    assert audio["audioSource"] in ("pocket","unavailable")
                    if audio["audioUrl"]:
                        assert audio["audioUrl"].startswith(("/greek/audio/","/greek/pronunciation/"))
                else:assert "wordAudio" not in q

                user=f"scene-{card['id']}-{lang}"
                correct=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"],"srsOptIn":True
                })
                attempts+=1
                assert correct["correct"] and correct["answer"]==card["correct"]
                assert correct["clozeTranslation"]==card["fullTranslations"][lang]
                assert correct["clozeTranslationLang"]==lang
                assert correct["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert correct["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                if card.get("acceptedForms"):
                    for variant in card["acceptedForms"][1:]:
                        accepted=server.mark(user,{
                            "id":card["id"],"direction":"grammar_fill",
                            "lang":lang,"selected":variant,"srsOptIn":True
                        })
                        attempts+=1;variants+=1
                        assert accepted["correct"] and accepted["acceptedVariant"]
                        assert variant in accepted["clozeGreek"]
                        assert variant in accepted["acceptedAnswers"]
                bad_value="xxxx" if card["typedAnswer"] else card["options"][1]
                wrong=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":bad_value,"srsOptIn":True
                })
                attempts+=1
                assert not wrong["correct"] and wrong["answer"]==card["correct"]
                assert wrong["explanation"]==card["fullTips"][lang]
                assert wrong["missDebt"]==2

        # Each normal chapter-selected quiz starts with an intact five-step
        # scenario, never arbitrary disconnected fragments. Other cards are
        # still available after the first block, bounded by count=60.
        for chapter in (1,2,3,4,6,7):
            random.seed(17+chapter)
            batch=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(chapter)],
                "types":["grammar"],"lang":["ru"],"count":["60"],
                "study":["textbook"]
            })
            q=batch["questions"]
            assert q and batch["count"]<=60
            if batch["count"]>=5:
                first=q[:5]
                assert all(x.get("grammarGroup")=="review_scenario" for x in first),chapter
                assert len({x["scenarioId"] for x in first})==1,chapter
                assert [x["scenarioStep"] for x in first]==[1,2,3,4,5],chapter
            assert not any(x.get("grammarGroup")=="review_scenario" for x in q[5:]),chapter
            assert all(x["chapter"]==chapter for x in q)
        # Chapter 1 has exactly two scenarios. Exclude one step from
        # each: the normal 60-question pool must omit all orphaned steps.
        unavailable=[review.SCENARIOS["hello_class"][0]["id"],
                     review.SCENARIOS["meet_names"][0]["id"]]
        filtered=server.make_quiz("fresh",{
            "scope":["chapters"],"chapters":["1"],
            "types":["grammar"],"lang":["ru"],"count":["60"],
            "exclude":[",".join(unavailable)]
        })
        assert not any(q.get("grammarGroup")=="review_scenario"
                       for q in filtered["questions"])
        short=server.make_quiz("fresh",{
            "scope":["chapters"],"chapters":["1"],
            "types":["grammar"],"lang":["ru"],"count":["4"]
        })
        assert short["count"]<=4
        assert not any(q.get("grammarGroup")=="review_scenario"
                       for q in short["questions"])
        personalized=server.make_quiz("fresh",{
            "scope":["chapters"],"chapters":["1"],
            "types":["grammar"],"lang":["ru"],"count":["60"],
            "study":["personalized"]
        })
        assert not any(q.get("grammarGroup")=="review_scenario"
                       for q in personalized["questions"])
        # Weak mode keeps precise errored card and does NOT pull whole scene.
        sample=review.SCENARIOS["rainy_day"][0]
        weak_answer=server.mark("review-only",{
            "id":sample["id"],"direction":"grammar_fill",
            "lang":"ru","selected":sample["options"][1]
        })
        attempts+=1
        assert not weak_answer["correct"] and weak_answer["missDebt"]==2
        weak=server.make_quiz("review-only",{
            "scope":["chapters"],"chapters":["7"],
            "types":["grammar"],"mode":["weak"],"lang":["ru"],"count":["60"]
        })
        assert [x["id"] for x in weak["questions"]]==[sample["id"]]
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==attempts
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_secret

print(f"PASS #17: 10 original connected scenes ×5 steps, all 6 locales, {variants} authorial accepted alternatives")
print("PASS normal 60-count/10–60min Quick uses ordered 5-step scene, 1–7 gates, old cards remain available")
print("PASS weak/SRS only failed cards, in-place per-skill result, no new modes/routes/DB, 493 old grammar IDs")
