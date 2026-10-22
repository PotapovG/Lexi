"""Accent pedagogy + stage-gated verb exercises; isolated SQLite only."""
from pathlib import Path
import tempfile, collections
import server
import verb_curriculum,accent_guidance
from topics_verbs import VERBS
assert len(server.ALL)==1795
assert len(VERBS)==len(verb_curriculum.FIRST_UNIT)==17
verbs=[c for c in server.ALL if c['kind']=='verb']
assert len(verbs)==102 and len({c['id'] for c in verbs})==102
assert all(c['introducedUnit']==verb_curriculum.first_unit(c['gr']) for c in verbs)
with tempfile.TemporaryDirectory() as root:
 server.DB=str(Path(root)/'qa.sqlite3');server.init_db()
 base=dict(scope=['verbs'],types=['verb'],groups=['A,B1,B2'],levels=['A1,A2'],lang=['ru'],count=['60'])
 def run(stage):
  return server.make_quiz('test',{**base,'maxUnit':[str(stage)]})['questions']
 assert len(run(2))==6 and {q['id'] for q in run(2)}=={f'verb02_{i}' for i in range(6)}
 assert len(run(4))==42
 assert all(q['introducedUnit']<=4 for q in run(4))
 assert len({server.BY_ID[q['id']]['gr'] for q in run(4)})==7
 assert all(q['verbGroup'] in ('A','B1','B2') for q in run(20))
 assert {q['introducedUnit'] for q in run(20)}<=set(verb_curriculum.FIRST_UNIT.values())
 assert len(run(20))==60
 assert len(run(100))==60 and len(run(-100))==0 # clamped to unit1
 assert len(server.make_quiz('test',base)['questions'])==42 # default earliest 4
 # Capacity estimation uses the same stage gate; no session progress writes.
 for step,expected in ((2,6),(4,42),(20,102)):
  cap=server.estimate_capacity('test',{**base,'maxUnit':[str(step)],'duration':['30']})
  assert cap['uniqueCards']==expected,(step,cap)
  assert cap['requiredAt20Seconds']==90
  assert cap['enoughAt20Seconds']==(step==20)
 chapters=server.estimate_capacity('test',{'scope':['chapters'],'chapters':['1,2,3,4,5'],
       'types':['word,number,phrase,sentence,dialogue,accent'],'duration':['30']})
 assert chapters['uniqueCards']>=90 and chapters['enoughAt20Seconds']
 assert chapters['approximate'] and chapters['durationMinutes']==30

 early=server.make_quiz('test',{**base,'maxUnit':['4'],'groups':['B2']})['questions']
 assert not early # B2 group comes later
 late=server.make_quiz('test',{**base,'maxUnit':['16'],'groups':['B2']})['questions']
 assert late and all(q['introducedUnit']<=16 for q in late)
 for lang in ('ru','en','zh','ar','es','pt'):
  card=server.BY_ID['stress_w028']
  q=server.format_question(card,'accent',lang)
  assert len(q['letters'])==len(card['base'])
  assert len(q['accentableIndices'])>=2
  assert card['accent_index'] in q['accentableIndices']
  assert all(card['base'][i] in 'αεηιουω' for i in q['accentableIndices'])
  assert 'ει' in q['tonosHint'] and 'ου' in q['tonosHint']
  for cid,pair in [('stress_x06w018','πότε'),('stress_x07w001','ποσό'),('stress_x05w012','μέτρο')]:
   q=server.format_question(server.BY_ID[cid],'accent',lang)
   assert pair in q['tonosHint']
  result=server.mark('accent-'+lang,dict(id=card['id'],direction='accent',lang=lang,selected=str(card['accent_index'])))
  assert result['correct'] and result['missDebt']==0 and 'ει' in result['tonosHint']
 # One textbook accent card remains exactly one question and existing ID,
 # and one verb form uses old direction/grading/progress.
 c=server.BY_ID['verb08_0']
 assert c['gr']=='μιλάω' and c['accepted']==['μιλάω','μιλώ']
 for selected in c['accepted']:
  assert server.mark('v',dict(id=c['id'],direction='conjugate',lang='ru',selected=selected))['correct']
 with server.conn() as db:assert db.execute('pragma quick_check').fetchone()[0]=='ok'
print('PASS verb step gate: 2->6 questions, 4->42 questions, full 20->102 forms, A1/A2 and groups preserved')
print('PASS Greek tonos vowel positions + minimal pairs and six-language contextual explanation')
print('PASS unique-card capacity estimate: 30min=90 at 20s/card, no hidden repeat/fake guarantee')
print('PASS old verb IDs/alternate forms and stress IDs unchanged, no progress/database migration')
