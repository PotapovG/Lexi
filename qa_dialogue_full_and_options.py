"""After-answer complete dialogue translations and normalized option uniqueness."""
import collections
import re
import tempfile
from pathlib import Path

import server
import dialogue_full
import distractor_quality

cards=[c for c in server.ALL if c['kind']=='dialogue']
assert dialogue_full.validate(server.ALL)==100
norm=distractor_quality.norm
for lang in ('ru','en','zh','ar','es','pt'):
    for card in cards:
        info=dialogue_full.after_score(card,lang)
        assert len(info['dialogueFullTemplate'])==len(card['lines'])
        expected_language=lang if lang in ('ru','en') else 'en'
        assert info['dialogueFullLang']==expected_language
        result=[re.sub(r'\[\[(\d+)\]\]',lambda m:info['dialogueFullGlosses'][card['gaps'][int(m[1])]],line)
                for line in info['dialogueFullTemplate']]
        assert all('[[' not in line and line for line in result),card['id']
        if card['id']=='dlg035':
            assert any('У меня один брат и одна сестра' in t for t in result) if lang=='ru' else True
        if card['id']=='dlg033':
            assert len(info['dialogueFullGlosses'])==2
        for line in info['dialogueFullTemplate']:
            assert not re.search(r'\[\[(\d+)\]\].*\[\[(\d+)\]\].*\[\[(\d+)\]\]',line)
# Real screenshot, plus the other capitalization-only accepted answers.
case_duplicates=('w058','w059','w060','p002','p005')
for cid in case_duplicates:
    card=server.BY_ID[cid]
    for lang in ('ru','en','zh','ar','es','pt'):
        for i in range(4):
            options,_=server.generate_options(card,'gr-ru',card[lang],lang)
            assert len(options)==8 and len(set(map(norm,options)))==8,(cid,lang,options)

with tempfile.TemporaryDirectory() as folder:
    server.DB=str(Path(folder)/'test.sqlite3')
    server.init_db()
    for lang in ('ru','en','zh','ar','es','pt'):
        for card in cards:
            assert 'dialogueFullTemplate' not in server.format_question(card,'gap0',lang)
            for i,greek in enumerate(card['gaps']):
                result=server.mark('tester_'+lang+card['id']+str(i),
                        dict(id=card['id'],direction=f'gap{i}',selected=greek,lang=lang))
                assert result['correct']
                assert result['dialogueFullLang'] in (lang,'en')
                assert len(result['dialogueFullTemplate'])==len(card['lines'])
                if i==0:
                    wrong=server.mark('wrong_'+lang+card['id'],
                       dict(id=card['id'],direction='gap0',selected='not an answer',lang=lang))
                    assert not wrong['correct'] and wrong['dialogueFullTemplate']==result['dialogueFullTemplate']
    card=server.BY_ID['dlg033']
    for selected in card['gaps']:
        result=server.mark('jobs'+selected,dict(id='dlg033',direction='gap0',selected=selected,lang='ru'))
        assert result['correct']
        assert result['dialogueFullGlosses'][selected]==result['translation']
    with server.conn() as db:
        assert db.execute('pragma quick_check').fetchone()[0]=='ok'
js=Path(__file__).with_name('app.js').read_text()
assert 'if(Array.isArray(result.dialogueFullTemplate))' in js
assert 'const anotherGap=state.dialogueStep<q.gapIndices.length-1' in js
assert 'panel.className="dialogue-full-translation"' in js
print('PASS 100 full dialogues RU/EN + EN-labelled fallback x 6 locales')
print('PASS translations after scoring, complete only at last gap, bad answers, accepted alternatives')
print('PASS distinct normalized choices for case-duplicate word and phrase cards')
