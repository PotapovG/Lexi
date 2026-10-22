"""Alignment to the 314-page *user-supplied* Patakis Ελληνικά Α΄ PDF.

The PDF has printed book pages 1–312; its page index is printed_page + 2.
Verified against the printed contents on PDF pages 6–9, as well as lesson
openings and exemplars (pp 14–56, 66, 80, 94, 108, 132, 150, 166, etc.).
NO book text, scans or copyrighted exercise pages are served or bundled.

Existing practice content is independently authored. The original app labels
its 16 teaching units 1–16, whereas the PRINTED book has 20 sections, with
revision at 5/10/15/20. This module maps OLD app chapters to PRINTED units
without changing a single existing question ID, answer, or account progress.

A card's page is an approximate pedagogical anchor within the verified
printed unit, not a claim that its exact wording occurs on that page.
"""
from collections import Counter

PRINTED_UNITS = [
    (1, 14,23,"Γεια σας","Hello","Γνωριμίες · χαιρετισμοί · είμαι · 1–10"),
    (2, 24,37,"Πού μένεις;","Where do you live?","Χαιρετισμοί · διεύθυνση · τηλέφωνο · μένω, έχω, κάνω · 10–100"),
    (3, 38,47,"Τι δουλειά κάνεις;","What do you do?","Οικογένεια · επαγγέλματα · οικογενειακή κατάσταση · ποιος"),
    (4, 48,58,"Μιλάς ελληνικά;","Do you speak Greek?","Εθνικότητες · γλώσσες · μιλάω · ξέρω · 100–1000"),
    (5, 59,65,"Πάμε πάλι!","Review 1–4","Επανάληψη και τεστ · ενότητες 1–4"),
    (6, 66,79,"Πού πάτε;","Where are you going?","Μετακινήσεις · ώρα · προθέσεις · πάω"),
    (7, 80,93,"Ποτέ την Κυριακή","Never on Sunday","Καθημερινή ρουτίνα · καιρός · ημέρες · μήνες · τρώω, λέω, ακούω"),
    (8, 94,107,"Πόσο κάνουν όλα;","How much is everything?","Καθημερινές αγορές · οριστικό/αόριστο άρθρο · πληθυντικός"),
    (9, 108,121,"Πάμε για ψώνια;","Shall we go shopping?","Αγορές σε καταστήματα · χρώματα · επίθετα · έρχομαι, χρειάζομαι"),
    (10,122,131,"Πάμε πάλι!","Review 6–9","Επανάληψη και τεστ · ενότητες 6–9"),
    (11,132,149,"Ψάχνω για σπίτι","Looking for a home","Κατοικία · ενοίκιο · οδηγίες · γενική · συγκριτικός"),
    (12,150,165,"Πού ήσουν;","Where were you?","Εκδρομές · ταξίδια · αφήγηση · αόριστος"),
    (13,166,183,"Είναι μεγάλη ιστορία","It's a long story","Ιστορίες ζωής · ευχές · αόριστος"),
    (14,184,199,"Τι θα κάνουμε;","What shall we do?","Ταβέρνα · σχέδια · φαγητό · απλός μέλλοντας"),
    (15,200,211,"Πάμε πάλι!","Review 11–14","Επανάληψη και τεστ · ενότητες 11–14"),
    (16,212,231,"Πάμε βόλτα;","Shall we go out?","Ψυχαγωγία · διακοπές · απλή υποτακτική"),
    (17,232,245,"Βρήκες δουλειά;","Did you find a job?","Εργασία · αγγελίες · βιογραφικό · προστακτική"),
    (18,246,261,"Δεν αισθάνομαι καλά","I don't feel well","Στον γιατρό · συμπτώματα · θεραπεία · υποθετικές προτάσεις"),
    (19,262,277,"Περιμένετε στην ουρά, παρακαλώ!","Please wait in line!","Δημόσιες υπηρεσίες · τράπεζα · ταχυδρομείο"),
    (20,278,289,"Πάμε πάλι!","Review 16–19","Επανάληψη και τεστ · ενότητες 16–19"),
]
REVIEW_IDS={5,10,15,20}
# Published original questions are organized in a 16-unit *teaching* sequence.
LEGACY_TO_PRINTED={
    0:0, 1:1,2:2,3:3,4:4,
    5:6,6:7,7:8,8:9,
    9:11,10:12,11:13,12:14,
    13:16,14:17,15:18,16:19,
    -1:5,-2:10,-3:15,-4:20,-5:-5,
}
CHAPTERS=[
    dict(id=0,start=8,end=13,title="Από το Α στο Ω",en="Greek alphabet",
         focus="Εισαγωγή · αλφάβητο",review=False,reference="printed-contents"),
    *[dict(id=u,start=start,end=end,title=title,en=en,focus=focus,
           review=u in REVIEW_IDS,reference="printed-contents")
      for u,start,end,title,en,focus in PRINTED_UNITS],
    dict(id=-5,start=290,end=312,title="Παράρτημα",en="Appendix",
         focus="Απαντήσεις και επιπλέον υλικό",review=True,reference="printed-contents"),
]
INDEX={x["id"]:x for x in CHAPTERS}
assert [x["start"] for x in CHAPTERS[1:21]]==[14,24,38,48,59,66,80,94,108,122,132,150,166,184,200,212,232,246,262,278]
assert all(CHAPTERS[i]["end"]+1==CHAPTERS[i+1]["start"] for i in range(20))

# Curatorial moves based on the actual first 56 pages, and practical
# mismatches in previously self-authored dialogues. These are NOT quotations.
# Only the grouping changes: no user progress IDs are rewritten.
CARD_OVERRIDES={
    # Numbers 2–10 and the interrogative pronoun ποιος are introduced in
    # different real units, not in the old app's manually authored lists.
    **{f"w{x:03d}":(1,22) for x in range(118,127)},
    # Verified by reading printed page 39 (PDF page 41): question words
    # ποιος/ποια and "τον λένε / τη λένε" are actually taught there.
    # Chapter outline p38; worked question/λένε examples are on p40.
    **{f"w{x:03d}":(3,40) for x in (23,24,33,34)},
    "w025":(3,40), # ποιο worked example also printed p40
    "p008":(2,26),"p009":(2,26),"p010":(2,26),
    "s004":(3,40),"s005":(3,41),"s006":(3,42),
    "s007":(3,44),"s008":(3,46), # family/professions only after unit 3
    "s003":(4,51), # talking languages (μιλάω) comes in unit 4
    # Some original dialogues were authored to a convenient themed "unit",
    # not the corresponding real textbook grammar/theme.
    "dlg002":(2,26), # how are you: greeting/condition in lesson 2
    "dlg004":(3,40), # ποιος interrogative first covered in unit 3
    "dlg024":(2,27), # possessive my friend introduced in unit 2
    "dlg037":(16,217),# can you say it again? contains later να-subjunctive
    "dlg005":(11,137),# how old? (πόσων χρονών) taught in printed unit 11, PDF page 139
    "dlg027":(3,42), # ποια interrogative introduced in printed unit 3, not unit 2
    "dlg007":(8,99), # ordering coffee: daily purchases
    "dlg008":(8,101),# buying potatoes: daily purchases
    "dlg009":(11,139),# home contents, not transport
    "dlg011":(6,72), # directions, not shopping
    "dlg012":(6,77), # travel ticket, not clothes
    "dlg013":(14,191),# restaurant, not renting a home
    "dlg014":(7,89), # talking on phone / routine
    "dlg015":(18,252),# pharmacy, not life story
    "dlg016":(18,254),# doctor's appointment
    "dlg017":(16,225),# hotel holiday booking
    "dlg019":(16,219),# holiday planning
    "dlg020":(11,145),# describing a new neighbourhood
    "dlg030":(4,53), # language question belongs to chapter 4
}
# Discourage nouns in plural drills before printed unit 8, where noun
# plural morphology is explicitly introduced (and can be enabled separately).
FIRST_NOUN_PLURALS_UNIT=8

def align(cards):
    """Mutate only catalogue metadata, not exercise text, IDs or answers."""
    moved=Counter()
    by_id={card["id"]:card for card in cards}
    for card in [c for c in cards if c["kind"]!="accent"] + [c for c in cards if c["kind"]=="accent"]:
        if card.get("curriculum") in ("topic","verb","personalized"):continue
        old=card["chapter"]
        if old not in LEGACY_TO_PRINTED:
            # Standalone topic and verb drills use their own curriculum and
            # must NOT be reassigned to a printed book section.
            if card.get("curriculum") in ("topic","verb","personalized"):
                continue
            raise ValueError("Unknown legacy book chapter for "+card["id"]+": "+str(old))
        target=LEGACY_TO_PRINTED[old]
        card["legacy_chapter"]=old
        if card["kind"]=="plural" and 0<target<FIRST_NOUN_PLURALS_UNIT:
            target=FIRST_NOUN_PLURALS_UNIT
        # The old eighth teaching bucket was about groceries, whereas the
        # printed chapter 9 is clothes/colours. Move its grocery prompts to
        # printed chapter 8 (everyday purchases); keep the separate new
        # chapter-9 clothing corpus and independent dialogue scenarios.
        if old==8 and (card["id"].startswith("x08") or card["id"].startswith("xn08")):
            target=8
            card["page"]=max(94,min(107,card["page"]-14))
        # The old tenth bucket teaches simple PRESENT travel logistics,
        # while printed chapter 12 specifically teaches aorist narration.
        # Travel logistics fit printed chapter 16 (holidays/travel) better;
        # past-tense narration is supplied by authored chapter-12 tasks.
        if old==10 and (card["id"].startswith("x10p") or card["id"].startswith("x10s")):
            target=16
            card["page"]=max(212,min(231,card["page"]+65))
        if card["id"] in CARD_OVERRIDES:
            target,newpage=CARD_OVERRIDES[card["id"]]
            card["page"]=newpage
        if card["kind"]=="accent" and card["id"].startswith("stress_"):
            original=by_id.get(card["id"][len("stress_"):])
            if original is not None:
                target=original["chapter"]
                card["page"]=original["page"]
        # Delayed grammar/phrases not yet introduced in the real early pages.
        import pedagogy_rules as _pedagogy
        if card['id'] in _pedagogy.LEXICAL_INTRO_OVERRIDES:
            target=_pedagogy.LEXICAL_INTRO_OVERRIDES[card['id']]
            card['page']=INDEX[target]['start']
        card["chapter"]=target
        card["unit"]=target
        spec=INDEX[target]
        if not(spec["start"]<=card["page"]<=spec["end"]):
            # Approximate page anchors belong inside the actual teaching unit.
            card["page"]=min(spec["end"],max(spec["start"],card["page"]))
        card["source_alignment"]="pdf-toc-topic-approximate"
        if target!=old:moved[(old,target)]+=1
        assert spec["start"]<=card["page"]<=spec["end"],card["id"]
    return moved
