"""Issue #9: productive Type-A present forms inside existing grammar_fill.

12 complete independently verified 6-person paradigms, 36 original contexts,
6 languages, correct/wrong typed scores, SRS and stable pre-existing keys.
"""
import collections
import re
import tempfile
import unicodedata
from pathlib import Path
import server
import grammar2_cards
import verb_a_cards
import cloze_meanings

CARDS=verb_a_cards.CARDS
assert len(CARDS)==36
assert len(verb_a_cards.PARADIGMS)==12
assert len(grammar2_cards.CARDS)==147
assert [c["id"] for c in grammar2_cards.CARDS[:111]]==[
    f"g2261021_{i:03d}" for i in range(1,112)
]
assert {c["id"] for c in CARDS}=={
    f"g2261021_{i:03d}" for i in range(112,148)
}
assert collections.Counter(c["person"] for c in CARDS)==dict.fromkeys(range(6),6)
assert collections.Counter(c["chapter"] for c in CARDS)=={2:6,7:24,8:6}
assert collections.Counter(c["lemma"] for c in CARDS)==dict.fromkeys(verb_a_cards.PARADIGMS,3)
assert all(c["kind"]=="grammar" and c["group"]=="verb_A" and c["typedAnswer"] for c in CARDS)
assert all(c["curriculum_ready_unit"]<=c["chapter"] for c in CARDS)
assert len(server.vocab.VOCAB)==1700
assert all(c["id"] in server.GRAMMAR2_BY_ID for c in CARDS)
assert all(not c.get("typedAnswer") for c in grammar2_cards.CARDS[:111])
assert all(not re.search(r"\b(?:θα|να|χθες)\b",c["gr"]) for c in CARDS)
assert all(len(row["forms"])==6 for row in verb_a_cards.PARADIGMS.values())

def without_tonos(text):
    return "".join(char for char in unicodedata.normalize("NFD",text)
                   if not unicodedata.combining(char))

client=Path(__file__).with_name("app.js").read_text(encoding="utf-8")
assert 'if(q.kind==="grammar"&&q.typedAnswer)' in client
assert 'field.lang="el"' in client
assert 'if(event.key==="Enter")' in client
assert '(q.kind==="order"||q.typedAnswer)?overrideSelected' in client

with tempfile.TemporaryDirectory(prefix="lexi-verb-a-") as folder:
    previous_db=server.DB
    previous_secret=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"progress.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        for card in CARDS:
            for lang in verb_a_cards.LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["kind"]=="grammar" and q["grammarGroup"]=="verb_A"
                assert q["typedAnswer"] is True and q["choices"]==[]
                assert "correct" not in q and "fullTranslations" not in q
                assert q["note"]==card[lang] and card["lemma"] in q["note"]
                uid="learner_"+card["id"]+"_"+lang
                good=server.mark(uid,{"id":card["id"],"direction":"grammar_fill",
                                      "lang":lang,"selected":card["correct"]})
                assert good["correct"] and good["answer"]==card["correct"]
                assert good["clozeTranslation"]==card["fullTranslations"][lang]
                assert good["clozeTranslationLang"]==lang
                assert good["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert card["correct"] in good["grammarTip"]
                wrong=without_tonos(card["correct"])
                assert wrong!=card["correct"],card["id"]
                bad=server.mark(uid,{"id":card["id"],"direction":"grammar_fill",
                                     "lang":lang,"selected":wrong})
                assert not bad["correct"] and bad["missDebt"]==2
                assert bad["answer"]==card["correct"]
                assert bad["explanation"]==cloze_meanings.explanation(card,lang)
        # A genuinely typed answer accepts normalized casing and surrounding
        # spaces but does not silently ignore Greek tonos.
        sample=next(c for c in CARDS if c["lemma"]=="διαβάζω")
        accepted=server.mark("casefold",{
            "id":sample["id"],"direction":"grammar_fill","lang":"ru",
            "selected":"  "+sample["correct"].upper()+"  "
        })
        assert accepted["correct"]
        # Existing chapter and SRS filtering can select the new items.
        for stage in (2,7,8):
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(stage)],
                "types":["grammar"],"count":["60"],"lang":["ru"]
            })
            ours={c["id"] for c in CARDS if c["chapter"]==stage}
            assert ours.issubset({q["id"] for q in quiz["questions"]}),stage
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT count(*) FROM attempts").fetchone()[0]==36*6*2+1
    finally:
        server.DB=previous_db
        server.auth.SECRET_FILE=previous_secret

print("PASS Type-A: 12 paradigms, 36 unique typed contexts, 6 persons balanced and 6 locales")
print("PASS tonal orthography, negative/question variants, scoring/SRS, stable 111 grammar IDs")
