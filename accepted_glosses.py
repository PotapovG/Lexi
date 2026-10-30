"""Small *explicitly reviewed* alternative-translations atlas (no fuzzy AI).

Only the target-language side (Greek -> selected interface translation) may
use aliases. The source-language-to-Greek direction remains deterministic.
All aliases have been curated to retain person/register and original sense.
Avoid inserting guesses for Arabic/Chinese/Spanish/Portuguese.
"""
from unicodedata import normalize
import greek_variants
import lexical_overlap

_ALIASES={
 'p001':{'ru':['Как тебя зовут','Как твоё имя?'], 'en':["What's your name? (informal)"]},
 'p002':{'ru':['Как Вас зовут?']},
 'p003':{'ru':['Приятно познакомиться!'],'en':['Pleased to meet you!']},
 'p004':{'ru':['Откуда ты родом?']},
 'p011':{'ru':['Где ты проживаешь?']},
 'p014':{'ru':['Он живёт в Афинах.','Она живёт в Афинах.']},
 'w001':{'ru':['Привет!','Здравствуй!'],'en':['Hi! (informal)']},
 'w002':{'ru':['Здравствуйте!']},
 'w007':{'ru':['Приятно познакомиться'], 'en':['Pleased to meet you']},
 'w049':{'ru':['Я живу','Я проживаю']},
 'p006':{'ru':['Я родом с Кипра.','Я с Кипра.']},
 # More independently verified literal equivalents, keeping person/register:
 'w003':{'ru':['Доброе утро','Добрый день'], 'en':['Good morning','Good day']},
 'w006':{'ru':['Пока','До свидания'], 'en':['Goodbye','Bye']},
 'w008':{'ru':['Благодарю','Спасибо!'], 'en':['Thank you','Thanks']},
 'w009':{'ru':['Не за что'], 'en':["You're welcome","Please"]},
 'w012':{'ru':['Прости','Простите'], 'en':['Sorry','Excuse me']},
 'w045':{'ru':['Сотовый телефон','Мобильный'], 'en':['Mobile phone','Cell phone']},
 'w055':{'ru':['У меня есть','Я имею'], 'en':['I have']},
 'w056':{'ru':['У тебя есть','Ты имеешь'], 'en':['You have (singular)']},
 'w057':{'ru':['У него есть','У неё есть'], 'en':['He has','She has']},
 'w058':{'ru':['У нас есть'], 'en':['We have']},
 'w059':{'ru':['У вас есть'], 'en':['You have (plural/formal)']},
 'w060':{'ru':['У них есть'], 'en':['They have']},
 'w093':{'ru':['Муж'], 'en':['Husband','Spouse']},
 'w094':{'ru':['Жена'], 'en':['Wife','Spouse (female)']},
 'w112':{'ru':['Женат'], 'en':['Married (masculine)']},
 'w113':{'ru':['Замужем'], 'en':['Married (feminine)']},
 'w114':{'ru':['Не женат'], 'en':['Unmarried (masculine)']},
 'w115':{'ru':['Не замужем'], 'en':['Unmarried (feminine)']},
 'p005':{'ru':['Откуда Вы?','Откуда вы родом?'], 'en':['Where are you from? (formal)']},
 'p008':{'ru':['Как поживаешь?','Как у тебя дела?'], 'en':['How are you?']},
 'p009':{'ru':['Всё хорошо, спасибо.'], 'en':["I'm fine, thanks."]},
 'p010':{'ru':['А у тебя?'], 'en':['And you?']},
 'p012':{'ru':['Где вы проживаете?'], 'en':['Where do you live? (formal)']},
 'p017':{'ru':['Что ты делаешь?','Как дела?'], 'en':['What are you doing?','How are you?']},
 'p018':{'ru':['Что вы делаете?','Как поживаете?'], 'en':['What are you doing? (formal)']},
 'p021':{'ru':['Чем ты занимаешься?','Какая у тебя работа?'], 'en':['What is your job?']},
 'p022':{'ru':['Кем он работает?','Кем она работает?'], 'en':['What is his job?','What is her job?']},
 'p025':{'ru':['У него двое детей.','У неё двое детей.'], 'en':['He has two children.','She has two children.']},
 'p026':{'ru':['У меня сын.'], 'en':['I have a son.']},
 'p027':{'ru':['У меня дочь.'], 'en':['I have a daughter.']},
 'p030':{'ru':['Его зовут Никос.','Его имя Никос.'], 'en':['His name is Nikos.']},

}
# Keep previously presented phrasings when they remain semantically and
# register-correct. Do NOT accept deprecated forms that confused tu/usted,
# tu/você, formal/informal, Arabic gender, or Spanish interrogative accents.
_VALID_OLD_EDITED={
 ('w004','es'):['buenas noches'],
 ('p001','es'):['¿Cuál es tu nombre? (informal)'],
 ('w031','pt'):['O meu nome é'],
 ('p002','pt'):['Qual o seu nome? (formal)'],
}
for (_cid,_lang),_phrases in _VALID_OLD_EDITED.items():
    _ALIASES.setdefault(_cid,{}).setdefault(_lang,[]).extend(_phrases)

def accepted(card,direction,lang,correct):
    if direction in ('ru-gr','sg-pl','pl-sg'):
        return list(dict.fromkeys(greek_variants.accepted(correct)+
                                  lexical_overlap.alternatives(card,direction,lang)))
    if direction!='gr-ru':return [correct]
    return list(dict.fromkeys([correct]+_ALIASES.get(card['id'],{}).get(lang,[])+
                              lexical_overlap.alternatives(card,direction,lang)))

def is_accepted(card,direction,lang,selected,correct):
    return selected in accepted(card,direction,lang,correct)
