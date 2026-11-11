"""Original likes/dislikes practice using ONLY Lexi's existing grammar_fill kind.

The nominated thing (not the experiencer) controls αρέσει/αρέσουν;
the genitive clitic means "to me/you/her...", NOT possessive ownership.
All answer alternatives are explicitly checked per card, no generic fuzzy rule.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/likes_dislikes_20261111.json").read_text(encoding="utf-8"))
SOURCE="independent_likes_dislikes_20261111"
LANGS=("ru","en","zh","ar","es","pt")
EXPERIENCERS=("μου","σου","του","της","μας","σας","τους")
GROUP="likes"
LABEL={
 "agreement":{
   "ru":"Выбери αρέσει или αρέσουν по числу того, что нравится, а не по человеку.",
   "en":"Choose αρέσει or αρέσουν by the number of things liked, not the person.",
   "zh":"根据被喜欢事物的单复数选择 αρέσει / αρέσουν，而非人的数量。",
   "ar":"اختر αρέσει أو αρέσουν حسب عدد الأشياء المحبوبة، لا حسب الشخص.",
   "es":"Elige αρέσει o αρέσουν según el número de lo que gusta, no de la persona.",
   "pt":"Escolhe αρέσει ou αρέσουν pelo número daquilo de que se gosta, não da pessoa."
 },
 "experiencer":{
   "ru":"Выбери, кому именно нравится предмет: μου/σου/του/της/μας/σας/τους.",
   "en":"Choose the person who likes it: μου/σου/του/της/μας/σας/τους.",
   "zh":"选择表示喜欢者的代词：μου/σου/του/της/μας/σας/τους。",
   "ar":"اختر ضمير الشخص الذي يعجبه الشيء: μου/σου/του/της/μας/σας/τους.",
   "es":"Elige el pronombre de quien siente el gusto: μου/σου/του/της/μας/σας/τους.",
   "pt":"Escolhe o pronome de quem gosta: μου/σου/του/της/μας/σας/τους."
 },
 "typed":{
   "ru":"По ситуации впиши целую греческую фразу «нравится / не нравится».",
   "en":"Use the situation to type the complete Greek phrase “likes / dislikes”.",
   "zh":"根据情境输入完整的希腊语“喜欢／不喜欢”短语。",
   "ar":"اكتب عبارة يونانية كاملة عن الإعجاب أو عدم الإعجاب وفق السياق.",
   "es":"Escribe la frase griega completa de gusto o disgusto según la situación.",
   "pt":"Escreve a expressão grega completa de preferência segundo o contexto."
 }
}
CLITIC_DISTRACTORS={
 "μου":["σου","του","μας"],
 "σου":["μου","σας","του"],
 "του":["της","τους","σου"],
 "της":["του","μας","μου"],
 "μας":["σας","μου","τους"],
 "σας":["σου","μας","τους"],
 "τους":["του","της","μας"]
}
TYPED_DISTRACTORS=(
 "Μου αρέσει","Σου αρέσουν","Της αρέσει","Δεν του αρέσουν",
 "Μας αρέσουν","Δεν σας αρέσει","Του αρέσει","Δεν μου αρέσει"
)
CARDS=[]
assert DATA["version"]==1 and len(DATA["cards"])==36
for idx,raw in enumerate(DATA["cards"],224):
    cid=f"g2261021_{idx:03d}"
    assert raw["id"]==cid
    chapter=raw["chapter"]
    assert chapter in (7,8,16)
    assert chapter>=8 if raw["number"]=="pl" else chapter>=7
    assert INDEX[chapter]["start"]<=INDEX[chapter]["end"]
    skill=raw["skill"]
    assert skill in LABEL
    prompt=raw["prompt"]
    answer=raw["correct"]
    assert prompt.count("___")==1 and prompt==unicodedata.normalize("NFC",prompt)
    assert raw["number"] in ("sg","pl")
    assert raw["experiencer"] in EXPERIENCERS
    translations=raw["translations"]
    assert set(translations)==set(LANGS) and all(
        isinstance(translations[l],str) and translations[l].strip()
        and translations[l]==unicodedata.normalize("NFC",translations[l])
        for l in LANGS
    ),cid
    if skill=="agreement":
        assert answer==("αρέσει" if raw["number"]=="sg" else "αρέσουν"),cid
        assert raw["experiencer"].casefold() in prompt.casefold(),cid
        options=["αρέσει","αρέσουν","αρέσω","αρέσεις"]
        typed=False
    elif skill=="experiencer":
        assert answer==raw["experiencer"] and answer in EXPERIENCERS,cid
        assert re.search(r"\bαρέσ(?:ει|ουν)\b",prompt),cid
        assert ("αρέσουν" in prompt)==(raw["number"]=="pl"),cid
        options=[answer,*CLITIC_DISTRACTORS[answer]]
        typed=False
    else:
        assert chapter>=16,cid
        assert raw["number"]=="pl" if "αρέσουν" in answer else raw["number"]=="sg"
        assert raw["experiencer"].casefold() in answer.casefold(),cid
        accepted=raw["accepted"]
        assert accepted and accepted[0]==answer and len(accepted)==len(set(accepted)),cid
        assert all(s==unicodedata.normalize("NFC",s) for s in accepted)
        # Only μ' αρέσει, attested colloquial clipping of μου αρέσει,
        # is explicitly authorized for the sole first-person singular card.
        if len(accepted)>1:
            assert answer=="Μου αρέσει" and set(accepted[1:])=={"Μ' αρέσει","Μ’ αρέσει"}
        options=[answer,*[v for v in TYPED_DISTRACTORS if v!=answer][:3]]
        typed=True
    assert len(options)==len(set(options))==4,cid
    card=dict(
        id=cid,kind="grammar",chapter=chapter,unit=chapter,
        page=INDEX[chapter]["start"]+min(idx%4,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
        topic="Γραμματική · Likes",group=GROUP,source=SOURCE,
        book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=answer,options=options,
        typedAnswer=typed,skill=skill,number=raw["number"],
        experiencer=raw["experiencer"],fullTranslations=translations,
        grammar_tags=[],
        **{lang:LABEL[skill][lang] for lang in LANGS}
    )
    if typed:
        card["acceptedForms"]=list(raw["accepted"])
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=chapter,cid
    CARDS.append(card)
assert len({c["id"] for c in CARDS})==len(CARDS)==36
assert len({c["prompt"] for c in CARDS})==36
assert Counter(c["skill"] for c in CARDS)=={"agreement":18,"experiencer":12,"typed":6}
assert Counter(c["chapter"] for c in CARDS)=={7:13,8:9,16:14}
BY_ID={c["id"]:c for c in CARDS}
