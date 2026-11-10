"""Issue #6: independent A1 dialogues in the existing gap mode only."""
from pathlib import Path
import re
import tempfile

import server
import dialogues_a1_expansion as extra
import dialogue_full
import dialogue_translations

new = extra.CARDS
all_dialogues = [c for c in server.ALL if c["kind"] == "dialogue"]
assert len(new) == 12
assert len(all_dialogues) == 112
assert len({c["id"] for c in all_dialogues}) == len(all_dialogues)
assert set(c["id"] for c in new) == {f"dlg{i:03d}" for i in range(101, 113)}
assert len([c for c in all_dialogues if c["source"] != extra.SOURCE]) == 100
assert len(server.vocab.VOCAB) == 1700
assert dialogue_full.validate(server.ALL) == 112
assert dialogue_translations.validate(server.ALL) == 112
assert set(extra.LANGUAGES) == {"ru", "en", "zh", "ar", "es", "pt"}
assert all(c["curriculum_ready_unit"] <= c["chapter"] for c in new)
assert all(len(c["bank"]) == len(set(c["bank"])) == 8 for c in new)
assert all(len(c["gaps"]) == 2 and len(c["lines"]) == 4 for c in new)
assert all(c["kind"] == "dialogue" and c["book_page_verified"] is False for c in new)
assert all(not re.search(r"\b(?:θα|ήρθα|ήμουν|πρέπει να|θέλω να)\b", c["gr"], re.I) for c in new)

with tempfile.TemporaryDirectory(prefix="lexi-a1-dialogues-") as temp:
    previous_db = server.DB
    previous_secret = server.auth.SECRET_FILE
    server.DB = str(Path(temp) / "learner.sqlite3")
    server.auth.SECRET_FILE = Path(temp) / "login-pepper"
    try:
        server.init_db()
        for card in new:
            for lang in extra.LANGUAGES:
                question = server.format_question(card, "gap0", lang)
                assert question["kind"] == "dialogue"
                assert question["dialogueLines"] == card["lines"]
                assert question["gapIndices"] == [0, 1]
                assert set(question["choices"]) == set(card["bank"])
                assert "dialogueFullTemplate" not in question
                owner = f"qa-{card['id']}-{lang}"
                for i, correct in enumerate(card["gaps"]):
                    direction = f"gap{i}"
                    result = server.mark(owner, {
                        "id": card["id"], "direction": direction,
                        "lang": lang, "selected": correct
                    })
                    assert result["correct"] and result["answer"] == correct
                    assert result["dialogueFullLang"] == lang
                    assert result["dialogueFullTemplate"] == card["locales"][lang]["lines"]
                    assert result["dialogueFullGlosses"][correct] == card["locales"][lang]["glosses"][i]
                    assert result["translation"] == card["locales"][lang]["glosses"][i]
                incorrect = server.mark(owner, {
                    "id": card["id"], "direction": "gap0",
                    "lang": lang, "selected": "WRONG"
                })
                assert not incorrect["correct"]
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0] == "ok"
    finally:
        server.DB = previous_db
        server.auth.SECRET_FILE = previous_secret

print("PASS: 12 new authorial A1 conversations, 24 gaps x 6 locales, scoring + explanations")
print("PASS: 100 legacy dialogue IDs preserved, no new exercise kinds or modes, 1700 vocab IDs frozen")
