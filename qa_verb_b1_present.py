"""Issue #10: B1 present forms in existing grammar typed clozes.

Test 9 curated paradigms, 36 distinct contexts, six balanced persons, six
locales, correct and alternate answers, stress and SRS. No new learner mode.
"""
from collections import Counter
from pathlib import Path
import tempfile
import unicodedata

import cloze_meanings
import grammar2_cards
import server
import verb_a_cards
import verb_b1_cards

CARDS=verb_b1_cards.CARDS
LANGS=verb_b1_cards.LANGS
assert len(verb_b1_cards.PARADIGMS)==9 and len(CARDS)==36
assert len(grammar2_cards.CARDS)>=183  # later B2 cards append; old IDs stable
assert [c["id"] for c in grammar2_cards.CARDS[:147]]==[
    f"g2261021_{i:03d}" for i in range(1,148)
]
assert {c["id"] for c in CARDS}=={
    f"g2261021_{i:03d}" for i in range(148,184)
}
assert Counter(c["person"] for c in CARDS)==dict.fromkeys(range(6),6)
assert Counter(c["chapter"] for c in CARDS)=={4:12,6:4,8:8,16:12}
assert Counter(c["lemma"] for c in CARDS)==dict.fromkeys(verb_b1_cards.PARADIGMS,4)
assert len({c["prompt"] for c in CARDS})==36
assert len(server.vocab.VOCAB)==1700
assert all(c["kind"]=="grammar" and c["group"]=="verb_B1" and c["typedAnswer"] for c in CARDS)
assert not any(c["id"] in {p["id"] for p in verb_a_cards.CARDS} for c in CARDS)

def strip_tonos(word):
    return "".join(char for char in unicodedata.normalize("NFD",word)
                   if not unicodedata.combining(char))

with tempfile.TemporaryDirectory(prefix="lexi-b1-") as folder:
    old_db=server.DB
    old_secret=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"progress.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        alt_count=0
        for card in CARDS:
            for lang in LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["id"]==card["id"] and q["grammarGroup"]=="verb_B1"
                assert q["typedAnswer"] is True and q["choices"]==[]
                assert "correct" not in q and "acceptedForms" not in q
                assert q["note"]==card[lang] and card["lemma"] in q["note"]
                learner="b1-"+card["id"]+"-"+lang
                good=server.mark(learner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                assert good["correct"] and good["answer"]==card["correct"]
                assert good["clozeTranslationLang"]==lang
                assert good["clozeTranslation"]==card["fullTranslations"][lang]
                assert good["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert card["correct"] in good["grammarTip"]
                assert good["acceptedAnswers"]==card["acceptedForms"]
                assert not good["acceptedVariant"]

                if len(card["acceptedForms"])>1:
                    alternative=card["acceptedForms"][1]
                    alt=server.mark(learner,{
                        "id":card["id"],"direction":"grammar_fill",
                        "lang":lang,"selected":" "+alternative.upper()+" "
                    })
                    assert alt["correct"] and alt["acceptedVariant"]
                    assert alternative in alt["clozeGreek"].casefold()
                    alt_count+=1
                # Every canonical form has tonos. Missing stress is wrong,
                # not an HTTP validation error or a false accepted variant.
                wrong=strip_tonos(card["correct"])
                assert wrong!=card["correct"]
                bad=server.mark(learner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":wrong
                })
                assert not bad["correct"] and bad["missDebt"]==2
                assert bad["answer"]==card["correct"]
                assert bad["explanation"]==cloze_meanings.explanation(card,lang)
                # An A-pattern ending must not be treated as B1 correct.
                stem=verb_b1_cards.PARADIGMS[card["lemma"]]["stem"]
                wrong_a=stem+("εις","ει","ετε")[card["person"]%3]
                assert not server.mark(learner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":wrong_a
                })["correct"]
        assert alt_count>0
        for chapter in (4,6,8,16):
            expected={c["id"] for c in CARDS if c["chapter"]==chapter}
            excluded=",".join(c["id"] for c in server.GRAMMAR2_ALL
                              if c["chapter"]==chapter and c["id"] not in expected)
            options={"scope":["chapters"],"chapters":[str(chapter)],
                     "types":["grammar"],"count":["60"],"lang":["ru"],
                     "exclude":[excluded]}
            quiz=server.make_quiz("fresh",options)
            got={q["id"] for q in quiz["questions"]}
            assert expected.issubset(got),(chapter,expected-got)
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==36*6*3+alt_count
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_secret

print(f"PASS 36 B1 typed contexts, 9 paradigms, 6 persons/locales, {alt_count} reviewed alternate scores")
print("PASS 147 old grammar IDs preserved, type-A confusion/tonos rejected, weak/SRS and stage gates")
