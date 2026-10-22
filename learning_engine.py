"""Opt-in spaced review, conservative learning feedback, and analytics for Λέξη.

No external models, no changes to permanent card identities, and no implicit
migration of historical mistakes into due schedules. Times are UTC ISO 8601.
"""
import datetime as dt
import math
import statistics

LANGS=('ru','en','zh','ar','es','pt')
UTC=dt.timezone.utc

def schema(db):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS srs_schedule (
      user_id TEXT NOT NULL,
      card_key TEXT NOT NULL,
      interval_days INTEGER NOT NULL DEFAULT 0,
      success_streak INTEGER NOT NULL DEFAULT 0,
      due_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      PRIMARY KEY(user_id, card_key)
    );
    CREATE INDEX IF NOT EXISTS ix_srs_user_due ON srs_schedule(user_id,due_at);
    """)

def update(db,user_id,key,correct,now):
    """Apply bounded expanding intervals only after explicit opt-in answers."""
    previous=db.execute("SELECT success_streak FROM srs_schedule WHERE user_id=? AND card_key=?",
                        (user_id,key)).fetchone()
    streak=(int(previous['success_streak'])+1 if previous and correct else (1 if correct else 0))
    intervals=(0,1,3,7,14,30,60,120,180)
    days=intervals[min(streak,8)]
    moment=dt.datetime.fromisoformat(now)
    due=moment+(dt.timedelta(days=days) if correct else dt.timedelta(minutes=10))
    due_iso=due.isoformat(timespec="seconds")
    db.execute("""INSERT INTO srs_schedule(user_id,card_key,interval_days,success_streak,due_at,updated_at)
                  VALUES(?,?,?,?,?,?)
                  ON CONFLICT(user_id,card_key) DO UPDATE SET
                    interval_days=excluded.interval_days,
                    success_streak=excluded.success_streak,
                    due_at=excluded.due_at,updated_at=excluded.updated_at""",
               (user_id,key,days,streak,due_iso,now))
    return dict(nextReview=due_iso,srsIntervalDays=days)

def status(db,user_id,now=None):
    now=now or dt.datetime.now(UTC).isoformat(timespec="seconds")
    row=db.execute("""SELECT COUNT(*) AS total,
                       SUM(CASE WHEN due_at<=? THEN 1 ELSE 0 END) AS due
                      FROM srs_schedule WHERE user_id=?""",(now,user_id)).fetchone()
    return dict(scheduled=row["total"],due=row["due"] or 0,optInOnly=True)

def due_entries(db,user_id,now=None,limit=500):
    now=now or dt.datetime.now(UTC).isoformat(timespec="seconds")
    return db.execute("""SELECT s.card_key AS card_key,COALESCE(p.attempts,0) AS attempts
          FROM srs_schedule s LEFT JOIN progress p ON p.user_id=s.user_id AND p.card_key=s.card_key
          WHERE s.user_id=? AND s.due_at<=?
          ORDER BY s.due_at ASC LIMIT ?""",(user_id,now,limit)).fetchall()

def pace_seconds(db,user_id):
    """Robust observed pace from nearby answers. Long breaks are ignored."""
    rows=db.execute("SELECT created_at FROM attempts WHERE user_id=? ORDER BY id DESC LIMIT 110",
                    (user_id,)).fetchall()
    times=[dt.datetime.fromisoformat(r["created_at"]) for r in rows]
    intervals=[(a-b).total_seconds() for a,b in zip(times,times[1:])]
    valid=[s for s in intervals if 3<=s<=90]
    return (int(max(8,min(60,statistics.median(valid)))),len(valid)) if len(valid)>=12 else (20,0)

def stage(kind):
    if kind in ('word','letter','number','accent','syllable'):return 0
    if kind in ('plural','verb','article'):return 1
    if kind in ('phrase','listening'):return 2
    return 3

def adaptive_order(db,user_id,choices):
    """Within already user-filtered cards only. Never widen chapter/grammar scope."""
    recents=db.execute("SELECT correct FROM attempts WHERE user_id=? ORDER BY id DESC LIMIT 40",
                       (user_id,)).fetchall()
    n=len(recents)
    acc=sum(row["correct"] for row in recents)/n if n else 0
    target=(0 if n<12 or acc<0.64 else 1 if n<24 or acc<0.76 else 2 if n<35 or acc<0.86 else 3)
    # Deterministic coarse band of ability, not a formal CEFR assessment.
    import random
    choices.sort(key=lambda entry:(abs(stage(entry[0]["kind"])-target),-entry[2],random.random()))
    return target

TEMPLATES={
 'ru':{
  'article':'Проверь род и падеж: в этом пропуске требуется форма «{correct}».',
  'verb':'Для лица «{person}» здесь используется форма «{correct}». Сравни окончания в таблице спряжения.',
  'accent':'Ударение меняет написание слова. Верный вариант: «{correct}».',
  'plural':'Сравни единственное и множественное число и окончание: «{correct}».',
  'order':'Собери заданную модель предложения: «{correct}». Другой естественный порядок слов здесь пока не проверяется.',
  'dialogue':'Здесь по контексту диалога ожидается реплика: «{correct}».',
  'default':'Правильное значение для этой карточки: «{correct}». Сравни его с исходным греческим текстом.'
 },
 'en':{
  'article':'Check gender and case: this blank requires “{correct}”.',
  'verb':'For “{person}”, the form is “{correct}”. Compare the endings in the verb table.',
  'accent':'The accent matters in spelling. Correct form: “{correct}”.',
  'plural':'Compare singular/plural endings: “{correct}”.',
  'order':'Rebuild the model sentence: “{correct}”. Other natural word orders are not graded yet.',
  'dialogue':'The dialogue context calls for: “{correct}”.',
  'default':'The accepted meaning here is “{correct}”. Compare it with the Greek source.'
 },
 'zh':{
  'article':'请检查性别和格：这里需要“{correct}”。',
  'verb':'主语“{person}”对应的动词形式是“{correct}”。请比较变位表中的词尾。',
  'accent':'重音符号影响拼写。正确形式：“{correct}”。',
  'plural':'请比较单复数词尾：“{correct}”。',
  'order':'请还原本题指定的句子：“{correct}”。其他自然语序暂不评分。',
  'dialogue':'根据对话语境，应填：“{correct}”。',
  'default':'本题对应的正确含义是“{correct}”。请与希腊语原文比较。'
 },
 'ar':{
  'article':'تحقّق من الجنس والحالة الإعرابية: المطلوب هنا «{correct}».',
  'verb':'مع «{person}» الصيغة الصحيحة هي «{correct}». قارن نهايات الفعل في الجدول.',
  'accent':'علامة النبر مهمة في الكتابة. الصواب «{correct}».',
  'plural':'قارن نهايات المفرد والجمع: «{correct}».',
  'order':'رتّب الجملة وفق النموذج «{correct}». لا تُقيَّم الترتيبات الصحيحة الأخرى بعد.',
  'dialogue':'بحسب سياق الحوار، الجواب المطلوب هو «{correct}».',
  'default':'المعنى المقبول هنا هو «{correct}». قارنه بالنص اليوناني.'
 },
 'es':{
  'article':'Comprueba género y caso: aquí se necesita «{correct}».',
  'verb':'Para «{person}» corresponde «{correct}». Compara las terminaciones en la tabla.',
  'accent':'La tilde importa en la escritura. Forma correcta: «{correct}».',
  'plural':'Compara las terminaciones de singular y plural: «{correct}».',
  'order':'Reconstruye la frase modelo: «{correct}». Otros órdenes naturales aún no se evalúan.',
  'dialogue':'Por el contexto del diálogo se espera «{correct}».',
  'default':'El significado aceptado es «{correct}». Compáralo con el texto griego.'
 },
 'pt':{
  'article':'Confere o género e o caso: a forma necessária é «{correct}».',
  'verb':'Para «{person}», usa-se «{correct}». Compara as terminações na tabela.',
  'accent':'O acento é importante na escrita. Forma correta: «{correct}».',
  'plural':'Compara as terminações do singular e plural: «{correct}».',
  'order':'Reconstrói a frase modelo: «{correct}». Outras ordens naturais ainda não são avaliadas.',
  'dialogue':'Pelo contexto do diálogo, espera-se «{correct}».',
  'default':'O significado aceite aqui é «{correct}». Compara-o com o grego original.'
 }
}
def explanation(card,direction,lang,correct_answer):
    kind=card['kind']
    bucket=kind if kind in ('article','verb','accent','plural','order','dialogue') else 'default'
    return TEMPLATES[lang][bucket].format(correct=correct_answer,person=card.get('personName',''))

def mastery(rows,lookup):
    """Approximate textbook chapter heatmap from attempted card IDs."""
    counts={i:[0,0] for i in range(1,21)}
    for r in rows:
        card=lookup(r['card_key'].split(':',1)[0])
        unit=card.get('chapter',0) if card else 0
        if unit in counts:
            counts[unit][0]+=1
            counts[unit][1]+=int(r['correct'])
    result=[]
    for chapter,(attempts,correct) in counts.items():
        accuracy=round(100*correct/attempts) if attempts else None
        status=('unseen' if attempts==0 else 'early' if attempts<8 else
                'review' if accuracy<65 else 'developing' if accuracy<85 else 'strong')
        result.append(dict(chapter=chapter,attempts=attempts,correct=correct,
                           accuracy=accuracy,status=status,provisional=attempts<8))
    return result

# Item-level evidence: only direct exercise forms are labelled as grammar
# practice. Broad themed chapter flags are *not* skill mastery evidence.
DIRECT_SKILLS={
 'article':'article_case','verb':'conjugation','accent':'stress',
 'plural':'noun_number','order':'word_order','syllable':'stress_syllables','enclitic':'enclitic_stress','grammar':'grammar_morphology','dialogue':'dialogue_context',
 'listening':'listening'
}
PATTERN_SKILLS={
 'aorist_narrative':'aorist_examples',
 'future_tense':'future_examples',
 'subjunctive_na':'subjunctive_examples',
 'medical_conditional':'conditional_examples',
}

def detailed_mastery(rows,lookup):
    """Aggregate user attempts without altering stored historical IDs.
    
    Page bins are approximate pedagogical anchors, NOT actual confirmed source
    matches. Pattern tags measure practice in context, not grammar competence.
    """
    from collections import defaultdict
    pages=defaultdict(lambda:[0,0])
    skills=defaultdict(lambda:[0,0])
    for attempt in rows:
        cid=attempt['card_key'].split(':',1)[0]
        card=lookup(cid)
        if not card:continue
        correct=int(attempt['correct'])
        page=card.get('page')
        if card.get('curriculum') not in ('personalized','topic','verb') and isinstance(page,int) and 1<=page<=312:
            pages[page][0]+=1
            pages[page][1]+=correct
        direct=DIRECT_SKILLS.get(card['kind'])
        if direct:
            skills[direct][0]+=1
            skills[direct][1]+=correct
        if card['kind'] in ('phrase','sentence','dialogue'):
            for tag in set(card.get('grammar_tags',[])):
                if tag in PATTERN_SKILLS:
                    skill=PATTERN_SKILLS[tag]
                    skills[skill][0]+=1
                    skills[skill][1]+=correct
    result_pages=[
      dict(page=page,attempts=a,correct=c,accuracy=round(c*100/a),approximate=True,provisional=a<5)
      for page,(a,c) in sorted(pages.items())
    ]
    result_skills=[
      dict(skill=key,attempts=a,correct=c,accuracy=round(c*100/a),
           provisional=a<8,contextual=key.endswith('_examples'))
      for key,(a,c) in sorted(skills.items())
    ]
    return dict(pages=result_pages,skills=result_skills,pagePrecision='approximate')

_REASON={
 'ru':('Ты выбрал «{selected}», но здесь требуется «{correct}». Сверь лицо и окончание глагола.',
       'Ты выбрал «{selected}», а по роду, падежу и контексту нужна форма «{correct}».'),
 'en':('You selected “{selected}”; this person requires “{correct}”. Check the verb ending.',
       'You chose “{selected}”; gender, case and context require “{correct}”.'),
 'zh':('你选了“{selected}”，但这里对应的人称要求“{correct}”。请比较动词词尾。',
       '你选了“{selected}”，但此处性、格及语境要求“{correct}”。'),
 'ar':('اخترت «{selected}»، لكن المطلوب لهذا الضمير «{correct}». قارن نهاية الفعل.',
       'اخترت «{selected}»، لكن الجنس والحالة والسياق تتطلب «{correct}».'),
 'es':('Elegiste «{selected}»; esta persona requiere «{correct}». Compara la terminación.',
       'Elegiste «{selected}»; el género, el caso y el contexto requieren «{correct}».'),
 'pt':('Escolheste «{selected}»; esta pessoa exige «{correct}». Confere a terminação.',
       'Escolheste «{selected}»; o género, o caso e o contexto exigem «{correct}».')
}
def mistake_explanation(card,direction,lang,correct,selected):
    """Use only deterministic relationships, never infer an arbitrary diagnosis."""
    if card['kind']=='verb' and direction=='conjugate' and selected in card.get('forms',()):
        return _REASON[lang][0].format(selected=selected,correct=correct)
    if card['kind']=='article' and selected in card.get('options',()):
        return _REASON[lang][1].format(selected=selected,correct=correct)
    return explanation(card,direction,lang,correct)
