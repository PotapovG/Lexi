"""Independent original A1 Greek pattern and mini-market practice.

Likes: Δεν μου/σου/του/της/μας/σας/τους αρέσει να + inflected verb.
Periptero: correctly request products and quantities via polite Greek phrases.
Persists by account via study_tracks.learning_tracks; never enters standard quiz.
"""
import random
import study_tracks as tracks

PERSONS=(
    ("μου","мне","I","I"),
    ("σου","тебе","you","you"),
    ("του","ему","he","he"),
    ("της","ей","she","she"),
    ("μας","нам","we","we"),
    ("σας","вам","you (plural)","you (plural)"),
    ("τους","им","they","they"),
)
# Greek present indicative after να conveys habitual/ongoing actions.
VERBS=(
    ("διαβάζω","читать","read",("διαβάζω","διαβάζεις","διαβάζει","διαβάζει","διαβάζουμε","διαβάζετε","διαβάζουν")),
    ("παίζω","играть","play",("παίζω","παίζεις","παίζει","παίζει","παίζουμε","παίζετε","παίζουν")),
    ("μαγειρεύω","готовить","cook",("μαγειρεύω","μαγειρεύεις","μαγειρεύει","μαγειρεύει","μαγειρεύουμε","μαγειρεύετε","μαγειρεύουν")),
    ("περπατάω","гулять пешком","walk",("περπατάω","περπατάς","περπατάει","περπατάει","περπατάμε","περπατάτε","περπατάνε")),
    ("πηγαίνω","ходить","go",("πηγαίνω","πηγαίνεις","πηγαίνει","πηγαίνει","πηγαίνουμε","πηγαίνετε","πηγαίνουν")),
    ("μιλάω","говорить","speak",("μιλάω","μιλάς","μιλάει","μιλάει","μιλάμε","μιλάτε","μιλάνε")),
    ("δουλεύω","работать","work",("δουλεύω","δουλεύεις","δουλεύει","δουλεύει","δουλεύουμε","δουλεύετε","δουλεύουν")),
    ("ακούω","слушать","listen",("ακούω","ακούς","ακούει","ακούει","ακούμε","ακούτε","ακούνε")),
    ("τρώω","есть","eat",("τρώω","τρως","τρώει","τρώει","τρώμε","τρώτε","τρώνε")),
    ("βλέπω","смотреть","watch",("βλέπω","βλέπεις","βλέπει","βλέπει","βλέπουμε","βλέπετε","βλέπουν")),
)
# Keep the full A1 contrast: να + inflected verb, singular αρέσει
# before noun subjects, plural αρέσουν before plural noun subjects.
NOUNS=(
    ("ο καφές","кофе","coffee",False),
    ("το γάλα","молоко","milk",False),
    ("το νερό","вода","water",False),
    ("το βιβλίο","книга","the book",False),
    ("η μουσική","музыка","music",False),
    ("το πάρκο","парк","the park",False),
    ("τα μήλα","яблоки","apples",True),
    ("οι ταινίες","фильмы","films",True),
    ("τα βιβλία","книги","books",True),
    ("οι μπανάνες","бананы","bananas",True),
)
LIKES_TOTAL=len(PERSONS)*(len(VERBS)+len(NOUNS))*2
def _like_scene(index):
    index%=LIKES_TOTAL
    negative=index%2==1
    p=(index//2)%len(PERSONS)
    group=index//(2*len(PERSONS))
    pronoun=PERSONS[p][0]
    polarity="Δεν " if negative else ""
    if group%2==0:
        lemma,ru,en,forms=VERBS[group//2]
        expected=polarity+pronoun+" αρέσει να "+forms[p]
        ru_verb="нравится "+ru
        en_verb="like to "+en
    else:
        lemma,ru,en,plural=NOUNS[group//2]
        expected=polarity+pronoun+(" αρέσουν " if plural else " αρέσει ")+lemma
        ru_verb=("нравятся " if plural else "нравится ")+ru
        en_verb="like "+en
    ru_prompt=PERSONS[p][1].capitalize()+" "+("не " if negative else "")+ru_verb+"."
    english_subject=PERSONS[p][2].capitalize()
    en_prompt=english_subject+" "+("don't " if negative else "")+en_verb+"."
    if p in (2,3):
        en_prompt=english_subject+" "+("doesn't " if negative else "likes ")+(
            en_verb.removeprefix("like ") if not negative else en_verb)+"."
        # A negative person already carries "like" after doesn't.
    if p==0:en_prompt="I "+("don't " if negative else "")+en_verb+"."
    return {"promptRU":ru_prompt,"promptEN":en_prompt,
            "lemma":lemma,"negative":negative,"person":p,
            "expected":expected+"."}

def _init():return {"index":0,"misses":0}
def likes_get(db,uid,lang):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    state,rev=tracks._load(db,uid,"likes",lang,_init)
    if state["index"]>=LIKES_TOTAL:
        return {"revision":rev,"completed":True,"total":LIKES_TOTAL,
                "misses":state["misses"]}
    data=_like_scene(state["index"])
    return {"revision":rev,"step":state["index"]+1,"total":LIKES_TOTAL,
            "misses":state["misses"],"chapter":6,
            "prompt":data["promptRU"] if lang=="ru" else data["promptEN"],
            "promptLang":"ru" if lang=="ru" else "en",
            "lemma":data["lemma"]}
def likes_action(db,uid,lang,body):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    state,rev=tracks._load(db,uid,"likes",lang,_init)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    action=body.get("action")
    if action not in ("submit","restart"):raise ValueError("invalid_track_action")
    feedback=None
    if action=="restart":
        if state["index"]<LIKES_TOTAL:raise ValueError("not_finished")
        state["index"]=0
    else:
        if state["index"]>=LIKES_TOTAL:raise ValueError("already_finished")
        answer=body.get("answer")
        if not isinstance(answer,str) or len(answer)>180:raise ValueError("invalid_answer")
        expected=_like_scene(state["index"])["expected"]
        correct=tracks._normalized(answer)==tracks._normalized(expected)
        feedback={"correct":correct,"expected":expected}
        if correct:state["index"]+=1
        else:state["misses"]+=1
    tracks._save(db,uid,"likes",lang,state,rev)
    view=likes_get(db,uid,lang) if state["index"]<LIKES_TOTAL else {
        "revision":rev+1,"completed":True,"total":LIKES_TOTAL,"misses":state["misses"]}
    view["feedback"]=feedback
    return view

PRODUCTS=(
 ("apple","одно яблоко","one apple","ένα μήλο","🍎"),
 ("milk","один литр молока","one litre of milk","ένα λίτρο γάλα","🥛"),
 ("water","одну бутылку воды","one bottle of water","ένα μπουκάλι νερό","💧"),
 ("beef","полкило говядины","half a kilo of beef","μισό κιλό μοσχάρι","🥩"),
 ("bread","одну буханку хлеба","one loaf of bread","ένα ψωμί","🍞"),
 ("cheese","полкило сыра","half a kilo of cheese","μισό κιλό τυρί","🧀"),
 ("tomato","килограмм помидоров","one kilo of tomatoes","ένα κιλό ντομάτες","🍅"),
 ("orange","два килограмма апельсинов","two kilos of oranges","δύο κιλά πορτοκάλια","🍊"),
 ("eggs","шесть яиц","six eggs","έξι αυγά","🥚"),
 ("banana","три банана","three bananas","τρεις μπανάνες","🍌"),
 ("sugar","килограмм сахара","one kilo of sugar","ένα κιλό ζάχαρη","🛍️"),
 ("juice","один апельсиновый сок","one orange juice","έναν χυμό πορτοκάλι","🧃"),
)
REQUESTS=("θα ήθελα ","θέλω ","μπορώ να έχω ","θα πάρω ")
def _store_init():return {"round":0,"bought":[],"misses":0}
def _shopping_scene(round):
    # Stable sets of four, starting with the items explicitly requested.
    offset=(round*3)%len(PRODUCTS)
    return [PRODUCTS[(offset+i)%len(PRODUCTS)] for i in range(4)]
def _items(scene,lang):
    return [{"id":p[0],"name":p[1] if lang=="ru" else p[2],
             "icon":p[4]} for p in scene]
def store_get(db,uid,lang):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    state,rev=tracks._load(db,uid,"periptero",lang,_store_init)
    scene=_shopping_scene(state["round"])
    return {"revision":rev,"round":state["round"]+1,
            "items":_items(scene,lang),"bought":list(state["bought"]),
            "misses":state["misses"],"chapter":6,
            "translationLang":"ru" if lang=="ru" else "en",
            "stage":"complete" if len(state["bought"])==4 else "shopping"}
def store_action(db,uid,lang,body):
    if lang not in tracks.LANGUAGES:raise ValueError("invalid_language")
    db.execute("BEGIN IMMEDIATE")
    state,rev=tracks._load(db,uid,"periptero",lang,_store_init)
    if body.get("revision")!=rev:raise ValueError("stale_track")
    scene=_shopping_scene(state["round"])
    action=body.get("action")
    feedback=None
    if action=="next":
        if len(state["bought"])!=4:raise ValueError("not_finished")
        state.update(round=state["round"]+1,bought=[])
    elif action=="buy":
        if len(state["bought"])==4:raise ValueError("already_finished")
        product=next((p for p in scene if p[0]==body.get("productId")),None)
        if product is None or product[0] in state["bought"]:raise ValueError("invalid_item")
        phrase=body.get("phrase")
        if not isinstance(phrase,str) or len(phrase)>250:raise ValueError("invalid_answer")
        normalized=tracks._normalized(phrase)
        correct=any(normalized==tracks._normalized(start+product[3]) or
                    normalized==tracks._normalized(start+product[3]+" παρακαλώ")
                    for start in REQUESTS)
        feedback={"correct":correct,"expected":"Θα ήθελα "+product[3]+", παρακαλώ.",
                  "productId":product[0]}
        if correct:state["bought"].append(product[0])
        else:state["misses"]+=1
    else:raise ValueError("invalid_track_action")
    tracks._save(db,uid,"periptero",lang,state,rev)
    return {**store_get(db,uid,lang),"feedback":feedback}

def validate():
    assert LIKES_TOTAL==280
    assert len(PRODUCTS)>=12 and len({p[0] for p in PRODUCTS})==len(PRODUCTS)
    assert len(set(p[3] for p in PRODUCTS))==len(PRODUCTS)
    for i in range(LIKES_TOTAL):
        d=_like_scene(i)
        assert (" αρέσει να " in d["expected"] if (i//14)%2==0 else " αρέσει " in d["expected"] or " αρέσουν " in d["expected"])
        assert "Δεν " in d["expected"] if i%2 else "Δεν " not in d["expected"]
    for i in range(24):
        scene=_shopping_scene(i)
        assert len(scene)==len(set(x[0] for x in scene))==4
    return LIKES_TOTAL,len(PRODUCTS)
