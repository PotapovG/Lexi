"""Original A1 Greek consonant-cluster spelling and αυ/ευ pronunciation.

No new learner modes: these 36 original questions reuse grammar_fill. Writing
a known word is tested with the exact grapheme; listening/pronunciation uses
a visible word, not a hidden spelling or guessed audio clip. Never collapse
γκ/γγ into separate gamma phonemes or claim medial μπ/ντ/γκ are always nasal.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/consonant_patterns_20261113.json").read_text("utf-8"))
SOURCE="independent_consonant_clusters_20261113"
GROUP="consonant"
LANGS=("ru","en","zh","ar","es","pt")
CLUSTERS=("μπ","ντ","γκ","γγ","αυ","ευ","τσ","τζ")
VOICE_FORMS=("[av]","[af]","[ev]","[ef]")
VOICED_AFTER=frozenset("αεηιουωβγδζλμνρ")
VOICELESS_AFTER=frozenset("θκξπστφχψ")
WORD_DECOYS={
 "μπ":("μπ","ντ","γκ","γγ","τσ","τζ"),
 "ντ":("ντ","μπ","γκ","γγ","τσ","τζ"),
 "γκ":("γκ","γγ","μπ","ντ","τσ","τζ"),
 "γγ":("γγ","γκ","μπ","ντ","τσ","τζ"),
 "αυ":("αυ","αύ","ευ","εύ","ου","ού"),
 "ευ":("ευ","εύ","αυ","αύ","ου","ού"),
 "τσ":("τσ","τζ","ντ","γκ","μπ","γγ"),
 "τζ":("τζ","τσ","γκ","ντ","μπ","γγ")
}
LABEL={
 "spelling":{
   "ru":"Восстанови ТОЧНОЕ написание пропуска в знакомой греческой фразе. Перевод: {meaning}",
   "en":"Restore the EXACT missing Greek letters in the familiar sentence. Meaning: {meaning}",
   "zh":"按词语的正确拼写补全希腊语句子。译文：{meaning}",
   "ar":"أكمل الحروف اليونانية الناقصة وفق الإملاء الصحيح للكلمة. المعنى: {meaning}",
   "es":"Completa las letras que faltan según la ortografía EXACTA de la frase. Traducción: {meaning}",
   "pt":"Completa as letras gregas em falta, respeitando a grafia EXATA. Tradução: {meaning}"
 },
 "voicing":{
   "ru":"Прочитай видимое слово «{word}» ({meaning}) и выбери произношение αυ/ευ. Учитывай следующий звук.",
   "en":"Read “{word}” ({meaning}) and choose the pronunciation of αυ/ευ based on the following sound.",
   "zh":"阅读“{word}”（{meaning}），根据后面的音选择 αυ/ευ 的读音。",
   "ar":"اقرأ «{word}» ({meaning}) واختر نطق αυ/ευ وفق الصوت التالي.",
   "es":"Lee «{word}» ({meaning}) y elige cómo suena αυ/ευ según el sonido siguiente.",
   "pt":"Lê «{word}» ({meaning}) e escolhe o som de αυ/ευ conforme o som seguinte."
 }
}
SPELLING_RULES={
 "μπ":{
 "ru":"Начальное μπ обычно звучит как [b]; внутри слова возможны [mb] и [b] в зависимости от речи. Это не последовательность двух отдельных звуков м + п.",
 "en":"Initial μπ is usually [b]; inside words both [mb] and [b] occur in modern speech, not invariably separate m+p.",
 "zh":"词首 μπ 通常读 [b]；词中可能有 [mb] 或 [b] 的变体，不能机械地拆成两个音。",
 "ar":"يُنطق μπ أول الكلمة غالباً [b]، وفي وسطها قد يُسمع [mb] أو [b] بحسب المتحدث؛ ليس صوتين منفصلين دائماً.",
 "es":"Al inicio μπ suele sonar [b]; en el interior puede sonar [mb] o [b], no necesariamente m+p por separado.",
 "pt":"No início μπ soa geralmente [b]; no interior pode soar [mb] ou [b], não obrigatoriamente m+p separados."
 },
 "ντ":{
 "ru":"Начальное ντ часто передаёт [d]; внутри слова встречаются как [nd], так и [d]. Не навязываем один носовой вариант всем словам.",
 "en":"Initial ντ commonly represents [d]; inside a word both [nd] and [d] occur, so nasalization is not mandatory.",
 "zh":"词首 ντ 通常读 [d]；词中可读 [nd] 或 [d]，鼻音并非在所有词中都必有。",
 "ar":"غالباً ما يُنطق ντ في أول الكلمة [d]؛ وفي الوسط قد يكون [nd] أو [d]، دون إلزام بالنطق الأنفي.",
 "es":"ντ inicial suele sonar [d]; dentro de la palabra se oyen [nd] y [d], sin nasalización obligatoria.",
 "pt":"ντ inicial soa normalmente [d]; dentro da palavra surgem [nd] e [d], sem nasalização obrigatória."
 },
 "γκ":{
 "ru":"Начальное γκ часто читается [g], внутри слова возможен носовой оттенок [ŋg] или [g]; точное произношение зависит от позиции и говорящего.",
 "en":"Initial γκ is generally [g]; medial γκ may be [ŋg] or [g], depending on position and speaker.",
 "zh":"词首 γκ 通常读 [g]；词中可能读 [ŋg] 或 [g]，会因位置和说话人而不同。",
 "ar":"غالباً ما يُنطق γκ في البداية [g]، وقد يُنطق في الوسط [ŋg] أو [g] بحسب السياق والمتكلم.",
 "es":"γκ inicial suele sonar [g]; en el interior puede ser [ŋg] o [g], según la posición y el hablante.",
 "pt":"γκ inicial costuma soar [g]; no interior pode ser [ŋg] ou [g], dependendo da posição e do falante."
 },
 "γγ":{
 "ru":"В словах вроде αγγλικά сочетание γγ не читается как два независимых γ: встречается носовой [ŋg] и варианты без отчётливого носового призвука.",
 "en":"In words like αγγλικά, γγ is not two independently pronounced γ sounds: [ŋg] and less nasal variants are heard.",
 "zh":"在 αγγλικά 一类词中，γγ 不是两个独立的 γ 音；常有 [ŋg]，也可能较少鼻音。",
 "ar":"في كلمات مثل αγγλικά لا يُنطق γγ كصوتَي γ منفصلين؛ قد يُسمع [ŋg] أو نطق أقل أنفية.",
 "es":"En palabras como αγγλικά, γγ no son dos sonidos γ separados: se oye [ŋg] y también variantes menos nasales.",
 "pt":"Em palavras como αγγλικά, γγ não são dois sons γ separados: ouve-se [ŋg] e variantes menos nasais."
 },
 "αυ":{
 "ru":"αυ произносится [av] перед гласными и звонкими, [af] перед глухими согласными. Но в конкретном слове написание αυ/αύ остаётся неизменным.",
 "en":"αυ sounds [av] before a vowel or voiced sound and [af] before a voiceless consonant; spelling remains αυ/αύ in the word.",
 "zh":"αυ 在元音或浊辅音前读 [av]，在清辅音前读 [af]；词语仍按 αυ/αύ 拼写。",
 "ar":"يُنطق αυ بصوت [av] قبل حرف علة أو صوت مجهور وبصوت [af] قبل الصامت المهموس؛ تبقى كتابته αυ/αύ.",
 "es":"αυ se pronuncia [av] ante vocal o consonante sonora y [af] ante consonante sorda; se sigue escribiendo αυ/αύ.",
 "pt":"αυ soa [av] antes de vogal ou consoante sonora e [af] antes de surda; a grafia continua αυ/αύ."
 },
 "ευ":{
 "ru":"ευ перед гласным или звонким звуком читается [ev], перед глухим — [ef]. Орфография ευ/εύ остаётся той же.",
 "en":"ευ is [ev] before vowels/voiced sounds, [ef] before voiceless consonants; spelling remains ευ/εύ.",
 "zh":"ευ 在元音或浊音前读 [ev]，在清辅音前读 [ef]；拼写仍是 ευ/εύ。",
 "ar":"يُنطق ευ بصوت [ev] قبل الأصوات المجهورة وبصوت [ef] قبل المهموسة؛ وتبقى كتابته ευ/εύ.",
 "es":"ευ suena [ev] ante vocales/sonoras y [ef] ante sordas; siempre se escribe ευ/εύ.",
 "pt":"ευ soa [ev] antes de vogais/sonoras e [ef] antes de surdas; a grafia mantém-se ευ/εύ."
 },
 "τσ":{
 "ru":"τσ передаёт слитный звук [ts], как в слове τσάι; это не то же самое, что τζ [dz].",
 "en":"τσ represents the affricate [ts], as in τσάι; it differs from τζ [dz].",
 "zh":"τσ 表示 [ts] 这个塞擦音，如 τσάι，与 τζ 的 [dz] 不同。",
 "ar":"يمثل τσ الصوت المركب [ts] مثل τσάι، وهو مختلف عن τζ [dz].",
 "es":"τσ representa la africada [ts], como en τσάι, distinta de τζ [dz].",
 "pt":"τσ representa a africada [ts], como em τσάι, diferente de τζ [dz]."
 },
 "τζ":{
 "ru":"τζ передаёт [dz], как в слове τζιν; не путай его со звуком [ts], который пишется τσ.",
 "en":"τζ represents [dz], as in τζιν; do not confuse it with [ts] written τσ.",
 "zh":"τζ 表示 [dz]，如 τζιν；不要与写作 τσ 的 [ts] 混淆。",
 "ar":"يمثل τζ الصوت [dz] كما في τζιν؛ لا تخلطه مع [ts] الذي يُكتب τσ.",
 "es":"τζ representa [dz], como en τζιν; no lo confundas con [ts], que se escribe τσ.",
 "pt":"τζ representa [dz], como em τζιν; não confundas com [ts], escrito τσ."
 }
}
FOLLOW_GUIDANCE={
 "ru":"Указанная после αυ/ευ буква «{following}» относится к {class_name} звукам, поэтому сочетание в этом слове читается {correct}.",
 "en":"The sound after αυ/ευ, written «{following}», is {class_name}; thus the combination sounds {correct} in this word.",
 "zh":"αυ/ευ 后面的字母“{following}”属于{class_name}，因此这个词中的组合读作 {correct}。",
 "ar":"الصوت التالي لـ αυ/ευ المكتوب «{following}» هو {class_name}؛ لذلك النطق هنا {correct}.",
 "es":"El sonido siguiente a αυ/ευ, escrito «{following}», es {class_name}; por eso aquí suena {correct}.",
 "pt":"O som após αυ/ευ, escrito «{following}», é {class_name}; por isso aqui soa {correct}."
}
CLASS_NAMES={
 "voiced":{"ru":"звонким (или гласным)","en":"voiced (or a vowel)","zh":"浊音（或元音）","ar":"مجهوراً (أو حرف علة)","es":"sonoro (o una vocal)","pt":"sonoro (ou uma vogal)"},
 "voiceless":{"ru":"глухим","en":"voiceless","zh":"清音","ar":"مهموساً","es":"sordo","pt":"surdo"}
}

assert DATA["version"]==1 and len(DATA["wordSpelling"])==24 and len(DATA["soundReadings"])==12
assert set(WORD_DECOYS)==set(SPELLING_RULES)==set(CLUSTERS)
assert set(FOLLOW_GUIDANCE)==set(LANGS)
assert all(set(d)==set(LANGS) for d in (*SPELLING_RULES.values(),*LABEL.values(),*CLASS_NAMES.values()))
CARDS=[]
def append(raw,skill,chapter,prompt,answer,options,meanings,word,group,following=None):
    cid=f"g2261021_{458+len(CARDS):03d}"
    assert cid==raw["id"] and group in CLUSTERS and chapter in INDEX
    assert 1<=chapter<=16 and INDEX[chapter]["start"]<=INDEX[chapter]["end"]
    assert prompt.count("___")==1 and unicodedata.normalize("NFC",prompt)==prompt,cid
    assert options[0]==answer and len(options)==len(set(options))==4,cid
    assert set(meanings)==set(LANGS)
    assert all(isinstance(meanings[l],str) and meanings[l].strip() for l in LANGS),cid
    full={}
    help_text={}
    for lang in LANGS:
        if skill=="spelling":
            full[lang]=meanings[lang]
            help_text[lang]=SPELLING_RULES[group][lang]
            label=LABEL[skill][lang].format(meaning=meanings[lang])
        else:
            assert following is not None
            class_name=("voiced" if following in VOICED_AFTER else "voiceless")
            full[lang]=meanings[lang]
            help_text[lang]=(SPELLING_RULES[group][lang]+" "+
                FOLLOW_GUIDANCE[lang].format(
                    following=following,class_name=CLASS_NAMES[class_name][lang],correct=answer
                ))
            label=LABEL[skill][lang].format(word=word,meaning=meanings[lang])
        full[lang]=full[lang]
        assert unicodedata.normalize("NFC",full[lang])==full[lang]
        assert help_text[lang]
        raw.setdefault("_labels",{})[lang]=label
    card=dict(
        id=cid,kind="grammar",chapter=chapter,unit=chapter,
        page=INDEX[chapter]["start"]+min(len(CARDS)%4,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
        group=GROUP,topic="Γραμματική · Σύμφωνα και δίψηφα",skill=skill,
        family=group,source=SOURCE,
        book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=answer,options=options,
        typedAnswer=False,fullTranslations=full,fullTips=help_text,
        grammar_tags=["alphabet"],
        **raw["_labels"]
    )
    if skill=="voicing":
        # The source word is *visible* in the question: approved Pocket
        # audio lookup does not leak a masked spelling or the IPA answer.
        card["phoneticWord"]=word
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=chapter,cid
    CARDS.append(card)

for raw in DATA["wordSpelling"]:
    group=raw["group"]
    assert group in CLUSTERS and raw["skill"]=="spelling"
    word=raw["word"]
    mask=raw["masked"]
    grapheme=raw["correct"]
    assert mask.count("◇")==1 and word in mask.replace("◇",grapheme),(raw["id"],word,mask)
    assert (grapheme.casefold().replace("ά","α").replace("ύ","υ")
            ==group),(raw["id"],grapheme,group)
    decoys=WORD_DECOYS[group]
    if grapheme in ("Ευ","εύ","αύ"):
        pool=("Ευ","Εύ","Αυ","Αύ") if grapheme=="Ευ" else ("αυ","αύ","ευ","εύ","ου","ού")
    else:pool=decoys
    options=[grapheme,*[g for g in pool if g!=grapheme][:3]]
    prompt=f'Στην πρόταση: «{mask}»\nΓράμματα στο ◇: ___'
    append(raw,"spelling",raw["chapter"],prompt,grapheme,options,
           raw["translations"],word,group)

for raw in DATA["soundReadings"]:
    group=raw["group"]
    assert group in ("αυ","ευ") and raw["skill"]=="voicing"
    word=raw["word"]
    following=raw["following"].casefold()
    assert following in VOICED_AFTER|VOICELESS_AFTER,(raw["id"],following)
    # Accept the listed context fact only if the digraph is truly followed
    # by this letter in the original word; tonos/capital are normalized
    # for inspection, NEVER for scoring a written word answer.
    canon=unicodedata.normalize("NFD",word.casefold())
    canon="".join(c for c in canon if not unicodedata.combining(c))
    idx=canon.index(group)
    assert canon[idx+len(group)]==following,(raw["id"],word,following)
    expected=("v" if following in VOICED_AFTER else "f")
    assert raw["correct"]==f'[{"a" if group=="αυ" else "e"}{expected}]',(raw["id"],raw["correct"])
    prompt=f'Λέξη «{word}»\nΠώς ακούγεται το «{group}» εδώ; ___'
    append(raw,"voicing",raw["chapter"],prompt,raw["correct"],
           [raw["correct"],*[v for v in VOICE_FORMS if v!=raw["correct"]]],
           raw["translations"],word,group,following)

assert len(CARDS)==len({x["id"] for x in CARDS})==36
assert len({x["prompt"] for x in CARDS})==36
assert Counter(x["skill"] for x in CARDS)=={"spelling":24,"voicing":12}
assert Counter(x["family"] for x in CARDS if x["skill"]=="spelling")==dict.fromkeys(CLUSTERS,3)
assert Counter(x["family"] for x in CARDS if x["skill"]=="voicing")=={"αυ":6,"ευ":6}
BY_ID={x["id"]:x for x in CARDS}
