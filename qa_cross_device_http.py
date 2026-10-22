#!/usr/bin/env python3
"""Two-device authenticated cross-device quiz handoff through real HTTP.

Uses disposable SQLite and two different browser-login cookies for the same
account plus a separate unrelated account. No production sessions or progress.
"""
import concurrent.futures,json,os,socket,subprocess,sys,tempfile,time,urllib.error,urllib.request,uuid
from pathlib import Path
import server
with tempfile.TemporaryDirectory(prefix='lexi-device-sync-') as root:
 s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
 proc=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),
     env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(root)/'students.sqlite3')),
     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 base='http://127.0.0.1:'+str(port)
 def request(path,body=None,cookie=None):
  headers={'Origin':'https://potapovfamily.com'}
  if body is not None:headers['Content-Type']='application/json'
  if cookie:headers['Cookie']=cookie
  req=urllib.request.Request(base+path,data=json.dumps(body,ensure_ascii=False).encode('utf-8') if body is not None else None,headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=12) as r:return r.status,json.loads(r.read()),r.headers
  except urllib.error.HTTPError as e:return e.code,json.loads(e.read()),e.headers
 try:
  for i in range(40):
   try:
    if request('/health')[0]==200:break
   except OSError:time.sleep(.15)
  else:raise AssertionError('isolated HTTP backend not ready')
  status,body,_=request('/api/session')
  assert status==401
  nick='CrossDevice'+uuid.uuid4().hex[:7]
  status,registration,h1=request('/api/auth/register',{'nickname':nick})
  assert status==200 and registration['code']
  c1=h1.get('Set-Cookie').split(';',1)[0]
  status,_,h2=request('/api/auth/login',{'code':registration['code']})
  assert status==200
  c2=h2.get('Set-Cookie').split(';',1)[0]
  assert c1!=c2
  status,_,h3=request('/api/auth/register',{'nickname':'OtherDevice'+uuid.uuid4().hex[:7]})
  assert status==200
  other=h3.get('Set-Cookie').split(';',1)[0]
  assert request('/api/session',cookie=other)[1]=={'exists':False}
  status,quiz,_=request('/api/quiz?scope=chapters&chapters=1,2,3,4&types=word&count=12&lang=ru',cookie=c1)
  assert status==200 and quiz['questions']
  q=quiz['questions'][0]
  sid=str(uuid.uuid4());d1=str(uuid.uuid4());d2=str(uuid.uuid4());d3=str(uuid.uuid4())
  snapshot={'version':2,'nickname':nick,'deadline':int(time.time()*1000)+1_200_000,
        'started':int(time.time()*1000),'settings':{'lang':'ru'},
        'mode':'all','questions':quiz['questions'],
        'index':0,'correct':0,'wrong':0,'count':0,'seen':[],
        'answered':False,'pendingAnswer':None,'savedAt':int(time.time()*1000)}
  start={'op':'start','sessionId':sid,'deviceId':d1,'revision':0,'snapshot':snapshot}
  status,started,_=request('/api/session',start,c1)
  assert status==200 and started['revision']==1
  status,remote,_=request('/api/session',cookie=c2)
  assert status==200 and remote['exists'] and remote['ownerDevice']==d1
  assert remote['snapshot']['questions']==snapshot['questions']
  assert request('/api/session',cookie=other)[1]=={'exists':False}
  # Commit first answer on device A, then simulate a lost response and
  # replay its immutable requestId after transferring to device B.
  target=server.book_or_audio_card(q['id'])
  answer=server.shape(target,q['direction'],'ru')[1]
  token=str(uuid.uuid4())
  post={'id':q['id'],'direction':q['direction'],'lang':'ru','selected':answer,
        'requestId':token,'srsOptIn':True,'sessionId':sid,'deviceId':d1}
  status,first,_=request('/api/answer',post,c1)
  assert status==200 and first['correct']
  status,claim,_=request('/api/session',
      {'op':'takeover','sessionId':sid,'deviceId':d2,'revision':1},c2)
  assert status==200 and claim['revision']==2 and claim['snapshot']==snapshot
  # Replay accepted after takeover because original receipt already committed.
  status,replayed,_=request('/api/answer',{**post,'deviceId':d2},c2)
  assert status==200 and replayed==first
  status,forbidden,_=request('/api/answer',{**post,'requestId':str(uuid.uuid4())},c1)
  assert status==409 and forbidden['error']=='session_conflict'
  status,forbidden,_=request('/api/session',{**start,'op':'save','revision':1},c1)
  assert status==409 and forbidden['error']=='session_conflict'
  advanced=dict(snapshot,index=1,count=1,correct=1,savedAt=int(time.time()*1000)+300)
  status,saved,_=request('/api/session',
      {'op':'save','sessionId':sid,'deviceId':d2,'revision':2,'snapshot':advanced},c2)
  assert status==200 and saved['revision']==3
  assert request('/api/session',cookie=c2)[1]['snapshot']['index']==1
  status,stats,_=request('/api/stats',cookie=c2)
  assert status==200 and stats['attempts']==1 and stats['correct']==1
  # Completed device can clear even if a recent save incremented revision.
  status,deleted,_=request('/api/session',
      {'op':'clear','sessionId':sid,'deviceId':d2,'revision':2},c2)
  assert status==200 and deleted['cleared']
  assert request('/api/session',cookie=c1)[1]=={'exists':False}
  # Two simultaneous attempts to claim one revision: exactly one succeeds.
  start={'op':'start','sessionId':sid,'deviceId':d1,'revision':0,'snapshot':snapshot}
  assert request('/api/session',start,c1)[0]==200
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   outcome=list(pool.map(lambda d:request('/api/session',
     {'op':'takeover','sessionId':sid,'deviceId':d,'revision':1},c2)[0],(d2,d3)))
  assert sorted(outcome)==[200,409],outcome
  print('PASS CROSS DEVICE HTTP: cookie auth, account isolation, resume snapshot,'
        ' explicit takeover, old-device 409, immutable-answer replay without duplicate,'
        ' CAS save, safe completion cleanup, simultaneous takeover one winner')
 finally:
  proc.terminate()
  try:proc.communicate(timeout=4)
  except subprocess.TimeoutExpired:proc.kill();proc.communicate(timeout=4)
