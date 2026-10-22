#!/usr/bin/env python3
"""Real local HTTP smoke for syllable practice; no live SQLite or student session."""
import json,os,socket,subprocess,sys,tempfile,time,urllib.request,urllib.error,uuid
from pathlib import Path
import server
with tempfile.TemporaryDirectory(prefix='lexi-syllable-http-') as root:
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(root)/'student.sqlite3'))
    proc=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),
        env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    def call(path,body=None,cookie=''):
        headers={'Origin':'https://potapovfamily.com'}
        if body is not None:headers['Content-Type']='application/json'
        if cookie:headers['Cookie']=cookie
        req=urllib.request.Request('http://127.0.0.1:'+str(port)+path,
               data=json.dumps(body,ensure_ascii=False).encode('utf-8') if body is not None else None,
               headers=headers)
        try:
            with urllib.request.urlopen(req,timeout=7) as response:
                return response.status,json.loads(response.read()),response.headers
        except urllib.error.HTTPError as e:
            return e.code,json.loads(e.read()),e.headers
    try:
        for i in range(35):
            try:
                if call('/health')[0]==200:break
            except OSError:time.sleep(.15)
        else:raise AssertionError('isolated server not ready')
        status,cat,_=call('/api/catalog')
        assert status==200 and (cat['cardCount'],cat['supplementalCount'],cat['supplementalSyllables'],cat['practiceCardCount'],cat['listeningCount'])==(1795,26,35,1978,717)
        assert 'syllable' in cat['types']
        status,account,header=call('/api/auth/register',dict(nickname='SyllableQA'+uuid.uuid4().hex[:7]))
        assert status==200,account
        cookie=header.get('Set-Cookie','').split(';',1)[0]
        assert cookie.startswith('greek_session=')
        status,quiz,_=call('/api/quiz?scope=chapters&chapters=1,2,3,4&types=syllable&count=60&lang=ru',cookie=cookie)
        assert status==200,quiz
        assert quiz['questions'] and all(q['kind']=='syllable' for q in quiz['questions'])
        assert all(q.get('sourcePageVerified') is False for q in quiz['questions'])
        selected=quiz['questions'][0]
        assert 'correctIndex' not in selected
        assert len(selected['choices'])>=2 and len(selected['choices'])<=6
        source=server.SYLLABLE_BY_ID[selected['id']]
        correct=server.shape(source,'stress_syllable','ru')[1]
        reqid=str(uuid.uuid4())
        body=dict(id=source['id'],direction='stress_syllable',lang='ru',selected=correct,requestId=reqid,srsOptIn=True)
        status,answer,_=call('/api/answer',body,cookie)
        assert status==200 and answer['correct'] and answer['correctIndex']==source['stressedIndex']
        assert source['gr'] in answer['tonosHint']
        status,replayed,_=call('/api/answer',body,cookie)
        assert status==200 and replayed==answer
        status,stats,_=call('/api/stats',cookie=cookie)
        assert status==200 and stats['attempts']==1 and stats['correct']==1
        assert any(x['skill']=='stress_syllables' for x in stats['details']['skills'])
        assert any(x['id']=='stress_syllables' for x in stats['details']['grammar'])
        status,cap,_=call('/api/capacity?scope=chapters&chapters=9&types=dialogue,syllable&duration=20&lang=ru',cookie=cookie)
        assert status==200 and cap['grammarDeferred']>=1
        status,chapter9,_=call('/api/quiz?scope=chapters&chapters=9&types=dialogue,syllable&count=60&lang=ru',cookie=cookie)
        assert status==200 and chapter9['grammarDeferred']>=1
        assert all(q['id']!='dlg059' for q in chapter9['questions'])
        print('PASS SYLLABLE HTTP: catalog 1795+26+35, isolated registered learner, '
              'syllable-only quiz/answer/replay, grammar + stress skill stats, chapter9 gating')
    finally:
        proc.terminate()
        try:proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.communicate(timeout=3)

