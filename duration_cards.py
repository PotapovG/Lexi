"""Original Modern Greek duration practice in Lexi's existing grammar-fill kind.

πόση ώρα -> duration of a bounded event in these contexts;
πόσο καιρό -> elapsed span of an ongoing situation in these contexts.
These questions overlap in ordinary language: not a universal minutes/years rule.
No parallel clock mode, route, backend state or private textbook material.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from textbook_alignment import INDEX
import pedagogy_rules

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/duration_a1_20261111.json").read_text(encoding="utf-8"))
LANGS=("ru","en","zh","ar","es","pt")
SOURCE="independent_duration_contexts_20261111"
GROUP="duration"
LABEL={
 "contrast":{
  "ru":"Выбери естественный вопрос по ситуации: длительность события или период до сегодняшнего дня.",
  "en":"Choose the natural question for the context: duration of one event, or a continuing period.",
  "zh":"根据语境选择自然的问法：单次活动的时长，还是持续至今的时期。",
  "ar":"اختر السؤال الملائم للسياق: مدة حدث محدد أم فترة مستمرة حتى اليوم.",
  "es":"Elige la pregunta natural: duración de un evento o período que continúa hasta hoy.",
  "pt":"Escolhe a pergunta natural: duração de um evento ou período que continua até hoje."
 },
 "unit":{
  "ru":"По карточке выбери правильное единственное/множественное число и падеж единицы длительности.",
  "en":"Use the source card to choose the correct number and case of the time unit.",
  "zh":"根据提示选择正确的时间单位单复数及格形式。",
  "ar":"اختر صيغة العدد والحالة الصحيحة لوحدة المدة وفق البطاقة.",
  "es":"Según la tarjeta, elige el número y caso correctos de la unidad de duración.",
  "pt":"Segundo o cartão, escolhe o número e caso certos da unidade de duração."
 },
 "timeline":{
  "ru":"Прочитай начало и длительность. Выбери время окончания; не путай длительность с моментом на часах.",
  "en":"Read the start and duration; choose the end time. Duration is not a clock-time point.",
  "zh":"根据开始时间和持续时长，选择结束时刻；不要混淆时长与钟点。",
  "ar":"اقرأ وقت البداية والمدة واختر وقت النهاية؛ المدة ليست ساعة محددة.",
  "es":"Lee el inicio y la duración; elige la hora de fin, no confundas duración con hora.",
  "pt":"Lê o início e a duração; escolhe a hora de fim, sem confundir duração com hora."
 },
 "typed":{
  "ru":"Введи по-гречески естественный ответ о длительности, учитывая числительное и форму существительного.",
  "en":"Type a natural Greek answer about duration, matching numeral and noun form.",
  "zh":"用希腊语输入自然的时长回答，注意数字与名词形式。",
  "ar":"اكتب جواباً يونانياً طبيعياً للمدة مع موافقة العدد والاسم.",
  "es":"Escribe una respuesta natural en griego sobre la duración con numeral y sustantivo correctos.",
  "pt":"Escreve uma resposta natural em grego sobre a duração com numeral e nome corretos."
 }
}
QUESTION_CHOICE=("Πόση ώρα","Πόσο καιρό","Τι ώρα","Πότε")
CARDS=[]
assert DATA["version"]==1 and len(DATA["questions"])==34
for n,row in enumerate(DATA["questions"],302):
    cid=f"g2261021_{n:03d}"
    assert row["id"]==cid
    chapter=row["chapter"]
    skill=row["skill"]
    prompt=row["prompt"]
    correct=row["correct"]
    assert skill in LABEL and chapter in (7,11,13)
    assert skill=="timeline" and chapter==7 or skill!="timeline"
    assert INDEX[chapter]["start"]<=INDEX[chapter]["end"]
    assert prompt.count("___")==1 and prompt==unicodedata.normalize("NFC",prompt)
    assert len(prompt)<400 and "θα " not in prompt and "χθες" not in prompt
    translations=row["translations"]
    assert set(translations)==set(LANGS)
    assert all(isinstance(translations[l],str) and translations[l].strip()
               and translations[l]==unicodedata.normalize("NFC",translations[l])
               for l in LANGS),cid
    if skill=="contrast":
        assert row["context"] in ("event","ongoing"),cid
        assert correct==("Πόση ώρα" if row["context"]=="event" else "Πόσο καιρό")
        choices=[correct,*[x for x in QUESTION_CHOICE if x!=correct]]
        typed=False
    elif skill=="unit":
        assert correct==row["unit"]
        choices=[correct,*row["wrong"]]
        typed=False
        assert len(set(choices))==4,cid
    elif skill=="timeline":
        assert row["start"] in prompt and row["end"] in correct
        start_h,start_m=map(int,row["start"].split(":"))
        end_h,end_m=map(int,row["end"].split(":"))
        assert (start_h*60+start_m+row["minutes"])%(24*60)==end_h*60+end_m,cid
        assert correct=="στις "+row["end"]
        choices=[correct,*row["wrong"]]
        typed=False
        assert len(set(choices))==4,cid
    else:
        assert skill=="typed" and chapter in (7,11,13)
        assert row["accepted"][0]==correct
        assert len(set(row["accepted"]))==len(row["accepted"])
        choices=[correct,"δύο λεπτά","τρεις ώρες","μία εβδομάδα"]
        choices=[correct,*[x for x in choices[1:] if x!=correct][:3]]
        assert len(set(choices))==4,cid
        typed=True
    assert len(choices)==4 and len(set(choices))==4 and choices[0]==correct,cid
    card=dict(
        id=cid,kind="grammar",chapter=chapter,unit=chapter,
        page=INDEX[chapter]["start"]+min(n%4,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
        topic="Γραμματική · Διάρκεια",group=GROUP,
        source=SOURCE,book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=correct,options=choices,
        typedAnswer=typed,skill=skill,fullTranslations=translations,
        grammar_tags=[],
        **{l:LABEL[skill][l] for l in LANGS}
    )
    if skill=="contrast":
        card["contextType"]=row["context"]
    elif skill=="timeline":
        card.update(startTime=row["start"],minutes=row["minutes"],endTime=row["end"])
    elif skill=="typed":
        card["acceptedForms"]=list(row["accepted"])
    else:
        card["unit"]=row["unit"]  # overloaded? overwritten below: retain course unit!
        card["unit"]=chapter
        card["durationUnit"]=row["unit"]
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=chapter,(cid,card["curriculum_ready_unit"])
    CARDS.append(card)

assert len(CARDS)==len({c["id"] for c in CARDS})==34
assert len({c["prompt"] for c in CARDS})==34
assert Counter(c["skill"] for c in CARDS)=={
    "contrast":8,"unit":10,"timeline":8,"typed":8
}
BY_ID={c["id"]:c for c in CARDS}
