#!/usr/bin/env python3
"""Minimal, dependency-free Greek drill server. HTTP bound to localhost, HTTPS at Caddy."""
import collections
import datetime as dt
import http.cookies
import hashlib
import json
import os
import random
import re
import secrets
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from catalog_v2 import ALL, BY_ID, CHAPTERS, INDEX, TOPICS, VERB_GROUPS, VERB_REFERENCE
import auth_v1 as auth
import vocab_lessons as vocab
import verb_phrase
import personalized
import accepted_glosses
import greek_variants
import final_n_guidance
import verb_curriculum
import accent_guidance
import learning_engine
import learning_upgrade
import advanced_syllables as _syllables
import enclitic_stress as _enclitic
import grammar2_cards as _grammar2
import distractor_quality as _distractors
import lesson_audio_mix as _listen_mix
import grammar_scope_guard as _grammar_guard
import extra_sentences_20261021 as _extra_sentences
import order2_cards as _order2
import order_valid_permutations as _order_variants
import answer_idempotency
import lesson_session_sync as _lesson_sync
for _card in ALL:
    # New book-syllabus supplements ship with reviewed Arabic glosses.
    # Do not overwrite them with an English fallback from the legacy cache.
    if not _card.get("ar"):
        _card["ar"] = vocab.AR.get(_card["en"], _card["en"])

# Arabic is filled only in the server layer for historical reasons; run its
# exact editorial overrides before listening copies the source glosses.
from editorial_localization import apply as _editorial_fix_locales
REVIEWED_ARABIC_EDITS=_editorial_fix_locales(ALL,langs=("ar",))
from editorial_localization_round2 import apply as _editorial_fix_round2
REVIEWED_ARABIC_ROUND2=_editorial_fix_round2(ALL,langs=("ar",))
# Arabic source corrections are applied at server initialization, after
# catalog creation; resync the authored order-card prompts afterwards.
from order_translation_sync import apply as _sync_order_arabic
ORDER_ARABIC_TRANSLATIONS_SYNCED=_sync_order_arabic(ALL,langs=("ar",))


import listening_catalog as listening
import word_audio as _word_audio
LISTEN_CARDS=listening.build(ALL)
VOCAB_OFFLINE_AUDIO=sum(bool(_word_audio.lookup(w["gr"],listening)["audioUrl"]) for w in vocab.VOCAB)
LISTEN_BY_ID={c["id"]:c for c in LISTEN_CARDS}
EXTRA_ALL=_extra_sentences.ALL
EXTRA_BY_ID=_extra_sentences.BY_ID
SYLLABLE_ALL=_syllables.CARDS
SYLLABLE_BY_ID=_syllables.BY_ID
ENCLITIC_ALL=_enclitic.CARDS
ENCLITIC_BY_ID=_enclitic.BY_ID
ORDER2_ALL=_order2.build(ALL)
ORDER2_BY_ID={c["id"]:c for c in ORDER2_ALL}
GRAMMAR2_ALL=_grammar2.CARDS
GRAMMAR2_BY_ID=_grammar2.BY_ID
PRACTICE_ALL=ALL+EXTRA_ALL+SYLLABLE_ALL+ENCLITIC_ALL+GRAMMAR2_ALL+ORDER2_ALL
_ORDER_VARIANT_COUNT=_order_variants.validate({**BY_ID,**ORDER2_BY_ID})
def book_or_audio_card(cid):
    return BY_ID.get(cid) or EXTRA_BY_ID.get(cid) or SYLLABLE_BY_ID.get(cid) or ENCLITIC_BY_ID.get(cid) or GRAMMAR2_BY_ID.get(cid) or ORDER2_BY_ID.get(cid) or LISTEN_BY_ID.get(cid)

ROOT = Path(__file__).parent
DB = os.environ.get("GREEK_DB", "/var/lib/greek-trainer/progress.sqlite3")
ORIGIN = "https://potapovfamily.com"
COOKIE = "greek_session"
KINDS = ("word", "number", "letter", "phrase", "plural", "sentence", "accent", "verb", "dialogue", "article", "order", "syllable", "enclitic", "grammar", "listening")
DIRECTIONS = ("mixed", "gr-ru", "ru-gr")
COUNT_MAX = 60
LISTENING_ENABLED=True # approved complete six-voice offline audio set

def conn():
    db = sqlite3.connect(DB, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout=10000")
    return db

def init_db():
    with conn() as db:
        db.execute("PRAGMA journal_mode=WAL")
        db.executescript("""
        CREATE TABLE IF NOT EXISTS attempts (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id TEXT NOT NULL,
          card_key TEXT NOT NULL,
          kind TEXT NOT NULL,
          unit INTEGER NOT NULL,
          correct INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS ix_attempts_user_time ON attempts(user_id,id);
        CREATE INDEX IF NOT EXISTS ix_attempts_created ON attempts(created_at,user_id);
        CREATE TABLE IF NOT EXISTS leaderboard_members (
          user_id TEXT PRIMARY KEY,
          joined_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS progress (
          user_id TEXT NOT NULL,
          card_key TEXT NOT NULL,
          attempts INTEGER NOT NULL DEFAULT 0,
          correct INTEGER NOT NULL DEFAULT 0,
          miss_debt INTEGER NOT NULL DEFAULT 0,
          updated_at TEXT NOT NULL,
          PRIMARY KEY (user_id,card_key)
        );
        """)
    with conn() as db:
        answer_idempotency.schema(db)
        _lesson_sync.schema(db)
        auth.schema(db)
        vocab.schema(db)
        learning_engine.schema(db)

def allowed_kinds(s):
    xs = [i for i in s.split(",") if i in KINDS]
    return set(xs) if xs else {"word","number","phrase","sentence"}

def card_key(card, direction, lang="ru"):
    # Keep original keys stable to preserve Russian learning history.
    suffix="" if (lang=="ru" or card["kind"] in ("accent","dialogue","article","order","syllable","enclitic","grammar")) else ":"+lang
    return card["id"]+":"+direction+suffix

def shape(card, direction, lang="ru"):
    if card['kind']=='listening':
        if direction!='listen':raise ValueError('invalid listening direction')
        prompt,note=listening.LABELS[lang]
        return prompt,card[lang],note
    if card['kind']=='grammar':
        if direction!='grammar_fill':raise ValueError('invalid grammar direction')
        return card['prompt'],card['correct'],card[lang]
    if card['kind']=='enclitic':
        if direction!='stress_enclitic':raise ValueError('invalid enclitic direction')
        return f"{card['article']} {card['noun']} + {card['pronoun']}",card['correct'],card[lang]
    if card['kind']=='syllable':
        if direction!='stress_syllable':raise ValueError('invalid syllable direction')
        choices=[str(i+1)+" · "+part for i,part in enumerate(card['plainParts'])]
        return ' · '.join(card['plainParts']),choices[card['stressedIndex']],card[lang]
    if card['kind']=='article':
        if direction!='fill':raise ValueError('invalid article direction')
        return card['prompt'],card['correct'],card[lang]
    if card['kind']=='order':
        if direction!='arrange':raise ValueError('invalid word order direction')
        notes={'ru':'Собери греческое предложение из слов в правильном порядке.',
               'en':'Arrange the Greek words into the correct sentence.',
               'zh':'将希腊语单词排列成正确的句子。',
               'ar':'رتّب الكلمات اليونانية لتكوين جملة صحيحة.',
               'es':'Ordena las palabras griegas para formar la frase correcta.',
               'pt':'Ordena as palavras gregas para formar a frase correta.'}
        return card[lang],card['gr'],notes[lang]
    if card["kind"]=="dialogue":
        index=int(direction[3:])
        return card["gr"],card["gaps"][index],"Greek dialogue"
    if card["kind"] == "verb":
        if direction=="translate":
            g,translated=verb_phrase.phrase(card,lang)
            return g,translated,"Μετάφρασε όλη την πρόταση / Translate the whole sentence"
        return card["personName"]+"  ____  ("+card["gr"]+")",card["forms"][card["person"]],card["group"]+" · "+card[lang]
    if card["kind"] == "accent":
        label = {"ru":"Выбери букву для ударения","en":"Choose the letter to accent",
                 "zh":"请选择应加重音符号的字母","ar":"اختر حرف النبرة", "so":"Dooro xarafka lahjadda saaran tahay",
                 "es":"Elige la letra que lleva tilde","pt":"Escolhe a letra com acento"}[lang]
        return card["base"], card["accented"], label+" · "+card[lang]
    if card["kind"] == "plural":
        label={
            "ru":("Множественное число: ","Единственное число: ","Формы числа"),
            "en":("Plural: ","Singular: ","Noun forms"),
            "zh":("复数：","单数：","名词单复数"),
            "ar":("الجمع: ","المفرد: ","صيغ الأسماء"),
            "so":("Jamac: ","Keli: ","Qaababka magacyada"),
            "es":("Plural: ","Singular: ","Formas del sustantivo"),
            "pt":("Plural: ","Singular: ","Formas do substantivo")
        }[lang]
        if direction == "sg-pl":return label[0]+card["sg"],card["pl"],label[2]
        return label[1]+card["pl"],card["sg"],label[2]
    translated=card[lang]
    names={"ru":"русский","en":"English","zh":"中文","ar":"العربية","so":"Soomaali","es":"Español","pt":"Português"}
    if direction=="gr-ru":return card["gr"],translated,"Ελληνικά → "+names[lang]
    return translated,card["gr"],names[lang]+" → Ελληνικά"

def generate_options(card,direction,answer,lang):
    """Eight distinct choices, favoring *learned* morphologically plausible decoys.

    Early A1 cards should not use obvious B1/A2 words simply to reach eight
    options. Source-explainable priorities: same unit, same part of speech,
    comparable Greek morphology/length, with modest controlled shuffle.
    When few sentence items exist, earlier short phrases are permitted as
    fallback; never score a different synonym as an incorrect distractor.
    """
    kind=card['kind']
    if kind=='listening':
        source=BY_ID[card['sourceId']]
        accepted=set(accepted_glosses.accepted(source,'gr-ru',lang,answer))
        pool=[c for c in LISTEN_CARDS if c['id']!=card['id'] and c['en'].casefold()!=card['en'].casefold()]
        random.shuffle(pool)
        pool.sort(key=lambda c:(c['chapter']!=card['chapter'],
                                 c['sourceKind']!=card['sourceKind'],
                                 abs(len(c['gr'])-len(card['gr']))))
        pairs=[(answer,card['en'])];seen=set(accepted)
        for other in pool:
            value=other[lang]
            if value in seen:continue
            seen.add(value);pairs.append((value,other['en']))
            if len(pairs)==8:break
        if len(pairs)!=8:raise ValueError('listening distractors unavailable')
        random.shuffle(pairs)
        return [p[0] for p in pairs],[p[1] for p in pairs]
    allowed={kind}
    if kind=='sentence':allowed.add('phrase')
    if kind=='phrase':allowed.add('sentence')
    pool=[c for c in PRACTICE_ALL if c['kind'] in allowed and c['id']!=card['id']]
    current_unit=max(0,card.get('curriculum_ready_unit',card['chapter']))
    # Stable pedagogical ranking with a little shuffled tie noise. This
    # prioritizes similar, taught morphology and topic, not arbitrary words.
    random.shuffle(pool)
    pool.sort(key=lambda c:_distractors.rank(card,c,lang,current_unit,random.random()))
    pairs=[(answer,card.get('en',''))]
    allowed=accepted_glosses.accepted(card,direction,lang,answer)
    if len(allowed)>1:
        # Some language questions really have more than one correct gloss.
        # Render one documented alternate in the bank and accept *either*.
        pairs.append((allowed[1],card.get('en','')))
    seen={_distractors.norm(value) for value in allowed}
    for other in pool:
        # Same publisher gloss or curated Greek spelling alternatives are
        # not correct "wrong" answers and must not be shown as decoys.
        if (_distractors.same_english_meaning(card,other) or
            _distractors.same_sense_or_variant(card,other)):continue
        try:choice=shape(other,direction,lang)[1]
        except (ValueError,KeyError):continue
        normalized=_distractors.norm(choice)
        if choice and normalized and normalized not in seen:
            pairs.append((choice,other.get('en','')))
            seen.add(normalized)
        if len(pairs)==8:break
    if len(pairs)!=8:raise ValueError('Not enough distinct answer choices')
    random.shuffle(pairs)
    return [x[0] for x in pairs],[x[1] for x in pairs]

def parse_options(params):
    lang=params.get("lang",["ru"])[0]
    if lang not in ("ru","en","zh","ar","es","pt"): lang="ru"
    mode=params.get("mode",["all"])[0]
    kinds=allowed_kinds(params.get("types",["word,number,phrase,sentence"])[0])
    try:
        page_from=max(1,min(312,int(params.get("from",["1"])[0])))
        page_to=max(page_from,min(312,int(params.get("to",["56"])[0])))
    except (ValueError,TypeError):
        page_from,page_to=1,56
    chapters_raw=params.get("chapters",[""])[0]
    if chapters_raw:
        try: chapters={int(x) for x in chapters_raw.split(",")} & {chapter["id"] for chapter in CHAPTERS if chapter["id"]>0}
        except ValueError:chapters=set()
    else:chapters=None
    try:count=max(1,min(COUNT_MAX,int(params.get("count",["60"])[0])))
    except ValueError:count=60
    exclude=set(params.get("exclude",[""])[0].split(","))
    return lang,mode,kinds,page_from,page_to,chapters,count,exclude


def valid_weak_entries(user_id, display_lang="ru"):
    """Return recoverable due answers, preserving the language of each old key.

    Legacy IDs and unsupported old locales remain in the SQLite history but
    must not count as actionable or produce a dead-end practice session.
    """
    with conn() as db:
        rows=db.execute("""SELECT card_key,miss_debt,attempts FROM progress
                           WHERE user_id=? AND miss_debt>0
                           ORDER BY miss_debt DESC, updated_at DESC""",(user_id,)).fetchall()
        results=[]
        for row in rows:
            key=row["card_key"]
            bits=key.split(":")
            if len(bits) not in (2,3):continue
            cid,direction=bits[:2]
            card=book_or_audio_card(cid)
            if card is None and cid.startswith("personal_"):
                wid=cid[len("personal_"):]
                if wid in vocab.VOCAB_BY_ID and personalized.is_learned(db,user_id,wid):
                    card=personalized.to_card(vocab.VOCAB_BY_ID[wid])
            if not card:continue
            if card['kind']=='listening' and not LISTENING_ENABLED:continue
            elif card['kind']=='listening':allowed={'listen'}
            elif card['kind']=='article':allowed={'fill'}
            elif card['kind']=='order':allowed={'arrange'}
            elif card["kind"]=="dialogue":
                allowed={f"gap{i}" for i in range(len(card["gaps"]))}
            elif card["kind"]=="verb":
                allowed={"conjugate","translate"}
            elif card["kind"]=="accent":allowed={"accent"}
            elif card["kind"]=="syllable":allowed={"stress_syllable"}
            elif card["kind"]=="enclitic":allowed={"stress_enclitic"}
            elif card["kind"]=="grammar":allowed={"grammar_fill"}
            elif card["kind"]=="plural":allowed={"sg-pl","pl-sg"}
            else:allowed={"gr-ru","ru-gr"}
            if direction not in allowed:continue
            source_lang=bits[2] if len(bits)==3 else ("ru" if card["kind"] not in ("accent","dialogue","article","order","syllable","enclitic","grammar") else display_lang)
            if source_lang not in ("ru","en","zh","ar","es","pt"):continue
            if card_key(card,direction,source_lang)!=key:continue
            results.append(dict(card=card,direction=direction,lang=source_lang,
                                key=key,missDebt=row["miss_debt"],attempts=row["attempts"]))
    return results,len(rows)


def format_question(card,direction,lang,weak=False,variant_index=None):
    """One canonical question renderer for all normal/scoped/global review modes."""
    prompt,correct,note=shape(card,direction,lang)
    item=dict(id=card["id"],direction=direction,kind=card["kind"],unit=card["unit"],
              chapter=card["chapter"],page=card["page"],topic=card["topic"],prompt=prompt,
              note=note,lang=lang,semanticId=card.get("semanticId",card["id"]),
              sourcePageVerified=bool(card.get("book_page_verified",False)))
    if card['kind'] not in ('article','order','dialogue','accent','verb','enclitic','grammar') and len(accepted_glosses.accepted(card,direction,lang,correct))>1:
        item['multipleValid']=True
    # Greek variant metadata never replaces canonical printed spelling or stable ID.
    # Accent task tests a letter position on printed spelling only; its
    # lexical alternative is displayed AFTER answering, not as a score index.
    canonical_greek=(card.get('accented') if card['kind']=='accent' else
                     card.get('sg') if card['kind']=='plural' and direction=='pl-sg' else
                     card.get('pl') if card['kind']=='plural' else card.get('gr',''))
    item['greekVariants']=greek_variants.variants(canonical_greek)
    if card['kind']=='grammar':
        item['choices']=random.sample(card['options'],len(card['options']))
        item['grammarGroup']=card['group']
    if card['kind']=='enclitic':
        item['choices']=random.sample(card['options'],len(card['options']))
        item['wordAudio']=_word_audio.lookup(card['correct'],listening)
        item['hasExtraStress']=card['hasExtraStress']
    if card['kind'] in ('accent','syllable'):
        spelling=card.get('accented') if card['kind']=='accent' else card['gr']
        item['wordAudio']=_word_audio.lookup(spelling,listening)
    if card['kind'] in ('enclitic','grammar'):
        pass  # curated Greek-only morphology options, not translation distractors
    elif card['kind']=='listening':
        variant=(card['audioVariants'][variant_index%2] if variant_index is not None else random.choice(card['audioVariants']))
        item['audioUrl']='/greek/audio/'+variant['file']
        item['audioVoice']=variant['voice']
        item['audioStyle']=variant['style']
        item['listeningDifficulty']=card['sourceKind']
        item['choices'],en=generate_options(card,direction,correct,lang)
        if lang!='en':item['choicesEn']=en
    elif card['kind']=='syllable':
        item['choices']=[str(i+1)+" · "+part for i,part in enumerate(card['plainParts'])]
        item['syllableCount']=card['syllableCount']
        item['syllables']=list(card['plainParts'])
    elif card['kind']=='article':
        item['choices']=list(card['options'])
        random.shuffle(item['choices'])
        item['note']=card[lang]
        if len(card.get('acceptedForms',[]))>1:
            item['articleSpellingVariant']=True
    elif card['kind']=='order':
        item['alternativeOrderCount']=len(_order_variants.VARIANTS.get(card['id'],()))
        item['tokens']=list(card['tokens'])
        random.shuffle(item['tokens'])
        item['note']=shape(card,direction,lang)[2]
        if lang!='en':item['promptEn']=card['en']
    elif card["kind"]=="accent":
        item["letters"]=list(card["base"])
        item["tonosHint"]=accent_guidance.accents(card,lang)
        item["accentableIndices"]=[i for i,ch in enumerate(card["base"]) if ch.lower() in "αεηιουω"]
        assert card["accent_index"] in item["accentableIndices"]
    elif card["kind"]=="dialogue":
        item["dialogueLines"]=card["lines"]
        item["dialogueGaps"]=card["gaps"]
        # Every student sees a new order; no answer-position leak from the
        # historically ordered bank (some original correct entries were first).
        item["choices"]=random.sample(card["bank"],k=len(card["bank"]))
        item["gapIndices"]=[int(direction[3:])] if weak else list(range(len(card["gaps"])))
        item["note"]="dialogue"
    elif card["kind"]=="verb":
        item["choices"],_=generate_options(card,direction,correct,lang)
        item["introducedUnit"]=card["introducedUnit"]
        item["verbGroup"]=card["group"]
        item["personName"]=card["personName"]
        item["phrasePrompt"],item["phraseChoices"],item["phraseChoicesEn"]=verb_phrase.options(card,lang,ALL)
    else:
        item["choices"],en_choices=generate_options(card,direction,correct,lang)
        if lang!="en" and direction=="gr-ru":
            item["choicesEn"]=en_choices
        if lang!="en" and direction=="ru-gr":
            item["promptEn"]=card["en"]
    return item


def estimate_capacity(user_id,params):
    """Read-only unique-target estimate at 20 seconds per item.

    Reuses the same material filters as make_quiz; targets are counted by
    semantic identity, never translation direction or cloned review ID.
    """
    import math
    lang,mode,kinds,first,last,chapters,count,exclude=parse_options(params)
    scope=params.get("scope",["pages"])[0]
    levels=set(params.get("levels",["A1,A2"])[0].split(","))&{"A1","A2"}
    groups=set(params.get("groups",["A,B1,B2"])[0].split(","))&set(VERB_GROUPS)
    if scope=="listening" and not LISTENING_ENABLED:
        return dict(uniqueCards=0,requiredAt20Seconds=0,durationMinutes=0,
                    estimatedMinutesAt20Seconds=0,enoughAt20Seconds=False,
                    approximate=False,unavailable="listening_alpha_disabled")
    deferred_for_grammar=0
    if scope=="listening":
        pool=[x for x in LISTEN_CARDS if x['sourceKind'] in kinds
              and ((x["chapter"] in chapters) if chapters is not None else first<=x["page"]<=last)]
    elif scope=="verbs":
        max_unit=verb_curriculum.selected_max(params.get("maxUnit",["4"])[0])
        pool=[x for x in ALL if x["kind"]=="verb" and x["group"] in groups
              and x["level"] in levels and x["introducedUnit"]<=max_unit]
    elif scope=="topics":
        topics=set(params.get("topics",[""])[0].split(","))
        pool=[x for x in ALL if x["kind"] in kinds and x.get("level") in levels
              and set(x.get("topics",[]))&topics]
    else:
        pool=[x for x in PRACTICE_ALL if x["kind"] in kinds and x.get("curriculum") not in ("topic","verb")
              and ((x["chapter"] in chapters) if chapters is not None else (first<=x["page"]<=last))]
        stage=_grammar_guard.max_taught_unit(chapters,first,last,CHAPTERS)
        pool,deferred_for_grammar=_grammar_guard.filter_ready(pool,stage)
        if params.get("study",["textbook"])[0]=="personalized":
            with conn() as db:pool+=personalized.learned_cards(db,user_id)
    audio_options=(_listen_mix.candidates(LISTEN_CARDS,kinds,chapters,first,last,exclude)
        if scope not in ("listening","topics","verbs") and params.get('listenMix',['0'])[0]=='1'
        and mode not in ('weak','weak_all','srs_due') and LISTENING_ENABLED else [])
    available=len({x.get("semanticId",x["id"]) for x in pool})
    try:duration=max(10,min(60,int(params.get("duration",["20"])[0])))
    except (ValueError,TypeError):duration=20
    with conn() as db:pace,observations=learning_engine.pace_seconds(db,user_id)
    need=math.ceil(duration*60/pace)
    with conn() as db:
        task_projection=learning_upgrade.capacity_projection(db,user_id,pool,duration)
    return dict(uniqueCards=available,requiredAt20Seconds=need,durationMinutes=duration,
                estimatedMinutesAt20Seconds=round(available*pace/60,1),
                enoughAt20Seconds=available>=need,approximate=True,
                paceSeconds=pace,personalizedPace=observations>=12,paceObservations=observations,
                grammarDeferred=deferred_for_grammar,
                listeningMixEnabled=params.get('listenMix',['0'])[0]=='1',
                listeningMixAvailable=len(audio_options),
                **task_projection)


def make_srs_due_quiz(user_id,params,display_lang,count,exclude):
    """Opt-in scheduled answer-direction review; never serves another account's data."""
    with conn() as db:
        rows=learning_engine.due_entries(db,user_id)
        questions=[]
        for row in rows:
            key=row['card_key']
            if key in exclude:continue
            bits=key.split(':')
            if len(bits) not in (2,3):continue
            cid,direction=bits[:2]
            card=book_or_audio_card(cid)
            if card is None and cid.startswith('personal_'):
                wid=cid[len('personal_'):]
                if wid in vocab.VOCAB_BY_ID and personalized.is_learned(db,user_id,wid):
                    card=personalized.to_card(vocab.VOCAB_BY_ID[wid])
            if not card or card['kind']=='listening' and not LISTENING_ENABLED:continue
            lang=bits[2] if len(bits)==3 else (
                display_lang if card['kind'] in ('accent','dialogue','article','order','syllable') else 'ru')
            if lang not in ('ru','en','zh','ar','es','pt'):continue
            if card_key(card,direction,lang)!=key:continue
            try:
                shape(card,direction,lang)
                questions.append(format_question(card,direction,lang,weak=True,
                    variant_index=row['attempts']%2 if card['kind']=='listening' else None))
            except (ValueError,IndexError,KeyError,TypeError):continue
            if len(questions)>=count:break
    return dict(questions=questions,available=len(rows),count=len(questions),
                mode='srs_due',pagePrecision='approximate',lang=display_lang)


def make_global_weak_quiz(user_id,params,display_lang,count,exclude):
    entries,total=valid_weak_entries(user_id,display_lang)
    questions=[]
    for row in entries:
        if row["key"] in exclude:continue
        questions.append(format_question(row["card"],row["direction"],row["lang"],weak=True,
            variant_index=row["attempts"]%2 if row["card"]["kind"]=="listening" else None))
        if len(questions)>=count:break
    return dict(questions=questions,available=len(entries),unavailable=total-len(entries),
                count=len(questions),mode="weak_all",pagePrecision="approximate",lang=display_lang)


def make_quiz(user_id,params):
    lang,mode,kinds,first,last,chapters,count,exclude=parse_options(params)
    if mode=="weak_all":
        return make_global_weak_quiz(user_id,params,lang,count,exclude)
    if mode=="srs_due":
        return make_srs_due_quiz(user_id,params,lang,count,exclude)
    scope=params.get("scope",["book"])[0]
    levels=set(params.get("levels",["A1,A2"])[0].split(",")) & {"A1","A2"}
    topics=set(params.get("topics",[""])[0].split(","))
    groups=set(params.get("groups",["A,B1,B2"])[0].split(",")) & set(VERB_GROUPS)
    deferred_for_grammar=0
    if scope=="listening":
        if not LISTENING_ENABLED:raise ValueError("listening_alpha_disabled")
        cards=[c for c in LISTEN_CARDS if c['sourceKind'] in kinds and
               ((c["chapter"] in chapters) if chapters is not None else first<=c["page"]<=last)]
    elif scope=="topics":
        cards=[c for c in ALL if c["kind"] in kinds and c.get("level") in levels and
               (set(c.get("topics",[])) & topics)]
    elif scope=="verbs":
        max_unit=verb_curriculum.selected_max(params.get("maxUnit",["4"])[0])
        cards=[c for c in ALL if c["kind"]=="verb" and c["group"] in groups and
               c["level"] in levels and c["introducedUnit"]<=max_unit]
    else:
        cards=[c for c in PRACTICE_ALL if c["kind"] in kinds and c.get("curriculum") not in ("topic","verb") and
               ((c["chapter"] in chapters) if chapters is not None else (first<=c["page"]<=last))]
    if scope not in ("listening","topics","verbs"):
        stage=_grammar_guard.max_taught_unit(chapters,first,last,CHAPTERS)
        cards,deferred_for_grammar=_grammar_guard.filter_ready(cards,stage)
    study=params.get("study",["textbook"])[0]
    personal_cards=[]
    if study=="personalized" and scope not in ("verbs","topics","listening"):
        with conn() as db:personal_cards=personalized.learned_cards(db,user_id)
        cards+=personal_cards
    with conn() as db:
        records=db.execute("SELECT card_key,miss_debt,attempts FROM progress WHERE user_id=?",(user_id,)).fetchall()
    debts={x["card_key"]:x["miss_debt"] for x in records}
    attempt_counts={x["card_key"]:x["attempts"] for x in records}
    choices=[]
    # Alternate both language directions for regular drills, while weak-mode
    # remains keyed to the precise failed direction.
    random.shuffle(cards)
    for card in cards:
        # The strict normal session is semantic-identity based: never show the
        # same word again just because its direction/kind/ID changed. Weak
        # practice deliberately continues to use precise answer-direction IDs.
        if mode not in ("weak",) and (card["id"] in exclude or card.get("semanticId") in exclude):
            continue
        directions=(tuple(f"gap{i}" for i in range(len(card["gaps"]))) if card["kind"]=="dialogue" else
                    ("conjugate",) if card["kind"]=="verb" else ("grammar_fill",) if card["kind"]=="grammar" else ("stress_enclitic",) if card["kind"]=="enclitic" else ("stress_syllable",) if card["kind"]=="syllable" else ("accent",) if card["kind"]=="accent" else
                    ("listen",) if card['kind']=='listening' else
                ("fill",) if card['kind']=='article' else ("arrange",) if card['kind']=='order' else
                    (("sg-pl","pl-sg") if card["kind"]=="plural" else ("gr-ru","ru-gr")))
        if mode=="weak":
            due=[d for d in directions if debts.get(card_key(card,d,lang),0)>0]
            if not due:continue
            direction=max(due,key=lambda d:debts.get(card_key(card,d,lang),0))
        else:
            direction="gap0" if card["kind"]=="dialogue" else random.choice(directions)
        key=card_key(card,direction,lang)
        if key in exclude:continue
        score=10*debts.get(key,0)+max(0,5-attempt_counts.get(key,0))
        choices.append((card,direction,score))
    random.shuffle(choices)
    if mode=="weak":
        choices.sort(key=lambda x:-x[2])
    else:
        # Priority plus randomness to avoid serving the same top cards forever.
        choices.sort(key=lambda x:-x[2]+random.uniform(-15,15))
    if mode!="weak" and params.get("adaptive",["0"])[0]=="1":
        with conn() as db:learning_engine.adaptive_order(db,user_id,choices)
    if mode!="weak":
        unique=[]
        used=set()
        for card,direction,score in choices:
            fingerprint=card.get("semanticId",card["id"])
            if fingerprint in used:continue
            used.add(fingerprint)
            unique.append((card,direction,score))
        choices=unique
    # Guarantee that mastered course words aren't crowded out by fresh textbook cards.
    if personal_cards and mode!="weak":
        learned=[x for x in choices if x[0].get("curriculum")=="personalized"]
        textbook=[x for x in choices if x[0].get("curriculum")!="personalized"]
        random.shuffle(learned)
        slots=max(1,min(len(learned),count//3))
        mix=[]
        for i in range(count):
            if i%3==2 and learned and slots>0:
                mix.append(learned.pop(0));slots-=1
            elif textbook:mix.append(textbook.pop(0))
            elif learned:mix.append(learned.pop(0))
            else:break
        choices=mix
    questions=[]
    for index,(card,direction,score) in enumerate(choices[:count]):
        if mode!="weak" and card["kind"] not in ("plural","accent","syllable","enclitic","grammar","verb","dialogue","article","order","listening"):
            direction=("gr-ru","ru-gr")[index%2]  # guaranteed mixed translation directions per batch
        if mode!="weak" and card["kind"]=="plural":
            direction=("sg-pl","pl-sg")[index%2]
        key=card_key(card,direction,lang)
        if key in exclude:
            # Previous-session exclusions apply to the final direction too.
            if card["kind"] in ("accent","syllable","enclitic","grammar","verb","dialogue","article","order","listening"):continue
            other=("ru-gr" if direction=="gr-ru" else "gr-ru") if card["kind"]!="plural" else ("pl-sg" if direction=="sg-pl" else "sg-pl")
            if card_key(card,other,lang) in exclude:continue
            direction=other
        questions.append(format_question(card,direction,lang,weak=mode=="weak",
            variant_index=attempt_counts.get(card_key(card,direction,lang),0)%2 if card["kind"]=="listening" else None))
    audio_options=(_listen_mix.candidates(LISTEN_CARDS,kinds,chapters,first,last,exclude)
        if scope not in ("listening","topics","verbs") and params.get('listenMix',['0'])[0]=='1'
        and mode not in ('weak','weak_all','srs_due') and LISTENING_ENABLED else [])
    mixed_count=_listen_mix.mix(questions,audio_options,book_or_audio_card,format_question,lang)
    return dict(questions=questions,available=len(choices),count=len(questions),mode=mode,
                mixedListening=mixed_count,mixedListeningAvailable=len(audio_options),
                grammarDeferred=deferred_for_grammar,grammarGate="curriculum_ready_unit",
                pagePrecision="approximate",lang=lang)

_syllables_hints={
'ru':'Ударение на слоге {index} из {total}: «{breakdown}» (слово «{greek}»).',
'en':'Syllable {index} of {total} is stressed: “{breakdown}” (“{greek}”).',
'zh':'重音在第 {index}/{total} 个音节：“{breakdown}”（{greek}）。',
'ar':'النبر على المقطع {index} من {total}: «{breakdown}» («{greek}»).',
'es':'El acento va en la sílaba {index} de {total}: «{breakdown}» («{greek}»).',
'pt':'O acento está na sílaba {index} de {total}: «{breakdown}» («{greek}»).',
}
def mark(user_id,body,injected_db=None):
    cid=body.get("id")
    direction=body.get("direction")
    selected=body.get("selected")
    lang=body.get("lang","ru")
    if lang not in ("ru","en","zh","ar","es","pt"): raise ValueError("invalid language")
    card=book_or_audio_card(cid) if isinstance(cid,str) else None
    if isinstance(cid,str) and cid.startswith("personal_"):
        wid=cid[len("personal_"):]
        with conn() as db:
            if wid in vocab.VOCAB_BY_ID and personalized.is_learned(db,user_id,wid):
                card=personalized.to_card(vocab.VOCAB_BY_ID[wid])
    if card and card["kind"]=="listening" and not LISTENING_ENABLED:
        raise ValueError("listening_alpha_disabled")
    if not card or not isinstance(selected,str) or len(selected)>500:
        raise ValueError("invalid answer")
    directions=(tuple(f"gap{i}" for i in range(len(card["gaps"]))) if card["kind"]=="dialogue" else ("conjugate","translate") if card["kind"]=="verb" else ("grammar_fill",) if card["kind"]=="grammar" else ("stress_enclitic",) if card["kind"]=="enclitic" else ("stress_syllable",) if card["kind"]=="syllable" else ("accent",) if card["kind"]=="accent" else
                ("listen",) if card['kind']=='listening' else
                ("fill",) if card['kind']=='article' else ("arrange",) if card['kind']=='order' else
                (("sg-pl","pl-sg") if card["kind"]=="plural" else ("gr-ru","ru-gr")))
    if direction not in directions:raise ValueError("invalid direction")
    correct_answer=shape(card,direction,lang)[1]
    if card['kind']=='grammar':
        if selected not in card['options']:raise ValueError('invalid grammar form')
        correct=selected==correct_answer
    elif card['kind']=='enclitic':
        if selected not in card['options']:raise ValueError('invalid enclitic variant')
        correct=selected==correct_answer
    elif card["kind"]=="syllable":
        options=[str(i+1)+" · "+part for i,part in enumerate(card["plainParts"])]
        if selected not in options:raise ValueError("invalid syllable answer")
        correct=selected==correct_answer
    elif card["kind"]=="accent":
        if not selected.isdecimal() or len(selected)>3 or int(selected)>=len(card["base"]):
            raise ValueError("invalid stress position")
        correct=int(selected)==card["accent_index"]
    else:
        correct=selected in card["accepted"] if card["kind"]=="verb" and direction=="conjugate" else \
                (selected in card['acceptedForms'] if card['kind']=='article' else
                 accepted_glosses.is_accepted(BY_ID[card['sourceId']],'gr-ru',lang,selected,correct_answer)
                 if card['kind']=='listening' else
                 accepted_glosses.is_accepted(card,direction,lang,selected,correct_answer))
    if card['kind']=='order':
        correct=_order_variants.matches(card,selected)
    if card["kind"]=="dialogue" and card["id"]=="dlg024":
        correct=selected in [x for x in card["bank"] if x.casefold()==correct_answer.casefold()]
    key=card_key(card,direction,lang)
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if injected_db is None:
        with conn() as own_db:
            return mark(user_id,body,injected_db=own_db)
    db=injected_db
    row=db.execute("SELECT attempts,correct,miss_debt FROM progress WHERE user_id=? AND card_key=?",
                   (user_id,key)).fetchone()
    if row:
        miss_debt=max(0,row["miss_debt"]-1) if correct else min(7,row["miss_debt"]+2)
        db.execute("""UPDATE progress SET attempts=attempts+1,correct=correct+?,miss_debt=?,updated_at=?
                       WHERE user_id=? AND card_key=?""",(int(correct),miss_debt,now,user_id,key))
    else:
        miss_debt=0 if correct else 2
        db.execute("""INSERT INTO progress(user_id,card_key,attempts,correct,miss_debt,updated_at)
                      VALUES(?,?,?,?,?,?)""",(user_id,key,1,int(correct),miss_debt,now))
    db.execute("""INSERT INTO attempts(user_id,card_key,kind,unit,correct,created_at)
                  VALUES(?,?,?,?,?,?)""",(user_id,key,card["kind"],card["unit"],int(correct),now))
    srs_info=(learning_engine.update(db,user_id,key,correct,now)
              if body.get('srsOptIn') is True else None)
    result=dict(correct=correct,answer=correct_answer,missDebt=miss_debt)
    if card['kind']=='order':
        result['acceptedOrderCount']=len(_order_variants.all_valid(card))
    if srs_info:result.update(srs_info)
    if not correct:
        result['explanation']=learning_upgrade.selected_explanation(card,direction,lang,correct_answer,selected)
    if card["kind"]=="dialogue" and card["id"]=="dlg024":
        result["acceptedAnswers"]=[x for x in card["bank"] if x.casefold()==correct_answer.casefold()]
    if card['kind']=='listening':
        result['transcript']=card['gr']
        result['acceptedAnswers']=accepted_glosses.accepted(BY_ID[card['sourceId']],'gr-ru',lang,correct_answer)
    if card['kind']=='article':
        result['acceptedAnswers']=list(card['acceptedForms'])
        result['preferredAnswer']=card['correct']
        if len(card['acceptedForms'])>1:
            result['spellingNote']=final_n_guidance.explanation(card,lang)
            result['acceptedVariant']=correct and selected!=correct_answer
    if direction in ('gr-ru','ru-gr','sg-pl','pl-sg'):
        result['acceptedAnswers']=accepted_glosses.accepted(card,direction,lang,correct_answer)
    # Expose variants after scoring, including accent and listening prompts.
    source_greek=(card.get('accented') if card['kind']=='accent' else
                  correct_answer if card['kind']=='plural' else card.get('gr',''))
    variants=greek_variants.variants(source_greek)
    if variants:result['greekVariants']=variants
    if card['kind']=='grammar':
        result['grammarTip']=card[lang]
        if not correct:result['explanation']=card[lang]+' → '+correct_answer
    if card['kind']=='enclitic':
        result['hasExtraStress']=card['hasExtraStress']
        result['tonosHint']=_enclitic.explanation(card,lang)
    if card["kind"]=="syllable":
        result["correctIndex"]=card["stressedIndex"]
        result["syllableBreakdown"]="-".join(card["parts"])
        result["tonosHint"]=_syllables_hints[lang].format(
            index=card["stressedIndex"]+1,total=card["syllableCount"],
            greek=card["gr"],breakdown="-".join(card["parts"]))
    if card["kind"]=="accent":
        result["correctIndex"]=card["accent_index"]
        result["tonosHint"]=accent_guidance.accents(card,lang)
    if card["kind"]=="verb" and direction=="conjugate":
        result["conjugation"]={"group":card["group"],"lemma":card["gr"],
                               "persons":list(__import__("topics_verbs").PEOPLE),
                               "forms":card["forms"],"accepted":card["accepted"],
                               "person":card["person"]}
    return result

def stats(user_id):
    with conn() as db:
        rows = db.execute("SELECT card_key,kind,unit,correct,created_at FROM attempts WHERE user_id=? ORDER BY id DESC LIMIT 20000",(user_id,)).fetchall()
        prog = db.execute("SELECT card_key,attempts,correct,miss_debt FROM progress WHERE user_id=?",
                          (user_id,)).fetchall()
    total = len(rows)
    good = sum(r["correct"] for r in rows)
    streak = 0
    for row in rows:
        if not row["correct"]:break
        streak+=1
    categories = {}
    for kind in KINDS:
        rr = [r for r in rows if r["kind"]==kind]
        categories[kind] = {"attempts":len(rr),"correct":sum(r["correct"] for r in rr)}
    # Historical attempts.unit contains the old internal 16-unit topic ID.
    # Recalculate against the stable card ID to display the true 20 printed
    # textbook units without changing/deleting a single saved attempt.
    units = {}
    by_unit=collections.defaultdict(list)
    for r in rows:
        cid=r["card_key"].split(":",1)[0]
        current=book_or_audio_card(cid)
        current_unit=current["chapter"] if current else r["unit"]
        by_unit[current_unit].append(r)
    for c in CHAPTERS:
        rr=by_unit.get(c["id"],[])
        units[str(c["id"])] = {"attempts":len(rr),"correct":sum(r["correct"] for r in rr)}
    daily = collections.defaultdict(lambda:{"attempts":0,"correct":0})
    for row in rows:
        day=row["created_at"][:10]
        daily[day]["attempts"]+=1
        daily[day]["correct"]+=row["correct"]
    debt = sorted((dict(r) for r in prog if r["miss_debt"] > 0),
                  key=lambda x:(-x["miss_debt"],x["correct"]))
    detailed=learning_engine.detailed_mastery(rows,book_or_audio_card)
    detailed.update(learning_upgrade.knowledge_breakdown(rows,book_or_audio_card))
    valid,total_weak=valid_weak_entries(user_id)
    with conn() as db:
        srs_status=learning_engine.status(db,user_id)
        detailed['vocabTopics']=learning_upgrade.vocabulary_knowledge(db,user_id,vocab.VOCAB_BY_ID)
    actionable={x["key"] for x in valid}
    archive_count=total_weak-len(valid)
    return {
        "attempts":total,"correct":good,"accuracy":round(100*good/total) if total else 0,
        "streak":streak,"studied":len(prog),"weak":len(valid),
        "weakOverall":total_weak,"weakUnavailable":archive_count,"srs":srs_status,
        "recentAccuracy":round(100*sum(r["correct"] for r in rows[:30])/len(rows[:30])) if rows else 0,
        "categories":categories,"units":units,
        "mastery":learning_engine.mastery(rows,book_or_audio_card),
        "details":detailed,
        "daily":[{"date":d,**daily[d]} for d in sorted(daily)[-14:]],
        "weakest":[{"key":r["card_key"],"missDebt":r["miss_debt"],"attempts":r["attempts"]}
                    for r in debt if r["card_key"] in actionable][:12],
        "catalog":{kind:(len(LISTEN_CARDS) if kind=="listening" else
                         sum(c["kind"]==kind for c in PRACTICE_ALL)) for kind in KINDS}
    }

# No real names or cookie IDs are exposed to the leaderboard.
ADJECTIVES=[
("Сонный","Sleepy"),("Зачётный","Legendary"),("Хитрый","Clever"),
("Кофейный","Caffeinated"),("Вечный","Eternal"),("Голодный","Hungry"),
("Ленивый","Lazy"),("Невозмутимый","Unshaken"),("Секретный","Secret"),
("Гениальный","Genius"),("Растрёпанный","Messy"),("Отважный","Brave"),
("Тревожный","Nervous"),("Непобедимый","Unstoppable"),("Греческий","Greek"),
("Забывчивый","Forgetful"),("Полуночный","Midnight"),("Упрямый","Stubborn"),
("Магический","Magical"),("Случайный","Random"),("Загадочный","Mysterious"),
("Проверенный","Certified"),("Сдающий","Exam-ready"),("Читающий","Studious")]
NOUNS=[
("Аспирант","Postgrad"),("Профессор","Professor"),("Бакалавр","Bachelor"),
("Первокурсник","Freshman"),("Декан","Dean"),("Студент","Student"),
("Библиотекарь","Librarian"),("Конспект","Notebook"),("Зачёт","Credit"),
("Семинар","Seminar"),("Учебник","Textbook"),("Лектор","Lecturer"),
("Филолог","Philologist"),("Шпаргалист","Cheat-sheet Ace"),
("Экзаменатор","Examiner"),("Алфавит","Alphabet"),("Сократ","Socrates"),
("Платон","Plato"),("Диплом","Diploma"),("Словарь","Dictionary"),
("Переводчик","Translator"),("Лингвист","Linguist"),
("Абитуриент","Applicant"),("Зубрила","Bookworm")]
AVATARS=["🎓","📚","✍️","☕","🤓","📝","🏛️","📖","🔤","🧠"]

def pseudonym(user_id):
    digest=hashlib.blake2s(user_id.encode("ascii"),digest_size=16).digest()
    a=ADJECTIVES[int.from_bytes(digest[:2],"big")%len(ADJECTIVES)]
    n=NOUNS[int.from_bytes(digest[2:4],"big")%len(NOUNS)]
    suffix=digest.hex()[-4:].upper()
    return dict(name=a[0]+" "+n[0]+" ·"+suffix,
                english=a[1]+" "+n[1]+" ·"+suffix,
                avatar=AVATARS[digest[4]%len(AVATARS)])

def leaderboard(user_id):
    # Rolling 7 days. Active time is an estimate based on answer events,
    # not the time an idle browser tab stays open.
    now=dt.datetime.now(dt.timezone.utc)
    since=(now-dt.timedelta(days=7)).isoformat(timespec="seconds")
    with conn() as db:
        account_names={r["user_id"]:r["nickname"] for r in db.execute("SELECT user_id,nickname FROM accounts")}
        joined_users={r["user_id"] for r in db.execute("SELECT user_id FROM leaderboard_members")}
        rows=db.execute("""SELECT a.user_id,a.created_at,a.correct
                 FROM attempts a INNER JOIN leaderboard_members m ON m.user_id=a.user_id
                 WHERE a.created_at>=? ORDER BY a.user_id,a.created_at,a.id""",(since,)).fetchall()
        debt={r["user_id"]:r["n"] for r in db.execute(
            """SELECT p.user_id,COUNT(*) AS n FROM progress p
               INNER JOIN leaderboard_members m ON m.user_id=p.user_id
               WHERE p.miss_debt>0 GROUP BY p.user_id""")}
    totals={uid:dict(seconds=0,answers=0,correct=0,last=None) for uid in joined_users}
    for row in rows:
        uid=row["user_id"]
        entry=totals.setdefault(uid,dict(seconds=0,answers=0,correct=0,last=None))
        when=dt.datetime.fromisoformat(row["created_at"])
        if when.tzinfo is None:when=when.replace(tzinfo=dt.timezone.utc)
        delta=(when-entry["last"]).total_seconds() if entry["last"] else 9999
        # New activity burst gets estimated 20s; gaps <=120s count at most 90s.
        entry["seconds"]+=20 if delta>120 else min(90,max(0,int(delta)))
        entry["answers"]+=1
        entry["correct"]+=int(row["correct"])
        entry["last"]=when
    ranked=[]
    for uid,e in totals.items():
        nick=pseudonym(uid)
        if uid in account_names:
            nick["name"]=account_names[uid]
            nick["english"]=account_names[uid]
        ranked.append(dict(**nick,seconds=e["seconds"],minutes=round(e["seconds"]/60,1),
                          answers=e["answers"],correct=e["correct"],
                          errors=e["answers"]-e["correct"],
                          accuracy=round(100*e["correct"]/e["answers"]) if e["answers"] else 0,
                          weak=debt.get(uid,0),isMe=uid==user_id))
    ranked.sort(key=lambda x:(-x["seconds"],-x["answers"],-x["correct"],x["name"]))
    for index,row in enumerate(ranked,1):row["rank"]=index
    mine=next((dict(r) for r in ranked if r["isMe"]),None)
    return dict(period="rolling-7-days",timeMethod="answer-activity-estimate",
                members=len(joined_users),activeMembers=sum(bool(r["answers"]) for r in ranked),
                joined=user_id in joined_users,rows=ranked[:40],me=mine,
                updatedAt=now.isoformat(timespec="seconds"))

class Handler(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    def log_message(self, *args):
        pass
    def identity(self):
        cookie=http.cookies.SimpleCookie()
        try: cookie.load(self.headers.get("Cookie",""))
        except http.cookies.CookieError: pass
        existing=cookie.get(COOKIE)
        if existing and re.fullmatch(r"[a-f0-9]{32}",existing.value):
            return existing.value,False
        return secrets.token_hex(16),True
    def respond(self, status, body, ctype, fresh_cookie=False, user_id=None, cache=False):
        self.send_response(status)
        self.send_header("Content-Type",ctype)
        self.send_header("Content-Length",str(len(body)))
        if self.close_connection:
            self.send_header("Connection","close")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("X-Frame-Options","DENY")
        self.send_header("Cache-Control","public, max-age=300" if cache else "no-store")
        self.send_header("Content-Security-Policy","default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; media-src 'self'; img-src 'self' data:; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        if fresh_cookie and user_id:
            self.send_header("Set-Cookie",f"{COOKIE}={user_id}; Path=/greek/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax")
        self.end_headers()
        self.wfile.write(body)
    def send_json(self,status, payload, fresh_cookie=False,user_id=None):
        self.respond(status,json.dumps(payload,ensure_ascii=False).encode("utf-8"),
                     "application/json; charset=utf-8",fresh_cookie,user_id)
    def do_HEAD(self):
        path = urlparse(self.path).path
        if path=="/tts-demo/pocket-short" or path.startswith("/tts-demo/pocket-short/"):
            return self.serve_pocket_short_demo("/tts-demo/pocket-short/" if path=="/tts-demo/pocket-short" else path,head=True)
        if path=="/tts-demo/pocket-long" or path.startswith("/tts-demo/pocket-long/"):
            return self.serve_pocket_long_demo("/tts-demo/pocket-long/" if path=="/tts-demo/pocket-long" else path,head=True)
        if path=="/tts-demo/pocket" or path.startswith("/tts-demo/pocket/"):
            return self.serve_pocket_demo("/tts-demo/pocket/" if path=="/tts-demo/pocket" else path,head=True)
        if path=="/tts-demo/mms" or path.startswith("/tts-demo/mms/"):
            return self.serve_mms_demo("/tts-demo/mms/" if path=="/tts-demo/mms" else path,head=True)

        if path.startswith('/audio/'):
            return self.send_audio(path[len('/audio/'):],head=True)
        if path.startswith('/pronunciation/'):
            return self.send_pronunciation(path[len('/pronunciation/'):],head=True)
        files = {"/":"index.html","/index.html":"index.html",
                 "/app.js":"app.js","/vocab.js":"vocab.js","/greek_word_audio.js":"greek_word_audio.js","/styles.css":"styles.css"}
        filename = files.get(path)
        if filename:
            file = ROOT / filename
            kind = ("text/html" if filename.endswith(".html")
                    else "text/javascript" if filename.endswith(".js") else "text/css")
            self.send_response(200)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(file.stat().st_size))
            self.send_header("X-Content-Type-Options","nosniff")
            self.send_header("Cache-Control","no-store")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Length","0")
            self.end_headers()
    def serve_pocket_short_demo(self,route,head=False):
        """Read-only audited six-voice short speech samples; unrelated to ALPHA."""
        allowed={"index.html","style.css","short-samples.zip"}
        allowed.update(f"{voice}_{style}_{kind}.wav" for voice in
                       ("athina","eleni","katerina","kostas","spyros","nikos")
                       for style in ("clear","lively")
                       for kind in ("word","phrase","sentence"))
        name=route[len("/tts-demo/pocket-short/"):] or "index.html"
        if name not in allowed:
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        path=ROOT/"tts-evaluation-pocket"/"short-tests"/name
        if not path.is_file():
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        mime=("audio/wav" if name.endswith(".wav") else
              "application/zip" if name.endswith(".zip") else
              "text/css; charset=utf-8" if name.endswith(".css") else
              "text/html; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type",mime)
        self.send_header("Content-Length",str(path.stat().st_size))
        self.send_header("Cache-Control","public, max-age=600")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Content-Security-Policy","default-src 'none'; style-src 'self'; media-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        if name.endswith(".zip"):
            self.send_header("Content-Disposition","attachment; filename=pocket-greek-short-qa.zip")
        self.end_headers()
        if not head:self.wfile.write(path.read_bytes())

    def serve_pocket_long_demo(self,route,head=False):
        # Standalone Pocket Greek quality comparison. Not student listening.
        allowed={"index.html","style.css","all-six.zip","all-voices.zip"}
        allowed.update(voice+"_"+style+".wav" for voice in
                       ("athina","kostas","eleni","katerina","spyros","nikos")
                       for style in ("01_default","02_clear_phrases","03_lively_phrases"))
        allowed.update(("mms_04_even.wav","mms_05_expressive.wav"))
        name=route[len("/tts-demo/pocket-long/"):] or "index.html"
        if name not in allowed:
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        file=ROOT/"tts-evaluation-pocket"/"long-tests"/name
        if not file.is_file():
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        mime=("audio/wav" if name.endswith(".wav") else
              "application/zip" if name.endswith(".zip") else
              "text/css; charset=utf-8" if name.endswith(".css") else
              "text/html; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type",mime)
        self.send_header("Content-Length",str(file.stat().st_size))
        self.send_header("Cache-Control","public, max-age=600")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Content-Security-Policy","default-src 'none'; style-src 'self'; media-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        if name.endswith(".zip"):
            self.send_header("Content-Disposition","attachment; filename="+
                             ("pocket-greek-voices-comparison.zip" if name=="all-voices.zip"
                              else "pocket-greek-clarity-test.zip"))
        self.end_headers()
        if not head:self.wfile.write(file.read_bytes())

    def serve_pocket_demo(self,route,head=False):
        # Narrow 8-preset comparison, separate from disabled student ALPHA.
        allowed={"index.html","style.css","eight-voices.zip"}
        allowed.update(name+".wav" for name in (
            "eleni","athina","katerina","sophia",
            "spyros","kostas","nikos","giorgos"))
        name=route[len("/tts-demo/pocket/"):] or "index.html"
        if name not in allowed:
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        source=ROOT/"tts-evaluation-pocket"/"samples"/name
        if not source.is_file():
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        mime=("audio/wav" if name.endswith(".wav") else "application/zip" if name.endswith(".zip")
              else "text/css; charset=utf-8" if name.endswith(".css") else "text/html; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type",mime)
        self.send_header("Content-Length",str(source.stat().st_size))
        self.send_header("Cache-Control","public, max-age=600")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Content-Security-Policy","default-src 'none'; style-src 'self'; media-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        if not head:self.wfile.write(source.read_bytes())

    def serve_mms_demo(self, route, head=False):
        # Narrow public comparison preview, distinct from DISABLED listening.
        allowed={"index.html","style.css","all-five.zip",
                 "01_original.wav","02_slow.wav","03_fast.wav",
                 "04_even.wav","05_expressive.wav"}
        filename=route[len("/tts-demo/mms/"):] or "index.html"
        if filename not in allowed:
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        f=ROOT/"tts-evaluation-mms"/"outputs"/filename
        if not f.is_file():
            self.send_response(404);self.send_header("Content-Length","0");self.end_headers();return
        mime=("audio/wav" if filename.endswith(".wav") else
              "application/zip" if filename.endswith(".zip") else
              "text/css; charset=utf-8" if filename.endswith(".css") else
              "text/html; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type",mime)
        self.send_header("Content-Length",str(f.stat().st_size))
        self.send_header("Cache-Control","public, max-age=600")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Content-Security-Policy","default-src 'none'; style-src 'self'; media-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        if filename.endswith(".zip"):
            self.send_header("Content-Disposition","attachment; filename=lexi-mms-tts-greek-5-samples.zip")
        self.end_headers()
        if not head:self.wfile.write(f.read_bytes())

    def send_pronunciation(self,filename,head=False):
        # No arbitrary filesystem paths: manifest-verified content hashes only.
        import pronunciation_audio as pre
        source=pre.BY_FILE.get(filename)
        if source is None or not source.is_file():
            self.send_response(404)
            self.send_header("Content-Length","0")
            self.send_header("X-Content-Type-Options","nosniff")
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type","audio/wav")
        self.send_header("Content-Length",str(source.stat().st_size))
        self.send_header("Cache-Control","public, max-age=31536000, immutable")
        self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers()
        if not head:self.wfile.write(source.read_bytes())

    def send_audio(self,filename,head=False):
        if not LISTENING_ENABLED:
            self.send_response(410);self.send_header("Content-Length","0");self.end_headers();return
        source=listening.AUDIO.get(filename)
        if source is None or not source.is_file():
            self.send_response(404)
            self.send_header("Content-Length","0")
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type","audio/wav")
        self.send_header("Content-Length",str(source.stat().st_size))
        self.send_header("Cache-Control","public, max-age=31536000, immutable")
        self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers()
        if not head:self.wfile.write(source.read_bytes())

    def do_GET(self):
        path=urlparse(self.path).path
        if path=="/tts-demo/pocket-short" or path.startswith("/tts-demo/pocket-short/"):
            return self.serve_pocket_short_demo("/tts-demo/pocket-short/" if path=="/tts-demo/pocket-short" else path)
        if path=="/tts-demo/pocket-long" or path.startswith("/tts-demo/pocket-long/"):
            return self.serve_pocket_long_demo("/tts-demo/pocket-long/" if path=="/tts-demo/pocket-long" else path)
        if path=="/tts-demo/pocket" or path.startswith("/tts-demo/pocket/"):
            return self.serve_pocket_demo("/tts-demo/pocket/" if path=="/tts-demo/pocket" else path)
        if path=="/tts-demo/mms" or path.startswith("/tts-demo/mms/"):
            return self.serve_mms_demo("/tts-demo/mms/" if path=="/tts-demo/mms" else path)

        if path.startswith('/audio/'):
            return self.send_audio(path[len('/audio/'):])
        if path.startswith('/pronunciation/'):
            return self.send_pronunciation(path[len('/pronunciation/'):])
        if path=="/health":
            return self.send_json(200,{"status":"ok"})
        token,new=self.identity()
        with conn() as db:account=auth.current(db,token)
        uid=account["user_id"] if account else token
        if path=="/api/profile":
            return self.send_json(200,dict(registered=bool(account),
                 nickname=account["nickname"] if account else None,
                 avatar=pseudonym(uid)["avatar"] if account else None),new,token)
        if path in ("/api/quiz","/api/capacity","/api/stats","/api/leaderboard","/api/vocab/lesson","/api/personalized/status","/api/srs/status","/api/session") and not account:
            return self.send_json(401,{"error":"login_required"},new,token)
        if path=="/api/session":
            with conn() as db:result=_lesson_sync.read(db,uid)
            return self.send_json(200,result,new,uid)
        if path=="/api/srs/status":
            with conn() as db:result=learning_engine.status(db,uid)
            return self.send_json(200,result,new,token)
        if path=="/api/personalized/status":
            with conn() as db:summary=personalized.progress_summary(db,uid)
            return self.send_json(200,summary,new,token)
        if path=="/api/vocab/meta":
            groups=[dict(**t, count=sum(t["id"] in w["topics"] for w in vocab.VOCAB),
                  a1=sum(t["id"] in w["topics"] and w["level"]=="A1" for w in vocab.VOCAB),
                  a2=sum(t["id"] in w["topics"] and w["level"]=="A2" for w in vocab.VOCAB))
                  for t in vocab.THEMES]
            return self.send_json(200,dict(count=len(vocab.VOCAB),levels={"A1":sum(w["level"]=="A1" for w in vocab.VOCAB),"A2":sum(w["level"]=="A2" for w in vocab.VOCAB)},topics=groups,offlineAudioWords=VOCAB_OFFLINE_AUDIO,
                 audioMode="pocket_offline_only",microphoneEnabled=False,
                 source="Independent authored and book-aligned teaching words. Editorial A1/A2 labels; not CEFR-certified."),new,token)
        if path=="/api/vocab/lesson":
            try:
                qp=parse_qs(urlparse(self.path).query)
                with conn() as db:
                    output=vocab.lesson(db,uid,qp.get("topic",["all"])[0],qp.get("level",["A1"])[0],
                      qp.get("lang",["ru"])[0],qp.get("review",["0"])[0]=="1")
                for word in output['words']:
                    word['wordAudio']=_word_audio.lookup(word['gr'],listening)
                return self.send_json(200,output,new,token)
            except ValueError:return self.send_json(400,{"error":"invalid lesson query"},new,token)
        if path=="/api/capacity":
            try:
                return self.send_json(200,estimate_capacity(uid,parse_qs(urlparse(self.path).query)),new,uid)
            except Exception:
                return self.send_json(500,{"error":"capacity estimate unavailable"},new,uid)
        if not LISTENING_ENABLED and path=="/api/quiz" and parse_qs(urlparse(self.path).query).get("scope")==["listening"]:
            return self.send_json(503,{"error":"listening_alpha_disabled"},new,uid)
        if path=="/api/quiz":
            try:
                result=make_quiz(uid,parse_qs(urlparse(self.path).query))
                return self.send_json(200,result,new,uid)
            except Exception:
                return self.send_json(500,{"error":"quiz unavailable"},new,uid)
        if path=="/api/stats":
            return self.send_json(200,stats(uid),new,uid)
        if path=="/api/leaderboard":
            return self.send_json(200,leaderboard(uid),new,uid)
        if path=="/api/topic-words":
            if not account:return self.send_json(401,{"error":"login_required"},new,token)
            qp=parse_qs(urlparse(self.path).query)
            categories=set(qp.get("topics",[""])[0].split(",")) & {x["id"] for x in TOPICS}
            levels=set(qp.get("levels",["A1,A2"])[0].split(",")) & {"A1","A2"}
            lang=qp.get("lang",["ru"])[0]
            if lang not in ("ru","en","zh","ar","es","pt"):lang="ru"
            words=[c for c in ALL if c["kind"]=="word" and c.get("level") in levels and
                   set(c.get("topics",[])) & categories]
            unique={}
            for card in words:
                unique.setdefault(card["gr"],dict(gr=card["gr"],translation=card[lang],
                                                   level=card["level"]))
            output=sorted(unique.values(),key=lambda c:(c["level"],c["gr"]))
            return self.send_json(200,dict(count=len(output),words=output[:300]),new,token)
        if path=="/api/topics":
            counts={t["id"]:sum(t["id"] in c.get("topics",[]) and c["kind"]=="word" for c in ALL) for t in TOPICS}
            return self.send_json(200,dict(topics=TOPICS,counts=counts,levels=["A1","A2"],
                               groups=VERB_GROUPS,verbs=VERB_REFERENCE),new,token)
        if path=="/api/catalog":
            counts={c["id"]:sum(x["chapter"]==c["id"] for x in PRACTICE_ALL) for c in CHAPTERS}
            printed_sections=[c for c in CHAPTERS if c["id"] not in (0,-5)]
            listening_units=[dict(c,id=i) for i,c in enumerate(sorted(printed_sections,key=lambda c:c["start"]),1)]
            assert len(listening_units)==20
            return self.send_json(200,dict(chapters=CHAPTERS,counts=counts,
                 types=list(KINDS),languages=["ru","en","zh","ar","es","pt"],pages=312,cardCount=len(ALL),supplementalCount=len(EXTRA_ALL),
                 practiceCardCount=len(PRACTICE_ALL),supplementalSentences=18,supplementalOrder=8,
                 supplementalSyllables=len(SYLLABLE_ALL),
                 supplementalEnclitics=len(ENCLITIC_ALL),supplementalGrammar=len(GRAMMAR2_ALL),supplementalOrder2=len(ORDER2_ALL),
                 listeningCount=len(LISTEN_CARDS) if LISTENING_ENABLED else 0,
                 listeningAlpha=not LISTENING_ENABLED,listeningAvailable=LISTENING_ENABLED,
                 listeningVoices=list(listening.APPROVED) if LISTENING_ENABLED else [],
                 listeningByKind={name:sum(c['sourceKind']==name for c in LISTEN_CARDS) for name in ('word','phrase','sentence')} if LISTENING_ENABLED else {},
                 listeningChapters=listening_units,
                 listeningByChapter={str(n):sum(x["chapter"]==n for x in LISTEN_CARDS) for n in range(1,21)},
                 printedUnits=20,reviewUnits=[5,10,15,20],pdfOffset=2,
                 pagePrecision="approximate",source="Verified printed unit start/end and pedagogy from uploaded Patakis PDF; independently authored practice questions, approximate within-unit page anchors"),new,uid)
        files={"/":"index.html","/index.html":"index.html","/app.js":"app.js","/vocab.js":"vocab.js","/greek_word_audio.js":"greek_word_audio.js","/styles.css":"styles.css"}
        file=files.get(path)
        if file:
            b=(ROOT/file).read_bytes()
            mimetype="text/html; charset=utf-8" if file.endswith(".html") else (
                "text/javascript; charset=utf-8" if file.endswith(".js") else "text/css; charset=utf-8")
            return self.respond(200,b,mimetype,new,uid,cache=False)
        self.send_json(404,{"error":"not found"},new,uid)
    def do_POST(self):
        path=urlparse(self.path).path
        if path not in ("/api/answer","/api/leaderboard/join","/api/leaderboard/leave",
                         "/api/auth/register","/api/auth/login","/api/auth/logout",
                         "/api/vocab/answer","/api/session"):
            self.close_connection=True  # Avoid leaving unread POST bodies on reused HTTP/1.1 connections.
            return self.send_json(404,{"error":"not found"})
        if self.headers.get("Origin") != ORIGIN:
            self.close_connection=True
            return self.send_json(403,{"error":"bad origin"})
        if self.headers.get("Content-Type","").split(";")[0]!="application/json":
            self.close_connection=True
            return self.send_json(415,{"error":"JSON required"})
        try:
            size=int(self.headers.get("Content-Length","0"))
            if size<2 or size>(260000 if path=="/api/session" else 2048): raise ValueError("body size")
            body=json.loads(self.rfile.read(size))
            if not isinstance(body,dict):raise ValueError("body type")
            token,new=self.identity()
            if path=="/api/auth/register":
                address=(self.headers.get("X-Forwarded-For","").split(",")[0].strip()
                         or self.client_address[0])
                with conn() as db:registration=auth.register(db,token,body.get("nickname"),address)
                return self.send_json(200,{"registered":True,"nickname":registration["nickname"],
                                           "code":registration["code"]},True,registration["token"])
            if path=="/api/auth/login":
                # We only listen on loopback behind two trusted Caddy reverse proxies.
                address=(self.headers.get("X-Forwarded-For","").split(",")[0].strip()
                         or self.client_address[0])
                with conn() as db:session=auth.login(db,body.get("code"),address)
                return self.send_json(200,{"registered":True,"nickname":session["nickname"]},
                                      True,session["token"])
            with conn() as db:account=auth.current(db,token)
            if not account:return self.send_json(401,{"error":"login_required"},new,token)
            uid=account["user_id"]
            if path=="/api/auth/logout":
                with conn() as db:auth.logout(db,token)
                return self.send_json(200,{"loggedOut":True},True,secrets.token_hex(16))
            if path=="/api/session":
                with conn() as db:result=_lesson_sync.action(db,uid,body)
                return self.send_json(200,result,new,uid)
            if path=="/api/vocab/answer":
                with conn() as db:return self.send_json(200,vocab.answer(db,uid,body),new,uid)
            if path in ("/api/leaderboard/join","/api/leaderboard/leave"):
                with conn() as db:
                    if path.endswith("/join"):
                        db.execute("INSERT OR IGNORE INTO leaderboard_members(user_id,joined_at) VALUES (?,?)",
                                   (uid,dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
                    else:
                        db.execute("DELETE FROM leaderboard_members WHERE user_id=?",(uid,))
                return self.send_json(200,{"joined":path.endswith("/join")},new,uid)
            return self.send_json(200,answer_idempotency.score_once(conn,mark,uid,body,validate_attempt=_lesson_sync.assert_owner),new,uid)
        except (ValueError,json.JSONDecodeError) as error:
            self.close_connection=True
            reason=str(error)
            status=429 if reason=="rate_limited" else 409 if reason in ("nickname_taken","already_registered","session_conflict") else 401 if reason=="invalid_credentials" else 400
            return self.send_json(status,{"error":reason if reason in ("nickname_invalid","nickname_taken","already_registered","invalid_credentials","rate_limited","session_conflict") else "invalid request"})
        except Exception:
            self.close_connection=True
            return self.send_json(500,{"error":"write failed"})

if __name__=="__main__":
    init_db()
    port=int(os.environ.get("GREEK_PORT","18560"))
    ThreadingHTTPServer(("127.0.0.1",port),Handler).serve_forever()

