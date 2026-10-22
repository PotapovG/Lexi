#!/usr/bin/env python3
"""Batch004 full 250 source/provenance ledger QA without inventing publisher matches."""
import collections,json
from pathlib import Path
import server,greek_variants
root=Path('/opt/greek-trainer')
d=json.loads((root/'editorial-audit/source-page-batch-004-751-1000.json').read_text())
assert d['scope']=={'from':751,'to':1000,'total_card_count':1795,'reviewed_count':250}
assert len(d['items'])==250
assert list(range(751,1001))==[x['index'] for x in d['items']]
assert [c['id'] for c in server.ALL[750:1000]]==[x['id'] for x in d['items']]
assert d['counts']=={'INDEPENDENT_REVIEW_CLONE':104,'DERIVED_ACCENT_PARENT_ATTESTED':105,'DERIVED_ACCENT_PARENT_UNCONFIRMED':41}
assert d['metadata_page_changes']==0 and d['verified_publisher_exercises']==0
assert not d['methodology']['publisher_exercise_identity_verified']
seen=collections.Counter()
for c,r in zip(server.ALL[750:1000],d['items']):
    assert c['id']==r['id'] and c['chapter']==r['chapter'] and c['page']==r['current_page'],r['id']
    assert not c.get('book_page_verified') and not r['source_page_verified'],r['id']
    seen[c['kind']]+=1
    if c['kind']=='accent':
        parent=server.BY_ID[r['parent_card_id']]
        assert parent['id']==c['id'][len('stress_'):]
        assert r['parent_page']==c['page']==parent['page']
        assert r['parent_source_page_verified']==bool(parent.get('book_page_verified'))
        assert r['evidence_type']==('DERIVED_ACCENT_PARENT_ATTESTED' if parent.get('book_page_verified') else 'DERIVED_ACCENT_PARENT_UNCONFIRMED')
        q=server.format_question(c,'accent','ru')
        assert q['sourcePageVerified'] is False
        assert q['page']==parent['page']
        # Important: Greek spelling variants on sibling headwords are educational,
        # not a claim the publisher's original accent exercise has been found.
        if greek_variants.variants(c['accented']):
            assert q['greekVariants']==greek_variants.variants(c['accented'])
    else:
        assert r['evidence_type']=='INDEPENDENT_REVIEW_CLONE'
        assert c['source']=='review-original'
        q=server.format_question(c,'gr-ru','ru')
        assert not q['sourcePageVerified'] and q['page']==c['page']
assert seen=={'accent':146,'word':94,'number':4,'phrase':6}
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
print('PASS BATCH004: all 250 cards: 104 independent review clones; 146 accent exercises (105 inherited attested parent word pages, 41 unconfirmed), no false publisher-verified exercise or pages, no metadata changes')

