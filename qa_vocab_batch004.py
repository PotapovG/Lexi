"""Review #004: 250×6 source-target checks, exact values, stable curriculum."""
from pathlib import Path
import json,hashlib,collections
import vocab_lessons as v
import server

report=json.loads(Path('/opt/greek-trainer/editorial-audit/vocab-batch-004-751-1000.json').read_text())
assert report['greek_headwords_inspected']==250 and report['six_locale_cells_inspected']==1500
assert report['range_first_1indexed']==751 and report['range_last_1indexed']==1000
assert report['corrected_translation_fields']==124
assert report['headwords_with_corrections']==75 and report['context_review_flagged_words']==25
assert not report['native_linguist_verified'] and not report['full_1700_first_pass_complete']
assert len(report['rows'])==250 and len(report['edits'])==124
assert len({x['id'] for x in report['rows']})==250
assert len(v.VOCAB)==1700 and len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert sum(x['level']=='A1' for x in v.VOCAB)==700 and sum(x['level']=='A2' for x in v.VOCAB)==1000
assert report['frozen_order_sha256']==hashlib.sha256('\n'.join(x['id'] for x in v.VOCAB).encode()).hexdigest()
assert report['rows'][0]['id']=='vx3152' and report['rows'][-1]['id']=='lexi_23d21ab0e164eeb73370'
assert hashlib.sha256(Path(__file__).with_name('vocab_translations_1700.json').read_bytes()).hexdigest()==report['revised_atlas_sha256']
ctr=collections.Counter()
for w,row in zip(v.VOCAB[750:1000],report['rows']):
    assert w['id']==row['id'] and w['gr']==row['greek']
    assert row['status'].startswith('AI_FIRST_PASS_')
    for lang in ('ru','en','zh','ar','es','pt'):
        assert row['translations'][lang]==w[lang],(w['id'],lang,row['translations'][lang],w[lang])
        assert row['translations'][lang].strip()
for e in report['edits']:
    assert 751<=e['index']<=1000
    assert v.VOCAB_BY_ID[e['id']][e['lang']]==e['after']
    assert e['before']!=e['after']
    ctr[e['lang']]+=1
assert ctr=={'pt':47,'ar':29,'es':30,'zh':18},ctr
assert len({e['id'] for e in report['edits']})==75
w=v.VOCAB
assert w[772]['gr']=='η πατάτα τηγανητή' and w[772]['pt']=='batatas fritas'
assert w[778]['gr']=='ο συγγενής' and 'parente' in w[778]['pt']
assert w[783]['gr']=='η πρωτεύουσα' and w[783]['zh']=='首都' and w[783]['ar']=='العاصمة'
assert w[804]['gr']=='το τελωνείο' and w[804]['es']=='la aduana' and w[804]['pt']=='a alfândega'
assert w[809]['gr']=='το τρέξιμο' and w[809]['ar']=='الجري'
assert w[833]['gr']=='αρέσω' and 'agradar' in w[833]['pt']
assert w[837]['gr']=='ρωτώ' and w[837]['pt']=='pergunto'
assert w[841]['gr']=='μπαίνω' and '进入' in w[841]['zh']
assert w[853]['gr']=='φτιάχνω' and '制作' in w[853]['zh']
assert w[857]['gr']=='κοιτάζω' and w[857]['es']=='miro'
assert w[861]['gr']=='κλαίω' and w[861]['ar']=='أبكي'
assert w[892]['gr']=='η πιπεριά' and w[892]['zh']=='甜椒 / 辣椒'
assert w[902]['gr']=='το τηλεχειριστήριο' and w[902]['zh']=='遥控器'
assert w[913]['gr']=='ο κάδος' and 'سلة' in w[913]['ar']
assert w[920]['gr']=='το κουτί' and 'صندوق' in w[920]['ar']
assert w[938]['gr']=='η αεροσυνοδός' and 'comissária' in w[938]['pt']
assert w[945]['gr']=='το χάπι' and 'دواء' in w[945]['ar']
assert w[949]['gr']=='η παλάμη' and w[949]['ar']=='راحة اليد'
assert w[960]['gr']=='το νύχι' and w[960]['zh']=='指甲' and w[960]['ar']=='ظفر' and w[960]['pt']=='a unha'
assert w[969]['gr']=='η πεδιάδα' and w[969]['zh']=='平原'
assert w[976]['gr']=='το κλαδί' and w[976]['zh']=='树枝'
assert w[977]['gr']=='ο βράχος' and w[977]['zh']=='岩石 / 大石头'
assert w[997]['gr']=='το τένις' and w[997]['pt']=='ténis'
print('PASS: Batch004 250 inspected, 1500 locale fields, 124 correct edits across 75 words; high-impact mistranslations verified, 1700/717 unchanged')
