"""Issue #11: B2 present in EXISTING Lexi grammar_fill typed questions.

Regression coverage: 10 authorial paradigms, 40 independent contexts, six
languages, published choice/typed API, approved 3pl variants, tonos, weak debt,
lesson gates, stable older IDs. Disposable account DB and secret only.
"""
from collections import Counter
from pathlib import Path
import tempfile
import unicodedata

import cloze_meanings
import grammar2_cards
import server
import verb_b2_cards

CARDS=verb_b2_cards.CARDS
LANGS=verb_b2_cards.LANGS
assert len(verb_b2_cards.PARADIGMS)==10 and len(CARDS)==40
assert len(grammar2_cards.CARDS)>=223  # issue #13 appends likes without altering old IDs
assert [c["id"] for c in grammar2_cards.CARDS[:183]]==[
    f"g2261021_{i:03d}" for i in range(1,184)
]
assert {c["id"] for c in CARDS}=={
    f"g2261021_{i:03d}" for i in range(184,224)
}
assert Counter(c["lemma"] for c in CARDS)==dict.fromkeys(verb_b2_cards.PARADIGMS,4)
assert Counter(c["chapter"] for c in CARDS)=={6:4,7:8,16:24,17:4}
assert max(Counter(c["person"] for c in CARDS).values())-min(Counter(c["person"] for c in CARDS).values())<=1
assert len({c["prompt"] for c in CARDS})==40
assert all(c["kind"]=="grammar" and c["group"]=="verb_B2" and c["typedAnswer"] for c in CARDS)
assert all(c["curriculum_ready_unit"]<=c["chapter"] for c in CARDS)
assert not any(c["id"] in server.BY_ID for c in CARDS)
assert len(server.vocab.VOCAB)==1700
assert all(not c.get("typedAnswer") for c in grammar2_cards.CARDS[:111])

def strip_tonos(word):
    return "".join(c for c in unicodedata.normalize("NFD",word)
                   if not unicodedata.combining(c))

with tempfile.TemporaryDirectory(prefix="lexi-b2-") as folder:
    old_db=server.DB
    old_secret=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"progress.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        variants=0
        for card in CARDS:
            for lang in LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["id"]==card["id"] and q["grammarGroup"]=="verb_B2"
                assert q["kind"]=="grammar" and q["typedAnswer"] is True and q["choices"]==[]
                assert "correct" not in q and "acceptedForms" not in q
                assert "fullTranslations" not in q and card["lemma"] in q["note"]
                student=f"b2-{card['id']}-{lang}"
                right=server.mark(student,dict(
                    id=card["id"],direction="grammar_fill",
                    lang=lang,selected=card["correct"]
                ))
                assert right["correct"] and not right["acceptedVariant"]
                assert right["acceptedAnswers"]==card["acceptedForms"]
                assert right["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert right["clozeTranslation"]==card["fullTranslations"][lang]
                assert right["clozeTranslationLang"]==lang
                assert right["answer"]==card["correct"]
                if len(card["acceptedForms"])>1:
                    alt=card["acceptedForms"][1]
                    other=server.mark(student,dict(
                        id=card["id"],direction="grammar_fill",
                        lang=lang,selected=" "+alt.upper()+" "
                    ))
                    assert other["correct"] and other["acceptedVariant"]
                    assert alt in other["clozeGreek"].casefold()
                    variants+=1
                # Stress and B1 morphology remain meaningful distinctions.
                noaccent=strip_tonos(card["correct"])
                assert noaccent!=card["correct"]
                bad=server.mark(student,dict(
                    id=card["id"],direction="grammar_fill",
                    lang=lang,selected=noaccent
                ))
                assert not bad["correct"] and bad["missDebt"]==2
                assert bad["explanation"]==cloze_meanings.explanation(card,lang)
                stem=verb_b2_cards.PARADIGMS[card["lemma"]]["stem"]
                b1=stem+"άς"
                wrong=server.mark(student,dict(
                    id=card["id"],direction="grammar_fill",
                    lang=lang,selected=b1
                ))
                assert not wrong["correct"]
        assert variants>0
        for chapter in (6,7,16,17):
            expected={c["id"] for c in CARDS if c["chapter"]==chapter}
            excluded=",".join(c["id"] for c in server.GRAMMAR2_ALL
                              if c["chapter"]==chapter and c["id"] not in expected)
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(chapter)],
                "types":["grammar"],"count":["60"],"lang":["ru"],
                "exclude":[excluded]
            })
            assert expected.issubset({q["id"] for q in quiz["questions"]}),chapter
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==40*6*3+variants
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_secret
print(f"PASS 40 B2 typed contexts, 10 paradigms, all six persons and locales; {variants} accepted variants")
print("PASS tonos/B1 errors graded wrong, chapter scope and weak-debt, 183 old grammar IDs and 1700 vocabulary intact")
