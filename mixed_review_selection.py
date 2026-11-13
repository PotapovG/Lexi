"""Keep the 5 steps of one eligible A1 scenario together in existing quizzes.

Only for a normal (non-weak) grammar-inclusive textbook session. The entire
eligible five-card block is rendered in authored step order; the remaining
ordinary question slots still use the existing score/random/clock balance.
Never take a partial scenario or override a learner's selected chapter/page
gate. For weak/SRS review, individual failed cards remain independently due.
"""
import random

def select_block(choices,count,rng=None):
    """Return (linked_block, ordinary_pool) from prefiltered choices.

    Each input is a (card,direction,score) tuple already lesson-gated,
    excluded/semantic deduped and ranked by the ordinary quiz code.
    """
    if count<5:return [],choices
    groups={}
    for entry in choices:
        card=entry[0]
        if card.get("group")=="review_scenario":
            groups.setdefault(card["scenarioId"],[]).append(entry)
    candidates=[]
    for sid,rows in groups.items():
        if len(rows)!=5:continue
        seq=sorted(rows,key=lambda item:item[0]["scenarioStep"])
        if [item[0]["scenarioStep"] for item in seq]!=[1,2,3,4,5]:continue
        if len({item[0]["chapter"] for item in seq})!=1:continue
        candidates.append(seq)
    if not candidates:return [],choices
    rng=rng or random
    # Shuffle equal-priority scenarios so a learner does not keep receiving the
    # same sequence when earlier mistakes or completion are already recorded.
    rng.shuffle(candidates)
    candidates.sort(key=lambda sequence:-sum(item[2] for item in sequence))
    chosen=candidates[0]
    remainder=[item for item in choices if item[0].get("group")!="review_scenario"]
    return chosen,remainder
