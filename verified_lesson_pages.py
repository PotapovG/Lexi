"""Small visual-evidence register for beginner headwords in the owner's PDF.

These are pedagogical *worked example / visible usage* locations, not
claims of first-ever appearance or publisher exercise copying. No PDF bytes,
screenshots or excerpts are deployed. Only IDs and printed page anchors.
"""
PAGE_HEADWORDS={
    # Printed p15: introductory greetings in speech/example panels.
    15:[1,2],
    # Printed p19: greetings/name/introductions example panels.
    19:[3,7,21,22,31,32],
    # Printed p25: introductory μένω example and conjugation in dialogue.
    25:[49,50],
    # Printed p34: telephone, possessives, and present έχω examples.
    34:[44,45,55,56,70,71,72,73,74,75,76],
    # Printed p40: actually worked examples for question pronouns, family,
    # "τον/τη λένε", marital adjectives; p38 is only chapter outline.
    40:[23,24,25,33,34,87,88,89,90,91,92,95,96,112,113,116,117],
    # Printed p49: present B1 conjugation table and understanding lines.
    49:[137,138,139,140,141,142,146,149,150,151],
    # Printed p50: language and nationality vocabulary/usage table.
    50:[129,130,131,132,133,135,153,154,155,156],
}
MANUAL_EVIDENCE={
    15:'greeting speech/example panel',
    19:'introduction dialogue and phrase comparison',
    25:'residence dialogue and model utterances',
    34:'telephone grammar panel and possessive table',
    40:'question pronoun/family/marital status worked examples',
    49:'verb B1 conjugation and comprehension dialogue',
    50:'language/nationality vocabulary model table',
}
PAGES_BY_ID={f'w{n:03d}':page for page,nums in PAGE_HEADWORDS.items() for n in nums}
assert len(PAGES_BY_ID)==sum(map(len,PAGE_HEADWORDS.values()))==58

def apply(cards):
    byid={c['id']:c for c in cards}
    modified=[]
    for cid,page in PAGES_BY_ID.items():
        assert cid in byid,cid
        card=byid[cid]
        assert card['kind'] in ('word','number') and 1<=card['chapter']<=4,(cid,card)
        card['page']=page
        card['source_alignment']='owner_pdf_worked_example_visual'
        card['book_page_verified']=True
        card['book_page_evidence']='worked_usage_or_model_not_first_occurrence'
        modified.append(cid)
        accent=byid.get('stress_'+cid)
        if accent:
            accent['page']=page
            accent['source_alignment']='derived_from_verified_headword'
            accent['book_page_verified']=False
            accent['book_page_evidence']='parent_lemma_verified_not_accent_exercise'
    return modified
