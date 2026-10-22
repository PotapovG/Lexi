"""Second source-Greek-anchored professional-skill editorial batch, no fuzzy grading.

Translator, Educational Content Reviewer & Course Localization Specialist
review workflow: Greek source is authoritative; protect politeness, person,
grammatical gender, European PT-PT inflections, then style/diacritics.
Only exact and explained edits; owner PDF is not published.
"""
# source card id, target locale -> (previous exact gloss, corrected gloss, why)
REVISIONS = {
 ('p004','pt'):('De onde é? (informal)','De onde és? (informal)','είσαι is informal second-person singular; PT-PT és'),
 ('p005','es'):('¿De dónde eres? (formal)','¿De dónde es usted? (formal)','είστε is plural or polite, not tú/eres'),
 ('p005','zh'):('你从哪来？ （正式）','您从哪里来？（正式）','Greek είστε polite singular: Chinese 您'),
 ('p008','pt'):('Como vai?','Como estás?','Πώς είσαι is informal second-person singular'),
 ('p010','pt'):('E você?','E tu?','Κι εσύ informal; keep European Portuguese tu'),
 ('p011','pt'):('Onde mora? (informal)','Onde moras? (informal)','μένεις informal 2sg not mora 3sg'),
 ('p012','zh'):('你住在哪里？ （正式）','您住在哪里？（正式）','μένετε polite singular or plural, formal label requires 您'),
 ('p015','pt'):('Tem telefone?','Tens telefone?','έχεις second-person singular, PT-PT tens'),
 ('p016','es'):('¿Tienes un teléfono móvil? (formal)','¿Tiene usted teléfono móvil? (formal)','έχετε polite/plural, not informal tienes'),
 ('p016','pt'):('Tem um celular? (formal)','Tem telemóvel? (formal)','European Portuguese telemóvel (not Brazil celular)'),
 ('p016','zh'):('你有手机吗？ （正式）','您有手机吗？（正式）','έχετε polite singular: 您'),
 ('p018','es'):('¿Cómo estás? / ¿Qué estás haciendo? (formal)','¿Cómo está usted? / ¿Qué está haciendo? (formal)','κάνετε 2pl/polite; change tú -> usted'),
 ('p018','zh'):('你好吗？ / 你在干什么？ （正式）','您好吗？ / 您在做什么？（正式）','formal είστε/κάνετε register, 您'),
 ('p019','es'):('¿Cuál es su dirección?','¿Cuál es tu dirección?','σου indicates informal your (tú), not formal su'),
 ('p019','pt'):('Qual é o seu endereço?','Qual é a tua morada?','σου means informal tu; PT-PT morada is postal address'),
 ('p020','pt'):('Qual é o seu número de telefone?','Qual é o teu número de telefone?','σου informal possessive -> teu'),
 ('p020','zh'):('您的电话号码是多少？','你的电话号码是多少？','σου informal rather than formal'),
 ('p022','es'):('¿A qué se dedica en su trabajo?','¿A qué se dedica él/ella?','κάνει is third-person singular unspecified he/she, not question to usted'),
 ('p033','pt'):('Fala grego? (informal)','Falas grego? (informal)','μιλάς informal second-person'),
 ('p034','es'):('¿Hablas ruso? (formal)','¿Habla usted ruso? (formal)','μιλάτε plural/polite requires usted not hablas'),
 ('p034','zh'):('你会说俄语吗？ （正式）','您会说俄语吗？（正式）','μιλάτε formal polite'),
 ('p038','pt'):('Conhece o meu amigo?','Conheces o meu amigo?','ξέρεις informal second-person'),
 ('p041','pt'):('De que país é?','De que país és?','είσαι informal second-person'),
 ('p014','ar'):('هو / هي تعيش في أثينا.','هو يعيش في أثينا / هي تعيش في أثينا.','Greek μένει subject he or she, Arabic masculine and feminine verbs agree'),
 ('patk01_002','pt'):('É a Ana ou a Maria?','És a Ana ou a Maria?','εσύ είσαι informal singular'),
 ('patk02_003','es'):('Vivo en Nicosia, pero mi amigo vive en Paphos.','Vivo en Nicosia, pero mi amiga vive en Paphos.','η φίλη μου explicitly feminine friend'),
 ('patk02_003','ar'):('أعيش في نيقوسيا، لكن صديقي يعيش في بافوس.','أعيش في نيقوسيا، لكن صديقتي تعيش في بافوس.','η φίλη μου is female; Arabic friend and verb gender'),
 ('patk02_004','pt'):('Tem um telemóvel ou um telefone residencial?','Tens telemóvel ou telefone em casa?','έχεις informal tu, European Portuguese phrasing'),
 ('patk02_004','zh'):('您有手机或家庭电话吗？','你有手机或家用电话吗？','έχεις is informal, not polite 您'),
 ('patk03_004','es'):('¿María es estudiante o maestra?','¿María es estudiante universitaria o profesora?','φοιτήτρια university student, καθηγήτρια professor/teacher'),
 ('patk03_004','pt'):('A Maria é aluna ou professora?','A Maria é estudante universitária ou professora?','φοιτήτρια university student, not generic school pupil'),
 ('patk03_005','es'):('Mi amiga tiene dos hijos, un hijo y una hija.','Mi amigo tiene dos hijos, un hijo y una hija.','ο φίλος μου masculine friend'),
 ('patk04_002','pt'):('Conhece Maria? Sim, conheço-a.','Conheces a Maria? Sim, conheço-a.','ξέρεις informal 2sg tu'),
 ('patk04_004','es'):('¿Hablas alemán o inglés?','¿Habla usted alemán o inglés?','μιλάτε polite or plural; use usted'),
 ('patk04_004','zh'):('你说德语还是英语？','您会说德语还是英语？','μιλάτε formal/polite and natural Chinese'),
 ('patk04_006','pt'):('É italiano e fala italiano?','És italiano e falas italiano?','είσαι and μιλάς both informal 2sg'),
 ('patk04_006','zh'):('您是意大利人并且会说意大利语吗？','你是意大利人，也会说意大利语吗？','είσαι informal singular'),
}
GREEK = {
'p004':'Από πού είσαι;', 'p005':'Από πού είστε;', 'p008':'Πώς είσαι;',
'p010':'Κι εσύ;', 'p011':'Πού μένεις;', 'p012':'Πού μένετε;',
'p015':'Έχεις τηλέφωνο;', 'p016':'Έχετε κινητό;', 'p018':'Τι κάνετε;',
'p019':'Ποια είναι η διεύθυνσή σου;', 'p020':'Ποιο είναι το τηλέφωνό σου;',
'p022':'Τι δουλειά κάνει;', 'p033':'Μιλάς ελληνικά;', 'p034':'Μιλάτε ρωσικά;',
'p038':'Ξέρεις τον φίλο μου;', 'p041':'Από ποια χώρα είσαι;',
'p014':'Μένει στην Αθήνα.',
'patk01_002':'Εσύ είσαι η Άννα ή η Μαρία;',
'patk02_003':'Εγώ μένω στη Λευκωσία, αλλά η φίλη μου μένει στην Πάφο.',
'patk02_004':'Έχεις κινητό ή τηλέφωνο στο σπίτι;',
'patk03_004':'Η Μαρία είναι φοιτήτρια ή καθηγήτρια;',
'patk03_005':'Ο φίλος μου έχει δύο παιδιά, έναν γιο και μία κόρη.',
'patk04_002':'Ξέρεις τη Μαρία; Ναι, την ξέρω.',
'patk04_004':'Μιλάτε γερμανικά ή αγγλικά;',
'patk04_006':'Είσαι Ιταλός και μιλάς ιταλικά;',
}
def apply(cards,langs=('es','pt','zh')):
    by={c['id']:c for c in cards}
    log=[]
    for (cid,lang),(before,after,reason) in REVISIONS.items():
        if lang not in langs:continue
        card=by[cid]
        assert card['gr']==GREEK[cid],(cid,card['gr'])
        assert card[lang]==before,(cid,lang,'EXPECTED',before,'ACTUAL',card[lang])
        assert lang in ('es','pt','ar','zh') and before!=after and after
        card[lang]=after
        log.append(dict(id=cid,lang=lang,greek=card['gr'],before=before,after=after,reason=reason,
                        level='source_author_text_validated_ai_not_native_certified'))
    assert len(log)==sum(lang in langs for _,lang in REVISIONS)
    return log
