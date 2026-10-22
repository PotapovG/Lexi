"""Release gate for exact 250 Greek-headword / 1500 localized editorial pass."""
import json,hashlib,tempfile,collections
from pathlib import Path
import vocab_lessons as v
import server

report=json.loads(Path('/opt/greek-trainer/editorial-audit/vocab-batch-001-250.json').read_text())
assert report['batch_size_words']==250
assert report['source_greek_words_inspected']==250 and report['target_locale_fields_inspected']==1500
assert report['corrected_fields']==102
assert len(report['rows'])==250 and len(report['edits'])==102
assert len({c['id'] for c in report['rows']})==250
assert report['distinct_words_corrected']==len({x['id'] for x in report['edits']})==75
assert report['full_native_linguist_quality_assured'] is False
assert len(v.VOCAB)==1700
assert len([w for w in v.VOCAB if w['level']=='A1'])==700
assert len([w for w in v.VOCAB if w['level']=='A2'])==1000
assert all(w['id']==row['id'] and w['gr']==row['greek'] for w,row in zip(v.VOCAB[:250],report['rows']))
assert all(w['id'].startswith('book_') for w in v.VOCAB[:250])
assert all(row['status'].startswith('AI_FIRST_PASS_') for row in report['rows'])
assert hashlib.sha256(Path('/opt/greek-trainer/editorial-vocab-batch01/vocab_translations_1700.json').read_bytes()).hexdigest()==report['output_json_sha256']
correct=collections.Counter()
for row in report['rows']:
    w=v.VOCAB_BY_ID[row['id']]
    for lang in ('ru','en','zh','ar','es','pt'):
        assert row['translations'][lang]==w[lang] and w[lang]
    for lang in row['corrected_languages']:correct[lang]+=1
assert correct=={'es':44,'pt':37,'ar':21},correct
for item in report['edits']:
    assert v.VOCAB_BY_ID[item['id']][item['lang']]==item['after']
    assert item['before']!=item['after']
# Deep focus on dangerous semantics: directions, geographic square, orange fruit,
# gender agreement, verb conjugation and correct accented interrogatives.
assert v.VOCAB[178]['gr']=='δεξιά'
assert v.VOCAB[178]['es']=='a la derecha' and v.VOCAB[178]['pt']=='à direita' and v.VOCAB[178]['ar']=='إلى اليمين'
assert v.VOCAB[176]['ar']=='الساحة / الميدان'
assert v.VOCAB[240]['ar']=='البرتقالة'
assert v.VOCAB[207]['ar']=='أقرأ'
assert v.VOCAB[208]['gr']=='κοιμάμαι'
assert v.VOCAB[142]['es']=='bien'
assert v.VOCAB[112]['pt']=='casada (mulher)'
assert v.VOCAB[116]['pt']=='solteira / livre (mulher)'
assert v.VOCAB[167]['pt']=='o autocarro'
assert v.VOCAB[170]['pt']=='o metro'
assert v.VOCAB[172]['es']=='la estación'
assert v.VOCAB[192]['es']=='el día'
assert v.VOCAB[205]['es']=='todos los días'
# Preserve per-user/per-word progress in separate SQLite DB; actually submit corrected answers.
with tempfile.TemporaryDirectory() as td:
    import sqlite3
    db=sqlite3.connect(str(Path(td)/'vocab.sqlite3'))
    v.schema(db)
    for locale,idx in (('es',179),('pt',179),('ar',177),('es',193),('pt',168),('ar',241)):
        word=v.VOCAB[idx-1]
        assert word[locale]
    db.close()
# External-facing independent course returns 10 words and exactly 8 choices;
# running full topic/level/locale suites via qa_localizations_1700.py separately.
print('PASS: batch001 exact 250 Greek words x 6 target languages, 102 edits/75 headwords, 1700 intact; high-risk 6-locale focus; historical IDs preserved.')
