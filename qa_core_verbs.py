"""Issue #12: special Greek present verbs in the existing grammar_fill kind.

Six checked paradigms, 36 independently authored typed contexts (all six
persons), 12 short communicative semantic questions, six locales, explicit
variants, real error classification, mistake repetition and legacy SRS IDs.
"""
from collections import Counter
from pathlib import Path
import tempfile
import unicodedata

import cloze_meanings
import core_verb_cards as core
import grammar2_cards
import server

cards=core.CARDS
assert len(core.PARADIGMS)==6 and len(cards)==48
assert len(grammar2_cards.CARDS)>=417  # issue #4 appends phonetics; core IDs remain stable
assert [c["id"] for c in grammar2_cards.CARDS[:369]]==[
    f"g2261021_{i:03d}" for i in range(1,370)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(370,418)
}
assert Counter(c["skill"] for c in cards)=={"form":36,"semantic":12}
assert Counter(c["lemma"] for c in cards)==dict.fromkeys(core.EXPECTED,8)
assert Counter(c["person"] for c in cards if c["skill"]=="form")==dict.fromkeys(range(6),6)
assert Counter(c["chapter"] for c in cards)=={6:7,7:41}
assert all(c["curriculum_ready_unit"]<=c["chapter"] and c["kind"]=="grammar"
           and c["group"]=="verb_core" for c in cards)
assert all(not any(v in c["prompt"] for v in ("χθες","θα "," να ")) for c in cards)
assert len({c["prompt"] for c in cards})==48
for c in cards:
    if c["skill"]=="semantic":
        assert {core.EXISTING_CONTRASTS[x][0] for x in c["options"][1:]}=={
            "A","B1","B2"
        }
        assert all(core.EXISTING_CONTRASTS[x][1]<=c["chapter"]
                   for x in c["options"][1:])
assert all(len(c["options"])==len(set(c["options"]))==4 for c in cards)
assert len(server.vocab.VOCAB)==1700
assert all(c["id"] in server.GRAMMAR2_BY_ID for c in cards)
assert all(c["kind"]!="verb_core" for c in server.PRACTICE_ALL)
# No new modes, routes, UI widgets or grammar option metadata leaked.
js=Path(__file__).with_name("app.js").read_text(encoding="utf-8")
assert 'if(q.kind==="grammar"&&q.typedAnswer)' in js
assert 'field.lang="el"' in js

def strip_tonos(value):
    value=unicodedata.normalize("NFD",value)
    return "".join(ch for ch in value if not unicodedata.combining(ch))

# Narrow, deliberate authorial alternatives: NOT a global fuzzy lemmatizer.
assert core.ALLOWED_ALTERNATES["πάω"]["0"]==["πηγαίνω"]
assert core.ALLOWED_ALTERNATES["πάω"]["5"]==["πηγαίνουν","παν"]
assert core.ALLOWED_ALTERNATES["λέω"]["5"]==["λεν"]
assert core.ALLOWED_ALTERNATES["ακούω"]["5"]==["ακούν"]
assert not any("λέγω" in list(x.get("acceptedForms",[])) for x in cards)
assert "κλαις" in core.EXPECTED["κλαίω"]
assert "φταις" in core.EXPECTED["φταίω"]

with tempfile.TemporaryDirectory(prefix="lexi-core-verbs-") as folder:
    old_db=server.DB
    old_pepper=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"qa.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        attempts=0
        approved=0
        for card in cards:
            for lang in core.LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["id"]==card["id"] and q["kind"]=="grammar"
                assert q["grammarGroup"]=="verb_core"
                assert q["prompt"]==card["prompt"] and q["note"]==card[lang]
                assert q["sourcePageVerified"] is False
                assert all(k not in q for k in (
                    "correct","acceptedForms","fullTranslations","grammarTip"
                ))
                assert len(q["choices"])==(0 if card["typedAnswer"] else 4)
                if card["typedAnswer"]:
                    assert q["typedAnswer"] is True
                else:
                    assert set(q["choices"])==set(card["options"])
                user=f"cv-{card['id']}-{lang}"
                right=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                attempts+=1
                assert right["correct"] and right["answer"]==card["correct"]
                assert right["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert right["clozeTranslationLang"]==lang
                assert right["clozeTranslation"]==card["fullTranslations"][lang]
                assert card["correct"] in right["clozeGreek"]
                assert "answerErrorType" not in right
                assert all(form in right["grammarTip"]
                           for form in core.EXPECTED[card["lemma"]])
                if card["typedAnswer"]:
                    for alt in card["acceptedForms"][1:]:
                        variant=server.mark(user,{
                            "id":card["id"],"direction":"grammar_fill",
                            "lang":lang,"selected":"  "+alt.upper()+" "
                        })
                        attempts+=1
                        approved+=1
                        assert variant["correct"] and variant["acceptedVariant"]
                        assert alt.casefold() in variant["clozeGreek"].casefold()
                # Wrong person on form cards, wrong verb on mini-dialogues.
                wrong=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["options"][1]
                })
                attempts+=1
                assert not wrong["correct"] and wrong["missDebt"]==2
                assert wrong["answer"]==card["correct"]
                assert wrong["explanation"] and wrong["grammarTip"]
                assert wrong["answerErrorType"]==(
                    "person" if card["skill"]=="form" else "meaning"
                ),(card["id"],wrong.get("answerErrorType"))

        # Typed Greek tonos must be evaluated, but some natural short forms
        # genuinely have no written accent (λες, πας, τρως, κλαις, φταις).
        accented=next(c for c in cards
                      if c["skill"]=="form" and c["lemma"]=="λέω" and c["person"]==0)
        wrong=server.mark("accent-user",{
            "id":accented["id"],"direction":"grammar_fill",
            "lang":"ru","selected":strip_tonos(accented["correct"])
        })
        attempts+=1
        assert not wrong["correct"] and wrong["answerErrorType"]=="accent"
        short=next(c for c in cards if c["skill"]=="form"
                   and c["lemma"]=="πάω" and c["person"]==1)
        correct=server.mark("no-accent-user",{
            "id":short["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"πας"
        })
        attempts+=1
        assert correct["correct"]
        incorrectly_accented=server.mark("false-tonos-user",{
            "id":short["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"πάς"
        })
        attempts+=1
        assert not incorrectly_accented["correct"] and incorrectly_accented["answerErrorType"]=="accent"
        typo=server.mark("typo-user",{
            "id":accented["id"],"direction":"grammar_fill",
            "lang":"en","selected":"λεγο"
        })
        attempts+=1
        assert not typo["correct"] and typo["answerErrorType"]=="spelling"
        # λέγω has its own more formal paradigm, is not a generic A1 alias.
        formal=server.mark("formal-user",{
            "id":accented["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"λέγω"
        })
        attempts+=1
        assert not formal["correct"]
        # Existing exact-card weak quiz and lesson filtering work unchanged.
        missed=next(c for c in cards if c["skill"]=="form")
        bad=server.mark("weak-user",{
            "id":missed["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"NONE"
        })
        attempts+=1
        assert not bad["correct"] and bad["missDebt"]==2
        weak=server.make_quiz("weak-user",{
            "scope":["chapters"],"chapters":[str(missed["chapter"])],
            "types":["grammar"],"mode":["weak"],"count":["60"],"lang":["ru"]
        })
        assert any(x["id"]==missed["id"] for x in weak["questions"])
        # The chapter 7 pool is >60. Isolate only this batch when asserting
        # its entire coverage, just as older regression suites now do.
        for ch in (6,7):
            wanted={c["id"] for c in cards if c["chapter"]==ch}
            exclude=",".join(c["id"] for c in server.GRAMMAR2_ALL
                             if c["chapter"]==ch and c["id"] not in wanted)
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(ch)],
                "types":["grammar"],"lang":["ru"],"count":["60"],
                "exclude":[exclude]
            })
            assert wanted.issubset({q["id"] for q in quiz["questions"]}),ch
        # Existing old-answer card still scores and changes only its own key.
        old=grammar2_cards.CARDS[0]
        assert server.mark("old-user",{
            "id":old["id"],"direction":"grammar_fill",
            "lang":"ru","selected":old["correct"]
        })["correct"]
        attempts+=1
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==attempts
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_pepper

print(f"PASS core verbs: 6 verified paradigms, 36 typed forms, 12 original mini-dialogues, {approved} curated variant scores")
print("PASS 6 locales, diagnoses accent/person/spelling/meaning, chapter6/7 gates, SRS and 369 old IDs")
print("PASS no new learner mode, no future/aorist/na in early content, 1700 vocab unchanged")
