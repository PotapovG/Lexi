"""Modern Greek noun + enclitic stress placement, authorial minimal pairs.

One unstressed post-nominal possessive clitic follows a noun:
third-to-last stress on the noun -> additional ultimate accent; otherwise
the original noun tone stays as-is. No homophonous verbal clitics, which
can require a different orthographic interpretation. This curated deck
is not presented as verbatim publisher textbook content.
"""
import random
import unicodedata
import pedagogy_rules

# article, bare noun, inflected noun WITH required enclitic stress, lesson.
# The few words not attested at exactly this chapter are authorial new
# examples pinned to the relevant printed grammar theme (not book citations).
BASES=(
 ("το","τηλέφωνο","τηλέφωνό",3,True),
 ("το","όνομα","όνομά",3,True),
 ("το","μάθημα","μάθημά",7,True),
 ("το","παράθυρο","παράθυρό",11,True),
 ("το","δωμάτιο","δωμάτιό",11,True),
 ("το","αυτοκίνητο","αυτοκίνητό",11,True),
 ("το","πρόγραμμα","πρόγραμμά",17,True),
 ("ο","δάσκαλος","δάσκαλός",3,True),
 ("η","ερώτηση","ερώτησή",16,True),
 ("το","βιβλίο","βιβλίο",8,False),
 ("το","σπίτι","σπίτι",3,False),
 ("η","καρέκλα","καρέκλα",8,False),
 ("η","μητέρα","μητέρα",3,False),
)
POSSESSIVE=("μου","σου")
ACCENT={'α':'ά','ε':'έ','η':'ή','ι':'ί','ο':'ό','υ':'ύ','ω':'ώ'}
INVERSE={v:k for k,v in ACCENT.items()}

def unaccent(word):
    word=unicodedata.normalize('NFC',word)
    return ''.join(INVERSE.get(c,c) for c in word)

def add_final(word):
    for i in range(len(word)-1,-1,-1):
        if word[i] in ACCENT:
            return word[:i]+ACCENT[word[i]]+word[i+1:]
        if word[i] in INVERSE:
            return word
    raise ValueError("Greek noun without final vowel")

def make_variants(article,noun,correct_stem,enclitic,extra):
    # Four carefully chosen orthographic contrasts, not arbitrary strings
    # with three/four impossible accents.
    correct=f'{article} {correct_stem} {enclitic}'
    if extra:
        options=[
          correct,
          f'{article} {noun} {enclitic}', # missing extra accent
          f'{article} {add_final(unaccent(noun))} {enclitic}', # lost original
          f'{article} {unaccent(noun)} {enclitic}', # no written accents
        ]
    else:
        options=[
          correct,
          f'{article} {add_final(noun)} {enclitic}', # invented extra
          f'{article} {unaccent(noun)} {enclitic}', # lost normal stress
          f'{article} {noun} {enclitic[:-1]+ACCENT[enclitic[-1]]}', # wrongly stress clitic
        ]
    assert len(set(options))==4,(noun,options)
    return options

LABELS={
'ru':'Выбери правильное написание с «{pronoun}». Дополнительное ударение нужно не всегда.',
'en':'Choose the correct spelling with “{pronoun}”. An extra accent is not always needed.',
'zh':'选出与“{pronoun}”搭配的正确重音拼写。并非总要加第二个重音。',
'ar':'اختر الكتابة الصحيحة مع «{pronoun}». لا يلزم دائمًا نبر إضافي.',
'es':'Elige la escritura correcta con «{pronoun}». No siempre hace falta otro acento.',
'pt':'Escolhe a grafia correta com «{pronoun}». Nem sempre é preciso outro acento.',
}
EXPLANATIONS={
'ru':("Ударение в слове «{noun}» на третьем слоге от конца. Перед «{pronoun}» добавляем второе ударение на последнем слоге: «{correct}».","В слове «{noun}» основное ударение не на третьем слоге от конца. Дополнительное ударение перед «{pronoun}» не нужно: «{correct}»."),
'en':("“{noun}” is stressed on the third-to-last syllable. Before “{pronoun}”, add a second accent to its final syllable: “{correct}”.","“{noun}” is not stressed on its third-to-last syllable. No extra accent is needed before “{pronoun}”: “{correct}”."),
'zh':("“{noun}”的重音在倒数第三个音节，接“{pronoun}”时末音节要增加重音：“{correct}”。","“{noun}”不属于倒数第三音节重读，接“{pronoun}”时不需再加重音：“{correct}”。"),
'ar':("النبر في «{noun}» على المقطع الثالث من النهاية؛ نضيف نبرًا على المقطع الأخير قبل «{pronoun}»: «{correct}».","النبر في «{noun}» ليس على المقطع الثالث من النهاية، لذا لا نضيف نبرًا قبل «{pronoun}»: «{correct}»."),
'es':("“{noun}” lleva el acento en la antepenúltima sílaba. Con “{pronoun}” recibe otro en la última: “{correct}”.","“{noun}” no tiene el acento en la antepenúltima. No añadimos otro con “{pronoun}”: “{correct}”."),
'pt':("“{noun}” tem o acento na antepenúltima sílaba. Com “{pronoun}”, acrescenta-se outro na última: “{correct}”.","“{noun}” não tem o acento na antepenúltima, por isso não se acrescenta outro com “{pronoun}”: “{correct}”.")
}
CARDS=[]
for index,(article,noun,accented,chapter,extra) in enumerate(BASES,1):
    assert (add_final(noun)==accented) if extra else noun==accented,(noun,accented)
    for j,pronoun in enumerate(POSSESSIVE):
        correct=f'{article} {accented} {pronoun}'
        card=dict(id=f'en261021_{index:02d}{j+1}',kind='enclitic',
            chapter=chapter,unit=chapter,page={1:14,2:24,3:39,7:104,8:115,11:154,16:233,17:245}.get(chapter,39),
            article=article,noun=noun,stemWithClitic=accented,pronoun=pronoun,gr=correct,
            correct=correct,hasExtraStress=extra,
            options=make_variants(article,noun,accented,pronoun,extra),
            topic='Τονισμός · εγκλιτικά',grammar_tags=['enclitic_stress'],
            source='independent_possessive_enclitic_20261021',
            book_page_verified=False,
            **{lang:LABELS[lang].format(pronoun=pronoun) for lang in LABELS}
        )
        pedagogy_rules.tag(card)
        assert card['curriculum_ready_unit']<=chapter
        CARDS.append(card)
assert len(CARDS)==26 and len({c['id'] for c in CARDS})==26
BY_ID={c['id']:c for c in CARDS}
def explanation(card,lang):
    template=EXPLANATIONS[lang][0 if card['hasExtraStress'] else 1]
    return template.format(noun=card['noun'],pronoun=card['pronoun'],correct=card['correct'])
