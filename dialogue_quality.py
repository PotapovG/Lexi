"""Editorially reviewed A1/A2 Greek dialogue choices (original authored content).

Rebuild only option banks, never original correct answers, identifiers or
historic scoring directions. Examples use grammar known by the source unit,
avoid later-unit vocabulary as implausible distractors and aim at a distinct
dialogue context. This is manually scoped, not an arbitrary all-language fuzzy
scorer.
"""
import re

# Carefully selected stage-safe distractors for formerly early-stage exercises.
# Each string must be distinct and fail to answer ANY gap in its specific item.
EARLY={
'dlg001':["Πώς σε λένε;","Από πού είσαι;","Είσαι η Μαρία;","Είσαι ο Νίκος;","Με λένε Κώστα","Από 'δώ η Άννα"],
'dlg002':["Από πού είσαι","Πώς σε λένε","Πού μένεις","Έχεις τηλέφωνο","Με λένε Νίκο","Είμαι από την Κύπρο"],
'dlg003':["Πώς σε λένε","Από πού είσαι","Έχεις τηλέφωνο","Τι κάνεις","Με λένε Πέτρο","Είμαι από την Ελλάδα"],
'dlg004':["Πώς σε λένε;","Πού μένεις;","Τι δουλειά κάνεις;","Ποια είναι αυτή;","Έχω ένα τηλέφωνο","Είμαι ο Πέτρος"],
'dlg021':["Από πού είσαι","Είσαι ο Νίκος","Είσαι από την Ελλάδα","Καλημέρα","Χαίρω πολύ","Είμαι από την Κύπρο"],
'dlg025':["Πώς σε λένε","Από πού είσαι","Είσαι η Μαρία","Με λένε Κώστα","Είμαι από την Ελλάδα","Όχι, δεν είμαι","Ναι, είμαι"],
'dlg026':["Πώς σε λένε","Από πού είσαι","Είμαι από την Ελλάδα","Με λένε Μαρία","Έχω τηλέφωνο","Η μητέρα μου είναι δασκάλα","Πού μένεις"],
'dlg027':["Πώς σε λένε;","Τι δουλειά κάνεις;","Ποιος είναι αυτός;","Έχω ένα τηλέφωνο","Η μητέρα μου είναι δασκάλα","Είμαι μηχανικός"],
'dlg028':["Πώς σε λένε;","Από πού είσαι;","Τι κάνεις;","Έχεις τηλέφωνο;","Το τηλέφωνό μου είναι εδώ","Με λένε Νίκο"],
'dlg029':["Πώς σε λένε","Από πού είσαι","Τι κάνεις","Η μητέρα μου είναι δασκάλα","Είμαι από την Κύπρο","Έχω τηλέφωνο","Το τηλέφωνο είναι εδώ"],
'dlg030':["Πώς σε λένε","Έχεις τηλέφωνο","Πού μένεις","Ποιος είναι αυτός","Το τηλέφωνο είναι εδώ","Έχω δύο αδελφούς"],
'dlg031':["Πού μένεις;","Πώς σε λένε;","Πόσα παιδιά έχεις;","Τι δουλειά κάνεις;","Έχω ένα τηλέφωνο","Είμαι από την Κύπρο"],
'dlg032':["Από πού είσαι;","Πώς σε λένε;","Τι δουλειά κάνεις;","Η μητέρα μου είναι δασκάλα","Ο πατέρας μου είναι οδηγός","Είμαι από την Ελλάδα"],
'dlg033':["Πού μένεις;","Από πού είσαι;","Πώς σε λένε;","Έχω ένα τηλέφωνο","Ο αδελφός μου είναι παντρεμένος","Μένω στην Κύπρο"],
'dlg034':["Πού μένεις;","Από πού είσαι;","Έχεις τηλέφωνο;","Ο πατέρας μου είναι οδηγός","Είμαι από την Ελλάδα","Με λένε Νίκο"],
'dlg035':["Πού μένεις;","Τι δουλειά κάνεις;","Από πού είσαι;","Πώς σε λένε;","Η μητέρα μου είναι δασκάλα","Έχω ένα τηλέφωνο","Είμαι από την Ελλάδα"],
}

# Unit 6–9 distractors are restricted to vocabulary/grammar known no later
# than that unit. Their meaning is out of context with the actual replies.
LATER_POOL=[
 "Με λένε Πέτρο","Είμαι από την Ελλάδα","Μιλάω αγγλικά",
 "Η μητέρα μου είναι δασκάλα","Μένω στη Λάρνακα",
 "Έχω έναν αδελφό","Έχω ένα τηλέφωνο","Ο Νίκος είναι φίλος μου",
 "Πώς σε λένε;","Από πού είσαι;","Τι δουλειά κάνεις;",
 "Έχεις τηλέφωνο;","Πού μένεις;","Ποιος είναι αυτός;",
 "Μιλάς ελληνικά;","Πού είναι η Άννα;",
]
# Group IDs that originally appeared with later grammar in distractors.
LATER_IDS={
'dlg010','dlg011','dlg012','dlg014',
'dlg022','dlg041','dlg042','dlg043','dlg046','dlg047','dlg048','dlg049','dlg050',
'dlg052','dlg053','dlg056','dlg057','dlg058','dlg059'
}
# Specific candidates may be an alternate correct answer in some contexts.
# Filter them from the independent A1 pool on a per-dialogue basis.
BLOCKED={
'dlg014':{"Με λένε Πέτρο"},
'dlg041':{"Μένω στη Λάρνακα"},
'dlg042':{"Μένω στη Λάρνακα"},
'dlg043':{"Πού μένεις;"},
'dlg047':{"Μένω στη Λάρνακα"},
'dlg049':{"Πού είναι η Άννα;"},
'dlg056':{"Πού μένεις;"},
'dlg058':{"Έχω έναν αδελφό"},
}

def apply(cards):
    edited=[]
    for card in cards:
        cid=card['id']
        if card['kind']!='dialogue' or cid not in EARLY and cid not in LATER_IDS:
            continue
        correct=list(card['gaps'])
        if cid in EARLY:
            wrong=list(EARLY[cid])
        else:
            # Preserve only stage-verified original off-topic items for earlier
            # already-graded cards; the remaining options come from safe pool.
            wrong=[]
            seen=set(correct)|BLOCKED.get(cid,set())
            for candidate in LATER_POOL:
                if candidate in seen:continue
                wrong.append(candidate)
                if len(wrong)==8-len(correct):break
        assert len(wrong)>=8-len(correct),(cid,len(wrong))
        bank=correct+wrong[:8-len(correct)]
        assert len(bank)==len(set(bank))==8,(cid,bank)
        assert all(x for x in bank),(cid,bank)
        card['bank']=bank
        card['bank_source']='curated-stage-safe-20261020'
        edited.append(cid)
    assert len(edited)==len(EARLY)+len(LATER_IDS),(len(edited),len(EARLY),len(LATER_IDS))
    return edited
