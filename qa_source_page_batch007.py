#!/usr/bin/env python3
"""QA provenance batch007 1501–1750, 6 locales, isolated answers and stable identities."""
from pathlib import Path
import tempfile,json,collections
import source_page_batch007 as audit
import server,catalog_v2,greek_variants
D=json.loads(audit.OUT.read_text(encoding='utf-8'))
assert D==audit.build_report(),'Ledger stale vs live app cards'
assert D['scope']=={'start':1501,'end':1750,'reviewed':250,'total':1795}
assert D['counts']=={'dialogue':100,'phrase':23,'sentence':31,'verb':80,'word':16}
assert D['dialogue_gap_counts']=={'1':15,'2':77,'3':8}
assert D['evidence_summary']==dict(authorial_verb_drills=80,authorial_dialogue_cards=100,
   authorial_topic_phrases_sentences=54,visually_attested_book_headwords=14,
   topic_words_unconfirmed=2,publisher_exercises_verified=0,
   sentence_exact_text_layer_hits=0,corrected_headword_page_labels=14)
assert set(catalog_v2.SOURCE_PAGE_BATCH007)==set(audit.VISUAL)
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert len({c['id'] for c in server.ALL})==1795
locales=('ru','en','zh','ar','es','pt')
renders=0; correct_gradings=0
with tempfile.TemporaryDirectory(prefix='greek-batch007-') as temp:
    prior=server.DB
    try:
        server.DB=str(Path(temp)/'learner.sqlite3')
        server.init_db()
        for n,(c,proof) in enumerate(zip(server.ALL[1500:1750],D['items']),1501):
            assert n==proof['index'] and c['id']==proof['id']
            assert c['page']==proof['current_page'] and c['chapter']==proof['chapter']
            assert not proof['publisher_exercise_verified']
            dirs=([f'gap{k}' for k in range(len(c['gaps']))] if c['kind']=='dialogue'
                  else ['conjugate','translate'] if c['kind']=='verb'
                  else ['gr-ru','ru-gr'])
            if c['kind']=='word':
                assert proof['page_source_verified']==bool(c.get('book_page_verified'))
                if c['id'] in audit.VISUAL:
                    assert c['page']==audit.VISUAL[c['id']]
                    assert c['source_alignment']=='owner_pdf_visual_attested_usage'
                else: assert c['id'] in {'patk09_009','patk09_010'} and not c.get('book_page_verified')
            elif c['kind']!='word':
                assert not c.get('book_page_verified')
                assert not proof['page_source_verified']
            for lang in locales:
                for direction in dirs:
                    q=server.format_question(c,direction,lang)
                    renders+=1
                    assert q['id']==c['id'] and q['page']==c['page']
                    assert q['sourcePageVerified']==bool(c.get('book_page_verified',False))
                    if c['kind']=='dialogue':
                        assert q['choices'] and set(q['choices'])==set(c['bank'])
                    else:
                        assert len(q['choices'])==len(set(q['choices']))==8,(c['id'],direction,lang)
                        if c['kind']!='verb':
                            assert q['greekVariants']==greek_variants.variants(c['gr'])
            # Each card marks one correct answer; dialogues grade ALL gaps.
            for direction in ([f'gap{i}' for i in range(len(c['gaps']))] if c['kind']=='dialogue'
                               else ['conjugate','translate'] if c['kind']=='verb'
                               else ['gr-ru','ru-gr']):
                lang='ru' if direction!='translate' else 'en'
                selected=(c['gaps'][int(direction[3:])] if c['kind']=='dialogue'
                          else c['accepted'][0] if c['kind']=='verb' and direction=='conjugate'
                          else server.shape(c,direction,lang)[1])
                answer=server.mark('qa-batch007',dict(id=c['id'],direction=direction,selected=selected,lang=lang))
                correct_gradings+=1
                assert answer['correct'],(c['id'],direction,selected,answer)
        with server.conn() as db:
            assert db.execute('pragma quick_check').fetchone()[0]=='ok'
    finally:
        server.DB=prior
assert renders==sum(6*(len(server.ALL[i]['gaps']) if server.ALL[i]['kind']=='dialogue' else 2)
                    for i in range(1500,1750))
print('PASS BATCH007',len(D['items']),'cards',renders,'six-locale render checks',
      correct_gradings,'isolated graded responses; 14 publisher headword occurrences (NOT exercises),'
      ' 2 unconfirmed words, 54 independent sample phrases/sentences; no user DB operations')
