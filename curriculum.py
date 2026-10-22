"""Original self-authored exercises aligned to Patakis Ελληνικά Α΄ chapter topics.
Legacy internal 16-unit teaching corpus, NOT the printed book numbering.
The final mapping to verified 20 printed units and review sections is in
textbook_alignment.py (from the user's complete licensed PDF).
Per-card pages are approximate teaching anchors, not a transcription.
"""
CHAPTERS = [
 (1,14,23,"Γεια σας","Hello"),(2,24,37,"Πού μένεις;","Where do you live?"),
 (3,38,47,"Τι δουλειά κάνεις;","What do you do?"),(4,48,58,"Μιλάς ελληνικά;","Do you speak Greek?"),
 (5,66,79,"Πού πάτε;","Where are you going?"),(6,80,93,"Ποτέ την Κυριακή","Never on Sunday"),
 (7,94,107,"Πόσο κάνουν όλα;","How much is everything?"),(8,108,121,"Πάμε για ψώνια","Let's go shopping"),
 (9,132,149,"Ψάχνω για σπίτι","Looking for a home"),(10,150,165,"Ένα ταξίδι","A trip"),
 (11,166,183,"Η ιστορία της ζωής μου","My life story"),(12,184,199,"Τι θα κάνουμε;","What shall we do?"),
 (13,212,231,"Πάμε βόλτα","Let's go out"),(14,232,245,"Πάμε για δουλειά","Off to work"),
 (15,246,261,"Στον γιατρό","At the doctor"),(16,262,277,"Περιμένετε στην ουρά, παρακαλώ","Please wait in line")
]
EXTRA_SECTIONS = [(0,8,13,"Από το Α στο Ω","Alphabet"),(-1,59,65,"Πάμε πάλι","Review 1"),
 (-2,122,131,"Πάμε πάλι","Review 2"),(-3,200,211,"Πάμε πάλι","Review 3"),
 (-4,278,289,"Πάμε πάλι","Review 4"),(-5,290,312,"Παράρτημα","Appendix")]
# Each entry: Greek|Russian|English, all examples independently authored.
RAW = {
 5: {
 "word": """
πού πάω|куда я иду|where I am going
πάω|я иду / еду|I go
πηγαίνω|я иду / еду|I am going
πηγαίνεις|ты идёшь|you go
πηγαίνει|он / она идёт|he / she goes
πάμε|пойдём / мы идём|let's go / we go
πηγαίνετε|вы идёте|you go (plural)
πηγαίνουν|они идут|they go
το λεωφορείο|автобус|the bus
το ταξί|такси|the taxi
το τρόλεϊ|троллейбус|the trolleybus
το μετρό|метро|the metro
η στάση|остановка|the stop
ο σταθμός|станция|the station
το εισιτήριο|билет|the ticket
το σχολείο|школа|the school
το πανεπιστήμιο|университет|the university
η πλατεία|площадь|the square
το κέντρο|центр|the centre
δεξιά|направо|right
αριστερά|налево|left
ευθεία|прямо|straight ahead
κοντά|близко|near
μακριά|далеко|far
με|с / на (транспорте)|with / by
""",
 "phrase": """
Πώς πάω στο κέντρο;|Как добраться до центра?|How do I get to the centre?
Πού είναι η στάση;|Где остановка?|Where is the bus stop?
Πάμε με το λεωφορείο.|Поедем на автобусе.|Let's take the bus.
Ο σταθμός είναι κοντά.|Станция рядом.|The station is nearby.
Θέλω ένα εισιτήριο.|Я хочу билет.|I want a ticket.
""",
 "sentence": """
Η Άννα πηγαίνει στο πανεπιστήμιο με το λεωφορείο και ο Νίκος πάει με το μετρό.|Анна едет в университет на автобусе, а Никос — на метро.|Anna goes to university by bus and Nikos takes the metro.
Ο σταθμός είναι κοντά στην πλατεία, αλλά το σχολείο είναι μακριά.|Станция рядом с площадью, но школа далеко.|The station is near the square, but the school is far away.
"""},
 6: {
 "word": """
η Δευτέρα|понедельник|Monday
η Τρίτη|вторник|Tuesday
η Τετάρτη|среда|Wednesday
η Πέμπτη|четверг|Thursday
η Παρασκευή|пятница|Friday
το Σάββατο|суббота|Saturday
η Κυριακή|воскресенье|Sunday
η εβδομάδα|неделя|the week
η μέρα|день|the day
το πρωί|утро|the morning
το μεσημέρι|полдень|noon
το απόγευμα|послеобеденное время|the afternoon
το βράδυ|вечер|the evening
σήμερα|сегодня|today
αύριο|завтра|tomorrow
χτες|вчера|yesterday
πάντα|всегда|always
ποτέ|никогда|never
συχνά|часто|often
συνήθως|обычно|usually
μερικές φορές|иногда|sometimes
κάθε μέρα|каждый день|every day
δουλεύω|я работаю|I work
διαβάζω|я читаю|I read
κοιμάμαι|я сплю|I sleep
ξυπνάω|я просыпаюсь|I wake up
""",
 "phrase": """
Τι κάνεις την Κυριακή;|Что ты делаешь в воскресенье?|What do you do on Sunday?
Δουλεύω κάθε μέρα.|Я работаю каждый день.|I work every day.
Το Σάββατο δεν δουλεύω.|В субботу я не работаю.|I do not work on Saturday.
Ξυπνάω νωρίς το πρωί.|Я просыпаюсь рано утром.|I wake up early in the morning.
""",
 "sentence": """
Τη Δευτέρα δουλεύω το πρωί, αλλά την Κυριακή κοιμάμαι πολύ.|В понедельник я работаю утром, но в воскресенье много сплю.|On Monday I work in the morning, but on Sunday I sleep a lot.
Η Μαρία διαβάζει κάθε βράδυ και το Σάββατο πηγαίνει στο κέντρο.|Мария читает каждый вечер и по субботам ходит в центр.|Maria reads every evening and goes downtown on Saturdays.
"""},
 7: {
 "word": """
πόσο|сколько|how much
πόσα|сколько (мн.ч.)|how many
κάνει|стоит (о цене)|it costs
κάνουν|стоят|they cost
το ευρώ|евро|the euro
το λεπτό|цент / минута|the cent / minute
η τιμή|цена|the price
ακριβός|дорогой|expensive
φτηνός|дешёвый|cheap
το χρήμα|деньги|money
τα χρήματα|деньги (мн.ч.)|money
το βιβλίο|книга|the book
το τετράδιο|тетрадь|the notebook
το μολύβι|карандаш|the pencil
το στυλό|ручка|the pen
η τσάντα|сумка|the bag
η καρέκλα|стул|the chair
το τραπέζι|стол|the table
ο καφές|кофе|coffee
το νερό|вода|water
ο λογαριασμός|счёт|the bill
πληρώνω|я плачу|I pay
αγοράζω|я покупаю|I buy
θέλω|я хочу|I want
ένας καφές|один кофе|one coffee
""",
 "phrase": """
Πόσο κάνει αυτό το βιβλίο;|Сколько стоит эта книга?|How much is this book?
Όλα κάνουν είκοσι ευρώ.|Всё стоит двадцать евро.|Everything costs twenty euros.
Θέλω έναν καφέ, παρακαλώ.|Я хочу кофе, пожалуйста.|I would like a coffee, please.
Ο λογαριασμός, παρακαλώ.|Счёт, пожалуйста.|The bill, please.
""",
 "sentence": """
Το βιβλίο κάνει δέκα ευρώ και το τετράδιο κάνει τρία ευρώ.|Книга стоит десять евро, а тетрадь — три.|The book costs ten euros and the notebook costs three.
Θέλω έναν καφέ και νερό, αλλά δεν έχω πολλά χρήματα.|Я хочу кофе и воду, но у меня мало денег.|I want a coffee and water, but I do not have much money.
"""},
 8: {
 "word": """
τα ψώνια|покупки|shopping
το κατάστημα|магазин|the shop
το σούπερ μάρκετ|супермаркет|the supermarket
η αγορά|рынок|the market
το φρούτο|фрукт|the fruit
το μήλο|яблоко|the apple
η μπανάνα|банан|the banana
το πορτοκάλι|апельсин|the orange
η ντομάτα|помидор|the tomato
η πατάτα|картофель|the potato
το ψωμί|хлеб|bread
το γάλα|молоко|milk
το τυρί|сыр|cheese
το κρέας|мясо|meat
το ψάρι|рыба|fish
η σαλάτα|салат|the salad
ένα κιλό|один килограмм|one kilogram
μισό|половина|half
φρέσκος|свежий|fresh
μεγάλος|большой|big
μικρός|маленький|small
κόκκινος|красный|red
πράσινος|зелёный|green
άσπρος|белый|white
""",
 "phrase": """
Θέλω ένα κιλό ντομάτες.|Я хочу килограмм помидоров.|I would like a kilogram of tomatoes.
Έχετε φρέσκο ψωμί;|У вас есть свежий хлеб?|Do you have fresh bread?
Πάμε στο σούπερ μάρκετ.|Пойдём в супермаркет.|Let's go to the supermarket.
Πόσο κάνουν τα μήλα;|Сколько стоят яблоки?|How much are the apples?
""",
 "sentence": """
Σήμερα αγοράζω ψωμί, τυρί και ντομάτες από το σούπερ μάρκετ.|Сегодня я покупаю в супермаркете хлеб, сыр и помидоры.|Today I buy bread, cheese and tomatoes at the supermarket.
Θέλω ένα κιλό μήλα και μισό κιλό πορτοκάλια, παρακαλώ.|Я хочу килограмм яблок и полкило апельсинов.|I would like a kilo of apples and half a kilo of oranges, please.
"""},
 9: {
 "word": """
το διαμέρισμα|квартира|the apartment
η πολυκατοικία|многоквартирный дом|the apartment building
το δωμάτιο|комната|the room
η κουζίνα|кухня|the kitchen
το μπάνιο|ванная|the bathroom
το υπνοδωμάτιο|спальня|the bedroom
το σαλόνι|гостиная|the living room
το μπαλκόνι|балкон|the balcony
ο όροφος|этаж|the floor
το ενοίκιο|арендная плата|the rent
ο ιδιοκτήτης|владелец|the owner
νοικιάζω|я снимаю / сдаю|I rent
ψάχνω|я ищу|I am looking for
βρίσκω|я нахожу|I find
η πόρτα|дверь|the door
το παράθυρο|окно|the window
το κρεβάτι|кровать|the bed
το ψυγείο|холодильник|the fridge
το κλειδί|ключ|the key
επιπλωμένο|меблированное|furnished
φωτεινό|светлое (помещение)|bright
ήσυχο|тихое|quiet
""",
 "phrase": """
Ψάχνω για ένα διαμέρισμα.|Я ищу квартиру.|I am looking for an apartment.
Πόσο είναι το ενοίκιο;|Сколько стоит аренда?|How much is the rent?
Το διαμέρισμα έχει δύο υπνοδωμάτια.|В квартире две спальни.|The apartment has two bedrooms.
Είναι κοντά στο κέντρο;|Это близко к центру?|Is it near the centre?
""",
 "sentence": """
Ψάχνω για ένα μικρό διαμέρισμα με δύο δωμάτια και μπαλκόνι.|Я ищу небольшую квартиру с двумя комнатами и балконом.|I am looking for a small apartment with two rooms and a balcony.
Η κουζίνα είναι μεγάλη, αλλά το μπάνιο είναι μικρό και δεν έχει παράθυρο.|Кухня большая, но ванная маленькая и без окна.|The kitchen is large, but the bathroom is small and has no window.
"""},
 10: {
 "word": """
το ταξίδι|путешествие|the trip
οι διακοπές|каникулы / отпуск|the holidays
το αεροπλάνο|самолёт|the aeroplane
το αεροδρόμιο|аэропорт|the airport
το τρένο|поезд|the train
το πλοίο|корабль|the ship
το λιμάνι|порт|the port
το ξενοδοχείο|отель|the hotel
η βαλίτσα|чемодан|the suitcase
το διαβατήριο|паспорт|the passport
η κράτηση|бронь|the booking
η αναχώρηση|отправление|the departure
η άφιξη|прибытие|the arrival
ο τουρίστας|турист|the tourist
ο χάρτης|карта|the map
το νησί|остров|the island
η θάλασσα|море|the sea
η παραλία|пляж|the beach
ταξιδεύω|я путешествую|I travel
φεύγω|я ухожу / уезжаю|I leave
φτάνω|я прибываю|I arrive
μένω σε ξενοδοχείο|я останавливаюсь в отеле|I stay at a hotel
""",
 "phrase": """
Έχω κράτηση στο ξενοδοχείο.|У меня бронь в отеле.|I have a hotel booking.
Πού είναι το αεροδρόμιο;|Где аэропорт?|Where is the airport?
Το τρένο φεύγει το πρωί.|Поезд отправляется утром.|The train leaves in the morning.
Ταξιδεύω στην Ελλάδα.|Я путешествую по Греции.|I am travelling in Greece.
""",
 "sentence": """
Αύριο ταξιδεύω στην Αθήνα με το αεροπλάνο και μένω σε ξενοδοχείο.|Завтра я лечу в Афины и останавливаюсь в отеле.|Tomorrow I travel to Athens by plane and stay at a hotel.
Έχω το διαβατήριο και τη βαλίτσα μου, αλλά δεν βρίσκω το εισιτήριο.|У меня с собой паспорт и чемодан, но я не могу найти билет.|I have my passport and suitcase, but I cannot find my ticket.
"""},
 11: {
 "word": """
η ιστορία|история|the story
η ζωή|жизнь|life
τα παιδικά χρόνια|детство|childhood
γεννήθηκα|я родился / родилась|I was born
ήμουν|я был / была|I was
ήταν|он / она был(а)|he / she was
πήγα|я пошёл / поехал|I went
ήρθα|я пришёл / приехал|I came
έζησα|я жил / жила|I lived
έμαθα|я выучил / узнал|I learned
δούλεψα|я работал|I worked
σπούδασα|я учился / училась|I studied
τελείωσα|я закончил|I finished
αρχίζω|я начинаю|I start
τελειώνω|я заканчиваю|I finish
πριν|раньше / до|before
μετά|потом / после|after
πέρσι|в прошлом году|last year
τότε|тогда|then
όταν|когда|when
μικρός|маленький (м.р.)|young (masculine)
μεγάλωσα|я вырос|I grew up
""",
 "phrase": """
Γεννήθηκα στην Κύπρο.|Я родился на Кипре.|I was born in Cyprus.
Πέρσι πήγα στην Ελλάδα.|В прошлом году я ездил в Грецию.|Last year I went to Greece.
Πού έζησες μικρός;|Где ты жил в детстве?|Where did you live as a child?
Δούλεψα δύο χρόνια στην Αθήνα.|Я два года работал в Афинах.|I worked in Athens for two years.
""",
 "sentence": """
Γεννήθηκα στη Λευκωσία, αλλά έζησα πολλά χρόνια στην Αθήνα.|Я родился в Никосии, но много лет жил в Афинах.|I was born in Nicosia, but lived in Athens for many years.
Πέρσι πήγα στην Ελλάδα, έμαθα ελληνικά και γνώρισα νέους φίλους.|В прошлом году я ездил в Грецию, учил греческий и познакомился с новыми друзьями.|Last year I went to Greece, learned Greek and met new friends.
"""},
 12: {
 "word": """
θα|частица будущего времени|future-tense particle
θα πάω|я пойду / поеду|I will go
θα κάνω|я сделаю|I will do
θα έρθω|я приду|I will come
θα δω|я увижу|I will see
θα φάω|я поем|I will eat
θα πιω|я выпью|I will drink
θα μείνω|я останусь|I will stay
θα αγοράσω|я куплю|I will buy
θα δουλέψω|я буду работать|I will work
θα μιλήσω|я поговорю|I will speak
μπορώ|я могу|I can
πρέπει|нужно / должен|must / need to
ίσως|возможно|perhaps
μαζί|вместе|together
το σχέδιο|план|the plan
το ραντεβού|встреча / запись|the appointment
το Σαββατοκύριακο|выходные|the weekend
την άλλη εβδομάδα|на следующей неделе|next week
απόψε|сегодня вечером|tonight
""",
 "phrase": """
Τι θα κάνεις αύριο;|Что ты будешь делать завтра?|What will you do tomorrow?
Θα πάω στο σχολείο.|Я пойду в школу.|I will go to school.
Θα έρθεις μαζί μου;|Ты пойдёшь со мной?|Will you come with me?
Πρέπει να φύγω τώρα.|Мне нужно сейчас уходить.|I must leave now.
""",
 "sentence": """
Αύριο θα πάω στην αγορά, θα αγοράσω ψωμί και θα δω έναν φίλο μου.|Завтра я пойду на рынок, куплю хлеб и увижусь с другом.|Tomorrow I will go to the market, buy bread and see a friend.
Το Σαββατοκύριακο θα μείνουμε στο σπίτι και θα μιλήσουμε με την οικογένεια.|На выходных мы останемся дома и поговорим с семьёй.|At the weekend we will stay home and talk with the family.
"""},
 13: {
 "word": """
η βόλτα|прогулка|a walk
η παρέα|компания друзей|a group of friends
ο κινηματογράφος|кинотеатр|the cinema
η ταινία|фильм|the film
η μουσική|музыка|music
η συναυλία|концерт|the concert
το θέατρο|театр|the theatre
το μουσείο|музей|the museum
το πάρκο|парк|the park
η ταβέρνα|таверна|the taverna
το εστιατόριο|ресторан|the restaurant
η καφετέρια|кафе|the café
η βόλτα στην πόλη|прогулка по городу|a walk around town
βγαίνω|я выхожу|I go out
περπατάω|я гуляю / иду пешком|I walk
συναντάω|я встречаю|I meet
μου αρέσει|мне нравится|I like
προτιμώ|я предпочитаю|I prefer
χορεύω|я танцую|I dance
τραγουδάω|я пою|I sing
ακούω|я слушаю|I listen
""",
 "phrase": """
Πάμε βόλτα το βράδυ;|Погуляем вечером?|Shall we go for a walk this evening?
Μου αρέσει η μουσική.|Мне нравится музыка.|I like music.
Θέλεις να πάμε σινεμά;|Хочешь пойти в кино?|Do you want to go to the cinema?
Προτιμώ να μείνω στο σπίτι.|Я предпочитаю остаться дома.|I prefer to stay at home.
""",
 "sentence": """
Το Σάββατο συναντάω φίλους, πίνουμε καφέ και μετά πάμε στον κινηματογράφο.|В субботу я встречаюсь с друзьями, мы пьём кофе, а потом идём в кино.|On Saturday I meet friends, we have coffee and then go to the cinema.
Μου αρέσει να περπατάω στο πάρκο, αλλά η φίλη μου προτιμάει το μουσείο.|Мне нравится гулять в парке, но подруга предпочитает музей.|I like walking in the park, but my friend prefers the museum.
"""},
 14: {
 "word": """
η εργασία|работа / труд|work
το γραφείο|офис|the office
ο συνάδελφος|коллега|the colleague
ο διευθυντής|директор / менеджер|the manager
η συνάντηση|встреча / совещание|the meeting
το πρόγραμμα|расписание / программа|the schedule
ο υπολογιστής|компьютер|the computer
το μήνυμα|сообщение|the message
το ηλεκτρονικό ταχυδρομείο|электронная почта|email
ο μισθός|зарплата|the salary
η ώρα|час / время|the hour / time
το διάλειμμα|перерыв|the break
η εταιρεία|компания|the company
ο πελάτης|клиент|the customer
τηλεφωνώ|я звоню|I call
γράφω|я пишу|I write
στέλνω|я отправляю|I send
απαντάω|я отвечаю|I answer
αργά|поздно|late
νωρίς|рано|early
κουρασμένος|уставший|tired
""",
 "phrase": """
Δουλεύω σε ένα γραφείο.|Я работаю в офисе.|I work in an office.
Έχω συνάντηση το πρωί.|У меня утром совещание.|I have a meeting in the morning.
Θα σου στείλω μήνυμα.|Я пришлю тебе сообщение.|I will send you a message.
Τι ώρα τελειώνεις τη δουλειά;|Во сколько ты заканчиваешь работу?|What time do you finish work?
""",
 "sentence": """
Δουλεύω σε μια εταιρεία, γράφω μηνύματα και μιλάω με τους πελάτες.|Я работаю в компании, пишу сообщения и разговариваю с клиентами.|I work at a company, write messages and speak with customers.
Ο συνάδελφός μου έχει συνάντηση το πρωί και εγώ δουλεύω στον υπολογιστή.|У моего коллеги утром совещание, а я работаю за компьютером.|My colleague has a meeting in the morning and I work on the computer.
"""},
 15: {
 "word": """
ο γιατρός|врач|the doctor
το νοσοκομείο|больница|the hospital
το φαρμακείο|аптека|the pharmacy
το φάρμακο|лекарство|the medicine
η υγεία|здоровье|health
ο πόνος|боль|pain
ο πονοκέφαλος|головная боль|a headache
ο πυρετός|температура / жар|a fever
ο βήχας|кашель|a cough
το κρυολόγημα|простуда|a cold
το κεφάλι|голова|the head
το χέρι|рука|the hand / arm
το πόδι|нога|the leg / foot
η κοιλιά|живот|the stomach / belly
ο λαιμός|горло / шея|the throat / neck
πονάω|у меня болит|I am in pain
νιώθω|я чувствую|I feel
άρρωστος|больной|ill / sick
καλύτερα|лучше|better
χειρότερα|хуже|worse
ξεκουράζομαι|я отдыхаю|I rest
""",
 "phrase": """
Δεν νιώθω καλά.|Я плохо себя чувствую.|I do not feel well.
Έχω πονοκέφαλο και πυρετό.|У меня болит голова и температура.|I have a headache and a fever.
Πού είναι το φαρμακείο;|Где аптека?|Where is the pharmacy?
Πρέπει να πάω στον γιατρό.|Мне нужно пойти к врачу.|I need to see a doctor.
""",
 "sentence": """
Σήμερα δεν νιώθω καλά, έχω πυρετό και θέλω να πάω στον γιατρό.|Сегодня я плохо себя чувствую, у меня температура и я хочу к врачу.|Today I do not feel well, I have a fever and want to see a doctor.
Ο αδελφός μου έχει πονοκέφαλο, αγοράζει φάρμακο και μένει στο σπίτι.|У моего брата болит голова, он покупает лекарство и остаётся дома.|My brother has a headache, buys medicine and stays at home.
"""},
 16: {
 "word": """
η ουρά|очередь|the queue
παρακαλώ|пожалуйста|please
περιμένω|я жду|I wait
το έγγραφο|документ|the document
η αίτηση|заявление|the application
η ταυτότητα|удостоверение личности|the identity card
το διαβατήριο|паспорт|the passport
η υπηρεσία|служба / учреждение|the service / office
το ταχυδρομείο|почта|the post office
η τράπεζα|банк|the bank
ο υπάλληλος|служащий|the clerk
το γραφείο πληροφοριών|справочное бюро|the information desk
η σειρά|очередь / порядок|the turn / order
ο αριθμός προτεραιότητας|номер очереди|the queue number
η υπογραφή|подпись|the signature
το έντυπο|бланк|the form
υπογράφω|я подписываю|I sign
συμπληρώνω|я заполняю|I fill in
χρειάζομαι|мне нужно|I need
φέρνω|я приношу|I bring
δίνω|я даю|I give
παίρνω|я беру / получаю|I take / receive
""",
 "phrase": """
Περιμένετε στην ουρά, παρακαλώ.|Подождите в очереди, пожалуйста.|Please wait in the queue.
Χρειάζομαι ένα έντυπο.|Мне нужен бланк.|I need a form.
Πού πρέπει να υπογράψω;|Где мне нужно подписать?|Where should I sign?
Έχετε το διαβατήριό σας;|У вас с собой паспорт?|Do you have your passport?
""",
 "sentence": """
Πηγαίνω στην τράπεζα, παίρνω αριθμό προτεραιότητας και περιμένω στην ουρά.|Я иду в банк, беру номерок и жду в очереди.|I go to the bank, take a queue ticket and wait in line.
Ο υπάλληλος χρειάζεται το διαβατήριό μου και μου δίνει ένα έντυπο.|Служащему нужен мой паспорт, и он даёт мне бланк.|The clerk needs my passport and gives me a form.
"""}
}
def build_extra():
    items=[]
    for unit,groups in RAW.items():
        for kind,raw in groups.items():
            for ix,line in enumerate(raw.strip().splitlines(),1):
                gr,ru,en=(x.strip() for x in line.split("|"))
                items.append(dict(id=f"x{unit:02d}{kind[0]}{ix:03d}",unit=unit,kind=kind,
                                  chapter=unit,topic=next(a[3] for a in CHAPTERS if a[0]==unit),
                                  gr=gr,ru=ru,en=en,source="original"))
    return items

