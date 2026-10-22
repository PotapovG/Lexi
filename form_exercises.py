"""Additional independently written grammar drills, staged to printed Ελληνικά Α΄.

Book unit 2 teaches places + σε/στον/στην/στο, unit 3 nominative articles
with professions/family, unit 4 object articles τον/τη/την/το, and unit 8
introduces buying food and nominative/accusative contrasts. Excerpts from
the bought PDF are NOT bundled. All prompts here are independently authored.

ORDER drills reuse the application's own original independently authored
sentences (their phrase/source ID is preserved separately).
"""
from patakis_context_cards import CARDS as PATK
ARTICLES=[]
_GROUPS={
  'places':('στο','στη','στην','στον','σε','ο','η','το'),
  'people':('ο','η','το','τον','τη','την','στο','στη'),
  'objects':('τον','τη','την','το','ο','η','οι','τα'),
}
# printed unit | approximate within-unit page | group | full original
# self-authored Greek cloze | expected article | skill label
_ITEMS=[
 (2,29,'places','Μένω ___ Λευκωσία.','στη'),
 (2,30,'places','Ο Πέτρος μένει ___ Αθήνα.','στην'),
 (2,31,'places','Ο Νίκος μένει ___ Πειραιά.','στον'),
 (2,33,'places','Η Κατερίνα μένει ___ σπίτι.','στο'),
 (2,34,'places','Μένουμε ___ Κύπρο.','στην'),
 (2,35,'places','Ο φίλος μου μένει ___ Στρόβολο.','στον'),
 (2,36,'places','Έχεις φίλο ___ Ελλάδα;','στην'),
 (2,37,'places','Το τηλέφωνο είναι ___ σπίτι.','στο'),
 (3,39,'people','___ μητέρα μου είναι δασκάλα.','η'),
 (3,40,'people','___ πατέρας μου είναι γιατρός.','ο'),
 (3,42,'people','___ παιδί μένει στην Αθήνα.','το'),
 (3,46,'people','___ αδελφή μου είναι φοιτήτρια.','η'),
 (4,51,'objects','Ξέρεις ___ Νίκο;','τον'),
 (4,52,'objects','Ξέρεις ___ Μαρία;','τη'),
 (4,54,'objects','Ξέρεις ___ Άννα;','την'),
 (4,55,'objects','Βλέπω ___ καθηγητή.','τον'),
 (4,55,'objects','Δεν καταλαβαίνω ___ λέξη.','τη'),
 (4,56,'objects','Ξέρεις ___ παιδί;','το'),
 (4,57,'objects','Ψάχνω ___ πατέρα μου.','τον'),
 (4,58,'objects','Η Ελένη ξέρει ___ φίλη σου.','τη'),
 (8,96,'objects','Αγοράζω ___ ψωμί.','το'),
 (8,100,'objects','Θέλω ___ εφημερίδα.','την'),
 (8,103,'objects','Παίρνω ___ ζάχαρη.','τη'),
 (8,106,'objects','Αγοράζω ___ γάλα.','το'),
]
# Curated examples where final -ν is commonly omitted according to the
# printed-school orthographic convention, but the retained-ν variant has the
# same feminine accusative case/gender. Do not generalize to vowels, κ/π/τ,
# clusters μπ/ντ/γκ/τσ/τζ, ξ/ψ, or masculine τον.
_ALLOW_RETAINED_N={1,14,17,20,23}  # στη Λευκωσία; τη Μαρία/λέξη/φίλη/ζάχαρη
_OPTIONAL_N={'τη':'την','στη':'στην'}
for i,(unit,page,group,prompt,correct) in enumerate(_ITEMS,1):
    bank=list(_GROUPS[group])
    assert len(bank)==len(set(bank))==8 and correct in bank
    assert prompt.count('___')==1
    full=prompt.replace('___',correct)
    accepted=[correct]
    if i in _ALLOW_RETAINED_N:
        # Explicit case identity only; the two forms are NOT generally
        # interchangeable outside this phonetic/orthographic context.
        assert correct in _OPTIONAL_N
        next_word=prompt.split('___',1)[1].strip().split()[0]
        assert next_word[0].casefold() in {'λ','μ','φ','ζ'},(i,next_word)
        accepted.append(_OPTIONAL_N[correct])
        assert accepted[1] in bank
    ARTICLES.append(dict(id=f'article_{i:03d}',kind='article',chapter=unit,unit=unit,page=page,
                 gr=full,prompt=prompt,correct=correct,options=bank,acceptedForms=accepted,
                 grammar_tags=['address_home_present' if unit==2 else
                               'family_profession_question' if unit==3 else
                               'languages_b1_and_object_articles' if unit==4 else 'plural_nouns'],
                 source='original_book_syllabus_grammar',
                 topic='Αρθρα · πτώσεις',
                 ru='Выбери подходящую греческую форму.',en='Choose the correct Greek form.',
                 zh='选择正确的希腊语形式。',ar='اختر الصيغة اليونانية الصحيحة.',
                 es='Elige la forma griega correcta.',pt='Escolhe a forma grega correta.'))

# Curated from ORIGINAL sentences already in Lexi, not transcription of PDF.
_ORDER_IDS=(
 'patk01_001','patk01_003','patk01_006',
 'patk02_001','patk02_003','patk02_005','patk02_006',
 'patk03_001','patk03_003','patk03_005','patk03_006',
 'patk04_001','patk04_003','patk04_005',
 'patk09_017','patk12_001','patk14_004',
)
_SOURCE={x['id']:x for x in PATK}
ORDERS=[]
for sourceid in _ORDER_IDS:
    original=_SOURCE[sourceid]
    tokens=original['gr'].split()
    assert 5<=len(tokens)<=18,(sourceid,len(tokens))
    item={key:original[key] for key in ('gr','ru','en','zh','ar','es','pt','page','chapter','unit','topic')}
    item.update(id='order_'+sourceid,kind='order',tokens=tokens,
           source='original_book_syllabus_sentence_order',
           grammar_tags=[],
           curriculum='textbook')
    ORDERS.append(item)
CARDS=ARTICLES+ORDERS
assert len(CARDS)==41 and len({x['id'] for x in CARDS})==41
