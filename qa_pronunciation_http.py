#!/usr/bin/env python3
"""Isolated HEAD/GET test for signed-off pronunciation hash URLs and path bypass."""
import os,socket,subprocess,sys,tempfile,time,urllib.request,urllib.error
from pathlib import Path
import pronunciation_audio as audio
source=next(iter(audio.BY_FILE))
with tempfile.TemporaryDirectory(prefix='lexi-pronaudio-http-') as temp:
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(temp)/'test.sqlite3'))
    process=subprocess.Popen([sys.executable,'server.py'],cwd=str(Path(__file__).parent),env=env,
                             stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    def get(path,method='GET'):
        try:
            with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:'+str(port)+path,method=method),
                                        timeout=7) as r:return r.status,r.headers,r.read()
        except urllib.error.HTTPError as e:return e.code,e.headers,e.read()
    try:
        for _ in range(40):
            try:
                if get('/health')[0]==200:break
            except OSError:time.sleep(.13)
        else:raise AssertionError('temporary server not ready')
        path='/pronunciation/'+source
        code,head,body=get(path,'HEAD')
        assert code==200 and int(head['Content-Length'])>5000 and not body
        code,headers,wav=get(path)
        assert code==200 and headers['Content-Type']=='audio/wav' and wav[:4]==b'RIFF'
        assert len(wav)==int(head['Content-Length'])
        for bad in ('/pronunciation/no.wav','/pronunciation/../server.py',
                    '/pronunciation/'+'f'*32+'.wav','/pronunciation/'+source+'.txt'):
            code,_,_=get(bad)
            assert code==404,(bad,code)
        print('PASS PRONUNCIATION HTTP: WAV/HEAD200, hash allowlist, path traversal, no auth/synthesis')
    finally:
        process.terminate()
        try:process.communicate(timeout=5)
        except subprocess.TimeoutExpired:process.kill();process.communicate(timeout=3)
