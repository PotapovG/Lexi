"""Transparent, conservative question distractor ranking for Greek practice.

Never invent translations, never decide that a new synonym is an accepted
answer and never permit out-of-stage material ahead of stage-local options.
The result is a *ranking* of stored editorial answer candidates only.
"""
from difflib import SequenceMatcher
import re
import unicodedata
import greek_variants
import pedagogy_rules

ARTICLE={'ο','η','το','οι','τα','τον','την','τη','τους','τις'}
GREEK_TENSE=re.compile(r'\b(?:θα|χθες|πέρσι|προχθές|αύριο|σήμερα|να|δεν|μην)\b',re.I)
def greek(card):
    return card.get('gr') or card.get('sg') or card.get('pl') or ''

def norm(text):
    text=unicodedata.normalize('NFC',str(text or '')).casefold().strip()
    return re.sub(r'[\s.!?;:·,]+',' ',text).strip()

def topic_set(card):
    tags=card.get('topics') or []
    if not isinstance(tags,(tuple,list,set)):tags=[]
    result=set(str(t) for t in tags if t)
    title=card.get('topic','')
    if title and title not in ('Διαλόγοι','Γραμματική','Λέξεις'):result.add(str(title))
    return result

def same_sense_or_variant(target,other):
    # Exact alternate Greek spellings approved in the teaching dataset are
    # NEVER plausible "wrong" choices; their grading is a separate matter.
    a=greek(target)
    b=greek(other)
    if not a or not b:return False
    return norm(b) in {norm(x) for x in greek_variants.accepted(a)}

def same_english_meaning(target,other):
    return bool(target.get('en') and other.get('en') and
                norm(target['en'])==norm(other['en']))

def rank(target,other,lang,stage,noise=0.0):
    word=greek(target);alt=greek(other)
    normalized=pedagogy_rules.canonical_greek(word)
    similar=pedagogy_rules.canonical_greek(alt)
    original_count=len(word.split())
    other_count=len(alt.split())
    form_a=word.split(' ',1)[0].casefold()
    form_b=alt.split(' ',1)[0].casefold()
    topic_overlap=bool(topic_set(target)&topic_set(other))
    same_article=(form_a==form_b and form_a in ARTICLE)
    primary_markers=set(GREEK_TENSE.findall(word.casefold()))
    other_markers=set(GREEK_TENSE.findall(alt.casefold()))
    tense_gap=len(primary_markers^other_markers)
    same_kind=target['kind']==other['kind']
    learned=(0<=other.get('chapter',0)<=stage and
             other.get('curriculum_ready_unit',other['chapter'])<=stage)
    # Keep earlier, same-morphology cards ahead of unrelated material;
    # close length and tense make answers challenging without being random.
    return (not learned,not same_kind,not topic_overlap,
            other['chapter']!=target['chapter'],
            (form_a in ARTICLE and not same_article),
            tense_gap,
            abs(original_count-other_count),
            abs(len(normalized)-len(similar)),
            -SequenceMatcher(None,normalized,similar).ratio(),
            noise)
