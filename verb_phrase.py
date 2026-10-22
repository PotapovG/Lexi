"""Two-stage present-tense practice: inflection then contextual sentence translation."""
import random
import json
from pathlib import Path
_AR=json.loads(Path(__file__).with_name("verb_phrases_ar.json").read_text("utf-8"))
_LOCALIZED=json.loads(Path(__file__).with_name("verb_phrase_locales.json").read_text("utf-8"))

# Greek contextual complements and six Russian present-tense forms for each lemma.
# Native subject pronouns are supplied separately. Sentences are original teaching examples.
SPECS={
"γράφω":("ένα μήνυμα","сообщение","a message",["пишу","пишешь","пишет","пишем","пишете","пишут"],"write","writes"),
"μένω":("στη Λευκωσία","в Никосии","in Nicosia",["живу","живёшь","живёт","живём","живёте","живут"],"live","lives"),
"διαβάζω":("ένα βιβλίο","книгу","a book",["читаю","читаешь","читает","читаем","читаете","читают"],"read","reads"),
"δουλεύω":("στο γραφείο","в офисе","in the office",["работаю","работаешь","работает","работаем","работаете","работают"],"work","works"),
"αγοράζω":("ψωμί","хлеб","bread",["покупаю","покупаешь","покупает","покупаем","покупаете","покупают"],"buy","buys"),
"παίζω":("στο πάρκο","в парке","in the park",["играю","играешь","играет","играем","играете","играют"],"play","plays"),
"μαθαίνω":("ελληνικά","греческий язык","Greek",["учу","учишь","учит","учим","учите","учат"],"learn","learns"),
"μιλάω":("ελληνικά","по-гречески","Greek",["говорю","говоришь","говорит","говорим","говорите","говорят"],"speak","speaks"),
"ρωτάω":("τον δάσκαλο","учителя","the teacher",["спрашиваю","спрашиваешь","спрашивает","спрашиваем","спрашиваете","спрашивают"],"ask","asks"),
"αγαπάω":("τη μουσική","музыку","music",["люблю","любишь","любит","любим","любите","любят"],"love","loves"),
"περπατάω":("στην πόλη","по городу","in the city",["гуляю","гуляешь","гуляет","гуляем","гуляете","гуляют"],"walk","walks"),
"απαντάω":("στην ερώτηση","на вопрос","the question",["отвечаю","отвечаешь","отвечает","отвечаем","отвечаете","отвечают"],"answer","answers"),
"μπορώ":("να βοηθήσω","помочь","help",["могу","можешь","может","можем","можете","могут"],"can","can"),
"οδηγώ":("στην πόλη","по городу","in the city",["езжу за рулём","ездишь за рулём","ездит за рулём","ездим за рулём","ездите за рулём","ездят за рулём"],"drive","drives"),
"τηλεφωνώ":("στον φίλο μου","своему другу","my friend",["звоню","звонишь","звонит","звоним","звоните","звонят"],"call","calls"),
"θεωρώ":("ότι είναι καλό","что это хорошо","that it is good",["считаю","считаешь","считает","считаем","считаете","считают"],"think","thinks"),
"χρησιμοποιώ":("τον υπολογιστή","компьютер","the computer",["использую","используешь","использует","используем","используете","используют"],"use","uses")
}
RU=["Я","Ты","Он/она","Мы","Вы","Они"]
EN=["I","You","He/she","We","You","They"]
EL=["εγώ","εσύ","αυτός","εμείς","εσείς","αυτοί"]
def phrase(card,lang):
    gr,ru_obj,en_obj,ru_forms,en_base,en_third=SPECS[card["gr"]]
    person=card["person"]
    g=f"{EL[person]} {card['forms'][person]} {gr}"
    if card["gr"]=="μπορώ":
        ru=f"{RU[person]} {ru_forms[person]} {ru_obj}"
        en=f"{EN[person]} can {en_obj}"
    elif card["gr"]=="απαντάω":
        ru=f"{RU[person]} {ru_forms[person]} {ru_obj}"
        en=f"{EN[person]} {en_third if person==2 else en_base} {en_obj}"
    else:
        ru=f"{RU[person]} {ru_forms[person]} {ru_obj}"
        en=f"{EN[person]} {en_third if person==2 else en_base} {en_obj}"
    en=en[:1].upper()+en[1:]
    ru=ru[:1].upper()+ru[1:]
    # Person-specific contextual translations: 102 distinct Greek sentences
    # in each selected language, preserving second-person singular/plural.
    if lang=="ru":return g,ru
    if lang=="en":return g,en
    if lang=="ar":
        return g,_AR[card["gr"]][str(person)]
    if lang in ("zh","es","pt"):
        return g,_LOCALIZED[lang][card["gr"]+":"+str(person)]
    raise ValueError("unknown translation language")

def options(card,lang,cards):
    g,correct=phrase(card,lang)
    possible=[x for x in cards if x["kind"]=="verb" and x["id"]!=card["id"]]
    rand=random.Random(card["id"]+lang+"phrase")
    rand.shuffle(possible)
    pairs=[(correct,phrase(card,"en")[1])]
    for x in possible:
        value=phrase(x,lang)[1]
        if value not in [pair[0] for pair in pairs]:
            pairs.append((value,phrase(x,"en")[1]))
        if len(pairs)==8:break
    if len(pairs)!=8:raise ValueError("Not enough verb phrase alternatives")
    rand.shuffle(pairs)
    return g,[x[0] for x in pairs],[x[1] for x in pairs]
