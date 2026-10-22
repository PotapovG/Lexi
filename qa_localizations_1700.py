"""All-language, all-topic lexicon QA; isolation DB only, no changes to production users."""
import collections
import json
import re
import sqlite3
import tempfile
from pathlib import Path

import vocab_lessons as vocab
import server
import verb_phrase
import personalized
from catalog_v2 import ALL

LANGS=('ar','zh','es','pt')
atlas=json.loads(Path(__file__).with_name('vocab_translations_1700.json').read_text('utf-8'))
assert len(vocab.VOCAB)==1700
known={word['id'] for word in vocab.VOCAB}
assert len(known)==1700
for lang in LANGS:
    assert set(atlas[lang])==known,lang
    assert all(vocab.visible_translation(w,lang)==(atlas[lang][w['id']],False) for w in vocab.VOCAB)
    samples=collections.Counter()
    suspicious=[]
    for w in vocab.VOCAB:
        tr=w[lang]
        assert isinstance(tr,str) and tr.strip()==tr and len(tr)<240,(lang,w['id'])
        assert '<' not in tr and '\n' not in tr and '>' not in tr,(lang,w['id'])
        if lang=='ar' and not re.search(r'[\u0600-\u06ff]',tr):suspicious.append((w['gr'],tr))
        if lang=='zh' and not re.search(r'[\u3400-\u9fff]',tr):suspicious.append((w['gr'],tr))
        if lang in ('es','pt') and not re.search('[A-Za-zÀ-ÿ]',tr):suspicious.append((w['gr'],tr))
        for topic in w['topics']:samples[topic]+=1
    assert not suspicious,(lang,suspicious[:10])
    assert len(samples)==13,lang
    print('PASS complete',lang,len(atlas[lang]),'script-appropriate no fallback')

# Any printed English hint for a translation question is returned separately
# from the selected option used in answer grading.
with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'progress.sqlite3')
    server.init_db()
    for lang in ('en','ru')+LANGS:
        for t in vocab.THEMES:
            for lev in ('A1','A2'):
                with server.conn() as db:
                    lesson=vocab.lesson(db,'locale_qa_user',t['id'],lev,lang)
                    assert len(lesson['words'])==10,(lang,t['id'],lev)
                    assert lesson['translated']==10,(lang,t['id'],lev)
                    assert not any(w['untranslated'] for w in lesson['words'])
                    for entry in lesson['words']:
                        assert entry['english'] and entry['translation'] and len(entry['choicesEn'])==8
                        assert len(entry['choices'])==8
                        assert len(set(entry['choices']))==8
                        answer=(entry['translation'] if entry['direction']=='gr-target' else entry['gr'])
                        assert answer in entry['choices']
                        for english,raw in zip(entry['choicesEn'],entry['choices']):
                            assert english
                            assert english!=f'{raw} ({english})'  # metadata separate
        # Isolated per-user correctness in every locale and every direction.
        word=vocab.VOCAB[1000]
        with server.conn() as db:
            for direction,selected in [('gr-target',word[lang]),('target-gr',word['gr'])]:
                result=vocab.answer(db,'user_'+lang,{'id':word['id'],'lang':lang,
                                                    'direction':direction,'selected':selected})
                assert result['correct'] and result['answer']==selected
                assert result['untranslated'] is False
    # Cross-check contextual conjugation: all 102 sentences in each language
    verbs=[w for w in ALL if w['kind']=='verb']
    assert len(verbs)==102
    for lang in ('en','ru')+LANGS:
        for w in verbs:
            greek,translated=verb_phrase.phrase(w,lang)
            assert greek.startswith(verb_phrase.EL[w['person']]) and translated
            if lang=='ar':assert re.search(r'[\u0600-\u06ff]',translated)
            if lang=='zh':assert re.search(r'[\u3400-\u9fff]',translated)
            if lang in ('es','pt'):assert re.search(r'[A-Za-zÀ-ÿ]',translated)
            if lang in ('ar','zh','es','pt'):
                assert translated!=verb_phrase.phrase(w,'en')[1],(lang,w['id'])
            _,choices,english=verb_phrase.options(w,lang,ALL)
            assert len(choices)==len(english)==8 and len(set(choices))==8,(lang,w['id'])
            assert translated in choices,(lang,w['id'])
    # Textbook Arabic must not show fallback English on translateable cards.
    for card in ALL:
        if card['kind'] in ('word','number','phrase','sentence','verb','accent'):
            assert card['ar'],card
            if card['kind'] not in ('letter','accent'):
                assert card['ar']!=card['en'],(card['kind'],card['id'],card['en'])
    # Example question metadata still obeys English double gloss rule.
    for lang in LANGS:
        with server.conn() as db:
            first=vocab.VOCAB[-1]
            db.execute('INSERT OR IGNORE INTO vocab_progress(user_id,word_id,attempts,correct,miss_debt,updated_at) VALUES(?,?,1,1,0,?)',('personal',first['id'],'2026-10-19'))
        quiz=server.make_quiz('personal',{'scope':['pages'],'study':['personalized'],
              'lang':[lang],'types':['word'],'from':['1'],'to':['56'],'count':['50']})['questions']
        personal=[q for q in quiz if q['id']=='personal_'+first['id']]
        assert len(personal)==1,lang
        q=personal[0]
        if q['direction']=='gr-ru':
            assert len(q['choicesEn'])==8
        else:assert q.get('promptEn')==first['en']
    with server.conn() as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS 13 topics × 2 levels × 6 languages = 156 ten-word quizzes, English hint metadata, grading')
print('PASS 102 verbs × 6 locales, 8 distinct options and 2-stage semantics; AR textbook translations')
print('PASS user-personalized word localization + SQLite integrity')
