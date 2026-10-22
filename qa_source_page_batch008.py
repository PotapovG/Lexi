#!/usr/bin/env python3
"""Regression batch008 all 45 app-authored cards over 6 languages and isolated SQLite."""
import collections,json,tempfile
from pathlib import Path
import server
import form_exercises
import source_page_batch008 as b8

snapshot=json.loads(b8.OUT.read_text(encoding='utf-8'))
assert snapshot==b8.build_report(),'Audit ledger drift from live cards'
assert snapshot['scope']==dict(start_index=1751,end_index=1795,catalog_total=1795,reviewed=45)
assert snapshot['counts']=={'article':24,'order':17,'phrase':2,'sentence':2}
assert snapshot['evidence_summary']['accepted_article_orthography_variants']==5
assert snapshot['evidence_summary']['linked_parent_sentences']==17
assert snapshot['evidence_summary']['verified_original_publisher_exercises']==0
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
languages=('ru','en','zh','ar','es','pt')
renders=grades=alternatives=negatives=0
with tempfile.TemporaryDirectory(prefix='batch008-') as tmp:
    original=server.DB
    try:
        server.DB=str(Path(tmp)/'progress.sqlite3')
        server.init_db()
        for card,ref in zip(server.ALL[1750:1795],snapshot['items']):
            assert card['id']==ref['id'] and not card.get('book_page_verified')
            dirs=(['fill'] if card['kind']=='article' else
                  ['arrange'] if card['kind']=='order' else
                  ['gr-ru','ru-gr'])
            for lang in languages:
                for direction in dirs:
                    question=server.format_question(card,direction,lang)
                    assert question['id']==card['id'] and not question['sourcePageVerified']
                    assert question['page']==card['page']
                    if card['kind']=='article':
                        assert set(question['choices'])==set(card['options'])
                        answer=card['correct']
                    elif card['kind']=='order':
                        assert collections.Counter(question['tokens'])==collections.Counter(card['tokens'])
                        assert ' '.join(card['tokens'])==card['gr']
                        answer=card['gr']
                    else:
                        assert len(question['choices'])==len(set(question['choices']))==8
                        answer=server.shape(card,direction,lang)[1]
                        assert answer in question['choices']
                    renders+=1
                    result=server.mark('batch008-test',dict(id=card['id'],direction=direction,lang=lang,selected=answer))
                    assert result['correct'],(card['id'],direction,lang,answer,result)
                    grades+=1
                    if card['kind']=='article' and len(card['acceptedForms'])==2:
                        alt=card['acceptedForms'][1]
                        answer_alt=server.mark('batch008-test',dict(id=card['id'],direction=direction,lang=lang,selected=alt))
                        assert answer_alt['correct'] and alt in answer_alt['acceptedAnswers'],(card['id'],lang)
                        alternatives+=1
                    if card['kind'] in ('article','order'):
                        wrong=next(x for x in card['options'] if x not in card['acceptedForms']) if card['kind']=='article' else 'NOT_THE_GREEK_SENTENCE'
                        result=server.mark('batch008-test',dict(id=card['id'],direction=direction,lang=lang,selected=wrong))
                        assert not result['correct'],(card['id'],lang,wrong)
                        negatives+=1
        with server.conn() as db:
            assert db.execute('pragma quick_check').fetchone()[0]=='ok'
    finally:
        server.DB=original
assert (renders,grades,alternatives,negatives)==(294,294,30,246),(renders,grades,alternatives,negatives)
print('PASS BATCH008',len(snapshot['items']),'items:',renders,'localized renders,',
      grades,'correct answers,',alternatives,'valid final-n alternates,',
      negatives,'rejected wrong answers; all tests isolated, publisher exercise claims=0')
