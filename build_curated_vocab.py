"""Developer-only content selector. Outputs independently written Greek-Russian-English lexical entries.

Kelly Greek frequency data may optionally guide ordering but IS NEVER incorporated
into shipped content. Source datasets are referenced, not copied.
"""
from __future__ import annotations
import collections
import hashlib
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Optional
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
import vocab_lessons as vocab

A1_GOALS={"everyday":39,"food":27,"home":27,"work":21,"health":22,"nature":21,
          "leisure":16,"shopping":17,"family":12,"time":14,"city":14,"road":9,"travel":10}
A2_GOALS={"everyday":80,"family":28,"food":50,"shopping":48,"home":50,"work":50,
          "road":40,"city":43,"travel":49,"leisure":49,"nature":52,"health":48,"time":36}
assert sum(A1_GOALS.values())==249
assert sum(A2_GOALS.values())==623

# Incorrect/unnatural learner senses, plural restatements, fragments,
# nonstandard synonyms, and compositional phrases that should not count as lemmas.
REJECT={
    "ο λόγος μου","το σήμερα","το αύριο","το χθες","οι παππούδες",
    "τα σκουπίδια","οι εκπτώσεις","τα μετρητά","οι συγγενείς",
    "η συνάδελφος", # already represented by ο συνάδελφος; identical lemma
    "η σύζυγος",    # represented by ο σύζυγος in original vocab
    "η μεζές","ο αντικαταβολή","το δέρμα τσάντας","η εγκατάσταση μπάνιου",
    "το μάτι του νερού","η ανησυχία μου","το ζευγάρι φίλων",
    "η εμπιστοσύνη μεταξύ φίλων","η κατεύθυνση σκέψης","η απόφαση της ημέρας",
    "η ταχύτητα της ζωής","το λόγο μου","η ανάγκη για βοήθεια",
    "η ποιότητα ζωής","η επικοινωνία με ντόπιους","η παραδοσιακή ζωή",
    "η περίοδος εγγύησης","η διαθεσιμότητα χρόνου","η σύγκριση προϊόντος",
    "η ολοκλήρωση για πάντα","η επιχείρηση ημέρας",
    "η φασολάδα μαγειρευτή",
    "ο πληροφοριοδότης", # advanced / low usefulness
    "η ωταλγία", # specialist term
    "η αιφνιδιάζομαι",
    "ο αερολιμένας", # overly formal for A2
}
def norm(gr):
    word=unicodedata.normalize("NFC",gr).casefold().strip()
    return re.sub(r"^(?:ο|η|το|οι|τα)\s+","",word)

def category(gr):
    if re.match(r"^(ο|η|το|οι|τα)\s",gr):return "noun"
    if gr.endswith(("ω","ώ","μαι","μώ")):return "verb"
    return "other"

def parse(level):
    source=ROOT/f"vocab_expansion_{level.lower()}.tsv"
    data=[]
    for line_num,line in enumerate(source.read_text('utf-8').splitlines(),1):
        if not line or line.startswith('#'):continue
        parts=line.split('|')
        if len(parts)!=4:raise ValueError(f"{source}:{line_num}: expected 4 fields")
        topic,gr,ru,en=(x.strip() for x in parts)
        if topic not in A1_GOALS:raise ValueError(f"Unknown topic {topic}")
        if not gr or not ru or not en:raise ValueError(f"Empty value {source}:{line_num}")
        if not re.search('[\u0370-\u03ff\u1f00-\u1fff]',gr):raise ValueError(f"No Greek in {gr}")
        if re.search('[\u0370-\u03ff\u1f00-\u1fff]',ru):raise ValueError(f"Greek in Russian gloss {gr}|{ru}")
        if re.search('[\u0400-\u052f]',en):raise ValueError(f"Cyrillic in English gloss {gr}|{en}")
        if len(gr)>56 or len(ru)>96 or len(en)>96:raise ValueError(f"Overlong gloss {gr}")
        data.append(dict(topic=topic,gr=gr,ru=ru,en=en,level=level,line=line_num,kind=category(gr)))
    return data

existing={norm(w["gr"]) for w in vocab.VOCAB if w.get("source")!="original_curated_vocab1700"}
selected=[]
used=set(existing)

def choose(level,targets):
    candidates=collections.defaultdict(list)
    skipped=collections.Counter()
    for x in parse(level):
        gr=x['gr']; k=norm(gr)
        if gr in REJECT or k in used:
            skipped['duplicate_or_reject']+=1
            continue
        # Even common compositional phrases should not inflate the unique *word* count.
        # Noun headwords with articles and a single lexical word count; all headwords
        # in A2 must be one lexical token after article.
        tokens=k.split()
        if level=='A2' and len(tokens)!=1:
            skipped['multiword_a2']+=1
            continue
        if level=='A1' and len(tokens)>2:
            skipped['multiword_a1']+=1
            continue
        if gr.startswith(("ο ","η ","το ","οι ","τα ")) and len(tokens)==1:
            # if no accent in longer Greek polysyllabic word => likely incorrect typography.
            pass
        candidates[x["topic"]].append(x)

    # Pick a varied selection of nouns/verbs/other, spreading across file rather
    # than only first entries. Stable digest shuffle avoids edits changing old IDs.
    for topic,goal in targets.items():
        bykind=collections.defaultdict(list)
        for item in candidates[topic]:
            bykind[item['kind']].append(item)
        for kind,items in bykind.items():
            items.sort(key=lambda x:hashlib.sha256((x["gr"]+"lexi-qa-v1").encode('utf-8')).digest())
        # Mildly prefer verbs/adjectives alongside nouns in the everyday group.
        cycle=('noun','verb','noun','other') if topic=='everyday' else ('noun','noun','verb','other')
        chosen=[]
        used_local=set()
        while len(chosen)<goal:
            before=len(chosen)
            for kind in cycle:
                for x in bykind[kind]:
                    if norm(x['gr']) in used or norm(x['gr']) in used_local:continue
                    chosen.append(x);used_local.add(norm(x['gr']))
                    break
                if len(chosen)>=goal:break
            if len(chosen)==before:
                raise ValueError(f"Insufficient {level}:{topic}: found {len(chosen)}/{goal}, "+str({k:len(v) for k,v in bykind.items()}))
        for x in chosen:
            selected.append(x)
            used.add(norm(x['gr']))
    return skipped

print('A1 source',len(parse('A1')),'A2 source',len(parse('A2')))
print('filtered',choose('A1',A1_GOALS))
print('filtered',choose('A2',A2_GOALS))
assert len(selected)==872
assert len({norm(x['gr']) for x in selected})==872
counts=collections.Counter(x['level'] for x in selected)
print('selected additional',counts)
out=ROOT/'vocab_curated_1700.tsv'
out.write_text("# topic|level|Greek|Russian|English. Original manually authored Greek learner headwords.\n"+
    "".join("|".join((x["topic"],x["level"],x["gr"],x["ru"],x["en"]))+"\n" for x in selected),encoding='utf-8')
print('wrote',out,len(out.read_text().splitlines())-1,'items',out.stat().st_size,'bytes')
for level in ['A1','A2']:
    print(level,dict(collections.Counter(x['topic'] for x in selected if x['level']==level)))
