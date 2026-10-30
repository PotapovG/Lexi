"""Reviewed semantic overlap for *contextless word translation* questions.

ελεύθερος means free/available and may mean single, whereas ανύπαντρος
specifically means unmarried. Neither is a synonym of the other in all
contexts. In an isolated vocabulary prompt, however, the unmarried/single
sense overlaps, so neither should be a wrong multiple-choice distractor.

Do not apply this atlas to dialogues, contextualized sentences, or grammar
questions. Do not mix grammatical gender or divorced/married categories.
"""
PAIRS={
    "ελεύθερος":"ανύπαντρος",
    "ανύπαντρος":"ελεύθερος",
    "ελεύθερη":"ανύπαντρη",
    "ανύπαντρη":"ελεύθερη",
}
# Exact English/Russian source glosses from the existing authored word cards.
# Only reviewed language aliases are accepted; other locales still benefit
# from avoiding near-synonymous distractors.
GLOSSES={
    "ru":{
        "ελεύθερος":"холостой / свободный",
        "ανύπαντρος":"неженатый",
        "ελεύθερη":"незамужняя / свободная",
        "ανύπαντρη":"незамужняя",
    },
    "en":{
        "ελεύθερος":"single / free (man)",
        "ανύπαντρος":"unmarried (man)",
        "ελεύθερη":"single / free (woman)",
        "ανύπαντρη":"unmarried (woman)",
    },
    "zh":{
        "ελεύθερος":"单身／自由的（男性）",
        "ανύπαντρος":"未婚（男）",
        "ελεύθερη":"单身／自由的（女性）",
        "ανύπαντρη":"未婚（女）",
    },
    "ar":{
        "ελεύθερος":"أعزب / حر (رجل)",
        "ανύπαντρος":"غير متزوج (رجل)",
        "ελεύθερη":"عازبة / حرة (امرأة)",
        "ανύπαντρη":"غير متزوج (امرأة)",
    },
    "es":{
        "ελεύθερος":"soltero / libre (hombre)",
        "ανύπαντρος":"soltero (hombre)",
        "ελεύθερη":"soltera/libre (mujer)",
        "ανύπαντρη":"soltera (mujer)",
    },
    "pt":{
        "ελεύθερος":"solteiro/livre (homem)",
        "ανύπαντρος":"solteiro (homem)",
        "ελεύθερη":("solteiro/livre (mulher)","solteira / livre (mulher)"),
        "ανύπαντρη":"solteira (mulher)",
    },
}

def eligible(card):
    return card.get("kind","word")=="word" and card.get("gr") in PAIRS

def overlaps(first,second):
    return (eligible(first) and eligible(second) and
            PAIRS[first["gr"]]==second["gr"])

def alternatives(card,direction,lang):
    """Only exact, curated contextless vocabulary alternatives."""
    if not eligible(card):return []
    counterpart=PAIRS[card["gr"]]
    if direction in ("ru-gr","target-gr"):
        return [counterpart]
    if direction in ("gr-ru","gr-target"):
        value=GLOSSES.get(lang,{}).get(counterpart)
        if isinstance(value,tuple):return list(value)
        return [value] if value else []
    return []

def is_paired_word(card):
    return eligible(card)
