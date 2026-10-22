"""One-time, restartable offline Greek Pocket TTS synthesis for textbook listening.

Two different preset speakers per distinct Greek source (clear and lively).
No real-time inference, paid APIs, teacher voices, microphone, or legacy Piper.
Manifests only include generated, validated WAVs. Publishing to the student
app happens in a separate explicit reviewed deployment.
"""
import hashlib, json, os, sys, time, wave, re
from pathlib import Path
import numpy as np
import torch
from pocket_tts import TTSModel
from voice_roster import VOICE_IDS,STYLE_PRESETS

ROOT=Path('/app')            # mounted read/write project root
POCKET=ROOT/'tts-evaluation-pocket'
OUT=ROOT/'pocket-listening'
WAV=OUT/'wav';WAV.mkdir(parents=True,exist_ok=True)
MANIFEST=OUT/'manifest.json'
CORPUS=OUT/'source.json'
texts=json.loads(CORPUS.read_text(encoding='utf-8'))
assert len(VOICE_IDS)==6
assert texts['engine']=='myned-ai/pocket-tts-greek'
assert len(texts['items'])>500
entries=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {
    'engine':texts['engine'],'approvedVoices':list(VOICE_IDS),'styles':list(STYLE_PRESETS),'entries':{}
}
assert entries['engine']==texts['engine']
assert entries['approvedVoices']==list(VOICE_IDS)
torch.set_num_threads(4)

def digest(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
def speaker_pair(text):
    raw=int(digest(text)[:8],16)
    first=raw%6
    second=(first+1+(raw//6)%5)%6
    assert first!=second
    return VOICE_IDS[first],VOICE_IDS[second]

def filename(text,voice,style):
    return digest('pocket-tts-greek-v1\n'+voice+'\n'+style+'\n'+text)[:32]+'.wav'

def verified(path):
    try:
        with wave.open(str(path),'rb') as f:
            if not(f.getnchannels()==1 and f.getsampwidth()==2 and f.getframerate()==24000):return False
            if f.getnframes()<f.getframerate()*.25 or f.getnframes()>f.getframerate()*120:return False
        return True
    except (OSError,wave.Error):return False

def split_sentences(text):
    # Greek question mark is ';'. Keep punctuation with phrase for natural ending.
    units=re.findall(r'[^.!;?]+[.!;?]*',text,flags=re.UNICODE)
    units=[s.strip() for s in units if s.strip()]
    return units or [text]

def save_manifest():
    stage=MANIFEST.with_suffix('.json.tmp')
    stage.write_text(json.dumps(entries,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    os.replace(stage,MANIFEST)
    MANIFEST.chmod(0o644)

start=time.monotonic();completed=0;new=0
# Keep a variant for each word in BOTH styles with two DIFFERENT preset speakers.
for stylename,settings in STYLE_PRESETS.items():
    print('LOADING_STYLE',stylename,flush=True)
    model=TTSModel.load_model(config=str(POCKET/'model'/'greek-local.yaml'),
          temp=settings['temperature'],sampler_decode_steps=settings['sampler_decode_steps'])
    speaker_states={voice:model.get_state_for_audio_prompt(str(POCKET/'model'/(voice+'.wav'))) for voice in VOICE_IDS}
    for raw in texts['items']:
        text=raw['text']
        voice1,voice2=speaker_pair(text)
        voice=voice1 if stylename=='clear' else voice2
        fn=filename(text,voice,stylename);path=WAV/fn
        tid=digest(text)[:32]
        if path.exists() and not verified(path):path.unlink()
        if not path.exists():
            pieces=split_sentences(text)
            outputs=[]
            for i,piece in enumerate(pieces):
                torch.manual_seed(int(digest(voice+stylename+text+str(i))[:8],16))
                audio=model.generate_audio(speaker_states[voice],piece).reshape(-1).cpu().numpy()
                if not np.isfinite(audio).all() or audio.size<3000:
                    raise RuntimeError(f'invalid generated data: {tid} {voice} {stylename}')
                outputs.append(audio)
                if i+1<len(pieces):
                    outputs.append(np.zeros(int(model.sample_rate*.22),dtype=np.float32))
            combined=np.concatenate(outputs)
            tmp=WAV/('.'+fn+'.tmp')
            with wave.open(str(tmp),'wb') as f:
                f.setnchannels(1);f.setsampwidth(2);f.setframerate(model.sample_rate)
                f.writeframes((np.clip(combined,-1,1)*32767).astype('<i2').tobytes())
            os.replace(tmp,path);path.chmod(0o644)
            assert verified(path)
            new+=1
        d=entries['entries'].setdefault(tid,{'text':text,'variants':{}})
        assert d['text']==text
        d['variants'][stylename]={'voice':voice,'file':fn}
        completed+=1
        if completed%15==0:
            save_manifest()
            print('COMPLETED',completed,'/',len(texts['items'])*2,'new',new,'elapsed',round(time.monotonic()-start,1),'s',flush=True)
    save_manifest()
    del speaker_states,model
    print('STYLE_DONE',stylename,completed,'/',len(texts['items'])*2,flush=True)
save_manifest()
print('ALL_COMPLETE',completed,'new',new,'texts',len(texts['items']),'elapsed_s',round(time.monotonic()-start,1),flush=True)
