"""Conservative chapter-level readiness gate for independently authored drills.

Never modify original card IDs, stored progress, or printed PDF/page claims.
Stages are curriculum introduction estimates, not attestations of when a
publisher first used a form. Explicit weak/SRS can always review learned work.
"""
import re

# Rule matches constrained to teachable constructions. Bare να appears in
# idiomatic phrases before the full subjunctive unit: don't gate all να.
_RULES=(
  ("comparative",11,re.compile(r'\b(?:πιο\s+(?:μεγάλος|μεγάλη|μεγάλο|γρήγορος|γρήγορη|γρήγορο|ακριβός|ακριβή|ακριβό|ήσυχος|ήσυχη|ήσυχο)|μεγαλύτερ\w*|μικρότερ\w*)\b',re.I)),
  ("past",12,re.compile(r'\b(?:χθες|πήγα|πήγαμε|πήγες|ήρθα|ήρθες|είδα|είδαμε|φάγαμε|έφαγα|ήμουν)\b',re.I)),
  ("future",14,re.compile(r'\bθα\b',re.I)),
  ("subjunctive",16,re.compile(r'\b(?:μπορείς\s+να|θέλω\s+να|θέλεις\s+να|πρέπει\s+να|για\s+να)\b',re.I)),
  ("conditional",18,re.compile(r'\bαν\s+(?:έχεις|νιώθεις|χρειάζεσαι|κάνει|είσαι|είναι|θέλεις)\b',re.I)),
)
def milestone(card):
    value=max(0,int(card.get('curriculum_ready_unit',card.get('chapter',0))))
    if card['kind'] not in ('phrase','sentence','dialogue','order'):
        return value
    greek=' '.join(card.get('lines',[])) if card['kind']=='dialogue' else card.get('gr','')
    for _,required,pattern in _RULES:
        if pattern.search(greek): value=max(value,required)
    # Adjective agreement with marked demonstratives, not every adjective:
    if card['kind'] in ('sentence','phrase','order') and re.search(
        r'\b(?:αυτό\s+το|εκείνο\s+το|αυτή\s+η)\s+\w+\s+είναι\b',greek,re.I):
        value=max(value,9)
    return value
def max_taught_unit(chapters,first_page,last_page,sections):
    if chapters is not None:
        return max((x for x in chapters if x>0),default=0)
    return max((x['id'] for x in sections if x['id']>0 and x['start']<=last_page),default=0)
def filter_ready(cards,max_unit):
    ready=[c for c in cards if milestone(c)<=max_unit or c.get('chapter',0)<=0]
    return ready,len(cards)-len(ready)
