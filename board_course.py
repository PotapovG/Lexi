"""Account-owned, curriculum-gated board-game journey with six quests per chapter.

The legacy practice endpoint and interface are unchanged. Board tasks use the
same reviewed questions and answer scorer. Unreviewed wording is never falsely
declared a grammar error; stage progress is revision-checked under SQLite lock.
"""
import hashlib
import random

import study_tracks as tracks
import life_answer_check
import greek_life

QUESTS=("book","lexicon","verb","grammar","listening","dialogue","clock","life")
TOTAL_CHAPTERS=20
PER_CHAPTER=len(QUESTS)
LOCALIZED={
 "ru":{"book":"Учебник","lexicon":"Новые слова A1","verb":"Глаголы","grammar":"Грамматика","listening":"Аудирование","dialogue":"Диалог","clock":"Часы и время","life":"Ситуация"},
 "en":{"book":"Textbook","lexicon":"A1 vocabulary","verb":"Verbs","grammar":"Grammar","listening":"Listening","dialogue":"Dialogue","clock":"Clock time","life":"Real life"},
}
DEFAULT={"chapterLimit":6,"position":0,"wins":0,"misses":0,"skips":0,"pending":None,"hasStarted":False}


def _load(db,uid):
    s,rev=tracks._load(db,uid,"board","shared",lambda:dict(DEFAULT))
    return s,rev


def _max(s):
    return max(1,min(TOTAL_CHAPTERS,int(s["chapterLimit"])))


def _choice_pool(cards,kind,chapter,ready):
    if kind=="book":
        return [c for c in cards if c.get("chapter") in (chapter,) and c["kind"] in
                ("word","phrase","number","sentence") and ready(c)<=chapter]
    if kind=="verb":
        return [c for c in cards if c.get("kind")=="verb" and
                c.get("introducedUnit",99)<=chapter and c.get("level")=="A1"]
    if kind=="grammar":
        return [c for c in cards if c.get("chapter",99)<=chapter and
                c.get("kind") in ("article","grammar") and ready(c)<=chapter]
    if kind=="listening":
        return [c for c in cards if c.get("kind")=="listening" and c.get("chapter",99)<=chapter]
    if kind=="dialogue":
        return [c for c in cards if c.get("kind")=="dialogue" and c.get("chapter",99)<=chapter and ready(c)<=chapter]
    if kind=="clock":
        return [c for c in cards if c.get("kind")=="clock" and chapter>=6]
    return []


def _pick(candidates,uid,position,kind):
    if not candidates:return None
    canonical=sorted(candidates,key=lambda c:c["id"])
    digest=hashlib.sha256(f"{uid}:{position}:{kind}".encode()).digest()
    return canonical[int.from_bytes(digest[:8],"big")%len(canonical)]


def _quest(s,uid,lang,cards,vocab,format_question,ready,listening_on,audio_lookup):
    pos=s["position"]
    chapter=pos//PER_CHAPTER+1
    kind=QUESTS[pos%PER_CHAPTER]
    candidate_kind=kind
    if kind=="lexicon":
        # Curated A1 lexical material is intentionally supplementary to book
        # pages; does not claim that each word occurs in the chosen chapter.
        pool=[w for w in vocab if w.get("level")=="A1" and all(w.get(k) for k in ("gr",lang))]
        word=_pick(pool,uid,pos,"lexicon")
        if word:
            rng=random.Random(int.from_bytes(hashlib.sha256(f"{uid}:{pos}:options".encode()).digest()[:8],"big"))
            other=sorted({w[lang] for w in pool if w["id"]!=word["id"] and
                         tracks._normalized(w[lang])!=tracks._normalized(word[lang])})
            options=rng.sample(other,min(3,len(other)))+[word[lang]]
            rng.shuffle(options)
            return {"type":"lexicon","kind":"word","chapter":chapter,"title":kind,
                    "question":{"id":word["id"],"chapter":chapter,"kind":"lexicon","prompt":word["gr"],
                        "note":"Ελληνικά → ?","choices":options,"lang":lang,
                        "wordAudio":audio_lookup(word["gr"])}}
    if kind=="life":
        options=[c for c in greek_life.SCENES if c["chapter"]<=chapter]
        scene=_pick(options,uid,pos,"life")
        return {"type":"life","kind":"life","chapter":chapter,"title":kind,
                "question":{"id":scene["id"],"chapter":scene["chapter"],"kind":"life",
                    "prompt":scene["prompt"] if lang=="ru" else scene["promptEN"],
                    "promptLang":"ru" if lang=="ru" else "en",
                    "note":"Γράψε στα ελληνικά","lang":lang}}
    if kind=="listening" and not listening_on:candidate_kind="book"
    pool=_choice_pool(cards,candidate_kind,chapter,ready)
    if not pool and candidate_kind in ("verb","grammar","book","dialogue","clock","listening"):
        # No premature grammar: fall back to earlier, already taught words.
        pool=_choice_pool(cards,"book",chapter,ready)
        if not pool:
            pool=[c for c in cards if c.get("chapter",99)<=chapter and
                  c.get("kind") in ("word","phrase","sentence","number") and ready(c)<=chapter]
        candidate_kind="book"
    card=_pick(pool,uid,pos,candidate_kind)
    if card is None:
        raise ValueError("no_quest_material")
    direction=("gap0" if card["kind"]=="dialogue" else
               "read" if card["kind"]=="clock" else
               "conjugate" if card["kind"]=="verb" else
               "grammar_fill" if card["kind"]=="grammar" else
               "fill" if card["kind"]=="article" else
               "listen" if card["kind"]=="listening" else
               "gr-ru" if pos%2==0 else "ru-gr")
    question=format_question(card,direction,lang)
    if card["kind"]=="word" and direction=="gr-ru":
        question["wordAudio"]=audio_lookup(card["gr"])
    # The existing formatter and scorer are authoritative. Avoid unsupported
    # widgets such as letter-position tasks or word-order token arrangement.
    assert question["choices"] and question["direction"]==direction
    return {"type":"quiz","kind":card["kind"],"chapter":chapter,"title":candidate_kind,
            "question":question}


def _path(s,lang):
    names=LOCALIZED.get(lang,LOCALIZED["en"])
    limit=_max(s)*PER_CHAPTER
    nodes=[]
    for pos in range(limit):
        chapter=pos//PER_CHAPTER+1
        typ=QUESTS[pos%PER_CHAPTER]
        state=("skipped" if pos<s.get("jumpedThrough",0) else
               "completed" if pos<s["position"] else
               "current" if pos==s["position"] else "locked")
        nodes.append({"index":pos,"chapter":chapter,"type":typ,"name":names[typ],
                      "state":state})
    return nodes


def _view(s,rev,lang):
    end=s["position"]>=_max(s)*PER_CHAPTER
    return {"revision":rev,"chapterLimit":_max(s),"position":s["position"],
            "wins":s["wins"],"misses":s["misses"],"skips":s["skips"],
            "hasStarted":s["hasStarted"],"finished":end,
            "completed":min(s["position"],_max(s)*PER_CHAPTER),
            "total":_max(s)*PER_CHAPTER,"nodes":_path(s,lang),
            "quest":None if end else s.get("pending")}


def board_get(db,uid,lang,cards,vocab,formatter,ready,listening_on,audio_lookup):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    s,rev=_load(db,uid)
    if s["position"]<_max(s)*PER_CHAPTER and (s.get("pending") is None or
            s["pending"]["question"].get("lang")!=lang):
        s["pending"]=_quest(s,uid,lang,cards,vocab,formatter,ready,listening_on,audio_lookup)
        s["hasStarted"]=True
        tracks._save(db,uid,"board","shared",s,rev)
        rev+=1
    return _view(s,rev,lang)


def board_action(db,uid,lang,body,scorer):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    s,rev=_load(db,uid)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    action=body.get("action")
    if action=="scope":
        value=body.get("chapterLimit")
        if isinstance(value,bool) or not isinstance(value,int) or not 1<=value<=TOTAL_CHAPTERS:
            raise ValueError("invalid_chapter")
        s["chapterLimit"]=value
        # Changing language/scope must not leave a future-unit pending card.
        if s["position"]>=value*PER_CHAPTER:s["pending"]=None
        feedback=None
    elif action=="jump":
        to=body.get("chapter")
        if (s["position"]!=0 or not isinstance(to,int) or isinstance(to,bool) or
                not 1<=to<=_max(s)):
            raise ValueError("invalid_jump")
        s["skips"]+=(to-1)*PER_CHAPTER
        s["jumpedThrough"]=(to-1)*PER_CHAPTER
        s["position"]=(to-1)*PER_CHAPTER
        s["pending"]=None
        feedback=None
    elif action in ("answer","skip"):
        q=s.get("pending")
        if not q or s["position"]>=_max(s)*PER_CHAPTER:raise ValueError("no_active_quest")
        if body.get("questId")!=q["question"]["id"]:raise ValueError("stale_track")
        if action=="skip":
            if not s.get("canSkip"):raise ValueError("skip_not_allowed")
            s["skips"]+=1;s["position"]+=1;s["pending"]=None;s.pop("canSkip",None)
            feedback={"correct":False,"skipped":True}
        else:
            selected=body.get("selected")
            if not isinstance(selected,str) or len(selected)>500:raise ValueError("bad_answer")
            question=q["question"]
            if q["type"]=="life":
                scene=greek_life.BY_ID.get(question["id"])
                if not scene or scene["chapter"]>q["chapter"]:raise ValueError("invalid_scene")
                result=life_answer_check.evaluate(selected,scene["accepted"],lang)
                feedback={"correct":result["correct"],"unverified":result["unverified"],
                          "answer":result["closest"],"explanation":result["explanation"],
                          "translation":scene["translation"] if lang=="ru" else scene["translationEN"]}
                s["canSkip"]=bool(result["unverified"])
            elif q["type"]=="lexicon":
                if selected not in question["choices"]:raise ValueError("invalid_choice")
                word=__import__("vocab_lessons").VOCAB_BY_ID[question["id"]]
                ok=tracks._normalized(selected)==tracks._normalized(word[lang])
                feedback={"correct":ok,"answer":word[lang],
                          "explanation":None if ok else ("Запомни перевод этого слова." if lang=="ru" else "Review the meaning of this word.")}
                s["canSkip"]=False
            else:
                if selected not in question["choices"]:raise ValueError("invalid_choice")
                feedback=scorer(uid,{"id":question["id"],"direction":question["direction"],
                    "lang":lang,"selected":selected},injected_db=db)
                s["canSkip"]=False
            if feedback["correct"]:
                s["position"]+=1;s["wins"]+=1;s["pending"]=None;s.pop("canSkip",None)
            elif not feedback.get("unverified"):
                s["misses"]+=1
    else:raise ValueError("invalid_board_action")
    tracks._save(db,uid,"board","shared",s,rev)
    response=_view(s,rev+1,lang)
    response["feedback"]=feedback
    return response
