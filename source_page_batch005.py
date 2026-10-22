#!/usr/bin/env python3
"""Batch #5: provenance of 250 independently generated tonos exercises.

The privately purchased Ελληνικά Α΄ PDF was checked in previous batches.
This report derives only lineage from existing app cards + publisher-word
evidence ledgers; it does not claim independently authored accent exercises
appear in the publisher's book. No source PDF is stored on Core.
"""
from pathlib import Path
from collections import Counter
import json
import catalog_v2 as cat
import server

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'editorial-audit/source-page-batch-005-1001-1250.json'
CONFIRMED = {'PDF_TEXT_EXACT_IN_UNIT', 'VISUAL_NEWLY_CONFIRMED', 'VISUAL_PREVERIFIED'}
START, END = 1001, 1250

def build_report():
    evidence = {}
    for n, stem in enumerate((
        'source-page-batch-001-1-250.json',
        'source-page-batch-002-251-500.json',
        'source-page-batch-003-501-750.json'), start=1):
        path = ROOT / 'editorial-audit' / stem
        data = json.loads(path.read_text(encoding='utf-8'))
        for row in data['items']:
            assert row['id'] not in evidence, row['id']
            evidence[row['id']] = (n, row)

    cards = server.ALL[START - 1:END]
    assert len(server.ALL) == 1795
    assert len(cards) == END - START + 1 == 250
    assert all(c['kind'] == 'accent' for c in cards)
    items = []
    counts = Counter()
    source_methods = Counter()
    seen = set()

    for number, accent in enumerate(cards, START):
        cid = accent['id']
        assert cid.startswith('stress_') and cid not in seen, cid
        seen.add(cid)
        parent_id = cid[len('stress_'):]
        parent = server.BY_ID[parent_id]
        batch_number, prior = evidence[parent_id]
        method = prior.get('source_method', prior.get('method'))
        verified = method in CONFIRMED
        assert verified == bool(parent.get('book_page_verified')), (cid, method)
        assert parent.get('source_alignment') in (
            'owner_pdf_visual_attested_usage',
            'owner_pdf_text_exact_attested_usage',
        ) if verified else not parent.get('book_page_verified')
        assert (parent['chapter'],parent['unit'],parent['page']) == (
            accent['chapter'],accent['unit'],accent['page'])
        assert cat._accent_parts(parent['gr']) == (
            accent['base'],accent['accented'],accent['accent_index'])
        assert accent['source'] == 'derived-original'
        assert not accent.get('book_page_verified') and accent['semanticId'] == parent['semanticId']
        choices = [i for i, char in enumerate(accent['base']) if char.lower() in 'αεηιουω']
        assert accent['accent_index'] in choices

        type_key = ('DERIVED_ACCENT_PARENT_ATTESTED' if verified
                    else 'DERIVED_ACCENT_PARENT_UNCONFIRMED')
        counts[type_key] += 1
        source_methods[method] += 1
        stripped_article = accent['accented'] != parent['gr']
        if stripped_article:
            counts['ARTICLE_STRIPPED_FROM_PARENT'] += 1
        row = dict(
            index=number,
            id=cid,
            kind='accent',
            chapter=accent['chapter'],
            current_page=accent['page'],
            greek_form=accent['accented'],
            source=accent['source'],
            parent_card_id=parent_id,
            parent_catalog_evidence_batch=batch_number,
            parent_source_method=method,
            parent_page=parent['page'],
            parent_page_attested=parent['page'] if verified else None,
            parent_source_page_verified=verified,
            article_stripped_from_parent=stripped_article,
            accent_index=accent['accent_index'],
            publisher_exercise_verified=False,
            source_page_verified=False,
            evidence_type=type_key,
            reason=('Auto-generated learner accent-position exercise; '
                    + ('Greek parent headword/form occurs on the recorded printed page, '
                       'but exercise identity is not in the book.'
                       if verified else
                       'no publisher page evidence for the parent Greek form; '
                       'the inherited page is a syllabus approximation.')),
        )
        items.append(row)
    assert len(items) == 250
    return dict(
        schema_version=1,
        task='Greek Trainer original catalog provenance batch #5: items 1001-1250',
        scope=dict(start_index=START,end_index=END,total_catalog=1795,reviewed_count=250),
        methodology=dict(
            original_source='Privately owned Ελληνικά Α΄ PDF, same SHA as batches 1–3',
            source_pdf_sha256='49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282',
            publisher_pdf_on_core=False,
            pdf_excerpts_on_core=False,
            pdf_page_images_on_core=False,
            fresh_source_line_by_line_checks=False,
            previous_source_word_attestations_reused=True,
            accent_exercises_are_learner_app_generated=True,
            exact_publisher_exercise_identity_verified=False,
            inherited_printed_page_not_an_exercise_citation=True,
        ),
        counts=dict(sorted(counts.items())),
        parent_evidence_methods=dict(sorted(source_methods.items())),
        verified_publisher_exercises=0,
        new_source_word_attestations=0,
        metadata_page_changes=0,
        items=items,
        release=dict(status='PROVENANCE_REPORT_ONLY', app_code_changed=False,
                     restart_required=False, progress_db_changed=False,
                     saved_card_ids_changed=False, audio_changed=False),
    )

if __name__ == '__main__':
    data = build_report()
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('BATCH005 ledger',OUT,'checked',len(data['items']),'counts',data['counts'])
