"""Every word-order card tests morphology/syntax, not token punctuation."""
import collections
import tempfile
from pathlib import Path
import server
import order_valid_permutations as order

cards=[c for c in server.PRACTICE_ALL if c['kind']=='order']
assert len(cards)==65,len(cards)
assert len({c['id'] for c in cards})==65
assert sum('μου:' in c['tokens'] for c in cards)==1

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'progress.sqlite3')
    server.init_db()
    for card in cards:
        normalized_words=[order.choice_token(x) for x in card['tokens']]
        assert all(x and x not in ('μου:', 'μου,', 'μου.') for x in normalized_words)
        # Shuffled token positions correspond exactly to clean choice labels.
        for lang in ('ru','en','zh','ar','es','pt'):
            q=server.format_question(card,'arrange',lang)
            assert len(q['choiceTokens'])==len(q['tokens'])
            assert q['choiceTokens']==[order.choice_token(x) for x in q['tokens']]
            assert collections.Counter(q['choiceTokens'])==collections.Counter(normalized_words)
            assert all(x and x==order.choice_token(x) for x in q['choiceTokens'])
            selected=' '.join(normalized_words)
            result=server.mark('learner_'+card['id']+'_'+lang,{
                'id':card['id'], 'direction':'arrange','lang':lang,
                'selected':selected})
            assert result['correct'] and result['formattedOrder']==card['gr'],(card['id'],lang,result)
            # Previous clients may still submit punctuation-bearing tokens.
            original=server.mark('original_'+card['id']+'_'+lang,{
                'id':card['id'], 'direction':'arrange','lang':lang,
                'selected':' '.join(card['tokens'])})
            assert original['correct']
        variants=order.VARIANTS.get(card['id'],[])
        for variant in variants:
            selected=' '.join(order.choice_token(x) for x in variant.split())
            result=server.mark('variant_'+card['id'],{
                'id':card['id'],'direction':'arrange','lang':'ru',
                'selected':selected})
            assert result['correct'] and result['formattedOrder']==variant,(card['id'],result)
        wrong=server.mark('wrong_'+card['id'],{
            'id':card['id'],'direction':'arrange','lang':'ru',
            'selected':' '.join(reversed(normalized_words))})
        assert not wrong['correct'],card['id']
    example=next(c for c in cards if c['id']=='order_patk03_001')
    assert collections.Counter(order.choice_token(x) for x in example['tokens'])['μου']==4
    assert order.formatted(example, ' '.join(order.choice_token(x) for x in example['tokens']))==example['gr']
    with server.conn() as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'

js=Path(__file__).with_name('app.js').read_text()
assert 'const words=orderWords(q);' in js
assert 'words.forEach((word,i)=>' in js
assert 'selected.map(i=>words[i]).join(" ")' in js
assert 'state.orderIndices.map(i=>orderWords(q)[i]).join(" ")' in js
assert 'if(result.correct)txt("order-draft",result.formattedOrder||result.answer)' in js
print('PASS 65 word-order exercises x six locales: punctuation-free choices, correct score, formatted result')
print('PASS 33 curated alternatives + wrong answers, restored old client payload compatibility')
