"""Curated independent A1/A2 topic vocabulary and verified present-tense patterns.
Items are supplemental teaching material, NOT textbook page transcriptions.
"""
THEMES=[
 ("shopping","Магазин и покупки","Shopping",["shop","buy","price","cost","money","bill","market","supermarket","cheap","expensive","euro","book","pen","pencil","ticket","sell","offer","cashier"]),
 ("road","Дорога и автомобиль","Road & car",["road","street","car","train","bus","station","stop","taxi","metro","ticket","right","left","driver","travel","airport","port","departure","arrival"]),
 ("home","Дом, кухня и комнаты","Home & kitchen",["house","home","apartment","room","bathroom","bedroom","kitchen","balcony","door","window","bed","fridge","chair","table","floor","rent","cupboard","sink"]),
 ("food","Еда и продукты","Food & groceries",["bread","cheese","milk","water","coffee","fish","meat","tomato","potato","fruit","apple","orange","banana","salad","fresh","kilogram","eat","drink"]),
 ("family","Семья и люди","Family & people",["mother","father","wife","husband","daughter","son","child","brother","sister","uncle","aunt","grand","cousin","friend","family","married"]),
 ("work","Работа и учёба","Work & study",["job","work","office","teacher","doctor","student","manager","meeting","company","computer","message","customer","salary","study","school","university","engineer","writing"]),
 ("city","Город и учреждения","City & services",["city","village","bank","post office","pharmacy","hospital","library","centre","square","street","market","museum","church","government","form","document","signature","queue"]),
 ("health","Здоровье","Health",["doctor","hospital","pharmacy","medicine","fever","headache","pain","sick","health","throat","stomach","leg","arm","hand","cough","cold"]),
 ("time","Время и расписание","Time & schedule",["monday","tuesday","wednesday","thursday","friday","saturday","sunday","week","day","today","tomorrow","yesterday","morning","evening","night","afternoon","time","year","month","hour"]),
 ("travel","Путешествия","Travel",["trip","travel","holiday","hotel","passport","booking","airport","aeroplane","train","ship","sea","island","beach","suitcase","tourist","map"]),
 ("leisure","Досуг и развлечения","Leisure",["walk","cinema","film","music","concert","theatre","museum","park","café","sing","dance","friends","book","photograph"]),
 ("nature","Природа и погода","Nature & weather",["sea","beach","sun","rain","wind","tree","flower","mountain","river","cloud","weather","season"]),
]
# topic|CEFR|Greek|Russian|English (independent new lexical entries)
TOPIC_RAW="""
shopping|A1|το ταμείο|касса|the checkout
shopping|A1|η απόδειξη|чек о покупке|the receipt
shopping|A2|η έκπτωση|скидка|the discount
shopping|A2|τα ρέστα|сдача (деньги)|the change (money)
shopping|A1|το καλάθι|корзина|the shopping basket
shopping|A2|η προσφορά|специальное предложение|the special offer
road|A1|το αυτοκίνητο|автомобиль|the car
road|A1|ο δρόμος|дорога|the road
road|A1|το φανάρι|светофор|the traffic light
road|A2|το τιμόνι|руль|the steering wheel
road|A2|η διασταύρωση|перекрёсток|the intersection
road|A2|η ζώνη ασφαλείας|ремень безопасности|the seat belt
road|A1|το πάρκινγκ|парковка|the parking lot
road|A2|η βενζίνη|бензин|petrol
road|A2|το πεζοδρόμιο|тротуар|the pavement (sidewalk)
home|A1|το πιάτο|тарелка|the plate
home|A1|το ποτήρι|стакан|the drinking glass
home|A1|το μαχαίρι|нож|the knife
home|A1|το πιρούνι|вилка|the fork
home|A1|το κουτάλι|ложка|the spoon
home|A2|η κατσαρόλα|кастрюля|the saucepan
home|A1|η ντουλάπα|шкаф|the wardrobe
home|A2|το πλυντήριο|стиральная машина|the washing machine
home|A2|ο νεροχύτης|кухонная раковина|the kitchen sink
home|A1|το πάτωμα|пол в помещении|the floor (inside a room)
food|A1|το αυγό|яйцо|the egg
food|A1|το κοτόπουλο|курица (мясо)|chicken
food|A1|το ρύζι|рис|rice
food|A1|το λάδι|растительное масло|cooking oil
food|A1|το βούτυρο|сливочное масло|butter
food|A1|η ζάχαρη|сахар|sugar
food|A1|το αλάτι|соль|salt
food|A2|το πιπέρι|перец (приправа)|black pepper
food|A1|το κρεμμύδι|лук (овощ)|the onion
work|A1|η οθόνη|экран|the screen
work|A1|το πληκτρολόγιο|клавиатура|the keyboard
work|A1|το ποντίκι|компьютерная мышь|the computer mouse
work|A2|η προθεσμία|срок исполнения|the deadline
work|A2|η άδεια|отпуск / разрешение|leave / permission
work|A2|το βιογραφικό|резюме|the CV
city|A1|η βιβλιοθήκη|библиотека|the library
city|A2|το δημαρχείο|мэрия|the town hall
city|A1|η εκκλησία|церковь|the church
city|A2|η γειτονιά|район / соседство|the neighbourhood
city|A2|η γέφυρα|мост|the bridge
city|A1|η είσοδος|вход|the entrance
city|A1|η έξοδος|выход|the exit
health|A2|η συνταγή|рецепт врача|the medical prescription
health|A2|η εξέταση|обследование|the medical examination
health|A1|η αρρώστια|болезнь|the illness
health|A2|η πίεση|давление|blood pressure
health|A2|το ασθενοφόρο|скорая помощь (машина)|the ambulance
time|A1|το ρολόι|часы|the clock
time|A1|ο μήνας|месяц|the month
time|A1|ο χρόνος|год / время|the year
time|A2|η ημερομηνία|дата|the date
time|A2|η εποχή|время года|the season
travel|A2|η πτήση|авиарейс|the flight
travel|A2|η επιβίβαση|посадка (на самолёт)|boarding
travel|A2|η καθυστέρηση|задержка|the delay
travel|A1|ο προορισμός|пункт назначения|the destination
travel|A1|ο ταξιδιώτης|путешественник|the traveller
leisure|A1|το ποδήλατο|велосипед|the bicycle
leisure|A1|η φωτογραφία|фотография|the photograph
leisure|A2|η γυμναστική|физические упражнения|exercise (fitness)
leisure|A2|το παιχνίδι|игра|the game
leisure|A1|το βιβλιοπωλείο|книжный магазин|the bookshop
nature|A1|ο ήλιος|солнце|the sun
nature|A1|η βροχή|дождь|the rain
nature|A1|ο αέρας|ветер / воздух|the wind
nature|A1|το δέντρο|дерево|the tree
nature|A1|το λουλούδι|цветок|the flower
nature|A2|το βουνό|гора|the mountain
nature|A2|το ποτάμι|река|the river
nature|A2|το σύννεφο|облако|the cloud
"""
TOPIC_EXTRA=[]
for i,line in enumerate(TOPIC_RAW.strip().splitlines(),1):
    topic,level,gr,ru,en=line.split("|")
    TOPIC_EXTRA.append(dict(id=f"topic{i:03d}",chapter=-8,unit=-8,page=0,
                            kind="word",gr=gr,ru=ru,en=en,topic=topic,
                            level=level,topics=[topic],curriculum="topic",source="original"))
# Verbs in the present indicative, rows: εγώ εσύ αυτός/αυτή εμείς εσείς αυτοί/αυτές.
VERBS=[
 ("A","A1","γράφω","писать","write",["γράφω","γράφεις","γράφει","γράφουμε","γράφετε","γράφουν"]),
 ("A","A1","μένω","жить / оставаться","live",["μένω","μένεις","μένει","μένουμε","μένετε","μένουν"]),
 ("A","A1","διαβάζω","читать","read",["διαβάζω","διαβάζεις","διαβάζει","διαβάζουμε","διαβάζετε","διαβάζουν"]),
 ("A","A1","δουλεύω","работать","work",["δουλεύω","δουλεύεις","δουλεύει","δουλεύουμε","δουλεύετε","δουλεύουν"]),
 ("A","A1","αγοράζω","покупать","buy",["αγοράζω","αγοράζεις","αγοράζει","αγοράζουμε","αγοράζετε","αγοράζουν"]),
 ("A","A2","παίζω","играть","play",["παίζω","παίζεις","παίζει","παίζουμε","παίζετε","παίζουν"]),
 ("A","A2","μαθαίνω","изучать","learn",["μαθαίνω","μαθαίνεις","μαθαίνει","μαθαίνουμε","μαθαίνετε","μαθαίνουν"]),
 ("B1","A1","μιλάω","говорить","speak",["μιλάω","μιλάς","μιλάει","μιλάμε","μιλάτε","μιλάνε"]),
 ("B1","A1","ρωτάω","спрашивать","ask",["ρωτάω","ρωτάς","ρωτάει","ρωτάμε","ρωτάτε","ρωτάνε"]),
 ("B1","A1","αγαπάω","любить","love",["αγαπάω","αγαπάς","αγαπάει","αγαπάμε","αγαπάτε","αγαπάνε"]),
 ("B1","A2","περπατάω","гулять пешком","walk",["περπατάω","περπατάς","περπατάει","περπατάμε","περπατάτε","περπατάνε"]),
 ("B1","A2","απαντάω","отвечать","answer",["απαντάω","απαντάς","απαντάει","απαντάμε","απαντάτε","απαντάνε"]),
 ("B2","A1","μπορώ","мочь","be able to",["μπορώ","μπορείς","μπορεί","μπορούμε","μπορείτε","μπορούν"]),
 ("B2","A2","οδηγώ","водить машину","drive",["οδηγώ","οδηγείς","οδηγεί","οδηγούμε","οδηγείτε","οδηγούν"]),
 ("B2","A2","τηλεφωνώ","звонить по телефону","phone",["τηλεφωνώ","τηλεφωνείς","τηλεφωνεί","τηλεφωνούμε","τηλεφωνείτε","τηλεφωνούν"]),
 ("B2","A2","θεωρώ","считать / полагать","consider",["θεωρώ","θεωρείς","θεωρεί","θεωρούμε","θεωρείτε","θεωρούν"]),
 ("B2","A2","χρησιμοποιώ","использовать","use",["χρησιμοποιώ","χρησιμοποιείς","χρησιμοποιεί","χρησιμοποιούμε","χρησιμοποιείτε","χρησιμοποιούν"])
]
PEOPLE=["εγώ","εσύ","αυτός / αυτή","εμείς","εσείς","αυτοί / αυτές"]
# Correct accepted alternatives, colloquial and standard B1 forms.
B1_ALTERNATES={0:lambda root:[root+"ώ"],2:lambda root:[root+"ά"],3:lambda root:[root+"ούμε"],5:lambda root:[root+"ούν"]}
def verb_cards():
    from verb_curriculum import first_unit
    out=[]
    for idx,(group,level,lemma,ru,en,forms) in enumerate(VERBS,1):
        assert len(forms)==6
        root=lemma[:-2] if lemma.endswith("άω") else lemma[:-1]
        for person,form in enumerate(forms):
            alternatives=[form]
            if group=="B1" and person in B1_ALTERNATES:
                alternatives+=B1_ALTERNATES[person](root)
            # Group variants are forms of this specific verb, not other subjects.
            out.append(dict(id=f"verb{idx:02d}_{person}",kind="verb",chapter=-9,unit=-9,page=0,
                            source="original",curriculum="verb",gr=lemma,ru=ru,en=en,level=level,
                            group=group,person=person,personName=PEOPLE[person],
                            forms=forms,accepted=list(dict.fromkeys(alternatives)),topic=group,
                            introducedUnit=first_unit(lemma),
                            topics=["work"] if lemma in ("δουλεύω","τηλεφωνώ") else []))
    return out

