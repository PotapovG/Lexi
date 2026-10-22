"""Independent taught-word Greek syllable / stress-location exercises.

Unlike the original 549 accent cards which ask for the TONOS LETTER,
these questions ask which *syllable* carries stress. Partition boundaries
are explicitly curated, not machine-hyphenated; original 1795 cards,
source certification and 717 listening items are never mutated.
"""
import unicodedata
from catalog_v2 import ALL as CORE_CARDS
import pedagogy_rules

# Original source syllable partitions, retained accents show the correct
# stressed syllable. All examples also exist in original accent-card corpus.
_SEGMENTED=(
 "κα-φές","σπί-τι","νε-ρό","άν-θρω-πος","κα-λη-μέ-ρα","ευ-χα-ρι-στώ",
 "τη-λέ-φω-νο","δου-λειά","πα-ρά-θυ-ρο","λε-ω-φο-ρεί-ο",
 "α-ε-ρο-δρό-μι-ο","μου-σι-κή","βι-βλί-ο","δα-σκά-λα",
 "πα-τέ-ρας","μη-τέ-ρα","α-δελ-φός","γυ-ναί-κα",
 "παι-δί","σχο-λεί-ο","φοι-τη-τής","φί-λος",
 "α-γο-ρά","ε-βδο-μά-δα","με-ση-μέ-ρι","ελ-λη-νι-κά",
 "σή-με-ρα","αύ-ρι-ο","νο-σο-κο-μεί-ο","κα-τά-στη-μα",
 "πορ-το-κά-λι","Λευ-κω-σί-α","Α-θή-να","συγ-γνώ-μη","πρό-γραμ-μα",
)
def _plain(word):
    return ''.join(ch for ch in unicodedata.normalize('NFD',word) if ch!='\u0301')
def syllable(word):
    return any('\u0301' in unicodedata.normalize('NFD',ch) for ch in word)
sources={}
for card in CORE_CARDS:
    if card["kind"]=="accent" and card["chapter"]>0:
        gr=card["accented"]
        if gr not in sources or (card["chapter"],card["page"])<(sources[gr]["chapter"],sources[gr]["page"]):
            sources[gr]=card
CARDS=[]
for i,row in enumerate(_SEGMENTED,1):
    parts=row.split('-');greek=''.join(parts)
    original=sources.get(greek)
    assert original,(i,greek)
    assert 2<=len(parts)<=6,(i,row)
    stressed=[j for j,p in enumerate(parts) if syllable(p)]
    assert len(stressed)==1,(i,row,stressed)
    unaccented=[_plain(p) for p in parts]
    assert ''.join(unaccented)==original['base'],(i,row,original['base'])
    assert sum(map(len,parts))==len(greek)
    item=dict(id=f"sy261021_{i:03d}",kind="syllable",
        chapter=original["chapter"],unit=original["unit"],page=original["page"],
        gr=greek,base=original["base"],parts=parts,plainParts=unaccented,
        stressedIndex=stressed[0],syllableCount=len(parts),
        source="independent_syllable_practice_20261021",
        source_parent_id=original["id"],
        book_page_verified=False,
        topic="Τονισμός · συλλαβές",grammar_tags=['stress_syllables'],
        ru="Укажи ударный слог.",en="Select the stressed syllable.",
        zh="请选择重读音节。",ar="اختر المقطع المشدد.",
        es="Elige la sílaba tónica.",pt="Escolhe a sílaba tónica.")
    pedagogy_rules.tag(item)
    CARDS.append(item)
BY_ID={c['id']:c for c in CARDS}
assert len(CARDS)==len(_SEGMENTED)==35 and len(BY_ID)==35
