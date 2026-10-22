#!/usr/bin/env python3
"""Regression for batch #5 all 250 derived accent cards and six locale renderings.

Mark() is exercised with an isolated temporary SQLite, never user progress.
"""
import json, tempfile
from pathlib import Path
import catalog_v2 as catalog
import server, greek_variants
from source_page_batch005 import build_report, OUT
expected = json.loads(OUT.read_text(encoding='utf-8'))
actual = build_report()
assert expected == actual, 'Provenance snapshot differs from current catalog/previous ledgers'
assert actual['scope'] == dict(start_index=1001,end_index=1250,total_catalog=1795,reviewed_count=250)
assert len(actual['items']) == 250
assert actual['counts'] == {
 'ARTICLE_STRIPPED_FROM_PARENT':133,
 'DERIVED_ACCENT_PARENT_ATTESTED':137,
 'DERIVED_ACCENT_PARENT_UNCONFIRMED':113}
assert actual['parent_evidence_methods'] == {
 'PDF_TEXT_EXACT_IN_UNIT':103,
 'UNCONFIRMED_OCR_OR_NOT_SOURCE':113,
 'VISUAL_NEWLY_CONFIRMED':34}
assert actual['verified_publisher_exercises'] == 0
assert actual['metadata_page_changes'] == actual['new_source_word_attestations'] == 0
assert not actual['release']['restart_required']
assert len(catalog.ALL) == 1795 and len(server.LISTEN_CARDS) == 717
assert len(set(c['id'] for c in catalog.ALL)) == 1795
locales = ('ru','en','zh','ar','es','pt')
for i, (c,row) in enumerate(zip(server.ALL[1000:1250],actual['items']), 1001):
    p=server.BY_ID[row['parent_card_id']]
    assert row['index']==i and row['id']==c['id']
    assert row['greek_form']==c['accented'] and row['parent_page']==p['page']
    assert c['semanticId']==p['semanticId'] and c['page']==p['page']
    assert not c.get('book_page_verified') and not row['source_page_verified']
    assert row['publisher_exercise_verified'] is False
    assert row['parent_source_page_verified']==bool(p.get('book_page_verified'))
    assert catalog._accent_parts(p['gr'])==(c['base'],c['accented'],c['accent_index'])
    for lang in locales:
        q=server.format_question(c,'accent',lang)
        assert q['kind']=='accent' and q['page']==p['page'] and not q['sourcePageVerified']
        assert q['greekVariants']==greek_variants.variants(c['accented'])
        assert c['accent_index'] in q['accentableIndices']
        assert len(q['letters'])==len(c['base']) and q['letters']==list(c['base'])
        assert q['semanticId']==p['semanticId']
with tempfile.TemporaryDirectory(prefix='greek-batch005-') as td:
    original_db = server.DB
    try:
        server.DB=str(Path(td)/'progress.sqlite3')
        server.init_db()
        for i,c in enumerate(server.ALL[1000:1250]):
            lang=locales[i % len(locales)]
            answer=server.mark('batch005-isolated',dict(
                id=c['id'],direction='accent',lang=lang,
                selected=str(c['accent_index'])))
            assert answer['correct'] and answer['correctIndex']==c['accent_index']
        with server.conn() as db:
            n=db.execute("SELECT COUNT(*) FROM progress WHERE user_id='batch005-isolated'").fetchone()[0]
            assert n==250,n
    finally:
        server.DB=original_db
print('PASS BATCH005: 250/250 accent-parent lineage; 137 parent source attestations, '
      '113 parent pages unproven; 1500/1500 localized renders; '
      '250 isolated SQLite correct-answer grade checks; '
      '0 publisher exercises/page edits; 1795 cards + 717 audio preserved')
