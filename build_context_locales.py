"""Translate still-fallback textbook Arabic glosses and conjugation phrase sentences."""
import json
from pathlib import Path
from fill_vocab_locales import translate
import catalog_v2 as cat
import verb_phrase as vp
ROOT=Path(__file__).parent
target=ROOT/'textbook_ar_complete.json'
existing=json.loads(target.read_text()) if target.exists() else {}
phrases=ROOT/'verb_phrase_locales.json'
atlas=json.loads(phrases.read_text()) if phrases.exists() else {k:{} for k in ('zh','es','pt')}
for key in atlas:atlas.setdefault(key,{})

def save():
 target.write_text(json.dumps(existing,ensure_ascii=False,indent=1))
 phrases.write_text(json.dumps(atlas,ensure_ascii=False,indent=1))

words={x.get('en') for x in cat.ALL if x.get('kind') not in ('dialogue','plural') and x.get('en') and not x.get('ar')}
current=json.loads((ROOT/'translations_ar.json').read_text())
words={en for en in words if not current.get(en) and not existing.get(en)}
print('missing Arabic textbook unique EN glosses',len(words),flush=True)
ordered=sorted(words)
for i in range(0,len(ordered),30):
 sub=ordered[i:i+30]
 t=translate(sub,'ar')
 for key,value in zip(sub,t):existing[key]=value
 if i%150==0:save();print('book Arabic',min(i+30,len(ordered)),len(ordered),flush=True)
save()
for lang in ('zh','es','pt'):
 todos=[]
 for lemma,verb_data in vp.SPECS.items():
  for person in range(6):
   # Use actual textbook verb card by lemma/person.
   sample=next(x for x in cat.ALL if x['kind']=='verb' and x['gr']==lemma and x['person']==person)
   _,en=vp.phrase(sample,'en')
   key=lemma+':'+str(person)
   if not atlas[lang].get(key):todos.append((key,en))
 print('Verb sentences',lang,len(todos),flush=True)
 for i in range(0,len(todos),20):
  sub=todos[i:i+20]
  values=translate([v[1] for v in sub],lang)
  for (key,en),value in zip(sub,values):atlas[lang][key]=value
  if i%100==0:save();print('verbs',lang,min(i+20,len(todos)),len(todos),flush=True)
 save()
print('textbook ar glosses',len(existing),'verbs',[(x,len(atlas[x])) for x in atlas],flush=True)
