"""Type B1 present (-άω/-ώ): original typed clozes in existing grammar.

All accepted alternate answers are explicitly curated per lemma and person
in this dataset, NOT generated at grading time. No new learner mode.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/verb_b1_present_20261111.json").read_text(encoding="utf-8"))
SOURCE="independent_type_b1_present_20261111"
LANGS=("ru","en","zh","ar","es","pt")
PERSON=("Εγώ","Εσύ","Η Μαρία","Εμείς","Εσείς","Αυτοί")
CANON_ENDINGS=("άω","άς","άει","άμε","άτε","άνε")
ALT_ENDINGS={0:"ώ",2:"ά",3:"ούμε",5:"ούν"}
LABEL={
 "ru":"Введи форму глагола «{lemma}» типа B1. Варианты написания проверяются отдельно; ударение важно.",
 "en":"Type the B1 verb form for “{lemma}”. Curated variants are accepted; Greek accents matter.",
 "zh":"输入 B1 类动词“{lemma}”的变位形式。接受经核对的变体，重音必须正确。",
 "ar":"اكتب تصريف الفعل «{lemma}» من المجموعة B1. تُقبل البدائل المراجَعة، والنبر مهم.",
 "es":"Escribe la forma del verbo B1 «{lemma}». Se aceptan variantes revisadas, con acento correcto.",
 "pt":"Escreve a forma do verbo B1 «{lemma}». Aceitam-se variantes revistas; o acento importa."
}

PARADIGMS={}
assert DATA["version"]==1 and len(DATA["verbs"])==9
for row in DATA["verbs"]:
    lemma=row["lemma"]
    stem=row["stem"]
    forms=row["forms"]
    assert lemma not in PARADIGMS
    assert lemma==stem+"άω"
    assert len(forms)==6 and forms==[stem+e for e in CANON_ENDINGS],lemma
    assert row["chapter"] in (4,6,8,16)
    assert all(v==unicodedata.normalize("NFC",v) for v in forms)
    # These alternative forms were reviewed in the vocabulary source; the
    # accepted set is explicitly declared here and must not be inferred for
    # arbitrary verbs just because they have the same suffix.
    alternatives=row["alternatives"]
    assert set(alternatives)=={"0","2","3","5"},lemma
    for k,altending in ALT_ENDINGS.items():
        assert alternatives[str(k)]==[stem+altending],(lemma,k)
    PARADIGMS[lemma]=row

CARDS=[]
assert len(DATA["cards"])==36
for pos,raw in enumerate(DATA["cards"],148):
    cid=f"g2261021_{pos:03d}"
    assert raw["id"]==cid
    lemma=raw["lemma"]
    paradigm=PARADIGMS[lemma]
    ch=raw["chapter"]
    person=raw["person"]
    assert ch==paradigm["chapter"] and 0<=person<6
    assert INDEX[ch]["start"]<=INDEX[ch]["end"]
    assert raw["correct"]==paradigm["forms"][person]
    accepted=[raw["correct"],*paradigm["alternatives"].get(str(person),[])]
    assert raw["accepted"]==accepted
    assert len(accepted)==len(set(accepted))
    prompt=raw["prompt"]
    assert prompt.startswith(PERSON[person]+" ") and prompt.count("___")==1
    assert raw["question"]==prompt.endswith(";")
    assert raw["polarity"]==("negative" if re.search(r"\bδεν\b",prompt) else "positive")
    assert prompt==unicodedata.normalize("NFC",prompt)
    assert not re.search(r"\b(?:χθες|θα|να)\b",prompt,re.I) if ch<=8 else True
    meanings=raw["translations"]
    assert set(meanings)==set(LANGS) and all(
        isinstance(meanings[lang],str) and meanings[lang].strip()
        and unicodedata.normalize("NFC",meanings[lang])==meanings[lang]
        for lang in LANGS
    ),cid
    # Existing four-option grammar tests still require curated internal
    # contrasts, but they never appear in typed cloze questions.
    other_forms=[form for form in paradigm["forms"] if form not in accepted]
    options=[raw["correct"],*other_forms[:3]]
    assert len(options)==len(set(options))==4
    card={
        "id":cid,"kind":"grammar","chapter":ch,"unit":ch,
        "page":INDEX[ch]["start"]+min(pos%4,INDEX[ch]["end"]-INDEX[ch]["start"]),
        "topic":"Γραμματική · B1","group":"verb_B1",
        "source":SOURCE,"book_page_verified":False,"page_anchor_approximate":True,
        "gr":prompt,"prompt":prompt,"correct":raw["correct"],
        "acceptedForms":accepted,"options":options,"typedAnswer":True,
        "lemma":lemma,"person":person,"personName":PERSON[person],
        "fullTranslations":meanings,"question":raw["question"],"polarity":raw["polarity"],
        "grammar_tags":[
            "languages_b1_and_object_articles" if ch==4 else
            "transport_and_time" if ch==6 else
            "plural_nouns" if ch==8 else
            "subjunctive_na" if ch==16 else "routine_and_days"
        ],
        **{lang:LABEL[lang].format(lemma=lemma) for lang in LANGS}
    }
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=ch,(cid,card["curriculum_ready_unit"])
    CARDS.append(card)

assert len(CARDS)==36
assert len({c["id"] for c in CARDS})==36
assert {c["lemma"] for c in CARDS}==set(PARADIGMS)
assert Counter(c["person"] for c in CARDS)==dict.fromkeys(range(6),6)
BY_ID={c["id"]:c for c in CARDS}
