"""Greek Life: curriculum-bounded interactive situations and learner-specific review.

Only original authored scenarios; the printed textbook is used for chapter
introductions, never copied. Every scenario has a reviewed entry gate.
Answers are scored deterministically; ambiguous alternatives are explicitly
curated instead of rejected by a generic exact-string comparison.
"""
import json
import re
import difflib
import study_tracks as tracks

LANGS=tracks.LANGUAGES
MAX_CHAPTER=20
# Simple situations deliberately use only vocabulary introduced by the
# indicated printed chapter or earlier. Do not silently add future grammar.
SCENES=(
    dict(id="meet",chapter=1,name="Знакомство",en="Meeting someone",
         prompt="Представься: «Меня зовут Мария».",promptEN="Introduce yourself: My name is Maria.",
         accepted=("Με λένε Μαρία.", "Είμαι η Μαρία."),
         translation="Меня зовут Мария.",translationEN="My name is Maria.",
         hint="με λένε ...",tokens=("με","λένε","μαρια")),
    dict(id="home_city",chapter=2,name="Где ты живёшь?",en="Where do you live?",
         prompt="Скажи: «Я живу в Никосии».",promptEN="Say: I live in Nicosia.",
         accepted=("Μένω στη Λευκωσία.","Μένω στην Λευκωσία."),
         translation="Я живу в Никосии.",translationEN="I live in Nicosia.",
         hint="Μένω στη ...",tokens=("μενω","στη","λευκωσια")),
    dict(id="family",chapter=3,name="Моя семья",en="My family",
         prompt="Скажи: «У меня есть один брат».",promptEN="Say: I have a brother.",
         accepted=("Έχω έναν αδελφό.","Έχω έναν αδερφό."),
         translation="У меня есть один брат.",translationEN="I have one brother.",
         hint="Έχω έναν ...",tokens=("εχω","εναν","αδελφο")),
    dict(id="languages",chapter=4,name="Знакомство с языками",en="Languages",
         prompt="Скажи: «Я говорю по-гречески».",promptEN="Say: I speak Greek.",
         accepted=("Μιλάω ελληνικά.","Μιλώ ελληνικά."),
         translation="Я говорю по-гречески.",translationEN="I speak Greek.",
         hint="Μιλάω ...",tokens=("μιλαω","ελληνικα")),
    dict(id="ticket",chapter=6,name="Автобусный билет",en="Buying a ticket",
         prompt="Попроси один билет до Лимасола.",promptEN="Ask for one ticket to Limassol.",
         accepted=("Ένα εισιτήριο για τη Λεμεσό, παρακαλώ.",
                   "Θέλω ένα εισιτήριο για τη Λεμεσό, παρακαλώ.",
                   "Ένα εισιτήριο για τη Λεμεσό."),
         translation="Один билет до Лимасола, пожалуйста.",translationEN="One ticket to Limassol, please.",
         hint="Ένα εισιτήριο για ...",tokens=("εισιτηριο","για","τη","λεμεσο")),
    dict(id="daily",chapter=7,name="Мой день",en="Daily routine",
         prompt="Скажи: «Я завтракаю в восемь».",promptEN="Say: I have breakfast at eight.",
         accepted=("Τρώω πρωινό στις οκτώ.","Στις οκτώ τρώω πρωινό."),
         translation="Я завтракаю в восемь.",translationEN="I have breakfast at eight.",
         hint="Τρώω πρωινό στις ...",tokens=("τρωω","πρωινο","στις","οκτω")),
    dict(id="groceries",chapter=8,name="Список покупок",en="Groceries",
         prompt="Попроси один килограмм помидоров.",promptEN="Ask for one kilo of tomatoes.",
         accepted=("Θέλω ένα κιλό ντομάτες, παρακαλώ.",
                   "Ένα κιλό ντομάτες, παρακαλώ.",
                   "Θέλω ένα κιλό ντομάτες."),
         translation="Один килограмм помидоров, пожалуйста.",
         translationEN="One kilo of tomatoes, please.",
         hint="Θέλω ένα κιλό ...",tokens=("θελω","ενα","κιλο","ντοματες")),
    dict(id="clothes",chapter=9,name="Покупка одежды",en="Clothes shop",
         prompt="Скажи: «Я хочу это платье».",promptEN="Say: I want this dress.",
         accepted=("Θέλω αυτό το φόρεμα.","Αυτό το φόρεμα θέλω."),
         translation="Я хочу это платье.",translationEN="I want this dress.",
         hint="Θέλω αυτό το ...",tokens=("θελω","αυτο","το","φορεμα")),
    dict(id="directions",chapter=11,name="Где находится дом?",en="Finding a home",
         prompt="Скажи: «Дом рядом с центром».",promptEN="Say: The home is near the centre.",
         accepted=("Το σπίτι είναι κοντά στο κέντρο.","Το σπίτι βρίσκεται κοντά στο κέντρο."),
         translation="Дом находится рядом с центром.",
         translationEN="The house is near the centre.",
         hint="Το σπίτι είναι κοντά ...",tokens=("το","σπιτι","ειναι","κοντα","στο","κεντρο")),
    dict(id="cafe",chapter=14,name="Заказ в кафе",en="Ordering coffee",
         prompt="Вежливо попроси один кофе.",promptEN="Politely ask for one coffee.",
         accepted=("Θα ήθελα έναν καφέ, παρακαλώ.",),
         translation="Я хотел(а) бы один кофе, пожалуйста.",
         translationEN="I'd like a coffee, please.",
         hint="Θα ήθελα έναν ...",tokens=("θα","ηθελα","εναν","καφε")),
    dict(id="plans",chapter=16,name="Планы на выходной",en="Weekend plans",
         prompt="Скажи: «Мне нравится гулять».",promptEN="Say: I like walking.",
         accepted=("Μου αρέσει να περπατάω.","Μου αρέσει να περπατώ."),
         translation="Мне нравится гулять.",translationEN="I like walking.",
         hint="Μου αρέσει να ...",tokens=("μου","αρεσει","να","περπαταω")),
)

BY_ID={x["id"]:x for x in SCENES}
assert len(BY_ID)==len(SCENES)

def _initial():
    return {"maxChapter":6,"results":{},"round":0}

def _max(s):
    return max(1,min(MAX_CHAPTER,int(s.get("maxChapter",6))))

def current_settings(db,uid,lang):
    if lang not in LANGS:raise ValueError("invalid_language")
    s,rev=tracks._load(db,uid,"life",lang,_initial)
    max_chapter=_max(s)
    relevant=db.execute("""SELECT unit,COUNT(*) AS total,SUM(correct) AS good
        FROM attempts WHERE user_id=? AND unit BETWEEN 1 AND ?
        GROUP BY unit""",(uid,max_chapter)).fetchall()
    weak_by_unit={r["unit"]:r["total"]-r["good"] for r in relevant}
    mastered_words=db.execute("""SELECT COUNT(*) FROM vocab_progress
        WHERE user_id=? AND correct>=2 AND miss_debt=0""",(uid,)).fetchone()[0]
    anki_state,_=tracks._load(db,uid,"anki",lang,tracks._anki_initial)
    mastered_words=max(mastered_words,len(anki_state.get("mastered",[])))
    # Early scenes remain available, but favour ones with unresolved errors
    # and topics where the learner has already demonstrated basic knowledge.
    scenarios=[]
    for scene in SCENES:
        if scene["chapter"]>max_chapter:continue
        result=s["results"].get(scene["id"],{})
        tries=result.get("attempts",0);errors=result.get("errors",0)
        demonstrated=next((r["good"] for r in relevant if r["unit"]==scene["chapter"]),0)
        ready=demonstrated>=6 or mastered_words>=30 or result.get("correct",0)>=1
        difficulty="independent" if ready else "guided"
        priority=(errors*4)+(weak_by_unit.get(scene["chapter"],0)//4)-tries
        scenarios.append({"id":scene["id"],"name":scene["name"] if lang=="ru" else scene["en"],
            "chapter":scene["chapter"],"attempts":tries,"errors":errors,
            "difficulty":difficulty,"priority":priority,"type":"roleplay"})
    extras=[
        ("route",6,"Автобусные маршруты","Bus routes"),
        ("periptero",8,"Περίπτερο · магазин","Περίπτερο · mini market"),
        ("likes",16,"Мне нравится / не нравится","Likes and dislikes")
    ]
    for id,gate,ru,en in extras:
        if gate<=max_chapter:
            scenarios.append({"id":id,"name":ru if lang=="ru" else en,
                "chapter":gate,"type":"activity","difficulty":"guided",
                "priority":0,"attempts":0,"errors":0})
    # Build one guided "next adventure" from all unlocked experiences. The
    # learner never has to choose a category or scroll through eleven scenes.
    # Reuse existing account-owned activity progress rather than resetting it.
    activity_data={
        "route":tracks._load(db,uid,"route",lang,tracks._route_initial)[0],
        "periptero":tracks._load(db,uid,"periptero",lang,lambda:{"round":0,"bought":[]})[0],
        "likes":tracks._load(db,uid,"likes",lang,lambda:{"index":0})[0],
    }
    for item in scenarios:
        if item["type"]=="activity":
            data=activity_data[item["id"]]
            item["correct"]=(int(data.get("index",0)) if item["id"] in ("route","likes")
                else int(data.get("round",0)))
            item["inProgress"]=(item["id"]=="periptero" and bool(data.get("bought")))
            item["attempts"]=item["correct"]
        else:
            item["correct"]=s["results"].get(item["id"],{}).get("correct",0)
            item["inProgress"]=False
    # Skipped unknown alternatives are deferred, never counted as mastery.
    for item in scenarios:
        if item["type"]=="roleplay":
            item["skipped"]=s["results"].get(item["id"],{}).get("skipped",0)
        else:item["skipped"]=0
    # Finish an already-started shopping basket before switching situations.
    pending=next((x for x in scenarios if x.get("inProgress")),None)
    # A failed scene is revisited, but only its demonstrated, curated errors
    # affect the queue; unverified alternative wordings were never penalized.
    preferred=sorted(scenarios,key=lambda x:(
        x["correct"]+x.get("skipped",0), -int(x.get("errors",0)>0), x["chapter"], x["id"]))
    recommended=pending or (preferred[0] if preferred else None)
    distinct_done=sum(x["correct"]>0 for x in scenarios)
    return {"revision":rev,"maxChapter":max_chapter,
            "available":scenarios,"recommended":recommended["id"] if recommended else None,
            "nextAdventure":recommended,
            "completedExperiences":distinct_done,"totalExperiences":len(scenarios),
            "masteredWords":mastered_words,"observations":sum(r["total"] for r in relevant),
            "printedChapterCount":MAX_CHAPTER}

def update_settings(db,uid,lang,body):
    if lang not in LANGS:raise ValueError("invalid_language")
    chapter=body.get("maxChapter")
    if isinstance(chapter,bool) or not isinstance(chapter,int) or not 1<=chapter<=MAX_CHAPTER:
        raise ValueError("invalid_chapter")
    db.execute("BEGIN IMMEDIATE")
    s,rev=tracks._load(db,uid,"life",lang,_initial)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    s["maxChapter"]=chapter
    tracks._save(db,uid,"life",lang,s,rev)
    return current_settings(db,uid,lang)

def skip_scene(db,uid,lang,body):
    """Skip an ambiguous response without marking any answer as correct/wrong."""
    sid=body.get("id")
    if lang not in LANGS or sid not in BY_ID:raise ValueError("invalid_scene")
    db.execute("BEGIN IMMEDIATE")
    state,rev=tracks._load(db,uid,"life",lang,_initial)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    if BY_ID[sid]["chapter"]>_max(state):raise ValueError("chapter_not_unlocked")
    item=state["results"].setdefault(sid,{"attempts":0,"correct":0,"errors":0})
    item["skipped"]=item.get("skipped",0)+1
    tracks._save(db,uid,"life",lang,state,rev)
    return current_settings(db,uid,lang)

def ensure(db,uid,lang,activity):
    if lang not in LANGS:raise ValueError("invalid_language")
    cfg,_=tracks._load(db,uid,"life",lang,_initial)
    min_chapter={"route":6,"periptero":8,"likes":16}.get(activity)
    if min_chapter is None:raise ValueError("invalid_activity")
    if _max(cfg)<min_chapter:raise ValueError("chapter_not_unlocked")
    return _max(cfg)

def _norm(s):
    return tracks._normalized(s)

def explain(selected,accepted,lang):
    """Trust only diagnostic patterns that a fixed script can know."""
    t=_norm(selected).split()
    expected=_norm(accepted).split()
    tr=(lang=="ru")
    if "να" in expected and "να" not in t:
        return "Пропущена частица να перед глаголом." if tr else "The particle να is missing before the verb."
    if "δεν" in expected and "δεν" not in t:
        return "Пропущено отрицание δεν." if tr else "The negative particle δεν is missing."
    if "δεν" in t and "δεν" not in expected:
        return "Лишнее отрицание δεν меняет смысл фразы." if tr else "Extra δεν changes the meaning."
    # Compare well-known functional words only, not free creative synonyms.
    articles=("ο","η","το","οι","τα","τον","τη","την","του","της","στο","στη","στην","στον","εναν","ένα","εναν")
    for x in expected:
        if x in articles and x not in t:
            return (f"Не хватает формы «{x}»: проверь артикль, род, падеж или предлог." if tr
                    else f"Missing «{x}»: check article, case, or preposition.")
    operations=difflib.SequenceMatcher(None,expected,t).get_opcodes()
    for operation,i,j,k,l in operations:
        if operation=="replace" and i<j and k<l:
            return (f"Здесь ожидается «{' '.join(expected[i:j])}», а написано «{' '.join(t[k:l])}». Проверь форму слова и смысл." if tr else
                    f"Expected «{' '.join(expected[i:j])}» rather than «{' '.join(t[k:l])}». Check the form and meaning.")
        if operation=="delete" and i<j:
            return (f"Пропущено «{' '.join(expected[i:j])}»." if tr else
                    f"Missing «{' '.join(expected[i:j])}».")
    return ("Фраза не совпала с проверенными вариантами. Проверь контекст и форму слов; допустимые варианты показаны ниже." if tr else
            "The response does not match reviewed alternatives. Check meaning and forms; accepted examples are below.")

def scene_get(db,uid,lang,scene_id):
    if lang not in LANGS:raise ValueError("invalid_language")
    if scene_id not in BY_ID:raise ValueError("unknown_scene")
    state,revision=tracks._load(db,uid,"life",lang,_initial)
    scene=BY_ID[scene_id]
    if scene["chapter"]>_max(state):raise ValueError("chapter_not_unlocked")
    progress=state["results"].get(scene_id,{})
    demonstrated=db.execute("SELECT COUNT(*) FROM attempts WHERE user_id=? AND correct=1 AND unit<=?",
                            (uid,scene["chapter"])).fetchone()[0]
    experienced=demonstrated>=12 or progress.get("correct",0)>=1
    return {"id":scene_id,"revision":revision,
            "chapter":scene["chapter"],"title":scene["name"] if lang=="ru" else scene["en"],
            "prompt":scene["prompt"] if lang=="ru" else scene["promptEN"],
            "promptLang":"ru" if lang=="ru" else "en",
            "hint":None if experienced else scene["hint"],
            "difficulty":"independent" if experienced else "guided",
            "attempts":progress.get("attempts",0),"correct":progress.get("correct",0),
            "errors":progress.get("errors",0)}

def scene_answer(db,uid,lang,body):
    if lang not in LANGS:raise ValueError("invalid_language")
    sid=body.get("id")
    answer=body.get("answer")
    if sid not in BY_ID or not isinstance(answer,str) or len(answer)>320:raise ValueError("invalid_answer")
    db.execute("BEGIN IMMEDIATE")
    state,rev=tracks._load(db,uid,"life",lang,_initial)
    scene=BY_ID[sid]
    if body.get("revision")!=rev:raise ValueError("stale_track")
    if scene["chapter"]>_max(state):raise ValueError("chapter_not_unlocked")
    correct=any(_norm(answer)==_norm(x) for x in scene["accepted"])
    history=state["results"].setdefault(sid,{"attempts":0,"correct":0,"errors":0})
    history["attempts"]+=1
    history["correct"]+=int(correct)
    explanation=None if correct else explain(answer,scene["accepted"][0],lang)
    # A response outside our reviewed grammar patterns may be valid Greek.
    # Do not count it as a learner error until it can be verified.
    # Only confidently detectable particles/articles can count as a
    # grammatical mistake. A different synonym, word order or verb choice
    # may be perfectly idiomatic and must not be penalized by string diff.
    confidently_known=bool(explanation and (
        explanation.startswith(("Пропущена частица", "The particle",
            "Пропущено отрицание", "The negative particle",
            "Лишнее отрицание", "Extra δεν",
            "Не хватает формы", "Missing «"))))
    unverified=bool(not correct and not confidently_known)
    history["errors"]+=int(not correct and not unverified)
    tracks._save(db,uid,"life",lang,state,rev)
    return {"revision":rev+1,"correct":correct,"unverified":unverified,
            "answer":scene["accepted"][0],
            "alternatives":list(scene["accepted"][1:]),
            "explanation":explanation,
            "translation":scene["translation"] if lang=="ru" else scene["translationEN"],
            "translationLang":"ru" if lang=="ru" else "en",
            "difficulty":"independent" if history["correct"]>=1 else "guided",
            "attempts":history["attempts"]}

def validate():
    assert len(SCENES)>=10
    assert len(BY_ID)==len(SCENES)
    assert set(range(1,5)).issubset({s["chapter"] for s in SCENES})
    assert all(1<=s["chapter"]<=MAX_CHAPTER and len(s["accepted"])>=1 for s in SCENES)
    for s in SCENES:
        assert len(set(_norm(x) for x in s["accepted"]))==len(s["accepted"]),s["id"]
    return len(SCENES)
