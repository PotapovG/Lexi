#!/usr/bin/env python3
"""250-item batch006 provenance and full six-locale grading checks in isolated DB."""
import json,tempfile,collections
from pathlib import Path
import server,catalog_v2,greek_variants
from source_page_batch006 import OUT,build
d=json.loads(OUT.read_text(encoding='utf-8'))
assert d==build(),'Live catalog/source ledger differs from persisted provenance report'
assert d['scope']=={'start_index':1251,'end_index':1500,'total':1795,'reviewed':250}
assert d['counts']=={
 'DERIVED_ACCENT_REVIEW_CLONE_PARENT':130,
 'DERIVED_ACCENT_MAIN_PARENT_ATTESTED':14,
 'DERIVED_ACCENT_MAIN_PARENT_UNCONFIRMED':9,
 'TOPICAL_VOCAB_EXACT_FULL_FORM_TEXT_HIT':18,
 'TOPICAL_VOCAB_LEMMA_ONLY_TEXT_HIT':23,
 'TOPICAL_VOCAB_NO_TEXT_LAYER_HIT':34,
 'INDEPENDENT_CONJUGATION_DRILL':22,
},d['counts']
assert d['metadata_page_changes']==d['verified_publisher_exercises']==0
assert d['source_lexeme_matches']=={'full_article_and_headword':18,'bare_headword_or_full':41,'unmatched_text_layer':34,'verb_lemmas':4}
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert len(set(c['id'] for c in server.ALL))==1795
locale=('ru','en','zh','ar','es','pt')
kind_counts=collections.Counter()
for index,(c,row) in enumerate(zip(server.ALL[1250:1500],d['items']),1251):
    assert row['id']==c['id'] and row['index']==index and row['page']==c['page']
    assert not row['publisher_exercise_verified'] and not row['source_page_verified']
    kind_counts[c['kind']]+=1
    if c['kind']=='accent':
        p=server.BY_ID[row['parent_card_id']]
        assert c['id']=='stress_'+p['id'] and c['page']==p['page']
        assert row['parent_source_page_attested']==bool(p.get('book_page_verified'))
        assert catalog_v2._accent_parts(p['gr'])==(c['base'],c['accented'],c['accent_index'])
        dirs=['accent']
    elif c['kind']=='word':
        assert c['page']==0 and c['chapter']==-8
        assert row['id'] in {f'topic{j:03d}' for j in range(1,76)}
        dirs=['gr-ru','ru-gr']
    else:
        assert c['kind']=='verb' and c['page']==0 and c['chapter']==-9
        assert c['forms'][c['person']] in c['accepted']
        dirs=['conjugate','translate']
    for lang in locale:
        for direction in dirs:
            q=server.format_question(c,direction,lang)
            assert q['id']==c['id'] and q['page']==c['page'] and not q['sourcePageVerified']
            if c['kind']=='accent':
                assert q['letters']==list(c['base'])
                assert c['accent_index'] in q['accentableIndices']
                assert q['greekVariants']==greek_variants.variants(c['accented'])
            else:
                assert len(q['choices'])==8 and len(set(q['choices']))==8,(c['id'],lang,direction,q)
assert kind_counts=={'accent':153,'word':75,'verb':22}
with tempfile.TemporaryDirectory(prefix='greek-batch006-') as tmp:
    prior=server.DB
    try:
        server.DB=str(Path(tmp)/'progress.sqlite3')
        server.init_db()
        for n,c in enumerate(server.ALL[1250:1500]):
            lang=locale[n%len(locale)]
            direction=('accent' if c['kind']=='accent' else 'gr-ru' if c['kind']=='word' else 'conjugate')
            selected=(str(c['accent_index']) if c['kind']=='accent' else c[lang] if c['kind']=='word' else c['forms'][c['person']])
            ans=server.mark('audit-batch006',dict(id=c['id'],lang=lang,direction=direction,selected=selected))
            assert ans['correct'],(c['id'],direction,selected,ans)
        for c in server.ALL[1403:1478]:
            ans=server.mark('audit-batch006',dict(id=c['id'],lang='ru',direction='ru-gr',selected=c['gr']))
            assert ans['correct'],c['id']
        for c in server.ALL[1478:1500]:
            trans=server.shape(c,'translate','en')[1]
            ans=server.mark('audit-batch006',dict(id=c['id'],lang='en',direction='translate',selected=trans))
            assert ans['correct'],(c['id'],trans,ans)
        with server.conn() as db:
            assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
    finally:
        server.DB=prior
print('PASS BATCH006 250/250 lineage/source classification; 2082 localized renders, '
      '347 isolated grading requests, 75 topic OCR evidence rows, 22 conjugations; '
      'no false publisher task attribution, no runtime/database edits')
