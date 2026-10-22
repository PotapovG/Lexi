"""More Greek sentence construction from existing authorial sentence examples.

Separate stable IDs and source-parent references, preserving original text,
translations and textbook provenance. No new copyrighted passages.
"""
from catalog_v2 import ALL as BASE
from extra_sentences_20261021 import CARDS as EXTRA
import pedagogy_rules

# Explicit independently curated parent selection. All have a complete Greek
# sentence, six translations and a reasonable tap-to-compose token count.
IDS=(
 'x05s001','x05s002','x06s001','x06s002','x07s001','x07s002',
 'x08s001','x08s002','x09s001','x09s002','x10s001','x10s002',
 'x11s001','x11s002','x12s001','x12s002','x13s001','x13s002',
 'x14s001','x14s002','x15s001','x15s002','x16s001','x16s002',
 'sx261021_002','sx261021_005','sx261021_007','sx261021_010',
 'sx261021_011','sx261021_013','sx261021_015','sx261021_016',
 'sx261021_017','sx261021_018',
 'patk12_002','patk12_004','patk14_005','patk18_001',
 'patk18_003','patk16_002'
)


assert len(IDS)==40 and len(set(IDS))==40
def build(books):
    # Called after the server has applied the already-reviewed legacy Arabic
    # localization overrides. Do not fall back to English for Arabic.
    parents={c['id']:c for c in books+EXTRA if c['kind']=='sentence'}
    existing={c['gr'] for c in books+EXTRA if c['kind']=='order'}
    cards=[]
    for cid in IDS:
        c=parents[cid]
        assert c['gr'] not in existing,cid
        assert 6<=len(c['gr'].split())<=16,(cid,c['gr'])
        translated={lang:c[lang] for lang in ('ru','en','zh','ar','es','pt')}
        assert all(translated.values()),cid
        item=dict(id='or261021_'+cid,kind='order',chapter=c['chapter'],unit=c['unit'],
            page=c['page'],gr=c['gr'],tokens=c['gr'].split(),topic=c.get('topic','Σύνταξη'),
            source='derived_authorial_sentence_order_20261021',source_parent_id=cid,
            source_alignment='reviewed_curriculum_stage_not_publisher_quote',
            book_page_verified=False,grammar_tags=list(c.get('grammar_tags',[])),
            **translated)
        pedagogy_rules.tag(item)
        assert item['curriculum_ready_unit']<=max(20,c['chapter'])
        assert item['semanticId']==c['semanticId']
        cards.append(item)
    assert len(cards)==40 and len({x["id"] for x in cards})==40
    return cards
