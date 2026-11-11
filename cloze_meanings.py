"""Curated post-answer translations for original article and grammar cloze cards.

Only returned after scoring, never in a quiz question. The translations give
the meaning of the *complete corrected sentence*, not a word-by-word literal
gloss of the article. Other UI languages use an explicitly labelled English
fallback until independently reviewed translations are available.
"""
from grammar2_cards import CARDS as GRAMMAR
from form_exercises import ARTICLES

ARTICLE_RU = """
Я живу в Никосии.
Петрос живёт в Афинах.
Никос живёт в Пирее.
Катерина живёт дома.
Мы живём на Кипре.
Мой друг живёт в Строволосе.
У тебя есть друг в Греции?
Телефон находится дома.
Моя мама — учительница.
Мой папа — врач.
Ребёнок живёт в Афинах.
Моя сестра — студентка.
Ты знаешь Никоса?
Ты знаешь Марию?
Ты знаешь Анну?
Я вижу преподавателя.
Я не понимаю это слово.
Ты знаешь этого ребёнка?
Я ищу своего отца.
Элени знает твою подругу.
Я покупаю хлеб.
Я хочу газету.
Я беру сахар.
Я покупаю молоко.
"""
ARTICLE_EN = """
I live in Nicosia.
Petros lives in Athens.
Nikos lives in Piraeus.
Katerina lives at home.
We live in Cyprus.
My friend lives in Strovolos.
Do you have a friend in Greece?
The phone is at home.
My mother is a teacher.
My father is a doctor.
The child lives in Athens.
My sister is a university student.
Do you know Nikos?
Do you know Maria?
Do you know Anna?
I see the teacher.
I don't understand the word.
Do you know the child?
I'm looking for my father.
Eleni knows your female friend.
I'm buying the bread.
I want the newspaper.
I'm taking the sugar.
I'm buying the milk.
"""
GRAMMAR_RU = """
Я вижу своего друга.
Я разговариваю со своей подругой.
Это дом моего друга.
Я даю книгу своей маме.
Где дети?
Я вижу женщин.
Машина моего отца.
Друзья Анны.
Мария видит учителя.
Книга принадлежит ученику.
Хороший друг здесь.
Хорошая ученица читает.
Маленький дом находится там.
Хорошие друзья приходят.
Хорошие подруги разговаривают.
Маленькие дети играют.
У меня есть большая сумка.
Я вижу хорошего учителя.
Мы разговариваем с маленькой девочкой-подругой.
Большие двери открыты.
Этот дом больше того.
Анна выше Марии.
Никос младше Петроса.
Эта машина быстрее другой.
Эта комната меньше кухни.
Эта сумка дороже той.
Мой брат старше меня.
Эта обувь дешевле той.
Город больше деревни.
Автобус медленнее велосипеда.
Вчера я ходил в музей.
Вчера мы смотрели фильм.
В субботу я остался дома.
Позавчера Мария купила книгу.
Вчера мои друзья приехали в Афины.
В прошлом году я был на Кипре.
Вчера вечером мы ели в таверне.
В воскресенье Никос проснулся рано.
Вчера Анна написала письмо.
Вчера утром я пил кофе.
Завтра я приду.
Мы останемся дома.
Мария купит книгу.
Они посмотрят фильм.
Я буду говорить по-гречески.
Ты напишешь письмо.
Мы поедим вместе.
Вы выпьете кофе.
Я хочу выучить греческий.
Ты можешь прийти сюда?
Нам нужно уйти сейчас.
Я хочу выпить воды.
Мы предпочитаем остаться дома.
Мне нужно поговорить с врачом.
Вы можете прочитать книгу?
Хочешь посмотреть фильм?
"""
GRAMMAR_EN = """
I see my friend.
I talk with my female friend.
This is my friend's house.
I give the book to my mother.
Where are the children?
I see the women.
My father's car.
Anna's friends.
Maria sees the teacher.
The book belongs to the student.
The good friend is here.
The good female student is reading.
The small house is over there.
The good friends are coming.
The good female friends are speaking.
The small children are playing.
I have a big bag.
I see the good teacher.
We are speaking with our younger female friend.
The big doors are open.
This house is bigger than that one.
Anna is taller than Maria.
Nikos is younger than Petros.
This car is faster than the other one.
The room is smaller than the kitchen.
This bag is more expensive than that one.
My brother is older than me.
These shoes are cheaper than those.
The city is bigger than the village.
The bus is slower than the bicycle.
Yesterday I went to the museum.
Yesterday we watched a film.
On Saturday I stayed at home.
The day before yesterday Maria bought a book.
Yesterday my friends came to Athens.
Last year I was in Cyprus.
Yesterday evening we ate at a tavern.
On Sunday Nikos woke up early.
Yesterday Anna wrote a letter.
Yesterday morning I drank coffee.
I will come tomorrow.
We will stay at home.
Maria will buy a book.
They will watch a film.
I will speak Greek.
You will write the letter.
We will eat together.
You will drink coffee.
I want to learn Greek.
Can you come here?
We need to leave now.
I want to drink water.
We prefer to stay at home.
I need to speak to the doctor.
Can you read the book?
Do you want to watch a film?
"""

# Independent issue #7 gender-cloze meanings are shown only after grading.
GRAMMAR_RU = GRAMMAR_RU.rstrip() + "\n" + "Дом находится в городе.\nДруг живёт в деревне.\nПодруга живёт в городе.\nМобильный телефон находится дома.\nМама — учительница.\nПапа — водитель.\nРебёнок живёт в Афинах.\nДвоюродный брат — инженер.\nДвоюродная сестра — студентка.\nМальчик родом с Кипра.\nВрач — моя сестра.\nДочь — студентка.\nГречанка говорит по-гречески.\nГрек знает английский.\nУченица говорит по-немецки.\nУченик говорит по-русски.\nМаркер находится на столе.\nСтраница находится в книге.\nВаза находится дома.\nЗажигалка находится в сумке."
GRAMMAR_EN = GRAMMAR_EN.rstrip() + "\n" + "The house is in the city.\nThe male friend lives in the village.\nThe female friend lives in the city.\nThe mobile phone is at home.\nThe mother is a teacher.\nThe father is a driver.\nThe child lives in Athens.\nThe male cousin is an engineer.\nThe female cousin is a university student.\nThe boy is from Cyprus.\nThe female doctor is my sister.\nThe daughter is a university student.\nThe Greek woman speaks Greek.\nThe Greek man knows English.\nThe schoolgirl speaks German.\nThe schoolboy speaks Russian.\nThe marker pen is on the table.\nThe page is in the book.\nThe vase is at home.\nThe lighter is in the bag."

# The first 10 grammar exercises contrast case and article forms, not merely
# vocabulary. Give a real grammatical reason instead of repeating the prompt.
CASE_RU = (
    "τον — мужской род, винительный падеж, единственное число: кого я вижу.",
    "τη — женский род, винительный падеж, единственное число, после предлога με.",
    "του — родительный падеж, мужской род, единственное число: чей дом.",
    "στη — сокращение σε + τη; направление действия к маме, женский род.",
    "τα — именительный падеж, множественное число, средний род.",
    "τις — винительный падеж, множественное число, женский род.",
    "του — родительный падеж, мужской род, единственное число: чья машина.",
    "της — родительный падеж, женский род, единственное число: чьи друзья.",
    "τον — мужской род, винительный падеж: кого видит Мария.",
    "του — родительный падеж, мужской род, единственное число; обозначает принадлежность ученику.",
)
CASE_EN = (
    "τον — masculine singular accusative: the direct object of 'see'.",
    "τη — feminine singular accusative after the preposition με.",
    "του — masculine singular genitive: possession ('whose house').",
    "στη — a contraction of σε + τη, marking the recipient (mother).",
    "τα — neuter plural nominative: subject of the question.",
    "τις — feminine plural accusative: direct object.",
    "του — masculine singular genitive: possession ('whose car').",
    "της — feminine singular genitive: possession ('whose friends').",
    "τον — masculine singular accusative: direct object of 'sees'.",
    "του — masculine singular genitive, indicating the student's ownership.",
)

def _rows(text):
    return tuple(x.strip() for x in text.strip().splitlines())

TABLES={
    "article":{"ru":_rows(ARTICLE_RU),"en":_rows(ARTICLE_EN)},
    "grammar":{"ru":_rows(GRAMMAR_RU),"en":_rows(GRAMMAR_EN)}
}
KINDS={"article":ARTICLES,"grammar":GRAMMAR}

def validate():
    for kind,cards in KINDS.items():
        for lang in ("ru","en"):
            lines=TABLES[kind][lang]
            legacy=[c for c in cards if c.get("group") not in ("possessive","verb_A","verb_B1","verb_B2","likes","schedule","duration","weather","verb_core")] if kind=="grammar" else cards
            assert len(lines)==len(legacy),(kind,lang,len(lines),len(legacy))
            assert all(lines),(kind,lang)
    assert len(ARTICLES)==24 and len(GRAMMAR)==417
    assert len(CASE_RU)==len(CASE_EN)==10
    return sum(len(cards) for cards in KINDS.values())

def translation(card,lang):
    if card["kind"]=="grammar" and card.get("group")=="verb_core":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="weather":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="duration":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="schedule":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="likes":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="verb_B2":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="verb_B1":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="verb_A":
        return card["fullTranslations"][lang],lang
    if card["kind"]=="grammar" and card.get("group")=="possessive":
        # Newly authored complete sentence glosses for all six locales.
        # Do not show any English fallback for this new content.
        return card["fullTranslations"][lang],lang
    kind=card["kind"]
    assert kind in TABLES
    number=(int(card["id"].split("_")[-1])-1)
    used=lang if lang in ("ru","en") else "en"
    assert KINDS[kind][number]["id"]==card["id"]
    return TABLES[kind][used][number],used

GENDER_EXPLANATIONS={
 "ru":{"Ο":"Ο — мужской род, именительный падеж, единственное число.",
       "Η":"Η — женский род, именительный падеж, единственное число.",
       "Το":"Το — средний род, именительный падеж, единственное число."},
 "en":{"Ο":"Ο — masculine singular nominative article.",
       "Η":"Η — feminine singular nominative article.",
       "Το":"Το — neuter singular nominative article."},
 "zh":{"Ο":"Ο — 阳性单数主格冠词。","Η":"Η — 阴性单数主格冠词。","Το":"Το — 中性单数主格冠词。"},
 "ar":{"Ο":"Ο — أداة التعريف للمفرد المذكر في حالة الرفع.",
       "Η":"Η — أداة التعريف للمفرد المؤنث في حالة الرفع.",
       "Το":"Το — أداة التعريف للمفرد المحايد في حالة الرفع."},
 "es":{"Ο":"Ο — artículo nominativo masculino singular.",
       "Η":"Η — artículo nominativo femenino singular.",
       "Το":"Το — artículo nominativo neutro singular."},
 "pt":{"Ο":"Ο — artigo nominativo masculino singular.",
       "Η":"Η — artigo nominativo feminino singular.",
       "Το":"Το — artigo nominativo neutro singular."}
}


POSSESSIVE_GUIDANCE={
 "ru":"«{form}» обозначает владельца: {owner}. Притяжательная форма зависит от владельца, а не от рода предмета. Это принадлежность, не конструкция «μου αρέσει».",
 "en":"“{form}” identifies the owner: {owner}. The owner, not the noun’s gender, determines the possessive. This is ownership, not the “μου αρέσει” construction.",
 "zh":"“{form}”表示拥有者：{owner}。物主形式取决于拥有者，而不是物品名词的性；这里不是“μου αρέσει”结构。",
 "ar":"«{form}» يدل على صاحب الشيء: {owner}. صيغة الملكية تتبع المالك لا جنس الاسم؛ وليست هنا صيغة «μου αρέσει».",
 "es":"«{form}» indica quién es el propietario: {owner}. La forma posesiva depende del propietario, no del género del objeto; aquí no es «μου αρέσει».",
 "pt":"«{form}» identifica o dono: {owner}. A forma possessiva depende de quem possui o objeto, não do género do nome; aqui não é «μου αρέσει»."
}
POSSESSIVE_OWNER={
 "mine":{
 "ru":"говорящий (я)",
 "en":"the speaker (I)",
 "zh":"说话者（我）",
 "ar":"المتكلم (أنا)",
 "es":"quien habla (yo)",
 "pt":"quem fala (eu)"
},
 "yours":{
 "ru":"собеседник на «ты»",
 "en":"the person addressed informally (you)",
 "zh":"被非正式称呼的人（你）",
 "ar":"المخاطب بصيغة المفرد غير الرسمية",
 "es":"la persona a la que se habla de tú",
 "pt":"a pessoa tratada por tu"
},
 "his":{
 "ru":"Никос (мужчина)",
 "en":"Nikos (he)",
 "zh":"尼科斯（他）",
 "ar":"نيكوس (هو)",
 "es":"Nikos (él)",
 "pt":"o Nikos (ele)"
},
 "hers":{
 "ru":"Мария (женщина)",
 "en":"Maria (she)",
 "zh":"玛丽亚（她）",
 "ar":"ماريا (هي)",
 "es":"María (ella)",
 "pt":"a Maria (ela)"
},
 "ours":{
 "ru":"говорящий и его группа (мы)",
 "en":"the speaker and their group (we)",
 "zh":"说话者与其同伴（我们）",
 "ar":"المتكلم ومجموعته (نحن)",
 "es":"quien habla y su grupo (nosotros)",
 "pt":"quem fala e o seu grupo (nós)"
},
 "yours_formal":{
 "ru":"собеседник на вежливое «вы»",
 "en":"the person addressed politely (you)",
 "zh":"被礼貌称呼的人（您）",
 "ar":"المخاطب بصيغة الاحترام (أنتم)",
 "es":"la persona tratada de usted",
 "pt":"a pessoa tratada com formalidade"
},
 "theirs":{
 "ru":"Никос и Мария вместе (они)",
 "en":"Nikos and Maria together (they)",
 "zh":"尼科斯和玛丽亚（他们）",
 "ar":"نيكوس وماريا معًا (هم)",
 "es":"Nikos y María juntos (ellos)",
 "pt":"o Nikos e a Maria juntos (eles)"
}
}

def _possessive_explanation(card,lang):
    from enclitic_stress import EXPLANATIONS as STRESS_GUIDANCE
    message=POSSESSIVE_GUIDANCE[lang].format(
        form=card["correct"],owner=POSSESSIVE_OWNER[card["owner"]][lang]
    )
    if card.get("stressNoun"):
        info=card["stressNoun"]
        stress=STRESS_GUIDANCE[lang][0].format(
            noun=info["noun"],pronoun=card["correct"],
            correct=f'{info["article"]} {info["rendered"]} {card["correct"]}'
        )
        message += " " + stress
    return message


VERB_A_ENDINGS=("ω","εις","ει","ουμε","ετε","ουν")
VERB_A_TIPS={
 "ru":"Лицо: {person}; глагол «{lemma}», основа «{root}» + окончание «-{ending}» → «{correct}». Ударение сохраняется; «δεν» не меняет спряжение.",
 "en":"Person: {person}; verb “{lemma}”, stem “{root}” + ending “-{ending}” → “{correct}”. Keep the Greek accent; δεν does not change conjugation.",
 "zh":"人称：{person}；动词“{lemma}”，词干“{root}”加词尾“-{ending}”→“{correct}”。注意重音；δεν 不改变变位。",
 "ar":"الشخص: {person}؛ الفعل «{lemma}»، الجذر «{root}» + النهاية «-{ending}» ← «{correct}». حافظ على النبر؛ «δεν» لا يغيّر التصريف.",
 "es":"Persona: {person}; verbo «{lemma}», raíz «{root}» + terminación «-{ending}» → «{correct}». Conserva la tilde griega; «δεν» no cambia la conjugación.",
 "pt":"Pessoa: {person}; verbo «{lemma}», radical «{root}» + terminação «-{ending}» → «{correct}». Mantém o acento grego; «δεν» não altera a conjugação."
}
VERB_A_PERSONS={
 "ru":["я, 1-е ед.ч.","ты, 2-е ед.ч.","Мария, 3-е ед.ч.","мы, 1-е мн.ч.","вы, 2-е мн.ч.","они, 3-е мн.ч."],
 "en":["I, 1st singular","you, 2nd singular","Maria, 3rd singular","we, 1st plural","you, 2nd plural","they, 3rd plural"],
 "zh":["我，第一人称单数","你，第二人称单数","玛丽亚，第三人称单数","我们，第一人称复数","你们，第二人称复数","他们，第三人称复数"],
 "ar":["أنا، المفرد الأول","أنت، المفرد الثاني","ماريا، المفرد الثالث","نحن، الجمع الأول","أنتم، الجمع الثاني","هم، الجمع الثالث"],
 "es":["yo, 1.ª singular","tú, 2.ª singular","María, 3.ª singular","nosotros, 1.ª plural","ustedes, 2.ª plural","ellos, 3.ª plural"],
 "pt":["eu, 1.ª singular","tu, 2.ª singular","Maria, 3.ª singular","nós, 1.ª plural","vocês, 2.ª plural","eles, 3.ª plural"]
}

def _verb_a_explanation(card,lang):
    lemma=card["lemma"]
    return VERB_A_TIPS[lang].format(
        lemma=lemma,root=lemma[:-1],person=VERB_A_PERSONS[lang][card["person"]],
        ending=VERB_A_ENDINGS[card["person"]],correct=card["correct"]
    )


VERB_B1_ENDINGS=("άω","άς","άει","άμε","άτε","άνε")
VERB_B1_TIPS={
 "ru":"B1, лицо: {person}. Основа «{root}» + «-{ending}» = «{correct}». Другие проверенные формы: {alternatives}. Не путай окончания B1 (-άς/-άει/-άτε) с группой A (-εις/-ει/-ετε).",
 "en":"B1, person: {person}. Stem “{root}” + “-{ending}” = “{correct}”. Other verified forms: {alternatives}. Do not confuse B1 (-άς/-άει/-άτε) with group A (-εις/-ει/-ετε).",
 "zh":"B1，人称：{person}。词干“{root}”加词尾“-{ending}”得到“{correct}”。已核对的变体：{alternatives}。不要把 B1 (-άς/-άει/-άτε) 与 A 组词尾混淆。",
 "ar":"المجموعة B1، الشخص: {person}. الجذر «{root}» + النهاية «-{ending}» = «{correct}». الصيغ البديلة المراجَعة: {alternatives}. لا تخلط نهايات B1 بنهايات المجموعة A.",
 "es":"B1, persona: {person}. Raíz «{root}» + terminación «-{ending}» = «{correct}». Otras formas verificadas: {alternatives}. No confundas B1 (-άς/-άει/-άτε) con el grupo A (-εις/-ει/-ετε).",
 "pt":"B1, pessoa: {person}. Radical «{root}» + terminação «-{ending}» = «{correct}». Outras formas verificadas: {alternatives}. Não confundas B1 (-άς/-άει/-άτε) com o grupo A (-εις/-ει/-ετε)."
}

def _verb_b1_explanation(card,lang):
    variants=card.get("acceptedForms",[card["correct"]])[1:]
    return VERB_B1_TIPS[lang].format(
        person=VERB_A_PERSONS[lang][card["person"]],
        root=card["lemma"][:-2],
        ending=VERB_B1_ENDINGS[card["person"]],
        correct=card["correct"],
        alternatives=" / ".join(variants) if variants else "—"
    )


VERB_B2_ENDINGS=("ώ","είς","εί","ούμε","είτε","ούν")
VERB_B2_TIPS={
 "ru":"B2, {person}: основа «{root}» + окончание «-{ending}» → «{correct}». {variant} Не путай с B1 (-άς/-άει/-άτε); ударение обязательно.",
 "en":"B2, {person}: stem “{root}” + ending “-{ending}” → “{correct}”. {variant} Do not confuse it with B1 (-άς/-άει/-άτε); keep the stress mark.",
 "zh":"B2，{person}：词干“{root}”加词尾“-{ending}”得到“{correct}”。{variant} 不要与 B1 的 -άς/-άει/-άτε 混淆；注意重音。",
 "ar":"B2، {person}: الجذر «{root}» + النهاية «-{ending}» ← «{correct}». {variant} لا تخلطها مع B1 (-άς/-άει/-άτε)، وحافظ على علامة النبر.",
 "es":"B2, {person}: raíz «{root}» + terminación «-{ending}» → «{correct}». {variant} No lo confundas con B1 (-άς/-άει/-άτε); conserva el acento.",
 "pt":"B2, {person}: radical «{root}» + terminação «-{ending}» → «{correct}». {variant} Não confundas com B1 (-άς/-άει/-άτε); mantém o acento."
}
VERB_B2_VARIANTS={
 "ru":["Допустим также разговорный вариант: {forms}.","Других вариантов для этой формы не указано."],
 "en":["Also accepted in conversation: {forms}.","No alternative is listed for this person."],
 "zh":["也接受口语变体：{forms}。","此人称未列出其他变体。"],
 "ar":["تُقبل أيضاً الصيغة المحكية: {forms}.","لا توجد صيغة بديلة محددة لهذا الشخص."],
 "es":["También se acepta la variante coloquial: {forms}.","No se admite otra variante para esta persona."],
 "pt":["Também se aceita a variante coloquial: {forms}.","Não há outra variante admitida para esta pessoa."]
}

def _verb_b2_explanation(card,lang):
    alternatives=card.get("acceptedForms",[card["correct"]])[1:]
    variant=(VERB_B2_VARIANTS[lang][0].format(forms=" / ".join(alternatives))
             if alternatives else VERB_B2_VARIANTS[lang][1])
    return VERB_B2_TIPS[lang].format(
        person=VERB_A_PERSONS[lang][card["person"]],
        root=card["lemma"][:-1],
        ending=VERB_B2_ENDINGS[card["person"]],
        correct=card["correct"],
        variant=variant
    )


LIKES_GUIDANCE={
 "agreement":{"ru":"Число определяется тем, что нравится: единственное число → «αρέσει», множественное → «αρέσουν». «{person}» указывает, кому нравится, а не кто владеет предметом.","en":"The liked subject controls agreement: singular → “αρέσει”, plural → “αρέσουν”. “{person}” identifies who experiences the preference, not the owner.","zh":"动词与被喜欢的事物一致：单数用“αρέσει”，复数用“αρέσουν”。“{person}”表示喜欢者，不表示物品的拥有者。","ar":"الفعل يتبع الشيء المحبوب: المفرد «αρέσει» والجمع «αρέσουν». الضمير «{person}» يحدد من يعجبه الشيء، لا مالكه.","es":"El número depende de lo que gusta: singular «αρέσει», plural «αρέσουν». «{person}» indica a quién le gusta, no quién lo posee.","pt":"O verbo concorda com aquilo de que se gosta: singular «αρέσει», plural «αρέσουν». «{person}» indica quem gosta, não o dono."},
 "experiencer":{"ru":"«{person}» означает «кому нравится», а не «чей предмет». Это местоимение стоит перед «αρέσει/αρέσουν»; число глагола задаёт то, что нравится.","en":"“{person}” says who likes it, not whose item it is. This clitic stands before αρέσει/αρέσουν; the liked subject determines singular or plural.","zh":"“{person}”表示谁喜欢，不表示物品归谁所有。它放在 αρέσει/αρέσουν 前；动词单复数由被喜欢的事物决定。","ar":"«{person}» يدل على من يعجبه الشيء، لا على مالكه. يأتي قبل αρέσει/αρέσουν، وعدد الفعل يتبع الشيء المحبوب.","es":"«{person}» indica a quién le gusta, no de quién es. Va antes de αρέσει/αρέσουν; el número depende de lo que gusta.","pt":"«{person}» indica quem gosta, não a quem pertence a coisa. Vem antes de αρέσει/αρέσουν; o número depende daquilo de que se gosta."},
 "typed":{"ru":"Полная конструкция: «{correct}». Местоимение указывает, кому нравится, а «αρέσει»/«αρέσουν» согласуется с тем, что нравится. Отрицание «δεν» ставится перед местоимением.","en":"Full phrase: “{correct}”. The clitic indicates who likes it, while αρέσει/αρέσουν agrees with the liked item. Negative δεν comes before the clitic.","zh":"完整表达：“{correct}”。代词表示喜欢者，αρέσει/αρέσουν 与被喜欢事物的单复数一致；否定词 δεν 放在代词之前。","ar":"العبارة الصحيحة «{correct}». الضمير يشير إلى من يعجبه الشيء، ويتبع αρέσει/αρέσουν عدد الشيء المحبوب؛ تأتي «δεν» قبل الضمير.","es":"Expresión completa: «{correct}». El clítico indica a quién le gusta; αρέσει/αρέσουν concuerda con lo que gusta. «δεν» va delante del clítico.","pt":"Expressão completa: «{correct}». O clítico indica quem gosta; αρέσει/αρέσουν concorda com o objeto do gosto. «δεν» vem antes do clítico."}
}

def _likes_explanation(card,lang):
    message=LIKES_GUIDANCE[card["skill"]][lang].format(
        person=card["experiencer"], correct=card["correct"]
    )
    if card.get("acceptedForms") and len(card["acceptedForms"])>1:
        messages={
            "ru":"Допустимое разговорное сокращение: {alternatives}.",
            "en":"Accepted colloquial contractions: {alternatives}.",
            "zh":"接受的口语缩略形式：{alternatives}。",
            "ar":"تُقبل الصيغ المختصرة المحكية: {alternatives}.",
            "es":"Contracciones coloquiales admitidas: {alternatives}.",
            "pt":"Contrações coloquiais aceites: {alternatives}."
        }
        message += " "+messages[lang].format(
            alternatives=" / ".join(card["acceptedForms"][1:])
        )
    return message


SCHEDULE_GUIDANCE={
 "time":{"ru":"Смотри на день и название события в расписании. Ответ «{correct}». Для 12-часовой разговорной записи уточни утро/день/вечер: «{spoken}».","en":"Match the day and activity in the agenda. Answer: “{correct}”. In 12-hour speech, disambiguate morning/afternoon/evening: “{spoken}”.","zh":"根据日程中的星期和活动确定时间。答案：“{correct}”。12小时口语必须标明早上、下午或晚上：“{spoken}”。","ar":"اقرأ اليوم والنشاط في الجدول. الإجابة «{correct}». في النطق بصيغة 12 ساعة حدّد الصباح/الظهر/المساء: «{spoken}».","es":"Localiza el día y la actividad en la agenda. Respuesta: «{correct}». Al hablar en formato de 12 horas, aclara mañana/tarde/noche: «{spoken}».","pt":"Encontra o dia e a atividade na agenda. Resposta: «{correct}». Em formato falado de 12 horas, distingue manhã/tarde/noite: «{spoken}»."},
 "day":{"ru":"Сопоставь единственное событие с нужной строкой недели. Правильный ответ: «{correct}». Перед днём недели используется τη/την/το.","en":"Match the unique event to its weekday row. Correct: “{correct}”. Greek weekday expressions use τη/την/το before the day.","zh":"将唯一的活动与日程中的星期匹配。正确答案：“{correct}”。希腊语星期前使用 τη/την/το。","ar":"طابق الحدث مع يومه في الجدول. الإجابة «{correct}». تُستخدم τη/την/το قبل اسم اليوم.","es":"Relaciona la actividad con su día. Respuesta: «{correct}». Antes del día griego se usa τη/την/το.","pt":"Relaciona a atividade com o dia certo. Resposta: «{correct}». Antes do dia em grego usa-se τη/την/το."},
 "date":{"ru":"В расписании указана неделя 2–8 ноября 2026 года. Ответ «{correct}» — день месяца и название месяца в родительном падеже.","en":"The schedule is for 2–8 November 2026. “{correct}” uses the day number and the genitive month name.","zh":"日程日期为2026年11月2日至8日。“{correct}”由日期数字和月份的属格形式组成。","ar":"الجدول للأسبوع 2–8 نوفمبر 2026. «{correct}» هو رقم اليوم مع اسم الشهر في حالة الإضافة.","es":"La agenda abarca del 2 al 8 de noviembre de 2026. «{correct}» combina día y nombre del mes en genitivo.","pt":"A agenda cobre 2–8 de novembro de 2026. «{correct}» combina o dia e o nome do mês no genitivo."},
 "spoken":{"ru":"24-часовое время «{clock}» в разговорной форме: «{correct}». Часть суток обязательна. «Μία» требует «στη», остальные часы — «στις».","en":"The 24-hour time “{clock}” spoken naturally is “{correct}”. Keep the part of day explicit. Use στη with μία and στις for other hours.","zh":"24小时制“{clock}”对应的希腊语口语为“{correct}”。必须说明时段。μία 前用 στη，其他钟点用 στις。","ar":"الوقت «{clock}» بصيغة 24 ساعة يُقال «{correct}». حدّد فترة اليوم. نستخدم στη مع μία و στις مع بقية الساعات.","es":"La hora de 24 horas «{clock}» se dice «{correct}». Mantén explícita la parte del día. Se usa στη con μία y στις con las demás horas.","pt":"A hora de 24h «{clock}» diz-se «{correct}». Indica a parte do dia. Usa στη com μία e στις nas restantes horas."}
}

def _schedule_explanation(card,lang):
    from agenda_cards import DAYS
    day=next(d for d in DAYS if d["id"]==card["dayID"])
    event=next(e for e in day["events"] if e["id"]==card["eventID"])
    return SCHEDULE_GUIDANCE[card["skill"]][lang].format(
        correct=card["correct"],clock=card["eventTime"],spoken=event["spoken"]
    )


DURATION_GUIDANCE={
 "contrast":{"ru":"Здесь «{correct}» — наиболее естественный вопрос: {reason}. Разница зависит от контекста, а не строго от количества минут или лет; некоторые формулировки пересекаются.","en":"Here “{correct}” is the most natural: {reason}. The distinction is contextual, not a strict minute-versus-year cutoff; usage can overlap.","zh":"本题最自然的问法是“{correct}”：{reason}。区别取决于语境，而不是严格按分钟或年份划分；两者有时可以互用。","ar":"الصيغة الأنسب هنا «{correct}»: {reason}. يعتمد الفرق على السياق، لا على حدّ صارم بين الدقائق والسنوات؛ وقد تتداخل الاستعمالات.","es":"Aquí «{correct}» es lo más natural: {reason}. La distinción depende del contexto, no de un corte rígido entre minutos y años; pueden solaparse.","pt":"Aqui «{correct}» é o mais natural: {reason}. A distinção depende do contexto, não de uma divisão rígida entre minutos e anos; os usos podem sobrepor-se."},
 "unit":{"ru":"«{correct}» — нужная форма единицы после числительного и предлога в данном предложении. Сравни: ένα λεπτό / δύο λεπτά; μία ώρα / τρεις ώρες; έναν μήνα / τρεις μήνες; έναν χρόνο / τέσσερα χρόνια.","en":"“{correct}” is the appropriate noun form after the numeral/preposition here. Compare ένα λεπτό / δύο λεπτά, μία ώρα / τρεις ώρες, έναν μήνα / τρεις μήνες, έναν χρόνο / τέσσερα χρόνια.","zh":"这里的正确时间单位形式是“{correct}”，由数字和介词决定。比较：ένα λεπτό / δύο λεπτά，μία ώρα / τρεις ώρες，έναν μήνα / τρεις μήνες，έναν χρόνο / τέσσερα χρόνια。","ar":"«{correct}» هي صيغة وحدة الزمن المناسبة بعد العدد وحرف الجر. قارن: ένα λεπτό / δύο λεπτά، μία ώρα / τρεις ώρες، έναν μήνα / τρεις μήνες، έναν χρόνο / τέσσερα χρόνια.","es":"«{correct}» es la forma correcta de la unidad tras el numeral/la preposición. Compara ένα λεπτό / δύο λεπτά, μία ώρα / τρεις ώρες, έναν μήνα / τρεις μήνες, έναν χρόνο / τέσσερα χρόνια.","pt":"«{correct}» é a forma certa da unidade após o numeral/a preposição. Compara ένα λεπτό / δύο λεπτά, μία ώρα / τρεις ώρες, έναν μήνα / τρεις μήνες, έναν χρόνο / τέσσερα χρόνια."},
 "timeline":{"ru":"Начало {start} + длительность {minutes} мин. = окончание {end}. «Στις» обозначает время на часах, а длительность отвечает на «πόση ώρα».","en":"Start {start} + {minutes} minutes = end {end}. Στις marks a clock-time point; duration answers πόση ώρα.","zh":"开始 {start}，加 {minutes} 分钟，结束于 {end}。“στις”表示钟点，而时长回答“πόση ώρα”。","ar":"البداية {start} + {minutes} دقيقة = النهاية {end}. تشير στις إلى وقت محدد؛ أما المدة فتجيب عن πόση ώρα.","es":"Inicio {start} + {minutes} minutos = fin {end}. Στις marca una hora concreta; la duración responde a πόση ώρα.","pt":"Início {start} + {minutes} minutos = fim {end}. Στις marca uma hora concreta; a duração responde a πόση ώρα."},
 "preposition":{"ru":"«{correct}» правильно: «από» указывает момент, с которого что-то идёт (с девяти), а «για» обозначает длительность (на две недели). Это не вопрос «который час?».",
 "en":"“{correct}” fits: από marks the point when something starts (from nine), while για marks a duration (for two weeks). Neither means “what time is it?”.",
 "zh":"正确答案是“{correct}”：από 表示时间起点（从九点），για 表示持续时长（两周）。这不是问“现在几点”。",
 "ar":"الصواب «{correct}»: تشير από إلى وقت البداية (من التاسعة)، وتشير για إلى المدة (لمدة أسبوعين)، لا إلى سؤال الساعة الآن.",
 "es":"«{correct}» es correcto: από indica el punto de inicio (desde las nueve) y για indica duración (durante dos semanas). No es «¿qué hora es?».",
 "pt":"«{correct}» é correto: από indica o ponto de início (desde as nove) e για indica duração (durante duas semanas). Não é «que horas são?»."},
 "typed":{"ru":"Правильный ответ: «{correct}». Важны форма числительного, род и падеж единицы длительности; допустимые цифровые написания перечислены отдельно, а не угадываются.","en":"Correct: “{correct}”. The numeral and the time unit's gender/case matter. Valid digit spellings are curated per question, not guessed.","zh":"正确答案是“{correct}”。注意数词、时间单位的性和格；可接受的数字写法只在本题明确列出。","ar":"الصواب «{correct}». يجب مراعاة العدد وجنس وحدة المدة وحالتها؛ صيغ الأرقام المسموح بها محددة لكل سؤال.","es":"Correcto: «{correct}». Importan el numeral, el género y el caso de la unidad; las variantes con cifras se verifican caso por caso.","pt":"Correto: «{correct}». Importam o numeral, o género e o caso da unidade; as variantes com algarismos são verificadas por pergunta."}
}
DURATION_REASONS={
 "event":{"ru":"указана продолжительность конкретного действия","en":"the duration of a bounded activity is in focus","zh":"重点是一次具体活动的时长","ar":"السؤال عن مدة نشاط محدد","es":"se pregunta por la duración de una actividad concreta","pt":"pergunta-se pela duração de uma atividade concreta"},
 "ongoing":{"ru":"указан общий период состояния до настоящего времени","en":"the ongoing period up to now is in focus","zh":"重点是一直持续到现在的时期","ar":"السؤال عن فترة مستمرة حتى الآن","es":"se pregunta por un período que continúa hasta hoy","pt":"pergunta-se por um período que continua até hoje"}
}

def _duration_explanation(card,lang):
    skill=card["skill"]
    return DURATION_GUIDANCE[skill][lang].format(
        correct=card["correct"],
        reason=DURATION_REASONS[card["contextType"]][lang] if skill=="contrast" else "",
        start=card.get("startTime",""),
        minutes=card.get("minutes",""),
        end=card.get("endTime","")
    )


WEATHER_GUIDANCE={
 "sun":{"ru":"«Έχει ήλιο» — безличное описание солнечной погоды: έχει + существительное ήλιο. Отрицание: «δεν έχει ήλιο».","en":"“Έχει ήλιο” is an impersonal weather expression: έχει + the noun ήλιο. Its negative is “δεν έχει ήλιο”.","zh":"“Έχει ήλιο”是非人称天气表达：έχει 加名词 ήλιο。否定形式是“δεν έχει ήλιο”。","ar":"«Έχει ήλιο» تعبير غير شخصي عن الجو المشمس: έχει مع الاسم ήλιο. النفي: «δεν έχει ήλιο».","es":"«Έχει ήλιο» es una expresión impersonal: έχει + el sustantivo ήλιο. Negación: «δεν έχει ήλιο».","pt":"«Έχει ήλιο» é uma expressão impessoal: έχει + o nome ήλιο. Negação: «δεν έχει ήλιο»."},
 "cloud":{"ru":"«Έχει συννεφιά» — описание облачной погоды с έχει + существительное συννεφιά. Отрицание: «δεν έχει συννεφιά».","en":"“Έχει συννεφιά” describes cloudy weather using έχει + the noun συννεφιά. Negative: “δεν έχει συννεφιά”.","zh":"“Έχει συννεφιά”用 έχει 加名词 συννεφιά 来表示多云。否定是“δεν έχει συννεφιά”。","ar":"«Έχει συννεφιά» يصف الجو الغائم باستخدام έχει مع الاسم συννεφιά. النفي: «δεν έχει συννεφιά».","es":"«Έχει συννεφιά» describe el cielo nublado con έχει + el nombre συννεφιά. Negación: «δεν έχει συννεφιά».","pt":"«Έχει συννεφιά» descreve céu nublado com έχει + o nome συννεφιά. Negação: «δεν έχει συννεφιά»."},
 "rain":{"ru":"«Βρέχει» — безличный глагол «идёт дождь», без подлежащего «он/она». Отрицание «δεν βρέχει».","en":"“Βρέχει” is the impersonal verb “it is raining”, without a real he/she subject. Negative: “δεν βρέχει”.","zh":"“Βρέχει”是非人称动词“下雨”，不带真正的“他/她”主语。否定：“δεν βρέχει”。","ar":"«Βρέχει» فعل غير شخصي يعني نزول المطر، بلا فاعل بشري. النفي: «δεν βρέχει».","es":"«Βρέχει» es un verbo impersonal: «llueve», sin sujeto él/ella. Negación: «δεν βρέχει».","pt":"«Βρέχει» é um verbo impessoal: «está a chover», sem sujeito ele/ela. Negação: «δεν βρέχει»."},
 "snow":{"ru":"«Χιονίζει» — безличный глагол «идёт снег». Отрицание: «δεν χιονίζει».","en":"“Χιονίζει” is an impersonal verb for “it is snowing”. Negative: “δεν χιονίζει”.","zh":"“Χιονίζει”是表示“下雪”的非人称动词。否定：“δεν χιονίζει”。","ar":"«Χιονίζει» فعل غير شخصي يعني تساقط الثلج. النفي: «δεν χιονίζει».","es":"«Χιονίζει» es un verbo impersonal: «nieva». Negación: «δεν χιονίζει».","pt":"«Χιονίζει» é um verbo impessoal: «está a nevar». Negação: «δεν χιονίζει»."},
 "wind":{"ru":"«Φυσάει» — безличное «дует ветер». Знак ≋ обозначает ветер и подписан словом αέρας. Отрицание: «δεν φυσάει».","en":"“Φυσάει” means “it is windy” impersonally. The ≋ symbol is labelled αέρας (wind). Negative: “δεν φυσάει”.","zh":"“Φυσάει”是非人称的“刮风”。符号 ≋ 标为 αέρας（风）。否定：“δεν φυσάει”。","ar":"«Φυσάει» تعني هبوب الرياح بشكل غير شخصي. الرمز ≋ موسوم بكلمة αέρας. النفي: «δεν φυσάει».","es":"«Φυσάει» es impersonal: «hace viento». El símbolo ≋ lleva la etiqueta αέρας (viento). Negación: «δεν φυσάει».","pt":"«Φυσάει» é impessoal: «faz vento». O símbolo ≋ tem a legenda αέρας (vento). Negação: «δεν φυσάει»."}
}

def _weather_explanation(card,lang):
    # Negative δεν comes before the complete weather predicate. With ήλιο/
    # συννεφιά use έχει + noun; βρέχει/χιονίζει/φυσάει are impersonal.
    return WEATHER_GUIDANCE[card["weatherCode"]][lang]


CORE_PRESENT_TIPS={
 "ru":"Настоящее время «{lemma}», лицо {person}: «{correct}». Шесть лиц (я / ты / он или она / мы / вы / они): {forms}. {extra}",
 "en":"Present tense “{lemma}”, person {person}: “{correct}”. Six persons (I / you / he or she / we / you / they): {forms}. {extra}",
 "zh":"动词“{lemma}”的现在时，人称{person}：正确形式“{correct}”。六个人称（我／你／他或她／我们／你们／他们）：{forms}。{extra}",
 "ar":"المضارع للفعل «{lemma}»، الشخص {person}: «{correct}». الأشكال الستة (أنا/أنت/هو أو هي/نحن/أنتم/هم): {forms}. {extra}",
 "es":"Presente de «{lemma}», persona {person}: «{correct}». Seis personas (yo / tú / él o ella / nosotros / ustedes / ellos): {forms}. {extra}",
 "pt":"Presente de «{lemma}», pessoa {person}: «{correct}». Seis pessoas (eu / tu / ele ou ela / nós / vocês / eles): {forms}. {extra}"
}
CORE_PRESENT_VARIANT_NOTE={
 "ru":["Для этого лица допускается также: {variants}.","Только указанная форма принимается в этом упражнении."],
 "en":["Also accepted for this person: {variants}.","Only the listed canonical form is accepted here."],
 "zh":["此人称也接受：{variants}。","本题只接受列出的标准形式。"],
 "ar":["تُقبل أيضاً لهذه الصيغة: {variants}.","تُقبل هنا الصيغة الأساسية المدرجة فقط."],
 "es":["También se acepta para esta persona: {variants}.","Aquí solo se acepta la forma principal indicada."],
 "pt":["Também se aceita para esta pessoa: {variants}.","Aqui só se aceita a forma principal indicada."]
}
CORE_PRESENT_LEGO={
 "ru":"«Λέγω» — отдельный более книжный вариант; не считаем его автоматической заменой всей таблицы A1.",
 "en":"“Λέγω” is a distinct, more formal variant; it is not an automatic substitute for every A1 form.",
 "zh":"“Λέγω”属于较正式的另一组形式，不能自动替换所有 A1 变位。",
 "ar":"«Λέγω» صيغة أخرى أكثر رسمية، وليست بديلاً آلياً لجميع صيغ A1.",
 "es":"«Λέγω» es una variante más formal, no un reemplazo automático para todas las personas de A1.",
 "pt":"«Λέγω» é uma variante mais formal, não uma substituição automática de todas as formas de A1."
}

def _core_present_explanation(card,lang):
    from core_verb_cards import EXPECTED, ALLOWED_ALTERNATES
    forms=" / ".join(EXPECTED[card["lemma"]])
    variants=ALLOWED_ALTERNATES[card["lemma"]].get(str(card["person"]),[])
    extra=(CORE_PRESENT_VARIANT_NOTE[lang][0].format(
        variants=" / ".join(variants)) if variants
        else CORE_PRESENT_VARIANT_NOTE[lang][1])
    if card["lemma"]=="λέω":
        extra += " "+CORE_PRESENT_LEGO[lang]
    return CORE_PRESENT_TIPS[lang].format(
        lemma=card["lemma"],person=VERB_A_PERSONS[lang][card["person"]],
        correct=card["correct"],forms=forms,extra=extra
    )

def explanation(card,lang):
    if card["kind"]=="grammar" and card.get("group")=="verb_core":
        return _core_present_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="weather":
        return _weather_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="duration":
        return _duration_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="schedule":
        return _schedule_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="likes":
        return _likes_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="verb_B2":
        return _verb_b2_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="verb_B1":
        return _verb_b1_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="verb_A":
        return _verb_a_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="possessive":
        return _possessive_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="gender":
        return GENDER_EXPLANATIONS.get(lang,GENDER_EXPLANATIONS["en"])[card["correct"]]
    if card["kind"]!="grammar" or card.get("group")!="case":
        return None
    index=int(card["id"].split("_")[-1])-1
    if index>=10:return None
    return (CASE_RU if lang=="ru" else CASE_EN)[index]
