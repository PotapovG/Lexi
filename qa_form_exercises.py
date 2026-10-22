"""Book-informed article/case and sentence-building exercise regression.

Verified source book unit 2 printed p28-35: prepositional article / places;
unit 3 p38-47: family / gender; unit 4 p48-58: direct object forms;
unit 8 p94-107: purchases and articles. Exercises authored independently.
"""
from collections import Counter
from pathlib import Path
import random,sqlite3,tempfile
import server
import accepted_glosses

assert len(server.ALL)==1795
articles=[c for c in server.ALL if c['kind']=='article']
orders=[c for c in server.ALL if c['kind']=='order']
assert len(articles)==24 and len(orders)==17
assert Counter(x['chapter'] for x in articles)=={2:8,3:4,4:8,8:4}
assert all(5<=len(c['tokens'])<=18 for c in orders)
assert all(c['curriculum_ready_unit']<=c['chapter'] for c in articles+orders)
assert len({c['id'] for c in articles+orders})==41
for c in articles:
 assert c['prompt'].count('___')==1 and c['gr']==c['prompt'].replace('___',c['correct'])
 assert len(c['options'])==len(set(c['options']))==8 and c['correct'] in c['options']
for language in ('ru','en','zh','ar','es','pt'):
 for c in articles+orders:
  d='fill' if c['kind']=='article' else 'arrange'
  q=server.format_question(c,d,language)
  assert q['prompt'] and q['note']
  if c['kind']=='article':
   assert len(q['choices'])==len(set(q['choices']))==8 and c['correct'] in q['choices']
  else:
   assert Counter(q['tokens'])==Counter(c['tokens'])
   assert server.shape(c,d,language)[1]==' '.join(c['tokens'])

with tempfile.TemporaryDirectory() as temp:
 server.DB=str(Path(temp)/'test.sqlite3');server.init_db()
 for chapter in (1,2,3,4,8):
  params={'scope':['chapters'],'chapters':[str(chapter)],'types':['article,order'],
          'lang':['pt'],'count':['60'],'mode':['all']}
  q=server.make_quiz('learner',params)
  assert q['questions'],chapter
  assert all(item['chapter']==chapter for item in q['questions'])
  assert all(item['kind'] in ('article','order') for item in q['questions'])
 assert all(item['kind'] not in ('article','order') for item in server.make_quiz('learner',
          {'scope':['chapters'],'chapters':['1'],'types':['article'],'lang':['ru'],'count':['60']})['questions'])
 # Curated alternate translations are explicitly accepted without changing
 # the original progress key or affecting wrong choices.
 for language,cid,value in [('ru','p001','Как тебя зовут'),('ru','p014','Он живёт в Афинах.' ),
                             ('en','p003','Pleased to meet you!')]:
  c=server.BY_ID[cid]
  choices=server.format_question(c,'gr-ru',language)['choices']
  assert value in choices,(cid,language)
  correct=server.mark('learner',{'id':cid,'direction':'gr-ru','lang':language,'selected':value})
  assert correct['correct'] and value in correct['acceptedAnswers']
  assert correct['answer']==c[language]
 assert not server.mark('learner',dict(id='p001',direction='gr-ru',lang='ru',selected='Как вас зовут?'))['correct']
 # Correct and incorrect answers/weak debt for new Greek-only drills.
 for c,d in [(articles[0],'fill'),(orders[0],'arrange')]:
  bad=server.mark('learner',dict(id=c['id'],direction=d,lang='pt',selected='неверно'))
  assert not bad['correct'] and bad['missDebt']==2
  weak=server.make_quiz('learner',{'mode':['weak_all'],'lang':['en'],'count':['60']})
  assert any(q['id']==c['id'] for q in weak['questions'])
  correct=server.shape(c,d,'pt')[1]
  for debt in (1,0):
   good=server.mark('learner',dict(id=c['id'],direction=d,lang='en',selected=correct))
   assert good['correct'] and good['missDebt']==debt
 # Reversed word order should be wrong when restoring a specific given
 # sentence, rather than accepting random permutations as grammatically valid.
 first=orders[0]
 bad=' '.join(reversed(first['tokens']))
 assert bad!=first['gr']
 wrong=server.mark('learner',dict(id=first['id'],direction='arrange',lang='ru',selected=bad))
 assert not wrong['correct']
 for q in server.make_quiz('outsider',{'mode':['weak_all'],'lang':['ru'],'count':['60']})['questions']:
  assert False,('cross-user leak',q)
 with server.conn() as db:assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS 24 Greek article/case 8-option blanks at real unit 2/3/4/8; 17 word-order puzzles')
print('PASS all six locales, original Greek sentence reconstruction, correct/weak grading')
print('PASS reviewed alternative translations RU/EN accepted; wrong-case/register still wrong; user isolation')
