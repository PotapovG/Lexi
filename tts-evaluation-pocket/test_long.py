"""Human-audition benchmark of Greek Pocket TTS only: no product lessons."""
from pathlib import Path
import json, wave, time, numpy as np, torch
from pocket_tts import TTSModel
ROOT=Path('/work')
OUT=ROOT/'long-tests'; OUT.mkdir(exist_ok=True)
SEGMENTS=[
  'Το πρωί ξυπνάω νωρίς και ανοίγω το παράθυρο.',
  'Στη γειτονιά μου έχει ήλιο και τα παιδιά παίζουν στην αυλή.',
  'Μετά πίνω έναν καφέ και πηγαίνω στο κέντρο της Λευκωσίας.',
  'Στον δρόμο συναντώ τη Μαρία και τη ρωτάω: Πού μένεις; Εκείνη μου απαντάει: Μένω στη Λευκωσία.'
]
variants=[('01_default',.3,1,False),('02_clear_phrases',.3,5,True),('03_lively_phrases',.6,5,True)]
voices=[('athina','Женский, Афина'),('kostas','Мужской, Костас')]
def write(path,a,sr):
 a=np.asarray(a,np.float32).flatten()
 if not np.isfinite(a).all():raise RuntimeError('NaNs in '+str(path))
 a=np.clip(a,-1,1)
 with wave.open(str(path),'wb') as out:
  out.setnchannels(1);out.setsampwidth(2);out.setframerate(sr)
  out.writeframes((a*32767).astype('<i2').tobytes())
 path.chmod(0o644)

torch.set_num_threads(4)
manifest={'source_model':'myned-ai/pocket-tts-greek','license':'CC BY 4.0',
          'text':' '.join(SEGMENTS),'samples':[]}
for voice,descriptor in voices:
 for flavor,temperature,steps,chunked in variants:
  start=time.monotonic()
  print('START',voice,flavor,'t',temperature,'steps',steps,flush=True)
  model=TTSModel.load_model(config=str(ROOT/'model'/'greek-local.yaml'),temp=temperature,sampler_decode_steps=steps)
  voice_state=model.get_state_for_audio_prompt(str(ROOT/'model'/(voice+'.wav')))
  pieces=SEGMENTS if chunked else [' '.join(SEGMENTS)]
  waves=[]
  for i,piece in enumerate(pieces):
   torch.manual_seed(1972+i)
   audio=model.generate_audio(voice_state,piece)
   waves.append(audio.reshape(-1).cpu().numpy())
   if i<len(pieces)-1:waves.append(np.zeros(int(model.sample_rate*.22),dtype=np.float32))
   print('SEGMENT',voice,flavor,i,'s',round(waves[-1].size/model.sample_rate,2),flush=True)
  finished=np.concatenate(waves)
  filename=voice+'_'+flavor+'.wav'
  write(OUT/filename,finished,model.sample_rate)
  manifest['samples'].append(dict(voice=voice,voice_desc=descriptor,variant=flavor,
     filename=filename,temp=temperature,steps=steps,chunked=chunked,
     duration_s=round(finished.size/model.sample_rate,1),time_s=round(time.monotonic()-start,1)))
  (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  print('DONE',filename,manifest['samples'][-1],flush=True)
  del model,voice_state
print('ALL_DONE',flush=True)
