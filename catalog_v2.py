"""Merged full-book original topic-aligned catalog with approximate page anchors."""
import data as legacy
import curriculum
import english_legacy

CHAPTERS=[dict(id=unit,start=start,end=end,title=title,en=english,review=False)
          for unit,start,end,title,english in curriculum.CHAPTERS]
CHAPTERS += [dict(id=unit,start=start,end=end,title=title,en=english,review=True)
             for unit,start,end,title,english in curriculum.EXTRA_SECTIONS]
CHAPTERS.sort(key=lambda x:x["start"])
INDEX={x["id"]:x for x in CHAPTERS}
ALL=[]
num_ids=set(range(118,127)) | set(range(169,200))
for collection,translations in ((legacy.WORDS,english_legacy.WORDS_EN),
                                (legacy.PHRASES,english_legacy.PHRASES_EN),
                                (legacy.SENTENCES,english_legacy.SENTENCES_EN)):
    assert len(collection)==len(translations)
    counters={}
    totals={}
    for item in collection: totals[item["unit"]]=totals.get(item["unit"],0)+1
    for item,en in zip(collection,translations):
        c=dict(item)
        c["en"]=en
        c["chapter"]=c["unit"]
        n=counters.get(c["unit"],0)
        counters[c["unit"]]=n+1
        info=INDEX[c["unit"]]
        c["page"]=info["start"]+(n*(info["end"]-info["start"]+1)//totals[c["unit"]])
        c["source"]="original"
        if c["kind"]=="word" and int(c["id"][1:]) in num_ids: c["kind"]="number"
        ALL.append(c)
for item in legacy.PLURALS:
    c=dict(item)
    source_word=next((w for w in ALL if w["gr"]==c["sg"] and w["kind"]=="word"),None)
    c.update(chapter=source_word["chapter"] if source_word else 7,
             page=source_word["page"] if source_word else 94,
             en=c["ru"],source="original",supplemental=True)
    ALL.append(c)
for item in curriculum.build_extra():
    c=dict(item)
    # Distribute original teaching examples across the chapter as approximate anchors.
    siblings=[x for x in curriculum.RAW[c["chapter"]].values()]
    entries=sum(len(s.strip().splitlines()) for s in siblings)
    before=sum(len(curriculum.RAW[c["chapter"]][k].strip().splitlines()) for k in curriculum.RAW[c["chapter"]] if list(curriculum.RAW[c["chapter"]]).index(k)<list(curriculum.RAW[c["chapter"]]).index(c["kind"]))
    current=int(c["id"][-3:])-1
    section=INDEX[c["chapter"]]
    c["page"]=section["start"]+((before+current)*(section["end"]-section["start"]+1)//entries)
    ALL.append(c)

# Noun plural drills for the additional chapter-specific teaching corpus.
# All forms are original self-authored exercises, not a transcription of the textbook.
MORE_PLURALS = {
 5:[("το λεωφορείο","τα λεωφορεία"),("η στάση","οι στάσεις"),("ο σταθμός","οι σταθμοί")],
 6:[("η Δευτέρα","οι Δευτέρες"),("η εβδομάδα","οι εβδομάδες"),("η μέρα","οι μέρες")],
 7:[("το βιβλίο","τα βιβλία"),("το τετράδιο","τα τετράδια"),("το μολύβι","τα μολύβια")],
 8:[("το μήλο","τα μήλα"),("η μπανάνα","οι μπανάνες"),("η ντομάτα","οι ντομάτες")],
 9:[("το διαμέρισμα","τα διαμερίσματα"),("το δωμάτιο","τα δωμάτια"),("η πόρτα","οι πόρτες")],
 10:[("το ταξίδι","τα ταξίδια"),("το αεροπλάνο","τα αεροπλάνα"),("η βαλίτσα","οι βαλίτσες")],
 11:[("η ιστορία","οι ιστορίες"),("η ζωή","οι ζωές")],
 12:[("το σχέδιο","τα σχέδια"),("το ραντεβού","τα ραντεβού")],
 13:[("η βόλτα","οι βόλτες"),("η ταινία","οι ταινίες"),("το μουσείο","τα μουσεία")],
 14:[("ο συνάδελφος","οι συνάδελφοι"),("η συνάντηση","οι συναντήσεις"),("ο υπολογιστής","οι υπολογιστές")],
 15:[("το νοσοκομείο","τα νοσοκομεία"),("το φάρμακο","τα φάρμακα"),("ο πονοκέφαλος","οι πονοκέφαλοι")],
 16:[("η ουρά","οι ουρές"),("το έγγραφο","τα έγγραφα"),("το έντυπο","τα έντυπα")]
}
for unit,pairs in MORE_PLURALS.items():
    for i,(sg,pl) in enumerate(pairs):
        noun=next((c for c in ALL if c["kind"]=="word" and c["chapter"]==unit and c["gr"]==sg),None)
        assert noun, (unit,sg)
        ALL.append(dict(id=f"xn{unit:02d}{i:03d}",unit=unit,chapter=unit,page=noun["page"],
                        kind="plural",topic=noun["topic"],sg=sg,pl=pl,
                        ru=noun["ru"],en=noun["en"],supplemental=True,source="original"))
LETTERS=[
("Α α","альфа","alpha"),("Β β","бета","beta"),("Γ γ","гамма","gamma"),("Δ δ","дельта","delta"),
("Ε ε","эпсилон","epsilon"),("Ζ ζ","дзета","zeta"),("Η η","эта","eta"),("Θ θ","тета","theta"),
("Ι ι","йота","iota"),("Κ κ","каппа","kappa"),("Λ λ","лямбда","lambda"),("Μ μ","мю","mu"),
("Ν ν","ню","nu"),("Ξ ξ","кси","xi"),("Ο ο","омикрон","omicron"),("Π π","пи","pi"),
("Ρ ρ","ро","rho"),("Σ σ ς","сигма","sigma"),("Τ τ","тау","tau"),("Υ υ","ипсилон","upsilon"),
("Φ φ","фи","phi"),("Χ χ","хи","chi"),("Ψ ψ","пси","psi"),("Ω ω","омега","omega")]
for i,(gr,ru,en) in enumerate(LETTERS):
    ALL.append(dict(id=f"a{i:03d}",unit=0,chapter=0,page=8+(i*6//len(LETTERS)),
                    kind="letter",topic="Αλφάβητο",gr=gr,ru=ru,en=en,source="original"))
# Reviews reuse already studied examples as fresh practice cards, not purported textbook text.
for review_id,unit_range in [(-1,range(1,5)),(-2,range(5,9)),(-3,range(9,13)),(-4,range(13,17)),(-5,range(1,17))]:
    collection=[c for c in ALL if c["chapter"] in unit_range and c["kind"] in ("word","number","phrase","sentence")]
    # Max 24 review cards, spread among the four preceding lessons; appendix revisits all.
    chosen=[]
    for unit in unit_range:
        group=[c for c in collection if c["chapter"]==unit]
        chosen.extend(group[::max(1,len(group)//5)][:5])
    if not chosen: continue
    for idx,original in enumerate(chosen):
        clone=dict(original)
        clone["id"]=f"v{abs(review_id)}_{idx:03d}"
        clone["chapter"]=review_id
        clone["page"]=INDEX[review_id]["start"]+idx*(INDEX[review_id]["end"]-INDEX[review_id]["start"]+1)//len(chosen)
        clone["source"]="review-original"
        ALL.append(clone)
# Generate accent-placement questions from standalone Greek vocabulary.
# Accent position is the LETTER bearing tonos, not the pronunciation syllable.
# E.g. είναι -> ειναι, index 1 (the first ι).
import unicodedata as _ud
import re as _re

_ARTICLES={"ο","η","το","οι","τα","τον","την","τη","τους","τις"}
_ACCENT_CHARACTERS=set("αεηιουωΑΕΗΙΟΥΩ")
def _accent_parts(greek):
    text=_ud.normalize("NFC",greek.strip())
    tokens=text.split()
    if len(tokens)==2 and tokens[0].lower() in _ARTICLES:
        text=tokens[1]
    elif len(tokens)!=1:
        return None
    if not _re.fullmatch(r"[\u0370-\u03FF\u1F00-\u1FFF]+",text):
        return None
    # Track combining marks as belonging to their base letter.
    original=list(_ud.normalize("NFC",text))
    accented_indices=[]
    plain=[]
    for i,letter in enumerate(original):
        parts=_ud.normalize("NFD",letter)
        if "\u0301" in parts:
            if parts[0] not in _ACCENT_CHARACTERS: return None
            accented_indices.append(i)
        plain.append(_ud.normalize("NFC",parts.replace("\u0301","")))
    if len(accented_indices)!=1:
        return None
    return "".join(plain),text,accented_indices[0]

_added=set()
ACCENT_COUNT=0
for source_card in list(ALL):
    if source_card["kind"] not in ("word","number"): continue
    parts=_accent_parts(source_card["gr"])
    if not parts: continue
    plain,accented,stress_index=parts
    identity=(source_card["chapter"],plain.lower())
    if identity in _added:continue
    _added.add(identity)
    ALL.append(dict(id="stress_"+source_card["id"], kind="accent",
                    chapter=source_card["chapter"],unit=source_card["unit"],page=source_card["page"],
                    topic=source_card["topic"],source="derived-original",
                    gr=accented,ru=source_card["ru"],en=source_card["en"],
                    base=plain,accented=accented,accent_index=stress_index))
    ACCENT_COUNT+=1
# Offline translation cache: Simplified Chinese and standard Somali. Generated
# from the preexisting English teaching glosses; Somali is experimental and
# should be reviewed by a native speaker before formal instructional use.
import json as _json
from pathlib import Path as _Path
_TRANSLATIONS=_json.loads((_Path(__file__).parent/"translations_zh_so.json").read_text(encoding="utf-8"))
for _c in ALL:
    if _c["kind"]=="plural":
        # Plural training compares two GREEK word forms, not translations.
        continue
    for _lang in ("zh","so"):
        _value=_TRANSLATIONS[_lang].get(_c["en"])
        if not _value:
            raise ValueError("Missing "+_lang+" teaching translation for "+_c["id"]+" / "+_c["en"])
        _c[_lang]=_value
# Offline Spanish and European Portuguese teaching glosses.
_ES_PT=_json.loads((_Path(__file__).parent/"translations_es_pt.json").read_text(encoding="utf-8"))
for _card in ALL:
    if _card["kind"]=="plural":continue
    for _lang in ("es","pt"):
        _value=_ES_PT[_lang].get(_card["en"])
        if not _value:raise ValueError("Missing "+_lang+" gloss for "+_card["id"])
        _card[_lang]=_value
# Topic-oriented independent A1/A2 tracks, distinct from textbook page tags.
import topics_verbs as _tv
TOPICS=[dict(id=code,ru=ru,en=en) for code,ru,en,_ in _tv.THEMES]
_GROUPS={x[0]:x[3] for x in _tv.THEMES}
for _card in ALL:
    if _card["kind"]!="word":continue
    _gloss=_card.get("en","").casefold()
    _tags=[code for code,_,_,terms in _tv.THEMES if any(t in _gloss for t in terms)]
    _card["topics"]=_tags
    _card["level"]="A1" if _card["chapter"] in (0,1,2,3,4,5,6,7,8) else "A2"

_EXTRA=_json.loads((_Path(__file__).parent/"topic_translations.json").read_text("utf-8"))
for _word in _tv.TOPIC_EXTRA:
    _item=dict(_word)
    for _lang in ("zh","so","es","pt"):
        _item[_lang]=_EXTRA[_lang][_item["en"]]
    ALL.append(_item)
for _verb in _tv.verb_cards():
    _item=dict(_verb)
    for _lang in ("zh","so","es","pt"):
        _item[_lang]=_EXTRA[_lang][_item["en"]]
    ALL.append(_item)
import dialogues as _dialogues
ALL.extend(_dialogues.CARDS)
# 80 more authored chapter-aligned Greek-only conversation gap exercises.
import dialogues_extra as _dialogues_extra
ALL.extend(_dialogues_extra.CARDS)
# Final step: convert old internal 16-unit topic bucket IDs and approximate
# page labels to the verified PRINTED 20-unit structure of Ελληνικά Α΄.
# Existing word/question IDs remain untouched for historical progress keys.
import textbook_alignment as _book_alignment
ALIGNMENT_MOVES=_book_alignment.align(ALL)
CHAPTERS=_book_alignment.CHAPTERS
# Original language drills that specifically mirror the syllabus progression,
# distinct from the user-provided copyrighted book's exercise pages.
import patakis_context_cards as _patk
ALL.extend(_patk.CARDS)
import form_exercises as _form
ALL.extend(_form.CARDS)
# Independent contributor content. Only new, validated stable IDs are admitted.
import community_content as _community
COMMUNITY_CARDS = _community.load(ALL)
ALL.extend(COMMUNITY_CARDS)
# Shared semantic identities and source-backed grammar readiness on EVERY
# question type. This is metadata; never overwrites user progress keys.
import pedagogy_rules as _pedagogy
for _c in ALL:_pedagogy.tag(_c)
# dlg064's housing question was independently rewritten after a commercial
# textbook overlap review. Preserve the learner-facing semantic identity so
# existing error/revision history survives this wording-only correction.
for _c in ALL:
    if _c.get("id") == "dlg064":
        _c["semanticId"] = "lex_961c9af921492376"

# Final stage-aware option banks: correct gaps and stable ids remain unchanged.
import dialogue_quality as _dialogue_quality
ORIGINAL_DIALOGUE_SNAPSHOT={c["id"]:dict(gaps=list(c["gaps"]),gr=c["gr"],bank=list(c["bank"])) for c in ALL if c["kind"]=="dialogue"}
CURATED_DIALOGUE_BANKS=_dialogue_quality.apply(ALL)
# One ambiguous legacy item remains available by ID for old student history;
# only an independently authored, unambiguous v2 is shown to new learners.
import dialogue_versioning as _dialogue_versioning
ARCHIVED_DIALOGUES=_dialogue_versioning.version(ALL)
# Publisher PDF is held by the owner and NEVER served by Core. This small
# independent ID-to-page register is reviewed against actual printed pages.
import verified_lesson_pages as _lesson_pages
VERIFIED_LESSON_PAGES=_lesson_pages.apply(ALL)

# Source-page occurrence evidence from owner's private purchased PDF.
# No PDF/image/excerpt is published; attested usage != first introduction.
import source_page_batch001 as _source_page_batch001
SOURCE_PAGE_BATCH001=_source_page_batch001.apply(ALL)

# Independent source-form occurrence batch #2: 251–500 (user-owned PDF).
# Immutable Greek card IDs and answer keys; no publisher exercise copying.
import source_page_batch002 as _source_page_batch002
SOURCE_PAGE_BATCH002=_source_page_batch002.apply(ALL)

# Owner-PDF source-page attestations batch #3: 501–750.
# Only independent ID->printed-page metadata, not publisher exercises.
import source_page_batch003 as _source_page_batch003
SOURCE_PAGE_BATCH003=_source_page_batch003.apply(ALL)

# Proven Greek headword occurrences from owner PDF in extra syllabus words.
# These are NOT certified publisher exercises.
import source_page_batch007 as _source_page_batch007
SOURCE_PAGE_BATCH007=_source_page_batch007.apply(ALL)

# Source meaning + formal/informal pedagogy checked using Translator,
# Educational Content Reviewer and Course Localization Specialist skills.
# Exact per-card, per-locale editorial overrides; independent of machine
# translated cache so Greek IDs and historic answer progress remain stable.
import editorial_localization as _editorial_localization
REVIEWED_LOCALIZATION_EDITS=_editorial_localization.apply(ALL)

# Second exact author-edited context pass, after original localization fixes.
import editorial_localization_round2 as _locale_round2
REVIEWED_LOCALIZATION_ROUND2=_locale_round2.apply(ALL)

# Keep translated prompts of derived word-order drills consistent with
# reviewed parent sentences (3 verified male/female friend corrections).
import order_translation_sync as _order_translation_sync
ORDER_TRANSLATIONS_SYNCED=_order_translation_sync.apply(ALL,langs=('ru','en','zh','es','pt'))





VERB_GROUPS=["A","B1","B2"]
import verb_curriculum as _vstage
VERB_REFERENCE=[dict(group=g,level=level,lemma=lemma,ru=ru,en=en,forms=forms,
                     introducedUnit=_vstage.first_unit(lemma))
                for g,level,lemma,ru,en,forms in _tv.VERBS]
BY_ID={c["id"]:c for c in ALL}
BY_ID.update(ARCHIVED_DIALOGUES)
assert len(ALL) >= 1795 and len(BY_ID) == len(ALL) + 1
assert all("en" in c for c in ALL)
