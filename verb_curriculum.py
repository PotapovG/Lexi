"""Conservative editorial milestones for separate present-tense conjugation mode.

Derived from printed Greek Α΄ 20-unit syllabus and vetted early pp 14–58:
μένω unit 2, δουλεύω unit 3, γράφω/διαβάζω/μιλάω/απαντάω unit 4.
Other items are pedagogical *gates*, not claims of verbatim first appearance
on a precise publisher page. Users can choose later units up to 20.
"""
FIRST_UNIT={
 'μένω':2,
 'δουλεύω':3,
 'γράφω':4,'διαβάζω':4,'μιλάω':4,'ρωτάω':4,'απαντάω':4,
 'οδηγώ':6,'μαθαίνω':7,'τηλεφωνώ':7,
 'αγοράζω':8,
 'αγαπάω':16,'παίζω':16,'περπατάω':16,'μπορώ':16,
 'χρησιμοποιώ':17,'θεωρώ':19,
}
assert len(FIRST_UNIT)==17
DEFAULT_UNIT=4

def first_unit(lemma):
    return FIRST_UNIT[lemma]

def selected_max(raw):
    try:return max(1,min(20,int(raw)))
    except (ValueError,TypeError):return DEFAULT_UNIT
