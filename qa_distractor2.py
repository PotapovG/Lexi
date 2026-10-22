#!/usr/bin/env python3
"""Sampling / invariants for advanced Greek answer-choice quality and locale."""
import collections,random,tempfile
from pathlib import Path
import server,accepted_glosses,greek_variants,distractor_quality as dq
assert len(server.PRACTICE_ALL)==1978 and len(server.ALL)==1795
assert dq.same_sense_or_variant({'gr':'επτά'},{'gr':'εφτά'})
assert dq.same_sense_or_variant({'gr':'ο αδελφός'},{'gr':'ο αδερφός'})
assert not dq.same_sense_or_variant({'gr':'ο φίλος'},{'gr':'η φίλη'})
assert dq.same_english_meaning({'en':'Thank you.'},{'en':'thank you'})
assert not dq.same_english_meaning({'en':'Hello'},{'en':'Goodbye'})
kinds=('word','number','phrase','sentence','plural')
samples=[]
for kind in kinds:
 cards=[c for c in server.ALL if c['kind']==kind]
 picks=cards[:min(13,len(cards))]+cards[-min(10,len(cards)):]
 samples.extend(picks)
samples.extend(server.EXTRA_ALL[:12])
seen=collections.Counter()
langs=('ru','en','zh','ar','es','pt')
with tempfile.TemporaryDirectory(prefix='lexi-distractor2-') as tmp:
 old=server.DB;server.DB=str(Path(tmp)/'student.sqlite3')
 try:
  server.init_db()
  for c in samples:
   if c['kind'] not in kinds:continue
   dirs=('sg-pl','pl-sg') if c['kind']=='plural' else ('gr-ru','ru-gr')
   for lang in langs:
    for direction in dirs:
     q=server.format_question(c,direction,lang)
     assert len(q['choices'])==8 and len(set(q['choices']))==8,(c['id'],lang,direction)
     right=server.shape(c,direction,lang)[1]
     accepted=accepted_glosses.accepted(c,direction,lang,right)
     assert right in q['choices'],(c['id'],lang,direction)
     # All reviewed synonym variants must remain correct; other choices
     # are never accepted as a reviewed alternate of the SAME target.
     for choice in q['choices']:
      if choice not in accepted:
       assert not accepted_glosses.is_accepted(c,direction,lang,choice,right)
     assert q['id']==c['id']
     seen[(c['kind'],lang,direction)]+=1
  assert sum(seen.values())>650,sum(seen.values())
  with server.conn() as db:assert db.execute('pragma quick_check').fetchone()[0]=='ok'
 finally:server.DB=old
print('PASS DISTRACTOR2: tested',sum(seen.values()),'8-choice banks, 5 exercise types,'
      ' 6 languages, two directions, exact Greek variant filtering and accepted synonyms unchanged')
