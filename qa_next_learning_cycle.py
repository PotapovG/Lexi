#!/usr/bin/env python3
"""Advanced Greek syllable stress and chapter prerequisites; isolated DB only."""
import collections
from pathlib import Path
from tempfile import TemporaryDirectory
import server,advanced_syllables as syl,grammar_scope_guard as guard
import learning_upgrade
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717
assert len(server.EXTRA_ALL)==26 and len(server.SYLLABLE_ALL)==35
assert len(server.PRACTICE_ALL)==1978
assert len({c['id'] for c in server.PRACTICE_ALL})==1978
assert len({c['id'] for c in server.SYLLABLE_ALL})==35
assert len({c['source_parent_id'] for c in server.SYLLABLE_ALL})==35
assert 'syllable' in server.KINDS
for card in syl.CARDS:
    assert card['source'].startswith('independent_')
    assert not card.get('book_page_verified')
    assert len(card['parts'])==len(card['plainParts'])
    assert syl._plain(''.join(card['parts']))==card['base']
    assert ''.join(card['parts'])==card['gr']
    assert 1<=card['stressedIndex']+1<=card['syllableCount']
    assert card['curriculum_ready_unit']<=card['chapter']
    assert server.BY_ID[card['source_parent_id']]['accented']==card['gr']

langs=('ru','en','zh','ar','es','pt')
renders=right=wrong=0
with TemporaryDirectory(prefix='syllable-cycle-') as t:
    old=server.DB
    try:
        server.DB=str(Path(t)/'qa.sqlite3')
        server.init_db()
        for card in server.SYLLABLE_ALL:
            for lang in langs:
                q=server.format_question(card,'stress_syllable',lang)
                assert q['kind']=='syllable' and q['id']==card['id'] and q['direction']=='stress_syllable'
                assert q['syllableCount']==len(q['choices'])
                assert 2<=len(q['choices'])<=6
                assert len(set(q['choices']))==len(q['choices'])
                assert not q.get('sourcePageVerified')
                assert q['prompt'].replace(' · ','')==card['base']
                assert all('́' not in p for p in q['syllables'])
                assert 'correctIndex' not in q and 'accentSyllableIndex' not in q
                renders+=1
                answer=server.shape(card,'stress_syllable',lang)[1]
                assert answer in q['choices']
                result=server.mark('qa',dict(id=card['id'],direction='stress_syllable',lang=lang,selected=answer))
                assert result['correct'] and result['correctIndex']==card['stressedIndex']
                assert result['syllableBreakdown']=='-'.join(card['parts'])
                right+=1
                distractor=next(c for c in q['choices'] if c!=answer)
                negative=server.mark('qa',dict(id=card['id'],direction='stress_syllable',lang=lang,selected=distractor))
                assert not negative['correct'] and negative['missDebt']>=2
                assert negative.get('tonosHint')
                wrong+=1
        assert (renders,right,wrong)==(210,210,210)
        with server.conn() as db:
            assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
        early={'scope':['chapters'],'chapters':['9'],'types':['dialogue,syllable,sentence'],
               'count':['60'],'lang':['ru'],'mode':['all']}
        p=server.make_quiz('qa',early)
        assert p['grammarDeferred']>=1,p
        assert not any(q['id']=='dlg059' for q in p['questions'])
        assert all(guard.milestone(server.book_or_audio_card(q['id']))<=9 for q in p['questions'])
        earlycap=server.estimate_capacity('qa',early)
        assert earlycap['grammarDeferred']==p['grammarDeferred']
        late=dict(early,chapters=['9,16'])
        p_late=server.make_quiz('qa',late)
        assert p_late['grammarDeferred']==0
        assert any(q['id']=='dlg059' for q in p_late['questions']),[q['id'] for q in p_late['questions']]
        # 17–20 selector remains functional; no source ledger mutation.
        later=dict(early,chapters=['17,18'])
        assert server.make_quiz('qa',later)['count']>0
        # Stress syllable-only lesson mode and malformed answers
        scope={'scope':['chapters'],'chapters':['1,2,3,4'],'types':['syllable'],
               'count':['60'],'lang':['en'],'mode':['all']}
        syllables=server.make_quiz('qa',scope)
        assert syllables['count']>=15
        assert all(q['kind']=='syllable' for q in syllables['questions'])
        try:
            server.mark('qa',dict(id=server.SYLLABLE_ALL[0]['id'],direction='stress_syllable',
                  selected='7 · fake',lang='ru'))
            raise AssertionError('invalid syllable accepted')
        except ValueError:
            pass
        # Actual stress-letter questions still score by *letter*, not syllable.
        oldaccent=next(c for c in server.ALL if c['kind']=='accent')
        correct=server.mark('qa',dict(id=oldaccent['id'],direction='accent',lang='ru',
                                     selected=str(oldaccent['accent_index'])))
        assert correct['correct']
    finally:
        server.DB=old
print('PASS SYLLABLE CYCLE',renders,'question renders,',right,'correct,',wrong,
      'wrong grades in 6 languages; chapter gate/filter/capacity, old accents and source 1795 intact')
