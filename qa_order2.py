#!/usr/bin/env python3
"""Expanded Greek constructor cards, valid alternatives and strict SRS."""
import collections,tempfile,uuid
from pathlib import Path
import server,order2_cards as extension
import order_valid_permutations as valid
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert len(server.GRAMMAR2_ALL)==56 and len(server.ORDER2_ALL)==40
assert len(server.PRACTICE_ALL)==1978
assert len({c['id'] for c in server.PRACTICE_ALL})==1978
assert server._ORDER_VARIANT_COUNT==33
assert sum(bool(valid.VARIANTS.get(x['id'])) for x in server.ORDER2_ALL)==19
assert sum(c['kind']=='order' for c in server.PRACTICE_ALL)==65
for c in server.ORDER2_ALL:
 src=server.book_or_audio_card(c['source_parent_id'])
 assert src and src['kind']=='sentence'
 assert c['gr']==src['gr'] and c['semanticId']==src['semanticId']
 assert c['chapter']==src['chapter']
 assert c['book_page_verified'] is False
 assert c['source'].startswith('derived_')
 assert c['tokens']==c['gr'].split()
 for lang in ('ru','en','zh','ar','es','pt'):
  assert c[lang]==src[lang]
  q=server.format_question(c,'arrange',lang)
  assert q['kind']=='order' and q['direction']=='arrange'
  assert q['sourcePageVerified'] is False
  assert len(q['tokens'])==len(c['tokens'])
  assert collections.Counter(q['tokens'])==collections.Counter(c['tokens'])
  assert q['alternativeOrderCount']==len(valid.VARIANTS.get(c['id'],()))
  assert 'correct' not in q
with tempfile.TemporaryDirectory(prefix='lexi-order2-') as d:
 old=server.DB;server.DB=str(Path(d)/'student.sqlite3')
 try:
  server.init_db()
  for c in server.ORDER2_ALL:
   for lang in ('ru','en','zh','ar','es','pt'):
    ok=server.mark('learner',{'id':c['id'],'direction':'arrange','lang':lang,'selected':c['gr']})
    assert ok['correct']
    for alternative in valid.VARIANTS.get(c['id'],()):
     result=server.mark('learner',{'id':c['id'],'direction':'arrange','lang':lang,'selected':alternative})
     assert result['correct'],(c['id'],alternative)
    invalid=server.mark('learner',{'id':c['id'],'direction':'arrange','lang':lang,'selected':'ένα ένα βιβλίο δεν θα'})
    assert not invalid['correct']
  for chapters in ('6','12','18','1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19'):
   cfg={'scope':['chapters'],'chapters':[chapters],'types':['order'],
        'lang':['ru'],'count':['60']}
   result=server.make_quiz('fresh',cfg)
   assert all(q['kind']=='order' for q in result['questions'])
   assert all(q['chapter'] in set(map(int,chapters.split(','))) for q in result['questions'])
   assert len({x['semanticId'] for x in result['questions']})==len(result['questions'])
  with server.conn() as db:
   assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
  # Never broaden acceptance to any grammatical-looking random anagram.
  c=server.ORDER2_ALL[0]
  random_order=' '.join(reversed(c['tokens']))
  if valid.normalized(random_order) not in [valid.normalized(x) for x in valid.all_valid(c)]:
   assert not valid.matches(c,random_order)
 finally:
  server.DB=old
print('PASS ORDER2: +40 source-derived Greek builder sentences, 19 curated additional valid orders,'
      ' 6 locales, 65 total order exercises, no arbitrary anagrams, chapter scoping, old 1795+717 unchanged')
