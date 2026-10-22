#!/usr/bin/env python3
"""Textbook source-page occurrence provenance QA, original card indices 501–750."""
import json,sys,copy,collections
from pathlib import Path
ROOT=Path('/opt/greek-trainer')
sys.path.insert(0,str(ROOT))
import catalog_v2 as cat
import server
import source_page_batch003 as b3
import source_page_batch001 as b1
import source_page_batch002 as b2
D=json.loads((ROOT/'editorial-audit/source-page-batch-003-501-750.json').read_text())
STAGED='--staged' in sys.argv
assert D['scope']=={'range_start':501,'range_end':750,'full_catalog':1795,'reviewed':250}
assert len(D['items'])==250 and [i['index'] for i in D['items']]==list(range(501,751))
assert len({i['id'] for i in D['items']})==250
assert D['pdf_pages_parsed']==134
assert D['counts']=={
 'INDEPENDENT_AUTHORED_SENTENCE':11,
  'UNCONFIRMED_OCR_OR_NOT_SOURCE':76,
  'PDF_TEXT_EXACT_IN_UNIT':41,
 'VISUAL_NEWLY_CONFIRMED':32,
 'INDEPENDENT_AUTHORED_PLURAL':34,
 'REVIEW_CLONE_INDEPENDENT':56}
assert D['attested_count']==73 and D['unconfirmed_count']==177 and D['page_updates']==61
assert len(b3.SOURCE_PAGE_ATTESTATIONS)==73
assert set(b3.SOURCE_PAGE_ATTESTATIONS)=={x['id'] for x in D['items'] if x['attested_page'] is not None}
assert D['evidence_policy']['exact_form_not_first_introduction']
assert D['evidence_policy']['independently_authored_not_attributed_to_publisher']
assert len(cat.ALL)==1795 and len(cat.BY_ID)==1796 and len(server.LISTEN_CARDS)==717
assert len(cat.VERIFIED_LESSON_PAGES)==58
assert [x['id'] for x in cat.ALL[500:750]]==[x['id'] for x in D['items']]
assert not (set(b3.SOURCE_PAGE_ATTESTATIONS)&set(b2.SOURCE_PAGE_ATTESTATIONS))
assert not (set(b3.SOURCE_PAGE_ATTESTATIONS)&set(b1.NEW_ATTESTATIONS))
original=copy.deepcopy(cat.ALL)
after=copy.deepcopy(cat.ALL) if STAGED else cat.ALL
if STAGED:assert len(b3.apply(after))==73
indexed={c['id']:c for c in after}
for r in D['items']:
 c=indexed[r['id']]
 assert c['chapter']==r['chapter'] and c['kind']==r['kind'],r['id']
 assert c.get('source')==r['source'],r['id']
 if r['attested_page'] is None:
  assert not c.get('book_page_verified'),(r['id'],'unverified should not be green')
  assert c['page']==r['before_page'],(r['id'],c['page'],r['before_page'])
 else:
  assert c['page']==r['attested_page'],(r['id'],c['page'],r['attested_page'])
  assert c.get('book_page_verified') is True,r['id']
  assert c['source_alignment']==('owner_pdf_visual_attested_usage' if r['source_method']=='VISUAL_NEWLY_CONFIRMED' else 'owner_pdf_text_exact_attested_usage')
  assert c['book_page_evidence']=='surface_form_usage_not_first_intro_or_publisher_exercise'
for x in D['items']:
 assert x['source_method'] not in ('REVIEW_CLONE_INDEPENDENT','INDEPENDENT_AUTHORED_PLURAL','INDEPENDENT_AUTHORED_SENTENCE') or x['attested_page'] is None
for id,e in b3.SOURCE_PAGE_ATTESTATIONS.items():
 c=indexed[id]
 child=indexed.get('stress_'+id)
 if child:
  assert child['page']==c['page'] and not child.get('book_page_verified'),id
# No Greek, answer, stable IDs, chapters, localization, question ordering or scoring changes.
ALLOWED={'page','source_alignment','book_page_verified','book_page_evidence'}
for a in original:
 b=indexed[a['id']]
 for k in set(a)|set(b):
  if k not in ALLOWED:assert a.get(k)==b.get(k),(a['id'],k)
# Visually inspected printed p9 alphabet and selected source text/caption pages.
assert len([x for x in D['items'] if x['kind']=='letter' and x['attested_page']==9])==24
for cid,page in [('a000',9),('a023',9),('x13w001',213),('x15w011',249),('x15w014',249),('x15w015',249),('x16w010',263),('x16w011',263)]:
 assert indexed[cid]['page']==page and indexed[cid].get('book_page_verified'),(cid,page)
for cid in ('x12s001','xn14002','v2_001','v1_000'):
 assert not indexed[cid].get('book_page_verified'),cid
assert len(server.LISTEN_CARDS)==717
assert len(cat.ALL)==1795
if not STAGED:
 for cid in list(b3.SOURCE_PAGE_ATTESTATIONS)[:8]:
  c=indexed[cid]
  direction='gr-ru'
  formatted=server.format_question(c,direction,'ru')
  assert formatted['page']==c['page'] and formatted['sourcePageVerified']
print('PASS', 'STAGED' if STAGED else 'LIVE', 'batch003 250 reviewed, 73 attested (32 visual, 41 Greek text) 177 unconfirmed, 61 page updates; 1795 card identities/answers & 717 audio preserved')

