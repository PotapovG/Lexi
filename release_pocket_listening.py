"""One-shot manual quality-gated release of approved six-speaker offline listening.

Only run when the full generator finished successfully and isolated QA passed.
Roll back changed source on a failed live health check. Never touches progress.
"""
import json,shutil,subprocess,sqlite3,sys,time,urllib.request,urllib.error,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LOG=ROOT/'pocket-listening'
assert (LOG/'exit.code').exists(),'generation still running'
assert (LOG/'exit.code').read_text().strip()=='0','offline generation failed; keep ALPHA disabled'
def checked(cmd):
 print('TEST',cmd,flush=True)
 subprocess.run(cmd,check=True,cwd=ROOT,timeout=95)
for script in ('qa_pocket_media_audit.py','qa_pocket_curriculum.py','qa_stage3.py','qa_pedagogy_upgrade.py'):
 checked([sys.executable,script])
# Preflight catalog with the LIVE feature still paused, before any mutation:
import server
assert not server.LISTENING_ENABLED
assert len(server.LISTEN_CARDS)==717 and len(server.listening.AUDIO)==1266
db=Path('/var/lib/greek-trainer/progress.sqlite3')
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as conn:
 assert conn.execute('PRAGMA quick_check').fetchone()[0]=='ok'
 assert conn.execute("SELECT count(*) FROM attempts WHERE kind='listening'").fetchone()[0]==0

files=('server.py','index.html')
snapshot=LOG/('pre-release-source-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
snapshot.mkdir(parents=True,exist_ok=False)
for file in files:shutil.copy2(ROOT/file,snapshot/file)

def change():
 path=ROOT/'server.py'
 data=path.read_text()
 a='LISTENING_ENABLED=False # enable only after complete offline Pocket cache and QA'
 assert data.count(a)==1
 data=data.replace(a,'LISTENING_ENABLED=True # approved complete six-voice offline audio set')
 path.write_text(data)
 path=ROOT/'index.html';data=path.read_text()
 a='name="scope" value="listening" disabled><span data-i18n="listenAlphaMode">🎧 Аудирование · ALPHA — недоступно'
 b='name="scope" value="listening"><span data-i18n="listenMode">🎧 Аудирование'
 assert data.count(a)==1
 data=data.replace(a,b)
 a='id="listening-release-note" data-i18n="listenAlphaNotice">🎧 Аудирование · ALPHA: аудиотека ещё готовится; пока недоступно.'
 b='id="listening-release-note" data-i18n="listenReleaseNotice">🎧 Аудирование · BETA: шесть греческих голосов Pocket TTS, без платных API.'
 assert data.count(a)==1
 data=data.replace(a,b)
 data=data.replace('/greek/app.js?v=28','/greek/app.js?v=29')
 data=data.replace('/greek/styles.css?v=25','/greek/styles.css?v=26')
 path.write_text(data)

def service_restart():
 subprocess.run(['systemctl','restart','greek-trainer.service'],check=True,timeout=20)

try:
 change()
 checked([sys.executable,'-m','py_compile','server.py'])
 service_restart()
 root='https://potapovfamily.com/greek/'
 for i in range(18):
  try:
   with urllib.request.urlopen(root+'api/catalog',timeout=5) as r:meta=json.load(r)
   if meta['listeningAvailable'] and not meta['listeningAlpha'] and \
      meta['listeningCount']==717 and meta['cardCount']==1795 and \
      len(meta['listeningChapters'])==20 and len(meta['listeningVoices'])==6:
    break
  except Exception:
   pass
  time.sleep(1.2)
 else:raise RuntimeError('new site not live/valid after service restart')
 sample=server.LISTEN_CARDS[0]['audioVariants'][0]['file']
 with urllib.request.urlopen(root+'audio/'+sample,timeout=8) as r:
  assert r.status==200 and r.headers['Content-Type']=='audio/wav'
  assert r.read(4)==b'RIFF'
 print('RELEASE_SUCCESS: Pocket listening enabled. Six voices, 717 cards, 1266 WAV, 20 printed units.',flush=True)
except Exception as err:
 print('RELEASE_FAILED_ROLLING_BACK',repr(err),flush=True)
 for file in files:shutil.copy2(snapshot/file,ROOT/file)
 service_restart()
 raise
