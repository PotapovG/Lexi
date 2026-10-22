"""Editorial grammar prerequisite metadata for independent Greek practice.

Grounding: paid Ελληνικά Α΄ PDF, printed units 1–4, pp14–58, and
verified unit headings in textbook_alignment.py. These are *curriculum*
introduction milestones, not assertions every term first appears verbatim
on the card's approximate page. The app must never expose book exercises.
"""
import re
import unicodedata
from hashlib import sha256

GRAMMAR_FIRST_UNIT = {
    'alphabet': 0,
    'stress_syllables': 1,
    'greeting_be': 1,
    'address_home_present': 2,
    'family_profession_question': 3,
    'languages_b1_and_object_articles': 4,
    'transport_and_time': 6,
    'routine_and_days': 7,
    'enclitic_stress': 3,
    'plural_nouns': 8,
    'clothing_adjective_agreement': 9,
    'home_comparatives': 11,
    'aorist_narrative': 12,
    'future_tense': 14,
    'subjunctive_na': 16,
    'imperative': 17,
    'medical_conditional': 18,
}
# Curated high-confidence prerequisites. A Greek idiom in a later stage can
# contain an earlier grammatical form; therefore tag rather than interpret
# every token as a universal marker of a conjugation system.
PREMATURE_TEXT_RULES = (
    ('aorist_narrative', re.compile(r'\b(?:ήρθες|ήρθα|ήμουν|ήταν|πήγα|πήγαμε|έδωσα|είδα|χθες)\b',re.I)),
    ('future_tense', re.compile(r'\bθα\b',re.I)),
    ('subjunctive_na', re.compile(r'\b(?:μπορείς να|θέλεις να|πρέπει να|προτιμώ να|πάμε να)\b',re.I)),
    ('medical_conditional', re.compile(r'\bαν\s+(?:έχεις|νιώθεις|χρειάζεσαι)',re.I)),
)
# Textbook does not introduce these *verbs/expressions* in the printed
# first four units (checked book text, pp14–58; no match for respective
# phrases). Move original content, retain stable progress IDs.
LEXICAL_INTRO_OVERRIDES = {
    'dlg022': 7,  # idiomatic error acknowledgement; not unit-one introductions
    'dlg023': 13, # καλώς ήρθες: aorist of έρχομαι, too early for unit 1
    'dlg036': 7,  # μαθαίνω: general ongoing activities, not lesson-four dialogue
    'dlg038': 17, # passive γράφεται and spelling instructions
    'dlg039': 7,  # μαθαίνω before its curricular vocabulary introduction
    'dlg040': 17, # passive γράφεται and letter-by-letter dictation
    # dlg005 is source-aligned to printed unit 11 (age question) in CARD_OVERRIDES.
    'dlg007': 14, # coffee with future θα πάρετε, first introduced with future tense
    'dlg045': 16, # future θα and invitation να -> later planning/socializing
    'dlg051': 14, # shopping line with future θα πάρω
    'dlg054': 14, # future θα το δοκιμάσω
    'dlg060': 16, # θέλεις να αγοράσουμε: unit 16 subjunctive
    'dlg065': 16, # future θα μετακομίσεις
    'dlg070': 14, # future θα φύγει
    'dlg077': 16, # θέλεις να πάμε
    'dlg078': 16, # μπορείς να έρθεις
    'x12p004': 16, # πρέπει να φύγω
}

def canonical_greek(text):
    text=text.strip().casefold()
    text=' '.join(text.split())
    # Preserve grammatical distinctions that carry actual meaning:
    # τον/τη λένε are OBJECT PRONOUNS + verb, not articles to erase;
    # ο/η σύζυγος has a sex-specific feminine/masculine referent.
    # Generic article-stripping remains for ordinary nominal headwords so
    # 'ο υπάλληλος' and 'υπάλληλος' still study as the same word.
    if re.fullmatch(r'(?:τον|την|τη|το) λένε',text):
        return text
    if text in ('ο σύζυγοσ','η σύζυγοσ'):
        return text
    text=re.sub(r'^(?:ο|η|το|οι|τα|τον|την|τη|τους|τις)\s+','',text)
    return text


def semantic_id(card):
    # For accent cards, the lexical target is the accented original Greek word
    # (not the unaccented, rendered choice prompt).
    greek=card.get('accented') or card.get('gr') or card.get('sg') or card.get('base') or card['id']
    digest=sha256(canonical_greek(greek).encode('utf-8')).hexdigest()[:16]
    return 'lex_'+digest


def tag(card):
    kind=card['kind']
    unit=card.get('chapter',0)
    if card.get('curriculum') in ('topic','verb','personalized'):
        return card
    features=set(card.get('grammar_tags',[]))
    if unit==0:features.add('alphabet')
    if unit>=1 and unit<=4:
        features.add({1:'greeting_be',2:'address_home_present',3:'family_profession_question',4:'languages_b1_and_object_articles'}[unit])
    if kind=='plural':features.add('plural_nouns')
    gr=' '.join(card.get('lines',[])) if kind=='dialogue' else card.get('gr','')
    for feature,matcher in PREMATURE_TEXT_RULES:
        if matcher.search(gr):features.add(feature)
    earliest=max([GRAMMAR_FIRST_UNIT[x] for x in features] or [unit if unit>0 else 0])
    card['grammar_tags']=sorted(features)
    card['curriculum_ready_unit']=earliest
    card['semanticId']=semantic_id(card)
    return card
