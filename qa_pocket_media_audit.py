"""Production preflight: all 633 Greek texts rendered by 2 distinct licensed Pocket voices.

Voice timbre/prosody are learner-audition-approved. Numerical checks catch
truncations/silent/corrupt files but are NOT a phonetics assessment.
"""
import wave,hashlib,json,math,array,collections
from pathlib import Path
base=Path('/opt/greek-trainer/pocket-listening')
manifest=json.loads((base/'manifest.json').read_text())
source=json.loads((base/'source.json').read_text())
voices=('athina','eleni','katerina','kostas','spyros','nikos')
assert manifest['engine']=='myned-ai/pocket-tts-greek'
assert tuple(manifest['approvedVoices'])==voices
assert len(source['items'])==633
assert len(source['eligibleSourceIds'])==717
assert len(manifest['entries'])==633
assert {x['text'] for x in source['items']}=={x['text'] for x in manifest['entries'].values()}
counts=collections.Counter();durations=[];filenames=set();bad=[]
for tid,entry in manifest['entries'].items():
 assert hashlib.sha256(entry['text'].encode()).hexdigest()[:32]==tid
 variants=entry['variants']
 assert set(variants)=={'clear','lively'},tid
 assert variants['clear']['voice']!=variants['lively']['voice']
 for style,v in variants.items():
  assert v['voice'] in voices and v['file'] not in filenames,(tid,v)
  filenames.add(v['file'])
  f=base/'wav'/v['file']
  assert f.is_file(),f
  with wave.open(str(f),'rb') as audio:
   assert audio.getframerate()==24000 and audio.getnchannels()==1 and audio.getsampwidth()==2
   duration=audio.getnframes()/24000
   if not (.25<=duration<=120):bad.append((tid,duration))
   # Sample middle 1/3 of a recording to catch large silence / zero PCM.
   audio.setpos(audio.getnframes()//3)
   sample=array.array('h',audio.readframes(min(24000,audio.getnframes()//3)))
   if not sample or max(map(abs,sample))<60:bad.append((tid,'silent-middle'))
  durations.append(duration)
  counts[(style,v['voice'])]+=1
assert not bad,bad[:15]
assert len(filenames)==1266
assert all(sum(n for (style,voice),n in counts.items() if voice==v)>100 for v in voices)
print('PASS 633 texts x 2 voices = 1266 non-silent 24kHz audio; 717 source cards')
print('DISTRIBUTION',dict(counts))
print('DURATION',round(min(durations),2),round(sum(durations)/len(durations),2),round(max(durations),2))
print('ON_DISK_MB',round(sum((base/'wav'/f).stat().st_size for f in filenames)/(1024**2),1))
