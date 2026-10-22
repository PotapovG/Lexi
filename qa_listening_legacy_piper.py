"""Offline Greek listening: no API, STT or user audio recording."""
import tempfile, wave
from pathlib import Path
import server
assert len(server.ALL)==1795 and len(server.vocab.VOCAB)==1700
assert len(server.LISTEN_CARDS)==717 and len(server.LISTEN_BY_ID)==717
assert len(server.listening.AUDIO)==633
for c in server.LISTEN_CARDS:
 assert c['chapter'] in range(1,21)
 assert c['sourceId'] in server.BY_ID
 assert c['gr']==server.BY_ID[c['sourceId']]['gr']
 assert c['audioFile'] in server.listening.AUDIO
 assert all(c[lang] for lang in ('ru','en','zh','ar','es','pt'))
for fn in list(server.listening.AUDIO)[:30]:
 with wave.open(str(server.listening.AUDIO[fn]),'rb') as f:
  assert f.getframerate()==22050 and f.getnframes()>1200 and f.getnchannels()==1
with tempfile.TemporaryDirectory() as tmp:
 server.DB=str(Path(tmp)/'progress.sqlite3');server.init_db()
 params={'scope':['listening'],'chapters':['1,2,3,4'],'lang':['ru'],'count':['60']}
 seen=set()
 for _ in range(3):
  q=server.make_quiz('student',{**params,'exclude':[','.join(seen)]})['questions']
  assert len(q)==60
  assert all(x['kind']=='listening' and x['direction']=='listen' and x['chapter'] in (1,2,3,4) for x in q)
  assert all('transcript' not in x and 'gr' not in x and x['audioUrl'].startswith('/greek/audio/') for x in q)
  assert all(len(set(x['choices']))==8 for x in q)
  fingerprints={x['semanticId'] for x in q}
  assert not seen.intersection(fingerprints)
  seen|=fingerprints
 assert server.estimate_capacity('student',{**params,'duration':['30']})['uniqueCards']==len({c['semanticId'] for c in server.LISTEN_CARDS if c['chapter'] in (1,2,3,4)})
 for lang in ('ru','en','zh','ar','es','pt'):
  for cid in ('listen_p001','listen_w049','listen_patk03_001'):
   card=server.LISTEN_BY_ID[cid]
   q=server.format_question(card,'listen',lang)
   assert card[lang] in q['choices'] and len(set(q['choices']))==8
   assert 'transcript' not in q and 'gr' not in q
   r=server.mark('user-'+lang,{'id':cid,'direction':'listen','lang':lang,'selected':card[lang]})
   assert r['correct'] and r['transcript']==card['gr'] and r['missDebt']==0
 target=server.LISTEN_BY_ID['listen_p001']
 r=server.mark('weak',{'id':target['id'],'direction':'listen','lang':'ru','selected':'WRONG'})
 assert not r['correct'] and r['missDebt']==2
 due=server.make_quiz('weak',{'mode':['weak_all'],'lang':['ru']})['questions']
 assert len(due)==1 and due[0]['id']==target['id'] and due[0]['audioUrl'].endswith('.wav')
 for debt in (1,0):
  r=server.mark('weak',{'id':target['id'],'direction':'listen','lang':'ru','selected':target['ru']})
  assert r['correct'] and r['missDebt']==debt
 assert server.stats('weak')['weak']==0
 assert server.stats('user-ru')['categories']['listening']['correct']==3
 for chapter in range(1,21):
  q=server.make_quiz('other',{'scope':['listening'],'chapters':[str(chapter)],'lang':['en']})['questions']
  assert all(x['chapter']==chapter for x in q)
 assert not server.listening.has_audio('../voice-model/model.onnx')
 with server.conn() as db: assert db.execute('pragma quick_check').fetchone()[0]=='ok'
print('PASS offline 717-card listening catalog / 633 licensed Greek WAV; original 1795+1700 unchanged')
print('PASS 180 no-repeat cards / 6 language correct meaning / no transcript before grade')
print('PASS weak review, statistics, 20 printed chapter scopes, no unlisted audio access')
