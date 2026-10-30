"""Lexi lessons v2: eight LOCKED multi-question lessons per chapter/round.

Existing board v1 steps are archived without pretending they represent
completed 5–10 minute lessons. The unchanged Classic API owns quiz scoring;
new lessons store separate, server-authoritative progress and error backlog.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import random
import time

import greek_life
import life_answer_check
import study_tracks as tracks

FAMILIES=("book","lexicon","verb","grammar","listening","dialogue","clock","life")
PER_CHAPTER=8
MAX_CHAPTER=20
TARGETS=(14,14,12,12,12,12,12,10)
TITLE={
    "ru":{"book":"Учебник и фразы","lexicon":"Слова уровня A1",
          "verb":"Глаголы в действии","grammar":"Грамматика",
          "listening":"Слушаем греческий","dialogue":"Разговоры",
          "clock":"Часы и расписание","life":"Реальная жизнь"},
    "en":{"book":"Textbook and phrases","lexicon":"A1 vocabulary",
          "verb":"Verbs in action","grammar":"Grammar",
          "listening":"Greek listening","dialogue":"Conversations",
          "clock":"Time and schedules","life":"Everyday life"}
}
DEFAULT={"schema":2,"chapterLimit":6,"position":0,"lessons":[],"backlog":{},
         "skips":0,"hasStarted":False,"active":None,"legacyBoard":None,"roundSeen":[]}

def _now():
    return dt.datetime.now(dt.timezone.utc)

def _stamp(now=None):
    return (now or _now()).isoformat(timespec="seconds")

def _elapsed(start,end):
    try:
        return max(0,int((dt.datetime.fromisoformat(end)-dt.datetime.fromisoformat(start)).total_seconds()))
    except (TypeError,ValueError):return 0

def _load(db,uid):
    s,revision=tracks._load(db,uid,"board","shared",lambda:dict(DEFAULT))
    if s.get("schema")==2:
        s.setdefault("roundSeen",[])
        return s,revision,False
    # v1's one-question board moves are not the equivalent of full lessons.
    # Archive all old counters and choose the chapter previously reached.
    old=dict(s)
    chapter=min(int(old.get("chapterLimit",6)),MAX_CHAPTER,
                max(1,int(old.get("position",0))//PER_CHAPTER+1))
    fresh=dict(DEFAULT)
    fresh.update(chapterLimit=int(old.get("chapterLimit",6)),
                 position=(chapter-1)*PER_CHAPTER,skips=(chapter-1)*PER_CHAPTER,
                 legacyBoard=old,hasStarted=False)
    return fresh,revision,True

def _cap(s):
    return max(1,min(MAX_CHAPTER,int(s["chapterLimit"])))

def _rng(uid,pos,slot,tag):
    digest=hashlib.sha256(f"lexi-lessons-2:{uid}:{pos}:{slot}:{tag}".encode()).digest()
    return random.Random(int.from_bytes(digest[:8],"big"))

def _pick(pool,rng,seen):
    options=[card for card in pool if card["id"] not in seen]
    if not options:return None
    return options[rng.randrange(len(options))]

def _meta(s,pos,lang):
    chapter=pos//PER_CHAPTER+1
    family=FAMILIES[pos%PER_CHAPTER]
    name=TITLE.get(lang,TITLE["en"])[family]
    if family=="clock" and chapter<6:
        name="Практика фраз" if lang=="ru" else "Phrase practice"
    if family=="grammar" and chapter<4:
        name="Повторение языка" if lang=="ru" else "Language review"
    if family=="verb" and chapter<2:
        name="Повторение слов" if lang=="ru" else "Word review"
    return dict(index=pos,chapter=chapter,family=family,
                name=name,
                target=TARGETS[pos%PER_CHAPTER])

def _candidates(family,chapter,cards,ready,listening_on):
    def early(c):return c.get("chapter",99)<=chapter and ready(c)<=chapter
    base=[c for c in cards if c.get("kind") in ("word","number","phrase","sentence")
          and early(c)]
    if family=="book":
        exact=[c for c in base if c["chapter"]==chapter]
        return exact+ [c for c in base if c["chapter"]!=chapter]
    if family=="verb":
        primary=[c for c in cards if c["kind"]=="verb" and
                 c.get("introducedUnit",99)<=chapter and c.get("level")=="A1"]
    elif family=="grammar":
        primary=[c for c in cards if c["kind"] in ("grammar","article") and early(c)]
    elif family=="listening":
        primary=[c for c in cards if c["kind"]=="listening" and early(c)] if listening_on else []
    elif family=="dialogue":
        primary=[c for c in cards if c["kind"]=="dialogue" and early(c)]
    elif family=="clock":
        primary=[c for c in cards if c["kind"]=="clock"] if chapter>=6 else []
    else:
        primary=[]
    # Fallback never introduces grammar beyond chapter, and prevents
    # a 1-card 'lesson' when an early chapter has few verb forms.
    return primary+base

def _direction(card,rng):
    kind=card["kind"]
    if kind=="dialogue":return "gap0"
    if kind=="clock":return "read"
    if kind=="verb":return "conjugate"
    if kind=="grammar":return "grammar_fill"
    if kind=="article":return "fill"
    if kind=="listening":return "listen"
    return rng.choice(("gr-ru","ru-gr"))

def _lexicon(vocab,uid,pos,slot,lang,audio,seen):
    words=[w for w in vocab if w.get("level")=="A1" and w.get(lang) and w["id"] not in seen]
    if not words:return None
    rng=_rng(uid,pos,slot,"vocab")
    word=_pick(words,rng,seen)
    others={tracks._normalized(word[lang])}
    distractors=[]
    for item in sorted(words,key=lambda w:w["id"]):
        val=item[lang]
        normalized=tracks._normalized(val)
        if normalized not in others:
            distractors.append(val);others.add(normalized)
    if len(distractors)<3:return None
    opts=rng.sample(distractors,3)+[word[lang]]
    rng.shuffle(opts)
    return dict(type="lexicon",id=word["id"],kind="lexicon",chapter=pos//PER_CHAPTER+1,
                family="lexicon",direction="gr-ru",prompt=word["gr"],choices=opts,
                lang=lang,note="Ελληνικά → ?",wordAudio=audio(word["gr"]))

def _life_scene(uid,pos,slot,chapter,lang,seen):
    choices=[s for s in greek_life.SCENES if s["chapter"]<=chapter and s["id"] not in seen]
    if not choices:return None
    rng=_rng(uid,pos,slot,"life")
    scene=_pick(choices,rng,seen)
    return dict(type="life",id=scene["id"],kind="life",chapter=scene["chapter"],
                family="life",prompt=scene["prompt"] if lang=="ru" else scene["promptEN"],
                promptLang="ru" if lang=="ru" else "en",lang=lang)

def _as_question(card,uid,pos,slot,lang,fmt,audio):
    direction=_direction(card,_rng(uid,pos,slot,"direction"))
    q=fmt(card,direction,lang)
    if card["kind"]=="word" and direction=="gr-ru":
        q["wordAudio"]=audio(card["gr"])
    q["type"]="quiz"
    return q

def _review_candidates(s,chapter,cards,vocab,lang,fmt,audio):
    by_id={c["id"]:c for c in cards}
    word_by_id={w["id"]:w for w in vocab}
    choices=[]
    for key,info in s["backlog"].items():
        if not info.get("due") or info.get("chapter",99)>chapter:continue
        if info["kind"]=="lexicon" and info["id"] in word_by_id:
            choices.append((info["id"],info))
        elif info["kind"]=="life" and info["id"] in greek_life.BY_ID and greek_life.BY_ID[info["id"]]["chapter"]<=chapter:
            choices.append((info["id"],info))
        elif info["id"] in by_id and by_id[info["id"]]["kind"] not in ("order","accent","syllable","enclitic"):
            choices.append((info["id"],info))
    choices.sort(key=lambda x:(-x[1]["errors"],x[1]["lastWrong"],x[0]))
    return choices

def _build_lesson(s,uid,lang,cards,vocab,fmt,ready,listening_on,audio):
    pos=s["position"]
    meta=_meta(s,pos,lang)
    chapter=meta["chapter"];family=meta["family"];target=meta["target"]
    pool=_candidates(family,chapter,cards,ready,listening_on)
    used=set();items=[]
    # Two review questions per ordinary lesson; a dedicated review backlog
    # is also surfaced in summaries. Do not expose future syllabus content.
    by_id={c["id"]:c for c in cards}
    word_by_id={w["id"]:w for w in vocab}
    for rid,info in _review_candidates(s,chapter,cards,vocab,lang,fmt,audio)[:2]:
        if len(items)>=target:break
        if info["kind"]=="life" and rid in greek_life.BY_ID:
            scene=greek_life.BY_ID[rid]
            q=dict(type="life",id=rid,kind="life",chapter=scene["chapter"],
                   family="life",prompt=scene["prompt"] if lang=="ru" else scene["promptEN"],
                   promptLang="ru" if lang=="ru" else "en",lang=lang)
        elif info["kind"]=="lexicon" and rid in word_by_id:
            q=_lexicon(vocab,uid,pos,len(items),lang,audio,used)
            if q is None or q["id"]!=rid:
                word=word_by_id[rid]
                rng=_rng(uid,pos,len(items),"review")
                distractors=sorted({w[lang] for w in vocab if w.get("level")=="A1" and
                                   w.get(lang) and tracks._normalized(w[lang])!=tracks._normalized(word[lang])})
                if len(distractors)<3:continue
                opts=rng.sample(distractors,3)+[word[lang]];rng.shuffle(opts)
                q=dict(type="lexicon",id=rid,kind="lexicon",chapter=chapter,
                       family=family,direction="gr-ru",prompt=word["gr"],lang=lang,
                       choices=opts,wordAudio=audio(word["gr"]))
        else:
            card=by_id[rid]
            try:q=_as_question(card,uid,pos,len(items),lang,fmt,audio)
            except (ValueError,KeyError):continue
            q["family"]=family
        if q["id"] in used:continue
        q["review"]=True
        items.append(q);used.add(q["id"])
    scene_max=3 if family=="life" else 0
    scene_count=0
    for slot in range(target-len(items)):
        index=len(items)
        q=None
        if family=="life" and scene_count<scene_max:
            q=_life_scene(uid,pos,index,chapter,lang,used)
            if q:scene_count+=1
        if q is None and family=="lexicon":
            q=_lexicon(vocab,uid,pos,index,lang,audio,used)
        if q is None:
            card=_pick([x for x in pool if x["id"] not in used],_rng(uid,pos,index,family),used)
            if card:
                q=_as_question(card,uid,pos,index,lang,fmt,audio)
                q["family"]=family
        if q is None:
            q=_lexicon(vocab,uid,pos,index,lang,audio,used)
        if q is None:break
        q["review"]=False
        items.append(q);used.add(q["id"])
    if len(items)<8:
        raise ValueError("not_enough_lesson_material")
    stamp=_stamp()
    return dict(index=pos,chapter=chapter,family=family,name=meta["name"],
                items=items,at=0,startedAt=stamp,lastAt=stamp,activeSeconds=0,
                attempts=0,errors=0,correct=0,skips=0,paused=False)

def _backlog_view(s):
    due=[{k:v for k,v in item.items() if k in ("id","kind","chapter","prompt","errors","lastWrong","family")}
         for item in s["backlog"].values() if item.get("due")]
    due.sort(key=lambda x:(-x["errors"],x["lastWrong"]),reverse=False)
    by_family={}
    for x in due:by_family[x["family"]]=by_family.get(x["family"],0)+1
    return {"due":len(due),"byFamily":by_family,"items":due[:12],
            "totalMistakes":sum(x["errors"] for x in s["backlog"].values())}

def _summary(s,lang):
    chapter=s["position"]//PER_CHAPTER+1
    prior=(s["position"]>0 and s["position"]%PER_CHAPTER==0 and
           any(x["index"]==s["position"]-1 for x in s["lessons"]) and
           (s["position"]//PER_CHAPTER not in s.get("roundSeen",[])))
    shown=(s["position"]//PER_CHAPTER if prior else min(_cap(s),chapter))
    shown=max(1,min(_cap(s),shown))
    floor=(shown-1)*PER_CHAPTER
    results=[x for x in s["lessons"] if floor<=x["index"]<floor+PER_CHAPTER]
    finished=len(results)==8
    attempts=sum(x["attempts"] for x in results)
    errors=sum(x["errors"] for x in results)
    spent=sum(x["activeSeconds"] for x in results)
    elapsed=_elapsed(results[0]["startedAt"],results[-1]["finishedAt"]) if results else 0
    return {"chapter":shown,"finished":finished,"lessonsCompleted":len(results),
             "activeSeconds":spent,"elapsedSeconds":elapsed,"attempts":attempts,"errors":errors,
            "accuracy":round(100*(attempts-errors)/attempts) if attempts else None,
            "lessons":results}

def _view(s,rev,lang):
    cap=_cap(s)
    finished=s["position"]>=cap*PER_CHAPTER
    shown_ch=_summary(s,lang)["chapter"]
    waiting_round=(s["position"]>0 and s["position"]%PER_CHAPTER==0 and
        any(x["index"]==s["position"]-1 for x in s["lessons"]) and
        s["position"]//PER_CHAPTER not in s.get("roundSeen",[]) and
        s["position"]<cap*PER_CHAPTER)
    done={x["index"]:x for x in s["lessons"]}
    nodes=[]
    labels=TITLE.get(lang,TITLE["en"])
    for i in range((shown_ch-1)*PER_CHAPTER,shown_ch*PER_CHAPTER):
        chapter=i//PER_CHAPTER+1
        status=("skipped" if i<s.get("jumpedThrough",0) else
                "completed" if i in done else
                "current" if i==s["position"] and not finished else "locked")
        family=FAMILIES[i%PER_CHAPTER]
        node={"index":i,"number":i%PER_CHAPTER+1,"state":status}
        if status in ("completed","current"):
            if status=="completed" and i in done:node["name"]=done[i]["name"]
            elif family=="clock" and chapter<6:node["name"]="Практика фраз" if lang=="ru" else "Phrase practice"
            elif family=="grammar" and chapter<4:node["name"]="Повторение языка" if lang=="ru" else "Language review"
            elif family=="verb" and chapter<2:node["name"]="Повторение слов" if lang=="ru" else "Word review"
            else:node["name"]=labels[family]
            node["family"]=family
        if status=="completed":
            info=done[i]
            node["stats"]={k:info[k] for k in ("attempts","errors","activeSeconds","correct")}
        nodes.append(node)
    active=s.get("active")
    task=(active["items"][active["at"]] if active and active["at"]<len(active["items"]) else None)
    return {"schema":2,"revision":rev,"position":s["position"],"chapterLimit":cap,
            "round":shown_ch,"finished":finished,"nodes":nodes,
            "hasStarted":s["hasStarted"],"canJump":s["position"]==0 and not s["lessons"] and not s.get("active"),
        "roundReady":waiting_round,
            "lesson":({"index":active["index"],"name":active["name"],"family":active["family"],
                       "chapter":active["chapter"],"at":active["at"],"count":len(active["items"]),
                       "activeSeconds":active["activeSeconds"],"attempts":active["attempts"],
                       "errors":active["errors"],"correct":active["correct"],
                       "paused":active["paused"],"question":task}
                      if active and not finished else None),
            "roundStats":_summary(s,lang),"backlog":_backlog_view(s),
            "totals":{"lessons":len(s["lessons"]),
                      "activeSeconds":sum(x["activeSeconds"] for x in s["lessons"]),
                      "answers":sum(x["attempts"] for x in s["lessons"]),
                      "errors":sum(x["errors"] for x in s["lessons"])}}

def board_get(db,uid,lang,*_ignored):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    s,rev,migrate=_load(db,uid)
    if migrate:
        tracks._save(db,uid,"board","shared",s,rev);rev+=1
    # Do NOT generate future lessons on GET. Locked lesson content is unknown.
    return _view(s,rev,lang)

def _record_error(s,q,chapter):
    key=q["kind"]+":"+q["id"]
    row=s["backlog"].setdefault(key,{"id":q["id"],"kind":q["kind"],
        "chapter":chapter,"family":q.get("family",q["kind"]),"prompt":q["prompt"],
        "errors":0,"due":True,"lastWrong":_stamp()})
    row["errors"]+=1;row["due"]=True;row["lastWrong"]=_stamp()
    return key

def _review_success(s,q):
    key=q["kind"]+":"+q["id"]
    if q.get("review") and key in s["backlog"]:s["backlog"][key]["due"]=False

def _update_time(active):
    now=_stamp()
    if not active["paused"]:
        # Active engagement time is capped to avoid treating a night with a
        # browser left open as an 8-hour learning session.
        active["activeSeconds"]+=min(120,_elapsed(active["lastAt"],now))
    active["lastAt"]=now

def board_action(db,uid,lang,body,scorer,materials=None):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    s,rev,migrate=_load(db,uid)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    action=body.get("action")
    feedback=None
    if action=="scope":
        value=body.get("chapterLimit")
        if isinstance(value,bool) or not isinstance(value,int) or not 1<=value<=MAX_CHAPTER:
            raise ValueError("invalid_chapter")
        s["chapterLimit"]=value
        # Do not discard an unfinished lesson when temporarily reducing scope.
    elif action=="continue_round":
        if not s["position"] or s["position"]%PER_CHAPTER or s["position"]>=_cap(s)*PER_CHAPTER:
            raise ValueError("round_not_complete")
        n=s["position"]//PER_CHAPTER
        if n not in s["roundSeen"]:s["roundSeen"].append(n)
    elif action=="jump":
        value=body.get("chapter")
        if not isinstance(value,int) or isinstance(value,bool) or not 1<=value<=_cap(s) or s["lessons"] or s.get("active") or s["position"]!=0:
            raise ValueError("invalid_jump")
        s["skips"]+=(value-1)*PER_CHAPTER
        s["jumpedThrough"]=(value-1)*PER_CHAPTER
        s["position"]=(value-1)*PER_CHAPTER
    elif action=="lesson_start":
        if s["position"]>=_cap(s)*PER_CHAPTER:raise ValueError("chapter_limit_reached")
        if (s["position"]>0 and s["position"]%PER_CHAPTER==0 and
            any(x["index"]==s["position"]-1 for x in s["lessons"]) and
            s["position"]//PER_CHAPTER not in s["roundSeen"]):
            raise ValueError("round_report_not_seen")
        if s["active"] is None:
            if not materials:raise ValueError("missing_materials")
            s["active"]=_build_lesson(s,uid,lang,*materials)
            s["hasStarted"]=True
        elif s["active"]["paused"]:
            s["active"]["paused"]=False;s["active"]["lastAt"]=_stamp()
        elif s["active"]["items"][s["active"]["at"]].get("lang")!=lang:
            # Changing UI language cannot silently rewrite already scored
            # cards. Keep unfinished lesson's source language unchanged.
            pass
    elif action=="pause":
        active=s.get("active")
        if not active:raise ValueError("no_active_lesson")
        _update_time(active);active["paused"]=True
    elif action in ("answer","skip"):
        active=s.get("active")
        if not active or active["paused"]:raise ValueError("no_active_lesson")
        q=active["items"][active["at"]]
        if body.get("questionId")!=q["id"] or body.get("lessonIndex")!=active["index"]:
            raise ValueError("stale_track")
        _update_time(active)
        if action=="skip":
            if not s.get("canSkip"):raise ValueError("skip_not_allowed")
            feedback={"correct":False,"skipped":True,"unverified":True}
            active["skips"]+=1
            s["canSkip"]=False
            active["at"]+=1
        else:
            selected=body.get("selected")
            if not isinstance(selected,str) or len(selected)>500:raise ValueError("invalid_answer")
            if q["type"]=="life":
                scene=greek_life.BY_ID[q["id"]]
                result=life_answer_check.evaluate(selected,scene["accepted"],q["lang"])
                feedback={"correct":result["correct"],"unverified":result["unverified"],
                          "answer":result["closest"],"explanation":result["explanation"],
                          "translation":scene["translation"] if q["lang"]=="ru" else scene["translationEN"]}
                s["canSkip"]=bool(result["unverified"])
            elif q["type"]=="lexicon":
                if selected not in q["choices"]:raise ValueError("invalid_choice")
                import vocab_lessons as vocab_mod
                original=vocab_mod.VOCAB_BY_ID[q["id"]]
                correct=tracks._normalized(selected)==tracks._normalized(original[q["lang"]])
                feedback={"correct":correct,"answer":original[q["lang"]],
                          "explanation":None if correct else
                          ("Запомни перевод; слово появится снова в повторении." if q["lang"]=="ru" else
                           "Review this meaning; the word will return.")}
                s["canSkip"]=False
            else:
                if selected not in q["choices"]:raise ValueError("invalid_choice")
                feedback=scorer(uid,{"id":q["id"],"direction":q["direction"],"lang":q["lang"],
                              "selected":selected},injected_db=db)
                s["canSkip"]=False
            if not feedback.get("unverified"):
                active["attempts"]+=1
            if feedback["correct"]:
                active["at"]+=1;active["correct"]+=1
                _review_success(s,q)
            elif not feedback.get("unverified"):
                active["errors"]+=1
                _record_error(s,q,active["chapter"])
        if active["at"]>=len(active["items"]):
            complete=dict(index=active["index"],chapter=active["chapter"],family=active["family"],
                          name=active["name"],attempts=active["attempts"],errors=active["errors"],
                          correct=active["correct"],skips=active["skips"],
                          activeSeconds=active["activeSeconds"],startedAt=active["startedAt"],
                          finishedAt=_stamp(),total=len(active["items"]))
            s["lessons"].append(complete)
            s["position"]+=1
            s["active"]=None;s["canSkip"]=False
            feedback["lessonComplete"]=complete
            if s["position"]%PER_CHAPTER==0:
                feedback["roundFinished"]=True
    else:raise ValueError("invalid_board_action")
    tracks._save(db,uid,"board","shared",s,rev)
    out=_view(s,rev+1,lang)
    out["feedback"]=feedback
    return out
