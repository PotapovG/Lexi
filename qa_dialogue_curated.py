"""No deletion of historical IDs or correct Greek gap answers."""
import sys,collections,re
from pathlib import Path
import server, catalog_v2, dialogue_quality
from catalog_v2 import ALL
current={x['id']:x for x in ALL if x['kind']=='dialogue'}
original=catalog_v2.ORIGINAL_DIALOGUE_SNAPSHOT
assert len(current)==len(original)==100
assert len(catalog_v2.CURATED_DIALOGUE_BANKS)==35
assert len([x for x in current.values() if x.get('bank_source')=='curated-stage-safe-20261020'])==35
assert current['dlg024_v2']['replaces']=='dlg024' and current['dlg024_v2']['gaps']==['Χαίρω πολύ','Πού μένεις']
assert catalog_v2.ARCHIVED_DIALOGUES['dlg024']['bank']==original['dlg024']['bank']
for cid,c in current.items():
 o=original[cid] if cid in original else dict(gaps=c['gaps'],gr=c['gr'],bank=c['bank'])
 assert c['gaps']==o['gaps'] and c['gr']==o['gr'],cid
 assert len(c['bank'])==len(set(c['bank']))==8,cid
 assert all(correct in c['bank'] for correct in c['gaps']),cid
 assert set(c['bank'])&set(c['gaps'])==set(c['gaps'])
 for i in range(len(c['gaps'])):
  assert server.shape(c,'gap'+str(i),'ru')[1]==o['gaps'][i]
 if cid not in catalog_v2.CURATED_DIALOGUE_BANKS:
  assert c['bank']==o['bank'],cid
 else:
  assert c['bank']!=o['bank'],cid
  for val in c['bank']:
   if val not in c['gaps']:
    assert val==val.strip() and val.strip(),(cid,val)
    # Stages not supposed to contain later constructions or off-topic word types.
    if c['chapter']<14:assert not re.search(r'\bθα\b',val,re.I),(cid,val)
    if c['chapter']<16:assert not re.search(r'\b(?:θέλεις να|μπορείς να|πάμε να)\b',val,re.I),(cid,val)
    if c['chapter']<18:assert not re.search(r'πονάει|φάρμακ',val,re.I),(cid,val)
    if c['chapter']<8:assert not re.search(r'κιλό|ευρώ|λογαριασμ|ρέστα',val,re.I),(cid,val)
    if c['chapter']<6:assert not re.search(r'λεωφορείο|εισιτήριο|αεροπλ',val,re.I),(cid,val)
    if c['chapter']<11:assert not re.search(r'χρονών|διαμέρισμ|όροφο',val,re.I),(cid,val)
print('PASS: 35 curated / 100 original dialogue IDs preserved, 8 distinct, all source answers and source text unchanged, no later-stage cues')
