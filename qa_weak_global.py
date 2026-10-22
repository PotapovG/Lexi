"""Account-wide weak-review regression for all scopes, languages and stale IDs.

Uses disposable SQLite; deliberately does not read/write live account progress.
"""
import tempfile
import sqlite3
from pathlib import Path
import server

with tempfile.TemporaryDirectory() as root:
    server.DB=str(Path(root)/'review.sqlite3')
    server.init_db()
    uid='review_any_filter'
    examples=[
        ('w158','gr-ru','es'),
        ('w167','gr-ru','es'),
        ('w192','ru-gr','es'),
        ('dlg006','gap0','ru'),
    ]
    for cid,direction,lang in examples:
        word=server.BY_ID[cid]
        correct=server.shape(word,direction,lang)[1]
        wrong='an intentionally invalid multiple-choice answer'
        assert wrong!=correct
        outcome=server.mark(uid,{'id':cid,'direction':direction,'lang':lang,'selected':wrong})
        assert not outcome['correct'] and outcome['missDebt']==2
    assert server.stats(uid)['weak']==4
    # Existing scoped review cannot see these Spanish and dialogue mistakes.
    scoped={'mode':['weak'],'lang':['ru'],'scope':['pages'],'types':['sentence'],
            'from':['300'],'to':['300'],'count':['60']}
    assert server.make_quiz(uid,scoped)['count']==0
    # The new My Mistakes button ignores these filters and sees all 4.
    global_params=dict(scoped,mode=['weak_all'])
    result=server.make_quiz(uid,global_params)
    assert result['count']==result['available']==4,result
    got={(q['id'],q['direction'],q['lang']) for q in result['questions']}
    assert got==set(examples),(got,examples)
    assert all(len(q['choices'])==8 and len(set(q['choices']))==8 for q in result['questions'])
    assert len(next(q for q in result['questions'] if q['id']=='dlg006')['gapIndices'])==1
    assert all(q['choicesEn'] for q in result['questions'] if q['lang']=='es' and q['direction']=='gr-ru')
    # Input of the correct source-language answer must update the same
    # card_key/debt; incorrectly sending display_lang=ru would not.
    for cid,direction,lang in examples:
        card=server.BY_ID[cid]
        answer=server.shape(card,direction,lang)[1]
        key=server.card_key(card,direction,lang)
        before=server.stats(uid)['weak']
        for attempt in range(2):
            reply=server.mark(uid,{'id':cid,'direction':direction,'lang':lang,'selected':answer})
            assert reply['correct'] and reply['missDebt']==1-attempt,(cid,reply)
        assert server.stats(uid)['weak']==before-1
        with server.conn() as db:
            assert db.execute('select miss_debt from progress where user_id=? and card_key=?',(uid,key)).fetchone()[0]==0
    assert server.make_quiz(uid,global_params)['count']==0
    assert server.stats(uid)['weak']==0

    # Old, vanished/corrupted keys stay in SQLite for history but are not
    # advertised as answerable, never deleted or counted as reviewable.
    old='nonexistent_stress_card:accent'
    with server.conn() as db:
        db.execute('insert into progress values(?,?,?,?,?,?)',(uid,old,3,1,2,'2026-10-20'))
    summary=server.stats(uid)
    assert (summary['weak'],summary['weakOverall'],summary['weakUnavailable'])==(0,1,1),summary
    assert server.make_quiz(uid,global_params)['count']==0
    with server.conn() as db:
        assert db.execute('select miss_debt from progress where user_id=? and card_key=?',(uid,old)).fetchone()[0]==2

    # Greek accent and dialogue are language-independent, but their UI
    # stays in the selected locale, without fabricating an English suffix.
    for cid,dir in [('stress_w008','accent'),('dlg025','gap0')]:
        if cid not in server.BY_ID:continue
        card=server.BY_ID[cid]
        with server.conn() as db:
            db.execute('insert into progress values(?,?,?,?,?,?)',
                       (uid,server.card_key(card,dir),1,0,2,'2026-10-20'))
    result=server.make_quiz(uid,{**global_params,'lang':['ar']})
    assert all(q['lang']=='ar' for q in result['questions']),result
    assert server.stats(uid)['weakUnavailable']==1

    # Independent accounts can never obtain another person's overdue cards.
    assert server.make_quiz('someone_else',global_params)['count']==0
    assert server.stats('someone_else')['weak']==0
    with server.conn() as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS: 4 cross-language/course mistakes actionable despite empty current selection')
print('PASS: original per-card answer languages and gap directions preserved, 2 correct reviews clear debt')
print('PASS: stale/missing legacy keys retained but separated from actionable count')
print('PASS: Greek-only directions, per-account isolation and isolated SQLite integrity')
