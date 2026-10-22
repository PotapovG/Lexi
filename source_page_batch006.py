#!/usr/bin/env python3
"""Original catalog 1251-1500 source/provenance audit, zero runtime changes.

Text-layer page candidates were privately analyzed against owner's licensed
PDF. No PDF/text/screenshots supplied to the deployed app. A lexical surface
match is NOT evidence of a publisher exercise or of first introduction.
"""
from pathlib import Path
import json, collections
import server, catalog_v2

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'editorial-audit/source-page-batch-006-1251-1500.json'
CONFIRMED={'PDF_TEXT_EXACT_IN_UNIT','VISUAL_NEWLY_CONFIRMED','VISUAL_PREVERIFIED'}
SOURCE_TEXT_MATCHES = "001:176,264|113,176,264,267,268,269\n002:104,107,122,272,279|104,107,109,122,247,261,272,273,279\n003:-|113,128\n004:95,98,101,104,122|94,95,98,101,104,122,175\n005:-|-\n006:-|-\n007:68,112,126,130,136,154,155,208,280,281,282|16,68,69,71,73,112,126,127,130,136,154,155,177,178,203,208,259,280,281,282,286\n008:176,180|29,176,180\n009:-|140\n010:203|203\n011:-|-\n012:-|-\n013:-|208,283\n014:-|-\n015:-|-\n016:-|186,204\n017:-|204\n018:-|-\n019:-|-\n020:-|-\n021:-|204\n022:-|145,174\n023:-|145,146\n024:-|145,146\n025:-|-\n026:-|-\n027:-|104,106,190,193\n028:-|103,104,106,193\n029:-|104\n030:-|104,193,199\n031:-|103,104,105,106,193,199,252\n032:-|104\n033:-|104\n034:-|260\n035:-|-\n036:-|-\n037:-|-\n038:-|-\n039:240,270|195,222,227,237,239,240,241,243,244,245,267,268,270,271,273,275,277,282\n040:233,234,238,241|233,234,238,241,245,285\n041:-|145,177,214\n042:-|-\n043:-|-\n044:143|84,90,101,102,125,131,143,161\n045:-|-\n046:-|-\n047:-|-\n048:-|247,251,252,259,261\n049:-|-\n050:-|180,286\n051:-|-\n052:258|258\n053:55,267|55,152,267\n054:-|-\n055:207|172,207\n056:-|234,243,273,276,279\n057:-|-\n058:225|225\n059:-|-\n060:-|-\n061:-|-\n062:208|208\n063:68|68,69\n064:-|39,282\n065:-|89,173,261\n066:-|-\n067:206|206\n068:181|29,181\n069:-|-\n070:-|-\n071:-|-\n072:-|-\n073:169,286|120,121,169,286\n074:-|-\n075:-|-"
VERB_LEXEME_SOURCE_TEXT = {
 'γράφω':{'literal_match_page_count':61,'sample_pages':[17,18,37,41,46,51,53,58]},
 'μένω':{'literal_match_page_count':30,'sample_pages':[25,26,27,28,30,35,42,59]},
 'διαβάζω':{'literal_match_page_count':37,'sample_pages':[17,31,36,51,61,82,86,89]},
 'δουλεύω':{'literal_match_page_count':29,'sample_pages':[16,42,59,61,75,80,81,84]},
}

def probe():
    def pages(s):
        return [] if s=='-' else [int(n) for n in s.split(',')]
    pairs={}
    for line in SOURCE_TEXT_MATCHES.splitlines():
        n, data=line.split(':',1)
        full,lemma=data.split('|')
        rid='topic'+n
        assert rid not in pairs
        fp,lp=pages(full),pages(lemma)
        assert len(fp)==len(set(fp)) and len(lp)==len(set(lp))
        assert set(fp)<=set(lp)
        assert all(1<=n<=289 for n in fp+lp)
        pairs[rid]=(fp,lp)
    assert len(pairs)==75
    return pairs

def build():
    prev={}
    for n,stem in enumerate([
       'source-page-batch-001-1-250.json',
       'source-page-batch-002-251-500.json',
       'source-page-batch-003-501-750.json',
       'source-page-batch-004-751-1000.json'
    ],1):
        d=json.loads((ROOT/'editorial-audit'/stem).read_text(encoding='utf-8'))
        for row in d['items']:
            assert row['id'] not in prev
            prev[row['id']]=(n,row)
    textbook_probes=probe()
    items=[]
    counts=collections.Counter()
    source_evidence=collections.Counter()
    cards=server.ALL[1250:1500]
    assert len(cards)==250 and len(server.ALL)==1795
    assert len({c['id'] for c in cards})==250
    for index,c in enumerate(cards,1251):
        row=dict(index=index,id=c['id'],kind=c['kind'],
                 greek_form=c.get('accented',c.get('gr')),
                 chapter=c['chapter'],page=c['page'],source=c['source'],
                 publisher_exercise_verified=False,source_page_verified=False)
        if c['kind']=='accent':
            assert c['id'].startswith('stress_') and c['source']=='derived-original'
            p=server.BY_ID[c['id'][7:]]
            evidence_batch, prior=prev[p['id']]
            meth=prior.get('source_method',prior.get('method',prior.get('evidence_type')))
            verified=bool(p.get('book_page_verified'))
            assert (verified == (meth in CONFIRMED)),(c['id'],meth)
            assert cat_parts(p)==(c['base'],c['accented'],c['accent_index'])
            assert p['page']==c['page'] and p['chapter']==c['chapter']
            assert p['semanticId']==c['semanticId']
            assert not c.get('book_page_verified')
            source_evidence[meth]+=1
            if p['source']=='review-original':
                assert not verified
                typ='DERIVED_ACCENT_REVIEW_CLONE_PARENT'
            else:
                assert p['source']=='original'
                typ=('DERIVED_ACCENT_MAIN_PARENT_ATTESTED' if verified
                     else 'DERIVED_ACCENT_MAIN_PARENT_UNCONFIRMED')
            row.update(parent_card_id=p['id'],parent_catalog_evidence_batch=evidence_batch,
                       parent_source_method=meth,parent_page=p['page'],
                       parent_source_page_attested=verified,
                       parent_source=p['source'],accent_index=c['accent_index'],
                       evidence_type=typ,
                       reason='Generated accent drill; source-page lineage is parent-word occurrence or approximation, not publisher task provenance.')
        elif c['kind']=='word':
            assert c['chapter']==-8 and c['page']==0 and c['id'] in textbook_probes
            assert c['source']=='original'
            fp,lp=textbook_probes[c['id']]
            if fp:typ='TOPICAL_VOCAB_EXACT_FULL_FORM_TEXT_HIT'
            elif lp:typ='TOPICAL_VOCAB_LEMMA_ONLY_TEXT_HIT'
            else:typ='TOPICAL_VOCAB_NO_TEXT_LAYER_HIT'
            row.update(evidence_type=typ,
                       pdf_exact_full_form_printed_pages=fp,
                       pdf_exact_lemma_printed_pages=lp,
                       note='Supplemental app-authored topic word; text-layer lexical hit does not mean identical book exercise. OCR absence is not absence from the book.',
                       page_label_unchanged_zero=True)
        elif c['kind']=='verb':
            assert c['chapter']==-9 and c['page']==0 and c['source']=='original'
            assert c['gr'] in VERB_LEXEME_SOURCE_TEXT
            assert c['person'] in range(6)
            assert c['forms'][c['person']] in c['accepted']
            assert c['introducedUnit']>=1
            typ='INDEPENDENT_CONJUGATION_DRILL'
            row.update(evidence_type=typ,person=c['person'],
                       person_name=c['personName'],correct_person_form=c['forms'][c['person']],
                       introduced_unit=c['introducedUnit'],
                       pdf_base_verb_lemma_text_matches=VERB_LEXEME_SOURCE_TEXT[c['gr']],
                       note='App-authored conjugation/translation drill; independent of exact printed publisher exercise. Printed source page label remains zero.')
        else: raise AssertionError(c['id'])
        counts[typ]+=1
        items.append(row)
    assert len(items)==250 and len(textbook_probes)==75
    return dict(schema_version=1,
      task='Original Greek textbook catalog source and authorship batch006 indices 1251–1500',
      scope=dict(start_index=1251,end_index=1500,total=1795,reviewed=250),
      methodology=dict(
        owned_private_pdf=True,
        source_pdf_sha256='49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282',
        pdf_page_count=314,printed_page_mapping='PDF one-indexed page minus 2',
        scanned_text_layer_is_imperfect=True,
        source_pages_considered='printed pp14–289 (narrative only, no appendix)',
        exact_publisher_exercise_identity_verified=False,
        fresh_text_layer_lexeme_checks_for_topics=True,
        visually_inspected_printed_pages=[104,208,258],
        no_pdf_page_images_or_excerpts_on_core=True,
        exact_text_hit_is_not_first_introduction=True,
        topic_page_0_untouched=True,
        conjugation_page_0_untouched=True
      ),
      counts=dict(sorted(counts.items())),
      accent_parent_evidence_methods=dict(sorted(source_evidence.items())),
      metadata_page_changes=0,
      verified_publisher_exercises=0,
      source_lexeme_matches=dict(full_article_and_headword=18,bare_headword_or_full=41,unmatched_text_layer=34,verb_lemmas=4),
      items=items,
      release=dict(status='AUDIT_LEDGER_NO_RUNTIME_RELEASE',
        server_code_changed=False,restart_required=False,
        user_sqlite_changed=False,card_ids_changed=False,
        student_history_changed=False,audio_changed=False))
def cat_parts(card):
    return catalog_v2._accent_parts(card['gr'])
if __name__=='__main__':
    d=build()
    OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('BATCH006 CREATED',OUT,len(d['items']),d['counts'])
