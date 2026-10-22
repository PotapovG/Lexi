#!/usr/bin/env python3
"""Validate Greek Pocket pronunciation manifest, exact joins and fallbacks."""
import json,wave,hashlib,re
from pathlib import Path
import server,pronunciation_audio as audio,word_audio
base=Path(__file__).parent
manifest=json.loads((base/'pocket-pronunciation/manifest.json').read_text())
assert manifest['engine']=='myned-ai/pocket-tts-greek'
assert len(manifest['entries'])>=315
assert len(audio.BY_FILE)==len(manifest['entries'])
for digest,item in manifest['entries'].items():
    text=item['text'];name=item['file']
    assert hashlib.sha256(text.encode()).hexdigest()[:32]==digest
    assert re.fullmatch(r'[0-9a-f]{32}\.wav',name)
    path=audio.BY_FILE.get(name);assert path and path.is_file()
    with wave.open(str(path)) as w:
        assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,24000)
        assert 4800<=w.getnframes()<=24000*30
assert len(server.ALL)==1795 and len(server.PRACTICE_ALL)==1978
assert len(server.LISTEN_CARDS)==717 and len(server.listening.AUDIO)==1266
assert len(server.vocab.VOCAB)==1700
assert server.VOCAB_OFFLINE_AUDIO>=752
assert sum(bool(word_audio.lookup(c['gr'],server.listening)['audioUrl']) for c in server.SYLLABLE_ALL)==35
assert word_audio.lookup('plain unavailable invented word',server.listening)['audioUrl'] is None
assert audio.url('../secret') is None
assert audio.url('') is None
assert 'PERMANENTLY OUT OF SCOPE' in (base/'PEDAGOGY_ROADMAP.md').read_text()
print('PASS PRONUNCIATION MANIFEST',len(audio.BY_FILE),'new verified WAV,',
      server.VOCAB_OFFLINE_AUDIO,'/1700 A1/A2 offline, 35/35 syllable, original listening untouched')
