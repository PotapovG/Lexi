"""Original A1 weather scenarios inside Lexi's EXISTING grammar_fill cards.

The five elementary weather expressions are a closed source-of-truth. These
cards add productive and communicative practice, not duplicate word headwords,
new learner modes or any real-time weather claims. Monochrome Unicode symbols
have explicit textual Greek labels for accessibility and color independence.
"""
import json
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/weather_contexts_20261111.json").read_text(encoding="utf-8"))
SOURCE="independent_a1_weather_contexts_20261111"
LANGS=("ru","en","zh","ar","es","pt")
GROUP="weather"
LABEL={
 "symbol":{
  "ru":"По чёрно-белому символу и его названию выбери греческую фразу о погоде.",
  "en":"Use the monochrome symbol and its text label to choose the Greek weather phrase.",
  "zh":"根据黑白天气符号及文字标签，选择正确的希腊语天气表达。",
  "ar":"اختر عبارة الطقس اليونانية من الرمز الأحادي اللون واسمه المكتوب.",
  "es":"Usa el símbolo en blanco y negro y su etiqueta para elegir la expresión del tiempo.",
  "pt":"Usa o símbolo monocromático e a sua legenda para escolher a expressão meteorológica."
 },
 "negative":{
  "ru":"Символ помечен «όχι» («нет»). Самостоятельно напиши отрицательную фразу о погоде.",
  "en":"The weather symbol is marked όχι (no). Type the complete negative Greek weather phrase.",
  "zh":"天气符号标有 όχι（否）。请输入完整的希腊语天气否定句。",
  "ar":"رمز الطقس عليه علامة όχι (لا). اكتب جملة نفي كاملة باليونانية.",
  "es":"El símbolo lleva la marca όχι (no). Escribe la frase meteorológica negativa en griego.",
  "pt":"O símbolo está marcado όχι (não). Escreve a frase meteorológica negativa em grego."
 },
 "activity":{
  "ru":"По символу и повседневной ситуации выбери естественную греческую фразу о погоде.",
  "en":"Use the symbol and the everyday situation to choose a natural Greek weather phrase.",
  "zh":"根据天气符号和日常情境，选择自然的希腊语天气表达。",
  "ar":"اختر عبارة الطقس اليونانية الطبيعية حسب الرمز والموقف اليومي.",
  "es":"Elige la expresión meteorológica griega más natural según el símbolo y la situación.",
  "pt":"Escolhe a expressão meteorológica grega mais natural segundo o símbolo e a situação."
 }
}
NOUN_LABELS={
 "sun":"ήλιος","cloud":"σύννεφα","rain":"βροχή",
 "snow":"χιόνι","wind":"αέρας"
}
WEATHER={}
assert DATA["version"]==1
assert len(DATA["expressions"])==5
for item in DATA["expressions"]:
    name=item["code"]
    assert name not in WEATHER
    assert name in NOUN_LABELS
    assert item["positive"] in ("έχει ήλιο","έχει συννεφιά","βρέχει","χιονίζει","φυσάει")
    assert item["negative"]=="δεν "+item["positive"]
    assert set(item["meaning"])==set(LANGS)
    assert set(item["negativeMeaning"])==set(LANGS)
    WEATHER[name]=item
assert set(WEATHER)==set(NOUN_LABELS)
assert len({v["positive"] for v in WEATHER.values()})==5
assert len({v["negative"] for v in WEATHER.values()})==5

CARDS=[]
assert len(DATA["cards"])==30
for number,raw in enumerate(DATA["cards"],340):
    cid=f"g2261021_{number:03d}"
    assert raw["id"]==cid
    ch=raw["chapter"]
    assert ch==7 and INDEX[ch]["start"]<=INDEX[ch]["end"]
    skill=raw["skill"]
    assert skill in LABEL
    weather=raw["weather"]
    assert weather in WEATHER
    data=WEATHER[weather]
    assert raw["polarity"]==("negative" if skill=="negative" else "positive")
    word=data["negative"] if skill=="negative" else data["positive"]
    assert raw["correct"]==word,cid
    options=[word,*raw["wrong"]]
    assert len(options)==len(set(options))==4,cid
    permitted={x["negative" if skill=="negative" else "positive"] for x in WEATHER.values()}
    assert set(options)<=permitted,cid
    prompt=raw["prompt"]
    assert prompt.count("___")==1 and prompt==unicodedata.normalize("NFC",prompt)
    # Pictogram labels make tasks legible on grayscale/low-resolution phones;
    # they are already Greek A1 weather nouns, not publisher-owned images.
    assert data["symbol"]+" ("+NOUN_LABELS[weather]+")" in prompt,cid
    assert "όχι" in prompt if skill=="negative" else "όχι" not in prompt,cid
    translations=raw["translations"]
    assert set(translations)==set(LANGS)
    assert all(isinstance(translations[l],str) and translations[l].strip()
               and unicodedata.normalize("NFC",translations[l])==translations[l]
               for l in LANGS),cid
    card=dict(
        id=cid,kind="grammar",chapter=ch,unit=ch,
        page=INDEX[ch]["start"]+(number%11),
        topic="Γραμματική · Καιρός",group=GROUP,skill=skill,
        weatherCode=weather,source=SOURCE,
        book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=word,options=options,
        typedAnswer=(skill=="negative"),
        fullTranslations=translations,
        grammar_tags=["routine_and_days"],
        **{l:LABEL[skill][l] for l in LANGS}
    )
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]==7,cid
    CARDS.append(card)
assert len({c["id"] for c in CARDS})==len(CARDS)==30
assert len({c["prompt"] for c in CARDS})==30
assert Counter(c["skill"] for c in CARDS)==dict.fromkeys(LABEL,10)
assert Counter(c["weatherCode"] for c in CARDS)==dict.fromkeys(WEATHER,6)
BY_ID={c["id"]:c for c in CARDS}
