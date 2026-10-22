"""Apply reviewed polysemy/grammar corrections on top of bulk glossary candidates."""
import json
from pathlib import Path
import vocab_lessons as vocab
ROOT=Path(__file__).parent
reviewed=json.loads((ROOT/'vocab_manual_corrections.json').read_text('utf-8'))
atlas_path=ROOT/'vocab_translations_1700.json'
atlas=json.loads(atlas_path.read_text('utf-8'))
vocab_by_gr={w['gr']:w for w in vocab.VOCAB}
unknown=set(reviewed)-set(vocab_by_gr)
if unknown:raise ValueError('Corrected words not in course: '+str(sorted(unknown)))
for gr,locales in reviewed.items():
    for lang,translation in locales.items():
        if lang not in ('zh','es','pt','ar'):raise ValueError('unexpected locale '+lang)
        atlas[lang][vocab_by_gr[gr]['id']]=translation
atlas_path.write_text(json.dumps(atlas,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('Applied',sum(map(len,reviewed.values())),'verified updates on',len(reviewed),'Greek headwords')
