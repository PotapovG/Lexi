"""Greek offline listening collection: only vetted Pocket TTS audio, NEVER Piper.

Original self-authored textbook units supply question and translation data.
A media manifest generated once offline provides two distinct Pocket preset
speakers for each distinct Greek sentence/word, in teacher-approved styles.
No online synthesis, microphone, speech recognition or charged API.
"""
from pathlib import Path
import json,re,hashlib

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'pocket-listening'
DIR=DATA/'wav'
MANIFEST=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
APPROVED=('athina','eleni','katerina','kostas','spyros','nikos')
ELIGIBLE_IDS=frozenset(json.loads((DATA/'source.json').read_text(encoding='utf-8'))['eligibleSourceIds'])
assert MANIFEST['engine']=='myned-ai/pocket-tts-greek'
assert tuple(MANIFEST['approvedVoices'])==APPROVED
LABELS={
 'ru':('Что ты услышал?','Прослушай запись и выбери правильный перевод.'),
 'en':('What did you hear?','Play the recording and choose the correct meaning.'),
 'zh':('你听到了什么？','听录音并选择正确的含义。'),
 'ar':('ماذا سمعت؟','استمع إلى التسجيل واختر المعنى الصحيح.'),
 'es':('¿Qué has escuchado?','Escucha el audio y elige la traducción correcta.'),
 'pt':('O que ouviste?','Ouve a gravação e escolhe a tradução correta.')
}
AUDIO={}
CARDS=[]
BY_TEXT={}
DIFFICULTY={'word':1,'phrase':2,'sentence':3}
VOICE_LABELS={'athina':'Афина','eleni':'Елени','katerina':'Катерина',
              'kostas':'Костас','spyros':'Спирос','nikos':'Никос'}

def key(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()[:32]

def build(book_cards):
    by_id={c['id']:c for c in book_cards}
    for sourceid,source in by_id.items():
        if sourceid not in ELIGIBLE_IDS or source.get('kind') not in DIFFICULTY:
            continue
        text=source.get('gr','').strip()
        if not text:continue
        payload=MANIFEST['entries'].get(key(text))
        if not payload or payload.get('text')!=text:continue
        variants=payload.get('variants',{})
        ready=[]
        for style in ('clear','lively'):
            entry=variants.get(style)
            if not entry:continue
            fn=entry.get('file','');voice=entry.get('voice','')
            if not re.fullmatch(r'[a-f0-9]{32}\.wav',fn) or voice not in APPROVED:continue
            path=DIR/fn
            if not path.is_file():continue
            AUDIO[fn]=path
            ready.append(dict(file=fn,voice=voice,style=style))
        # Do not issue an exercise where both alternate voices aren't ready.
        if len(ready)!=2 or ready[0]['voice']==ready[1]['voice']:continue
        card={k:source[k] for k in ('chapter','unit','page','gr','en','ru','zh','ar','es','pt','topic')}
        card.update(id='listen_'+sourceid,kind='listening',sourceKind=source['kind'],
                    sourceId=sourceid,audioVariants=ready,difficulty=DIFFICULTY[source['kind']],
                    curriculum='listening',semanticId='audio_'+source.get('semanticId',sourceid))
        CARDS.append(card)
        BY_TEXT[text]=ready
    assert len({x['id'] for x in CARDS})==len(CARDS)
    assert len(CARDS)<=len(ELIGIBLE_IDS)==717
    return CARDS

def has_audio(filename):return filename in AUDIO
