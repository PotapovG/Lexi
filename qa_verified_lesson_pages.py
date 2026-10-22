"""All verified page anchors are source-reviewed; unrelated content remains approximate."""
import catalog_v2 as catalog
import server,verified_lesson_pages as reviewed
assert len(catalog.ALL)==1795 and len(catalog.BY_ID)==1796
assert len(catalog.VERIFIED_LESSON_PAGES)==58
assert len(reviewed.PAGE_HEADWORDS)==7
for cid,page in reviewed.PAGES_BY_ID.items():
    c=catalog.BY_ID[cid]
    assert c['page']==page and c['book_page_verified'] is True
    assert c['source_alignment']=='owner_pdf_worked_example_visual'
    assert 1<=c['chapter']<=4
    accent=catalog.BY_ID.get('stress_'+cid)
    if accent:
        assert accent['page']==c['page']
        assert not accent['book_page_verified']
        assert accent['source_alignment']=='derived_from_verified_headword'
    q=server.format_question(c,'gr-ru','ru')
    assert q['sourcePageVerified'] and q['page']==page
for cid in ('dlg024_v2','dlg024','w004'):
    c=catalog.BY_ID[cid]
    assert not c.get('book_page_verified'),cid
    q=server.format_question(c,('gap0' if c['kind']=='dialogue' else 'gr-ru'),'ru')
    assert q['sourcePageVerified'] is False
assert all(catalog.BY_ID[x]['page']==40 for x in ('w023','w024','w025','w033','w034'))
assert server.LISTENING_ENABLED and len(server.LISTEN_CARDS)==717
print('PASS 58 manually reviewed page anchors, all derived accents same parent page, old/new dialogue IDs, 717 audio and source provenance API')
