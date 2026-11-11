"""Type A present indicative: authorial typed cloze items in EXISTING grammar kind.

No standalone conjugation mode, no new route or persistence schema.
Source material supplies only learning goals, not reproduced exercise text.
"""
import json
import unicodedata
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/verb_a_present_20261111.json").read_text(encoding="utf-8"))
SOURCE="independent_type_a_present_20261111"
LANGS=("ru","en","zh","ar","es","pt")
ENDING=("ω","εις","ει","ουμε","ετε","ουν")
PERSON=("εγώ","εσύ","η Μαρία","εμείς","εσείς","αυτοί")
LABEL={
 "ru":"Впиши греческую форму глагола «{lemma}» в настоящем времени. Ударение важно.",
 "en":"Type the Greek present-tense form of “{lemma}”. Accents matter.",
 "zh":"输入希腊语动词“{lemma}”的现在时形式。注意重音符号。",
 "ar":"اكتب صيغة المضارع اليوناني للفعل «{lemma}». علامات النبر مهمة.",
 "es":"Escribe la forma griega del presente de «{lemma}». Los acentos importan.",
 "pt":"Escreve a forma grega do presente de «{lemma}». Os acentos são importantes."
}
PARADIGMS={}
assert DATA["version"]==1 and len(DATA["verbs"])==12
for row in DATA["verbs"]:
    lemma=row["lemma"]
    assert lemma not in PARADIGMS
    forms=row["forms"]
    assert len(forms)==6 and len(set(forms))==6
    assert lemma==forms[0]
    assert all(form==forms[0][:-1]+ENDING[i] for i,form in enumerate(forms)),lemma
    assert all(form==unicodedata.normalize("NFC",form) for form in forms)
    assert row["chapter"] in (2,7,8)
    PARADIGMS[lemma]=row

CARDS=[]
assert len(DATA["cards"])==36
for n,raw in enumerate(DATA["cards"],112):
    cid=f"g2261021_{n:03d}"
    assert raw["id"]==cid
    lemma=raw["lemma"]
    spec=PARADIGMS[lemma]
    person=raw["person"]
    ch=raw["chapter"]
    assert ch==spec["chapter"] and 0<=person<6
    assert raw["correct"]==spec["forms"][person]
    assert 1<=ch<=20 and INDEX[ch]["start"]<=INDEX[ch]["end"]
    prompt=raw["prompt"]
    assert prompt.casefold().startswith(PERSON[person].casefold()+" ") and prompt.count("___")==1
    assert prompt==unicodedata.normalize("NFC",prompt)
    assert raw["question"]==(prompt.endswith(";"))
    assert raw["polarity"]==("negative" if " δεν ___ " in prompt else "positive")
    assert set(raw["translations"])==set(LANGS)
    assert all(isinstance(raw["translations"][lang],str) and raw["translations"][lang].strip()
               and raw["translations"][lang]==unicodedata.normalize("NFC",raw["translations"][lang])
               for lang in LANGS),cid
    # Four distinct internal contrast answers help QA, but are never returned
    # as options for these TYPE-IN clozes.
    options=[raw["correct"]]+[
        x for x in spec["forms"] if x!=raw["correct"]
    ][:3]
    assert len(options)==len(set(options))==4
    card={
        "id":cid,"kind":"grammar","chapter":ch,"unit":ch,
        "page":INDEX[ch]["start"]+min(n%4,INDEX[ch]["end"]-INDEX[ch]["start"]),
        "topic":"Γραμματική · A","group":"verb_A",
        "source":SOURCE,"book_page_verified":False,"page_anchor_approximate":True,
        "gr":prompt,"prompt":prompt,"correct":raw["correct"],
        "options":options,"typedAnswer":True,
        "lemma":lemma,"person":person,"personName":PERSON[person],
        "fullTranslations":raw["translations"],"question":raw["question"],
        "polarity":raw["polarity"],
        "grammar_tags":[
            "address_home_present" if ch==2 else "routine_and_days" if ch==7
            else "routine_and_days"
        ],
        **{lang:LABEL[lang].format(lemma=lemma) for lang in LANGS}
    }
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=ch,(cid,card["curriculum_ready_unit"])
    CARDS.append(card)

assert len(CARDS)==36
assert len({c["id"] for c in CARDS})==36
assert {c["lemma"] for c in CARDS}==set(PARADIGMS)
assert {p:sum(c["person"]==p for c in CARDS) for p in range(6)}==dict.fromkeys(range(6),6)
BY_ID={c["id"]:c for c in CARDS}
