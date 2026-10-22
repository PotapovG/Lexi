#!/usr/bin/env python3
"""Three learning upgrades: isolated user-scoped statistics, timing and feedback."""
import datetime as dt
from pathlib import Path
import sqlite3,tempfile,collections
import server,learning_upgrade as u
locales=('ru','en','zh','ar','es','pt')
assert len(server.ALL)==1795 and len(server.LISTEN_CARDS)==717

# No inference of proficiency from one repeated word; unique IDs needed.
word=next(c for c in server.ALL if c['kind']=='word' and c.get('topics'))
article=next(c for c in server.ALL if c['kind']=='article' and len(c['acceptedForms'])>1)
verb=next(c for c in server.ALL if c['kind']=='verb' and len(set(c['forms']))==6)
accent=next(c for c in server.ALL if c['kind']=='accent' and len(c['base'])>1)
plural=next(c for c in server.ALL if c['kind']=='plural')
dialogue=next(c for c in server.ALL if c['kind']=='dialogue')
order=next(c for c in server.ALL if c['kind']=='order')
synthetic=[dict(card_key=word['id']+':gr-ru',correct=1) for _ in range(16)]
topic=u.knowledge_breakdown(synthetic,server.book_or_audio_card)
assert topic['topics'] and topic['topics'][0]['attempts']==16
assert topic['topics'][0]['uniqueTargets']==1
assert topic['topics'][0]['provisional'] # 16 answers do not prove knowledge of a whole topic
assert not topic['grammar']
direct=[dict(card_key=article['id']+':fill',correct=1) for _ in range(12)]
gram=u.knowledge_breakdown(direct,server.book_or_audio_card)
assert not gram['topics']
assert gram['grammar'] and all(x['provisional'] and x['uniqueTargets']==1 for x in gram['grammar'])
assert all(0<=x['accuracy']<=100 for x in topic['topics']+gram['grammar'])
assert u.knowledge_breakdown([],server.book_or_audio_card)['topics']==[]

# Specific wrong-vs-right comparisons in each locale; no LLM guesses.
for lang in locales:
    wrong_article=next(x for x in article['options'] if x not in article['acceptedForms'])
    message=u.selected_explanation(article,'fill',lang,article['correct'],wrong_article)
    assert wrong_article in message and article['correct'] in message and message.count('{')==0
    other=verb['forms'][(verb['person']+1)%6]
    explanation=u.selected_explanation(verb,'conjugate',lang,verb['forms'][verb['person']],other)
    assert verb['personName'] in explanation and other in explanation
    bad_pos=next(x for x in range(len(accent['base'])) if x!=accent['accent_index'])
    message=u.selected_explanation(accent,'accent',lang,accent['accented'],str(bad_pos))
    assert accent['accented'] in message
    for c,d,right,wrong in ((plural,'sg-pl',plural['pl'],'wrong plural'),
                             (dialogue,'gap0',dialogue['gaps'][0],'wrong reply'),
                             (order,'arrange',order['gr'],'WRONG '+order['gr'])):
        explanation=u.selected_explanation(c,d,lang,right,wrong)
        assert ('WRONG' if c['kind']=='order' else wrong) in explanation and right in explanation
    assert 'BAD' in u.selected_explanation(word,'ru-gr',lang,word['gr'],'BAD')

with tempfile.TemporaryDirectory(prefix='greek-learning-upgrade-') as tmp:
    prior=server.DB
    try:
        server.DB=str(Path(tmp)/'progress.sqlite3')
        server.init_db()
        epoch=dt.datetime(2026,10,20,9,0,tzinfo=dt.timezone.utc)
        with server.conn() as db:
            for i in range(80):
                # Natural mixed-type answer stream. No pause >= 150 sec counted.
                if i<20:card=word;seconds=17
                elif i<40:card=article;seconds=24
                elif i<60:card=verb;seconds=31
                else:card=dialogue;seconds=37
                epoch+=dt.timedelta(seconds=seconds)
                db.execute('INSERT INTO attempts(user_id,card_key,kind,unit,correct,created_at) VALUES(?,?,?,?,?,?)',
                      ('learner-A',card['id']+':'+('fill' if card['kind']=='article' else 'conjugate' if card['kind']=='verb' else 'gap0' if card['kind']=='dialogue' else 'gr-ru'),
                      card['kind'],card['unit'],1 if i%4 else 0,epoch.isoformat(timespec='seconds')))
            db.execute('INSERT INTO attempts(user_id,card_key,kind,unit,correct,created_at) VALUES(?,?,?,?,?,?)',
                      ('learner-B',word['id']+':gr-ru','word',word['unit'],1,epoch.isoformat(timespec='seconds')))
            db.commit()
            before=db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]
            modeled=u.capacity_projection(db,'learner-A',[word,article,verb,dialogue,order],30)
            new_user=u.capacity_projection(db,'new-account',[word,article,verb,dialogue,order],30)
            assert modeled['paceModel']=='observed' and modeled['measuredAnswerIntervals']>=12
            assert new_user['paceModel']=='fallback'
            assert modeled['taskAware'] and modeled['estimatedMinutes']>0
            assert modeled['requiredUniqueAtEstimatedPace']>0
            assert 0<new_user['estimatedMinutes'] and new_user['expectedRangeMinutes'][0]<new_user['expectedRangeMinutes'][1]
            assert db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]==before
        cap=server.estimate_capacity('learner-A',{'scope':['verbs'],'maxUnit':['4'],'duration':['30']})
        assert cap['paceModel']=='observed' and cap['taskAware']
        assert cap['estimatedMinutes']>0 and cap['uniqueCards']==42
        assert cap['requiredAt20Seconds']==__import__('math').ceil(30*60/cap['paceSeconds']) # legacy behavior
        other=server.estimate_capacity('learner-B',{'scope':['verbs'],'maxUnit':['4'],'duration':['30']})
        assert other['paceModel']=='fallback'  # no timing leakage between accounts
        st=server.stats('learner-A')
        assert st['details']['topics'] and st['details']['grammar']
        assert st['details']['confidenceRule']=='at_least_8_answers_and_3_distinct_targets'
        assert st['details']['grammarOnlyDirectExercises']
        st_other=server.stats('learner-B')
        assert st_other['attempts']==1 and st_other['details']['grammar']==[]
        with server.conn() as db:
            assert db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]==80+1
            assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
    finally:
        server.DB=prior
print('PASS LEARNING_UPGRADE six locale chosen-vs-correct diagnostics, '
      'topic/grammar evidence confidence, multi-step task-aware pace, '
      'user-scoped historical timing, 1795 source cards and 717 listening preserved')
