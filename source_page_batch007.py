#!/usr/bin/env python3
"""Owner-PDF printed-headword attestation for catalog 1501–1750.

No publisher exercise text or PDF copied to Core. Derived app exercises
are not certified as original publisher questions.
"""
import json, collections
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'editorial-audit/source-page-batch-007-1501-1750.json'
PDF_SHA='49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282'
VISUAL={
'patk09_001':116,'patk09_002':116,'patk09_003':116,'patk09_004':116,
'patk09_005':115,'patk09_006':116,'patk09_007':116,'patk09_008':116,
'patk09_011':108,'patk09_012':108,'patk09_013':108,
'patk09_014':108,'patk09_015':108,'patk09_016':108}
OLD={
'patk09_001':109,'patk09_002':109,'patk09_003':110,
'patk09_004':110,'patk09_005':111,'patk09_006':111,
'patk09_007':112,'patk09_008':112,'patk09_011':114,
'patk09_012':114,'patk09_013':114,'patk09_014':115,
'patk09_015':115,'patk09_016':116}
PDF_TEXT_HITS={
'patk09_001':[113,116,118,119,126],
'patk09_002':[116,119],'patk09_003':[115,116,128],'patk09_004':[116],
'patk09_005':[115,117,118,119],'patk09_006':[116,117,118],
'patk09_007':[116,219],'patk09_008':[116],
'patk09_009':[],'patk09_010':[],
'patk09_011':[108,110,111,112,124,144,147],
'patk09_012':[108,110,111,124,144,181],
'patk09_013':[108,109,110,111,112,113,119,124,127,143,144,147,148,205],
'patk09_014':[108,111,112,124,170],
'patk09_015':[108,111,114,124,126,133,143,162,170,178,228,229,242,284],
'patk09_016':[108,109,111,112,124,148,162,170,178,179,188,197,227,268,270]}
assert len(VISUAL)==len(OLD)==14 and set(VISUAL)==set(OLD)
assert len(PDF_TEXT_HITS)==16 and all(p in PDF_TEXT_HITS[i] for i,p in VISUAL.items())
def apply(cards):
    byid={c['id']:c for c in cards}
    edited=[]
    for cid,page in VISUAL.items():
        c=byid[cid]
        assert c['kind']=='word' and c['source']=='original-from-book-syllabus'
        assert c['chapter']==c['unit']==9 and c['page']==OLD[cid],(cid,c['page'])
        assert not c.get('book_page_verified'),cid
        c['page']=page
        c['source_alignment']='owner_pdf_visual_attested_usage'
        c['book_page_verified']=True
        c['book_page_evidence']='printed_word_form_usage_not_publisher_exercise_or_first_introduction'
        edited.append(cid)
    assert len(edited)==14
    return edited

def build_report():
    import server
    counts=collections.Counter()
    gaps=collections.Counter()
    items=[]
    for n,c in enumerate(server.ALL[1500:1750],1501):
        t=c['kind'];counts[t]+=1
        row=dict(index=n,id=c['id'],kind=t,source=c['source'],
                 chapter=c['chapter'],current_page=c['page'],
                 publisher_exercise_verified=False)
        if t=='verb':
            assert c['chapter']==-9 and c['page']==0
            assert c['forms'][c['person']] in c['accepted']
            row.update(evidence_type='INDEPENDENT_VERB_PERSON_DRILL',page_source_verified=False,
                       greek_lemma=c['gr'],person=c['personName'],
                       target=c['forms'][c['person']],introducedUnit=c['introducedUnit'])
        elif t=='dialogue':
            assert c['source']=='original'
            assert len(c['gaps']) in (1,2,3) and len(c['bank'])==len(set(c['bank']))
            assert all(g in c['bank'] and f'[[{i}]]' in c['gr'] for i,g in enumerate(c['gaps']))
            gaps[len(c['gaps'])]+=1
            row.update(evidence_type='INDEPENDENT_DIALOGUE_COMPLETION',page_source_verified=False,
                       gap_count=len(c['gaps']),choice_count=len(c['bank']))
        elif t in ('word','phrase','sentence'):
            assert c['source']=='original-from-book-syllabus' and c['id'].startswith('patk')
            row['greek_form']=c['gr']
            if t=='word':
                cid=c['id']
                assert cid in PDF_TEXT_HITS
                page=VISUAL.get(cid)
                assert bool(c.get('book_page_verified'))==(page is not None)
                assert c['page']==(page if page is not None else 113)
                row.update(evidence_type='PDF_HEADWORD_VISUALLY_ATTESTED' if page
                           else 'TOPIC_WORD_UNCONFIRMED_TEXT_LAYER',
                           page_source_verified=page is not None,
                           visual_attested_printed_page=page,
                           earlier_approximate_page=OLD.get(cid,113),
                           pdf_text_exact_surface_hits=PDF_TEXT_HITS[cid])
            else:
                assert not c.get('book_page_verified')
                row.update(evidence_type='INDEPENDENT_TOPIC_SENTENCE_OR_PHRASE',
                           page_source_verified=False,exact_full_sentence_pdf_text_hit=False)
        else: raise AssertionError((n,c['id'],t))
        items.append(row)
    assert len(items)==250 and counts=={'verb':80,'dialogue':100,'word':16,'phrase':23,'sentence':31}
    assert gaps=={1:15,2:77,3:8}
    return dict(schema_version=1,task='Original book catalog evidence/provenance batch007 1501–1750',
       scope=dict(start=1501,end=1750,reviewed=250,total=1795),
       counts=dict(sorted(counts.items())),dialogue_gap_counts={str(k):v for k,v in sorted(gaps.items())},
       evidence_summary=dict(authorial_verb_drills=80,authorial_dialogue_cards=100,
          authorial_topic_phrases_sentences=54,visually_attested_book_headwords=14,
          topic_words_unconfirmed=2,publisher_exercises_verified=0,
          sentence_exact_text_layer_hits=0,corrected_headword_page_labels=14),
       methodology=dict(
          privately_owned_source_pdf=True,pdf_sha256=PDF_SHA,pdf_page_count=314,
          pdf_one_indexed_to_printed_page_offset=-2,
          searched_source_printed_pages=[14,289],
          visual_inspected_printed_pages=[108,109,114,115,116,186,216],
          no_pdf_bytes_images_or_excerpts_on_core=True,
          pdf_text_layer_is_imperfect=True,
          absence_of_literal_sentence_hit_does_not_prove_absence=True,
          word_occurrence_does_not_prove_publisher_exercise_identity=True,
          derived_syllabus_examples_are_independent_not_book_excerpts=True),
       items=items,
       deployment=dict(mode='graceful_bluegreen_required',metadata_page_edits=14,
                      source_greek_and_question_answers_changed=False,
                      user_sqlite_migration=False,audio_changed=False))
if __name__=='__main__':
    d=build_report()
    OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('BATCH007',OUT,'reviewed',len(d['items']),'counts',d['counts'])
