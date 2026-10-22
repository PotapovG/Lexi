"""74 independently authored additional textbook-context exercises.

Motivation and printed-page tags are anchored in the user's purchased PDF
contents, p14–56 conversations, noun/article/adjective pp94–121, aorist
pp150–165, job commands pp232–245 and doctor/conditionals pp246–261.
The source PDF is NOT included or served. Page tags are curricular anchors.
"""
from pathlib import Path
import json

ROOT=Path(__file__).parent
GLOSS=json.loads((ROOT/'patakis_context_locales.json').read_text(encoding='utf-8'))
# Transparent, repeatable bilingual-sense edits. The machine-assisted bulk
# output remains a candidate source, not certified professional translation.
for english,translations in json.loads((ROOT/'patakis_context_manual.json').read_text(encoding='utf-8')).items():
    for lang,value in translations.items():
        if english not in GLOSS[lang]:raise ValueError(f"Unknown manual entry {english} / {lang}")
        GLOSS[lang][english]=value

CARDS=[]
COUNTS={}
for line in (ROOT/'patakis_context_original.tsv').read_text(encoding='utf-8').splitlines():
    if not line or line.startswith('#'):continue
    fields=line.split('|')
    assert len(fields)==6,fields
    chapter,page,kind,greek,ru,en=fields
    chapter,page=int(chapter),int(page)
    assert kind in ('word','phrase','sentence')
    assert all(item.strip() for item in fields)
    index=COUNTS.get(chapter,0)+1
    COUNTS[chapter]=index
    item=dict(id=f"patk{chapter:02d}_{index:03d}",chapter=chapter,unit=chapter,page=page,
              kind=kind,topic="Ελληνικά Α΄ · Ενότητα "+str(chapter),
              gr=greek,ru=ru,en=en,source="original-from-book-syllabus",
              source_alignment="pdf-toc-topic-approximate",curriculum="textbook")
    for lang in ('zh','ar','es','pt'):
        item[lang]=GLOSS[lang][en]
        if not item[lang].strip():raise ValueError(f"Missing {lang} translation for "+greek)
    CARDS.append(item)

assert len(CARDS)==74 and len({x['id'] for x in CARDS})==74
