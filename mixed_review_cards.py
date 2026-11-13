"""Original linked A1 role situations in Lexi's CURRENT grammar_fill kind.

Ten distinct authorial scenes x five connected steps, completely localized
across six UI languages.  The reviewed book supplies *learning goals only*,
never copied dialogue text.  No new learner mode, route or DB changes.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/mixed_review_scenarios_20261113.json").read_text(encoding="utf-8"))
SOURCE="independent_mixed_a1_review_20261113"
LANGS=("ru","en","zh","ar","es","pt")
GROUP="review_scenario"
SKILLS=("greetings","identity","possessive","verbs","dialogue","phonetics","time","weather","schedule","transport")
TIP={
 "ru":"Ситуация «{scene}», шаг {step}/5. По смыслу подходит «{correct}». {alternatives} Возвращайся к ошибке через существующий повтор.",
 "en":"Situation “{scene}”, step {step}/5. The fitting answer is “{correct}”. {alternatives} Revisit mistakes through the existing weak review.",
 "zh":"场景“{scene}”，第 {step}/5 步。正确答案是“{correct}”。{alternatives} 错题会进入现有的复习。",
 "ar":"الموقف «{scene}»، الخطوة {step}/5. الإجابة الصحيحة «{correct}». {alternatives} أعد التدريب على الخطأ عبر المراجعة الحالية.",
 "es":"Situación «{scene}», paso {step}/5. La respuesta adecuada es «{correct}». {alternatives} Repite los errores en el repaso habitual.",
 "pt":"Situação «{scene}», passo {step}/5. A resposta certa é «{correct}». {alternatives} Repete os erros na revisão existente."
}
ALT_NOTE={
 "ru":("Также принимается: {forms}.",""),
 "en":("Also accepted: {forms}.",""),
 "zh":("还接受：{forms}。",""),
 "ar":("تُقبل أيضاً: {forms}.",""),
 "es":("También se acepta: {forms}.",""),
 "pt":("Também se aceita: {forms}.","")
}
FORM_CUE={
 "ru":"Продолжи связанную ситуацию. Введи греческую форму, учитывая контекст и ударение.",
 "en":"Continue this connected situation. Type the Greek form in context, keeping accents.",
 "zh":"继续同一个情境。按语境输入希腊语形式，注意重音。",
 "ar":"تابع الموقف نفسه. اكتب الصيغة اليونانية في السياق مع مراعاة النبر.",
 "es":"Continúa la situación conectada. Escribe la forma griega según el contexto y el acento.",
 "pt":"Continua a situação ligada. Escreve a forma grega no contexto, com atenção ao acento."
}
CHOICE_CUE={
 "ru":"Продолжи тот же разговор, выбери единственный ответ по смыслу и грамматике.",
 "en":"Continue the same conversation. Choose the one contextually and grammatically correct answer.",
 "zh":"继续同一个对话。按语境和语法选择唯一正确的答案。",
 "ar":"تابع الحوار نفسه. اختر الإجابة الوحيدة المناسبة للسياق والقواعد.",
 "es":"Continúa el mismo diálogo. Elige la única respuesta adecuada por sentido y gramática.",
 "pt":"Continua o mesmo diálogo. Escolhe a única resposta adequada no sentido e na gramática."
}
EXPECTED_CHAPTERS=(1,1,2,3,4,6,6,7,7,7)
assert DATA["version"]==1 and len(DATA["scenarios"])==10
assert all(set(s["title"])==set(LANGS) for s in DATA["scenarios"])
assert tuple(s["chapter"] for s in DATA["scenarios"])==EXPECTED_CHAPTERS
assert len({s["id"] for s in DATA["scenarios"]})==10
SCENARIOS={}
CARDS=[]
for scene in DATA["scenarios"]:
    sid=scene["id"]
    assert sid not in SCENARIOS
    chapter=scene["chapter"]
    assert chapter in INDEX and 1<=chapter<=7
    steps=scene["steps"]
    assert len(steps)==5, sid
    greek=scene["sourceGreek"]
    assert isinstance(greek,str) and greek and unicodedata.normalize("NFC",greek)==greek
    # Do not sneak post-A1/7 structures into early scenarios.
    assert not re.search(r"\b(?:χθες|θα|μπορείς να|θέλω να|πρέπει να)\b",greek),sid
    record=[]
    for idx,raw in enumerate(steps):
        cid=f"g2261021_{494+len(CARDS):03d}"
        assert raw["id"]==cid,cid
        skill=raw["skill"]
        assert skill in SKILLS
        kind=raw["kind"]
        assert kind in ("typed","choice")
        prompt=raw["prompt"]
        assert prompt.count("___")==1 and unicodedata.normalize("NFC",prompt)==prompt,cid
        assert not re.search(r"\b(?:χθες|θα|μπορείς να|θέλω να|πρέπει να)\b",prompt),cid
        answer=raw["correct"]
        assert answer and unicodedata.normalize("NFC",answer)==answer,cid
        translations=raw["translations"]
        assert set(translations)==set(LANGS),cid
        assert all(isinstance(translations[l],str) and translations[l].strip()
                   and unicodedata.normalize("NFC",translations[l])==translations[l]
                   for l in LANGS),cid
        if kind=="typed":
            accepted=raw["accepted"]
            assert accepted and accepted[0]==answer
            assert len(set(accepted))==len(accepted)
            # Existing typed checks preserve tonos/case, no arbitrary token order.
            wrong=["κάνεις","μιλάμε","γράφω","πέντε","αυτό"][:3]
            wrong=[w for w in wrong if w!=answer][:3]
        else:
            assert len(raw["wrong"])==3
            accepted=[]
            wrong=raw["wrong"]
        options=[answer,*wrong]
        assert len(set(options))==4
        source=f'Μικρή σκηνή · {greek}\nΒήμα {idx+1}/5 · {prompt}'
        assert source.count("___")==1
        texts={}
        hints={}
        for lang in LANGS:
            alternatives=(ALT_NOTE[lang][0].format(forms=" / ".join(accepted[1:]))
                          if len(accepted)>1 else ALT_NOTE[lang][1])
            hints[lang]=TIP[lang].format(scene=scene["title"][lang],
                     step=idx+1,correct=answer,alternatives=alternatives)
            texts[lang]=translations[lang]
        card=dict(
            id=cid,kind="grammar",chapter=chapter,unit=chapter,
            page=INDEX[chapter]["start"]+min(idx,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
            topic="Γραμματική · Σύντομες ιστορίες",group=GROUP,
            scenarioId=sid,scenarioStep=idx+1,scenarioTotal=5,
            scenarioTitles=dict(scene["title"]),reviewSkill=skill,
            source=SOURCE,book_page_verified=False,page_anchor_approximate=True,
            gr=source,prompt=source,correct=answer,options=options,
            typedAnswer=kind=="typed",fullTranslations=texts,fullTips=hints,
            grammar_tags=[],
            **{l:(FORM_CUE if kind=="typed" else CHOICE_CUE)[l] for l in LANGS}
        )
        if kind=="typed":card["acceptedForms"]=accepted
        if skill=="phonetics" and answer=="[av]":
            card["phoneticWord"]="αύριο"
        pedagogy_rules.tag(card)
        assert card["curriculum_ready_unit"]<=chapter,cid
        CARDS.append(card)
        record.append(card)
    SCENARIOS[sid]=tuple(record)

assert len(CARDS)==50 and len({c["id"] for c in CARDS})==50
assert len({c["prompt"] for c in CARDS})==50
assert len(SCENARIOS)==10 and all(len(a)==5 for a in SCENARIOS.values())
assert all(tuple(c["scenarioStep"] for c in value)==(1,2,3,4,5)
           for value in SCENARIOS.values())
assert sum(c["typedAnswer"] for c in CARDS)>=20
assert sum(not c["typedAnswer"] for c in CARDS)>=20
assert len(set(c["reviewSkill"] for c in CARDS))>=8
BY_ID={c["id"]:c for c in CARDS}
