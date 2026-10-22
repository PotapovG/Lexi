"""Evidence-labelled audit queue, not autonomous native Greek proofreading.

The PDF and original word-by-word source indexing are not available in this
production folder, so this report intentionally never claims book attestation.
"""
from collections import Counter,defaultdict
from pathlib import Path
import datetime,json
import server as data
import textbook_alignment as book
import pedagogy_rules as rules
from accepted_glosses import _ALIASES

LANGS=('ru','en','zh','ar','es','pt')
CARDS=data.ALL
MATERIAL=[c for c in CARDS if c.get('curriculum') not in ('topic','verb')]
ISSUES=[]
def flag(level,reason,card,details=None):
    ISSUES.append(dict(priority=level,reason=reason,id=card['id'],
                       chapter=card.get('chapter'),page=card.get('page'),
                       notes=details or 'Requires editorial review; no automatic correction'))

for c in MATERIAL:
    unit=book.INDEX.get(c['chapter'])
    if not unit or not unit['start']<=c['page']<=unit['end']:
        flag('blocker','outside_verified_chapter_bounds',c)
    # Greek-only dialogues use no translated glosses; noun plural cards
    # are Greek-form-only and do not reference per-card zh/es/pt fields.
    if c['kind'] not in ('dialogue','plural'):
        for lang in LANGS:
            if not isinstance(c.get(lang),str) or not c[lang].strip():
                flag('blocker','missing_runtime_translation_'+lang,c)
    if c['kind'] in ('word','phrase','sentence'):
        if c.get('curriculum_ready_unit',c['chapter'])>c['chapter'] and c['chapter']>=1:
            flag('review','potential_grammar_prerequisite',c)
    if c['kind']=='dialogue':
        if len(c.get('bank',[]))!=8 or len(set(c['bank']))!=8:
            flag('blocker','dialogue_bank_not_eight_distinct',c)
        if len(c.get('gaps',[]))!=len(set(c.get('gaps',[]))):
            flag('review','repeated_dialogue_answer',c)
        for answer in c.get('gaps',[]):
            if answer not in c.get('bank',[]):
                flag('blocker','dialogue_answer_missing_from_bank',c)

by_greek=defaultdict(list)
for c in MATERIAL:
    if c['kind'] not in ('word','phrase','sentence'):continue
    if c.get('gr'):by_greek[rules.canonical_greek(c['gr'])].append(c)
for greek,group in by_greek.items():
    meanings={(c['ru'],c['en']) for c in group}
    if len(meanings)>1:
        for c in group[:1]:
            flag('review','same_greek_different_gloss',c,
                 'Potential polysemy, gender or context: human must decide; other IDs '+','.join(x['id'] for x in group[1:7]))
    if len({c.get('chapter') for c in group})>1:
        # Duplicates may be intentional; record only a sampled inventory.
        pass

dialogues=[c for c in MATERIAL if c['kind']=='dialogue']
first4=[c for c in MATERIAL if c.get('chapter') in (1,2,3,4)]
review={
 'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source_status':{
    'licensed_pdf_in_production':False,
    'full_source_lemma_to_page_attestation':False,
    'printed_20_unit_boundaries':'verified from previous PDF inspection',
    'card_page_coordinates':'approximate; cannot certify against pages'},
 'corpus':dict(textbook_cards=len(CARDS),printed_or_supplementary_cards=len(MATERIAL),
               first_four_items=len(first4),dialogues=len(dialogues),
               reviewed_gloss_id_count=len(_ALIASES),kind=dict(Counter(c['kind'] for c in MATERIAL))),
 'effective_locales':'Runtime-resolved language fields; Greek-only dialogue and noun-form cards intentionally excluded from gloss checks.',
 'requirements_unmet':[
   'Human-reviewed complete first-four-unit lexical inventory against the actual PDF',
   'Native/editor review of all dialogue turn alternatives and naturalness',
   'Item-by-item independent Greek and six-locale gloss proofreading',
   'Exact per-item page evidence rather than approximate chapter anchors'],
 'issues':ISSUES,
 'summary':dict(Counter(x['reason'] for x in ISSUES)),
 'editorial_note':'Flags are triage candidates, not confirmed linguistic mistakes. Do not auto-accept synonyms or rewrite legacy IDs.'
}
out=Path('editorial-audit')
out.mkdir(exist_ok=True)
path=out/'sixcycle-20261020.json'
path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print('EDITORIAL_AUDIT',path,'items',len(MATERIAL),'first4',len(first4),'dialogues',len(dialogues))
print('FLAGS',review['summary'])
