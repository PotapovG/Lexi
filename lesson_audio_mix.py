"""Insert approved Pocket listening cards into regular page/chapter lessons.

Never mix into explicit listening mode, topic/verb drills, or dedicated weak
and SRS sessions. Keep the original 717 canonical listening IDs, chapters
and source word/phrase/sentence selections. Replacing ~1 in 5 slots
prevents shortening or silently extending a lesson.
"""
import random

def candidates(cards,kinds,chapters,first,last,excluded=None):
    selected={'word','phrase','sentence'} & set(kinds)
    if not selected:return []
    excluded=excluded or set()
    return [c for c in cards if c['sourceKind'] in selected
            and (c['chapter'] in chapters if chapters is not None else first<=c['page']<=last)
            and c['id'] not in excluded and c.get('semanticId') not in excluded]

def mix(questions,options,card_lookup,question_factory,lang):
    """Replace 20 percent of answer slots only after successful formatting."""
    if not questions or not options:return 0
    positions=list(range(4,len(questions),5))
    if not positions:return 0
    protected_ids={q['id'] for i,q in enumerate(questions) if i not in positions}
    protected_sem={q['semanticId'] for i,q in enumerate(questions) if i not in positions}
    options=list(options)
    random.shuffle(options)
    count=0
    for pos in positions:
        for idx,c in enumerate(options):
            if c['sourceId'] in protected_ids:continue
            original=card_lookup(c['sourceId'])
            if original is None:continue
            original_sem=original.get('semanticId',original['id'])
            if original_sem in protected_sem:continue
            try:q=question_factory(c,'listen',lang)
            except (KeyError,ValueError,IndexError):continue
            questions[pos]=q
            protected_sem.add(original_sem)
            protected_ids.add(c['sourceId'])
            options.pop(idx)
            count+=1
            break
    return count
