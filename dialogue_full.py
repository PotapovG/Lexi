"""Curated Russian and English translations of complete authorial Lexi dialogues.

The .txt tables mirror the number of Greek lines and placeholder positions.
Only returned after a scored answer; the browser reveals them once the final
exercise gap is completed, not while a learner is still choosing replies.
"""
from pathlib import Path
import re
import dialogue_translations as gap_glosses

ROOT=Path(__file__).parent
MARK=re.compile(r'\[\[(\d+)\]\]')

def load(lang):
    path=ROOT/f'dialogue_full_{lang}.txt'
    result={}
    for line in path.read_text(encoding='utf-8').strip().splitlines():
        cid,*lines=line.split('|')
        if not cid or not lines: raise ValueError(f'bad full-dialogue translation: {lang}/{cid}')
        cid='dlg'+cid
        if cid in result:raise ValueError(f'duplicate full-dialogue id: {cid}')
        result[cid]=lines
    return result

TABLES={lang:load(lang) for lang in ('ru','en')}

def validate(cards):
    dialogues={c['id']:c for c in cards if c['kind']=='dialogue'}
    for lang,table in TABLES.items():
        if table.keys()!=dialogues.keys():
            raise ValueError(f'full-dialogue coverage mismatch for {lang}')
        for cid,card in dialogues.items():
            lines=table[cid]
            if len(lines)!=len(card['lines']):
                raise ValueError(f'line count mismatch {lang}/{cid}')
            for i,(original,translated) in enumerate(zip(card['lines'],lines)):
                expected=MARK.findall(original)
                got=MARK.findall(translated)
                if expected!=got:
                    raise ValueError(f'placeholder mismatch {lang}/{cid}/line{i}: {expected} vs {got}')
                if not translated.strip() or not re.match(r'^[ΑΒΓAАВБBC]:',translated):
                    raise ValueError(f'bad translated speaker line {lang}/{cid}/line{i}')
    return len(dialogues)

def after_score(card,lang):
    # The other four UI locales currently receive fully English dialogue text
    # visibly marked "EN". Do not blend English static lines with translations
    # of only the gaps in an unrelated UI language.
    used_lang='ru' if lang=='ru' else 'en'
    glosses={}
    for i,canonical in enumerate(card['gaps']):
        direction=f'gap{i}'
        for greek in {canonical,*card.get('acceptedByGap',{}).get(direction,[])}:
            gloss,actual=gap_glosses.lookup(card,direction,used_lang,greek)
            assert actual==used_lang
            glosses[greek]=gloss
    return {'dialogueFullTemplate':TABLES[used_lang][card['id']],
            'dialogueFullGlosses':glosses,
            'dialogueFullLang':used_lang}
