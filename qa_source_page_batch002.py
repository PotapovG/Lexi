#!/usr/bin/env python3
"""Check batch002 251–500 source page attestations; no author question rewriting."""
import collections,copy,json,sys
from pathlib import Path
ROOT=Path('/opt/greek-trainer')
sys.path.insert(0,str(ROOT))
import catalog_v2 as catalog
import server
import source_page_batch002 as batch
d=json.loads((ROOT/'editorial-audit/source-page-batch-002-251-500.json').read_text())
staged='--staged' in sys.argv
assert len(d['items'])==250 and d['scope']['indices']==[251,500]
assert d['counts']=={'INDEPENDENT_AUTHORED_SENTENCE':26,'INDEPENDENT_AUTHORED_PLURAL':29,
'UNCONFIRMED_OCR_OR_NOT_SOURCE':103,'VISUAL_NEWLY_CONFIRMED':18,'PDF_TEXT_EXACT_IN_UNIT':74}
assert d['confirmed_occurrences']==92 and d['unconfirmed']==158
assert d['page_updates']==74
assert d['pdf']['private_owned_copy'] and d['pdf']['no_excerpt_or_pdf_on_core']
assert len(catalog.ALL)==1795 and len(catalog.BY_ID)==1796
assert len(server.LISTEN_CARDS)==717 and server.LISTENING_ENABLED
assert len(batch.SOURCE_PAGE_ATTESTATIONS)==92
orig=copy.deepcopy(catalog.ALL)
aft=copy.deepcopy(orig) if staged else catalog.ALL
if staged: assert len(batch.apply(aft))==92
by={x['id']:x for x in aft}
prior={x['id']:x for x in orig}
assert [x['id'] for x in catalog.ALL[250:500]]==[x['id'] for x in d['items']]
seen=[]
for k,row in enumerate(d['items'],251):
    assert row['index']==k
    c=by[row['id']]
    assert row['kind']==c['kind'] and row['chapter']==c['chapter']
    if row['attested_page'] is not None:
        assert c['page']==row['attested_page'],(k,c['page'],row['attested_page'])
        assert c['book_page_verified'] and c['source_alignment'].startswith('owner_pdf_')
        seen.append(row['id'])
    else:
        assert c['page']==row['old_page'],row['id']
        assert not c.get('book_page_verified'),row['id']
    assert row['method'] not in ('INDEPENDENT_AUTHORED_SENTENCE','INDEPENDENT_AUTHORED_PLURAL') or not c.get('book_page_verified')
assert len(seen)==92 and set(seen)==set(batch.SOURCE_PAGE_ATTESTATIONS)
# Exercise questions, required answers, points, Greek, chapter, semantic IDs intact.
allowed={'page','source_alignment','book_page_verified','book_page_evidence'}
for x in orig:
    c=by[x['id']]
    for key in set(x)|set(c):
        if key not in allowed:assert x.get(key)==c.get(key),(x['id'],key)
for cid,e in batch.SOURCE_PAGE_ATTESTATIONS.items():
    parent=by[cid]
    assert parent['book_page_evidence']=='surface_form_usage_not_first_introduction_or_publisher_exercise'
    child=by.get('stress_'+cid)
    if child:
        assert child['page']==parent['page']
        assert not child.get('book_page_verified')
assert [by[cid]['page'] for cid in ('x05w002','x06w001','x08w013','x09w001','x11w004')]==[68,87,104,132,170]
assert all(not by[cid].get('book_page_verified') for cid in ['s008','n001','x05s001','x09s001'])
if not staged:
    for cid in list(batch.SOURCE_PAGE_ATTESTATIONS)[:12]:
        c=catalog.BY_ID[cid]
        q=server.format_question(c,'gr-ru','ru')
        assert q['sourcePageVerified'] and q['page']==c['page']
print('PASS',('STAGED' if staged else 'LIVE'),'batch002 250 inspected, 92 source-attested (18 visual, 74 text), 158 unconfirmed, 74 page adjustments; 1795 cards, IDs/answers, 717 listening unchanged')

