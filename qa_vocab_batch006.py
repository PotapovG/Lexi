#!/usr/bin/env python3
"""Batch #6 exhaustive scoped QA; run --staged or after publication."""
import hashlib,json,collections,sys
from pathlib import Path
ROOT=Path('/opt/greek-trainer');sys.path.insert(0,str(ROOT))
import vocab_lessons as v
import server
STAGE='--staged' in sys.argv
DIR=ROOT/'editorial-audit'
report=json.loads((DIR/('vocab-batch006-candidate-report.json' if STAGE else 'vocab-batch-006-1251-1500.json')).read_text())
plan=json.loads((DIR/('vocab-batch006-candidate-plan.json' if STAGE else 'vocab-review-plan-v1.json')).read_text())
atlas_path=DIR/'vocab-batch006-candidate-translations.json' if STAGE else ROOT/'vocab_translations_1700.json'
tsv_path=DIR/'vocab-batch006-candidate-curated.tsv' if STAGE else ROOT/'vocab_curated_1700.tsv'
atlas=json.loads(atlas_path.read_text()); text=tsv_path.read_text()
assert len(v.VOCAB)==1700 and len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert sum(w['level']=='A1' for w in v.VOCAB)==700 and sum(w['level']=='A2' for w in v.VOCAB)==1000
assert report['batch_size_words']==250 and report['greek_headwords_inspected']==250 and report['six_locale_cells_inspected']==1500
assert report['range_first_1indexed']==1251 and report['range_last_1indexed']==1500
assert report['corrected_translation_fields']==257 and report['headwords_with_corrections']==123
assert report['corrections_by_language']=={'es':63,'pt':91,'ar':65,'zh':33,'ru':3,'en':2}
assert plan['completed_word_rows']==1500 and plan['completed_localized_cells']==9000
assert plan['corrected_translation_fields']==939 and plan['distinct_words_corrected']==524
assert plan['remaining_word_rows']==200 and plan['next_batch_start']==1501 and plan['next_batch_end']==1700
assert plan['batch_ranges'][5]['status']=='AI_FIRST_PASS_COMPLETE' and plan['batch_ranges'][6]['status']=='PENDING'
assert not report['native_linguist_verified'] and not report['full_1700_first_pass_complete']
assert not plan['native_proofread_completed']
order=[w['id'] for w in v.VOCAB]
assert hashlib.sha256('\n'.join(order).encode()).hexdigest()==report['frozen_order_sha256']==plan['ordered_id_sha256']
assert hashlib.sha256(atlas_path.read_bytes()).hexdigest()==report['revised_atlas_sha256']
assert hashlib.sha256(tsv_path.read_bytes()).hexdigest()==report['revised_curated_tsv_sha256']
assert set(atlas)=={'ar','zh','es','pt'}
assert all(set(atlas[lang])==set(order) for lang in atlas)
assert len(report['rows'])==250 and len(report['edits'])==257
changed=collections.Counter()
seen=set()
for row,w in zip(report['rows'],v.VOCAB[1250:1500]):
    assert row['id']==w['id'] and row['greek']==w['gr'] and row['level']==w['level']
    assert set(row['translations'])=={'ru','en','ar','es','pt','zh'}
    assert all(isinstance(z,str) and z.strip() for z in row['translations'].values())
    assert row['status'].startswith('AI_FIRST_PASS_')
    for lang in ('ar','zh','es','pt'):
        assert atlas[lang][w['id']]==row['translations'][lang],(w['id'],lang)
    if not STAGE:
        for lang in row['translations']:
            assert w[lang]==row['translations'][lang],(w['id'],lang)
for e in report['edits']:
    assert 1251<=e['index']<=1500 and e['id']==order[e['index']-1]
    assert e['lang'] in ('ru','en','ar','zh','es','pt') and e['before']!=e['after']
    assert e['after']==report['rows'][e['index']-1251]['translations'][e['lang']]
    assert (e['id'],e['lang']) not in seen
    seen.add((e['id'],e['lang']))
    changed[e['lang']]+=1
assert dict(changed)==report['corrections_by_language']
def t(i,lang):
    return report['rows'][i-1251]['translations'][lang]
assert t(1281,'es')=='suela' and t(1281,'pt')=='sola'
assert t(1315,'es')=='clavo' and t(1316,'zh')=='给植物浇水'
assert t(1333,'es')=='moho' and t(1338,'ar')=='مكبّر الصوت'
assert t(1361,'es')=='archivo adjunto / anexo'
assert t(1369,'zh')=='接口 / 端口'
assert t(1387,'pt')=='capô'
assert t(1389,'zh')=='停车' and t(1389,'ar')=='أركن السيارة'
assert t(1405,'pt')=='elétrico' and t(1413,'pt')=='embraiagem'
assert t(1414,'ar')=='سيارة إطفاء' and t(1420,'zh')=='罚款' and t(1420,'es')=='multa' and t(1420,'pt')=='multa'
assert t(1442,'pt')=='presidente da câmara municipal'
assert t(1453,'zh')=='牙科诊所'
assert t(1470,'ar')=='شباك الخدمة'
assert t(1474,'en')=='migration' and t(1474,'pt')=='migração'
assert t(1499,'zh')=='机长 / 指挥官'
lookup={}
for line in text.splitlines():
    if not line.strip() or line.startswith('#'):continue
    a=line.split('|',4)
    assert len(a)==5
    lookup[a[2]]=a[3:5]
for idx in (1453,1457,1474):
    w=v.VOCAB[idx-1]
    assert lookup[w['gr']]==[t(idx,'ru'),t(idx,'en')]
if STAGE:
    before=json.loads((ROOT/'vocab_translations_1700.json').read_text())
    expected=collections.defaultdict(set)
    for e in report['edits']:
        if e['lang'] in before:
            expected[e['lang']].add(e['id'])
            assert before[e['lang']][e['id']]==e['before']
    for lang in before:
        actual={wid for wid in before[lang] if before[lang][wid]!=atlas[lang][wid]}
        assert actual==expected[lang],(lang,len(actual),len(expected[lang]))
    old_lines=(ROOT/'vocab_curated_1700.tsv').read_text().splitlines()
    new_lines=text.splitlines()
    assert len(old_lines)==len(new_lines)
    changed_sources={v.VOCAB[int(e['index'])-1]['gr'] for e in report['edits'] if e['lang'] in ('ru','en')}
    actual_source=set()
    for beforeline,afterline in zip(old_lines,new_lines):
        if beforeline!=afterline:
            b=beforeline.split('|',4);a=afterline.split('|',4)
            assert b[:3]==a[:3] and len(a)==5
            actual_source.add(a[2])
    assert changed_sources==actual_source
print('PASS batch006', 'STAGED' if STAGE else 'LIVE','250×6; 257 guarded edits over 123 words; 1700 stable IDs, 717 listening cards, 1795 textbook cards')

