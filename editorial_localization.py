"""Controlled professional-skill-inspired editorial atlas for textbook beginners.

Process: compare original Greek -> resolve instructional person/register ->
check natural target-language gloss -> independently review teaching intent ->
record old/new text and rationale -> run six-locale scoring regressions.

Source-workflow references (guidance, not imported executable code):
https://github.com/mcroitor/agent-skills-library/blob/main/documents/translator/SKILL.md
https://github.com/mcroitor/agent-skills-library/blob/main/education/educational-content-reviewer/SKILL.md
https://github.com/mcroitor/agent-skills-library/blob/main/education/course-localization-specialist/SKILL.md

Target Portuguese locale: European PT-PT, not Brazilian PT-BR.
The owner's Patakis PDF is private, used to understand Greek course topics.
No claim that the skill itself proves a translation is native certified.
"""

# (id, lang): (literal pre-edit value, reviewed replacement, editorial reason)
REVIEWED={
 ('w003','es'):('buenos dias','buenos días','Spanish stress mark: días'),
 ('w004','es'):('buenas noches','buenas tardes / buenas noches','Greek early-evening greeting; context-dependent Spanish'),
 ('w006','es'):('adios','adiós','Spanish stress mark: adiós'),
 ('w010','es'):('si','sí','affirmation sí, not conditional si'),
 ('w015','es'):('tú (plural/formal)','vosotros / ustedes (plural); usted (formal)','distinguish plural from singular politeness; tú is singular informal'),
 ('w022','es'):('donde / desde donde','dónde / de dónde','accented Spanish interrogatives; από πού = de dónde'),
 ('w023','es'):('quien (masculino)','quién (masculino en griego)','accent on Spanish question pronoun; gender is Greek, not Spanish'),
 ('w024','es'):('quien (femenino)','quién (femenino en griego)','accent on Spanish question pronoun; gender is Greek, not Spanish'),
 ('w025','es'):('cual (neutro)','cuál (neutro en griego)','accent on Spanish interrogative; grammatical neuter belongs to Greek'),
 ('p001','es'):('¿Cuál es tu nombre? (informal)','¿Cómo te llamas? (informal)','idiomatic Spanish informal second-person (tú)'),
 ('p002','es'):('¿Cómo te llamas? (formal)','¿Cómo se llama usted? (formal)','restore formal register from Greek σας'),
 ('p021','es'):('¿Qué haces para trabajar?','¿A qué te dedicas? (informal)','idiomatic job question preserving 2sg informal'),
 ('w014','pt'):('você (singular)','tu (singular, informal)','European Portuguese informal 2sg (not BR você)'),
 ('w015','pt'):('te (plural/formal)','vocês (plural) / o senhor, a senhora (formal)','te is an object clitic, not a subject or formal plural'),
 ('w031','pt'):('O meu nome é','Chamo-me','idiomatic European Portuguese naming'),
 ('w032','pt'):('O seu nome é','Chamas-te / o teu nome é','preserve Greek σε: informal 2sg tu, not formal seu'),
 ('p001','pt'):('Qual é o seu nome? (informal)','Como te chamas? (informal)','in PT-PT, te chamas is informal, seu points to formal third person'),
 ('p002','pt'):('Qual o seu nome? (formal)','Como se chama? (formal)','idiomatic formal second person in PT-PT'),
 ('p017','pt'):('Como está? / O que está a fazer? (informal)','Como estás? / O que estás a fazer? (informal)','preserve informal 2sg from κάνεις'),
 ('p021','pt'):('O que faz no trabalho?','Em que trabalhas? (informal)','preserve informal 2sg and question about profession'),
 ('p002','zh'):('你叫什么名字？ （正式）','您叫什么名字？（正式）','Greek σας is respectful; Chinese 您 marks politeness'),
 ('w093','ar'):('الزوج / الزوجة','الزوج (مذكر)','the masculine spouse card must not list wife'),
 ('w094','ar'):('الزوجة / الزوجة','الزوجة (مؤنث)','remove duplicated female spouse label'),
 ('w014','ar'):('أنت (المفرد)','أنتَ / أنتِ (مفرد)','Arabic gender on singular 2nd-person, Greek εσύ is gender-neutral'),
 ('w015','ar'):('أنت (بصيغة الجمع / رسمية)','أنتم / أنتنّ (جمع أو مخاطبة رسمية)','Arabic plural and Greek polite plural, not bare singular أنت'),
}
SOURCE_GREEK={
 'w003':'καλημέρα','w004':'καλησπέρα','w006':'αντίο','w010':'ναι',
 'w015':'εσείς','w022':'πού','w023':'ποιος','w024':'ποια','w025':'ποιο',
 'p001':'Πώς σε λένε;','p002':'Πώς σας λένε;','p021':'Τι δουλειά κάνεις;',
 'w014':'εσύ','w031':'με λένε','w032':'σε λένε','p017':'Τι κάνεις;',
 'w093':'ο σύζυγος','w094':'η σύζυγος'
}

def apply(cards,langs=("es","pt","zh")):
    by={c['id']:c for c in cards}
    changes=[]
    for (cid,lang),(old,new,rationale) in REVIEWED.items():
        if lang not in langs:continue
        card=by[cid]
        assert card['gr']==SOURCE_GREEK[cid],(cid,card['gr'])
        assert card[lang]==old,(cid,lang,'expected prior gloss',old,card[lang])
        assert new and old!=new and lang in ('ar','zh','es','pt')
        card[lang]=new
        changes.append(dict(card=cid,lang=lang,greek=card['gr'],before=old,after=new,why=rationale,
                            status='AI_editor_reviewed_not_native_verified'))
    assert len(changes)==sum(lang in langs for _,lang in REVIEWED)
    return changes
