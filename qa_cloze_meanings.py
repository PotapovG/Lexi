"""Post-scoring translations and case explanations for every cloze card."""
import tempfile
from pathlib import Path

import server
import cloze_meanings as meanings

assert meanings.validate()==80
assert len(server.GRAMMAR2_ALL)==56
articles=[c for c in server.ALL if c["kind"]=="article"]
assert len(articles)==24
cards=articles+server.GRAMMAR2_ALL

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'test.sqlite3')
    server.init_db()
    for lang in ('ru','en','zh','ar','es','pt'):
        expected_lang=lang if lang in ('ru','en') else 'en'
        for card in cards:
            direction='fill' if card['kind']=='article' else 'grammar_fill'
            question=server.format_question(card,direction,lang)
            assert 'clozeTranslation' not in question
            assert 'clozeGreek' not in question
            assert 'Книга принадлежит ученику' not in str(question)
            correct=card['correct']
            answer=server.mark('right-'+card['id']+lang,{
                'id':card['id'],'direction':direction,'lang':lang,'selected':correct})
            assert answer['correct'],(card['id'],lang,answer)
            assert answer['clozeGreek']==card['prompt'].replace('___',correct)
            assert answer['clozeTranslationLang']==expected_lang
            assert answer['clozeTranslation']==meanings.translation(card,lang)[0]
            bad=next(x for x in (card.get('options') or []) if x not in
                     (card.get('acceptedForms') or [correct]))
            wrong=server.mark('wrong-'+card['id']+lang,{
                'id':card['id'],'direction':direction,'lang':lang,'selected':bad})
            assert not wrong['correct']
            assert wrong['clozeGreek']==answer['clozeGreek']
            assert wrong['clozeTranslation']==answer['clozeTranslation']
            assert wrong['missDebt']==2
            if card['kind']=='grammar' and card.get('group')=='case':
                assert answer['clozeFormHint'],(card['id'],lang)
                assert answer['grammarTip']==answer['clozeFormHint']
                assert wrong['explanation']==answer['clozeFormHint']
        # Double-option feminine article forms keep the user's correct
        # selection and still show the meaning of the whole sentence.
        card=next(c for c in articles if len(c['acceptedForms'])>1)
        alternative=card['acceptedForms'][1]
        variant=server.mark('alternate-'+lang,{
            'id':card['id'],'direction':'fill','lang':lang,'selected':alternative})
        assert variant['correct'] and variant['acceptedVariant']
        assert alternative in variant['clozeGreek']
        assert variant['clozeTranslation']
    target=server.GRAMMAR2_ALL[9]
    assert target['id']=='g2261021_010'
    example=server.mark('example',{
        'id':target['id'],'direction':'grammar_fill','lang':'ru','selected':'του'})
    assert example['clozeGreek']=='Το βιβλίο είναι του μαθητή.'
    assert example['clozeTranslation']=='Книга принадлежит ученику.'
    assert 'родительный падеж' in example['clozeFormHint']
    with server.conn() as db:
        assert db.execute('pragma quick_check').fetchone()[0]=='ok'

js=Path(__file__).with_name('app.js').read_text()
assert 'result.clozeTranslation && (q.kind==="article"||q.kind==="grammar")' in js
assert 'txt("question-prompt",result.clozeGreek)' in js
assert '(language!==answerLang?" (EN)":"")' in js
print('PASS 80 article/grammar cloze cards x six locales: full after-answer translations')
print('PASS right/wrong feedback, actual case hint, valid spelling alternatives, no pre-answer leak')
