"""Keep new clock cards proportional in ordinary mixed Greek lessons.

A chapter's 144 clock variants should not crowd out vocabulary, cases,
dialogues, and reading. This is an ordinary-session sampling rule, not
a limiter for clock-only study or weak/SRS reviews.
"""
def balance(choices,count):
    if count<=0:return []
    clocks=[x for x in choices if x[0]['kind']=='clock']
    others=[x for x in choices if x[0]['kind']!='clock']
    if not clocks or not others:
        return choices[:count]
    quota=max(1,count//10)  # 10% of a standard 10- or 60-card batch
    take_clock=min(quota,len(clocks),count)
    take_other=min(len(others),count-take_clock)
    # If other material is exhausted, fill the session with available clocks
    # rather than shortening the learner's scheduled session.
    if take_other+take_clock<count:
        take_clock=min(len(clocks),count-take_other)
    total=take_clock+take_other
    if not take_clock:return others[:count]
    positions={round((i+1)*total/(take_clock+1))-1 for i in range(take_clock)}
    # At most one clock per position: enough distance because quota<=count.
    assert len(positions)==take_clock,(total,take_clock)
    it_clock=iter(clocks[:take_clock])
    it_other=iter(others[:take_other])
    result=[next(it_clock) if i in positions else next(it_other) for i in range(total)]
    assert len(result)==total
    return result
