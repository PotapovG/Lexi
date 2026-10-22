"""Read-only learning insights for Lexi: practice evidence, pace, and deterministic feedback.

No schema changes, no LLM or publisher material, no relabelling past results.
"""
import collections
import datetime as dt
import math
import statistics

LOCALES=('ru','en','zh','ar','es','pt')
DIRECT={'article','verb','accent','plural','order','dialogue'}
DEFAULT_SECONDS={'word':19,'number':16,'letter':16,'accent':18,
 'plural':22,'article':20,'verb':25,'syllable':22,'dialogue':27,'phrase':27,
 'sentence':36,'order':34,'enclitic':22,'grammar':24,'listening':35}
# Grammar-tag evidence only from explicit form exercises. Other reading/
# conversational examples are not evidence of mastery of a grammar rule.
DIRECT_TAG_KINDS={'article','verb','accent','syllable','enclitic','grammar','plural','order'}
REGULAR_TEMPLATES={
'ru':{
 'article':'Ты выбрал «{selected}», но перед «{context}» нужна форма «{correct}». Сравни род, падеж и наличие предлога.',
 'verb':'Ты выбрал «{selected}» (форма для «{other}»), а задание про «{person}»: «{correct}». Сравни окончания.',
 'accent':'Ты отметил позицию {picked}, но в «{correct}» знак ударения стоит на позиции {target}. В греческом ударение пишется над гласной.',
 'plural':'Ты выбрал «{selected}», но здесь требуется «{correct}». Сравни число, артикль и окончание существительного.',
 'dialogue':'Реплика «{selected}» не подходит в этот пропуск. По контексту нужна «{correct}». Проверь обращение и смысл ответа.',
 'order':'Первое расхождение на слове №{position}: у тебя «{picked}», в заданной модели «{expected}». Полная модель: «{correct}». Другие допустимые порядки пока не оцениваются.',
 'default':'Ты выбрал «{selected}». Для этой греческой карточки ожидается «{correct}». Сравни различия значений.'
},
'en':{
 'article':'You chose “{selected}”; before “{context}” this needs “{correct}”. Check gender, case and preposition.',
 'verb':'You chose “{selected}” (form for “{other}”), but the subject is “{person}”: “{correct}”. Compare endings.',
 'accent':'You marked position {picked}, but in “{correct}” the accent belongs at position {target}. Written Greek accents sit over vowels.',
 'plural':'You chose “{selected}”, but the required form is “{correct}”. Compare number, article and noun ending.',
 'dialogue':'“{selected}” does not fit this gap. The context calls for “{correct}”. Check the question and reply.',
 'order':'The first mismatch is at word {position}: you put “{picked}”; the model has “{expected}”. Target: “{correct}”. Other valid orders are not graded.',
 'default':'You chose “{selected}”; this Greek item expects “{correct}”. Compare their meanings.'
},
'zh':{
 'article':'你选了“{selected}”，但在“{context}”前需要“{correct}”。请比较性、格和介词。',
 'verb':'你选了“{selected}”（对应“{other}”），但题目主语是“{person}”：应为“{correct}”。',
 'accent':'你标记了第 {picked} 个位置，正确单词“{correct}”的重音应在第 {target} 个位置。',
 'plural':'你选了“{selected}”，正确形式是“{correct}”。请比较单复数、冠词和词尾。',
 'dialogue':'“{selected}”不适合这个空格。根据上下文应答“{correct}”。',
 'order':'从第 {position} 个词开始不同：你放了“{picked}”，模型是“{expected}”。完整句：“{correct}”。目前不评判其他语序。',
 'default':'你选了“{selected}”，本题对应“{correct}”。请比较含义。'
},
'ar':{
 'article':'اخترت «{selected}»، لكن قبل «{context}» يلزم «{correct}». قارن الجنس والحالة وحرف الجر.',
 'verb':'اخترت «{selected}» (صيغة «{other}»)، لكن الفاعل هو «{person}»: «{correct}».',
 'accent':'اخترت الموضع {picked}، لكن علامة النبر في «{correct}» تقع في الموضع {target}.',
 'plural':'اخترت «{selected}»، لكن الصيغة المطلوبة «{correct}». قارن العدد والأداة والنهاية.',
 'dialogue':'«{selected}» لا يناسب هذا الفراغ. يتطلّب السياق «{correct}».',
 'order':'يبدأ الاختلاف في الكلمة رقم {position}: اخترت «{picked}» والنموذج «{expected}». الجملة: «{correct}». لا تُقيّم الترتيبات الأخرى بعد.',
 'default':'اخترت «{selected}»، لكن الإجابة هنا «{correct}». قارن المعنى.'
},
'es':{
 'article':'Elegiste «{selected}», pero antes de «{context}» se necesita «{correct}». Compara género, caso y preposición.',
 'verb':'Elegiste «{selected}» (forma de «{other}»), pero el sujeto es «{person}»: «{correct}».',
 'accent':'Marcaste la posición {picked}, pero en «{correct}» el acento va en la posición {target}.',
 'plural':'Elegiste «{selected}», pero se requiere «{correct}». Compara número, artículo y terminación.',
 'dialogue':'«{selected}» no encaja aquí. El contexto requiere «{correct}». Revisa la pregunta y la respuesta.',
 'order':'La primera diferencia está en la palabra {position}: pusiste «{picked}», el modelo dice «{expected}». Frase: «{correct}». Aún no se evalúan otros órdenes.',
 'default':'Elegiste «{selected}», pero esta tarjeta espera «{correct}». Compara los significados.'
},
'pt':{
 'article':'Escolheste «{selected}», mas antes de «{context}» é necessário «{correct}». Compara género, caso e preposição.',
 'verb':'Escolheste «{selected}» (forma de «{other}»), mas o sujeito é «{person}»: «{correct}».',
 'accent':'Assinalaste a posição {picked}, mas em «{correct}» o acento está na posição {target}.',
 'plural':'Escolheste «{selected}», mas a forma pedida é «{correct}». Compara número, artigo e terminação.',
 'dialogue':'«{selected}» não se ajusta a esta lacuna. Pelo contexto é «{correct}».',
 'order':'A primeira diferença está na palavra {position}: escolheste «{picked}», o modelo tem «{expected}». Frase: «{correct}». Outras ordens ainda não são avaliadas.',
 'default':'Escolheste «{selected}»; esta pergunta espera «{correct}». Compara os significados.'
}}
def selected_explanation(card,direction,lang,correct,selected):
    """Precise comparison when evidence is known; no invented linguistic reason."""
    labels=REGULAR_TEMPLATES.get(lang,REGULAR_TEMPLATES['en'])
    kind=card['kind']
    info={'selected':selected,'correct':correct,'context':'','person':'',
          'other':'','picked':'','target':'','position':'','expected':'','picked':''}
    if kind=='article' and selected in card['options']:
        info['context']=card['prompt'].split('___',1)[-1].lstrip().split()[0]
        return labels['article'].format(**info)
    if kind=='verb' and direction=='conjugate' and selected in card.get('forms',()):
        pos=card['forms'].index(selected)
        info['other']=('εγώ','εσύ','αυτός/αυτή','εμείς','εσείς','αυτοί/αυτές')[pos]
        info['person']=card['personName']
        return labels['verb'].format(**info)
    if kind=='accent' and selected.isdecimal():
        info['picked']=str(int(selected)+1);info['target']=str(card['accent_index']+1)
        return labels['accent'].format(**info)
    if kind=='plural':
        return labels['plural'].format(**info)
    if kind=='dialogue':
        return labels['dialogue'].format(**info)
    if kind=='order' and direction=='arrange':
        got=selected.split();expected=correct.split()
        first=next((i for i,(a,b) in enumerate(zip(got,expected)) if a!=b),
                   min(len(got),len(expected)))
        info['position']=first+1
        info['picked']=got[first] if first<len(got) else '∅'
        info['expected']=expected[first] if first<len(expected) else '∅'
        return labels['order'].format(**info)
    return labels['default'].format(**info)

def _summary(values):
    out=[]
    for key,item in values.items():
        count=item['count'];good=item['correct'];unique=len(item['unique'])
        confident=count>=8 and unique>=3
        accuracy=round(good/count*100)
        out.append(dict(id=key,attempts=count,correct=good,accuracy=accuracy,
              uniqueTargets=unique,provisional=not confident,
              status=('early' if not confident else 'review' if accuracy<65 else
                      'developing' if accuracy<85 else 'strong')))
    return sorted(out,key=lambda r:(r['provisional'],r['accuracy'],-r['attempts'],r['id']))

def knowledge_breakdown(rows,lookup):
    """Evidence groups. Historical attempts are read-only and account-scoped."""
    topics=collections.defaultdict(lambda:dict(count=0,correct=0,unique=set()))
    grammar=collections.defaultdict(lambda:dict(count=0,correct=0,unique=set()))
    for row in rows:
        cid=row['card_key'].split(':',1)[0]
        card=lookup(cid)
        if not card:continue
        ident=card.get('semanticId',cid)
        correct=int(row['correct'])
        if card['kind']=='word':
            for topic in set(card.get('topics',())):
                if topic:
                    item=topics[topic];item['count']+=1;item['correct']+=correct;item['unique'].add(ident)
        if card['kind'] in DIRECT_TAG_KINDS:
            for tag in set(card.get('grammar_tags',())):
                if tag:
                    item=grammar[tag];item['count']+=1;item['correct']+=correct;item['unique'].add(ident)
    return dict(topics=_summary(topics),grammar=_summary(grammar),
                confidenceRule='at_least_8_answers_and_3_distinct_targets',
                topicsOverlapPossible=True,grammarOnlyDirectExercises=True)

def _kind_profile(db,user_id):
    """Each gap / verb stage is a separate answer event; long pauses excluded."""
    rows=db.execute('SELECT kind,created_at FROM attempts WHERE user_id=? ORDER BY id DESC LIMIT 160',
                    (user_id,)).fetchall()
    groups=collections.defaultdict(list);overall=[]
    for now,prior in zip(rows,rows[1:]):
        try:seconds=(dt.datetime.fromisoformat(now['created_at'])-
                     dt.datetime.fromisoformat(prior['created_at'])).total_seconds()
        except (TypeError,ValueError):continue
        if 4<=seconds<=150:
            groups[now['kind']].append(seconds);overall.append(seconds)
    bykind={k:statistics.median(v) for k,v in groups.items() if len(v)>=6}
    return bykind,(statistics.median(overall) if len(overall)>=12 else None),len(overall)

def _card_seconds(card,bykind,overall):
    kind=card['kind']
    basic=DEFAULT_SECONDS.get(kind,25)
    if kind in bykind:
        step=max(8,min(75,bykind[kind]))
    elif overall is not None:
        step=max(8,min(75,basic*overall/22))
    else:step=basic
    steps=(2 if kind=='verb' else
           len(card.get('gaps',[])) if kind=='dialogue' else 1)
    return step*steps

def capacity_projection(db,user_id,pool,duration_minutes):
    """Selection-local expected supply at per-kind pace, not a time guarantee.

    No relation to stopwatch session duration; predicts enough unique
    teaching targets at observed vs fallback task complexity.
    """
    bykind,overall,observations=_kind_profile(db,user_id)
    unique={}
    for card in pool:
        identity=card.get('semanticId',card['id'])
        # Prefer the longer independent target if same semantic identity appears
        # in regular and supplemental review sections.
        s=_card_seconds(card,bykind,overall)
        if identity not in unique or s>unique[identity]:
            unique[identity]=s
    total=sum(unique.values());n=len(unique)
    avg=total/n if n else 20
    needed=math.ceil(duration_minutes*60/avg)
    return dict(estimatedMinutes=round(total/60,1),
       requiredUniqueAtEstimatedPace=needed,
       enoughAtEstimatedPace=n>=needed,
       averageSecondsPerUnique=round(avg,1),
       measuredAnswerIntervals=observations,
       paceModel=('observed' if overall is not None else 'fallback'),
       taskAware=True,
       expectedRangeMinutes=[round(total/60*0.7,1),round(total/60*1.4,1)])


def vocabulary_knowledge(db,user_id,vocab_lookup):
    """Separate A1/A2 lessons are stored in vocab_progress, not attempts.

    Report independently; never merge duplicate headwords across two
    learning modes or inflate textbook mastery with vocabulary review.
    """
    topics=collections.defaultdict(lambda:dict(count=0,correct=0,unique=set()))
    rows=db.execute('SELECT word_id,attempts,correct FROM vocab_progress WHERE user_id=?',(user_id,)).fetchall()
    for row in rows:
        word=vocab_lookup.get(row['word_id'])
        if not word or not row['attempts']:continue
        for topic in set(word.get('topics',())):
            if topic:
                item=topics[topic]
                item['count']+=row['attempts']
                item['correct']+=row['correct']
                item['unique'].add(word['id'])
    return _summary(topics)
