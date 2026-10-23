"""Source-grounded Patakis progression and genuinely repeat-free sessions.

Documented source snippets verified locally from user's PDF (ABBYY text):
printed p40 -> «Τη λένε Ελένη»; unit 4 pp48–58 -> μιλάω,
ξέρεις τον/την/το; review chapter 5 pp59–65.
No publisher exercises are embedded in this test or code.
"""
from collections import Counter
from pathlib import Path
import tempfile
import re
import random
import catalog_v2 as cat
import pedagogy_rules as pedagogy
import server
import vocab_lessons as vocab

# Authentic grammar milestones and progression; no prematurity in chapters 1–4.
assert pedagogy.GRAMMAR_FIRST_UNIT['plural_nouns']==8
assert pedagogy.GRAMMAR_FIRST_UNIT['aorist_narrative']==12
assert pedagogy.GRAMMAR_FIRST_UNIT['future_tense']==14
assert pedagogy.GRAMMAR_FIRST_UNIT['subjunctive_na']==16
assert all(card['curriculum_ready_unit']<=card['chapter'] for card in cat.ALL
           if 'curriculum_ready_unit' in card and card['chapter']>0)
for card in cat.ALL:
    if card['kind'] not in ('dialogue','phrase','sentence'):continue
    if card['chapter'] in (1,2,3,4):
        gr=card['gr']
        assert not re.search(r'\b(?:θα|ήρθες|ήμουν|χθες|να|γράφεται|μαθαίνω|μαθαίνεις)\b',gr,re.I),(card['id'],gr)
assert cat.BY_ID['dlg023']['chapter']>=12
assert cat.BY_ID['dlg040']['chapter']>=16
assert cat.BY_ID['dlg039']['chapter']>=6
assert cat.BY_ID['dlg005']['chapter']==11
assert cat.BY_ID['dlg027']['chapter']==3
# Verify source-supported punctuation/terminal nu fix without breaking
# historical sha-based word identity in the standalone A1/A2 mode.
assert cat.BY_ID['w034']['gr']=='τη λένε'
assert vocab.VOCAB_BY_ID['book_d37c2e558c331d']['gr']=='τη λένε'
assert len(vocab.VOCAB)==1700
assert all(card['semanticId'].startswith('lex_') for card in cat.ALL if card.get('curriculum') not in ('topic','verb'))

params={'scope':['chapters'],'chapters':['1,2,3,4,5'],
        'types':['word,number,phrase,sentence,dialogue,accent'],
        'count':['60'],'lang':['ru'],'mode':['all']}
with tempfile.TemporaryDirectory() as tmp:
    server.DB=str(Path(tmp)/'qa.sqlite3')
    server.auth.SECRET_FILE=Path(tmp)/'login-pepper'
    server.init_db()
    seen=set()
    for page in range(4):
        batch=server.make_quiz('user',dict(params,exclude=[','.join(seen)]))
        assert len(batch['questions'])==60,(page,len(batch['questions']))
        ids=[q['semanticId'] for q in batch['questions']]
        assert len(ids)==len(set(ids)),('duplicate meaning inside API batch',page)
        assert not (seen & set(ids)),('duplicate across batches',page)
        seen.update(ids)
        assert all(q['chapter'] in (1,2,3,4,5) for q in batch['questions'])
    print('PASS 240 cards from first five printed units without repeating semantic headwords across four API batches')
    # Even reverse translation or different question kind must exclude the same
    # canonical Greek target. Weak mode must still offer exact due directions.
    first=server.BY_ID['w049']
    id=first['semanticId']
    assert not any(q['semanticId']==id for q in server.make_quiz('user',dict(params,exclude=[id]))['questions'])
    bad=server.mark('user',{'id':'w049','direction':'ru-gr','selected':'INCORRECT','lang':'ru'})
    assert not bad['correct'] and bad['missDebt']==2
    weak=server.make_quiz('user',{'scope':['chapters'],'chapters':['1,2,3,4,5'],
                                  'types':['word'],'count':['60'],'lang':['ru'],'mode':['weak']})
    q=next(x for x in weak['questions'] if x['id']=='w049')
    assert q['direction']=='ru-gr'
    assert q['semanticId']==id
    for i in range(2):
        resp=server.mark('user',{'id':'w049','direction':'ru-gr','selected':server.shape(first,'ru-gr','ru')[1],'lang':'ru'})
        assert resp['correct'] and resp['missDebt']==1-i
    assert server.stats('user')['weak']==0
    # Choices must be distinct across all 6 UI languages, with English hint
    # metadata separate from answers, including new stage-specific edits.
    for lang in ('ru','en','zh','ar','es','pt'):
        for k in ('w034','w049','w137','patk03_001','patk04_006'):
            card=server.BY_ID[k]
            for direction in ('gr-ru','ru-gr'):
                q=server.format_question(card,direction,lang)
                assert len(q['choices'])==len(set(q['choices']))==8,(k,lang)
                assert server.shape(card,direction,lang)[1] in q['choices']
    with server.conn() as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS semantic exclusion survives translation direction, exact weak debt unchanged, answer options unique in all six locales')
print('PASS all early-grammar readiness requirements and original PDF τη λένε correction with historical course ID preserved')
