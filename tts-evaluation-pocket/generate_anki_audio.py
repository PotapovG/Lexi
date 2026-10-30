#!/usr/bin/env python3
"""Bounded offline Pocket Greek pronunciation build, one approved voice.

Safe to rerun. A manifest entry is committed only after a RIFF PCM file
has passed format/duration/energy checks. Never touches listening WAV,
historic cards, students or the production SQLite.
"""
import argparse,hashlib,json,math,os,tempfile,time,wave
from pathlib import Path
import numpy as np
import torch
from pocket_tts import TTSModel
from voice_roster import VOICE_IDS,STYLE_PRESETS
import sys
sys.path.insert(0,'/app')
import vocab_lessons,advanced_syllables,listening_catalog,catalog_v2,enclitic_stress

ROOT=Path('/app')
OUT=ROOT/'pocket-pronunciation'
WAV=OUT/'wav'
MANIFEST=OUT/'manifest.json'
WAV.mkdir(parents=True,exist_ok=True)
text_hash=lambda t:hashlib.sha256(t.encode('utf-8')).hexdigest()[:32]

def checked(path):
    try:
        with wave.open(str(path),'rb') as f:
            if f.getnchannels()!=1 or f.getsampwidth()!=2 or f.getframerate()!=24000:return False
            frames=f.getnframes()
            if not 4800<=frames<=24000*30:return False
            # Audio should not be silent: inspect a few samples.
            raw=f.readframes(min(frames,24000))
            signal=np.frombuffer(raw,dtype='<i2')
            return float(np.sqrt(np.mean(signal.astype(np.float32)**2)))>120
    except (OSError,wave.Error):
        return False

def save_manifest(entries):
    temp=MANIFEST.with_suffix('.json.tmp')
    temp.write_text(json.dumps({'engine':'myned-ai/pocket-tts-greek','entries':entries},ensure_ascii=False,separators=(',',':'))+'\n')
    os.replace(temp,MANIFEST)
    os.chmod(MANIFEST,0o644)

parser=argparse.ArgumentParser()
parser.add_argument('--max-words',type=int,default=100)
parser.add_argument('--syllables-only',action='store_true')
parser.add_argument('--accents-only',action='store_true')
parser.add_argument('--enclitics-only',action='store_true')
parser.add_argument('--anki-only',action='store_true',help='Generate missing audio in 30-card Anki curriculum order')
parser.add_argument('--list-only',action='store_true',help='Show missing Anki words without generating')
args=parser.parse_args()
assert 0<=args.max_words<=1700
data=json.loads(MANIFEST.read_text())
assert data['engine']=='myned-ai/pocket-tts-greek'
entries=data['entries']
def ready(text):
    key=text_hash(text);item=entries.get(key)
    prior=listening_catalog.MANIFEST['entries'].get(key)
    legacy_ok=bool(prior and prior.get('text')==text and any(
        (listening_catalog.DIR/variant.get('file','')).is_file()
        for variant in prior.get('variants',{}).values()))
    return bool((item and item['text']==text and checked(WAV/item['file'])) or legacy_ok)
targets=[]
if args.anki_only:
    import study_tracks
    for word in study_tracks.WORDS:
        greek=word['gr']
        if not ready(greek) and greek not in targets:
            targets.append(greek)
        if len(targets)>=args.max_words:break
elif args.enclitics_only:
    for item in enclitic_stress.CARDS:
        greek=item['correct']
        if not ready(greek) and greek not in targets:
            targets.append(greek)
        if len(targets)>=args.max_words:break
elif args.accents_only:
    # Accent exercises print the accented lexeme, not necessarily the
    # article-prefixed expression in A1/A2. Only exact audio can be used.
    accent_words=[c['accented'] for c in catalog_v2.ALL if c['kind']=='accent']
    for greek in accent_words:
        if not ready(greek) and greek not in targets:
            targets.append(greek)
        if len(targets)>=args.max_words:break
else:
    for c in advanced_syllables.CARDS:
        if not ready(c['gr']) and c['gr'] not in targets:targets.append(c['gr'])
    if not args.syllables_only:
        missing=[w['gr'] for w in vocab_lessons.VOCAB if not ready(w['gr']) and w['gr'] not in targets]
        targets.extend(missing[:args.max_words])
print('TARGETS',len(targets),'Syllable missing',sum(not ready(c['gr']) for c in advanced_syllables.CARDS),'A1A2 candidates',args.max_words,flush=True)
if args.list_only:
    print('MISSING_ANKI',len(targets),'first',targets[:30],flush=True)
    raise SystemExit(0)
if not targets:
    print('ALL_READY',flush=True);raise SystemExit(0)
torch.set_num_threads(4)
model=TTSModel.load_model(config=str(ROOT/'tts-evaluation-pocket/model/greek-local.yaml'),temp=.3,sampler_decode_steps=5)
speaker={}
for voice in ('athina','eleni','katerina','kostas','spyros','nikos'):
    speaker[voice]=model.get_state_for_audio_prompt(str(ROOT/'tts-evaluation-pocket/model'/(voice+'.wav')))
start=time.monotonic();created=0;errors=[]
for i,text in enumerate(targets,1):
    if ready(text):continue
    voice=VOICE_IDS[int(text_hash(text)[:8],16)%len(VOICE_IDS)]
    filename=hashlib.sha256(('pocket-greek-pronunciation-v1\n'+voice+'\n'+text).encode()).hexdigest()[:32]+'.wav'
    target=WAV/filename
    try:
        if not checked(target):
            torch.manual_seed(int(text_hash(voice+text)[:8],16))
            array=model.generate_audio(speaker[voice],text).reshape(-1).cpu().numpy()
            if array.size<24000*.2 or not np.isfinite(array).all():
                raise ValueError('invalid synthesis array')
            fd,tmp=tempfile.mkstemp(prefix='.pron-',suffix='.wav',dir=WAV)
            os.close(fd)
            try:
                with wave.open(tmp,'wb') as f:
                    f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000)
                    f.writeframes((np.clip(array,-1,1)*32767).astype('<i2').tobytes())
                if not checked(Path(tmp)):raise ValueError('invalid WAV content')
                os.replace(tmp,target);target.chmod(0o644)
            finally:
                if os.path.exists(tmp):os.unlink(tmp)
        entries[text_hash(text)]={'text':text,'file':filename,'voice':voice}
        created+=1
        if i%12==0:
            save_manifest(entries)
            print('AUDIO',i,'/',len(targets),'new',created,'elapsed',round(time.monotonic()-start,1),flush=True)
    except Exception as e:
        errors.append((text,type(e).__name__,str(e)[:200]))
        print('ERROR',text,str(e)[:120],flush=True)
save_manifest(entries)
print('DONE',created,'/',len(targets),'errors',len(errors),'elapsed',round(time.monotonic()-start,1),flush=True)
if errors:raise RuntimeError(repr(errors[:8]))
