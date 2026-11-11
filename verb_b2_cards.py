"""Original Type B2 present-tense exercises in Lexi's EXISTING grammar_fill kind.

Explicitly declared forms and third-plural colloquial variants; no universal
normalization that would swallow stress/ending errors. Never add learner modes.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/verb_b2_present_20261111.json").read_text(encoding="utf-8"))
SOURCE="independent_type_b2_present_20261111"
LANGS=("ru","en","zh","ar","es","pt")
PERSON=("Εγώ","Εσύ","Η Μαρία","Εμείς","Εσείς","Αυτοί")
ENDINGS=("ώ","είς","εί","ούμε","είτε","ούν")
LABEL={
 "ru":"Впиши форму B2-глагола «{lemma}»: -ώ/-είς/-εί/-ούμε/-είτε/-ούν. Ударение важно.",
 "en":"Type the B2 present form of “{lemma}”: -ώ/-είς/-εί/-ούμε/-είτε/-ούν. Accents matter.",
 "zh":"输入 B2 类动词“{lemma}”的现在时：-ώ/-είς/-εί/-ούμε/-είτε/-ούν。注意重音。",
 "ar":"اكتب مضارع الفعل «{lemma}» من المجموعة B2: -ώ/-είς/-εί/-ούμε/-είτε/-ούν. النبر مهم.",
 "es":"Escribe el presente B2 de «{lemma}»: -ώ/-είς/-εί/-ούμε/-είτε/-ούν. Respeta las tildes.",
 "pt":"Escreve o presente B2 de «{lemma}»: -ώ/-είς/-εί/-ούμε/-είτε/-ούν. Respeita a acentuação."
}
PARADIGMS={}
assert DATA["version"]==1 and len(DATA["verbs"])==10
for row in DATA["verbs"]:
    lemma=row["lemma"]
    root=row["stem"]
    assert lemma not in PARADIGMS and lemma==root+"ώ",lemma
    assert row["forms"]==[root+ending for ending in ENDINGS],lemma
    assert row["chapter"] in (6,7,16,17)
    assert all(text==unicodedata.normalize("NFC",text) for text in row["forms"])
    # Only this editorial whitelist may accept the optional third-plural -ούνε.
    # No guessing suffix variants based solely on shape in the grader.
    alternatives=row["alternatives"]
    assert set(alternatives)<={"5"},lemma
    if alternatives:
        assert alternatives=={"5":[root+"ούνε"]},lemma
    PARADIGMS[lemma]=row

CARDS=[]
assert len(DATA["cards"])==40
for idx,raw in enumerate(DATA["cards"],184):
    cid=f"g2261021_{idx:03d}"
    assert raw["id"]==cid
    lemma=raw["lemma"]
    spec=PARADIGMS[lemma]
    person=raw["person"]
    chapter=raw["chapter"]
    assert chapter==spec["chapter"] and 0<=person<6
    assert INDEX[chapter]["start"]<=INDEX[chapter]["end"]
    assert raw["correct"]==spec["forms"][person]
    accepted=[raw["correct"],*spec["alternatives"].get(str(person),[])]
    assert raw["accepted"]==accepted and len(accepted)==len(set(accepted))
    prompt=raw["prompt"]
    assert prompt.startswith(PERSON[person]+" ") and prompt.count("___")==1
    assert prompt==unicodedata.normalize("NFC",prompt)
    assert raw["question"]==prompt.endswith(";")
    assert raw["polarity"]==("negative" if re.search(r"\bδεν\b",prompt) else "positive")
    assert not re.search(r"\b(?:χθες|θα)\b",prompt,re.I),cid
    # Early stages never introduce να; B2 μπορώ/προσπαθώ are intentionally 16+.
    if chapter<=7:
        assert not re.search(r"\bνα\b",prompt,re.I),cid
    translations=raw["translations"]
    assert set(translations)==set(LANGS)
    assert all(isinstance(translations[lang],str) and translations[lang].strip()
               and translations[lang]==unicodedata.normalize("NFC",translations[lang])
               for lang in LANGS),cid
    distractors=[x for x in spec["forms"] if x not in accepted][:3]
    options=[raw["correct"],*distractors]
    assert len(options)==len(set(options))==4,cid
    card=dict(
        id=cid,kind="grammar",chapter=chapter,unit=chapter,
        page=INDEX[chapter]["start"]+min(idx%4,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
        topic="Γραμματική · B2",group="verb_B2",source=SOURCE,
        book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=raw["correct"],acceptedForms=accepted,
        options=options,typedAnswer=True,lemma=lemma,person=person,
        personName=PERSON[person],fullTranslations=translations,
        question=raw["question"],polarity=raw["polarity"],grammar_tags=[],
        **{lang:LABEL[lang].format(lemma=lemma) for lang in LANGS}
    )
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=chapter,cid
    CARDS.append(card)

assert len({c["id"] for c in CARDS})==len(CARDS)==40
assert len({c["prompt"] for c in CARDS})==40
assert Counter(c["lemma"] for c in CARDS)==dict.fromkeys(PARADIGMS,4)
counts=Counter(c["person"] for c in CARDS)
assert max(counts.values())-min(counts.values())<=1 and len(counts)==6
BY_ID={c["id"]:c for c in CARDS}
