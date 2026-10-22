#!/usr/bin/env python3
"""OFFLINE ONLY. Generate hash-named WAV from self-authored Lexi Greek words.

Runs explicitly in a disposable piper-enabled Docker image; no server TTS,
paid API, live request synthesis, speaker/microphone, or publisher material.
Safe to rerun: existing audio files and manifest are never overwritten.
"""
import argparse,hashlib,json,os,tempfile,wave
from pathlib import Path
from catalog_v2 import ALL
from piper import PiperVoice

ROOT=Path(__file__).resolve().parent
VOICE='el_GR-rapunzelina-medium'
VOICEPATH=ROOT/'voice-model'/f'{VOICE}.onnx'
OUT=ROOT/'audio'
MANIFEST=ROOT/'listening_audio_manifest.json'

def filename(text):
 return hashlib.sha256((VOICE+'\n'+text.strip()).encode('utf-8')).hexdigest()[:28]+'.wav'

def prepare(units):
 cards=[c for c in ALL if c['chapter'] in units and c['kind'] in ('word','phrase','sentence')
        and c.get('curriculum') not in ('topic','verb') and c.get('gr','').strip()]
 # PDF exercises are not embedded in the app; existing ones are independent authored content.
 return sorted(cards,key=lambda c:(c['chapter'],c['id']))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--chapters',default='1,2,3,4');parser.add_argument('--limit',type=int,default=0)
 args=parser.parse_args();units={int(s) for s in args.chapters.split(',')}
 cards=prepare(units)
 if args.limit:cards=cards[:args.limit]
 OUT.mkdir(exist_ok=True,parents=True)
 entries=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'voice':VOICE,'items':{}}
 assert entries['voice']==VOICE
 voice=PiperVoice.load(str(VOICEPATH))
 generated=0;errors=[]
 for i,card in enumerate(cards,1):
  fn=filename(card['gr']);target=OUT/fn
  if not target.exists():
   fd,tmp=tempfile.mkstemp(prefix='.wav-',dir=OUT);os.close(fd)
   try:
    with wave.open(tmp,'wb') as f:voice.synthesize_wav(card['gr'],f)
    with wave.open(tmp,'rb') as check:
     assert check.getframerate()==22050 and check.getnframes()>=1200,(card['id'],check.getnframes())
    os.replace(tmp,target);target.chmod(0o644);generated+=1
   except Exception as exc:
    errors.append((card['id'],str(exc)))
    try:os.unlink(tmp)
    except OSError:pass
    continue
  entries['items'][card['id']]=fn
  if i%25==0:print('AUDIO',i,'/',len(cards),'GENERATED',generated,flush=True)
 tmp=MANIFEST.with_suffix('.json.tmp')
 tmp.write_text(json.dumps(entries,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
 tmp.replace(MANIFEST)
 MANIFEST.chmod(0o644)
 print('DONE','new',generated,'total',len(entries['items']),'errors',errors,flush=True)
 if errors:raise SystemExit(1)
