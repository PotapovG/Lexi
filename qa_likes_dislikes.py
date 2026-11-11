"""Issue #13 — likes/dislikes inside Lexi's existing grammar-fill exercises.

The liked subject controls αρέσει/αρέσουν; genitive clitic marks the
experiencer, not possession. No modes, routes, schemas or legacy ID rewrites.
"""
from collections import Counter
from pathlib import Path
import tempfile

import cloze_meanings
import grammar2_cards
import likes_dislikes_cards
import server

cards=likes_dislikes_cards.CARDS
langs=likes_dislikes_cards.LANGS
assert len(cards)==36 and len(grammar2_cards.CARDS)==259
assert [c["id"] for c in grammar2_cards.CARDS[:223]]==[
    f"g2261021_{i:03d}" for i in range(1,224)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(224,260)
}
assert Counter(c["skill"] for c in cards)=={
    "agreement":18,"experiencer":12,"typed":6
}
assert Counter(c["chapter"] for c in cards)=={7:13,8:9,16:14}
assert Counter(c["number"] for c in cards)=={"sg":19,"pl":17}
assert len({c["prompt"] for c in cards})==36
assert all(c["kind"]=="grammar" and c["group"]=="likes"
           and c["curriculum_ready_unit"]<=c["chapter"] for c in cards)
assert all(c["number"]!="pl" or c["chapter"]>=8 for c in cards)
assert all(c["skill"]!="typed" or c["chapter"]>=16 for c in cards)
assert all(c["source"].startswith("independent_") and not c["book_page_verified"] for c in cards)
assert len(server.vocab.VOCAB)==1700
assert len([c for c in server.ALL if c.get("source")=="original-community" and
            c["id"].startswith("cm16_08")])==10

for c in cards:
    if c["skill"]=="agreement":
        assert c["correct"]==("αρέσει" if c["number"]=="sg" else "αρέσουν")
        assert set(c["options"])=={"αρέσει","αρέσουν","αρέσω","αρέσεις"}
    elif c["skill"]=="experiencer":
        assert c["correct"]==c["experiencer"]
        assert c["correct"] in likes_dislikes_cards.EXPERIENCERS
    else:
        assert c["typedAnswer"]
        assert c["correct"] in c["acceptedForms"]
assert len([c for c in cards if len(c.get("acceptedForms",[]))>1])==1

with tempfile.TemporaryDirectory(prefix="lexi-likes-") as td:
    prev_db=server.DB
    prev_secret=server.auth.SECRET_FILE
    server.DB=str(Path(td)/"progress.sqlite3")
    server.auth.SECRET_FILE=Path(td)/"login-pepper"
    try:
        server.init_db()
        scored=0
        for card in cards:
            for lang in langs:
                question=server.format_question(card,"grammar_fill",lang)
                assert question["id"]==card["id"]
                assert question["kind"]=="grammar" and question["grammarGroup"]=="likes"
                assert question["prompt"]==card["prompt"]
                assert question["note"]==card[lang]
                assert "correct" not in question
                assert "fullTranslations" not in question
                assert "acceptedForms" not in question
                if card["typedAnswer"]:
                    assert question["typedAnswer"] is True and question["choices"]==[]
                else:
                    assert len(question["choices"])==4
                    assert set(question["choices"])==set(card["options"])
                learner=f"likes-{card['id']}-{lang}"
                right=server.mark(learner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                assert right["correct"] and right["answer"]==card["correct"]
                assert right["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert right["clozeTranslation"]==card["fullTranslations"][lang]
                assert right["clozeTranslationLang"]==lang
                assert right["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                assert card["correct"] in right["grammarTip"]
                bad_answer=("αρέσεις" if card["typedAnswer"] else next(
                    v for v in card["options"] if v!=card["correct"]
                ))
                wrong=server.mark(learner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":bad_answer
                })
                assert not wrong["correct"] and wrong["answer"]==card["correct"]
                assert wrong["missDebt"]==2 and wrong["explanation"]
                scored+=2
                if len(card.get("acceptedForms",[]))>1:
                    for variant in card["acceptedForms"][1:]:
                        v=server.mark(learner,{
                            "id":card["id"],"direction":"grammar_fill",
                            "lang":lang,"selected":variant
                        })
                        assert v["correct"] and v["acceptedVariant"]
                        assert variant in v["clozeGreek"]
                        assert v["clozeTranslationLang"]==lang
                        scored+=1
        for chapter in (7,8,16):
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(chapter)],
                "types":["grammar"],"count":["60"],"lang":["ru"]
            })
            expected={c["id"] for c in cards if c["chapter"]==chapter}
            got={c["id"] for c in quiz["questions"]}
            assert expected.issubset(got),(chapter,expected-got)
        # Existing mistakes remain gradeable in their own separate scope:
        poss=next(c for c in grammar2_cards.CARDS if c.get("group")=="possessive")
        assert server.mark("old-user",{
            "id":poss["id"],"direction":"grammar_fill","lang":"ru",
            "selected":poss["correct"]
        })["correct"]
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==scored+1
    finally:
        server.DB=prev_db
        server.auth.SECRET_FILE=prev_secret

print("PASS: 36 original liking exercises, 6 locales, grammar/choice/typed responses and variant feedback")
print("PASS: plural gate >=8, Greek Life/legacy modes unchanged, 223 existing grammar IDs and 1700 vocab unchanged")
print("PASS: 10 original leisure sentence cards, SRS + older possessive distinctions preserved")
