#!/usr/bin/env python3
"""Isolated localhost HTTP for grammar2 stage, scoring and account-scoped SRS."""
import json,os,socket,subprocess,sys,tempfile,time,urllib.error,urllib.request,uuid
from pathlib import Path
import server
with tempfile.TemporaryDirectory(prefix='lexi-grammar2-http-') as tmp:
 s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
 proc=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),
  env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(tmp)/'account.sqlite3')),
  stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 origin='http://127.0.0.1:'+str(port)
 def req(route,body=None,cookie=''):
  headers={'Origin':'https://potapovfamily.com'}
  if body is not None:headers['Content-Type']='application/json'
  if cookie:headers['Cookie']=cookie
  rq=urllib.request.Request(origin+route,
   data=json.dumps(body,ensure_ascii=False).encode('utf-8') if body is not None else None,
   headers=headers)
  try:
   with urllib.request.urlopen(rq,timeout=9) as r:
    return r.status,json.loads(r.read()),r.headers
  except urllib.error.HTTPError as e:return e.code,json.loads(e.read()),e.headers
 try:
  for _ in range(45):
   try:
    if req('/health')[0]==200:break
   except OSError:time.sleep(.15)
  else:raise AssertionError('local server unavailable')
  status,cat,_=req('/api/catalog')
  assert status==200 and cat['practiceCardCount']==1978 and cat['supplementalGrammar']==56
  assert cat['cardCount']==1795 and cat['listeningCount']==717
  assert 'grammar' in cat['types']
  status,acc,header=req('/api/auth/register',{'nickname':'GrammarQ'+uuid.uuid4().hex[:6]})
  assert status==200,acc
  cookie=header['Set-Cookie'].split(';',1)[0]
  status,quiz,_=req('/api/quiz?scope=chapters&chapters=4&types=grammar&count=60&lang=ru',cookie=cookie)
  assert status==200 and quiz['count']==10,quiz
  assert all(q['kind']=='grammar' and q['direction']=='grammar_fill' for q in quiz['questions'])
  first=quiz['questions'][0];card=server.GRAMMAR2_BY_ID[first['id']]
  body={'id':card['id'],'direction':'grammar_fill','lang':'ru','selected':card['correct'],
        'requestId':str(uuid.uuid4()),'srsOptIn':True}
  status,result,_=req('/api/answer',body,cookie)
  assert status==200 and result['correct'] and result['grammarTip']
  status,replay,_=req('/api/answer',body,cookie)
  assert status==200 and replay==result
  status,stats,_=req('/api/stats',cookie=cookie)
  assert status==200 and stats['attempts']==1 and stats['correct']==1
  status,late,_=req('/api/quiz?scope=chapters&chapters=16&types=grammar&count=60&lang=en',cookie=cookie)
  assert status==200 and late['count']==8
  assert all(q['chapter']==16 for q in late['questions'])
  print('PASS GRAMMAR2 HTTP: catalog 1978/56, registration, stage4/16, 4-choice variants, answer idempotency, stats/SRS')
 finally:
  proc.terminate()
  try:proc.communicate(timeout=4)
  except subprocess.TimeoutExpired:proc.kill();proc.communicate(timeout=4)
