"""A1 chapter-6 clock-reading exercise: 12 hours and five-minute increments."""
import collections
import random
import tempfile
from pathlib import Path

import clock_cards
import server

assert server.CLOCK_COUNT == 144
cards=clock_cards.CARDS
assert len({c['id'] for c in cards})==144
assert all(c['kind']=='clock' and c['chapter']==6 and c['page']==74 for c in cards)
assert len({c['gr'] for c in cards})==144
assert clock_cards.expression(8,45)=='Είναι εννέα παρά τέταρτο.'
assert clock_cards.expression(1,30)=='Είναι μία και μισή.'
assert clock_cards.expression(12,55)=='Είναι μία παρά πέντε.'

with tempfile.TemporaryDirectory() as tmp:
    server.DB=str(Path(tmp)/'progress.sqlite3')
    server.init_db()
    for lang in ('ru','en','zh','ar','es','pt'):
        for c in cards:
            q=server.format_question(c,'read',lang)
            assert q['kind']=='clock' and q['direction']=='read'
            assert q['clockHour']==c['hour'] and q['clockMinute']==c['minute']
            assert q['note']==clock_cards.HELP[lang]
            assert q['prompt']=='Τι ώρα είναι;'
            assert len(q['choices'])==len(set(q['choices']))==8 and c['gr'] in q['choices']
            assert 'answer' not in q and 'clockTime' not in q
            assert q['page']==74 and not q['sourcePageVerified']
            marked=server.mark('right_'+lang+c['id'],dict(
                id=c['id'],direction='read',lang=lang,selected=c['gr']))
            assert marked['correct'] and marked['clockTime']==f"{c['hour']:02d}:{c['minute']:02d}"
            assert marked['clockLabel']==clock_cards.AFTER[lang]
            wrong=server.mark('wrong_'+lang+c['id'],dict(
                id=c['id'],direction='read',lang=lang,selected='Είναι εκατό.'))
            assert not wrong['correct'] and wrong['missDebt']==2
        try:
            server.mark('bad',dict(id=cards[0]['id'],direction='gr-ru',lang=lang,selected=cards[0]['gr']))
            raise AssertionError('clock accepted invalid direction')
        except ValueError:pass
    for lang in ('ru','en','zh','ar','es','pt'):
        params=dict(scope=['chapters'],chapters=['6'],types=['clock'],count=['60'],lang=[lang])
        q=server.make_quiz('chapter_'+lang,params)['questions']
        assert len(q)==60 and all(c['kind']=='clock' and c['chapter']==6 for c in q)
        assert len({c['id'] for c in q})==60
        params=dict(scope=['pages'],**{'from':['74'],'to':['74']},types=['clock'],count=['60'],lang=[lang])
        q=server.make_quiz('pages_'+lang,params)['questions']
        assert len(q)==60 and all(c['page']==74 for c in q)
        params=dict(scope=['chapters'],chapters=['5'],types=['clock'],count=['60'],lang=[lang])
        assert not server.make_quiz('too_early_'+lang,params)['questions']
        params=dict(scope=['chapters'],chapters=['6'],types=['clock'],count=['60'],lang=[lang],mode=['weak'])
        q=server.make_quiz('wrong_'+lang+cards[0]['id'],params)['questions']
        assert len(q)==1 and q[0]['id']==cards[0]['id'] and q[0]['direction']=='read'
    with server.conn() as db:
        assert db.execute('pragma quick_check').fetchone()[0]=='ok'

js=Path(__file__).with_name('app.js').read_text()
html=Path(__file__).with_name('index.html').read_text()
assert 'id="clock-face"' in html and 'value="clock" checked' in html
assert 'if(q.kind==="clock")renderClock(q)' in js
assert 'const hourDegrees=((q.clockHour%12)+q.clockMinute/60)*30' in js
assert 'const minute=pos(q.clockMinute*6,77)' in js
assert 'result.clockLabel+": "+result.clockTime' in js
assert 'if((Number(o.kindSchemaVersion)||0)<6)types.add("clock")' in js
print('PASS: chapter 6, clock 144 x six locales, 8 unique choices, scoring + weak review')
print('PASS: old book chapters unaffected, no answers leaked, SVG hands + new-mode settings')
