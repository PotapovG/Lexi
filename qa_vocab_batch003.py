"""Batch003 exact Greek 501–750 headword audit and 6-language retained content."""
from pathlib import Path
import json,hashlib,collections
import vocab_lessons as v
import server
report=json.loads(Path('/opt/greek-trainer/editorial-audit/vocab-batch-003-501-750.json').read_text())
assert len(v.VOCAB)==1700 and len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert sum(w['level']=='A1' for w in v.VOCAB)==700
assert sum(w['level']=='A2' for w in v.VOCAB)==1000
assert report['range_first_1indexed']==501 and report['range_last_1indexed']==750
assert report['greek_words_inspected']==250 and report['six_locale_cells_inspected']==1500
assert report['confirmed_field_corrections']==111 and report['distinct_headwords_corrected']==70
assert report['context_flags_count']==24
assert report['native_proofread_certified'] is False
assert len(report['rows'])==250 and len(report['edits'])==111
assert len({r['id'] for r in report['rows']})==250
assert report['frozen_order_sha256']==hashlib.sha256('\n'.join(w['id'] for w in v.VOCAB).encode()).hexdigest()
assert hashlib.sha256(Path(__file__).with_name('vocab_translations_1700.json').read_bytes()).hexdigest()==report['after_atlas_sha256']
assert report['rows'][0]['id']=='vx0004' and report['rows'][-1]['id']=='vx3151'
assert all(w['gr']==row['greek'] and w['id']==row['id']
           for w,row in zip(v.VOCAB[500:750],report['rows']))
for row in report['rows']:
    c=v.VOCAB_BY_ID[row['id']]
    assert row['status'].startswith('AI_FIRST_PASS_')
    for lang in ('ru','en','zh','ar','es','pt'):
        assert row['translations'][lang]==c[lang] and c[lang]
langs=collections.Counter()
for e in report['edits']:
    assert 501<=e['index']<=750
    assert v.VOCAB_BY_ID[e['id']][e['lang']]==e['after']
    assert e['before']!=e['after']
    langs[e['lang']]+=1
assert langs=={'es':35,'zh':33,'pt':23,'ar':20},langs
# Must not confuse English ambiguous sense with original Greek actual meaning:
vocab=v.VOCAB
assert vocab[503]['gr']=='η μπλούζα' and vocab[503]['es']=='la blusa / la camiseta'
assert vocab[503]['pt']=='a blusa / a camisola'
assert vocab[507]['gr']=='η παραγγελία' and vocab[507]['ar']=='الطلب'
assert vocab[534]['gr']=='το φως' and vocab[534]['ar']=='الضوء'
assert vocab[537]['gr']=='η βρύση' and vocab[537]['zh']=='水龙头'
assert vocab[552]['gr']=='το μέλι' and vocab[552]['pt']=='mel'
assert vocab[559]['gr']=='το ορεκτικό' and vocab[559]['es']=='el entrante / el aperitivo'
assert vocab[578]['gr']=='ο πίνακας' and vocab[578]['zh']=='黑板 / 白板'
assert vocab[578]['ar']=='السبورة'
assert vocab[599]['gr']=='το δευτερόλεπτο' and vocab[599]['zh']=='秒'
assert vocab[613]['gr']=='το σύνορο' and vocab[613]['zh']=='边境 / 国界'
assert vocab[618]['gr']=='η παράσταση' and vocab[618]['zh']=='演出 / 表演'
assert vocab[626]['gr']=='το αστέρι' and vocab[626]['zh']=='星星 / 恒星'
assert vocab[634]['gr']=='η άνοιξη' and vocab[634]['ar']=='الربيع'
assert vocab[672]['gr']=='κοντός' and vocab[672]['ar']=='قصير'
assert vocab[680]['gr']=='πότε' and vocab[680]['es']=='cuándo'
assert vocab[696]['gr']=='βάζω' and vocab[696]['es']=='pongo' and vocab[696]['pt']=='ponho / coloco'
assert vocab[711]['gr']=='πετυχαίνω' and vocab[711]['pt']=='consigo / tenho êxito'
assert vocab[737]['gr']=='ο μαθητής' and vocab[737]['zh']=='学生 / 小学生' and vocab[737]['ar']=='تلميذ'
assert vocab[742]['gr']=='η επιχείρηση' and vocab[742]['zh']=='企业 / 公司'
print('PASS batch003 250×6, 111 changes/70 words, exact fixed corpus, 1700/717 intact')
