"""Non-linguistic pre-release audit of stable IDs and language metadata.

Passing this audit does NOT certify textbook exact-page proof or natural Greek.
"""
import collections,json,datetime,unicodedata,re
from pathlib import Path
import server
lang=('ru','en','zh','ar','es','pt')
issues=[]
counts=collections.Counter()
book=server.ALL
for c in book:
    cid=c['id'];kind=c['kind'];counts[kind]+=1
    if not cid or not isinstance(cid,str):issues.append((cid,'invalid_id'))
    if c.get('curriculum') not in ('topic','verb','personalized') and c.get('chapter',0)>0:
        unit=next((u for u in server.CHAPTERS if u['id']==c['chapter']),None)
        if unit is None or not(unit['start']<=c.get('page',-1)<=unit['end']):issues.append((cid,'outside_chapter_page_range'))
    greek=c.get('gr') or c.get('sg') or c.get('prompt') or ''
    if greek and unicodedata.normalize('NFC',greek)!=greek:issues.append((cid,'non_nfc_greek'))
    if greek and re.search('[A-Za-zА-Яа-яЁё]',greek):issues.append((cid,'unexpected_non_greek_letters'))
    if greek and '  ' in greek:issues.append((cid,'double_whitespace'))
    if kind=='dialogue':
        if len(c['bank'])!=8 or len(set(c['bank']))!=8:issues.append((cid,'bank_choices_not_unique_8'))
        if any(a not in c['bank'] for a in c['gaps']):issues.append((cid,'missing_gap_answer_from_bank'))
    if kind=='article':
        if len(c['options'])!=8 or c['correct'] not in c['options']:issues.append((cid,'article_options'))
    if kind in ('word','phrase','sentence','number','verb','article','order','accent','letter'):
        for l in lang:
            if not isinstance(c.get(l),str) or not c[l].strip():issues.append((cid,'missing_'+l))
assert len(book)>=1795
assert len({c['id'] for c in book})==len(book)
assert counts['dialogue']==100
assert len(__import__('catalog_v2').CURATED_DIALOGUE_BANKS)==35
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'catalog_cards':len(book),'kind_counts':dict(counts),
 'dialogue_options_recurated':35,'case_equivalence_mitigated':'dlg024',
 'source_provenance':'The owner-provided purchased book PDF is not served by Core. Page anchors remain approximate.',
 'audit_type':'Machine-verifiable card structure only; NOT native Greek proofreading or exact lemma-to-page concordance.',
 'issue_count':len(issues),'issues':issues[:250],
 'remaining_work':['Human lexical inventory first four units','Native Greek+6 locale content reading','Real page evidence per lemma','Meaning-specific correct synonyms across 6 languages','Versioned replacement for ambiguous dlg024']}
path=Path('editorial-audit/full-card-structure-20261020.json');path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('FULL_CARD_STRUCTURE',dict(counts),'issues',len(issues),'saved',path)
assert not issues,issues[:20]
