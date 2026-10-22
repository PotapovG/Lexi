"""Comprehensive 700/1000 editorial vocabulary regression test; never touches prod database."""
from pathlib import Path
import collections, hashlib, sqlite3, tempfile, re, unicodedata
import vocab_lessons as v
import personalized as pers
import server
from catalog_v2 import ALL

counts=collections.Counter(w['level'] for w in v.VOCAB)
assert len(v.VOCAB)==1700 and counts=={'A1':700,'A2':1000}
assert len(v.VOCAB_BY_ID)==len(v.VOCAB)
curated=[w for w in v.VOCAB if w['source']=='original_curated_vocab1700']
assert len(curated)==872

# Basic teaching-data integrity checks.
topics={x['id'] for x in v.THEMES}
for word in v.VOCAB:
    gr,ru,en=word['gr'],word['ru'],word['en']
    assert gr.strip()==gr and ru.strip()==ru and en.strip()==en,word
    assert all([gr,ru,en,word['topics']]),word
    assert all(t in topics for t in word['topics']),word
    assert all(not ('<' in field or '>' in field or '\n' in field) for field in (gr,ru,en)),word
    assert re.search(r'[\u0370-\u03ff\u1f00-\u1fff]',gr),word
    assert re.search(r'[\u0400-\u052f]',ru),word

assert all(w['level']=='A1' for w in curated[:249])
assert all(w['level']=='A2' for w in curated[249:])
assert all(len(re.sub(r'^(?:ο|η|το|οι|τα)\s+','',x['gr']).split())==1
           for x in curated if x['level']=='A2')

topic_counts=collections.Counter(t for w in v.VOCAB for t in w['topics'])
assert len(topic_counts)==13 and min(topic_counts.values())>=80

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'qa.sqlite3')
    server.init_db()
    with server.conn() as db:
        user='test-user-1700'
        for topic in sorted(topics):
            for level in ['A1','A2']:
                for lang in ['ru','en','zh','ar','es','pt']:
                    lesson=v.lesson(db,user,topic,level,lang)
                    assert len(lesson['words'])==10,(topic,level,lang,lesson)
                    assert lesson['total']>=10,(topic,level)
                    assert all(len(row['choices'])==8 and len(set(row['choices']))==8 for row in lesson['words']),(topic,level,lang)
                    assert all(row['level']==level for row in lesson['words'])
                    assert lesson['learned']==0 and lesson['remaining']==lesson['total']
        newest=next(x for x in curated if x['level']=='A2')
        assert not pers.is_learned(db,user,newest['id'])
        got=v.answer(db,user,{'id':newest['id'],'lang':'ru','direction':'target-gr','selected':newest['gr']})
        assert got['correct']
    with server.conn() as db:
        assert pers.is_learned(db,user,newest['id'])
        assert pers.progress_summary(db,user)['learned']==1
        assert any(c['id']=='personal_'+newest['id'] for c in pers.learned_cards(db,user))
        miss=v.answer(db,user,{'id':newest['id'],'lang':'ru','direction':'target-gr','selected':'INVALID'})
        assert not miss['correct']
        assert not pers.is_learned(db,user,newest['id'])
        due=v.lesson(db,user,newest['topics'][0],'A2','ru',review=True)
        assert newest['id'] in {w['id'] for w in due['words']}
        for _ in range(2):
            v.answer(db,user,{'id':newest['id'],'lang':'ru','direction':'target-gr','selected':newest['gr']})
        assert pers.is_learned(db,user,newest['id'])
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
    for scope in ('book','personalized'):
        mode=('textbook' if scope=='book' else 'personalized')
        quiz=server.make_quiz('test-user-1700',{'scope':['pages'],'types':['word'],'study':[mode],
                 'lang':['ru'],'from':['1'],'to':['56'],'count':['30']})
        assert len(quiz['questions'])>=20
        if scope=='personalized':
            assert any(q['id']=='personal_'+newest['id'] for q in quiz['questions'])
        else:
            assert all(not q['id'].startswith('personal_') for q in quiz['questions'])

print('PASS: exact 1700 unique cards, A1=700, A2=1000; +872 stable-ID curated headwords')
print('PASS: 13 topic classifications, >=80 entries/topic; Greek/Russian/English complete')
print('PASS: 13 topics × 2 levels × 6 languages = 156 themed 10-word, 8-choice lessons')
print('PASS: lesson weak review and per-account personalized unlock/relock without production DB')
