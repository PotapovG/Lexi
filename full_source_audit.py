#!/usr/bin/env python3
"""Reconcile original Lexi card source-page ledgers #1..#8. Read-only."""
import json,hashlib,glob,collections
from pathlib import Path
import server,vocab_lessons
ROOT=Path(__file__).parent
OUT=ROOT/'editorial-audit/full-source-audit-1795-final.json'
PROVEN={'VISUAL_PREVERIFIED','VISUAL_NEWLY_CONFIRMED','PDF_TEXT_EXACT_IN_UNIT'}
def generate():
    assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717 and len(vocab_lessons.VOCAB)==1700
    assert len({c['id'] for c in server.ALL})==1795
    entries=[]; batches=[]; kinds=collections.Counter();attested=collections.Counter();sources=collections.Counter()
    for b in range(1,9):
        paths=glob.glob(str(ROOT/f'editorial-audit/source-page-batch-{b:03d}-*.json'))
        assert len(paths)==1,paths
        path=Path(paths[0]);raw=path.read_bytes();data=json.loads(raw)
        rows=data['items'];start=1+(b-1)*250;end=min(start+249,1795)
        assert [x['index'] for x in rows]==list(range(start,end+1))
        n_attested=0
        for row in rows:
            i=row['index'];c=server.ALL[i-1]
            assert row['id']==c['id'] and row['kind']==c['kind'],(i,c['id'])
            if b==1: page=row['selected_page'] if row['selected_page'] is not None else row['before_page']
            elif b==2:page=row['attested_page'] if row['attested_page'] is not None else row['old_page']
            elif b==3:page=row['attested_page'] if row['attested_page'] is not None else row['before_page']
            elif b in (4,5,7,8):page=row['current_page']
            else:page=row['page']
            assert c['page']==page,(i,c['id'],c['page'],page)
            if 'chapter' in row:assert c['chapter']==row['chapter'],i
            method=row.get('source_method',row.get('method',row.get('evidence_type','none')))
            proven=(method in PROVEN if b<=3 else (bool(row['page_source_verified']) if b==7 else False))
            assert proven==bool(c.get('book_page_verified')),(i,c['id'],method)
            if c['kind'] in ('accent','article','order','dialogue','verb','plural','sentence'):
                assert not proven,('derived exercise incorrectly certified',c['id'])
            if b>=4:assert not row.get('publisher_exercise_verified',False)
            if c['kind']=='order':
                p=server.BY_ID[c['id'][len('order_'):]]
                assert c['gr']==p['gr'] and c['tokens']==p['gr'].split()
                assert all(c[l]==p[l] for l in ('ru','en','zh','ar','es','pt'))
            n_attested+=proven;kinds[c['kind']]+=1;sources[c['source']]+=1
            if proven:attested[c['kind']]+=1
            entries.append(dict(index=i,id=c['id'],kind=c['kind'],chapter=c['chapter'],
                printed_page=c['page'],source=c['source'],
                source_page_verified=proven,publisher_exercise_identity_verified=False,
                evidence_method=method,audit_batch=b))
        batches.append(dict(batch=b,file=path.name,sha256=hashlib.sha256(raw).hexdigest(),
                            start=start,end=end,reviewed=len(rows),source_verified=n_attested))
    assert [x['source_verified'] for x in batches]==[142,92,73,0,0,0,14,0]
    assert len(entries)==1795 and len({r['id'] for r in entries})==1795
    assert sum(attested.values())==321
    assert dict(attested)=={'word':270,'number':23,'letter':24,'phrase':4},attested
    assert [x['index'] for x in entries]==list(range(1,1796))
    return dict(schema=1,title='Lexi 1795 original catalog eight-batch provenance audit',
        status='INDEX_AND_SOURCE_PROVENANCE_COVERED_NOT_ALL_SOURCE_MATCHED',
        totals=dict(catalog=1795,audited=1795,attested_lexical_or_alphabet_pages=321,
                    not_source_attested_or_authored=1474,verified_publisher_exercises=0,
                    listening=717,standalone_A1_A2=1700),
        kind_counts=dict(sorted(kinds.items())),
        attested_kind_counts=dict(sorted(attested.items())),
        source_counts=dict(sorted(sources.items())),
        batch_checksums=batches,
        card_ids_sha256=hashlib.sha256(json.dumps([e['id'] for e in entries],ensure_ascii=False).encode()).hexdigest(),
        source_pdf_sha256='49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282',
        limitations=['Verified lexical occurrence is not exercise identity or first use',
          'Independently written accent, article, word-order and dialog tasks cannot be publisher-certified',
          'OCR/text-layer incompleteness means unmatched is not proof of absence',
          'Native editorial review and exact original-publisher exercise equivalence not completed'],
        cards=entries)
if __name__=='__main__':
    m=generate()
    OUT.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
    print('ALL8 PROVENANCE',len(m['cards']),m['totals'])
