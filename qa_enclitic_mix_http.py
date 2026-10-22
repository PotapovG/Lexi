#!/usr/bin/env python3
"""End-to-end isolated HTTP: Greek enclitic + embedded approved Pocket listening."""
import json,os,socket,subprocess,sys,tempfile,time,urllib.error,urllib.parse,urllib.request,uuid
from pathlib import Path
import server
with tempfile.TemporaryDirectory(prefix='lexi-enclitic-http-') as folder:
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(folder)/'progress.sqlite3'))
    proc=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),env=env,
                    stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    base='http://127.0.0.1:'+str(port)
    def get(route,body=None,cookie=None):
        hdr={'Origin':'https://potapovfamily.com'}
        if cookie:hdr['Cookie']=cookie
        if body is not None:hdr['Content-Type']='application/json'
        rq=urllib.request.Request(base+route,data=json.dumps(body).encode('utf-8') if body is not None else None,headers=hdr)
        with urllib.request.urlopen(rq,timeout=9) as response:
            return response.status,json.loads(response.read()),response.headers
    try:
        for i in range(40):
            try:
                if get('/health')[0]==200:break
            except (TimeoutError,OSError):time.sleep(.15)
        else:raise AssertionError('local backend unavailable')
        status,meta,_=get('/api/catalog')
        assert status==200 and meta['cardCount']==1795 and meta['supplementalEnclitics']==26
        assert meta['practiceCardCount']==1978 and meta['listeningCount']==717
        assert 'enclitic' in meta['types']
        status,account,headers=get('/api/auth/register',dict(nickname='EncliticQA'+uuid.uuid4().hex[:8]))
        assert status==200,account
        cookie=headers.get('Set-Cookie','').split(';',1)[0]
        assert cookie.startswith('greek_session=')
        status,group,_=get('/api/quiz?scope=chapters&chapters=1,2,3,4&types=word,phrase,sentence,enclitic&count=60&lang=ru&listenMix=1',cookie=cookie)
        assert status==200,group
        assert group['mixedListening']==12
        assert len(group['questions'])==60
        assert sum(q['kind']=='listening' for q in group['questions'])==12
        assert len({q['id'] for q in group['questions']})==60
        status,only,_=get('/api/quiz?scope=chapters&chapters=1,2,3,4&types=enclitic&count=60&lang=ru&listenMix=1',cookie=cookie)
        assert status==200
        assert only['mixedListening']==0 and only['questions']
        assert all(x['kind']=='enclitic' for x in only['questions'])
        q=only['questions'][0];orig=server.ENCLITIC_BY_ID[q['id']]
        assert len(q['choices'])==4 and len(set(q['choices']))==4
        assert q['wordAudio']['audioSource']=='pocket'
        assert q['wordAudio']['audioUrl'].startswith('/greek/pronunciation/')
        # Same UUID must not double-score.
        payload=dict(id=q['id'],direction='stress_enclitic',selected=orig['correct'],lang='ru',
                     requestId=str(uuid.uuid4()),srsOptIn=True)
        status,ok,_=get('/api/answer',payload,cookie=cookie)
        assert status==200 and ok['correct'] and ok['tonosHint']
        status,replay,_=get('/api/answer',payload,cookie=cookie)
        assert replay==ok
        listen=next(q for q in group['questions'] if q['kind']=='listening')
        answer=server.LISTEN_BY_ID[listen['id']]['ru']
        status,aud,_=get('/api/answer',dict(id=listen['id'],direction='listen',lang='ru',selected=answer),cookie=cookie)
        assert status==200 and aud['correct'] and aud['transcript']
        status,stat,_=get('/api/stats',cookie=cookie)
        assert status==200 and stat['attempts']==2 and stat['correct']==2
        assert 'enclitic' in stat['byKind'] if 'byKind' in stat else True
        status,cap,_=get('/api/capacity?scope=chapters&chapters=1,2,3,4&types=word,phrase,sentence,enclitic&duration=20&lang=ru&listenMix=1',cookie=cookie)
        assert cap['listeningMixEnabled'] and cap['listeningMixAvailable']>=12
        status,nomix,_=get('/api/quiz?scope=chapters&chapters=1,2,3,4&types=word,phrase,sentence,enclitic&count=60&lang=ru&listenMix=0',cookie=cookie)
        assert nomix['mixedListening']==0
        assert not any(q['kind']=='listening' for q in nomix['questions'])
        print('PASS ENCLITIC+MIX HTTP: student auth, 1978 cards, 26 enclitics,'
              ' mixed 12/60 listening, 4 contrastive choices, exact Pocket WAV,'
              ' answer+idempotent replay, 2 attempts/stats, capacity and opt-out')
    finally:
        proc.terminate()
        try:proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.communicate(timeout=4)
