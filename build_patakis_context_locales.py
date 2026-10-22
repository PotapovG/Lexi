"""Run on Core to build 4 target gloss languages for independently-written
book-context tasks. No PDF, scans, publisher exercises, or user DB are used."""
from pathlib import Path
import csv,json
# Independent translation helper: do not import the app here, since the app
# imports the completed locale atlas and that would create a circular import.
import requests, time
LOCALES={'zh':'zh-CN','ar':'ar','es':'es','pt':'pt-PT'}
def translate(items,lang):
    if not items:return []
    text='\n'.join(items)
    r=requests.get('https://translate.googleapis.com/translate_a/single',
        params={'client':'gtx','sl':'en','tl':LOCALES[lang],'dt':'t','q':text},timeout=20)
    r.raise_for_status()
    translated=''.join(chunk[0] or '' for chunk in r.json()[0]).split('\n')
    if len(translated)!=len(items) or not all(x.strip() for x in translated):
        if len(items)==1:raise ValueError('Bad translation response')
        mid=len(items)//2
        return translate(items[:mid],lang)+translate(items[mid:],lang)
    return [x.strip() for x in translated]

ROOT=Path(__file__).parent
rows=[]
with (ROOT/'patakis_context_original.tsv').open(encoding='utf-8') as f:
    for line in f:
        if line.startswith('#') or not line.strip():continue
        cols=line.rstrip('\n').split('|')
        assert len(cols)==6,line
        rows.append(cols)
output=ROOT/'patakis_context_locales.json'
cache=json.loads(output.read_text()) if output.exists() else {l:{} for l in ('ar','zh','es','pt')}
enlist=list(dict.fromkeys(row[5] for row in rows))
for locale in ('zh','ar','es','pt'):
    missing=[en for en in enlist if not cache[locale].get(en)]
    print(locale,'missing',len(missing),flush=True)
    for i in range(0,len(missing),20):
        group=missing[i:i+20]
        response=translate(group,locale)
        for en,tr in zip(group,response):cache[locale][en]=tr
        output.write_text(json.dumps(cache,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('Complete',len(rows),'original book-informed cards in four locales')
