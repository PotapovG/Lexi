#!/usr/bin/env python3
"""Exact-scope and high-impact QA for lexical editorial batch #5; --staged before publication."""
import sys,json,hashlib,collections
from pathlib import Path
ROOT=Path('/opt/greek-trainer')
sys.path.insert(0,str(ROOT))
import vocab_lessons as v
import server

p=ROOT/'editorial-audit'
report=json.loads((p/('vocab-batch005-candidate-report.json' if '--staged' in sys.argv else 'vocab-batch-005-1001-1250.json')).read_text())
atlas_file=p/'vocab-batch005-candidate-translations.json' if '--staged' in sys.argv else ROOT/'vocab_translations_1700.json'
tsv_file=p/'vocab-batch005-candidate-curated.tsv' if '--staged' in sys.argv else ROOT/'vocab_curated_1700.tsv'
atlas=json.loads(atlas_file.read_text())
tsv=tsv_file.read_text()
plan=json.loads((p/('vocab-batch005-candidate-plan.json' if '--staged' in sys.argv else 'vocab-review-plan-v1.json')).read_text())
assert len(v.VOCAB)==1700 and len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert sum(x['level']=='A1' for x in v.VOCAB)==700 and sum(x['level']=='A2' for x in v.VOCAB)==1000
assert report['range_first_1indexed']==1001 and report['range_last_1indexed']==1250
assert report['greek_headwords_inspected']==250 and report['six_locale_cells_inspected']==1500
assert report['corrected_translation_fields']==267 and report['headwords_with_corrections']==118
assert report['corrections_by_language']=={'pt':86,'zh':41,'ar':75,'es':61,'en':3,'ru':1}
assert not report['native_linguist_verified']
assert plan['completed_word_rows']==1250 and plan['completed_localized_cells']==7500 and plan['corrected_translation_fields']==682
assert plan['distinct_words_corrected']==401 and plan['remaining_word_rows']==450
assert plan['batch_ranges'][4]['status']=='AI_FIRST_PASS_COMPLETE'
assert all(x['status']=='PENDING' for x in plan['batch_ranges'][5:])
assert len(report['rows'])==250 and len(report['edits'])==267
assert [w['id'] for w in v.VOCAB[1000:1250]]==[w['id'] for w in report['rows']]
order='\n'.join(x['id'] for x in v.VOCAB)
assert hashlib.sha256(order.encode()).hexdigest()==plan['ordered_id_sha256']==report['frozen_order_sha256']
assert hashlib.sha256(atlas_file.read_bytes()).hexdigest()==report['revised_atlas_sha256']
assert hashlib.sha256(tsv_file.read_bytes()).hexdigest()==report['revised_curated_tsv_sha256']
assert set(atlas)=={'ar','es','pt','zh'}
ids={w['id'] for w in v.VOCAB}
assert all(set(d)==ids for d in atlas.values())
original=json.loads((ROOT/'vocab_translations_1700.json').read_text()) if '--staged' in sys.argv else None
changed=collections.Counter()
for row,w in zip(report['rows'],v.VOCAB[1000:1250]):
    assert row['greek']==w['gr'] and row['id']==w['id']
    assert all(row['translations'][l].strip() for l in ['ru','en','ar','es','pt','zh'])
    for lang in ['ar','es','pt','zh']:
        assert atlas[lang][w['id']]==row['translations'][lang]
    if '--staged' not in sys.argv:
        assert all(w[l]==row['translations'][l] for l in ['ru','en','ar','es','pt','zh'])
for e in report['edits']:
    assert e['before']!=e['after'] and 1001<=e['index']<=1250
    w=v.VOCAB[e['index']-1]
    assert w['id']==e['id'] and e['greek']==w['gr']
    assert report['rows'][e['index']-1001]['translations'][e['lang']]==e['after']
    changed[e['lang']]+=1
assert dict(changed)==report['corrections_by_language']
# Reference assertions for translation failures that would be missed by structural checks.
def at(n,lang):
    return report['rows'][n-1001]['translations'][lang]
assert at(1195,'ar')=='الديك الرومي' # turkey bird, not country
assert at(1200,'ar')=='أقلي' # fry, not Federal Republic of Yugoslavia
assert at(1238,'zh')=='拉链' # zip fastener, not postcode
assert at(1204,'es')=='rallo' and at(1204,'pt')=='ralo' # grate verb
assert at(1139,'pt')=='simpatizo com alguém' # sympathize, not resemble
assert at(1245,'ar')=='المخزون' and at(1248,'zh')=='利息' # inventory & loan interest
assert at(1206,'pt')=='gorjeta' # restaurant gratuity, not helpful hint
assert at(1224,'zh')=='开瓶器' # opener, not opening remark
assert at(1022,'pt')=='apelido' # surname PT-PT
assert at(1216,'ru')=='мёрзну, мне холодно'
assert at(1056,'en')=='fountain'
assert at(1121,'en')=='unlikely / incredible'
source=dict((v.split('|',4)[2], v.split('|',4)[3:]) for v in tsv.splitlines() if v and not v.startswith('#'))
for ix in [1056,1121,1216]:
    w=v.VOCAB[ix-1]
    assert source[w['gr']]==[report['rows'][ix-1001]['translations'][lang] for lang in ['ru','en']]
if '--staged' in sys.argv:
    # No outside-block changes, and candidate vs production differs only via allowed edits.
    changes_by_lang=collections.defaultdict(set)
    for e in report['edits']:
        if e['lang'] in original:
            changes_by_lang[e['lang']].add(e['id'])
    for lang in atlas:
        assert {wid for wid in ids if atlas[lang][wid]!=original[lang][wid]}==changes_by_lang[lang]
print('PASS batch005 '+('STAGED' if '--staged' in sys.argv else 'LIVE')+': 250×6; 267 guarded changes across 118 headwords; stable IDs, 1700 vocab, 717 listening, 1795 book cards; reviewed critical false-friends')

