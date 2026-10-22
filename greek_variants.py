"""Reviewed lexical Greek surface-form variants for actual teaching targets.

Curated variants, not free fuzzy equivalence. Base spelling from printed book
remains canonical. Alternatives are equivalent only in the identified senses.
Primary source: Greek Ministry of Education numeral grammar and Triantafyllidis
Dictionary of Standard Modern Greek (Κέντρο Ελληνικής Γλώσσας).
Both are correct; forms with φτ/χτ and αδερφ- are typically more colloquial.
"""
import re
# Dictionary: inflected forms only where the morphological alternation is safe.
PAIRS=(
 ("δύο","δυο"),("μία","μια"),
 ("επτά","εφτά"),("οκτώ","οχτώ"),("εννέα","εννιά"),
 ("ένδεκα","έντεκα"),("δεκαέξι","δεκάξι"),
 ("δεκαεπτά","δεκαεφτά"),("δεκαοκτώ","δεκαοχτώ"),
 ("δεκαεννέα","δεκαεννιά"),
 ("αδελφός","αδερφός"),("αδελφό","αδερφό"),
 ("αδελφού","αδερφού"),("αδελφοί","αδερφοί"),
 ("αδελφούς","αδερφούς"),("αδελφών","αδερφών"),
 ("αδελφή","αδερφή"),("αδελφής","αδερφής"),
 ("αδελφές","αδερφές"),("αδελφών","αδερφών"),
 ("αδέλφια","αδέρφια"),
)
LOOKUP={}
for a,b in PAIRS:
 assert a not in LOOKUP or LOOKUP[a]==b
 LOOKUP[a]=b;LOOKUP[b]=a
P=re.compile(r"(?<!\w)(?:"+"|".join(sorted(map(re.escape,LOOKUP),key=len,reverse=True))+r")(?!\w)",re.I)
def variants(text):
    """One alternate form with preserved Greek context/article and accent.

    Also works inside phrases; doesn't change unrelated spellings like
    επτακόσια or αδελφικός, and never normalizes away cases or articles.
    """
    if not isinstance(text,str):return []
    def repl(m):
        t=m.group(0);target=LOOKUP.get(t.lower())
        if target is None:return t
        if t.isupper():return target.upper()
        if t[0].isupper():return target[0].upper()+target[1:]
        return target
    alternative=P.sub(repl,text)
    return [alternative] if alternative!=text else []
def accepted(text):
    return [text]+variants(text)
