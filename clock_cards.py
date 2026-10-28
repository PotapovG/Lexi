"""Original A1 Greek clock-reading drills, printed chapter 6 (pp. 66-79).

Students read a 12-hour clock face and select how to say its time in Greek.
The 12-hour clock deliberately does not teach AM/PM or absolute 24h scheduling.
No audio is promised. All sentences are independently generated teaching
examples and are not transcribed from a publisher's exercises.
"""
import random

HOURS={
    1:"μία",2:"δύο",3:"τρεις",4:"τέσσερις",5:"πέντε",6:"έξι",
    7:"επτά",8:"οκτώ",9:"εννέα",10:"δέκα",11:"έντεκα",12:"δώδεκα",
}
MINUTES={
    5:"πέντε",10:"δέκα",15:"τέταρτο",20:"είκοσι",
    25:"είκοσι πέντε",30:"μισή",
}
MINUTE_VALUES=tuple(range(0,60,5))
HELP={
    "ru":"Посмотри на стрелки часов и выбери, как сказать это время по-гречески. Короткая стрелка — часы, длинная — минуты.",
    "en":"Read the hands of the clock and choose the Greek expression. Short hand: hour; long hand: minutes.",
    "zh":"看钟表指针，选择正确的希腊语时间表达。短针表示小时，长针表示分钟。",
    "ar":"اقرأ عقارب الساعة واختر التعبير اليوناني الصحيح. العقرب القصير للساعات والطويل للدقائق.",
    "es":"Lee las manecillas del reloj y elige la expresión griega. La corta indica horas y la larga minutos.",
    "pt":"Lê os ponteiros do relógio e escolhe a expressão grega. O curto indica horas e o comprido minutos.",
}
AFTER={
    "ru":"Время на часах",
    "en":"Time shown",
    "zh":"钟面时间",
    "ar":"الوقت على الساعة",
    "es":"Hora indicada",
    "pt":"Hora indicada",
}
def next_hour(hour):
    return hour%12+1

def expression(hour,minute):
    assert hour in HOURS and minute in MINUTE_VALUES
    if minute==0:
        return f"Είναι {HOURS[hour]} ακριβώς."
    if minute<=30:
        return f"Είναι {HOURS[hour]} και {MINUTES[minute]}."
    return f"Είναι {HOURS[next_hour(hour)]} παρά {MINUTES[60-minute]}."

CARDS=[]
for hour in HOURS:
    for minute in MINUTE_VALUES:
        CARDS.append(dict(
            id=f"clock_{hour:02d}_{minute:02d}",kind="clock",
            chapter=6,unit=6,page=74,curriculum="textbook",
            book_page_verified=False,
            source="original_authorial_time_drill",topic="Τι ώρα είναι;",
            hour=hour,minute=minute,gr=expression(hour,minute),
            curriculum_ready_unit=6,grammar_tags=["clock_time"],
        ))
BY_ID={c["id"]:c for c in CARDS}
BY_TIME={(c["hour"],c["minute"]):c for c in CARDS}

def options(card, rng=None):
    """Eight different Greek times with near-hour/minute distractors."""
    rng=rng or random
    hour,minute=card["hour"],card["minute"]
    pool=[card]
    # Most alternatives stay close enough to demand reading both hands.
    minutes=sorted((x for x in MINUTE_VALUES if x!=minute),
                   key=lambda x:(min(abs(x-minute),60-abs(x-minute)),rng.random()))
    for m in minutes[:4]:
        pool.append(BY_TIME[(hour,m)])
    for h in (hour%12+1,(hour-2)%12+1):
        pool.append(BY_TIME[(h,minute)])
    # One mixed-hour decoy prevents simply matching the hour hand.
    pool.append(BY_TIME[(hour%12+1,minutes[0])])
    assert len(pool)==8 and len({c["gr"] for c in pool})==8
    choices=[x["gr"] for x in pool]
    rng.shuffle(choices)
    assert card["gr"] in choices
    return choices

def validate():
    assert len(CARDS)==144 and len(BY_ID)==len(CARDS)
    assert len({c["gr"] for c in CARDS})==len(CARDS)
    assert len(HELP)==len(AFTER)==6
    for c in CARDS:
        assert c["chapter"]==6 and c["page"]==74
        assert len(set(options(c,random.Random(c["id"]))))==8
    assert expression(1,0)=="Είναι μία ακριβώς."
    assert expression(1,30)=="Είναι μία και μισή."
    assert expression(8,45)=="Είναι εννέα παρά τέταρτο."
    assert expression(12,55)=="Είναι μία παρά πέντε."
    return len(CARDS)
