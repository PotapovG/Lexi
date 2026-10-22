#!/usr/bin/env python3
"""Two HTTP backends, one temp SQLite: replay after lost response / concurrent 502 retries."""
import concurrent.futures
import json,os,socket,sqlite3,subprocess,sys,tempfile,time,urllib.error,urllib.request,uuid
from pathlib import Path
import server
def port():
    s=socket.socket();s.bind(('127.0.0.1',0));n=s.getsockname()[1];s.close();return n
with tempfile.TemporaryDirectory(prefix='greek-bluegreen-retry-') as td:
    db=Path(td)/'test.sqlite3';ports=[port(),port()]
    procs=[]
    try:
        for number in ports:
            env=dict(os.environ,GREEK_PORT=str(number),GREEK_DB=str(db))
            procs.append(subprocess.Popen([sys.executable,'server.py'],
                cwd=str(Path(__file__).parent),env=env,
                stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
        def req(number,path,body=None,cookie=None):
            headers={'Origin':'https://potapovfamily.com'}
            if body is not None:headers['Content-Type']='application/json'
            if cookie:headers['Cookie']=cookie
            request=urllib.request.Request(f'http://127.0.0.1:{number}{path}',
                data=(json.dumps(body,ensure_ascii=False).encode('utf-8') if body is not None else None),
                headers=headers)
            try:
                with urllib.request.urlopen(request,timeout=12) as response:
                    return response.status,json.loads(response.read()),response.headers
            except urllib.error.HTTPError as error:
                return error.code,json.loads(error.read()),error.headers
        for number in ports:
            for _ in range(45):
                try:
                    if req(number,'/health')[0]==200:break
                except OSError:time.sleep(.15)
            else:raise AssertionError('backend did not become healthy')
        code,res,header=req(ports[0],'/api/auth/register',{'nickname':'HttpRetryQA'+uuid.uuid4().hex[:6]})
        assert code==200,res
        cookie=header.get('Set-Cookie','').split(';',1)[0]
        assert cookie.startswith('greek_session=')
        original=server.BY_ID['article_001']
        body={'id':original['id'],'direction':'fill','lang':'ru','selected':original['correct'],
              'srsOptIn':True,'requestId':str(uuid.uuid4())}
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            replies=list(pool.map(lambda i:req(ports[i%2],'/api/answer',body,cookie),range(24)))
        assert len(replies)==24
        assert all(x[0]==200 and x[1]==replies[0][1] for x in replies),replies
        # Simulated lost response: client retries same UUID on switched worker.
        code,again,_=req(ports[1],'/api/answer',body,cookie)
        assert code==200 and again==replies[0][1]
        altered=dict(body,selected='η')
        code,err,_=req(ports[1],'/api/answer',altered,cookie)
        assert code==400 and 'invalid request' in err['error']
        code,stats,_=req(ports[1],'/api/stats',cookie=cookie)
        assert code==200 and stats['attempts']==1 and stats['correct']==1
        with sqlite3.connect(db) as dbconn:
            assert dbconn.execute('select count(*) from attempts').fetchone()[0]==1
            assert dbconn.execute('select count(*) from answer_receipts').fetchone()[0]==1
            assert dbconn.execute('select count(*) from srs_schedule').fetchone()[0]==1
            assert dbconn.execute('select attempts from progress').fetchone()[0]==1
        status,quiz,_=req(ports[0],'/api/quiz?types=sentence&chapters=18&lang=ru&count=60',cookie=cookie)
        assert status==200,quiz
        assert any(q['id'].startswith('sx261021_') for q in quiz['questions']),quiz['questions']
        print('PASS DUAL HTTP: 24 concurrent retry deliveries across two workers => 1 attempt/receipt/SRS,'
              ' same replay response after simulated lost 502, conflict 400, later-unit 18 selectable')
    finally:
        for proc in procs:
            proc.terminate()
            try:proc.communicate(timeout=4)
            except subprocess.TimeoutExpired:proc.kill();proc.communicate()
