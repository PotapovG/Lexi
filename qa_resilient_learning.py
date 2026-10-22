#!/usr/bin/env python3
"""Atomic dedup, concurrent retries, alternative order, extra 6-locale corpus.

All scoring/database effects use disposable isolated SQLite.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import collections,tempfile,uuid
import server
import order_valid_permutations as order_rules
import extra_sentences_20261021 as extra
import answer_idempotency as dedup

assert len(server.ALL)==1795
assert len(server.EXTRA_ALL)==26 and len(extra.CARDS)==18 and len(extra.ORDER_CARDS)==8
assert len(server.LISTEN_CARDS)==717
assert len({x['id'] for x in server.PRACTICE_ALL})==1978
assert order_rules.validate({**server.BY_ID,**server.ORDER2_BY_ID})==33
assert all(c['source'].startswith('independent_') and not c.get('book_page_verified')
           for c in server.EXTRA_ALL)
for c in server.EXTRA_ALL:
    for lang in ('ru','en','zh','ar','es','pt'):
        assert isinstance(c[lang],str) and len(c[lang])>=3,(c['id'],lang)
        dirs=['arrange'] if c['kind']=='order' else ['gr-ru','ru-gr']
        for direction in dirs:
            q=server.format_question(c,direction,lang)
            assert q['id']==c['id'] and not q['sourcePageVerified']
            assert q['chapter']==c['chapter']
            if c['kind']=='order':assert sorted(q['tokens'])==sorted(c['tokens'])
            else:assert len(q['choices'])==8 and len(set(q['choices']))==8

with tempfile.TemporaryDirectory(prefix='lexi-answer-once-') as temp:
    old=server.DB
    server.DB=str(Path(temp)/'practice.sqlite3')
    try:
        server.init_db()
        c=server.BY_ID['article_001']
        direction='fill'
        first={'id':c['id'],'direction':direction,'lang':'ru','selected':c['correct'],
               'srsOptIn':True,'requestId':str(uuid.uuid4())}
        a=dedup.score_once(server.conn,server.mark,'student1',first)
        replay=dedup.score_once(server.conn,server.mark,'student1',first)
        assert a==replay and a['correct']
        with server.conn() as db:
            assert db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]==1
            assert db.execute('SELECT COUNT(*) FROM answer_receipts').fetchone()[0]==1
            assert db.execute('SELECT COUNT(*) FROM srs_schedule').fetchone()[0]==1
            assert db.execute('SELECT attempts FROM progress').fetchone()[0]==1
        altered=dict(first,selected='wrong')
        try:dedup.score_once(server.conn,server.mark,'student1',altered)
        except ValueError as e:assert 'reused' in str(e)
        else:raise AssertionError('conflicting replay accepted')
        # Same request id is scoped by signed-in account.
        second=dedup.score_once(server.conn,server.mark,'student2',first)
        assert second==a
        concurrent=dict(first,id='article_002',selected=server.BY_ID['article_002']['correct'],
                        requestId=str(uuid.uuid4()),srsOptIn=False)
        with ThreadPoolExecutor(max_workers=10) as pool:
            results=list(pool.map(lambda _:dedup.score_once(server.conn,server.mark,'student1',concurrent),range(25)))
        assert all(r==results[0] for r in results)
        with server.conn() as db:
            assert db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]==3
            assert db.execute('SELECT COUNT(*) FROM answer_receipts').fetchone()[0]==3
            assert db.execute('SELECT COUNT(*) FROM srs_schedule').fetchone()[0]==2
            assert db.execute('SELECT SUM(attempts) FROM progress').fetchone()[0]==3
        # Legacy clients remain compatible (no replay token needed).
        legacy=server.mark('student3',{'id':c['id'],'direction':'fill','lang':'ru','selected':c['correct']})
        assert legacy['correct']
        with server.conn() as db:
            assert db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]==4
            assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
        # Validate old selected alternatives without converting every Greek anagram to a right answer.
        for cid,variants in order_rules.VARIANTS.items():
            card=server.book_or_audio_card(cid)
            for v in variants:
                result=server.mark('order_student',{'id':cid,'direction':'arrange','lang':'ru','selected':v})
                assert result['correct'],(cid,v,result)
                assert result['acceptedOrderCount']>=2
            assert not server.mark('order_student',{'id':cid,'direction':'arrange','lang':'ru',
                    'selected':'γεια σας Καλημέρα πόλη'})['correct']
        # New independent material appears with old scope filters, but not before its unit.
        scoped=server.make_quiz('new_student',{'types':['sentence'],'chapters':['18'],'mode':['all'],'count':['60'],'lang':['ru']})
        ids={q['id'] for q in scoped['questions']}
        assert any(x.startswith('sx261021_') for x in ids)
        assert not any(x.startswith('sx261021_001') for x in ids)
        new=extra.CARDS[0]
        ans=server.mark('new_student',{'id':new['id'],'direction':'gr-ru','lang':'en','selected':new['en']})
        assert ans['correct']
        new_order=extra.ORDER_CARDS[0]
        ans=server.mark('new_student',{'id':new_order['id'],'direction':'arrange','lang':'ru','selected':new_order['gr']})
        assert ans['correct']
        # Source corpus and 8 ledgers stable, no reindex or user migration.
        assert len(server.ALL)==1795 and len(server.BY_ID)==1796
    finally:
        server.DB=old
print('PASS RESILIENCE: atomic replay, concurrent same-ID dedup, conflict rejection,'
      ' cross-account isolation, SRS only-once, 14 curated order variants,'
      ' 18 authored sentences + 8 new order exercises, 6 languages and unchanged original 1795')
