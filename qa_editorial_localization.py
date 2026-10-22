"""Skill-guided, deterministic locale quality gate without native-proofread claims."""
from collections import Counter
from pathlib import Path
import tempfile
import re
import server,catalog_v2,editorial_localization as audit,accepted_glosses

changes=catalog_v2.REVIEWED_LOCALIZATION_EDITS+server.REVIEWED_ARABIC_EDITS
assert len(changes)==len(audit.REVIEWED)==25
assert Counter(c['lang'] for c in changes)=={'es':12,'pt':8,'ar':4,'zh':1},Counter(c['lang'] for c in changes)
assert len(server.ALL)==1795 and len(catalog_v2.BY_ID)==1796
assert len({c['id'] for c in server.ALL})==1795
assert all(c['greek']==server.BY_ID[c['card']]['gr'] for c in changes)
assert all(server.BY_ID[c['card']][c['lang']]==c['after'] for c in changes)
assert all(c['status']=='AI_editor_reviewed_not_native_verified' for c in changes)
for cid in ('w003','w006','w010','w022','w023','w024','w025'):
    raw=server.BY_ID[cid]['es']
    assert re.search('[áéíóú]',raw),(cid,raw)
assert 'usted' in server.BY_ID['p002']['es'] and 'te llamas' in server.BY_ID['p001']['es']
assert 'tu ' in server.BY_ID['w014']['pt'] and 'te chamas' in server.BY_ID['p001']['pt']
assert 'se chama' in server.BY_ID['p002']['pt']
assert '您' in server.BY_ID['p002']['zh']
assert server.BY_ID['w093']['ar'].startswith('الزوج (')
assert server.BY_ID['w094']['ar'].startswith('الزوجة (')
assert server.BY_ID['p002']['gr']=='Πώς σας λένε;'
assert server.BY_ID['p001']['gr']=='Πώς σε λένε;'
assert server.BY_ID['w033']['semanticId']!=server.BY_ID['w034']['semanticId']

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'edittest.sqlite3')
    server.init_db()
    for change in changes:
        cid,lang=change['card'],change['lang']
        c=server.BY_ID[cid]
        q=server.format_question(c,'gr-ru',lang)
        assert change['after'] in q['choices'],(cid,lang,'new gloss missing from 8 choices',q['choices'])
        assert len(set(q['choices']))==8,(cid,lang)
        answer=server.mark('user-'+lang,{'id':cid,'direction':'gr-ru',
              'selected':change['after'],'lang':lang})
        assert answer['correct'] and answer['answer']==change['after'] and answer['missDebt']==0
        assert q['lang']==lang
    for (cid,lang),alternates in accepted_glosses._VALID_OLD_EDITED.items():
        for text in alternates:
            r=server.mark('legacy-'+cid+lang,{'id':cid,'direction':'gr-ru','selected':text,'lang':lang})
            assert r['correct'] and text in r['acceptedAnswers'],(cid,lang,text)
    for cid,lang,wrong in (
       ('p002','es','¿Cómo te llamas? (formal)'),
       ('p001','pt','Qual é o seu nome? (informal)'),
       ('w014','pt','você (singular)'),
       ('w015','pt','te (plural/formal)'),
       ('w093','ar','الزوج / الزوجة'),
       ('p002','zh','你叫什么名字？ （正式）'),
       ('w010','es','si')
    ):
        r=server.mark('wrong-'+lang+cid,{'id':cid,'direction':'gr-ru','selected':wrong,'lang':lang})
        assert not r['correct'] and r['missDebt']>=1,(cid,lang,wrong)
    with server.conn() as db:assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS translator + educational editor: 25 explicit localized revisions, 4 preserved equivalent older forms, 7 incorrect-register/orthography rejections, all 6-locale isolated scoring')
