#!/usr/bin/env python3
"""Keep authored order-drill translation prompts identical to reviewed parents.

The order drill inherits Greek text from a separately authored source
sentence. Later copy-editorial locale fixes on the sentence must also
propagate to the order drill so the prompt doesn't change friend gender.
Neither IDs, Greek tokens nor right answers are changed.
"""
LANGS=('ru','en','zh','ar','es','pt')
EXPECTED_CORRECTIONS={
 ('order_patk02_003','ar'),
 ('order_patk02_003','es'),
 ('order_patk03_005','es'),
}

def apply(cards,langs=LANGS):
    assert set(langs)<=set(LANGS) and langs
    byid={c['id']:c for c in cards}
    corrections=[]
    orders=[c for c in cards if c['kind']=='order']
    assert len(orders)==17,len(orders)
    for card in orders:
        assert card['id'].startswith('order_')
        parent=byid[card['id'][len('order_'):]]
        assert parent['kind'] in ('sentence','phrase')
        assert card['gr']==parent['gr'] and card['tokens']==parent['gr'].split()
        assert (card['chapter'],card['page'])==(parent['chapter'],parent['page'])
        for lang in langs:
            if card[lang]!=parent[lang]:
                corrections.append((card['id'],lang))
                card[lang]=parent[lang]
    expected={key for key in EXPECTED_CORRECTIONS if key[1] in langs}
    assert set(corrections)==expected,corrections
    return corrections
