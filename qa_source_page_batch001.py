#!/usr/bin/env python3
"""Independent original-textbook source-page audit batch #1, first 250 cards."""
import copy,json,sys,collections
from pathlib import Path
ROOT=Path('/opt/greek-trainer')
sys.path.insert(0,str(ROOT))
import catalog_v2 as cat
import server
import source_page_batch001 as batch
import verified_lesson_pages as visual
stage='--staged' in sys.argv
data=json.loads((ROOT/'editorial-audit/source-page-batch-001-1-250.json').read_text())
rows=data['items']
assert len(rows)==250
assert len({r['id'] for r in rows})==250
assert len(cat.ALL)==1795 and len(cat.BY_ID)==1796
assert len(cat.VERIFIED_LESSON_PAGES)==58
assert data['pdf']['private_owner_copy'] and not data['pdf']['publisher_excerpts_in_report']
assert data['policy']['does_not_assert_first_introduction']
assert data['counts']=={'VISUAL_PREVERIFIED':58,'UNCONFIRMED_OCR_OR_NOT_SOURCE':101,
 'PDF_TEXT_EXACT_IN_UNIT':38,'VISUAL_NEWLY_CONFIRMED':46,'INDEPENDENT_AUTHORED_SENTENCE':7}
assert data['source_evidence_confirmed_count']==142
assert data['not_source_proven_count']==108
assert len(batch.NEW_ATTESTATIONS)==84
byid={c['id']:c for c in cat.ALL}
assert [c['id'] for c in cat.ALL[:250]]==[r['id'] for r in rows]
assert all(r['index']==i for i,r in enumerate(rows,1))
original=copy.deepcopy(cat.ALL)
after=copy.deepcopy(cat.ALL) if stage else cat.ALL
if stage:
    changes=batch.apply(after)
else:
    changes=list(batch.NEW_ATTESTATIONS)
assert len(changes)==84
out={x['id']:x for x in after}
ref={x['id']:x for x in original}
assert [x['id'] for x in after]==[x['id'] for x in original]
for row in rows:
    cid=row['id']; card=out[cid]
    assert card['chapter']==row['chapter'] and card['kind']==row['kind']
    if row['selected_page'] is not None:
        assert card['page']==row['selected_page'],(cid,card['page'],row['selected_page'])
        assert card['book_page_verified'],cid
        if row['source_method']=='VISUAL_PREVERIFIED':
            assert card['source_alignment']=='owner_pdf_worked_example_visual'
        else:
            assert 'owner_pdf_' in card['source_alignment']
    else:
        assert not card.get('book_page_verified'),cid
        assert card['page']==row['before_page']
    assert row['source_method']!='INDEPENDENT_AUTHORED_SENTENCE' or not card.get('book_page_verified')
for id,e in batch.NEW_ATTESTATIONS.items():
    c=out[id]
    assert c['page']==e['page'] and c['book_page_evidence']=='matched_usage_not_first_intro_or_publisher_card'
    stress=out.get('stress_'+id)
    if stress:
        assert stress['page']==c['page'] and not stress['book_page_verified']
# No card contents, IDs, kinds, chapter IDs or evaluation answer keys mutated.
allowed_fields={'page','source_alignment','book_page_verified','book_page_evidence'}
for before in original:
    aftercard=out[before['id']]
    for k in set(before)|set(aftercard):
        if k not in allowed_fields:
            assert before.get(k)==aftercard.get(k),(before['id'],k)
assert len(server.LISTEN_CARDS)==717
# The existing visually verified 58 are strict unchanged original source evidence.
for cid,page in visual.PAGES_BY_ID.items():
    assert out[cid]['page']==page and out[cid]['book_page_verified']
# Manual screenshot regressions: new source visual words in 21/27/43/49.
for cid,page in [('w175',21),('w182',27),('w061',27),('w101',43),('w104',43),('w109',43),('w149',49)]:
    assert out[cid]['page']==page and out[cid]['book_page_verified']
for cid in ('w004','s001','s007'):
    assert not out[cid].get('book_page_verified')
print('PASS','STAGED' if stage else 'LIVE',
      'first 250 cards; 58 previous visual + 46 new visual + 38 exact Greek PDF text = 142 attested; 108 remain approximate, 69 page revisions; IDs/content/progress/audio untouched')

