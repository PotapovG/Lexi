#!/usr/bin/env python3
"""Complete 7-batch 1,700-word source/target and production scope QA. --staged for candidate."""
import collections,hashlib,json,sys
from pathlib import Path
ROOT=Path('/opt/greek-trainer');DIR=ROOT/'editorial-audit';sys.path.insert(0,str(ROOT))
import vocab_lessons as v
import server
STAGED='--staged' in sys.argv
p=lambda x:json.loads(x.read_text())
last=p(DIR/('vocab-batch007-candidate-report.json' if STAGED else 'vocab-batch-007-1501-1700.json'))
plan=p(DIR/('vocab-batch007-candidate-plan.json' if STAGED else 'vocab-review-plan-v1.json'))
atlas_file=DIR/'vocab-batch007-candidate-translations.json' if STAGED else ROOT/'vocab_translations_1700.json'
tsv_file=DIR/'vocab-batch007-candidate-curated.tsv' if STAGED else ROOT/'vocab_curated_1700.tsv'
atlas=p(atlas_file)
ids=[w['id'] for w in v.VOCAB]
assert len(ids)==1700 and len(set(ids))==1700
assert plan['ordered_id_sha256']==hashlib.sha256('\n'.join(ids).encode()).hexdigest()==last['frozen_order_sha256']
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert sum(w['level']=='A1' for w in v.VOCAB)==700
assert sum(w['level']=='A2' for w in v.VOCAB)==1000
assert len(set(w['gr'] for w in v.VOCAB))==1700
assert set(atlas)=={'ar','zh','es','pt'}
assert all(set(atlas[l])==set(ids) for l in atlas)
assert hashlib.sha256(atlas_file.read_bytes()).hexdigest()==last['revised_atlas_sha256']
assert hashlib.sha256(tsv_file.read_bytes()).hexdigest()==last['revised_curated_tsv_sha256']
assert plan['completed_word_rows']==1700 and plan['completed_localized_cells']==10200
assert plan['corrected_translation_fields']==1120 and plan['distinct_words_corrected']==609
assert plan['remaining_word_rows']==0 and plan['next_batch_start'] is None
assert plan['full_1700_first_pass_complete'] and not plan['native_proofread_completed']
assert len(plan['completed_batch_reports'])==7 and len(set(plan['completed_batch_reports']))==7
assert all(x['status']=='AI_FIRST_PASS_COMPLETE' for x in plan['batch_ranges'])
assert [x['number'] for x in plan['batch_ranges']]==list(range(1,8))
assert len(last['rows'])==200 and len(last['edits'])==181
assert last['greek_headwords_inspected']==200 and last['six_locale_cells_inspected']==1200
assert last['range_first_1indexed']==1501 and last['range_last_1indexed']==1700
assert last['corrected_translation_fields']==181 and last['headwords_with_corrections']==85
assert last['corrections_by_language']=={'ar':51,'pt':52,'zh':34,'es':44}
assert last['full_1700_first_pass_complete'] and not last['native_linguist_verified']
expected_langs={'ru','en','ar','zh','es','pt'}
allidx=[];allrows=[];alledits=[];counts=collections.Counter()
for n,filename in enumerate(plan['completed_batch_reports'],1):
    r=last if n==7 else p(DIR/filename)
    i0,i1=r['range_first_1indexed'],r['range_last_1indexed']
    expected_low=1+(n-1)*250
    expected_high=min(n*250,1700)
    assert (i0,i1)==(expected_low,expected_high),(n,i0,i1)
    assert len(r['rows'])==i1-i0+1
    assert len(r['edits'])>0
    for row in r['rows']:
        ix=row['index'];w=v.VOCAB[ix-1]
        assert i0<=ix<=i1 and row['id']==w['id'] and row['greek']==w['gr']
        assert set(row['translations'])==expected_langs,(n,ix,set(row['translations']))
        assert all(isinstance(s,str) and s.strip() for s in row['translations'].values())
        assert row['status'].startswith('AI_FIRST_PASS_')
        for lang in ('ar','zh','es','pt'):
            assert atlas[lang][row['id']]==row['translations'][lang],(n,ix,lang,atlas[lang][row['id']],row['translations'][lang])
        if n<7 or not STAGED:
            assert all(row['translations'][lang]==w[lang] for lang in expected_langs),(n,ix,'source differs')
        else:
            assert all(row['translations'][lang]==w[lang] for lang in ('ru','en'))
        allidx.append(ix);allrows.append(row)
    for edit in r['edits']:
        ix=edit['index'];lang=edit['lang'];wid=edit['id']
        assert i0<=ix<=i1 and wid==ids[ix-1]
        assert lang in expected_langs and edit['before']!=edit['after']
        assert r['rows'][ix-i0]['translations'][lang]==edit['after']
        alledits.append((wid,lang))
        counts[lang]+=1
assert len(allidx)==1700 and allidx==list(range(1,1701))
assert len(alledits)==1120 and len(set(alledits))==1120
assert len({wid for wid,_ in alledits})==609
assert sum(counts.values())==1120
for w in v.VOCAB:
    for lang in ('ar','zh','es','pt'):
        assert w[lang]==atlas[lang][w['id']] or STAGED and w['id'] in {x['id'] for x in last['edits'] if x['lang']==lang}
# Source.tsv exact-scope: final batch must not edit any source RU/EN.
if STAGED:
    assert (ROOT/'vocab_curated_1700.tsv').read_bytes()==tsv_file.read_bytes()
    old=p(ROOT/'vocab_translations_1700.json')
    changes=collections.defaultdict(set)
    for edit in last['edits']:
        assert edit['lang'] in old
        assert old[edit['lang']][edit['id']]==edit['before']
        changes[edit['lang']].add(edit['id'])
    for lang in old:
        actual={wid for wid in old[lang] if old[lang][wid]!=atlas[lang][wid]}
        assert actual==changes[lang],(lang,len(actual),len(changes[lang]))
# Critical false friend regression checks on the published candidate.
def at(ix,lang):
    return allrows[ix-1]['translations'][lang]
assert at(1512,'zh')=='风俗习惯' and at(1512,'ar')=='العادات والتقاليد'
assert at(1532,'es')=='red' and at(1531,'ar')=='راقص'
assert at(1562,'ar')=='رزمة أوراق اللعب'
assert at(1574,'ar')=='يرقة فراشة'
assert at(1586,'zh')=='海豹' and at(1586,'ar')=='فقمة' and at(1586,'es')=='foca' and at(1586,'pt')=='foca'
assert at(1591,'zh')=='泉水 / 源头' and at(1611,'zh')=='水流 / 电流'
assert at(1611,'ar')=='تيار مائي / تيار كهربائي'
assert at(1623,'pt')=='respiração' and at(1628,'es')=='toso'
assert at(1649,'zh')=='治疗' and at(1655,'ar')=='أعطي دواءً'
assert at(1670,'ar')=='للتوّ / بمجرّد أن'
assert at(1695,'es')=='espera'
print('PASS', 'STAGED' if STAGED else 'LIVE','7/7 batches, 1700 words, 10200 locale cells, 1120 per-field audited edits, 609 affected words; stable IDs, source Greek, 717 listening and 1795 book cards')
print('BY LANGUAGE',dict(counts))

