"""Issue #4: 5 Modern Greek vowel phonemes and original syllable division.

25 word-specific spellings, 5 phoneme -> multiple valid grapheme questions,
10 distinct A1 syllabifications. Reuse existing grammar_fill and optional
EXISTING Pocket WAV lookup; no new learner mode, audio synthesis or stress drill.
"""
from collections import Counter
from pathlib import Path
import tempfile
import unicodedata

import advanced_syllables
import cloze_meanings
import grammar2_cards
import phonetics_foundations as p
import server

cards=p.CARDS
assert len(cards)==40 and len(grammar2_cards.CARDS)>=457  # later issue #5 appends, old IDs immutable
assert [c["id"] for c in grammar2_cards.CARDS[:417]]==[
    f"g2261021_{i:03d}" for i in range(1,418)
]
assert {c["id"] for c in cards}=={
    f"g2261021_{i:03d}" for i in range(418,458)
}
assert Counter(c["skill"] for c in cards)=={
    "word":25,"sound":5,"syllables":10
}
assert Counter(c["soundCode"] for c in cards if c["skill"]=="word")==dict.fromkeys(p.SOUNDS,5)
assert all(c["group"]=="phonetic" and c["kind"]=="grammar"
           and c["source"].startswith("independent_") for c in cards)
assert len({c["prompt"] for c in cards})==40
assert all(c["curriculum_ready_unit"]<=c["chapter"] for c in cards)
assert all(not c["book_page_verified"] for c in cards)
assert all(c["correct"]==c["options"][0] and len(set(c["options"]))==4 for c in cards)
assert len(advanced_syllables.CARDS)==35
assert all(c["kind"]=="syllable" for c in advanced_syllables.CARDS)
assert not {c["phoneticWord"] for c in cards if c["skill"]=="syllables"} & {
    c["gr"] for c in advanced_syllables.CARDS
}
assert len(server.vocab.VOCAB)==1700 and server.CLOCK_COUNT==144
assert not any(c["kind"]=="phonetic" for c in server.PRACTICE_ALL)
assert all(c["id"] in server.GRAMMAR2_BY_ID for c in cards)
assert p.SOUNDS=={
    "a":("/a/",("α",)),"o":("/o/",("ο","ω")),
    "i":("/i/",("ι","η","υ","ει","οι")),
    "e":("/e/",("ε","αι")),"u":("/u/",("ου",))
}
# A free-standing phoneme can have >1 *correct* orthography. By contrast,
# the single identified word must have one exact written form.
for c in cards:
    if c["skill"]=="sound":
        assert tuple(c["acceptedForms"])==p.SOUNDS[c["soundCode"]][1]
        assert c["typedAnswer"] and not c.get("phoneticWord")
    elif c["skill"]=="word":
        assert not c["typedAnswer"]
        assert c["phoneticWord"] and not c.get("acceptedForms")
    else:
        assert c["typedAnswer"] and c["phoneticWord"]
        assert len(c["acceptedForms"])==3

client=Path(__file__).with_name("app.js").read_text("utf-8")
assert '(q.kind==="grammar"&&["phonetic","consonant"].includes(q.grammarGroup))' in client
assert 'window.LexiWordAudio?.available(q.wordAudio)' in client
assert 'wordAudioUnavailable' in client
assert 'field.lang="el"' in client
assert len([c for c in server.ALL if c["kind"]=="listening"])==0  # listening lives separately, not in main

with tempfile.TemporaryDirectory(prefix="lexi-phonetic-") as folder:
    old_db=server.DB
    old_secret=server.auth.SECRET_FILE
    server.DB=str(Path(folder)/"learner.sqlite3")
    server.auth.SECRET_FILE=Path(folder)/"login-pepper"
    try:
        server.init_db()
        total_attempts=0
        variant_scores=0
        available_audio=0
        missing_audio=0
        for card in cards:
            for lang in p.LANGS:
                q=server.format_question(card,"grammar_fill",lang)
                assert q["id"]==card["id"] and q["kind"]=="grammar"
                assert q["grammarGroup"]=="phonetic"
                assert q["note"]==card[lang] and q["prompt"]==card["prompt"]
                assert q["sourcePageVerified"] is False
                assert all(field not in q for field in
                           ("correct","acceptedForms","fullTranslations","grammarTip"))
                assert len(q["choices"])==(0 if card["typedAnswer"] else 4)
                if card["typedAnswer"]:
                    assert q["typedAnswer"] is True
                else:
                    assert set(q["choices"])==set(card["options"])
                # Audio is only the actual licensed Pocket word lookup. No fake
                # audio on sound-only isolated phonemes, or a replacement voice.
                audio=q.get("wordAudio")
                if card.get("phoneticWord"):
                    assert isinstance(audio,dict)
                    assert audio["speechText"]==card["phoneticWord"]
                    assert audio["audioSource"] in ("pocket","unavailable")
                    if audio["audioUrl"]:
                        assert audio["audioSource"]=="pocket"
                        assert audio["audioUrl"].startswith(("/greek/audio/","/greek/pronunciation/"))
                        available_audio+=1
                    else:
                        assert audio["audioSource"]=="unavailable"
                        missing_audio+=1
                else:
                    assert audio is None
                user="phonetic-"+card["id"]+"-"+lang
                good=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":card["correct"]
                })
                total_attempts+=1
                assert good["correct"] and good["answer"]==card["correct"]
                assert good["grammarTip"]==cloze_meanings.explanation(card,lang)
                assert good["clozeTranslation"]==card["fullTranslations"][lang]
                assert good["clozeTranslationLang"]==lang
                assert card["correct"] in good["clozeGreek"]
                assert not good.get("acceptedVariant",False)
                if card.get("acceptedForms"):
                    for alt in card["acceptedForms"][1:]:
                        answer=server.mark(user,{
                            "id":card["id"],"direction":"grammar_fill",
                            "lang":lang,"selected":" "+alt+" "
                        })
                        total_attempts+=1
                        variant_scores+=1
                        assert answer["correct"] and answer["acceptedVariant"]
                        assert alt in answer["clozeGreek"]
                        assert set(answer["acceptedAnswers"])==set(card["acceptedForms"])
                if card["typedAnswer"]:
                    incorrect="λα"
                else:
                    incorrect=card["options"][1]
                bad=server.mark(user,{
                    "id":card["id"],"direction":"grammar_fill",
                    "lang":lang,"selected":incorrect
                })
                total_attempts+=1
                assert not bad["correct"] and bad["missDebt"]==2
                assert bad["explanation"]==card["fullTranslations"][lang]

        assert variant_scores>0
        # Wrong skill must recur via existing weak practice with exact key.
        sample=next(c for c in cards if c["skill"]=="word")
        assert not server.mark("weak-phonetic",{
            "id":sample["id"],"direction":"grammar_fill",
            "lang":"ru","selected":sample["options"][1]
        })["correct"]
        total_attempts+=1
        weak=server.make_quiz("weak-phonetic",{
            "scope":["chapters"],"chapters":[str(sample["chapter"])],
            "types":["grammar"],"mode":["weak"],"count":["60"],"lang":["ru"]
        })
        assert any(c["id"]==sample["id"] for c in weak["questions"])
        # Preserve early chapter gating and all within-stage phonetics cards.
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
        server.auth.SECRET_FILE=old_secret

print(f"PASS issue #4: 25 word spellings + 5 phoneme aliases + 10 syllable boundaries, six locales, {variant_scores} variants")
print(f"PASS verified Pocket audio: {available_audio} scored questions with WAV, {missing_audio} text-only fallbacks; no synthesis")
print("PASS 417 old grammar IDs, 35 stress cards, SRS/weak, 1700 frozen vocab, no new modes")
