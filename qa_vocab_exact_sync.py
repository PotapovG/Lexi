"""Linked textbook/independent glossary consistency for only 17 reviewed forms."""
import json
from pathlib import Path
import catalog_v2 as c, vocab_lessons as v,server,editorial_localization as review
atlas=json.loads(Path(__file__).with_name('vocab_translations_1700.json').read_text())
changed=[]
by={w['gr']:w for w in v.VOCAB}
for (cid,lang),(before,after,why) in review.REVIEWED.items():
    card=c.BY_ID[cid]
    if card['kind']!='word' or lang not in ('es','pt','zh','ar') or card['gr'] not in by:continue
    w=by[card['gr']]
    assert atlas[lang][w['id']]==after,(cid,lang,w['id'])
    assert w[lang]==after,(cid,lang,w['id'],w[lang],after)
    assert server.BY_ID[cid][lang]==after,(cid,lang,server.BY_ID[cid][lang],after)
    assert w['source']=='book_aligned_original' and w['id'].startswith('book_')
    changed.append((cid,lang,w['id']))
assert len(changed)==17,len(changed)
assert len({(lang,wid) for _,lang,wid in changed})==17
assert len(v.VOCAB)==1700 and len(server.ALL)==1795
print('PASS 17 exact linked vocabulary glosses synced across 1700-word independent A1/A2 and book curriculum; word IDs stable')
