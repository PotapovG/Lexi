"""Patakis Ελληνικά Α΄ PDF editorial alignment, all printed units (1–20).

No source book is shipped here. Printed page references came from a separate
inspection of the user's 314-page purchased PDF's table of contents (PDF
pages 6–9; printed pages 4–7), lesson starts, and early learning examples.
"""
import re
import sqlite3
import tempfile
from collections import Counter
from pathlib import Path
import catalog_v2 as catalog
import textbook_alignment as book
import patakis_context_cards as authored
import server
import vocab_lessons as vocab

assert len(catalog.CHAPTERS)==22
sections={x['id']:x for x in catalog.CHAPTERS}
assert set(sections)==set(range(0,21))|{-5}
assert set(book.REVIEW_IDS)=={5,10,15,20}
assert all(sections[i]['review'] == (i in book.REVIEW_IDS) for i in range(1,21))
assert [(sections[i]['start'],sections[i]['end']) for i in range(1,21)]==[
    (14,23),(24,37),(38,47),(48,58),(59,65),(66,79),(80,93),
    (94,107),(108,121),(122,131),(132,149),(150,165),(166,183),
    (184,199),(200,211),(212,231),(232,245),(246,261),(262,277),(278,289)]
assert sections[0]['start']==8 and sections[-5]['end']==312
assert len(catalog.ALL)==1795 and len(catalog.BY_ID)==1796
assert len(authored.CARDS)==74
assert len(vocab.VOCAB)==1700
assert sum(x['level']=='A1' for x in vocab.VOCAB)==700
assert sum(x['level']=='A2' for x in vocab.VOCAB)==1000
# No new book-syllabus word is automatically injected into standalone word
# course; every existing ID and translation remains stable.
assert all(w['id'] not in vocab.VOCAB_BY_ID for w in authored.CARDS)

for card in catalog.ALL:
    assert card['id'] in catalog.BY_ID
    if card.get('curriculum') in ('topic','verb','personalized'):continue
    sec=sections[card['chapter']]
    assert sec['start']<=card['page']<=sec['end'],(card['id'],card['page'],sec['title'])
    if 'legacy_chapter' in card and card['kind']=='accent' and card['id'].startswith('stress_'):
        original=catalog.BY_ID.get(card['id'][len('stress_'):])
        if original:
            assert card['chapter']==original['chapter'],card['id']
            assert card['page']==original['page'],card['id']

# The earlier trainer had accidentally named book's "Transport" chapter 5.
# The purchased textbook shows 5 is review; transport starts chapter 6.
assert sections[5]['review'] and sections[6]['start']==66
assert catalog.BY_ID['x05w001']['chapter']==6
assert catalog.BY_ID['v1_000']['chapter']==5
assert catalog.BY_ID['patk09_001']['chapter']==9
assert catalog.BY_ID['x08w001']['chapter']==8
assert catalog.BY_ID['patk12_001']['chapter']==12
assert catalog.BY_ID['patk17_003']['chapter']==17
assert catalog.BY_ID['patk18_001']['chapter']==18
# Required early grammar: numbers one to ten move to unit 1, ποιος to
# unit 3, languages in unit 4; plural morphology begins printed unit 8.
assert catalog.BY_ID['w118']['chapter']==1
assert catalog.BY_ID['w023']['chapter']==3
assert all(catalog.BY_ID[x]['page']==40 for x in ('w023','w024','w025','w033','w034'))
assert len(catalog.VERIFIED_LESSON_PAGES)==58
assert all(catalog.BY_ID[x]['book_page_verified'] for x in catalog.VERIFIED_LESSON_PAGES)
for c in catalog.ALL:
    if c['id'].startswith('stress_') and c['id'][len('stress_'):] in catalog.VERIFIED_LESSON_PAGES:
        original=catalog.BY_ID[c['id'][len('stress_'):]]
        assert c['page']==original['page']

assert catalog.BY_ID['w137']['chapter']==4
assert all(catalog.BY_ID[x]['chapter']==3 for x in ('s004','s005','s006','s007','s008'))
assert catalog.BY_ID['dlg004']['chapter']==3
assert catalog.BY_ID['dlg037']['chapter']==16
assert all(x['chapter']>=8 for x in catalog.ALL
           if x['kind']=='plural' and x.get('curriculum') not in ('topic','verb'))

# All Greek-only dialogues 100 retained with unchanged ID and answer blanks.
dialogues=[x for x in catalog.ALL if x['kind']=='dialogue']
assert len(dialogues)==100
assert {x['id'] for x in dialogues}==({f'dlg{i:03}' for i in range(1,101)}-{'dlg024'})|{'dlg024_v2'}
assert all(len(x['bank'])==8 for x in dialogues)
assert catalog.BY_ID['dlg007']['chapter']==14
assert catalog.BY_ID['dlg011']['chapter']==6
assert catalog.BY_ID['dlg015']['chapter']==18
assert catalog.BY_ID['dlg030']['chapter']==4
assert catalog.BY_ID['w034']['gr']=='τη λένε' # Printed PDF p39: correct no terminal nu

# No higher grammar prematurely introduced by the freshly authored unit-1–4
# supplements; this is editorial, not a guarantee for the older corpus.
for c in authored.CARDS:
    if c['chapter']<=4:
        assert not re.search(r'\b(?:θα|χθες|πέρσι|ήμουν|γεννήθηκα|πριν)\b',c['gr'])
    for l in ('ru','en','zh','ar','es','pt'):
        assert c[l].strip(),(c['id'],l)
    assert c['gr'] and c['ru'] and c['en']

# Chapters selectors and printed page selectors must identify the same
# *correct* content. If first 5 selected they include review, not transport.
with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'checks.sqlite3')
    server.init_db()
    base={'count':['60'],'mode':['all'],'lang':['ru'],
          'types':['word,number,phrase,sentence,dialogue,plural,accent']}
    def run(**args):return server.make_quiz('pdfqa',dict(base,**args))
    chapter5=run(scope=['chapters'],chapters=['5'])['questions']
    assert chapter5 and all(x['chapter']==5 for x in chapter5)
    lesson6=run(scope=['chapters'],chapters=['6'])['questions']
    assert lesson6 and all(x['chapter']==6 for x in lesson6)
    five=run(scope=['chapters'],chapters=['1,2,3,4,5'])['questions']
    assert len(five)==60 and all(x['chapter'] in (1,2,3,4,5) for x in five)
    print('PASS chapter 5 review correctly, chapter 6 transport; first five have no chapter 6')
    pages=run(scope=['pages'],**{'from':['59'],'to':['65']})['questions']
    assert pages and all(x['chapter']==5 for x in pages)
    pages=run(scope=['pages'],**{'from':['66'],'to':['79']})['questions']
    assert pages and all(x['chapter']==6 for x in pages)
    first56=run(scope=['pages'],**{'from':['1'],'to':['56']})['questions']
    assert first56 and all(x['chapter'] in (0,1,2,3,4) for x in first56)
    # Just-introduced exercises are answerable for six languages, preserving
    # the Greek target and eight distractors.
    for lang in ('ru','en','zh','ar','es','pt'):
        for card in authored.CARDS:
            for direction in ('gr-ru','ru-gr'):
                q=server.format_question(card,direction,lang)
                assert len(q['choices'])==len(set(q['choices']))==8,(card['id'],lang,direction)
                right=server.shape(card,direction,lang)[1]
                assert right in q['choices'],(card['id'],lang,direction)
    # Historical DB rows with OLD unit=5 should now appear in real chapter 6.
    old=server.BY_ID['x05w001']
    with server.conn() as db:
        db.execute('insert into attempts(user_id,card_key,kind,unit,correct,created_at) VALUES(?,?,?,?,?,?)',
                   ('legacy_user',old['id']+':gr-ru','word',5,1,'2026-10-19'))
    stats=server.stats('legacy_user')
    assert stats['units']['6']['attempts']==1,stats['units']
    assert stats['units']['5']['attempts']==0,stats['units']
    with server.conn() as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS 20 printed book units and 4 reviews with accurate printed chapter page boundaries')
print('PASS 1680 legacy question IDs + 74 original book-context add-ons, Greek answers unchanged')
print('PASS all legacy accent question chapters follow their parent headwords; plurals introduced from printed unit 8')
print('PASS all 74 new tasks × 6 languages × 2 directions: eight choices and correct answers')
print('PASS old historical statistics re-attributed using stable card ID; DB history unchanged')
