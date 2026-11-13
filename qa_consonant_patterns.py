"""Issue #5: Greek consonant clusters in the existing Lexi grammar_fill.

24 original word-specific spelling cards across 8 spellings (μπ ντ γκ γγ
αυ ευ τσ τζ), 12 vowel-consonant voicing cards (av/af/ev/ef).
Six locales, no hardcoded nasalization for internal consonants, existing
Pocket WAV lookup on visible words only, old SRS/IDs stay intact.
"""
from collections import Counter
from pathlib import Path
import tempfile
import unicodedata

import cloze_meanings
import consonant_patterns_cards as phon
import grammar2_cards
import phonetics_foundations
import server

cards=phon.CARDS
assert len(cards)==36 and len(grammar2_cards.CARDS)>=493  # issue #17 appends; all prior IDs unchanged
assert [c["id"] for c in grammar2_cards.CARDS[:457]]==[
    f"g2261021_{i:03d}" for i in range(1,458)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(458,494)
}
assert Counter(c["skill"] for c in cards)=={"spelling":24,"voicing":12}
assert Counter(c["family"] for c in cards if c["skill"]=="spelling")=={
    x:3 for x in phon.CLUSTERS
}
assert Counter(c["family"] for c in cards if c["skill"]=="voicing")=={
    "αυ":6,"ευ":6
}
assert Counter(c["correct"] for c in cards if c["skill"]=="voicing")=={
    "[av]":3,"[af]":3,"[ev]":3,"[ef]":3
}
assert len({c["prompt"] for c in cards})==36
assert len({c["phoneticWord"] for c in cards if c["skill"]=="voicing"})==12
assert all(c["curriculum_ready_unit"]<=c["chapter"] for c in cards)
assert all(c["kind"]=="grammar" and c["group"]=="consonant" for c in cards)
assert all(c["source"].startswith("independent_") and not c["book_page_verified"] for c in cards)
assert all(c["options"][0]==c["correct"] and len(set(c["options"]))==4 for c in cards)
assert all(c["typedAnswer"] is False for c in cards)
assert not any(c["kind"]=="consonant" for c in server.PRACTICE_ALL)
assert len(phonetics_foundations.CARDS)==40 and len(server.vocab.VOCAB)==1700
assert len(server.SYLLABLE_ALL)==35
assert set(phon.VOICED_AFTER).isdisjoint(phon.VOICELESS_AFTER)
assert all(c["family"]!="γγ" or c["skill"]=="spelling" for c in cards)
assert all("δύο ανεξάρτητα" not in phon.SPELLING_RULES["γγ"]["ru"]
           for _ in range(1))

# Explicit Greek orthographic claims must be grounded in each word, not
# guessed from a blanket string replacement or mandatory medial nasalization.
rows=phon.DATA["wordSpelling"]
assert len({x["word"] for x in rows})==24
for raw in rows:
    assert raw["masked"].replace("◇",raw["correct"]).find(raw["word"])>=0,raw
for raw in phon.DATA["soundReadings"]:
    word=unicodedata.normalize("NFD",raw["word"].casefold())
    word="".join(c for c in word if not unicodedata.combining(c))
    idx=word.index(raw["group"])
    assert word[idx+2]==raw["following"]
    sound=("v" if raw["following"] in phon.VOICED_AFTER else "f")
    assert raw["correct"]==f'[{"a" if raw["group"]=="αυ" else "e"}{sound}]'
assert "not invariably" in phon.SPELLING_RULES["μπ"]["en"]
assert "both [nd] and [d]" in phon.SPELLING_RULES["ντ"]["en"]
assert "[ŋg] or [g]" in phon.SPELLING_RULES["γκ"]["en"]
assert "not two independently" in phon.SPELLING_RULES["γγ"]["en"]
assert "[ts]" in phon.SPELLING_RULES["τσ"]["en"]
assert "[dz]" in phon.SPELLING_RULES["τζ"]["en"]

client=Path(__file__).with_name("app.js").read_text("utf-8")
css=Path(__file__).with_name("styles.css").read_text("utf-8")
assert '["phonetic","consonant","review_scenario"].includes(q.grammarGroup)' in client
assert 'q.kind==="grammar"&&q.grammarGroup==="consonant"' in client
assert "white-space: pre-line" in css and "overflow-wrap: anywhere" in css

with tempfile.TemporaryDirectory(prefix="lexi-consonant-") as folder:
    old_db=server.DB
    old_pepper=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"student.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        total_attempts=0
        with_audio=0
        fallback=0
        for card in cards:
            for lang in phon.LANGS:
                question=server.format_question(card,"grammar_fill",lang)
                assert question["id"]==card["id"] and question["kind"]=="grammar"
                assert question["grammarGroup"]=="consonant"
                assert question["note"]==card[lang] and question["prompt"]==card["prompt"]
                assert question["sourcePageVerified"] is False
                assert not any(k in question for k in ("correct","acceptedForms","fullTranslations","fullTips","grammarTip"))
                assert set(question["choices"])==set(card["options"])
                assert len(question["choices"])==4 and not question.get("typedAnswer")
                if card["skill"]=="voicing":
                    audio=question.get("wordAudio")
                    assert isinstance(audio,dict),card["id"]
                    assert audio["speechText"]==card["phoneticWord"]
                    assert card["phoneticWord"] in question["prompt"]
                    assert audio["audioSource"] in ("pocket","unavailable")
                    if audio["audioUrl"]:
                        assert audio["audioSource"]=="pocket"
                        assert audio["audioUrl"].startswith(("/greek/audio/","/greek/pronunciation/"))
                        with_audio+=1
                    else:
                        assert audio["audioSource"]=="unavailable"
                        fallback+=1
                else:
                    # No pre-score pronunciation metadata that would reveal
                    # the missing letters in a masked word.
                    assert "phoneticWord" not in card
                    assert "wordAudio" not in question
                user=f"con-{card['id']}-{lang}"
                right=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                total_attempts+=1
                assert right["correct"] and right["answer"]==card["correct"]
                assert right["clozeTranslation"]==card["fullTranslations"][lang]
                assert right["clozeTranslationLang"]==lang
                assert right["grammarTip"]==card["fullTips"][lang]
                assert right["clozeGreek"]==card["prompt"].replace("___",card["correct"])
                bad=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["options"][1]
                })
                total_attempts+=1
                assert not bad["correct"] and bad["answer"]==card["correct"]
                assert bad["missDebt"]==2 and bad["explanation"]==card["fullTips"][lang]

        # Exact existing weak queue, one deliberately missed word.
        example=next(c for c in cards if c["skill"]=="spelling")
        missed=server.mark("weak-consonant",{
            "id":example["id"],"direction":"grammar_fill",
            "lang":"ru","selected":example["options"][1]
        })
        total_attempts+=1
        assert not missed["correct"] and missed["missDebt"]==2
        weak=server.make_quiz("weak-consonant",{
            "scope":["chapters"],"chapters":[str(example["chapter"])],
            "types":["grammar"],"mode":["weak"],"count":["60"],"lang":["ru"]
        })
        assert any(c["id"]==example["id"] for c in weak["questions"])
        # No arbitrary count of new cards is guaranteed in a normal random
        # 60-question session; isolate each chapter's lesson source instead.
        for chapter in sorted({c["chapter"] for c in cards}):
            wanted={c["id"] for c in cards if c["chapter"]==chapter}
            excluded=",".join(c["id"] for c in server.GRAMMAR2_ALL
                              if c["chapter"]==chapter and c["id"] not in wanted)
            quiz=server.make_quiz("fresh",{
                "scope":["chapters"],"chapters":[str(chapter)],
                "types":["grammar"],"count":["60"],"lang":["ru"],
                "exclude":[excluded]
            })
            assert wanted.issubset({q["id"] for q in quiz["questions"]}),chapter
        with server.conn() as db:
            assert db.execute("PRAGMA quick_check").fetchone()[0]=="ok"
            assert db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]==total_attempts
    finally:
        server.DB=old_db
        server.auth.SECRET_FILE=old_pepper

print("PASS #5 consonants: 24 exact spelling and 12 contextual αυ/ευ voicing choices (av/af/ev/ef)")
print(f"PASS six locales, {with_audio} validated Pocket clips, {fallback} text-only question scores")
print("PASS oral variants carefully explained, 457 existing grammar IDs/35 syllables, SRS/weak unchanged")
