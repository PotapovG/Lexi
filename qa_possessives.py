"""Issue #8: seven possessive forms in the pre-existing grammar cloze mode.

Proof that 35 authorial items have owner-anchored answers, correct stage,
six independent localizations, existing Pocket stress guidance, and stable
per-user scoring. No new UI mode, API route, or persistent schema.
"""
from collections import Counter
from pathlib import Path
import tempfile

import cloze_meanings
import enclitic_stress
import grammar2_cards
import possessive_cards
import server

cards=possessive_cards.CARDS
forms=("μου","σου","του","της","μας","σας","τους")
assert len(cards)==35
assert Counter(c["correct"] for c in cards)=={p:5 for p in forms}
assert {c["id"] for c in cards}=={f"g2261021_{i:03d}" for i in range(77,112)}
assert len(grammar2_cards.CARDS)>=111  # later grammar batches append, never rewrite these 111 IDs
assert len([c for c in grammar2_cards.CARDS if c["group"]=="possessive"])==35
assert [c["id"] for c in grammar2_cards.CARDS[:76]]==[
    f"g2261021_{i:03d}" for i in range(1,77)
]
assert len(server.vocab.VOCAB)==1700
assert not any(c["kind"]=="possessive" for c in server.PRACTICE_ALL)
assert all(c["kind"]=="grammar" and c["curriculum_ready_unit"]<=c["chapter"] for c in cards)
assert Counter(c["chapter"] for c in cards)=={2:20,3:15}
assert len([c for c in cards if c.get("stressNoun")])==7
assert all(c["prompt"].count("___")==1 for c in cards)
assert all(len(c["options"])==len(set(c["options"]))==4 for c in cards)
assert len({c["prompt"] for c in cards})==35

# All seven double-accent forms use the existing source of truth.
for c in cards:
    if c.get("stressNoun"):
        metadata=c["stressNoun"]
        assert metadata["rendered"]==enclitic_stress.add_final(metadata["noun"])
        assert metadata["rendered"]+" ___" in c["prompt"]

with tempfile.TemporaryDirectory(prefix="lexi-possessive-") as folder:
    original_db=server.DB
    original_secret=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"student.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        for card in cards:
            for lang in possessive_cards.LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["id"]==card["id"] and q["kind"]=="grammar"
                assert q["grammarGroup"]=="possessive"
                assert len(q["choices"])==4 and set(q["choices"])==set(card["options"])
                assert "correct" not in q and "fullTranslations" not in q
                assert q["sourcePageVerified"] is False
                user=f"test-{card['id']}-{lang}"
                good=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill","lang":lang,
                    "selected":card["correct"]
                })
                assert good["correct"] and good["answer"]==card["correct"]
                assert good["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert card["correct"] in good["grammarTip"]
                assert good["clozeTranslationLang"]==lang
                assert good["clozeTranslation"]==card["fullTranslations"][lang]
                assert good["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                wrong=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill","lang":lang,
                    "selected":card["options"][1]
                })
                assert not wrong["correct"] and wrong["answer"]==card["correct"]
                assert wrong["explanation"]==cloze_meanings.explanation(card,lang)
                assert wrong["clozeTranslationLang"]==lang
        for chapter in (2,3):
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(chapter)],
                "types":["grammar"],"count":["60"],"lang":["ru"]
            })
            assert len([q for q in quiz["questions"]
                        if q["id"].startswith("g2261021_")
                        and int(q["id"].split("_")[-1])>=77])==sum(
                c["chapter"]==chapter for c in cards
            )
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==35*6*2
    finally:
        server.DB=original_db
        server.auth.SECRET_FILE=original_secret

print("PASS 35 possessive clozes, seven owner forms x five nouns, 6 locales and 420 graded answers")
print("PASS stress from existing enclitic rules, lessons 2/3, 76 old grammar IDs and 1700 independent words")
