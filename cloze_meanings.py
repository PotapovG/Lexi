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
            legacy=[c for c in cards if c.get("group")!="possessive"] if kind=="grammar" else cards
            assert len(lines)==len(legacy),(kind,lang,len(lines),len(legacy))
            assert all(lines),(kind,lang)
    assert len(ARTICLES)==24 and len(GRAMMAR)==111
    assert len(CASE_RU)==len(CASE_EN)==10
    return sum(len(cards) for cards in KINDS.values())

def translation(card,lang):
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

def explanation(card,lang):
    if card["kind"]=="grammar" and card.get("group")=="possessive":
        return _possessive_explanation(card,lang)
    if card["kind"]=="grammar" and card.get("group")=="gender":
        return GENDER_EXPLANATIONS.get(lang,GENDER_EXPLANATIONS["en"])[card["correct"]]
    if card["kind"]!="grammar" or card.get("group")!="case":
        return None
    index=int(card["id"].split("_")[-1])-1
    if index>=10:return None
    return (CASE_RU if lang=="ru" else CASE_EN)[index]
