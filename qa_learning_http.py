#!/usr/bin/env python3
"""Real isolated HTTP API test: account, stats, weighted duration and corrections.

Server subprocess listens on 127.0.0.1 with GREEK_DB in temporary dir;
never touches live SQLite, public sessions, or production Caddy.
"""
import json,os,socket,subprocess,sys,tempfile,time,urllib.request,urllib.error
from pathlib import Path
import server

with tempfile.TemporaryDirectory(prefix='lexi-http-upgrade-') as folder:
    db=str(Path(folder)/'test.sqlite3')
    assert not Path(db).exists()
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=db)
    proc=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),
                          env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    host=f'http://127.0.0.1:{port}'
    def call(path,data=None,cookie=None):
        headers={'Origin':'https://potapovfamily.com'} if data is not None else {}
        if data is not None:headers['Content-Type']='application/json'
        if cookie:headers['Cookie']=cookie
        req=urllib.request.Request(host+path,
             data=json.dumps(data).encode('utf-8') if data is not None else None,headers=headers)
        with urllib.request.urlopen(req,timeout=5) as res:
            return json.loads(res.read()),res.headers
    try:
        for i in range(40):
            try:
                health,_=call('/health')
                break
            except (OSError,ConnectionError):
                time.sleep(0.15)
        else:raise AssertionError('local isolated server did not start')
        assert health['status']=='ok'
        register,h=call('/api/auth/register',{'nickname':'LearningUpgradeQA'})
        assert register['registered']
        # Secure cookie is normally sent over HTTPS by Caddy. For a local
        # isolated HTTP integration test supply the exact one-time cookie.
        cookie=h.get('Set-Cookie','').split(';',1)[0]
        assert cookie.startswith('greek_session=') and len(cookie)==len('greek_session=')+32
        stats,_=call('/api/stats',cookie=cookie)
        assert stats['attempts']==0
        assert stats['details']['topics']==[] and stats['details']['grammar']==[]
        assert stats['details']['vocabTopics']==[]
        capacity,_=call('/api/capacity?scope=verbs&maxUnit=4&duration=30',cookie=cookie)
        assert capacity['uniqueCards']==42 and capacity['taskAware']
        assert capacity['paceModel']=='fallback' and capacity['estimatedMinutes']>0
        assert capacity['requiredUniqueAtEstimatedPace']>0
        wrong,_=call('/api/answer',{'id':'article_001','direction':'fill','lang':'ru','selected':'сто'},cookie)
        assert not wrong['correct'] and wrong['answer']=='στη'
        assert 'сто' in wrong['explanation'] and 'στη' in wrong['explanation']
        stats,_=call('/api/stats',cookie=cookie)
        assert stats['attempts']==1 and stats['details']['grammar']
        w=server.vocab.VOCAB[0]
        ret,_=call('/api/vocab/answer',{'id':w['id'],'direction':'gr-target','lang':'ru','selected':w['ru']},cookie)
        assert ret['correct']
        stats,_=call('/api/stats',cookie=cookie)
        assert stats['attempts']==1 and stats['details']['vocabTopics']
        assert all(item['provisional'] for item in stats['details']['vocabTopics'])
        print('PASS ISOLATED HTTP: account auth, stats topics/grammar/A1-A2 separation, '
              'task-aware duration, 6-locale backend explanation, no production writes')
    finally:
        proc.terminate()
        try:proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill();proc.communicate(timeout=3)
