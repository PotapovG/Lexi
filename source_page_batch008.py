#!/usr/bin/env python3
"""Original catalog batch #8: authored grammar, word-order and theme prompts.

These 45 questions are independently authored exercises matching the
course syllabus. Printed page anchors are approximate teaching context,
not citations of reproduced publisher exercises. The purchased PDF
remains private, not uploaded to Core.
"""
import collections
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'editorial-audit/source-page-batch-008-1751-1795.json'
PDF_SHA='49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282'
START, END = 1751,1795

def build_report():
    import server
    import form_exercises
    items=[]
    counts=collections.Counter()
    gaps=collections.Counter()
    article_variants=0
    order_parent_ids=set()
    for i,card in enumerate(server.ALL[START-1:END],START):
        kind=card['kind']
        counts[kind]+=1
        assert not card.get('book_page_verified'),card['id']
        assert card['page']>0 and 1<=card['chapter']<=20
        item=dict(index=i,id=card['id'],kind=kind,
                  source=card['source'],chapter=card['chapter'],
                  current_page=card['page'],book_page_verified=False,
                  publisher_exercise_verified=False)
        if kind in ('sentence','phrase'):
            assert card['id'].startswith('patk19_')
            assert card['source']=='original-from-book-syllabus'
            assert card['chapter']==19
            item.update(evidence_type='INDEPENDENT_SYLLABUS_THEME_EXAMPLE',
                greek_form=card['gr'],
                note='App-authored Greek example; lesson page approximate, no publisher sentence identity proven.')
        elif kind=='article':
            assert card['source']=='original_book_syllabus_grammar'
            assert card['gr']==card['prompt'].replace('___',card['correct'])
            assert card['prompt'].count('___')==1
            assert len(card['options'])==8 and len(set(card['options']))==8
            assert len(card['acceptedForms']) in (1,2)
            assert card['acceptedForms'][0]==card['correct']
            assert set(card['acceptedForms'])<=set(card['options'])
            assert len(card.get('grammar_tags',[]))>=1
            assert card['id'].startswith('article_')
            assert card['chapter'] in (2,3,4,8)
            if len(card['acceptedForms'])==2:
                assert card['correct'] in ('τη','στη')
                assert card['acceptedForms'][1] in ('την','στην')
                article_variants+=1
            item.update(evidence_type='INDEPENDENT_ARTICLE_CASE_CLOZE',
                greek_form=card['gr'],cloze_prompt=card['prompt'],
                default_answer=card['correct'],
                accepted_spelling_forms=list(card['acceptedForms']),
                orthographic_variant_accepted=len(card['acceptedForms'])==2,
                note='Grammar practice authored for syllabus; no publisher exercise match asserted.')
        elif kind=='order':
            assert card['source']=='original_book_syllabus_sentence_order'
            assert card['id'].startswith('order_')
            parent_id=card['id'][len('order_'):]
            assert parent_id not in order_parent_ids
            order_parent_ids.add(parent_id)
            parent=server.BY_ID[parent_id]
            assert parent['source']=='original-from-book-syllabus'
            assert parent['kind'] in ('sentence','phrase')
            assert parent['gr']==card['gr']
            assert card['tokens']==parent['gr'].split()
            assert (card['chapter'],card['unit'],card['page'])==(
                parent['chapter'],parent['unit'],parent['page'])
            assert card['semanticId']==parent['semanticId']
            for lang in ('ru','en','zh','ar','es','pt'):
                assert card[lang]==parent[lang],(card['id'],lang)
            item.update(evidence_type='DERIVED_SENTENCE_ORDER_FROM_APP_OWN_PROMPT',
                greek_form=card['gr'],parent_card_id=parent_id,
                parent_card_source=parent['source'],parent_page=parent['page'],
                token_count=len(card['tokens']),repeated_tokens=len(card['tokens'])-len(set(card['tokens'])),
                note='Reordering app-created sentence; not copied from publisher exercise.')
        else:
            raise AssertionError((i,card['id'],kind))
        items.append(item)
    assert len(items)==45 and len({x['id'] for x in items})==45
    assert counts=={'sentence':2,'phrase':2,'article':24,'order':17},counts
    assert len(order_parent_ids)==17
    assert article_variants==5,article_variants
    return dict(schema_version=1,title='Greek Trainer original catalog source/authorship provenance batch #8',
       scope=dict(start_index=1751,end_index=1795,catalog_total=1795,reviewed=45),
       counts=dict(sorted(counts.items())),
       evidence_summary=dict(authored_syllabus_examples=4,authorial_article_exercises=24,
          authorial_word_order_exercises=17,accepted_article_orthography_variants=5,
          linked_parent_sentences=17,verified_original_publisher_exercises=0,
          source_page_attestations=0,card_page_changes=0),
       evidence_methodology=dict(
          owner_licensed_greek_book_pdf=True,original_pdf_sha256=PDF_SHA,
          no_pdf_pages_or_excerpts_stored_on_core=True,
          first_three_batched_source_evidence_reused=True,
          source_pdf_visual_inspection_not_needed_for_independent_app_question_identity=True,
          course_unit_and_page_reference_is_approximate_not_publisher_exercise_attestation=True,
          not_a_native_speaker_certification=True),
       items=items,
       deployment=dict(mode='AUDIT_REPORT_ONLY',restart_required=False,
            application_code_changed=False,card_content_changed=False,
            student_progress_changed=False,book_pdf_published=False,
            audio_changed=False))
if __name__=='__main__':
    report=build_report()
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('BATCH008',OUT,'items',len(report['items']),'kinds',report['counts'])
