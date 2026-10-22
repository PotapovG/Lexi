from pathlib import Path
p=Path('server.py');s=p.read_text()
def once(a,b):
 global s
 assert s.count(a)==1,(a[:90],s.count(a))
 s=s.replace(a,b)
once('import accent_guidance\n','import accent_guidance\nimport learning_engine\n')
once('        vocab.schema(db)\n','        vocab.schema(db)\n        learning_engine.schema(db)\n')
once('def make_global_weak_quiz(user_id,params,display_lang,count,exclude):',
'''def make_srs_due_quiz(user_id,params,display_lang,count,exclude):
    """Opt-in scheduled answer-direction review; never serves another account's data."""
    with conn() as db:
        rows=learning_engine.due_entries(db,user_id)
        questions=[]
        for row in rows:
            key=row['card_key']
            if key in exclude:continue
            bits=key.split(':')
            if len(bits) not in (2,3):continue
            cid,direction=bits[:2]
            card=book_or_audio_card(cid)
            if card is None and cid.startswith('personal_'):
                wid=cid[len('personal_'):]
                if wid in vocab.VOCAB_BY_ID and personalized.is_learned(db,user_id,wid):
                    card=personalized.to_card(vocab.VOCAB_BY_ID[wid])
            if not card or card['kind']=='listening' and not LISTENING_ENABLED:continue
            lang=bits[2] if len(bits)==3 else (
                display_lang if card['kind'] in ('accent','dialogue','article','order') else 'ru')
            if lang not in ('ru','en','zh','ar','es','pt'):continue
            if card_key(card,direction,lang)!=key:continue
            try:
                shape(card,direction,lang)
                questions.append(format_question(card,direction,lang,weak=True,
                    variant_index=row['attempts']%2 if card['kind']=='listening' else None))
            except (ValueError,IndexError,KeyError,TypeError):continue
            if len(questions)>=count:break
    return dict(questions=questions,available=len(rows),count=len(questions),
                mode='srs_due',pagePrecision='approximate',lang=display_lang)


def make_global_weak_quiz(user_id,params,display_lang,count,exclude):''')
once('    if mode=="weak_all":\n        return make_global_weak_quiz(user_id,params,lang,count,exclude)',
'''    if mode=="weak_all":
        return make_global_weak_quiz(user_id,params,lang,count,exclude)
    if mode=="srs_due":
        return make_srs_due_quiz(user_id,params,lang,count,exclude)''')
once('    if mode!="weak":\n        unique=[]',
'''    if mode!="weak" and params.get("adaptive",["0"])[0]=="1":
        with conn() as db:learning_engine.adaptive_order(db,user_id,choices)
    if mode!="weak":
        unique=[]''')
once('    need=math.ceil(duration*60/20)\n    return dict(uniqueCards=available,requiredAt20Seconds=need,durationMinutes=duration,\n                estimatedMinutesAt20Seconds=round(available/3,1),\n                enoughAt20Seconds=available>=need,approximate=True)',
'''    with conn() as db:pace,observations=learning_engine.pace_seconds(db,user_id)
    need=math.ceil(duration*60/pace)
    return dict(uniqueCards=available,requiredAt20Seconds=need,durationMinutes=duration,
                estimatedMinutesAt20Seconds=round(available*pace/60,1),
                enoughAt20Seconds=available>=need,approximate=True,
                paceSeconds=pace,personalizedPace=observations>=12,paceObservations=observations)''')
once('        db.execute("""INSERT INTO attempts(user_id,card_key,kind,unit,correct,created_at)\n                      VALUES(?,?,?,?,?,?)""",(user_id,key,card["kind"],card["unit"],int(correct),now))',
'''        db.execute("""INSERT INTO attempts(user_id,card_key,kind,unit,correct,created_at)
                      VALUES(?,?,?,?,?,?)""",(user_id,key,card["kind"],card["unit"],int(correct),now))
        srs_info=(learning_engine.update(db,user_id,key,correct,now)
                  if body.get('srsOptIn') is True else None)''')
once('    result=dict(correct=correct,answer=correct_answer,missDebt=miss_debt)',
'''    result=dict(correct=correct,answer=correct_answer,missDebt=miss_debt)
    if srs_info:result.update(srs_info)
    if not correct:
        result['explanation']=learning_engine.explanation(card,direction,lang,correct_answer)''')
once('    valid,total_weak=valid_weak_entries(user_id)\n    actionable=',
'''    valid,total_weak=valid_weak_entries(user_id)
    with conn() as db:srs_status=learning_engine.status(db,user_id)
    actionable=''')
once('        "weakOverall":total_weak,"weakUnavailable":archive_count,',
     '        "weakOverall":total_weak,"weakUnavailable":archive_count,"srs":srs_status,')
once('        "categories":categories,"units":units,',
     '        "categories":categories,"units":units,"mastery":learning_engine.mastery(rows,book_or_audio_card),')
once('"/api/personalized/status") and not account:', '"/api/personalized/status","/api/srs/status") and not account:')
once('        if path=="/api/personalized/status":',
'''        if path=="/api/srs/status":
            with conn() as db:result=learning_engine.status(db,uid)
            return self.send_json(200,result,new,token)
        if path=="/api/personalized/status":''')
p.write_text(s)
print('SERVER_PATCHED',len(s))
