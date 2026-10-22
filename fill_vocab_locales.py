"""Build complete, ID-stable locale glossary candidates for Lexi A1/A2.

Public machine translator is used as a candidate source only. The script never
touches the user's database, auth data or historical card IDs. Incremental
local JSON candidate outputs are resumable. Run QA and review before deploy.
"""
from __future__ import annotations
import collections
import json
import random
import re
import sys
import time
from pathlib import Path
import requests
import vocab_lessons as vocab

ROOT=Path(__file__).parent
DEST=ROOT/'vocab_translations_1700.json'
LANGUAGES={'ar':'ar','zh':'zh-CN','es':'es','pt':'pt-PT'}
ALL=vocab.VOCAB
OVERRIDES={
'ar':{
  'please or you are welcome':'من فضلك / على الرحب والسعة',
  'please / you\'re welcome':'من فضلك / على الرحب والسعة',
  'I':'أنا','you (singular)':'أنت','he or this':'هو / هذا','she or this':'هي / هذه',
  'he / this (masculine)':'هو / هذا','she / this (feminine)':'هي / هذه',
  'it / this (neuter)':'هو / هذا (لغير العاقل)',
  'a (masculine)':'واحد / أداة نكرة للمذكر',
  'a (feminine)':'واحدة / أداة نكرة للمؤنث',
  'and':'و','or':'أو','but':'لكن',
  'the (masculine)':'الـ (مذكر)','the (feminine)':'الـ (مؤنث)',
  'the (neuter)':'الـ (محايد)',
  'Greek language':'اللغة اليونانية',
},
'zh':{
  'please / you\'re welcome':'请 / 不客气',
  'the (masculine)':'定冠词（阳性）','the (feminine)':'定冠词（阴性）',
  'the (neuter)':'定冠词（中性）',
  'one or a (masculine)':'一 / 阳性不定冠词',
  'one or a (feminine)':'一 / 阴性不定冠词',
  'one or a (neuter)':'一 / 中性不定冠词',
},
'es':{'please / you\'re welcome':'por favor / de nada'},
'pt':{'please / you\'re welcome':'por favor / de nada'}
}
HEADERS={'User-Agent':'Mozilla/5.0 (compatible; LexiCurriculumTranslator/1.0)'}
URL='https://translate.googleapis.com/translate_a/single'

def call(text,lang):
    for tries in range(5):
        try:
            response=requests.get(URL,params={'client':'gtx','sl':'en','tl':LANGUAGES[lang],
                      'dt':'t','q':text},headers=HEADERS,timeout=24)
            response.raise_for_status()
            result=''.join(x[0] or '' for x in response.json()[0])
            if not result.strip():raise ValueError('blank translation')
            return result
        except (ValueError,requests.RequestException) as e:
            if tries==4:raise
            time.sleep(0.6*(tries+1))
    raise RuntimeError('translation failed')

def translate(english_list,lang):
    # The translation API preserves LF segments for most short lexical glosses.
    # Recursive fallback for collapsed lines prevents any gloss/ID misalignment.
    if not english_list:return []
    if len(english_list)==1:return [call(english_list[0],lang).strip()]
    source='\n'.join(english_list)
    result=call(source,lang)
    rows=result.split('\n')
    if len(rows)==len(english_list) and all(x.strip() for x in rows):
        return [x.strip() for x in rows]
    midpoint=len(english_list)//2
    return translate(english_list[:midpoint],lang)+translate(english_list[midpoint:],lang)

def run(lang):
    if lang not in LANGUAGES:raise ValueError(lang)
    atlas=json.loads(DEST.read_text('utf-8')) if DEST.exists() else {k:{} for k in LANGUAGES}
    for k in LANGUAGES:atlas.setdefault(k,{})
    existing=atlas[lang]
    wanted=[w for w in ALL if not existing.get(w['id'])]
    count_before=len(wanted)
    print(lang,'remaining',count_before,'out of',len(ALL),flush=True)
    # Work with semantic English word keys to avoid needless repeated calls.
    pending=collections.defaultdict(list)
    for w in wanted:
        if w.get(lang):
            existing[w['id']]=w[lang]
            continue
        en=w['en']
        if en in OVERRIDES[lang]:
            existing[w['id']]=OVERRIDES[lang][en]
        else:pending[en].append(w['id'])
    unique=list(pending)
    print(lang,'missing after existing/overrides',sum(map(len,pending.values())),
          'unique glossary terms',len(unique),flush=True)
    for offset in range(0,len(unique),30):
        batch=unique[offset:offset+30]
        translated=translate(batch,lang)
        assert len(translated)==len(batch)
        for en,answer in zip(batch,translated):
            for word_id in pending[en]:existing[word_id]=answer
        if offset%150==0 or offset+30>=len(unique):
            DEST.write_text(json.dumps(atlas,ensure_ascii=False,indent=1),encoding='utf-8')
            print(lang,'translated',min(offset+30,len(unique)),'/',len(unique),flush=True)
        time.sleep(0.12)
    assert len(existing)==len(ALL),(lang,len(existing),len(ALL))
    DEST.write_text(json.dumps(atlas,ensure_ascii=False,indent=1),encoding='utf-8')
    print('COMPLETE',lang,len(existing),flush=True)

if __name__=='__main__':
    for language in sys.argv[1:] or LANGUAGES:
        run(language)
