"""Six special Greek present-tense verbs inside Lexi's EXISTING grammar_fill kind.

The six complete paradigms are explicit lexicographic facts, not mechanically
derived from a suffix. Formal λέγω is intentionally outside this A1 answer
list. Present-tense πηγαίνω synonyms and attested third-plural short forms
are accepted only on the enumerated lemma/person cards.
No new learner mode, route, database schema or textbook reproductions.
"""
import json
import unicodedata
from collections import Counter
from pathlib import Path

import pedagogy_rules
from textbook_alignment import INDEX
from topics_verbs import VERBS as EXISTING_VERB_GROUPS
from verb_curriculum import first_unit as existing_verb_intro

# All distractors come from already shipped A/B1/B2 conjugations.
# Prevent a high-level lemma (e.g. μπορώ at unit 16) appearing in a
# chapter-six/seven semantic choice despite being a *wrong* answer.
EXISTING_CONTRASTS={}
for family,_level,lemma,_ru,_en,forms in EXISTING_VERB_GROUPS:
    for form in forms:
        EXISTING_CONTRASTS[form]=(family,existing_verb_intro(lemma))

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"content/grammar/core_verbs_present_20261111.json").read_text("utf-8"))
SOURCE="independent_core_present_verbs_20261111"
LANGS=("ru","en","zh","ar","es","pt")
PERSON=("Εγώ","Εσύ","Η Μαρία","Εμείς","Εσείς","Αυτοί")
EXPECTED={
 "λέω":("λέω","λες","λέει","λέμε","λέτε","λένε"),
 "πάω":("πάω","πας","πάει","πάμε","πάτε","πάνε"),
 "τρώω":("τρώω","τρως","τρώει","τρώμε","τρώτε","τρώνε"),
 "ακούω":("ακούω","ακούς","ακούει","ακούμε","ακούτε","ακούνε"),
 "κλαίω":("κλαίω","κλαις","κλαίει","κλαίμε","κλαίτε","κλαίνε"),
 "φταίω":("φταίω","φταις","φταίει","φταίμε","φταίτε","φταίνε")
}
ALLOWED_ALTERNATES={
 "λέω":{"5":["λεν"]},
 "πάω":{"0":["πηγαίνω"],"1":["πηγαίνεις"],"2":["πηγαίνει"],
       "3":["πηγαίνουμε"],"4":["πηγαίνετε"],
       "5":["πηγαίνουν","παν"]},
 "τρώω":{},
 "ακούω":{"5":["ακούν"]},
 "κλαίω":{},
 "φταίω":{}
}
LABEL={
 "form":{
  "ru":"Впиши форму «{lemma}» по лицу и контексту. Точное написание важно.",
  "en":"Type the present form of “{lemma}” for this person and context. Spelling matters.",
  "zh":"根据人称和情境输入“{lemma}”的现在时形式，注意拼写。",
  "ar":"اكتب صيغة المضارع للفعل «{lemma}» بحسب الشخص والسياق، مع مراعاة الإملاء.",
  "es":"Escribe la forma de «{lemma}» según la persona y el contexto. Cuida la ortografía.",
  "pt":"Escreve a forma de «{lemma}» segundo a pessoa e o contexto. Atenção à grafia."
 },
 "semantic":{
  "ru":"Выбери глагол, который подходит по смыслу короткого разговора.",
  "en":"Choose the verb that makes sense in this short conversation.",
  "zh":"根据简短对话的含义选择正确的动词。",
  "ar":"اختر الفعل المناسب لمعنى الحوار القصير.",
  "es":"Elige el verbo que tiene sentido en esta conversación breve.",
  "pt":"Escolhe o verbo adequado ao sentido deste diálogo curto."
 }
}

assert DATA["version"]==1 and len(DATA["verbs"])==6
PARADIGMS={}
for spec in DATA["verbs"]:
    lemma=spec["lemma"]
    assert lemma not in PARADIGMS and lemma in EXPECTED
    assert spec["forms"]==list(EXPECTED[lemma]),lemma
    assert spec["acceptedAlternatives"]==ALLOWED_ALTERNATES[lemma],lemma
    assert spec["chapter"]==(6 if lemma=="πάω" else 7),lemma
    PARADIGMS[lemma]=spec
assert set(PARADIGMS)==set(EXPECTED)

CARDS=[]
assert len(DATA["cards"])==48
for pos,raw in enumerate(DATA["cards"],370):
    cid=f"g2261021_{pos:03d}"
    assert raw["id"]==cid
    lemma=raw["lemma"]
    spec=PARADIGMS[lemma]
    person=raw["person"]
    chapter=raw["chapter"]
    assert 0<=person<6 and chapter in (6,7)
    assert chapter>=spec["chapter"],cid
    assert INDEX[chapter]["start"]<=INDEX[chapter]["end"]
    assert raw["correct"]==spec["forms"][person],cid
    prompt=raw["prompt"]
    assert prompt.count("___")==1 and prompt==unicodedata.normalize("NFC",prompt)
    assert not any(token in prompt for token in ("χθες","θα "," να ")),cid
    skill=raw["skill"]
    assert skill in LABEL
    if skill=="form":
        assert prompt.startswith(PERSON[person]+" "),cid
        accepted=[raw["correct"],*ALLOWED_ALTERNATES[lemma].get(str(person),[])]
        assert raw["accepted"]==accepted,cid
        options=[raw["correct"],*[
            other for other in spec["forms"] if other!=raw["correct"]
        ][:3]]
        typed=True
    else:
        assert skill=="semantic" and prompt.startswith("Α: ")
        assert "\nΒ: " in prompt,cid
        assert raw["wrong"] and len(raw["wrong"])==3
        options=[raw["correct"],*raw["wrong"]]
        assert all(other in EXISTING_CONTRASTS for other in raw["wrong"]),cid
        assert {EXISTING_CONTRASTS[other][0] for other in raw["wrong"]}=={
            "A","B1","B2"
        },cid
        assert all(EXISTING_CONTRASTS[other][1]<=chapter
                   for other in raw["wrong"]),(cid,raw["wrong"])
        accepted=None
        typed=False
    assert len(options)==len(set(options))==4 and options[0]==raw["correct"],cid
    translations=raw["translations"]
    assert set(translations)==set(LANGS)
    assert all(isinstance(translations[lang],str) and translations[lang].strip()
               and translations[lang]==unicodedata.normalize("NFC",translations[lang])
               for lang in LANGS),cid
    card=dict(
        id=cid,kind="grammar",chapter=chapter,unit=chapter,
        page=INDEX[chapter]["start"]+min((pos-370)%6,INDEX[chapter]["end"]-INDEX[chapter]["start"]),
        topic="Γραμματική · Συνηρημένα ρήματα",group="verb_core",skill=skill,
        source=SOURCE,book_page_verified=False,page_anchor_approximate=True,
        gr=prompt,prompt=prompt,correct=raw["correct"],options=options,
        typedAnswer=typed,lemma=lemma,person=person,personName=PERSON[person],
        fullTranslations=translations,grammar_tags=[],
        **{lang:LABEL[skill][lang].format(lemma=lemma) for lang in LANGS}
    )
    if typed:card["acceptedForms"]=accepted
    pedagogy_rules.tag(card)
    assert card["curriculum_ready_unit"]<=chapter,(cid,card["curriculum_ready_unit"])
    CARDS.append(card)
assert len(CARDS)==48 and len({c["id"] for c in CARDS})==48
assert len({c["prompt"] for c in CARDS})==48
assert Counter(c["skill"] for c in CARDS)=={"form":36,"semantic":12}
assert Counter(c["lemma"] for c in CARDS)==dict.fromkeys(PARADIGMS,8)
assert Counter(c["person"] for c in CARDS if c["skill"]=="form")==dict.fromkeys(range(6),6)
BY_ID={c["id"]:c for c in CARDS}

def _norm(word):
    return unicodedata.normalize("NFC",str(word).strip()).casefold()

def _without_accent(word):
    value=unicodedata.normalize("NFD",_norm(word))
    return "".join(ch for ch in value if not unicodedata.combining(ch))

ERROR_TEXT={
 "accent":{
    "ru":"Ошибка в ударении: сравни tonos с правильной формой.",
    "en":"Accent error: compare the tonos with the correct form.",
    "zh":"重音错误：请对照正确形式检查重音符号。",
    "ar":"خطأ في النبر: قارن علامة النبر بالصيغة الصحيحة.",
    "es":"Error de acento: compara la tilde con la forma correcta.",
    "pt":"Erro de acentuação: compara o acento com a forma correta."
 },
 "person":{
    "ru":"Выбрана форма другого лица или числа. Проверь подлежащее.",
    "en":"This is a different person's or number's form. Check the subject.",
    "zh":"这是另一人称或单复数的形式。请检查主语。",
    "ar":"هذه صيغة لشخص أو عدد آخر. تحقق من الفاعل.",
    "es":"Es la forma de otra persona o número. Comprueba el sujeto.",
    "pt":"É a forma de outra pessoa ou número. Confere o sujeito."
 },
 "spelling":{
    "ru":"Форма написана неверно. У этих глаголов особые изменения основы и окончания.",
    "en":"The spelling is not accepted. These verbs have specific stem and ending patterns.",
    "zh":"拼写不正确。这些动词有特定的词干和词尾变化。",
    "ar":"الكتابة غير صحيحة. لهذه الأفعال تغيّرات خاصة في الجذر والنهاية.",
    "es":"La grafía no es correcta. Estos verbos tienen cambios propios de raíz y terminación.",
    "pt":"A grafia não está correta. Estes verbos têm padrões próprios de radical e terminação."
 },
 "meaning":{
    "ru":"По смыслу диалога требуется другой глагол.",
    "en":"The dialogue context calls for a different verb.",
    "zh":"根据对话含义，这里需要另一个动词。",
    "ar":"السياق في الحوار يتطلب فعلاً آخر.",
    "es":"El contexto del diálogo requiere otro verbo.",
    "pt":"O sentido do diálogo pede outro verbo."
 }
}

def classify_mistake(card,selected,lang):
    """Post-score only: errors in tonos, person/number, spelling or meaning."""
    assert card.get("group")=="verb_core" and lang in LANGS
    if card["skill"]=="semantic":
        return "meaning",ERROR_TEXT["meaning"][lang]
    used=_norm(selected)
    accepted=card["acceptedForms"]
    if (used not in {_norm(x) for x in accepted}
            and _without_accent(used) in {_without_accent(x) for x in accepted}):
        category="accent"
    elif any(used==_norm(x) for pos,form in enumerate(EXPECTED[card["lemma"]])
             if pos!=card["person"]
             for x in (form,*ALLOWED_ALTERNATES[card["lemma"]].get(str(pos),[]))):
        category="person"
    else:
        category="spelling"
    return category,ERROR_TEXT[category][lang]
