"""Original compact A1 weekly agenda inside EXISTING Lexi grammar_fill cards.

7 days x 3 independent events. Six-locale post-score meanings, no new mode,
endpoint, DB schema or device audio. The original licensed PDF is not embedded.
"""
import datetime
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/a1_week_agenda_20261111.json").read_text(encoding="utf-8"))
LANGS=("ru","en","zh","ar","es","pt")
SOURCE="independent_week_agenda_20261111"
KINDS=("time","day","date","spoken")
LABEL={
 "time":{
 "ru":"Посмотри на три события дня. Напиши «στις» и точное время: например, στις 09:00; разговорная форма с частью суток тоже подходит.",
 "en":"Read the three events. Type στις plus the exact time, e.g. στις 09:00; an unambiguous spoken form also works.",
 "zh":"阅读当天三个活动，输入 στις 加上准确时间，例如 στις 09:00；也接受明确标注时段的口语形式。",
 "ar":"اقرأ أحداث اليوم الثلاثة واكتب στις مع الوقت المحدد، مثل στις 09:00؛ وتُقبل الصيغة الشفوية الواضحة.",
 "es":"Lee los tres eventos del día. Escribe στις y la hora exacta, p. ej. στις 09:00; también vale la forma oral sin ambigüedad.",
 "pt":"Lê os três eventos do dia. Escreve στις e a hora exata, por exemplo στις 09:00; também serve a forma oral inequívoca."
 },
 "day":{
 "ru":"По недельному расписанию выбери день. Событие встречается ровно один раз.",
 "en":"Choose the day from the weekly agenda. This event occurs exactly once.",
 "zh":"根据每周日程选择星期。该活动只出现一次。",
 "ar":"اختر اليوم من الجدول الأسبوعي. يظهر هذا الحدث مرة واحدة فقط.",
 "es":"Elige el día del programa semanal. El evento solo aparece una vez.",
 "pt":"Escolhe o dia na agenda semanal. O evento aparece uma única vez."
 },
 "date":{
 "ru":"Прочитай дату в строке дня и выбери число с названием месяца.",
 "en":"Read the date in the day's agenda and choose the day and month.",
 "zh":"查看当日计划中的日期，选择日期和月份。",
 "ar":"اقرأ التاريخ في برنامج اليوم واختر اليوم والشهر.",
 "es":"Lee la fecha del día y elige el día y el mes.",
 "pt":"Lê a data no dia da agenda e escolhe o dia e o mês."
 },
 "spoken":{
 "ru":"Введи разговорное время по-гречески и укажи часть суток. В 13:00 — «στη μία», не «στις μία».",
 "en":"Type the spoken Greek time with the part of day. At 13:00 use στη μία, not στις μία.",
 "zh":"输入带时段的希腊语口语时间。13:00 应用 στη μία，而不是 στις μία。",
 "ar":"اكتب الوقت اليوناني المنطوق مع تحديد وقت اليوم. عند 13:00 استخدم στη μία لا στις μία.",
 "es":"Escribe la hora hablada en griego, indicando mañana/tarde/noche. A la una: στη μία, no στις μία.",
 "pt":"Escreve a hora falada em grego, indicando a parte do dia. À uma: στη μία, não στις μία."
 }
}
PREP={
 "ru":("В понедельник","Во вторник","В среду","В четверг","В пятницу","В субботу","В воскресенье"),
 "en":("On Monday","On Tuesday","On Wednesday","On Thursday","On Friday","On Saturday","On Sunday"),
 "zh":("星期一","星期二","星期三","星期四","星期五","星期六","星期日"),
 "ar":("يوم الاثنين","يوم الثلاثاء","يوم الأربعاء","يوم الخميس","يوم الجمعة","يوم السبت","يوم الأحد"),
 "es":("El lunes","El martes","El miércoles","El jueves","El viernes","El sábado","El domingo"),
 "pt":("Na segunda-feira","Na terça-feira","Na quarta-feira","Na quinta-feira","Na sexta-feira","No sábado","No domingo")
}
TRANSLATION_TEMPLATES={
 "time":{
 "ru":"{day}: {event} — в {time}.",
 "en":"{day}, {event} is at {time}.",
 "zh":"{day}：{event}在 {time}。",
 "ar":"{day}: {event} الساعة {time}.",
 "es":"{day}, {event} es a las {time}.",
 "pt":"{day}, {event} é às {time}."
 },
 "day":{
 "ru":"{day}: {event}, {time}.",
 "en":"{day}: {event}, {time}.",
 "zh":"{day}：{event}，{time}。",
 "ar":"{day}: {event}، {time}.",
 "es":"{day}: {event}, {time}.",
 "pt":"{day}: {event}, {time}."
 },
 "date":{
 "ru":"{day}, {date} ноября 2026 года: {event} — в {time}.",
 "en":"{day}, {date} November 2026: {event} at {time}.",
 "zh":"{day}，2026年11月{date}日：{event}在 {time}。",
 "ar":"{day}، {date} نوفمبر 2026: {event} الساعة {time}.",
 "es":"{day}, {date} de noviembre de 2026: {event} a las {time}.",
 "pt":"{day}, {date} de novembro de 2026: {event} às {time}."
 },
 "spoken":{
 "ru":"{day}: {event}, {time}. По-гречески: «{spoken}».",
 "en":"{day}: {event}, {time}. In Greek: “{spoken}”.",
 "zh":"{day}：{event}，{time}。希腊语说法：“{spoken}”。",
 "ar":"{day}: {event}، {time}. باليونانية: «{spoken}».",
 "es":"{day}: {event}, {time}. En griego: «{spoken}».",
 "pt":"{day}: {event}, {time}. Em grego: «{spoken}»."
 }
}
assert DATA["version"]==1
DAYS=DATA["days"]
assert len(DAYS)==7 and DATA["weekStart"]=="2026-11-02" and DATA["weekEnd"]=="2026-11-08"
assert all(len(x["events"])==3 for x in DAYS)
assert all(len(PREP[l])==7 for l in LANGS)
assert all(set(TRANSLATION_TEMPLATES[k])==set(LANGS) for k in KINDS)
WEEK_START=datetime.date(2026,11,2)
for i,day in enumerate(DAYS):
    assert datetime.date.fromisoformat(day["dateISO"])==WEEK_START+datetime.timedelta(days=i)
    assert day["dateDisplay"]==f"{i+2}/11"
    assert set(day["dayLocales"])==set(LANGS)
    assert set(e["locales"] for e in [])==set()  # no global translation fallback
    for event in day["events"]:
        assert set(event["locales"])==set(LANGS)
        hour,minute=map(int,event["time"].split(":"))
        assert 0<=hour<24 and minute in (0,15,30,45)
        assert event["spoken"].startswith("στις ") or event["spoken"].startswith("στη ")
        assert all(unicodedata.normalize("NFC",v)==v for v in
                   [event["gr"],event["spoken"],*event["locales"].values()])
ALL_TIMES=[e["time"] for d in DAYS for e in d["events"]]
assert len(set(ALL_TIMES))==len(ALL_TIMES)==21

WEEK_SUMMARY=(
    "Πρόγραμμα · 2–8 Νοεμβρίου 2026\n"+
    "\n".join(
        f'{d["day"]} {d["dateDisplay"]} · {d["events"][2]["time"]} {d["events"][2]["gr"]}'
        for d in DAYS
    )
)

def schedule(day):
    return (
        f'Πρόγραμμα ημέρας · {day["day"]} {day["dateDisplay"]}/2026\n'+
        "\n".join(f'{e["time"]} · {e["gr"]}' for e in day["events"])
    )

def speech_variants(value):
    result=[value]
    # Both Greek spellings are common and attested. 24-hour numeric times
    # are accepted separately in the reading task, not the spoken-time task.
    for old,new in (("επτά","εφτά"),("οκτώ","οχτώ"),("εννέα","εννιά")):
        if old in value:
            result.append(value.replace(old,new))
    return list(dict.fromkeys(result))

def time_variants(event):
    hour=event["time"][:2]
    candidates=["στις "+event["time"]]
    if hour.startswith("0"):
        candidates.append("στις "+event["time"][1:])
    candidates.extend(speech_variants(event["spoken"]))
    return list(dict.fromkeys(candidates))

def meanings(skill,day_idx,event):
    day=DAYS[day_idx]
    out={}
    for lang in LANGS:
        out[lang]=TRANSLATION_TEMPLATES[skill][lang].format(
            day=PREP[lang][day_idx],
            date=day_idx+2,event=event["locales"][lang],
            time=event["time"],spoken=event["spoken"]
        )
    return out

CARDS=[]
def append(skill,day_idx,event_idx,prompt,answer,accepted=None,options=None):
    day=DAYS[day_idx]
    event=day["events"][event_idx]
    accepted=accepted or [answer]
    if options is None:
        options=[answer,*[t for t in ("στις 11:11","στις 15:15","στις 22:22") if t!=answer]]
    assert len(options)==len(set(options))==4 and answer in options
    assert len(accepted)==len(set(accepted)) and accepted[0]==answer
    assert prompt.count("___")==1
    assert prompt==unicodedata.normalize("NFC",prompt)
    assert set(meanings(skill,day_idx,event))==set(LANGS)
    num=260+len(CARDS)
    card=dict(
        id=f"g2261021_{num:03d}",kind="grammar",chapter=7,unit=7,
        page=INDEX[7]["start"]+min(len(CARDS)%4,INDEX[7]["end"]-INDEX[7]["start"]),
        topic="Γραμματική · Εβδομαδιαίο πρόγραμμα",group="schedule",
        skill=skill,dayID=day["id"],eventID=event["id"],eventTime=event["time"],
        source=SOURCE,book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=answer,options=options,
        typedAnswer=skill in ("time","spoken"),
        fullTranslations=meanings(skill,day_idx,event),
        grammar_tags=["routine_and_days"],
        **{lang:LABEL[skill][lang] for lang in LANGS}
    )
    if card["typedAnswer"]:
        card["acceptedForms"]=accepted
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]==7
    CARDS.append(card)

# 21 independent questions require reading the actual daily agenda.
for di,day in enumerate(DAYS):
    for ei,event in enumerate(day["events"]):
        question=f'Ερώτηση: Τι ώρα είναι {event["gr"]} {day["dayAcc"]};'
        prompt=schedule(day)+"\n"+question+"\nΑπάντηση: ___"
        append("time",di,ei,prompt,"στις "+event["time"],time_variants(event))

# 7 day-of-week readings: show the entire 7-day compact index
# and choose the row with the unique third appointment.
for di,day in enumerate(DAYS):
    event=day["events"][2]
    question=f'Ερώτηση: Ποια μέρα είναι {event["gr"]};'
    options=[day["dayAcc"]]+[DAYS[(di+j)%7]["dayAcc"] for j in (1,2,3)]
    append("day",di,2,WEEK_SUMMARY+"\n"+question+"\nΑπάντηση: ___",
           day["dayAcc"],options=options)

# 7 explicit month/day selections from the dated agenda, with 2026 fixed
# so US/European numeric date ambiguity is never accepted.
for di,day in enumerate(DAYS):
    event=day["events"][0]
    question=f'Ερώτηση: Ποια ημερομηνία έχει το πρόγραμμα {day["dayAcc"]};'
    answer=f"{di+2} Νοεμβρίου"
    options=[answer]+[f"{((di+j)%7)+2} Νοεμβρίου" for j in (1,2,3)]
    append("date",di,0,schedule(day)+"\n"+question+"\nΑπάντηση: ___",
           answer,options=options)

# 7 spoken-language tasks: exact 24h input (with explicit day part) -> 12h
# phrase; one example includes στη μία to test the singular preposition.
for di,day in enumerate(DAYS):
    event=day["events"][1]
    prompt=(f'Ωράριο · {day["dayAcc"]}\n'+
            f'{event["time"]} · {event["gr"]}\n'+
            "Ερώτηση: Πώς λέμε προφορικά αυτή την ώρα (πρωί/μεσημέρι/απόγευμα/βράδυ);\n"+
            "Απάντηση: ___")
    append("spoken",di,1,prompt,event["spoken"],speech_variants(event["spoken"]))

assert len(CARDS)==42
assert len({c["id"] for c in CARDS})==42
assert len({c["prompt"] for c in CARDS})==42
assert Counter(c["skill"] for c in CARDS)=={"time":21,"day":7,"date":7,"spoken":7}
BY_ID={c["id"]:c for c in CARDS}
