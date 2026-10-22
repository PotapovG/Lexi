"""Read-only resolver for student Greek pronunciation clips.

Only pre-rendered vetted Greek Pocket TTS WAV is served as recorded audio.
Older six-voice listening library is reused by exact Greek text.
Unavailable audio is explicitly indicated; no device TTS or speech synthesis.
"""
from pathlib import Path
import json, re, hashlib
import listening_catalog as listening

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'pocket-pronunciation'
WAV=OUT/'wav'
MANIFEST=OUT/'manifest.json'
PREFIX='/greek/pronunciation/'
_VALID=re.compile(r'[a-f0-9]{32}\.wav\Z')
def load():
    if not MANIFEST.is_file():return {}
    data=json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert data['engine']=='myned-ai/pocket-tts-greek'
    return data['entries']
ENTRIES=load()
BY_FILE={}
for item in ENTRIES.values():
    name=item.get('file','')
    if _VALID.fullmatch(name) and (WAV/name).is_file():
        BY_FILE[name]=WAV/name
def url(text):
    if not isinstance(text,str) or not text:return None
    item=ENTRIES.get(hashlib.sha256(text.encode('utf-8')).hexdigest()[:32])
    if item and item.get('text')==text and item.get('file') in BY_FILE:
        return PREFIX+item['file']
    variants=listening.BY_TEXT.get(text,())
    for variant in variants:
        name=variant.get('file')
        if name in listening.AUDIO:
            return '/greek/audio/'+name
    return None
def record(text):
    clip=url(text)
    return dict(pronunciationUrl=clip,pronunciationOffline=bool(clip),pronunciationText=text)
