"""Regression: underdetermined profession dialogue accepts both valid replies."""
import tempfile
from pathlib import Path
import server

card=server.BY_ID['dlg033']
assert card['lines']==['Α: Τι δουλειά κάνεις;', 'Β: [[0]]. Εσύ;', 'Α: [[1]].']
expected=set(card['gaps'])
assert expected=={'Είμαι δασκάλα','Είμαι οδηγός λεωφορείου'}
assert all(set(card['acceptedByGap'][f'gap{i}'])==expected for i in (0,1))
assert card['allowRepeatChoices']

with tempfile.TemporaryDirectory() as folder:
    server.DB=str(Path(folder)/'test.sqlite3')
    server.init_db()
    for lang in ('ru','en','zh','ar','es','pt'):
        q=server.format_question(card,'gap0',lang)
        assert q['allowRepeatChoices'] is True
        assert set(q['choices']).issuperset(expected)
        for i in (0,1):
            for text in expected:
                response=server.mark(f'{lang}:{i}:{text}',{
                    'id':'dlg033','direction':f'gap{i}','lang':lang,'selected':text
                })
                assert response['correct'],response
                assert response['answer']==text,response
                assert set(response['acceptedAnswers'])==expected,response
                assert response['missDebt']==0
            response=server.mark(f'wrong:{lang}:{i}',{
                'id':'dlg033','direction':f'gap{i}','lang':lang,
                'selected':'Πού μένεις;'
            })
            assert not response['correct']
        # The two speakers may independently have exactly the same job.
        for i in (0,1):
            response=server.mark(f'repeat:{lang}',{
                'id':'dlg033','direction':f'gap{i}','lang':lang,
                'selected':'Είμαι δασκάλα'
            })
            assert response['correct']
    with server.conn() as db:
        assert db.execute('pragma quick_check').fetchone()[0]=='ok'

js=Path(__file__).with_name('app.js').read_text()
assert 'if(!q.allowRepeatChoices&&Object.values(state.dialogueFilled).includes(choice))' in js
print('PASS: dlg033 accepts both profession answers for both blanks in six UI languages')
print('PASS: same job allowed for both speakers; irrelevant answers rejected; UI supports repeats')
