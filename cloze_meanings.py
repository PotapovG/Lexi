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
            assert len(lines)==len(cards),(kind,lang,len(lines),len(cards))
            assert all(lines),(kind,lang)
    assert len(ARTICLES)==24 and len(GRAMMAR)==56
    assert len(CASE_RU)==len(CASE_EN)==10
    return sum(len(cards) for cards in KINDS.values())

def translation(card,lang):
    kind=card["kind"]
    assert kind in TABLES
    number=(int(card["id"].split("_")[-1])-1)
    used=lang if lang in ("ru","en") else "en"
    assert KINDS[kind][number]["id"]==card["id"]
    return TABLES[kind][used][number],used

def explanation(card,lang):
    if card["kind"]!="grammar" or card.get("group")!="case":
        return None
    index=int(card["id"].split("_")[-1])-1
    if index>=10:return None
    return (CASE_RU if lang=="ru" else CASE_EN)[index]
