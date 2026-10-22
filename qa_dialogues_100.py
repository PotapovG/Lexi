"""Regression for 100 Greek-only dialogue cards with 1,2,3 gaps and 8 choices."""
import collections
import json
import re
import tempfile
from pathlib import Path

import server
import dialogues
import dialogues_extra
from catalog_v2 import ALL, BY_ID
from textbook_alignment import CHAPTERS as PRINTED_CHAPTERS, LEGACY_TO_PRINTED

cards=[x for x in ALL if x['kind']=='dialogue']
assert len(cards)==100
assert len(set(x['id'] for x in cards))==100
assert {x['id'] for x in cards}==({f'dlg{i:03}' for i in range(1,101)}-{'dlg024'})|{'dlg024_v2'}
assert all(x['id'] in BY_ID for x in cards)
assert len(dialogues.CARDS)==20 and len(dialogues_extra.CARDS)==80
assert 'dlg024' not in {c['id'] for c in cards}
assert server.BY_ID['dlg024']['gaps']==['Χαίρω πολύ','χαίρω πολύ']
assert server.BY_ID['dlg024_v2']['gaps']==['Χαίρω πολύ','Πού μένεις']
assert collections.Counter(len(c['gaps']) for c in cards)=={1:15,2:77,3:8}
for card in cards:
    n=len(card['gaps'])
    assert len(card['bank'])==8 and len(set(card['bank']))==8
    assert len(set(card['gaps']))==n
    assert all(g in card['bank'] for g in card['gaps'])
    # Placeholder enumeration unique, no unmapped/unrendered gap.
    indices=[int(m) for line in card['lines'] for m in re.findall(r'\[\[(\d+)\]\]',line)]
    assert sorted(indices)==list(range(n)),(card['id'],indices)
    assert all(re.search('[\u0370-\u03ff\u1f00-\u1fff]',line) for line in card['lines'])
    assert all(re.search('[\u0370-\u03ff\u1f00-\u1fff]',answer) for answer in card['bank'])
    assert all(len(x)<170 for x in card['bank'])
for chapter in range(1,17):
    expanded=[c for c in dialogues_extra.CARDS if c['legacy_chapter']==chapter]
    assert len(expanded)==5
    for card in expanded:
        actual=next(x for x in PRINTED_CHAPTERS if x['id']==card['chapter'])
        assert actual['start']<=card['page']<=actual['end'],card['id']

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'test.sqlite3')
    server.init_db()
    # Every dialogue's own gap is scored, logged and tracked independently,
    # including new gap2 and 1-gap-only cards.
    for card in cards:
        for lang in ('ru','en','zh','ar','es','pt'):
            for i,expected in enumerate(card['gaps']):
                user='user_'+card['id']+'_'+lang
                assert server.shape(card,f'gap{i}',lang)[1]==expected
                assert server.card_key(card,f'gap{i}',lang)==card['id']+':gap'+str(i)
                reply=server.mark(user,dict(id=card['id'],direction=f'gap{i}',selected=expected,lang=lang))
                assert reply['correct'] and reply['answer']==expected
            try:
                server.mark(user,dict(id=card['id'],direction=f'gap{len(card["gaps"])}',
                                      selected='WRONG',lang=lang))
                raise AssertionError('Could submit invalid gap index')
            except ValueError:pass

    # All 3 shapes are available through the public quiz assembler in six UI
    # languages, with full English-free Greek-only content.
    for card in (cards[20],cards[24],cards[44],cards[58],cards[79],cards[-1]):
        for lang in ('ru','en','zh','ar','es','pt'):
            params=dict(scope=['pages'],study=['textbook'],types=['dialogue'],lang=[lang],
                        **{'from':[str(card['page'])],'to':[str(card['page'])]},count=['60'])
            questions=server.make_quiz('test_parser',params)['questions']
            q=next((x for x in questions if x['id']==card['id']),None)
            assert q,q
            assert q['gapIndices']==list(range(len(card['gaps'])))
            assert q['dialogueGaps']==card['gaps'] and set(q['choices'])==set(card['bank'])
            assert 'choicesEn' not in q and 'promptEn' not in q
    # Failed third gap appears separately in weak-mode; earlier 2 stay correct.
    card=BY_ID['dlg045']
    assert len(card['gaps'])==3
    uid='third_gap_weak'
    for i in (0,1):
        assert server.mark(uid,{'id':card['id'],'direction':f'gap{i}',
                                'selected':card['gaps'][i],'lang':'ru'})['correct']
    assert not server.mark(uid,{'id':card['id'],'direction':'gap2','selected':'WRONG','lang':'ru'})['correct']
    params=dict(scope=['pages'],study=['textbook'],types=['dialogue'],lang=['ru'],
                **{'from':[str(card['page'])],'to':[str(card['page'])]},count=['15'],mode=['weak'])
    q=next(x for x in server.make_quiz(uid,params)['questions'] if x['id']=='dlg045')
    assert q['gapIndices']==[2],q
    assert q['dialogueGaps']==card['gaps']
    assert server.mark(uid,{'id':card['id'],'direction':'gap2','selected':card['gaps'][2],'lang':'ru'})['correct']
    assert server.mark(uid,{'id':card['id'],'direction':'gap2','selected':card['gaps'][2],'lang':'ru'})['correct']
    assert not any(x['id']=='dlg045' for x in server.make_quiz(uid,params)['questions'])
    with server.conn() as db:
        assert db.execute('pragma quick_check').fetchone()[0]=='ok'
        assert db.execute('select count(*) from attempts').fetchone()[0]>=sum(len(x['gaps']) for x in cards)*6
print('PASS 100 Greek-only dialogues, 1/2/3 gaps: 15 / 77 / 8')
print('PASS 80 new dialogues exactly 5 per chapter, in-book page ranges and unique content IDs')
print('PASS all six locales: per-gap answer validation, no accepted invalid direction, unchanged Greek bank')
print('PASS third-gap weak review, independent stats, test SQLite integrity')
