"""Version one ambiguous authored dialogue WITHOUT rewriting its history.

Published quiz switches one active item to a new stable ID. Legacy ID
remains addressable for weak debts, scheduled reviews, grading and analytics.
Neither copyrighted exercise text nor licensed PDF is involved.
"""
def version(cards):
    matches=[i for i,c in enumerate(cards) if c['id']=='dlg024' and c['kind']=='dialogue']
    assert len(matches)==1,matches
    i=matches[0]
    old=cards[i]
    assert old['gaps']==['Χαίρω πολύ','χαίρω πολύ']
    assert old['chapter']==2
    archived={'dlg024':old}
    lines=[
      'Α: Αυτή είναι η φίλη μου η Μαρία.',
      'Β: [[0]], Μαρία!',
      'Γ: Κι εγώ χαίρω πολύ, Γιώργο.',
      'Β: [[1]], Μαρία;',
      'Γ: Μένω στη Λευκωσία.',
    ]
    answers=['Χαίρω πολύ','Πού μένεις']
    wrong=['Πώς σε λένε','Με λένε Νίκο','Είμαι από την Ελλάδα',
           'Έχω ένα τηλέφωνο','Το τηλέφωνο είναι εδώ','Από πού είσαι']
    assert len(answers+wrong)==len(set(answers+wrong))==8
    updated=dict(old)
    updated.update(id='dlg024_v2',gr=' '.join(lines),lines=lines,
                   gaps=answers,bank=answers+wrong,
                   topic='Γνωριμία και διεύθυνση',
                   page=27,chapter=2,unit=2,
                   bank_source='authored-dialogue-v2-20261020',
                   replaces='dlg024',
                   curriculum_ready_unit=2)
    import pedagogy_rules as rules
    rules.tag(updated)
    cards[i]=updated
    return archived

def assert_archive(card):
    assert card['id']=='dlg024'
    assert card['gaps']==['Χαίρω πολύ','χαίρω πολύ']
