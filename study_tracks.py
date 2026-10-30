"""Account-owned Lexi learning tracks: 30-word mastery and typed bus routes.

Independent of timed quiz queues, leaderboard, and the existing topic lessons.
SQLite state is authoritative and revision-checked across devices/tabs.
"""
import hashlib
import json
import random
import re
import unicodedata
from collections import defaultdict

import vocab_lessons as vocab
import topics_verbs
import lexical_overlap
import word_audio as _word_audio
import listening_catalog as _listening

LANGUAGES=("ru","en","zh","ar","es","pt")
BATCH=30

def _normalized(value):
    value=unicodedata.normalize("NFD",str(value or "").casefold())
    value="".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w\s]+"," ",value,flags=re.UNICODE).split())

_VERB_FORMS={
    form for group,level,lemma,ru,en,forms in topics_verbs.VERBS
    for form in (lemma,*forms)
}
_VERB_FORMS.update((
    "είμαι","είσαι","είναι","είμαστε","είστε","είναι",
    "έχω","έχεις","έχει","έχουμε","έχετε","έχουν",
    "πηγαίνω","πηγαίνεις","πηγαίνει","πηγαίνουμε","πηγαίνετε","πηγαίνουν",
    "τρώω","τρως","τρώει","τρώμε","τρώτε","τρώνε",
))
_ADJECTIVE_EN=(
    "married","unmarried","single","tall","short","small","big","large",
    "good","bad","new","old","young","beautiful","pretty","cheap",
    "expensive","fast","slow","happy","sad","easy","difficult",
    "free","busy","delicious","quiet","comfortable","ready",
    "fresh","hot","cold","white","black","red","blue",
)
def _word_class(word):
    # Never infer part of speech solely from Greek word endings: εγώ and
    # εδώ end in -ω but are not verbs; αντίο is not an adjective.
    greek=word["gr"].casefold().strip()
    en=word.get("en","").casefold().strip()
    if greek.startswith(("ο ","η ","το ","οι ","τα ")) :return "noun"
    if greek in _VERB_FORMS or (
        en.startswith(("i ","you ","he ","she ","we ","they ")) and
        any(x in en for x in (" am"," are"," is","have","has","live","work","speak","do","make","learn","read"))
    ):return "verb"
    if en not in ("good morning","good evening","good night",
                 "good afternoon","happy birthday","goodbye") and any(
        en==label or en.startswith(label+" ") for label in _ADJECTIVE_EN
    ):
        return "adjective"
    return "other"

def _word_order():
    # Mix part-of-speech and topics from the *existing* authored curriculum.
    # Stable IDs/order, so a server release never reassigns learned blocks.
    unique={}
    for w in vocab.VOCAB:
        if all(w.get(lang) for lang in LANGUAGES) and w["gr"]:
            unique.setdefault(_normalized(w["gr"]),w)
    categories=defaultdict(list)
    for w in unique.values():
        categories[(w["level"],_word_class(w))].append(w)
    ordered=[]
    for level in ("A1","A2"):
        for i in range(2000):
            changed=False
            for cls in ("noun","verb","adjective","other"):
                group=categories[(level,cls)]
                if i<len(group):
                    ordered.append(group[i]);changed=True
            if not changed:break
    assert len(ordered)>500 and len(set(w["id"] for w in ordered))==len(ordered)
    return ordered

WORDS=_word_order()
BY_ID={w["id"]:w for w in WORDS}
WORD_IDS=[w["id"] for w in WORDS]

def schema(db):
    db.execute("""CREATE TABLE IF NOT EXISTS learning_tracks(
        user_id TEXT NOT NULL, name TEXT NOT NULL, lang TEXT NOT NULL,
        revision INTEGER NOT NULL DEFAULT 0, data TEXT NOT NULL,
        PRIMARY KEY(user_id,name,lang)
    )""")

def _load(db,uid,name,lang,initial):
    row=db.execute("SELECT revision,data FROM learning_tracks WHERE user_id=? AND name=? AND lang=?",
                   (uid,name,lang)).fetchone()
    if row:return json.loads(row["data"]),row["revision"]
    return initial(),0

def _save(db,uid,name,lang,s,rev):
    db.execute("""INSERT INTO learning_tracks(user_id,name,lang,revision,data)
        VALUES(?,?,?,?,?)
        ON CONFLICT(user_id,name,lang) DO UPDATE
        SET revision=excluded.revision,data=excluded.data""",
        (uid,name,lang,rev+1,json.dumps(s,ensure_ascii=False,separators=(",",":"))))

def _shuffle(items,salt):
    result=list(items)
    random.Random(int(hashlib.sha256(str(salt).encode()).hexdigest()[:16],16)).shuffle(result)
    return result

def _anki_initial():
    return {"phase":"preview","batch":0,"at":0,"mastered":[],"known":[],"queue":[],
            "nextPhase":None,"reviewRound":0,"misses":0}

def _cohort(s):
    start=s["batch"]*BATCH
    return WORD_IDS[start:start+BATCH]

def _options(word,lang,revision):
    source=word[lang]
    candidates=[w[lang] for w in WORDS if w["id"]!=word["id"] and
                w["level"]==word["level"] and
                _word_class(w)==_word_class(word) and
                not lexical_overlap.overlaps(word,w)]
    seen={_normalized(source)}
    alternatives=[]
    for value in _shuffle(candidates,f"{word['id']}:{lang}:{revision}"):
        key=_normalized(value)
        if key and key not in seen:
            seen.add(key);alternatives.append(value)
        if len(alternatives)==3:break
    if len(alternatives)<3:
        for w in WORDS:
            if lexical_overlap.overlaps(word,w):continue
            value=w[lang];key=_normalized(value)
            if key and key not in seen:
                seen.add(key);alternatives.append(value)
            if len(alternatives)==3:break
    if len(alternatives)!=3:raise ValueError("not_enough_choices")
    return _shuffle([source]+alternatives,f"choices:{word['id']}:{lang}:{revision}")

def _anki_view(s,rev,lang):
    phase=s["phase"]
    view={"phase":phase,"revision":rev,"batch":s["batch"]+1,
          "cohortSize":len(_cohort(s)) if phase in ("preview","quiz") else 0,
          "learned":len(s["mastered"]),"misses":s["misses"],
          "totalWords":len(WORD_IDS),"round":s["reviewRound"]}
    if phase=="preview":
        ids=_cohort(s)
        if ids:
            card=BY_ID[ids[s["at"]]]
            view.update(at=s["at"]+1,card={"id":card["id"],"gr":card["gr"],
                        "translation":card[lang],"level":card["level"],
                        "wordAudio":_word_audio.lookup(card["gr"],_listening)})
    elif phase in ("quiz","review"):
        if not s["queue"]:raise ValueError("invalid_track_queue")
        card=BY_ID[s["queue"][0]]
        view.update(card={"id":card["id"],"gr":card["gr"],"level":card["level"],
                          "wordAudio":_word_audio.lookup(card["gr"],_listening)},
                    options=_options(card,lang,rev),done=len(s["known"]),
                    target=len(_cohort(s)) if phase=="quiz" else min(60,len(s["mastered"])),
                    remaining=len(s["queue"]))
    elif phase=="milestone":
        view.update(nextPhase=s["nextPhase"],
                    achieved= BATCH if s["nextPhase"] in ("preview","review") else 0)
    elif phase=="finished":
        view["completed"]=True
    return view

def anki_get(db,uid,lang):
    if lang not in LANGUAGES:raise ValueError("invalid_language")
    s,rev=_load(db,uid,"anki",lang,_anki_initial)
    return _anki_view(s,rev,lang)

def anki_action(db,uid,lang,body):
    if lang not in LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    s,rev=_load(db,uid,"anki",lang,_anki_initial)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    action=body.get("action")
    feedback=None
    if action=="advance" and s["phase"]=="preview":
        s["at"]+=1
        if s["at"]>=len(_cohort(s)):
            s.update(phase="quiz",known=[],queue=_shuffle(_cohort(s),f"cohort:{uid}:{lang}:{s['batch']}"))
    elif action=="answer" and s["phase"] in ("quiz","review"):
        cid=s["queue"][0]
        if body.get("cardId")!=cid:raise ValueError("stale_track")
        card=BY_ID[cid]
        selected=body.get("selected")
        if not isinstance(selected,str) or len(selected)>250:raise ValueError("bad_answer")
        offered=_options(card,lang,rev)
        if selected not in offered and selected not in lexical_overlap.alternatives(card,"gr-target",lang):
            raise ValueError("invalid_choice")
        accepted=[card[lang]]+lexical_overlap.alternatives(card,"gr-target",lang)
        correct=_normalized(selected) in {_normalized(x) for x in accepted}
        feedback={"correct":correct,"greek":card["gr"],"translation":card[lang]}
        s["queue"].pop(0)
        if correct:
            if cid not in s["known"]:s["known"].append(cid)
        else:
            s["misses"]+=1
            s["queue"].append(cid)
        if not s["queue"]:
            if s["phase"]=="quiz":
                for word_id in _cohort(s):
                    if word_id not in s["mastered"]:s["mastered"].append(word_id)
                s["batch"]+=1
                next_phase="review" if s["batch"]%2==0 else "preview"
                if len(_cohort(s))==0:next_phase="finished"
            else:next_phase="preview"
            s.update(phase="milestone" if next_phase!="finished" else "finished",
                     nextPhase=next_phase,known=[])
    elif action=="continue" and s["phase"]=="milestone":
        if s["nextPhase"]=="review":
            s["reviewRound"]+=1
            selected=_shuffle(s["mastered"],f"review:{uid}:{lang}:{s['reviewRound']}")
            # Mix already learned words, including older blocks.
            subset=selected[:min(60,len(selected))]
            s.update(phase="review",queue=_shuffle(subset,f"exam:{uid}:{lang}:{s['reviewRound']}"),
                     known=[],nextPhase=None)
        elif s["nextPhase"]=="preview":
            s.update(phase="preview",at=0,queue=[],known=[],nextPhase=None)
        else:raise ValueError("invalid_track_transition")
    else:raise ValueError("invalid_track_action")
    _save(db,uid,"anki",lang,s,rev)
    return {**_anki_view(s,rev+1,lang),"feedback":feedback}

# Routes are fictional but internally consistent map diagrams. All landmarks
# have an unambiguous school-level Greek phrase and Russian/English name.
LANDMARKS=(
    ("Σχολείο","το σχολείο","Школа","School",6),
    ("Κέντρο","το κέντρο","Центр","Centre",6),
    ("Πανεπιστήμιο","το πανεπιστήμιο","Университет","University",6),
    ("Σπίτι","το σπίτι","Дом","Home",2),
    ("Τράπεζα","την τράπεζα","Банк","Bank",6),
    ("Πάρκο","το πάρκο","Парк","Park",16),
    ("Μουσείο","το μουσείο","Музей","Museum",16),
    ("Θέατρο","το θέατρο","Театр","Theatre",16),
    ("Νοσοκομείο","το νοσοκομείο","Больница","Hospital",18),
    ("Ταχυδρομείο","το ταχυδρομείο","Почта","Post office",19),
)

NUMBERS=(("55","πενήντα πέντε"),("24","είκοσι τέσσερα"),
         ("18","δεκαοκτώ"),("31","τριάντα ένα"),("42","σαράντα δύο"),
         ("16","δεκαέξι"),("63","εξήντα τρία"),("70","εβδομήντα"),
         ("88","ογδόντα οκτώ"),("90","ενενήντα"),("25","είκοσι πέντε"),
         ("36","τριάντα έξι"))
def _scene(index,stage=20):
    number,spelled=NUMBERS[index%len(NUMBERS)]
    available=[x for x in LANDMARKS if x[4]<=stage]
    if len(available)<5:raise ValueError("chapter_not_unlocked")
    steps=[available[(index*3+j)%len(available)] for j in range(5)]
    keys=("number","origin","via1","via2","stop","destination")
    expected=(spelled,steps[0][1],steps[1][1],steps[2][1],steps[3][0],steps[4][1])
    return {"bus":number,"stops":[{"name":x[0],"ru":x[2],"en":x[3]} for x in steps],
            "expected":dict(zip(keys,expected))}

def _route_initial():return {"index":0,"misses":0}
def route_get(db,uid,lang,stage=20):
    if lang not in LANGUAGES:raise ValueError("invalid_language")
    state,rev=_load(db,uid,"route",lang,_route_initial)
    scene=_scene(state["index"],stage)
    return {"revision":rev,"completed":state["index"],"misses":state["misses"],
            "bus":scene["bus"],"stops":scene["stops"],"chapter":6,
            "fields":["number","origin","via1","via2","stop","destination"]}

def route_action(db,uid,lang,body,stage=20):
    if lang not in LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    state,rev=_load(db,uid,"route",lang,_route_initial)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    fields=body.get("answers")
    if not isinstance(fields,dict):raise ValueError("bad_answers")
    scene=_scene(state["index"],stage)
    expected=scene["expected"]
    if set(fields)!=set(expected):raise ValueError("bad_answers")
    results={}
    notes={}
    for key,wanted in expected.items():
        value=fields[key]
        if not isinstance(value,str) or len(value)>160:raise ValueError("bad_answer")
        normalized=_normalized(value)
        # Name in Greek, or a full natural phrase including the prompt.
        if key=="number":
            normalized=normalized.removeprefix(_normalized("το λεωφορείο")).strip()
        else:
            for prefix in ("ξεκινάει από","περνάει από","μετά περνάει από",
                           "σταματάει στη στάση","πηγαίνει προς"):
                if normalized.startswith(_normalized(prefix)+" "):
                    normalized=normalized[len(_normalized(prefix))+1:]
        results[key]=(normalized==_normalized(wanted))
        if not results[key]:
            if not normalized:notes[key]="Напиши название или номер автобуса по-гречески." if lang=="ru" else "Enter the Greek place name or bus number."
            elif key=="number":notes[key]="Проверь греческие числительные и их порядок." if lang=="ru" else "Check the Greek number words."
            elif _normalized(wanted).split()[-1:] == normalized.split()[-1:]:
                notes[key]="Проверь предлог и артикль перед названием." if lang=="ru" else "Check the preposition and article."
            else:notes[key]="Сверь название с указанной остановкой на схеме." if lang=="ru" else "Check the stop name on the map."
    complete=all(results.values())
    if complete:state["index"]+=1
    else:state["misses"]+=1
    _save(db,uid,"route",lang,state,rev)
    response=route_get(db,uid,lang,stage)
    response["feedback"]={
        "correct":complete,"fields":results,
        "explanations":notes,
        "expected":expected,
        "greek":("Το λεωφορείο "+expected["number"]+". Ξεκινάει από "+expected["origin"]+
                 ". Περνάει από "+expected["via1"]+" και "+expected["via2"]+
                 ". Σταματάει στη στάση «"+expected["stop"]+"». Πηγαίνει "+(
                    "στην "+expected["destination"].removeprefix("την ")
                    if expected["destination"].startswith("την ") else
                    "στο "+expected["destination"].removeprefix("το "))+ "."),
        "translation":(
            "Автобус "+scene["bus"]+": от «"+scene["stops"][0]["ru"]+
            "» через «"+scene["stops"][1]["ru"]+"» и «"+scene["stops"][2]["ru"]+
            "», остановка «"+scene["stops"][3]["ru"]+"», конечная «"+
            scene["stops"][4]["ru"]+"»." if lang=="ru" else
            "Bus "+scene["bus"]+": from "+scene["stops"][0]["en"]+
            " via "+scene["stops"][1]["en"]+" and "+scene["stops"][2]["en"]+
            ", stopping at "+scene["stops"][3]["en"]+", ending at "+
            scene["stops"][4]["en"]+"."),
        "translationLang":"ru" if lang=="ru" else "en",
    }
    return response

def validate():
    assert len(WORD_IDS)>500
    assert len(set(WORD_IDS))==len(WORD_IDS)
    assert len({_normalized(w["gr"]) for w in WORDS})==len(WORD_IDS)
    for i in range(len(NUMBERS)):
        scene=_scene(i)
        assert len(scene["stops"])==5 and len(set(s["name"] for s in scene["stops"]))==5
        assert len(scene["expected"])==6
    return len(WORD_IDS)
