"""Exact-match pronunciation lookup for approved existing Greek Pocket TTS WAV.

Returns only files already indexed/validated by the listening_catalog's
six-voice manifest and file allowlist. No microphone, synthesis on server,
paid API or unlicensed resource. The client may separately use a Greek
No device speech voice is ever allowed: missing Pocket WAV means silence.
"""
import unicodedata
import pronunciation_audio as _pronunciation

def canonical(text):
    if not isinstance(text,str):
        return ''
    return unicodedata.normalize('NFC',text.strip())

def lookup(text,listening):
    greek=canonical(text)
    assert len(greek)<=400
    new_clip=_pronunciation.url(greek)
    if new_clip and new_clip.startswith('/greek/pronunciation/'):
        ident=_pronunciation.ENTRIES.get(_pronunciation.hashlib.sha256(greek.encode('utf-8')).hexdigest()[:32],{})
        return dict(speechText=greek,audioUrl=new_clip,audioVoice=ident.get('voice'),
                    audioSource='pocket')
    variants=listening.BY_TEXT.get(greek,[])
    clip=next((v for v in variants if v.get('style')=='clear' and
              v.get('file') in listening.AUDIO),None)
    return dict(speechText=greek,
          audioUrl=('/greek/audio/'+clip['file'] if clip else None),
          audioVoice=(clip['voice'] if clip else None),
          audioSource=('pocket' if clip else 'unavailable'))
