"""Exact stage/sense edits: score and grammar checks in temporary SQLite."""
import tempfile,collections,sqlite3
from pathlib import Path
import server,catalog_v2,editorial_localization_round2 as edits
assert len(server.ALL)==1795 and len(catalog_v2.BY_ID)==1796
latest=catalog_v2.REVIEWED_LOCALIZATION_ROUND2+server.REVIEWED_ARABIC_ROUND2
assert len(latest)==len(edits.REVISIONS)==37
assert collections.Counter(x['lang'] for x in latest)=={'pt':16,'es':10,'zh':9,'ar':2}
assert len({(x['id'],x['lang']) for x in latest})==37
assert all(server.BY_ID[e['id']]['gr']==e['greek'] and server.BY_ID[e['id']][e['lang']]==e['after'] for e in latest)
assert all(e['level']=='source_author_text_validated_ai_not_native_certified' for e in latest)
assert server.BY_ID['p005']['es']=='¿De dónde es usted? (formal)'
assert server.BY_ID['p004']['pt']=='De onde és? (informal)'
assert server.BY_ID['p016']['pt']=='Tem telemóvel? (formal)'
assert server.BY_ID['p016']['zh'].startswith('您')
assert server.BY_ID['patk02_003']['es'].find('mi amiga')>0
assert server.BY_ID['patk02_003']['ar'].find('صديقتي')>0
assert server.BY_ID['patk03_005']['es'].find('Mi amigo')==0
assert server.BY_ID['p014']['ar'].find('هو يعيش')==0

with tempfile.TemporaryDirectory() as tmp:
    server.DB=str(Path(tmp)/'test.sqlite3');server.init_db()
    for e in latest:
        c=server.BY_ID[e['id']]
        q=server.format_question(c,'gr-ru',e['lang'])
        assert len(q['choices'])==8 and len(set(q['choices']))==8 and e['after'] in q['choices'],(e['id'],e['lang'],q['choices'])
        res=server.mark('editor-'+e['lang'],{'id':e['id'],'direction':'gr-ru',
                                            'lang':e['lang'],'selected':e['after']})
        assert res['correct'] and res['answer']==e['after'] and res['missDebt']==0,(e,res)
        # Forward/reverse quiz must preserve Greek as source, and no
        # cross-locale answer is silently approved.
        reverse=server.shape(c,'ru-gr',e['lang'])[1]
        assert reverse==c['gr'] and reverse==e['greek'],e
    for cid,lang,wrong in (
       ('p005','es','¿De dónde eres? (formal)'),
       ('p016','es','¿Tienes un teléfono móvil? (formal)'),
       ('p019','es','¿Cuál es su dirección?'),
       ('p034','es','¿Hablas ruso? (formal)'),
       ('p011','pt','Onde mora? (informal)'),
       ('p033','pt','Fala grego? (informal)'),
       ('p004','pt','De onde é? (informal)'),
       ('p020','zh','您的电话号码是多少？'),
       ('p014','ar','هو / هي تعيش في أثينا.'),
       ('patk03_005','es','Mi amiga tiene dos hijos, un hijo y una hija.')
    ):
        res=server.mark('wrong-'+lang+cid,{'id':cid,'direction':'gr-ru','lang':lang,'selected':wrong})
        assert not res['correct'] and res['missDebt']==2,(cid,lang,res)
    # Previously edited translations remain valid and visible.
    assert server.BY_ID['p002']['es']=='¿Cómo se llama usted? (formal)'
    assert server.BY_ID['p001']['pt']=='Como te chamas? (informal)'
    assert server.BY_ID['p002']['zh']=='您叫什么名字？（正式）'
    assert server.BY_ID['w093']['ar']=='الزوج (مذكر)'
    from accepted_glosses import _VALID_OLD_EDITED
    for (cid,lang),aliases in _VALID_OLD_EDITED.items():
        for alias in aliases:
            res=server.mark('old-valid-'+lang+cid,{'id':cid,'direction':'gr-ru','lang':lang,'selected':alias})
            assert res['correct'],(cid,lang,alias)
    with server.conn() as db: assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS 37 source-anchored 4-locale edits, 10 wrong-register/gender rejected, 4 old valid aliases preserved and DB integrity')
