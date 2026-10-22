"""End-to-end local HTTP audio lookup for phonetics and A1/A2 vocab.

Starts a disposable SQLite-backed Greek trainer server on a random localhost
port; no real student progress, Caddy/VPN/Matrix or production API writes.
"""
import json,os,socket,subprocess,sys,tempfile,time,urllib.error,urllib.request,uuid
from pathlib import Path
import server
with tempfile.TemporaryDirectory(prefix='greek-audio-http-') as d:
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    env=dict(os.environ,GREEK_PORT=str(port),GREEK_DB=str(Path(d)/'isolated.sqlite3'))
    proc=subprocess.Popen([sys.executable,'server.py'],env=env,cwd=str(Path(__file__).parent),
                    stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    origin='http://127.0.0.1:'+str(port)
    def request(path,body=None,cookie=None,method=None):
        headers={'Origin':'https://potapovfamily.com'}
        if cookie:headers['Cookie']=cookie
        if body is not None:headers['Content-Type']='application/json'
        req=urllib.request.Request(origin+path,
            data=json.dumps(body).encode('utf-8') if body is not None else None,
            headers=headers,method=method)
        with urllib.request.urlopen(req,timeout=7) as response:
            return response.status,response.read(),response.headers
    try:
        for i in range(45):
            try:
                if request('/health')[0]==200:break
            except OSError:time.sleep(0.17)
        else:raise AssertionError('isolated HTTP server failed: '+proc.stderr.read().decode()[:500])
        for src in ('/app.js','/vocab.js','/greek_word_audio.js','/styles.css'):
            status,_,h=request(src,method='HEAD')
            assert status==200 and h['Content-Length']!='0',src
        status,raw,h=request('/api/vocab/meta')
        assert status==200
        meta=json.loads(raw)
        assert meta['count']==1700 and meta['offlineAudioWords']==1700
        assert meta['microphoneEnabled'] is False
        assert meta['audioMode']=='pocket_offline_only'
        reg=json.loads(request('/api/auth/register',{'nickname':'AudioQA'+uuid.uuid4().hex[:6]})[1])
        # Need registration cookie from response, not application response.
        status,raw,h=request('/api/auth/register',{'nickname':'AudioQB'+uuid.uuid4().hex[:6]})
        assert status==200
        cookie=h.get('Set-Cookie').split(';',1)[0]
        assert cookie.startswith('greek_session=')
        status,raw,_=request('/api/vocab/lesson?topic=all&level=A1&lang=ru',cookie=cookie)
        assert status==200
        words=json.loads(raw)['words']
        assert len(words)==10
        for w in words:
            assert w['wordAudio']['speechText']==w['gr']
            assert w['wordAudio']['audioSource']==('pocket' if w['wordAudio']['audioUrl'] else 'unavailable')
        status,raw,_=request('/api/quiz?scope=chapters&chapters=1,2,3,4&types=accent,syllable&count=60&lang=ru',cookie=cookie)
        assert status==200
        cards=json.loads(raw)['questions']
        assert cards and all(x['kind'] in ('accent','syllable') and x.get('wordAudio') for x in cards)
        assert all(x['wordAudio']['speechText'] for x in cards)
        examples=[q for q in cards if q['wordAudio']['audioUrl']]
        if not examples:
            first=next(w for w in server.vocab.VOCAB if server._word_audio.lookup(w['gr'],server.listening)['audioUrl'])
            examples=[{'wordAudio':server._word_audio.lookup(first['gr'],server.listening)}]
        audio=examples[0]['wordAudio']['audioUrl']
        status,wav,h=request(audio.replace('/greek',''))
        assert status==200 and wav[:4]==b'RIFF' and h['Content-Type']=='audio/wav'
        status,raw,h=request('/greek_word_audio.js')
        assert status==200 and b'getUserMedia' not in raw and b'speechSynthesis' not in raw
        print('PASS REAL HTTP: 1700 A1/A2, 1700 offline Pocket WAV, vocab preview/quiz wordAudio, '
              'accent/syllable wordAudio, local JS GET/HEAD and actual RIFF WAV, no microphone')
    finally:
        proc.terminate()
        try:proc.communicate(timeout=4)
        except subprocess.TimeoutExpired:
            proc.kill();proc.communicate(timeout=4)
