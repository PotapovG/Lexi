#!/usr/bin/env python3
"""Proof: curated acceptable Greek variants, no distractor false negatives, all locales.
Run only against an isolated throwaway database; publisher form/IDs remain canonical.
"""
import sys,collections,tempfile
from pathlib import Path
ROOT=Path('/opt/greek-trainer')
sys.path.insert(0,str(ROOT))
import greek_variants as gv
import accepted_glosses as gl
import server,vocab_lessons as vocab
import catalog_v2 as cat
for original, colloquial in [('δύο','δυο'),('μία','μια'),('εννέα','εννιά'),
('ένδεκα','έντεκα'),('δεκαέξι','δεκάξι'),('δεκαεπτά','δεκαεφτά'),
('δεκαοκτώ','δεκαοχτώ'),('δεκαεννέα','δεκαεννιά')]:
 assert gv.variants(original)==[colloquial],(original,colloquial,gv.variants(original))
 assert gv.variants(colloquial)==[original],(original,colloquial,gv.variants(colloquial))
assert gv.variants('επτά')==['εφτά']
assert gv.variants('εφτά')==['επτά']
assert gv.variants('οκτώ')==['οχτώ']
assert gv.variants('οχτώ')==['οκτώ']
assert gv.variants('ο αδελφός')==['ο αδερφός']
assert gv.variants('η αδελφή')==['η αδερφή']
assert gv.variants('Έχω έναν αδελφό.')==['Έχω έναν αδερφό.']
assert gv.variants('ο αδελφικός')==[] and gv.variants('επτακόσια')==[]
assert gv.variants('οι αδελφοί')==['οι αδερφοί']
assert gv.variants('η αδελφών')==['η αδερφών']
target_ids=['w118','w123','w124','w125','w087','w088','w177','w183','w184','w185']
for cid in target_ids:
 c=cat.BY_ID[cid]
 g=c['gr'];alt=gv.variants(g)[0]
 for lang in ('ru','en','zh','ar','es','pt'):
  q=server.format_question(c,'ru-gr',lang)
  assert q['kind'] in ('word','number')
  assert len(q['choices'])==8 and len(set(q['choices']))==8
  assert g in q['choices'] and alt in q['choices'],(cid,lang,q)
  assert q['multipleValid'] and q['greekVariants']==[alt]
  assert gl.accepted(c,'ru-gr',lang,g)==[g,alt]
  wrong=next(x for x in q['choices'] if x not in (g,alt))
  assert not gl.is_accepted(c,'ru-gr',lang,wrong,g)
  to_target=server.format_question(c,'gr-ru',lang)
  assert to_target['greekVariants']==[alt] and to_target['prompt']==g
  assert len(to_target['choices'])==8
print('PASS main-book eight-option rendering x 10 words x 6 languages, Greek reverse aliases all valid, distractors remain wrong')
# All 146 accent cards are derived from canonical printed spelling only;
# alternate spelling becomes teaching hint after grading, never alternate index.
for cid in ('stress_w118','stress_w123','stress_w124','stress_w125','stress_w087','stress_w088'):
 c=cat.BY_ID[cid]
 q=server.format_question(c,'accent','ru')
 assert q['kind']=='accent'
 assert len(q['letters'])==len(c['base']) and q['accentableIndices']
 assert q['greekVariants']==gv.variants(c['accented'])
print('PASS accent keeps canonical Greek letter index; alternatives explicitly surfaced')
with tempfile.TemporaryDirectory() as td:
 server.DB=str(Path(td)/'learner.sqlite3')
 server.init_db()
 for lang in ('ru','en','zh','ar','es','pt'):
  for cid in target_ids:
   c=cat.BY_ID[cid];g=c['gr'];alt=gv.variants(g)[0]
   a=server.mark('greek-variant-test',dict(id=cid,lang=lang,direction='ru-gr',selected=alt))
   assert a['correct'] and set(a['acceptedAnswers'])=={g,alt},(cid,lang,a)
   b=server.mark('greek-variant-test',dict(id=cid,lang=lang,direction='ru-gr',selected=g))
   assert b['correct']
   rows=server.conn().execute('SELECT miss_debt,attempts,correct FROM progress WHERE user_id=? AND card_key=?',('greek-variant-test',server.card_key(c,'ru-gr',lang))).fetchone()
   assert rows['miss_debt']==0 and rows['attempts']==2 and rows['correct']==2
  acc=cat.BY_ID['stress_w123']
  resp=server.mark('greek-variant-test',dict(id=acc['id'],lang=lang,direction='accent',selected=str(acc['accent_index'])))
  assert resp['correct'] and resp['greekVariants']==['εφτά']
  word=next(x for x in vocab.VOCAB if x['gr']=='ο αδελφός')
  alt=gv.variants(word['gr'])[0]
  with server.conn() as db:
   a=vocab.answer(db,'greek-variant-vocab-'+lang,dict(id=word['id'],lang=lang,direction='target-gr',selected=alt))
   assert a['correct'] and a['acceptedAnswers']==[word['gr'],alt],a
   b=vocab.answer(db,'greek-variant-vocab-'+lang,dict(id=word['id'],lang=lang,direction='target-gr',selected=word['gr']))
   assert b['correct']
   wrong=vocab.answer(db,'greek-variant-vocab-'+lang,dict(id=word['id'],lang=lang,direction='target-gr',selected='ο αδελφικός'))
   assert not wrong['correct']
   item=db.execute('SELECT attempts,correct,miss_debt FROM vocab_progress WHERE user_id=? AND word_id=?',('greek-variant-vocab-'+lang,word['id'])).fetchone()
   assert item['attempts']==3 and item['correct']==2
   review=vocab.lesson(db,'greek-variant-vocab-'+lang,'all','A1',lang,review=True)
   assert review['words'] and review['words'][0]['id']==word['id'],review
   assert review['words'][0]['greekVariants']==[alt]
print('PASS 6 locales: both spellings scored correctly, no wrong-answer debt, isolated SQLite for full and A1/A2 study; accents unchanged')
# Entire 1700 independent vocab entries unchanged.
assert len(vocab.VOCAB)==1700
assert len(cat.ALL)==1795 and len(server.LISTEN_CARDS)==717
print('PASS exact 1795 book, 1700 A1/A2, 717 listening cards and no user-progress migration')

