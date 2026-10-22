"""Small source-verification ledger compiled against user's purchased Patakis PDF.

Source: Ελληνικά Α΄ (Patakis), 314 PDF pages, printed_page = pdf_page - 2.
Only educational metadata and very short grammar labels; no publisher
exercise scans, text reproduction or the licensed PDF deployed on Core.
This is topic/lesson *source evidence*, not a card-by-card quote/attestation.
"""
from pathlib import Path
import json,datetime
import textbook_alignment

TOC_PDF_PAGES=(6,7,8,9)
VERIFIED={
 1:dict(start=14,end=23,topic='greetings / introductions',
        grammar=['είμαι','nominative pronouns','από + accusative','numbers 1–10']),
 2:dict(start=24,end=37,topic='address / contacts / residence',
        grammar=['μένω','έχω','κάνω','σε + accusative','possessives','numbers 10–100']),
 3:dict(start=38,end=47,topic='family / professions / marital status',
        grammar=['ποιος','τον λένε / τη λένε / το λένε']),
 4:dict(start=48,end=58,topic='languages / nationalities',
        grammar=['μιλάω (B1)','nationality adjectives','object accusative','numbers 100–1000']),
 5:dict(start=59,end=65,topic='review 1–4',grammar=[]),
 6:dict(start=66,end=79,topic='transport / time',grammar=['πάω','verbs B1/B2','prepositions']),
 7:dict(start=80,end=93,topic='daily routine / weather',grammar=['τρώω','λέω','ακούω','time expressions']),
 8:dict(start=94,end=107,topic='basic shopping',grammar=['plural nouns','articles cases','numbers gender']),
 9:dict(start=108,end=121,topic='clothing / colours / adjectives',grammar=['adjective agreement','-ομαι verbs']),
 10:dict(start=122,end=131,topic='review 6–9',grammar=[]),
 11:dict(start=132,end=149,topic='housing / orientation',grammar=['genitive','comparatives','-άμαι verbs']),
 12:dict(start=150,end=165,topic='trips / retelling',grammar=['aorist group A/B1/B2']),
 13:dict(start=166,end=183,topic='life stories',grammar=['additional irregular aorist']),
 14:dict(start=184,end=199,topic='food / future plans',grammar=['simple future']),
 15:dict(start=200,end=211,topic='review 11–14',grammar=[]),
 16:dict(start=212,end=231,topic='entertainment / holidays',grammar=['simple subjunctive']),
 17:dict(start=232,end=245,topic='employment',grammar=['simple imperative']),
 18:dict(start=246,end=261,topic='medical visit',grammar=['conditionals','comparative adverbs']),
 19:dict(start=262,end=277,topic='public services',grammar=['expanded future / subjunctive / aorist']),
 20:dict(start=278,end=289,topic='review 16–19',grammar=[]),
}
def verify():
    for unit,ref in VERIFIED.items():
        x=textbook_alignment.INDEX[unit]
        assert (x['start'],x['end'])==(ref['start'],ref['end']),unit
    assert all(unit in VERIFIED for unit in range(1,21))
    assert {5,10,15,20}==textbook_alignment.REVIEW_IDS
    return True
if __name__=='__main__':
    verify()
    destination=Path('editorial-audit/source-alignment-20261020.json')
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps({
      'edition':'Ελληνικά Α΄ · Μέθοδος εκμάθησης της ελληνικής ως ξένης γλώσσας, Patakis',
      'source':'User-purchased PDF, 314 pages, inspected privately; not copied to public Core',
      'pdf_contents_pages':TOC_PDF_PAGES,
      'printed_page_offset':2,
      'verified_lesson_topics':VERIFIED,
      'limit':'Verifies contents, grammar headings and chapter boundaries only; no exact first-occurrence guarantee for any card or complete lexical inventory.',
      'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
    },ensure_ascii=False,indent=2)+'\n')
    print('SOURCE_EVIDENCE_PASS',len(VERIFIED),'units','TOC PDF pages',TOC_PDF_PAGES)
