"""Regression for Greek post-answer translations."""
import tempfile
from pathlib import Path

import server
import dialogue_translations as glosses

cards=[c for c in server.ALL if c['kind']=='dialogue']
assert glosses.validate(server.ALL)==100
accent=next(c for c in server.ALL if c['kind']=='accent' and c['gr']=='μιλάνε')

with tempfile.TemporaryDirectory() as folder:
    server.DB=str(Path(folder)/'db.sqlite3')
    server.init_db()
    for lang in ('ru','en','zh','ar','es','pt'):
        assert 'translation' not in server.format_question(accent,'accent',lang)
        for selected in (str(accent['accent_index']),str(accent['accent_index']+1)):
            if int(selected)>=len(accent['base']):continue
            reply=server.mark('accent'+lang+selected,dict(
                id=accent['id'],direction='accent',selected=selected,lang=lang))
            assert reply['translation']==accent[lang]
            assert reply['translationLang']==lang
        for c in cards:
            for i,greek in enumerate(c['gaps']):
                direction='gap'+str(i)
                reply=server.mark(c['id']+lang+str(i),dict(
                    id=c['id'],direction=direction,selected=greek,lang=lang))
                assert reply['correct'] and reply['translation']
                assert reply['translationLang'] in (lang,'en')
                assert '[[' not in str(reply.get('greekVariants',[]))
                wrong=server.mark('wrong'+c['id']+lang+str(i),dict(
                    id=c['id'],direction=direction,selected='wrong',lang=lang))
                assert not wrong['correct']
                assert wrong['translation']==reply['translation']
    assert server.mark('brother',dict(id='dlg035',direction='gap0',
        selected='Έχω έναν αδελφό και μία αδελφή',lang='ru'))['translation']=='У меня один брат и одна сестра'
    assert server.mark('teacher',dict(id='dlg033',direction='gap0',
        selected='Είμαι δασκάλα',lang='ru'))['translation']=='Я учительница'
    with server.conn() as db:
        assert db.execute('pragma quick_check').fetchone()[0]=='ok'

js=Path(__file__).with_name('app.js').read_text()
assert 'result.translation && (q.kind==="accent"||q.kind==="dialogue")' in js
assert 'note.className="answer-translation"' in js
print('PASS stress and 100 dialogue cards x six locales after correct and wrong answers')
