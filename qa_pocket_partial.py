"""Real prepared WAV spot-check while background second-speaker pass continues.
This test *temporarily* enables features in-process with disposable SQLite only,
never in the public app and never writes production student progress.
"""
import tempfile,wave
from pathlib import Path
import server,listening_catalog as listening
assert server.LISTENING_ENABLED is False
cards=server.LISTEN_CARDS
assert len(cards)>=30, len(cards)
voices=set()
for item in cards:
 assert len(item['audioVariants'])==2
 a,b=item['audioVariants'];assert a['voice']!=b['voice']
 for v in (a,b):
  file=listening.AUDIO[v['file']];voices.add(v['voice'])
  with wave.open(str(file),'rb') as audio:
   assert audio.getframerate()==24000 and audio.getnchannels()==1
   assert audio.getnframes()/audio.getframerate()>=.25
assert len(voices)>=5,voices
server.LISTENING_ENABLED=True
with tempfile.TemporaryDirectory() as tmp:
 server.DB=str(Path(tmp)/'qa.db');server.init_db()
 for lang in ('ru','en','zh','ar','es','pt'):
  params={'scope':['listening'],'types':['word,phrase,sentence'],'from':['14'],'to':['289'],'lang':[lang],'count':['60']}
  r=server.make_quiz('q',params);assert r['count']==60
  assert len({x['semanticId'] for x in r['questions']})==60
  assert all(len(q['choices'])==8 and q['audioUrl'].startswith('/greek/audio/') and
             q['audioVoice'] in listening.APPROVED and 'transcript' not in q for q in r['questions'])
  item=cards[0];q=server.format_question(item,'listen',lang,variant_index=0)
  result=server.mark('student-'+lang,{'id':q['id'],'direction':'listen','lang':lang,'selected':item[lang]})
  assert result['correct'] and result['transcript']==item['gr']
  repeat=server.format_question(item,'listen',lang,variant_index=1)
  assert repeat['audioVoice']!=q['audioVoice']
print('PARTIAL REAL AUDIO QA PASSED:',len(cards),'ready cards',len(listening.AUDIO),'real WAV files',len(voices),'speakers')
