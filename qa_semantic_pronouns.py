"""No semantic headword collisions for Greek pronoun+verb and gendered spouse."""
import catalog_v2,server
from pedagogy_rules import canonical_greek
v=catalog_v2.BY_ID
assert canonical_greek('τον λένε')=='τον λένε'
assert canonical_greek('τη λένε')=='τη λένε'
assert canonical_greek('το λένε')=='το λένε'
assert canonical_greek('την λένε')=='την λένε'
assert canonical_greek('ο υπάλληλος')==canonical_greek('υπάλληλος')
assert canonical_greek('η Λευκωσία')==canonical_greek('Λευκωσία')
for left,right in [('w033','w034'),('w093','w094')]:
    assert v[left]['semanticId']!=v[right]['semanticId'],(left,right)
    assert v[left]['gr']!=v[right]['gr']
assert v['w033']['semanticId']!=v['stress_w033']['semanticId']
params={'scope':['pages'],'from':['40'],'to':['40'],'types':['word'],'lang':['ru'],'count':['60']}
quiz=server.make_quiz('student-semantic',params)
ids={q['id'] for q in quiz['questions']}
assert {'w033','w034'}<=ids,(ids,quiz['available'])
assert len({q['semanticId'] for q in quiz['questions']})==len(quiz['questions'])
assert v['w033']['chapter']==3 and v['w034']['chapter']==3
print('PASS distinct grammatical semantic IDs, both τον/τη λένε selectable in the same lesson, ordinary article dedup unchanged')
