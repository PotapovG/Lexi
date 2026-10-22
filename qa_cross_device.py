#!/usr/bin/env python3
"""Cross-device lesson state validation, isolation and concurrency (temp SQLite)."""
import copy,json,sqlite3,tempfile,time,uuid
from pathlib import Path
import lesson_session_sync as sync
def guid():return str(uuid.uuid4())
def snapshot():
 return {'version':2,'nickname':'LessonQAStudent',
  'questions':[{'id':'w001','kind':'word','direction':'gr-ru','choices':['a']*8,'prompt':'Γεια σου'}],
  'index':0,'settings':{'lang':'ru'},'started':int(time.time()*1000),
  'deadline':int(time.time()*1000)+60_000,'count':0,'correct':0,'wrong':0,
  'pendingAnswer':None,'savedAt':int(time.time()*1000)}
def raises(call,text):
 try:call()
 except ValueError as e:
  assert text in str(e),(text,str(e))
 else:raise AssertionError('expected ValueError '+text)
good=snapshot()
invalids=[
 ('missing questions',dict(good,questions=[])),
 ('too many questions',dict(good,questions=good['questions']*61)),
 ('bad index',dict(good,index=1)),
 ('bad index type',dict(good,index=True)),
 ('bad settings',dict(good,settings=[])),
 ('bad lang-free username',dict(good,nickname='x')),
 ('deadline expired',dict(good,deadline=int(time.time()*1000)-70_000)),
 ('deadline too distant',dict(good,deadline=int(time.time()*1000)+3*60*60_000)),
 ('oversize payload',dict(good,questions=[dict(good['questions'][0],prompt='a'*245760)]))
]
for name,snap in invalids:raises(lambda s=snap:sync.validate_snapshot(s),'too large' if name=='oversize payload' else 'invalid session')
with tempfile.TemporaryDirectory(prefix='lexi-account-sync-unit-') as root:
 dbpath=Path(root)/'temp.sqlite3'
 def open_db():
  db=sqlite3.connect(dbpath,timeout=15)
  db.row_factory=sqlite3.Row
  return db
 with open_db() as db:sync.schema(db)
 uid1='student-alpha';uid2='student-beta'
 sid=guid();a=guid();b=guid()
 with open_db() as db:
  start=sync.action(db,uid1,{'op':'start','sessionId':sid,'deviceId':a,'snapshot':good})
  assert start['saved'] and start['revision']==1
 with open_db() as db:
  assert sync.read(db,uid1)['exists']
  assert not sync.read(db,uid2)['exists']
  # Repeated start is harmless and must preserve subsequent saves.
  snap2=dict(good,count=1)
  saved=sync.action(db,uid1,{'op':'save','sessionId':sid,'deviceId':a,'revision':1,'snapshot':snap2})
  assert saved['revision']==2
 with open_db() as db:
  rep=sync.action(db,uid1,{'op':'start','sessionId':sid,'deviceId':a,'snapshot':good})
  assert rep['revision']==2
  assert sync.read(db,uid1)['snapshot']['count']==1
  db.commit()
  raises(lambda:sync.action(db,uid1,{'op':'start','sessionId':guid(),'deviceId':b,'snapshot':good}),
         'session_conflict')
 with open_db() as db:
  claimed=sync.action(db,uid1,{'op':'takeover','sessionId':sid,'deviceId':b,'revision':2})
  assert claimed['revision']==3
 with open_db() as db:
  raises(lambda:sync.assert_owner(db,uid1,{'sessionId':sid,'deviceId':a}), 'session_conflict')
  sync.assert_owner(db,uid1,{'sessionId':sid,'deviceId':b})
  sync.assert_owner(db,uid1,{})  # legacy mode compatible
 with open_db() as db:
  raises(lambda:sync.action(db,uid1,{'op':'save','sessionId':sid,'deviceId':a,'revision':2,'snapshot':good}),
         'session_conflict')
 with open_db() as db:
  assert sync.action(db,uid1,{'op':'clear','sessionId':sid,'deviceId':b,'revision':2})['cleared']
  assert sync.read(db,uid1)=={'exists':False}
  assert db.execute('pragma quick_check').fetchone()[0]=='ok'
 print('PASS CROSS_DEVICE VALIDATION: 9 malformed/oversize snapshots rejected, account-isolated,'
       ' idempotent start, takeover CAS, old owner locked out, safe clear, legacy supported')
