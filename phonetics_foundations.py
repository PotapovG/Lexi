"""Original Greek sound-spelling and syllable division in EXISTING grammar_fill.

The legacy 35 'syllable' tasks select STRESSED syllable; these 10 new tasks
divide different words into syllables. Greek has five vowel phonemes but some
phonemes have multiple valid spellings; sound-only cards accept ALL listed
A1 graphemes, while an identified word has one precise written form.
Never synthesize audio, remove tonos while grading, or introduce a new mode.
"""
import json
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX
from advanced_syllables import _SEGMENTED as OLD_STRESS_WORDS

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/phonetics_foundations_20261112.json").read_text("utf-8"))
SOURCE="independent_phonetics_foundations_20261112"
GROUP="phonetic"
LANGS=("ru","en","zh","ar","es","pt")
SOUNDS={
    "a":("/a/",("α",)),
    "o":("/o/",("ο","ω")),
    "i":("/i/",("ι","η","υ","ει","οι")),
    "e":("/e/",("ε","αι")),
    "u":("/u/",("ου",)),
}
LABEL={
 "word":{
 "ru":"Впиши точную пропущенную букву/буквосочетание знакомого слова «{meaning}». Звук /{sound}/ сам по себе не раскрывает орфографию.",
 "en":"Choose the exact missing letters in the familiar word “{meaning}”. The sound /{sound}/ alone does not determine spelling.",
 "zh":"为熟悉的词语“{meaning}”选择准确的缺失字母。仅凭 /{sound}/ 的读音不能确定拼写。",
 "ar":"اختر الحرف أو الحروف الناقصة في كلمة «{meaning}». صوت /{sound}/ وحده لا يكفي لمعرفة الإملاء.",
 "es":"Elige las letras que faltan en «{meaning}». El sonido /{sound}/ por sí solo no determina la ortografía.",
 "pt":"Escolhe as letras em falta na palavra «{meaning}». O som /{sound}/ não determina sozinho a grafia."
 },
 "sound":{
 "ru":"Назови ОДНО допустимое греческое написание звука /{sound}/ без ударения. Если написаний несколько, любое подойдёт.",
 "en":"Type ONE valid unaccented Greek spelling of the sound /{sound}/. Several spellings may be correct.",
 "zh":"写出 /{sound}/ 音的一种合法希腊语无重音写法。可能有多个正确答案。",
 "ar":"اكتب طريقة صحيحة واحدة لكتابة الصوت /{sound}/ باليونانية من دون علامة نبر. قد توجد عدة إجابات صحيحة.",
 "es":"Escribe UNA grafía griega válida, sin acento, del sonido /{sound}/. Puede haber varias.",
 "pt":"Escreve UMA grafia grega correta, sem acento, do som /{sound}/. Pode haver várias."
 },
 "syllables":{
 "ru":"Раздели знакомое слово «{meaning}» на слоги дефисами. Здесь не нужно угадывать ударный слог: проверяются границы слогов.",
 "en":"Divide the known word “{meaning}” into syllables with hyphens. This tests syllable boundaries, not which syllable is stressed.",
 "zh":"用连字符将熟悉的词语“{meaning}”分成音节。此题检查音节边界，不是选择重读音节。",
 "ar":"قسّم الكلمة المعروفة «{meaning}» إلى مقاطع باستخدام الشرطات. المطلوب حدود المقاطع لا اختيار المقطع المنبور.",
 "es":"Divide la palabra conocida «{meaning}» en sílabas con guiones. Se comprueban los límites, no cuál lleva el acento.",
 "pt":"Divide a palavra conhecida «{meaning}» em sílabas com hífenes. Avaliam-se os limites, não a sílaba tónica."
 }
}
EXPLAIN={
 "word":{
 "ru":"«{word}» ({meaning}) произносится со звуком {ipa}, но по правилам написания этого конкретного слова нужна «{correct}». Возможные графемы одного звука нельзя подменять друг другом.",
 "en":"“{word}” ({meaning}) uses the sound {ipa}, but this actual word is spelled with “{correct}”. Different spellings of the same sound are not interchangeable in words.",
 "zh":"“{word}”（{meaning}）包含 {ipa} 音，但这个词的正确拼写必须用“{correct}”。同音的不同写法不能在具体词语中随意替换。",
 "ar":"تحتوي «{word}» ({meaning}) على الصوت {ipa}، لكن الإملاء الصحيح لهذه الكلمة يستعمل «{correct}». لا يجوز استبدال الرسوم المتشابهة صوتياً في الكلمات.",
 "es":"«{word}» ({meaning}) tiene el sonido {ipa}, pero en esta palabra se escribe «{correct}». Las grafías que suenan igual no son intercambiables en las palabras.",
 "pt":"«{word}» ({meaning}) tem o som {ipa}, mas nesta palavra escreve-se «{correct}». Grafias do mesmo som não podem ser trocadas livremente nas palavras."
 },
 "sound":{
 "ru":"Звук {ipa} может записываться так: {choices}. Это фонема, а не название буквы; без конкретного слова все указанные варианты допустимы.",
 "en":"The phoneme {ipa} can be written {choices}. It is a sound, not a letter name; without a particular word, every listed spelling is valid.",
 "zh":"音素 {ipa} 可以写成：{choices}。这是声音而不是字母名称；未指定具体词语时，列出的写法都有效。",
 "ar":"يمكن كتابة الفونيم {ipa} بهذه الأشكال: {choices}. إنه صوت لا اسم حرف؛ ومن دون كلمة محددة تُقبل جميع هذه الأشكال.",
 "es":"El fonema {ipa} puede escribirse {choices}. Es un sonido, no el nombre de una letra; sin una palabra concreta, todas estas grafías son válidas.",
 "pt":"O fonema {ipa} pode escrever-se {choices}. É um som, não o nome de uma letra; sem palavra concreta, todas estas grafias são válidas."
 },
 "syllables":{
 "ru":"Слово «{word}» ({meaning}) делится на слоги так: {correct}. Это деление на слоги, а не отдельный тест на θέση ударения.",
 "en":"“{word}” ({meaning}) divides into syllables as {correct}. This is segmentation, not a stress-position test.",
 "zh":"“{word}”（{meaning}）的音节划分为：{correct}。这是音节切分，不是重音位置测试。",
 "ar":"تقسم كلمة «{word}» ({meaning}) إلى مقاطع هكذا: {correct}. المطلوب التقسيم لا تحديد موضع النبر.",
 "es":"«{word}» ({meaning}) se divide así: {correct}. Esto es silabificación, no una prueba de sílaba tónica.",
 "pt":"«{word}» ({meaning}) divide-se assim: {correct}. Isto é divisão silábica, não um teste de acentuação."
 }
}
assert DATA["version"]==1
assert len(DATA["phonemes"])==5 and len(DATA["wordSpelling"])==25
assert len(DATA["soundSpelling"])==5 and len(DATA["syllableDivision"])==10
assert {v["code"] for v in DATA["phonemes"]}==set(SOUNDS)
for r in DATA["phonemes"]:
    assert r["ipa"]==SOUNDS[r["code"]][0] and r["graphemes"]==list(SOUNDS[r["code"]][1])
assert Counter(x["sound"] for x in DATA["wordSpelling"])==dict.fromkeys(SOUNDS,5)
OLD_WORDS={w.replace("-","") for w in OLD_STRESS_WORDS}

CARDS=[]
def add(raw,skill,prompt,answer,options,accepted,chapter,source_word,word_meanings,sound):
    assert raw["id"]==f"g2261021_{418+len(CARDS):03d}"
    assert chapter in INDEX and 1<=chapter<=8
    assert len(options)==len(set(options))==4 and answer==options[0]
    assert len(accepted)==len(set(accepted)) and accepted[0]==answer
    assert prompt.count("___")==1 and prompt==unicodedata.normalize("NFC",prompt)
    if source_word is not None:
        assert source_word==unicodedata.normalize("NFC",source_word)
        assert set(word_meanings)==set(LANGS)
        assert all(word_meanings[l] and word_meanings[l]==unicodedata.normalize("NFC",word_meanings[l]) for l in LANGS)
    locales={}
    translations={}
    for l in LANGS:
        meaning=(word_meanings or {}).get(l,"")
        locales[l]=LABEL[skill][l].format(meaning=meaning,sound=sound or "")
        translations[l]=EXPLAIN[skill][l].format(
            word=source_word or "",meaning=meaning,correct=answer,
            ipa=SOUNDS[sound][0] if sound else "",
            choices=" / ".join(accepted)
        )
    card=dict(
        id=raw["id"],kind="grammar",chapter=chapter,unit=chapter,
        page=INDEX[chapter]["start"]+min(len(CARDS)%4,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
        topic="Γραμματική · Φθόγγοι και συλλαβές",group=GROUP,skill=skill,
        source=SOURCE,book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=answer,options=options,
        typedAnswer=skill in ("sound","syllables"),
        acceptedForms=accepted if skill in ("sound","syllables") else None,
        fullTranslations=translations,
        phoneticWord=source_word,
        soundCode=sound,
        grammar_tags=["alphabet" if skill in ("word","sound") else "stress_syllables"],
        **locales
    )
    if not card["typedAnswer"]:card.pop("acceptedForms")
    if not source_word:card.pop("phoneticWord")
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=chapter,card["id"]
    CARDS.append(card)

WORD_DECOYS={
    "a":("α","ά","ε","αι"),
    "o":("ο","ό","ω","ώ"),
    "i":("ι","ί","η","ή","υ","ύ","ει","εί","οι","οί"),
    "e":("ε","έ","αι","αί"),
    "u":("ου","ού","υ","ύ")
}
for r in DATA["wordSpelling"]:
    sound=r["sound"]
    assert sound in SOUNDS
    word=r["word"]
    mask=r["masked"]
    grapheme=r["correct"]
    assert mask.count("◇")==1 and mask.replace("◇",grapheme)==word,r["id"]
    # Correct spelling of an IDENTIFIED lexical item, unlike open-ended
    # phoneme cards: only a single grapheme is accepted here.
    assert unicodedata.normalize("NFD",grapheme)[0] in "αοωιηυε" or grapheme in ("ει","εί","οι","αι","αί","ου","ού")
    wrong=[x for x in WORD_DECOYS[sound] if x!=grapheme]
    # /a/ and /u/ have fewer orthographic variants; use contrasting sounds.
    if len(wrong)<3:wrong+=[x for x in ("ι","ο","ε","α") if x!=grapheme and x not in wrong]
    options=[grapheme,*wrong[:3]]
    add(r,"word",f'Λέξη: «{mask}» · Φθόγγος {SOUNDS[sound][0]}\nΓραφή στο ◇: ___',
        grapheme,options,[grapheme],r["chapter"],word,r["meanings"],sound)

for r in DATA["soundSpelling"]:
    sound=r["sound"]
    assert sound in SOUNDS and r["ipa"]==SOUNDS[sound][0]
    valid=list(SOUNDS[sound][1])
    assert r["accepted"]==valid and r["correct"]==valid[0]
    other=[x for x in ("α","ο","ι","ε","ου","αι","ω") if x not in valid][:3]
    options=[r["correct"],*other]
    add(r,"sound",
        f'Φθόγγος {r["ipa"]} · Γράψε ΜΙΑ σωστή γραφή, χωρίς τόνο: ___',
        r["correct"],options,valid,r["chapter"],None,None,sound)

for r in DATA["syllableDivision"]:
    word=r["word"]
    correct=r["correct"]
    assert word not in OLD_WORDS,word
    assert correct.replace("-","")==word and correct.count("-")>=1
    assert all(part for part in correct.split("-"))
    accepted=[correct,correct.replace("-","·"),correct.replace("-"," / ")]
    options=[correct,*[f"{word}{suffix}" for suffix in (";","!","?")]]
    add(r,"syllables",f'Λέξη «{word}» · Χώρισε σε συλλαβές με παύλες: ___',
        correct,options,accepted,r["chapter"],word,r["meanings"],None)

assert len(CARDS)==40 and len({c["id"] for c in CARDS})==40
assert len({c["prompt"] for c in CARDS})==40
assert Counter(c["skill"] for c in CARDS)=={"word":25,"sound":5,"syllables":10}
assert all(c["page"]>=INDEX[c["chapter"]]["start"] for c in CARDS)
BY_ID={x["id"]:x for x in CARDS}
