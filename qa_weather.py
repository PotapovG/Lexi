"""Issue #16: weather vocabulary & communication in existing grammar practice.

30 original expression-in-context items (10 symbol reading, 10 negative typed,
10 event/activity applications), six locales and 10 original sentence cards.
No new modes, UI routes, network weather access, images or account migrations.
"""
from collections import Counter
from pathlib import Path
import tempfile

import cloze_meanings
import grammar2_cards
import server
import weather_cards

cards=weather_cards.CARDS
langs=weather_cards.LANGS
assert len(cards)==30 and len(grammar2_cards.CARDS)>=369  # core verbs append; old IDs immutable
assert [c["id"] for c in grammar2_cards.CARDS[:339]]==[
    f"g2261021_{i:03d}" for i in range(1,340)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(340,370)
}
assert Counter(c["skill"] for c in cards)=={
    "symbol":10,"negative":10,"activity":10
}
assert Counter(c["weatherCode"] for c in cards)=={
    "sun":6,"cloud":6,"rain":6,"snow":6,"wind":6
}
assert len(weather_cards.WEATHER)==5
assert len({c["prompt"] for c in cards})==30
assert all(c["kind"]=="grammar" and c["group"]=="weather" for c in cards)
assert all(c["chapter"]==7 and c["curriculum_ready_unit"]==7 for c in cards)
assert all(c["typedAnswer"]==(c["skill"]=="negative") for c in cards)
assert all(len(c["options"])==len(set(c["options"]))==4 for c in cards)
assert all(c["correct"]==c["options"][0] for c in cards)
assert all(c["source"].startswith("independent_") and not c["book_page_verified"] for c in cards)
assert not any(c["kind"]=="weather" for c in server.PRACTICE_ALL)
assert len(server.vocab.VOCAB)==1700
assert len([c for c in server.ALL if c["id"].startswith("cm07_09") and
            c.get("source")=="original-community" and c["kind"]=="sentence"])==10
assert not any(c["kind"]=="word" and c["id"].startswith("cm07_09") for c in server.ALL)
# Symbols remain intelligible without color; the Greek textual cue is
# permanently part of the question, rather than a CSS-dependent alt.
for card in cards:
    weather=weather_cards.WEATHER[card["weatherCode"]]
    assert weather["symbol"]+" ("+weather_cards.NOUN_LABELS[card["weatherCode"]]+")" in card["prompt"]
    assert weather["negative" if card["skill"]=="negative" else "positive"]==card["correct"]

client=Path(__file__).with_name("app.js").read_text(encoding="utf-8")
css=Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
assert 'q.kind==="grammar"&&q.grammarGroup==="weather"' in client
assert 'white-space: pre-line' in css and 'overflow-wrap: anywhere' in css

with tempfile.TemporaryDirectory(prefix="lexi-weather-") as tmp:
    old_db=server.DB
    old_secret=server.auth.SECRET_FILE
    server.DB=str(Path(tmp)/"student.sqlite3")
    server.auth.SECRET_FILE=Path(tmp)/"login-pepper"
    try:
        server.init_db()
        attempts=0
        for card in cards:
            for lang in langs:
                question=server.format_question(card,"grammar_fill",lang)
                assert question["id"]==card["id"]
                assert question["kind"]=="grammar" and question["grammarGroup"]=="weather"
                assert question["note"]==card[lang]
                assert question["sourcePageVerified"] is False
                assert not any(k in question for k in
                               ("correct","grammarTip","fullTranslations","acceptedForms"))
                assert len(question["choices"])==(0 if card["typedAnswer"] else 4)
                if card["typedAnswer"]:
                    assert question["typedAnswer"] is True
                else:
                    assert set(question["choices"])==set(card["options"])
                owner="learner-"+card["id"]+"-"+lang
                good=server.mark(owner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                attempts+=1
                assert good["correct"] and good["answer"]==card["correct"]
                assert good["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert good["clozeTranslation"]==card["fullTranslations"][lang]
                assert good["clozeTranslationLang"]==lang
                assert good["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                assert "δεν" in good["answer"] if card["skill"]=="negative" else "δεν" not in good["answer"]
                wrong=server.mark(owner,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["options"][1]
                })
                attempts+=1
                assert not wrong["correct"] and wrong["missDebt"]==2
                assert wrong["answer"]==card["correct"] and wrong["explanation"]
        # Wrong-answer SRS/weak remains in standard chapter 7 quiz.
        missed=next(c for c in cards if c["skill"]=="negative")
        bad=server.mark("weather-review",{
            "id":missed["id"],"direction":"grammar_fill",
            "lang":"ru","selected":"είναι ήλιο"
        })
        attempts+=1
        assert not bad["correct"] and bad["missDebt"]==2
        weak=server.make_quiz("weather-review",{
            "scope":["chapters"],"chapters":["7"],
            "types":["grammar"],"mode":["weak"],"count":["60"],"lang":["ru"]
        })
        assert any(c["id"]==missed["id"] for c in weak["questions"])
        # Isolate this batch under the existing max-60 question cap.
        wanted={c["id"] for c in cards}
        excluded=",".join(c["id"] for c in server.GRAMMAR2_ALL
                          if c["chapter"]==7 and c["id"] not in wanted)
        quiz=server.make_quiz("weather-fresh",{
            "scope":["chapters"],"chapters":["7"],"types":["grammar"],
            "count":["60"],"lang":["en"],"exclude":[excluded]
        })
        assert wanted.issubset({q["id"] for q in quiz["questions"]})
        assert all(q["chapter"]==7 for q in quiz["questions"])
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==attempts
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_secret

print("PASS weather: 30 original grammar questions x 6 locales, 10 symbols, 10 negative typed, 10 activity")
print("PASS five A1 weather expressions, correct έχει + noun vs impersonal verbs, no headword duplicates")
print("PASS old 339 grammar keys, chapter7 gate, SRS/weak, 10 independent sentence cards, 1700 atlas unchanged")
