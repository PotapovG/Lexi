import greek_variants
"""Independent authored A1/A2 vocabulary lessons; never injected into book exercises.
CEFR descriptors do not prescribe exact word counts. Levels are editorial estimates.
"""
import hashlib
import json
import random
import datetime as dt
from pathlib import Path
from catalog_v2 import ALL
import topics_verbs

# Additional original teaching entries: topic|level|Greek|Russian|English.
# Greek headwords (including noun article) are counted once, not per inflected form.
EXTRA_RAW = """
shopping|A1|ο πελάτης|покупатель|customer
shopping|A1|η πελάτισσα|покупательница|female customer
shopping|A1|το προϊόν|товар|product
shopping|A1|το μέγεθος|размер|size
shopping|A1|το χρώμα|цвет|colour
shopping|A1|το παντελόνι|брюки|trousers
shopping|A1|η μπλούζα|кофта|top
shopping|A1|το φόρεμα|платье|dress
shopping|A1|το παπούτσι|ботинок|shoe
shopping|A1|η τσάντα|сумка|bag
shopping|A1|το πορτοφόλι|кошелёк|wallet
shopping|A2|η παραγγελία|заказ|order
shopping|A2|η επιστροφή|возврат|return
shopping|A2|η πληρωμή|оплата|payment
shopping|A2|η τιμή|цена|price
shopping|A2|η ποιότητα|качество|quality
shopping|A2|ο πωλητής|продавец|salesperson
shopping|A2|η εγγύηση|гарантия|warranty
shopping|A2|το νόμισμα|валюта|currency
shopping|A2|η κάρτα|карта для оплаты|payment card
road|A1|ο οδηγός|водитель|driver
road|A1|η στάση|остановка|stop
road|A1|η λεωφόρος|проспект|avenue
road|A1|το λεωφορείο|автобус|bus
road|A1|η μοτοσικλέτα|мотоцикл|motorcycle
road|A1|η ταχύτητα|скорость|speed
road|A1|ο χάρτης|карта местности|map
road|A2|η κυκλοφορία|движение транспорта|traffic
road|A2|η στροφή|поворот|turn
road|A2|η κατεύθυνση|направление|direction
road|A2|το εισιτήριο|билет|ticket
road|A2|η άδεια οδήγησης|водительские права|driving licence
road|A2|το φρένο|тормоз|brake
road|A2|ο κινητήρας|двигатель|engine
road|A2|η στάθμευση|парковка|parking
road|A2|ο πεζός|пешеход|pedestrian
road|A2|η διάβαση|пешеходный переход|crossing
road|A2|το ατύχημα|авария|accident
road|A2|η πινακίδα|дорожный знак|road sign
home|A1|ο καναπές|диван|sofa
home|A1|το μαξιλάρι|подушка|pillow
home|A1|η κουβέρτα|одеяло|blanket
home|A1|η πετσέτα|полотенце|towel
home|A1|ο καθρέφτης|зеркало|mirror
home|A1|το φως|свет|light
home|A1|ο τοίχος|стена|wall
home|A1|η σκάλα|лестница|staircase
home|A1|το κλειδί|ключ|key
home|A1|το μπάνιο|ванная|bathroom
home|A2|η βρύση|кран для воды|tap
home|A2|ο φούρνος|духовка|oven
home|A2|η καρέκλα|стул|chair
home|A2|το τραπέζι|стол|table
home|A2|το ταβάνι|потолок|ceiling
home|A2|η θέρμανση|отопление|heating
home|A2|το ενοίκιο|арендная плата|rent
home|A2|ο ιδιοκτήτης|владелец жилья|landlord
home|A2|η επισκευή|ремонт|repair
home|A2|το συμβόλαιο|договор|contract
food|A1|το σταφύλι|виноград|grape
food|A1|το καρπούζι|арбуз|watermelon
food|A1|το πεπόνι|дыня|melon
food|A1|το λεμόνι|лимон|lemon
food|A1|το αγγούρι|огурец|cucumber
food|A1|το καρότο|морковь|carrot
food|A1|τα φασόλια|фасоль|beans
food|A1|η σούπα|суп|soup
food|A1|το γιαούρτι|йогурт|yoghurt
food|A1|το μέλι|мёд|honey
food|A2|το αλεύρι|мука|flour
food|A2|το ξίδι|уксус|vinegar
food|A2|η μερίδα|порция|portion
food|A2|το επιδόρπιο|десерт|dessert
food|A2|η συνταγή μαγειρικής|кулинарный рецепт|cooking recipe
food|A2|το πιάτο ημέρας|блюдо дня|dish of the day
food|A2|το ορεκτικό|закуска|starter
food|A2|η γεύση|вкус|taste
food|A2|το τηγάνι|сковорода|frying pan
family|A1|ο παππούς|дедушка|grandfather
family|A1|η γιαγιά|бабушка|grandmother
family|A1|ο εγγονός|внук|grandson
family|A1|η εγγονή|внучка|granddaughter
family|A1|ο ξάδελφος|двоюродный брат|male cousin
family|A1|η ξαδέλφη|двоюродная сестра|female cousin
family|A1|ο γείτονας|сосед|neighbour
family|A1|η γειτόνισσα|соседка|female neighbour
family|A1|ο άντρας|мужчина|man
family|A1|η γυναίκα|женщина|woman
family|A1|το μωρό|младенец|baby
family|A2|η σχέση|отношения|relationship
family|A2|ο γάμος|свадьба|wedding
family|A2|το ζευγάρι|пара|couple
family|A2|ο συνάδελφος|коллега|colleague
family|A2|η ηλικία|возраст|age
family|A2|η γέννηση|рождение|birth
family|A2|η φιλία|дружба|friendship
work|A1|το τετράδιο|тетрадь|notebook
work|A1|η άσκηση|упражнение|exercise
work|A1|η ερώτηση|вопрос|question
work|A1|η απάντηση|ответ|answer
work|A1|το μάθημα|урок|lesson
work|A1|η τάξη|класс|classroom
work|A1|ο πίνακας|доска|board
work|A1|το γραφείο|офис или стол|office or desk
work|A1|το τηλέφωνο|телефон|telephone
work|A2|η συνέντευξη|собеседование|interview
work|A2|ο μισθός|зарплата|salary
work|A2|η σύσκεψη|рабочее совещание|meeting
work|A2|ο υπάλληλος|сотрудник|employee
work|A2|η εμπειρία|опыт|experience
work|A2|το πρόγραμμα|программа или расписание|schedule
work|A2|η εκπαίδευση|образование|education
work|A2|η ειδικότητα|специальность|specialty
work|A2|η υπογραφή|подпись|signature
work|A2|το έγγραφο|документ|document
work|A2|το μήνυμα|сообщение|message
city|A1|το πάρκο|парк|park
city|A1|η πλατεία|площадь|square
city|A1|το φαρμακείο|аптека|pharmacy
city|A1|το μουσείο|музей|museum
city|A1|η τράπεζα|банк|bank
city|A1|το ταχυδρομείο|почта|post office
city|A1|το νοσοκομείο|больница|hospital
city|A1|το σχολείο|школа|school
city|A2|η υπηρεσία|государственная служба|public service
city|A2|ο δήμος|муниципалитет|municipality
city|A2|η αίτηση|заявление|application
city|A2|το διαβατήριο|паспорт|passport
city|A2|η άδεια παραμονής|вид на жительство|residence permit
city|A2|το κέντρο|центр|centre
city|A2|η περιοχή|район|area
city|A2|το πεζοδρόμιο|тротуар|sidewalk
city|A2|η διεύθυνση|адрес|address
city|A2|ο ταχυδρόμος|почтальон|postman
health|A1|το κεφάλι|голова|head
health|A1|το μάτι|глаз|eye
health|A1|το αυτί|ухо|ear
health|A1|η μύτη|нос|nose
health|A1|το στόμα|рот|mouth
health|A1|το δόντι|зуб|tooth
health|A1|το χέρι|рука|hand
health|A1|το πόδι|нога|leg
health|A1|η κοιλιά|живот|belly
health|A1|ο λαιμός|шея или горло|neck or throat
health|A2|το φάρμακο|лекарство|medicine
health|A2|η θερμοκρασία|температура|temperature
health|A2|η αλλεργία|аллергия|allergy
health|A2|η ασφάλεια υγείας|медицинская страховка|health insurance
health|A2|η διάγνωση|диагноз|diagnosis
health|A2|το σύμπτωμα|симптом|symptom
health|A2|ο πόνος|боль|pain
health|A2|ο βήχας|кашель|cough
health|A2|η θεραπεία|лечение|treatment
time|A1|η ώρα|час или время|hour or time
time|A1|το λεπτό|минута|minute
time|A1|το δευτερόλεπτο|секунда|second
time|A1|το πρωί|утро|morning
time|A1|το βράδυ|вечер|evening
time|A1|το μεσημέρι|полдень|noon
time|A1|τα μεσάνυχτα|полночь|midnight
time|A1|το Σαββατοκύριακο|выходные|weekend
time|A2|η διάρκεια|продолжительность|duration
time|A2|το ραντεβού|встреча по записи|appointment
time|A2|η αρχή|начало|beginning
time|A2|το τέλος|конец|end
time|A2|η στιγμή|момент|moment
time|A2|το μέλλον|будущее|future
time|A2|το παρελθόν|прошлое|past
time|A2|η προθεσμία|крайний срок|deadline
travel|A1|η βαλίτσα|чемодан|suitcase
travel|A1|ο σταθμός|станция|station
travel|A1|το αεροπλάνο|самолёт|aeroplane
travel|A1|το αεροδρόμιο|аэропорт|airport
travel|A1|το ξενοδοχείο|отель|hotel
travel|A1|η παραλία|пляж|beach
travel|A1|το ταξίδι|путешествие|trip
travel|A1|το νησί|остров|island
travel|A2|η κράτηση|бронирование|reservation
travel|A2|η αναχώρηση|отправление|departure
travel|A2|η άφιξη|прибытие|arrival
travel|A2|η διαμονή|проживание|accommodation
travel|A2|η αποσκευή|багаж|luggage
travel|A2|η ακύρωση|отмена|cancellation
travel|A2|ο επιβάτης|пассажир|passenger
travel|A2|η ανταπόκριση|пересадка|connection
travel|A2|το δρομολόγιο|маршрут|itinerary
travel|A2|το σύνορο|граница|border
leisure|A1|το τραγούδι|песня|song
leisure|A1|ο χορός|танец|dance
leisure|A1|το θέατρο|театр|theatre
leisure|A1|η ταινία|фильм|film
leisure|A1|η μουσική|музыка|music
leisure|A1|το βιβλίο|книга|book
leisure|A1|το ποδόσφαιρο|футбол|football
leisure|A1|το μπάσκετ|баскетбол|basketball
leisure|A2|η παράσταση|спектакль|performance
leisure|A2|η εκδήλωση|мероприятие|event
leisure|A2|η έκθεση|выставка|exhibition
leisure|A2|το εισιτήριο|билет|ticket
leisure|A2|η συναυλία|концерт|concert
leisure|A2|η συλλογή|коллекция|collection
leisure|A2|η φωτογραφική μηχανή|фотоаппарат|camera
leisure|A2|ο περίπατος|прогулка|walk
leisure|A2|η ζωγραφική|рисование|painting
nature|A1|η θάλασσα|море|sea
nature|A1|ο ουρανός|небо|sky
nature|A1|το αστέρι|звезда|star
nature|A1|το φεγγάρι|луна|moon
nature|A1|η άμμος|песок|sand
nature|A1|το δάσος|лес|forest
nature|A1|η λίμνη|озеро|lake
nature|A1|το χιόνι|снег|snow
nature|A1|ο χειμώνας|зима|winter
nature|A1|το καλοκαίρι|лето|summer
nature|A1|η άνοιξη|весна|spring
nature|A1|το φθινόπωρο|осень|autumn
nature|A2|η καταιγίδα|гроза|storm
nature|A2|η ζέστη|жара|heat
nature|A2|το κρύο|холод|cold
nature|A2|η υγρασία|влажность|humidity
nature|A2|η σκιά|тень|shadow
nature|A2|η φύση|природа|nature
nature|A2|το περιβάλλον|окружающая среда|environment
nature|A2|η ακτή|побережье|coast
"""
ADDONS = []
for idx, line in enumerate(EXTRA_RAW.strip().splitlines(),1):
    t,level,gr,ru,en = line.strip().split("|")
    ADDONS.append(dict(id=f"vx{idx:04}", gr=gr,ru=ru,en=en,topics=[t],level=level,source="original_curated"))

for idx, line in enumerate(Path(__file__).with_name("vocab_more.tsv").read_text(encoding="utf-8").strip().splitlines(),3000):
    t,level,gr,ru,en=line.strip().split("|")
    ADDONS.append(dict(id=f"vx{idx:04}",gr=gr,ru=ru,en=en,topics=[t],level=level,source="original_curated"))

# Additional carefully selected lexical headwords for the 700 / 1000 vocabulary goal.
# IDs are content-stable rather than row-number based, so future content reordering
# cannot erase a student's progress. Pre-existing wx/vx/book IDs stay unchanged.
import hashlib as _lexi_hashlib
_EXPANSION=Path(__file__).with_name("vocab_curated_1700.tsv")
for _row in _EXPANSION.read_text(encoding="utf-8").splitlines():
    if not _row.strip() or _row.startswith("#"):continue
    _topic,_level,_gr,_ru,_en=_row.split("|",4)
    _identifier="lexi_"+_lexi_hashlib.sha256(_gr.encode("utf-8")).hexdigest()[:20]
    ADDONS.append(dict(id=_identifier,gr=_gr,ru=_ru,en=_en,topics=[_topic],
                       level=_level,source="original_curated_vocab1700"))

# Translate where a lexicographic match exists; do not misrepresent fallback English as Arabic.
_AR_PATH=Path(__file__).with_name("translations_ar.json")
AR=json.loads(_AR_PATH.read_text(encoding="utf-8")) if _AR_PATH.exists() else {}
# Textbook words, numbers and sentences: complete pre-existing English-gloss
# keys with Arabic values, without changing the original card identity/meaning.
_AR_BOOK_COMPLETE=Path(__file__).with_name("textbook_ar_complete.json")
AR.update(json.loads(_AR_BOOK_COMPLETE.read_text(encoding="utf-8")))

def build_vocabulary():
    by_word={}
    for c in ALL:
        # Supplementary textbook cards must not expand the independent
        # 1,700-word A1/A2 course or change saved vocabulary IDs.
        if c["kind"]!="word" or c.get("source")=="original-from-book-syllabus":continue
        gr=c["gr"].strip()
        if not gr or gr in by_word:continue
        # Stable word IDs must not change when a pedagogical Greek typo is
        # corrected. Before this release the book-aligned expression was
        # written «την λένε»; printed lesson 3 uses standard «τη λένε».
        # Preserve the former sha-based ID and all saved vocab progress.
        legacy_gr={"τη λένε":"την λένε"}.get(gr,gr)
        o=dict(id="book_"+hashlib.sha256(legacy_gr.encode()).hexdigest()[:14],
               gr=gr,ru=c["ru"],en=c["en"],topics=list(c.get("topics") or ["everyday"]),
               level=c.get("level","A1"),source="book_aligned_original")
        by_word[gr]=o
    for o in ADDONS:
        if o["gr"] in by_word:
            # Additional thematic classification may improve discoverability.
            old=by_word[o["gr"]]
            old["topics"]=sorted(set(old["topics"])|set(o["topics"]))
        else:by_word[o["gr"]]=dict(o)
    for o in by_word.values():
        o["ar"]=AR.get(o["en"],"")
        for language in ("zh","es","pt"):
            match=next((c.get(language) for c in ALL if c["kind"]=="word" and c["gr"]==o["gr"]),"")
            o[language]=match or ""
    return list(by_word.values())

VOCAB=build_vocabulary()
# Reviewed ID-specific gloss atlas: all 1,700 course words in all supported
# languages. Retain original Greek lemma IDs and independent user progress.
_LOCALE_GLOSS_PATH=Path(__file__).with_name("vocab_translations_1700.json")
_LOCALE_GLOSS=json.loads(_LOCALE_GLOSS_PATH.read_text(encoding="utf-8"))
for _lang in ("ar","zh","es","pt"):
    _values=_LOCALE_GLOSS[_lang]
    if len(_values)!=len(VOCAB) or {w["id"] for w in VOCAB}!=set(_values):
        raise ValueError("Vocabulary localization ID mismatch for "+_lang)
    for _word in VOCAB:
        _translation=_values[_word["id"]]
        if not isinstance(_translation,str) or not _translation.strip():
            raise ValueError("Missing vocabulary translation for "+_word["id"]+" / "+_lang)
        _word[_lang]=_translation.strip()
VOCAB_BY_ID={w["id"]:w for w in VOCAB}
THEMES=[dict(id=k,ru=r,en=e) for k,r,e,_ in topics_verbs.THEMES]+[dict(id="everyday",ru="Повседневные слова",en="Everyday words")]

def visible_translation(w,lang):
    s=w.get(lang,"")
    if not s:return w["en"], True
    return s,False

def scoped(topic,level,lang=None):
    words=[w for w in VOCAB if (topic=="all" or topic in w["topics"]) and
           (level=="all" or level==w["level"])]
    return words

def schema(db):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS vocab_progress (
      user_id TEXT NOT NULL,
      word_id TEXT NOT NULL,
      attempts INTEGER NOT NULL DEFAULT 0,
      correct INTEGER NOT NULL DEFAULT 0,
      miss_debt INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL,
      PRIMARY KEY(user_id,word_id)
    );
    CREATE TABLE IF NOT EXISTS vocab_batches (
      user_id TEXT NOT NULL,
      scope TEXT NOT NULL,
      words_json TEXT NOT NULL,
      created_at TEXT NOT NULL,
      PRIMARY KEY(user_id,scope)
    );
    """)

def lesson(db,user,topic,level,lang,review=False):
    if topic not in {w["id"] for w in THEMES}|{"all"}:raise ValueError("invalid topic")
    if level not in ("A1","A2","all"):raise ValueError("invalid level")
    if lang not in ("ru","en","zh","ar","es","pt"):raise ValueError("invalid language")
    words=scoped(topic,level,lang)
    prog={r["word_id"]:r for r in db.execute("SELECT word_id,attempts,correct,miss_debt FROM vocab_progress WHERE user_id=?",(user,))}
    count_learned=sum(bool(prog.get(w["id"])) for w in words)
    weak=sum(bool(prog.get(w["id"]) and prog[w["id"]]["miss_debt"]>0) for w in words)
    if review:
        selected=[w for w in words if prog.get(w["id"]) and prog[w["id"]]["miss_debt"]>0]
        selected.sort(key=lambda w:(-prog[w["id"]]["miss_debt"],w["gr"]))
        selected=selected[:10]
    else:
        scope=f"{topic}:{level}"
        stored=db.execute("SELECT words_json FROM vocab_batches WHERE user_id=? AND scope=?",(user,scope)).fetchone()
        original=json.loads(stored["words_json"]) if stored else []
        remaining={w["id"] for w in words if w["id"] not in prog}
        # Keep an interrupted batch until all its words have been practised.
        if original and any(wid in remaining for wid in original):
            selected=[VOCAB_BY_ID[x] for x in original if x in VOCAB_BY_ID]
        else:
            pool=[w for w in words if w["id"] not in prog]
            # Deterministic per-user ordering, stable across page reloads.
            pool.sort(key=lambda w:hashlib.sha256((user+w["id"]).encode()).digest())
            selected=pool[:10]
            db.execute("""INSERT INTO vocab_batches(user_id,scope,words_json,created_at)
              VALUES(?,?,?,?) ON CONFLICT(user_id,scope) DO UPDATE SET
              words_json=excluded.words_json,created_at=excluded.created_at""",
              (user,scope,json.dumps([w["id"] for w in selected]),dt.datetime.now(dt.timezone.utc).isoformat()))
    output=[]
    for i,w in enumerate(selected):
        translation,missing=visible_translation(w,lang)
        candidates=[v for v in words if v["id"]!=w["id"] and visible_translation(v,lang)[0]!=translation]
        if len(candidates)<7:candidates=[v for v in VOCAB if v["id"]!=w["id"] and visible_translation(v,lang)[0]!=translation]
        rand=random.Random(user+w["id"]+lang)
        rand.shuffle(candidates)
        direction="gr-target" if i%2==0 else "target-gr"
        pairs=[(translation,w["en"]) if direction=="gr-target" else (w["gr"],w["gr"])]
        accepted_greek=greek_variants.accepted(w["gr"]) if direction=="target-gr" else []
        if len(accepted_greek)>1:
            pairs.append((accepted_greek[1],w["gr"]))
        for other in candidates:
            answer=visible_translation(other,lang)[0] if direction=="gr-target" else other["gr"]
            if answer not in accepted_greek and answer not in [p[0] for p in pairs]:
                pairs.append((answer,other["en"] if direction=="gr-target" else other["gr"]))
            if len(pairs)==8:break
        rand.shuffle(pairs)
        output.append(dict(id=w["id"],gr=w["gr"],greekVariants=greek_variants.variants(w["gr"]),translation=translation,english=w["en"],
                           untranslated=missing,level=w["level"],direction=direction,
                           choices=[p[0] for p in pairs],choicesEn=[p[1] for p in pairs],
                           topic=w["topics"][0]))
    return dict(words=output,mode="review" if review else "new",total=len(words),
                learned=count_learned,weak=weak,remaining=max(0,len(words)-count_learned),
                count=len(output),translated=sum(not x["untranslated"] for x in output))

def answer(db,user,body):
    wid=body.get("id")
    if not isinstance(wid,str) or wid not in VOCAB_BY_ID:raise ValueError("invalid word")
    w=VOCAB_BY_ID[wid]
    lang=body.get("lang","ru")
    direction=body.get("direction")
    if lang not in ("ru","en","zh","ar","es","pt") or direction not in ("gr-target","target-gr"):raise ValueError("invalid answer")
    text,missing=visible_translation(w,lang)
    expected=text if direction=="gr-target" else w["gr"]
    selected=body.get("selected")
    if not isinstance(selected,str) or len(selected)>500:raise ValueError("invalid answer")
    accepted=greek_variants.accepted(expected) if direction=="target-gr" else [expected]
    correct=selected in accepted
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    row=db.execute("SELECT miss_debt FROM vocab_progress WHERE user_id=? AND word_id=?",(user,wid)).fetchone()
    debt=(max(0,row["miss_debt"]-1) if correct else min(7,row["miss_debt"]+2)) if row else (0 if correct else 2)
    db.execute("""INSERT INTO vocab_progress(user_id,word_id,attempts,correct,miss_debt,updated_at)
      VALUES(?,?,?,?,?,?) ON CONFLICT(user_id,word_id) DO UPDATE SET
      attempts=attempts+1,correct=correct+excluded.correct,
      miss_debt=excluded.miss_debt,updated_at=excluded.updated_at""",
      (user,wid,1,int(correct),debt,now))
    return dict(correct=correct,answer=expected,acceptedAnswers=accepted,
                greekVariants=greek_variants.variants(w["gr"]),
                missDebt=debt,untranslated=missing)
