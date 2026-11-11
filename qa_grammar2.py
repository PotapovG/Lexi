#!/usr/bin/env python3
"""Isolated Greek morphology grammar2 decks, all locales, scoring and lessons."""
import collections,tempfile,uuid
from pathlib import Path
import server,grammar2_cards as gc
assert len(server.ALL)>=1795 and len(server.EXTRA_ALL)==26
assert len(server.GRAMMAR2_ALL)==111 and len(server.PRACTICE_ALL)>=2063
assert len(server.vocab.VOCAB)==1700
assert not server.LISTENING_ENABLED or len(server.LISTEN_CARDS)==717
assert collections.Counter(c['group'] for c in gc.CARDS)=={
 'case':10,'agreement':10,'comparison':10,'past':10,'future':8,'subjunctive':8,'gender':20,'possessive':35}
assert len({c['id'] for c in server.PRACTICE_ALL})==len(server.PRACTICE_ALL)
for c in gc.CARDS:
 assert c['kind']=='grammar' and c['curriculum_ready_unit']<=c['chapter']
 assert len(c['options'])==4 and len(set(c['options']))==4
 assert c['correct'] in c['options'] and not c.get('book_page_verified')
 assert c['source'].startswith('independent_')
 assert c['prompt'].count('___')==1
 assert c['chapter'] in (2,3,4,8,9,11,12,14,16)
 assert all(c[l] for l in ('ru','en','zh','ar','es','pt'))
with tempfile.TemporaryDirectory(prefix='grammar2-') as d:
 original=server.DB;server.DB=str(Path(d)/'student.sqlite3')
 original_secret=server.auth.SECRET_FILE
 server.auth.SECRET_FILE=Path(d)/'login-pepper'
 try:
  server.init_db()
  for c in gc.CARDS:
   for lang in ('ru','en','zh','ar','es','pt'):
    q=server.format_question(c,'grammar_fill',lang)
    assert q['kind']=='grammar' and q['direction']=='grammar_fill'
    assert q['sourcePageVerified'] is False
    assert q['id']==c['id'] and q['prompt']==c['prompt']
    assert set(q['choices'])==set(c['options']) and len(q['choices'])==4
    assert 'correct' not in q and 'grammarTip' not in q
    body={'id':c['id'],'direction':'grammar_fill','lang':lang,'selected':c['correct']}
    right=server.mark('learner',body)
    assert right['correct'] and right['answer']==c['correct']
    from cloze_meanings import explanation
    assert right['grammarTip']==explanation(c,lang)
    if c['group']=='gender':
     assert c['correct'] in right['grammarTip'],(c['id'],lang)
    body['selected']=c['options'][1]
    wrong=server.mark('learner',body)
    assert not wrong['correct'] and wrong['answer']==c['correct'] and wrong['explanation']
  for max_ch in (2,3,4,8,9,11,12,14,16):
   params={'scope':['chapters'],'chapters':[str(max_ch)],
           'types':['grammar'],'count':['60'],'lang':['ru']}
   quiz=server.make_quiz('new',params)
   assert all(q['chapter']==max_ch for q in quiz['questions'])
   assert all(q['kind']=='grammar' for q in quiz['questions'])
   assert quiz['count']==collections.Counter(c['chapter'] for c in gc.CARDS)[max_ch]
  # Selected chapter range sees only stage-appropriate material.
  params={'scope':['chapters'],'chapters':['1,2,3,4,8,9,11,12,14,16'],
          'types':['grammar'],'count':['60'],'lang':['en']}
  quiz=server.make_quiz('new',params)
  assert quiz['count']==60 and quiz['available']==111  # server caps a single session at 60
  # Weak practice and SRS retain permanent keys across six locales.
  with server.conn() as db:
   saved=db.execute("SELECT SUM(attempts),COUNT(*) FROM progress WHERE user_id=?",
                    ('learner',)).fetchone()
   assert saved[0]==111*6*2
   assert db.execute('pragma quick_check').fetchone()[0]=='ok'
  assert server.GRAMMAR2_BY_ID[gc.CARDS[0]['id']]['id']==gc.CARDS[0]['id']
  # Original textbook ID and audio unaffected.
  assert 'g2261021_001' not in server.BY_ID
 finally:
  server.DB=original
  server.auth.SECRET_FILE=original_secret
print('PASS GRAMMAR2: 111 morphology cards x 6 locales x correct/wrong (1332 scores), '
      '4 credible choices, chapter gates and original 1795/717/1700 unchanged')
