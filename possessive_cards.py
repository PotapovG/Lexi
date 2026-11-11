"""A1 possessive cloze content using the existing Lexi grammar question kind.

Only independent Greek examples, original translations, and existing
enclitic stress guidance. No additional user-facing lesson mode or UI.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import enclitic_stress
import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
SOURCE="independent_possessive_cloze_20261111"
LANGS=("ru","en","zh","ar","es","pt")
PATH=ROOT/"content/grammar/possessives_a1_20261111.json"
RAW=json.loads(PATH.read_text(encoding="utf-8"))

OWNER_TO_FORM={
 "mine":"μου",
 "yours":"σου",
 "his":"του",
 "hers":"της",
 "ours":"μας",
 "yours_formal":"σας",
 "theirs":"τους",
}
LABEL={
 "ru":"Выбери притяжательное местоимение по владельцу предмета.",
 "en":"Choose the possessive pronoun that identifies the owner.",
 "zh":"根据物品的拥有者选择正确的物主代词。",
 "ar":"اختر ضمير الملكية المناسب لصاحب الشيء.",
 "es":"Elige el posesivo que corresponde a quien posee el objeto.",
 "pt":"Escolhe o possessivo que identifica o dono do objeto.",
}
CARDS=[]
assert isinstance(RAW,list) and len(RAW)==35
for pos,raw in enumerate(RAW,77):
    cid=f"g2261021_{pos:03d}"
    owner=raw["owner"]
    assert owner in OWNER_TO_FORM and raw["correct"]==OWNER_TO_FORM[owner],cid
    assert raw["id"]==cid
    ch=raw["chapter"]
    assert ch in (2,3) and INDEX[ch]["start"]<=raw["page"]<=INDEX[ch]["end"],cid
    options=[raw["correct"],*raw["wrong"]]
    assert len(options)==len(set(options))==4 and set(options)<=set(OWNER_TO_FORM.values()),cid
    prompt=raw["prompt"]
    assert prompt.count("___")==1 and prompt==unicodedata.normalize("NFC",prompt),cid
    assert "μου αρέσει" not in prompt and not re.search(r"\\b(?:να|θα)\\b",prompt),cid
    translations=raw["fullTranslations"]
    assert set(translations)==set(LANGS) and all(
        isinstance(translations[lang],str) and translations[lang].strip()
        for lang in LANGS
    ),cid
    stress=raw.get("stressNoun")
    if stress:
        assert stress["article"]=="το" and stress["noun"]=="τηλέφωνο"
        assert stress["rendered"]==enclitic_stress.add_final(stress["noun"]),cid
        assert any(
            (a,n,accented)==(stress["article"],stress["noun"],stress["rendered"])
            and extra
            for a,n,accented,_unit,extra in enclitic_stress.BASES
        ),cid
        assert stress["rendered"]+" ___" in prompt,cid

    card={
        "id":cid, "kind":"grammar", "chapter":ch, "unit":ch, "page":raw["page"],
        "topic":"Γραμματική · possessive", "group":"possessive",
        "source":SOURCE, "book_page_verified":False, "page_anchor_approximate":True,
        "gr":prompt,"prompt":prompt,"correct":raw["correct"],
        "options":options,"owner":owner,"possessedNoun":raw["noun"],
        "fullTranslations":translations,"grammar_tags":[
            "address_home_present" if ch==2 else "family_profession_question"
        ],
        **{lang:LABEL[lang] for lang in LANGS}
    }
    if stress:
        card["stressNoun"]=stress
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=ch,(cid,card["curriculum_ready_unit"])
    CARDS.append(card)

assert len(CARDS)==35 and len({c["id"] for c in CARDS})==35
assert Counter(c["correct"] for c in CARDS)==dict.fromkeys(OWNER_TO_FORM.values(),5)
BY_ID={c["id"]:c for c in CARDS}
