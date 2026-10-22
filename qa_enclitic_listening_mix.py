#!/usr/bin/env python3
"""Greek enclitic stress and mixed listening session checks, no production writes."""
import collections,random,tempfile
from pathlib import Path
import server,enclitic_stress as ens
from word_audio import lookup
import unicodedata
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert len(server.EXTRA_ALL)==26 and len(server.SYLLABLE_ALL)==35
assert len(server.ENCLITIC_ALL)==26
assert len(server.PRACTICE_ALL)==1978
assert len({x['id'] for x in server.PRACTICE_ALL})==1978
assert len(server.vocab.VOCAB)==1700
assert sum(bool(lookup(c['correct'],server.listening)['audioUrl']) for c in ens.CARDS)==26
assert len({c['correct'] for c in ens.CARDS})==26
for c in ens.CARDS:
    assert c['chapter']>=3 and c['curriculum_ready_unit']<=c['chapter']
    assert c['source'].startswith('independent_') and not c.get('book_page_verified')
    assert c['correct'] in c['options'] and len(set(c['options']))==4
    assert c['correct']==f"{c['article']} {c['stemWithClitic']} {c['pronoun']}"
    accent_count=sum(ch in 'άέήίόύώ' for ch in c['stemWithClitic'])
    assert accent_count==(2 if c['hasExtraStress'] else 1),c
    assert not c['pronoun'][-1] in 'άέήίόύώ'
    assert c['correct']!=c['options'][1]
    assert c['id'] in server.ENCLITIC_BY_ID
with tempfile.TemporaryDirectory(prefix='lexi-enclitic-mix-') as td:
    old=server.DB;server.DB=str(Path(td)/'student.sqlite3')
    try:
        server.init_db()
        count=0
        for c in ens.CARDS:
            for lang in ('ru','en','zh','ar','es','pt'):
                q=server.format_question(c,'stress_enclitic',lang)
                assert q['kind']=='enclitic' and q['direction']=='stress_enclitic'
                assert q['prompt']==f"{c['article']} {c['noun']} + {c['pronoun']}"
                assert len(set(q['choices']))==4 and set(q['choices'])==set(c['options'])
                assert q['wordAudio']['audioSource']=='pocket' and q['wordAudio']['audioUrl']
                assert q['sourcePageVerified'] is False and q['note']
                good=server.mark('student1',{'id':c['id'],'direction':'stress_enclitic','lang':lang,'selected':c['correct']})
                assert good['correct'] and good['hasExtraStress']==c['hasExtraStress']
                assert c['correct'] in good['tonosHint']
                wrong=server.mark('student1',{'id':c['id'],'direction':'stress_enclitic','lang':lang,
                                              'selected':next(v for v in c['options'] if v!=c['correct'])})
                assert not wrong['correct'] and 'tonosHint' in wrong
                count+=2
        assert count==312
        args={'scope':['chapters'],'chapters':['1,2,3,4'],'types':['word,phrase,sentence,accent,enclitic'],
              'lang':['ru'],'count':['60'],'listenMix':['1']}
        for i in range(6):
            q=server.make_quiz('student1',args)
            assert q['count']==60 and q['mixedListening']==12,(q['count'],q['mixedListening'])
            assert all(x['kind']=='listening' for x in q['questions'][4::5])
            assert all(x['kind']!='listening' for j,x in enumerate(q['questions']) if j%5!=4)
            assert len({x['id'] for x in q['questions']})==60
            assert len({x['semanticId'] for x in q['questions']})==60
            assert all(x['chapter'] in {1,2,3,4} for x in q['questions'])
            for card in q['questions']:
                if card['kind']=='listening':
                    assert card['audioUrl'].startswith('/greek/audio/')
                    assert len(card['choices'])==8
            assert len([x for x in q['questions'] if x['kind']=='listening'])==12
        args['listenMix']=['0']
        assert server.make_quiz('student1',args)['mixedListening']==0
        args['listenMix']=['1'];args['types']=['accent,enclitic']
        assert server.make_quiz('student1',args)['mixedListening']==0
        args['types']=['word,phrase,sentence']
        args['chapters']=['7,8,9,11']
        q=server.make_quiz('student1',args)
        assert q['mixedListening']<=12 and q['mixedListening']>0
        assert all(x['chapter'] in {7,8,9,11} for x in q['questions'])
        args['scope']=['listening']
        q=server.make_quiz('student1',args)
        assert q['mixedListening']==0 and all(x['kind']=='listening' for x in q['questions'])
        # pages scope respects exact published source-page constraints.
        args={'scope':['pages'],'from':['39'],'to':['56'],'types':['word,phrase,sentence,enclitic'],
              'count':['60'],'lang':['ru'],'listenMix':['1']}
        q=server.make_quiz('student1',args)
        assert q['mixedListening']>=1
        assert all(39<=x['page']<=56 for x in q['questions'])
        cap=server.estimate_capacity('student1',args)
        assert cap['listeningMixAvailable']>=q['mixedListening']
        assert cap['listeningMixEnabled']
        args['mode']=['srs_due']
        assert server.make_quiz('student1',args)['mode']=='srs_due'
        with server.conn() as db:
            assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
    finally:server.DB=old
print('PASS ENCLITIC MIX: 26 validated minimal pairs, 6 locales, 312 grades, 26 exact Pocket audio,'
      ' 12/60 inserted existing listening, chapter/page filtering, no audio duplicate, separate listening preserved')
