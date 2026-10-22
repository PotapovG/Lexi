"""Audio audition on isolated word/phrase/sentence for each approved Pocket profile.

No access to live quiz/DB. A synthetic sample is not proof of Greek clarity.
"""
import sys,math,wave,json
from pathlib import Path
import numpy as np
import torch
from pocket_tts import TTSModel
from voice_roster import VOICE_IDS,STYLE_PRESETS
R=Path('/work');O=R/'short-tests';O.mkdir(exist_ok=True)
UTTERANCES={
 'word':'ελεύθερη',
 'phrase':'Η μητέρα μου είναι δασκάλα.',
 'sentence':'Ο φίλος μου έχει δύο παιδιά, έναν γιο και μία κόρη.',
}

def save(path,data,rate):
 a=np.asarray(data,np.float32).flatten()
 assert len(a)>rate*.28 and np.isfinite(a).all()
 with wave.open(str(path),'wb') as wav:
  wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
  wav.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
 path.chmod(0o644)

torch.set_num_threads(4)
manifest={'model':'myned-ai/pocket-tts-greek','voices':VOICE_IDS,'samples':[],
 'all_original_audio_alpha_disabled':True,'texts':UTTERANCES}
for voice_id in VOICE_IDS:
 for style,settings in STYLE_PRESETS.items():
  model=TTSModel.load_model(config=str(R/'model'/'greek-local.yaml'),
    temp=settings['temperature'],sampler_decode_steps=settings['sampler_decode_steps'])
  voice=model.get_state_for_audio_prompt(str(R/'model'/(voice_id+'.wav')))
  for idx,(kind,text) in enumerate(UTTERANCES.items()):
   torch.manual_seed(2345+idx)
   audio=model.generate_audio(voice,text).reshape(-1).cpu().numpy()
   name=f'{voice_id}_{style}_{kind}.wav'
   save(O/name,audio,model.sample_rate)
   duration=round(len(audio)/model.sample_rate,2)
   manifest['samples'].append({'voice':voice_id,'style':style,'kind':kind,'file':name,'duration':duration})
   print('SAMPLE',name,'duration',duration,flush=True)
  (O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  del model,voice
print('SAMPLES_DONE',len(manifest['samples']),flush=True)
