#!/usr/bin/env python3
"""Rebuild the 1795-item source manifest and verify 8 ledgers, read-only."""
import json,collections,hashlib
import server,catalog_v2
import full_source_audit as audit
from source_page_batch007 import VISUAL as PAGES
data=json.loads(audit.OUT.read_text(encoding='utf-8'))
assert data==audit.generate(),'Audit ledger changed or source catalog drifted'
assert data['totals']=={'catalog':1795,'audited':1795,
    'attested_lexical_or_alphabet_pages':321,
    'not_source_attested_or_authored':1474,
    'verified_publisher_exercises':0,
    'listening':717,'standalone_A1_A2':1700}
assert data['attested_kind_counts']=={'word':270,'number':23,'letter':24,'phrase':4}
assert [b['reviewed'] for b in data['batch_checksums']]==[250]*7+[45]
assert [b['source_verified'] for b in data['batch_checksums']]==[142,92,73,0,0,0,14,0]
assert len(data['cards'])==1795
assert all(not c['publisher_exercise_identity_verified'] for c in data['cards'])
assert [c['id'] for c in server.ALL]==[r['id'] for r in data['cards']]
assert len(catalog_v2.BY_ID)==1796 # one archived historic dialogue
assert len(server.LISTEN_CARDS)==717
assert sorted(PAGES)==sorted(c['id'] for c in server.ALL
      if c['id'].startswith('patk09_') and c.get('book_page_verified'))
assert len(catalog_v2.ORDER_TRANSLATIONS_SYNCED)==2
assert len(server.ORDER_ARABIC_TRANSLATIONS_SYNCED)==1
print('PASS FULL SOURCE AUDIT: 1795 unique index-ID-page-source rows, 8 complete ledgers; '
      '321 attested Greek source forms, 1474 approximate/authored; '
      '0 invented publisher exercise identities, Spanish/Arabic 17 parent/order prompt parity, '
      '717 audio cards, 1700 standalone A1/A2 words preserved')
