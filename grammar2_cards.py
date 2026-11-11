"""Authorial Modern Greek grammar cloze drills, isolated from textbook provenance.

Explicit grammar prompts require exactly one correct form and four curated
morphologically contrastive choices. These are NOT quotations/pages from the
paid textbook. Do not mutate original 1795-card ledger or student keys.
"""
import hashlib
import unicodedata
from catalog_v2 import CHAPTERS
import pedagogy_rules
RAW="case|4|Βλέπω ___ φίλο μου.|τον|ο|του|οι\ncase|4|Μιλάω με ___ φίλη μου.|τη|η|της|τον\ncase|4|Αυτό είναι το σπίτι ___ φίλου μου.|του|τον|ο|τους\ncase|4|Δίνω το βιβλίο ___ μητέρα μου.|στη|της|η|τον\ncase|4|Πού είναι ___ παιδιά;|τα|τους|των|το\ncase|4|Βλέπω ___ γυναίκες.|τις|οι|της|την\ncase|4|Το αυτοκίνητο ___ πατέρα μου.|του|τον|ο|των\ncase|4|Οι φίλοι ___ Άννας.|της|τη|την|οι\ncase|4|Η Μαρία βλέπει ___ δάσκαλο.|τον|του|ο|των\ncase|4|Το βιβλίο είναι ___ μαθητή.|του|τον|ο|τους\nagreement|9|Ο ___ φίλος είναι εδώ.|καλός|καλή|καλό|καλοί\nagreement|9|Η ___ μαθήτρια διαβάζει.|καλή|καλός|καλό|καλές\nagreement|9|Το ___ σπίτι είναι εκεί.|μικρό|μικρός|μικρή|μικροί\nagreement|9|Οι ___ φίλοι έρχονται.|καλοί|καλός|καλή|καλά\nagreement|9|Οι ___ φίλες μιλούν.|καλές|καλοί|καλό|καλή\nagreement|9|Τα ___ παιδιά παίζουν.|μικρά|μικρό|μικροί|μικρές\nagreement|9|Έχω μία ___ τσάντα.|μεγάλη|μεγάλο|μεγάλος|μεγάλοι\nagreement|9|Βλέπω τον ___ δάσκαλο.|καλό|καλός|καλή|καλά\nagreement|9|Μιλάμε με τη ___ φίλη.|μικρή|μικρό|μικρός|μικρές\nagreement|9|Οι ___ πόρτες είναι ανοιχτές.|μεγάλες|μεγάλοι|μεγάλη|μεγάλο\ncomparison|11|Αυτό το σπίτι είναι ___ από εκείνο.|μεγαλύτερο|μεγαλύτερος|μεγαλύτερη|μεγάλοι\ncomparison|11|Η Άννα είναι ___ από τη Μαρία.|ψηλότερη|ψηλότερος|ψηλότερο|ψηλοί\ncomparison|11|Ο Νίκος είναι ___ από τον Πέτρο.|μικρότερος|μικρότερη|μικρότερο|μικρές\ncomparison|11|Αυτό το αυτοκίνητο είναι ___ από το άλλο.|πιο γρήγορο|πιο γρήγορος|πιο γρήγορη|οι γρήγοροι\ncomparison|11|Το δωμάτιο είναι ___ από την κουζίνα.|μικρότερο|μικρότερη|μικρότερος|μικρές\ncomparison|11|Αυτή η τσάντα είναι ___ από εκείνη.|πιο ακριβή|πιο ακριβός|πιο ακριβό|οι ακριβοί\ncomparison|11|Ο αδελφός μου είναι ___ από εμένα.|μεγαλύτερος|μεγαλύτερη|μεγαλύτερο|μεγάλες\ncomparison|11|Αυτά τα παπούτσια είναι ___ από εκείνα.|πιο φτηνά|πιο φτηνός|πιο φτηνή|πιο φτηνό\ncomparison|11|Η πόλη είναι ___ από το χωριό.|μεγαλύτερη|μεγαλύτερος|μεγαλύτερο|μεγάλες\ncomparison|11|Το λεωφορείο είναι ___ από το ποδήλατο.|πιο αργό|πιο αργός|πιο αργή|πιο αργοί\npast|12|Αόριστος: Χθες εγώ ___ στο μουσείο.|πήγα|πηγαίνω|θα πάω|πηγαίνεις\npast|12|Αόριστος: Χθες εμείς ___ μια ταινία.|είδαμε|βλέπουμε|θα δούμε|βλέπετε\npast|12|Αόριστος: Το Σάββατο εγώ ___ στο σπίτι.|έμεινα|μένω|θα μείνω|μένεις\npast|12|Αόριστος: Προχθές η Μαρία ___ ένα βιβλίο.|αγόρασε|αγοράζει|θα αγοράσει|αγοράζω\npast|12|Αόριστος: Χθες οι φίλοι μου ___ στην Αθήνα.|ήρθαν|έρχονται|θα έρθουν|έρχεσαι\npast|12|Παρατατικός: Πέρσι εγώ ___ στην Κύπρο.|ήμουν|είμαι|θα είμαι|είσαι\npast|12|Αόριστος: Χθες το βράδυ εμείς ___ στην ταβέρνα.|φάγαμε|τρώμε|θα φάμε|τρώτε\npast|12|Αόριστος: Την Κυριακή ο Νίκος ___ νωρίς.|ξύπνησε|ξυπνάει|θα ξυπνήσει|ξυπνάω\npast|12|Αόριστος: Χθες η Άννα ___ ένα γράμμα.|έγραψε|γράφει|θα γράψει|γράφω\npast|12|Αόριστος: Χθες το πρωί εγώ ___ καφέ.|ήπια|πίνω|θα πιω|πίνεις\nfuture|14|Μέλλοντας: Εγώ ___ αύριο.|θα έρθω|ήρθα|έρχομαι|έρχεται\nfuture|14|Μέλλοντας: Εμείς ___ στο σπίτι.|θα μείνουμε|μένουμε|μείναμε|μένω\nfuture|14|Μέλλοντας: Η Μαρία ___ ένα βιβλίο.|θα αγοράσει|αγοράζει|αγόρασε|αγοράζουμε\nfuture|14|Μέλλοντας: Αυτοί ___ μια ταινία.|θα δουν|βλέπουν|είδαν|βλέπει\nfuture|14|Μέλλοντας: Εγώ ___ ελληνικά.|θα μιλήσω|μιλάω|μίλησα|μιλάς\nfuture|14|Μέλλοντας: Εσύ ___ το γράμμα.|θα γράψεις|γράφεις|έγραψες|γράφω\nfuture|14|Μέλλοντας: Εμείς ___ μαζί.|θα φάμε|τρώμε|φάγαμε|τρώτε\nfuture|14|Μέλλοντας: Εσείς ___ καφέ.|θα πιείτε|πίνετε|ήπιατε|πίνουμε\nsubjunctive|16|Θέλω ___ ελληνικά.|να μάθω|μαθαίνω|θα μαθαίνω|έμαθα\nsubjunctive|16|Μπορείς ___ εδώ;|να έρθεις|έρχεσαι|θα έρθεις|ήρθες\nsubjunctive|16|Πρέπει ___ τώρα.|να φύγουμε|φεύγουμε|θα φύγουμε|φύγαμε\nsubjunctive|16|Θέλω ___ νερό.|να πιω|πίνω|θα πίνω|ήπια\nsubjunctive|16|Προτιμάμε ___ στο σπίτι.|να μείνουμε|μένουμε|μείναμε|θα μένουμε\nsubjunctive|16|Πρέπει ___ με τον γιατρό.|να μιλήσω|μιλάω|θα μιλήσω|μίλησα\nsubjunctive|16|Μπορείτε ___ το βιβλίο;|να διαβάσετε|διαβάζετε|θα διαβάσετε|διαβάσατε\nsubjunctive|16|Θέλεις ___ μια ταινία;|να δεις|βλέπεις|είδες|θα δεις"
# Original issue #7: article-by-gender practice, authored independently.
# Append, never renumber the original grammar cards (IDs 001–056).
RAW += "\n" + "gender|3|___ σπίτι είναι στην πόλη.|Το|Ο|Η|Οι\ngender|3|___ φίλος μένει στο χωριό.|Ο|Η|Το|Οι\ngender|3|___ φίλη μένει στην πόλη.|Η|Ο|Το|Οι\ngender|3|___ κινητό είναι στο σπίτι.|Το|Ο|Η|Οι\ngender|3|___ μητέρα είναι δασκάλα.|Η|Ο|Το|Οι\ngender|3|___ πατέρας είναι οδηγός.|Ο|Η|Το|Οι\ngender|3|___ παιδί μένει στην Αθήνα.|Το|Ο|Η|Οι\ngender|3|___ ξάδελφος είναι μηχανικός.|Ο|Η|Το|Οι\ngender|3|___ ξαδέλφη είναι φοιτήτρια.|Η|Ο|Το|Οι\ngender|3|___ αγόρι είναι από την Κύπρο.|Το|Ο|Η|Οι\ngender|3|___ γιατρός είναι η αδελφή μου.|Η|Ο|Το|Οι\ngender|3|___ κόρη είναι φοιτήτρια.|Η|Ο|Το|Οι\ngender|4|___ Ελληνίδα μιλάει ελληνικά.|Η|Ο|Το|Οι\ngender|4|___ Έλληνας ξέρει αγγλικά.|Ο|Η|Το|Οι\ngender|4|___ μαθήτρια μιλάει γερμανικά.|Η|Ο|Το|Οι\ngender|4|___ μαθητής μιλάει ρωσικά.|Ο|Η|Το|Οι\ngender|8|___ μαρκαδόρος είναι στο τραπέζι.|Ο|Η|Το|Οι\ngender|8|___ σελίδα είναι στο βιβλίο.|Η|Ο|Το|Οι\ngender|8|___ βάζο είναι στο σπίτι.|Το|Ο|Η|Οι\ngender|8|___ αναπτήρας είναι στην τσάντα.|Ο|Η|Το|Οι"
FIRST={'case':4,'agreement':9,'comparison':11,'past':12,'future':14,'subjunctive':16}
MILESTONE={'case':'languages_b1_and_object_articles',
 'agreement':'clothing_adjective_agreement',
 'comparison':'home_comparatives','past':'aorist_narrative',
 'future':'future_tense','subjunctive':'subjunctive_na'}
LABEL={
'case':{'ru':'Выбери подходящий артикль или падежную форму.','en':'Choose the correct article or case form.','zh':'选择正确的冠词或格形式。','ar':'اختر أداة التعريف أو صيغة الحالة الصحيحة.','es':'Elige el artículo o la forma de caso correcta.','pt':'Escolhe o artigo ou a forma de caso correta.'},
'agreement':{'ru':'Согласуй прилагательное с существительным по роду, числу и падежу.','en':'Match the adjective to the noun in gender, number and case.','zh':'使形容词与名词的性、数和格一致。','ar':'طابق الصفة مع الاسم في الجنس والعدد والحالة.','es':'Concordancia del adjetivo: género, número y caso.','pt':'Concordância do adjetivo: género, número e caso.'},
'comparison':{'ru':'Выбери правильную сравнительную форму и согласование.','en':'Choose the correctly agreed comparative form.','zh':'选择正确的比较级及一致形式。','ar':'اختر صيغة المقارنة المطابقة.','es':'Elige el comparativo con la concordancia correcta.','pt':'Escolhe o comparativo com a concordância correta.'},
'past':{'ru':'Выбери форму прошедшего времени и подходящее лицо.','en':'Choose the requested past-tense form and person.','zh':'选择正确的过去时和人称形式。','ar':'اختر صيغة الماضي المناسبة للفاعل.','es':'Elige la forma del pasado y la persona correcta.','pt':'Escolhe a forma do passado e a pessoa correta.'},
'future':{'ru':'Используй будущее время с θα и нужное лицо.','en':'Use the future with θα and match the subject.','zh':'使用带 θα 的将来时，并与主语保持一致。','ar':'استخدم المستقبل مع θα وطابق الفاعل.','es':'Usa el futuro con θα y la persona correcta.','pt':'Usa o futuro com θα e a pessoa correta.'},
'subjunctive':{'ru':'После этой конструкции нужна форма с να, согласованная с субъектом.','en':'This construction needs να with the appropriate verb form.','zh':'这一结构需要 να 和适当的动词形式。','ar':'يتطلب التعبير να مع صيغة الفعل المناسبة.','es':'Esta construcción requiere να y la forma verbal correcta.','pt':'Esta construção exige να e a forma verbal correta.'}
}
FIRST['gender']=3
MILESTONE['gender']='family_profession_question'
LABEL['gender']={
 'ru':'Выбери артикль именительного падежа по роду существительного.',
 'en':'Choose the nominative article that matches the noun’s gender.',
 'zh':'根据名词的性选择主格冠词。',
 'ar':'اختر أداة التعريف في حالة الرفع وفق جنس الاسم.',
 'es':'Elige el artículo nominativo que corresponde al género del sustantivo.',
 'pt':'Escolhe o artigo do nominativo de acordo com o género do nome.'
}
CARDS=[]
for n,line in enumerate(RAW.splitlines(),1):
    parts=line.split('|')
    assert len(parts)==7,(n,line)
    group,ch,prompt,correct,*wrong=parts
    ch=int(ch)
    assert group in FIRST and ch>=FIRST[group],(n,group,ch)
    assert prompt.count('___')==1 and len(set([correct]+wrong))==4,(n,prompt)
    card={'id':f'g2261021_{n:03d}','kind':'grammar',
          'chapter':ch,'unit':ch,
          'page':next(c['start']+1 for c in CHAPTERS if c['id']==ch),
          'topic':f"Γραμματική · {group}",
          'source':'independent_grammar_cloze_20261021',
          'book_page_verified':False,
          'group':group,'gr':prompt,
          'prompt':prompt,'correct':correct,'options':[correct]+wrong,
          'grammar_tags':[MILESTONE[group]],
          **{lang:LABEL[group][lang] for lang in ('ru','en','zh','ar','es','pt')}}
    pedagogy_rules.tag(card)
    assert card['curriculum_ready_unit']<=ch,(n,card['curriculum_ready_unit'])
    CARDS.append(card)
# Preserve original 76 stable answer IDs; issue #8 adds only new cards in
# the already shipped grammar-fill mode, with no separate mode or navigation.
assert len(CARDS)==76,len(CARDS)
from possessive_cards import CARDS as POSSESSIVE_CARDS
CARDS.extend(POSSESSIVE_CARDS)
assert len(CARDS)==111,len(CARDS)
# Issue #9 extends the EXISTING grammar-fill practice with typed examples.
# The original 111 immutable IDs and all answers stay unchanged.
from verb_a_cards import CARDS as VERB_A_CARDS
CARDS.extend(VERB_A_CARDS)
assert len(CARDS)==147,len(CARDS)
# B1 extends the existing typed grammar_fill answers; retain all 147 IDs.
from verb_b1_cards import CARDS as VERB_B1_CARDS
CARDS.extend(VERB_B1_CARDS)
assert len(CARDS)==183,len(CARDS)
# Issue #11: existing grammar_fill typed question, NO new mode; old IDs intact.
from verb_b2_cards import CARDS as VERB_B2_CARDS
CARDS.extend(VERB_B2_CARDS)
assert len(CARDS)==223,len(CARDS)
# Issue #13 extends existing grammar_fill questions (choice + typed);
# immutable previous 223 IDs and learner progress are never renumbered.
from likes_dislikes_cards import CARDS as LIKES_CARDS
CARDS.extend(LIKES_CARDS)
assert len(CARDS)==259,len(CARDS)
assert len({x['id'] for x in CARDS})==len(CARDS)
BY_ID={c['id']:c for c in CARDS}
