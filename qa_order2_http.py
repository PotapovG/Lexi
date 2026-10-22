import collections
#!/usr/bin/env python3
"""Real local HTTP sentence-building practice with additive valid alternatives."""
import json,os,socket,subprocess,sys,tempfile,time,urllib.error,urllib.request,uuid
from pathlib import Path
import server
with tempfile.TemporaryDirectory(prefix='lexi-builder-http-') as root:
 s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
 proc=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),
     env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(root)/'db.sqlite3')),
     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 def req(route,body=None,cookie=None):
  headers={'Origin':'https://potapovfamily.com'}
  if body is not None:headers['Content-Type']='application/json'
  if cookie:headers['Cookie']=cookie
  r=urllib.request.Request('http://127.0.0.1:'+str(port)+route,
      data=json.dumps(body,ensure_ascii=False).encode('utf-8') if body is not None else None,headers=headers)
  with urllib.request.urlopen(r,timeout=8) as response:
   return response.status,json.loads(response.read()),response.headers
 try:
  for _ in range(45):
   try:
    if req('/health')[0]==200:break
   except OSError:time.sleep(.15)
  else:raise AssertionError('server not healthy')
  status,cat,_=req('/api/catalog')
  assert status==200 and cat['practiceCardCount']==1978 and cat['supplementalOrder2']==40
  status,_,h=req('/api/auth/register',{'nickname':'Order2QA'+uuid.uuid4().hex[:6]})
  assert status==200
  cookie=h.get('Set-Cookie','').split(';',1)[0]
  status,quiz,_=req('/api/quiz?scope=chapters&chapters=6&types=order&count=60&lang=ru',cookie=cookie)
  assert status==200 and quiz['count']>=1
  assert all(q['kind']=='order' and q['chapter']==6 for q in quiz['questions'])
  card=next(q for q in quiz['questions'] if q['id'].startswith('or261021_') and q['alternativeOrderCount']>0)
  parent=server.ORDER2_BY_ID[card['id']]
  assert collections.Counter(card['tokens'])==collections.Counter(parent['tokens'])
  alternates=server._order_variants.VARIANTS.get(parent['id'])
  assert alternates and card['alternativeOrderCount']>=1
  selected=alternates[0]
  body={'id':parent['id'],'direction':'arrange','lang':'ru','selected':selected,
        'requestId':str(uuid.uuid4()),'srsOptIn':True}
  status,answer,_=req('/api/answer',body,cookie=cookie)
  assert status==200 and answer['correct'] and answer['acceptedOrderCount']>=2
  status,replay,_=req('/api/answer',body,cookie=cookie)
  assert replay==answer
  status,stats,_=req('/api/stats',cookie=cookie)
  assert stats['attempts']==1 and stats['correct']==1
  print('PASS ORDER2 HTTP: catalog 1978 +40, unit6 word builder, accepted semantic variant, UUID replay and SRS')
 finally:
  proc.terminate()
  try:proc.communicate(timeout=4)
  except subprocess.TimeoutExpired:proc.kill();proc.communicate(timeout=4)
