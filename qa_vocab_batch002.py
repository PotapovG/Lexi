"""Batch002 non-overlapping stable-ID and locale review hard gates."""
from pathlib import Path
import json,hashlib,collections
import vocab_lessons as v
import server
REPORT=Path('/opt/greek-trainer/editorial-audit/vocab-batch-002-251-500.json')
report=json.loads(REPORT.read_text())
assert len(v.VOCAB)==1700
assert len([x for x in v.VOCAB if x['level']=='A1'])==700
assert len([x for x in v.VOCAB if x['level']=='A2'])==1000
assert report['range_first_1indexed']==251 and report['range_last_1indexed']==500
assert report['greek_headwords_inspected']==250 and report['six_locale_fields_inspected']==1500
assert report['translation_fields_corrected']==78 and report['headwords_with_corrections']==63
assert len(report['rows'])==250 and len(report['edits'])==78
assert report['context_dependent_flagged']==17
assert not report['full_vocab_1700_native_proofread_complete']
assert len({r['id'] for r in report['rows']})==250
assert report['source_ids_frozen_sha256']==hashlib.sha256('\n'.join(w['id'] for w in v.VOCAB).encode()).hexdigest()
assert all(w['id']==r['id'] and w['gr']==r['greek'] for w,r in zip(v.VOCAB[250:500],report['rows']))
assert report['rows'][0]['id']=='book_528983e0df1e89'
assert report['rows'][-1]['id']=='vx0003'
assert hashlib.sha256(Path(__file__).with_name('vocab_translations_1700.json').read_bytes()).hexdigest()==report['output_translation_atlas_sha256']
for w,r in zip(v.VOCAB[250:500],report['rows']):
    for loc in ('ru','en','zh','ar','es','pt'):
        assert r['translations'][loc]==w[loc] and w[loc],(w['id'],loc)
    assert r['status'].startswith('AI_FIRST_PASS_')
by_lang=collections.Counter()
for e in report['edits']:
    w=v.VOCAB_BY_ID[e['id']]
    assert w['gr']==e['greek']
    assert w[e['lang']]==e['after'] and e['before']!=e['after']
    assert 251<=e['index']<=500
    by_lang[e['lang']]+=1
assert by_lang=={'pt':35,'es':18,'ar':16,'zh':9},by_lang
assert len({e['id'] for e in report['edits']})==63
assert v.VOCAB[265]['gr']=='ο όροφος' and v.VOCAB[265]['ar']=='الطابق'
assert v.VOCAB[283]['gr']=='το τρένο' and v.VOCAB[283]['pt']=='o comboio'
assert v.VOCAB[274]['gr']=='το ψυγείο' and v.VOCAB[274]['pt']=='o frigorífico'
assert v.VOCAB[320]['gr']=='όταν' and v.VOCAB[320]['ar']=='عندما'
assert v.VOCAB[325]['gr']=='θα έρθω' and v.VOCAB[325]['pt']=='eu virei'
assert v.VOCAB[357]['gr']=='συναντάω' and 'encontro-me' in v.VOCAB[357]['pt']
assert v.VOCAB[398]['gr']=='πονάω' and v.VOCAB[398]['es']=='me duele / siento dolor'
assert v.VOCAB[418]['gr']=='συμπληρώνω' and v.VOCAB[418]['ar']=='أملأ'
assert v.VOCAB[426]['gr']=='τα ρέστα' and v.VOCAB[426]['ar']=='الباقي (من النقود)'
assert v.VOCAB[443]['gr']=='η κατσαρόλα' and v.VOCAB[443]['zh']=='炖锅 / 汤锅'
assert v.VOCAB[446]['gr']=='ο νεροχύτης' and v.VOCAB[446]['ar']=='حوض المطبخ'
assert v.VOCAB[447]['gr']=='το πάτωμα' and v.VOCAB[447]['ar']=='أرضية الغرفة'
assert v.VOCAB[464]['gr']=='το δημαρχείο' and v.VOCAB[464]['pt']=='a câmara municipal'
assert v.VOCAB[476]['gr']=='ο μήνας' and '月份' in v.VOCAB[476]['zh']
assert v.VOCAB[489]['gr']=='το βιβλιοπωλείο' and v.VOCAB[489]['ar']=='مكتبة بيع الكتب'
assert v.VOCAB[493]['gr']=='το δέντρο' and v.VOCAB[493]['es']=='el árbol'
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
print('PASS: batch002 250×6 checked, 78 exact revisions (63 headwords), 17 contextual flags, all existing IDs and 717 listening unchanged')
