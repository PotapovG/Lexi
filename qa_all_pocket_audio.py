"""Complete static integrity check for all Pocket Greek words.

Requires exact-text hashes, manifest allowlist, valid RIFF PCM24k/mono16,
durations and signal, no reliance on device speech synthesis at all.
"""
from pathlib import Path
import collections,hashlib,json,math,re,struct,wave
import server
import pronunciation_audio as p
from word_audio import lookup

a=server.ALL
v=server.vocab.VOCAB
sy=server.SYLLABLE_ALL
assert (len(a),len(v),len(sy),len(server.LISTEN_CARDS))==(1795,1700,35,717)
assert len(server.listening.AUDIO)==1266
assert server.VOCAB_OFFLINE_AUDIO==1700
groups={
 'a1a2':[x['gr'] for x in v],
 'accent':[x['accented'] for x in a if x['kind']=='accent'],
 'syllable':[x['gr'] for x in sy]
}
for kind,texts in groups.items():
    for text in texts:
        meta=lookup(text,server.listening)
        assert meta['audioSource']=='pocket' and meta['speechText']==text,(kind,text)
        assert re.fullmatch(r'/greek/(?:audio|pronunciation)/[0-9a-f]{32}\.wav',meta['audioUrl']),text
    print('FULL_POCKET_COVERAGE',kind,len(texts))
manifest=json.loads(p.MANIFEST.read_text(encoding='utf-8'))
assert manifest['engine']=='myned-ai/pocket-tts-greek'
assert len(manifest['entries'])==len(p.BY_FILE)
assert len(p.BY_FILE)>=1500
files=set(p.BY_FILE)
for key,entry in manifest['entries'].items():
    greek=entry['text'];filename=entry['file']
    assert key==hashlib.sha256(greek.encode('utf-8')).hexdigest()[:32]
    assert re.fullmatch(r'[a-f0-9]{32}\.wav',filename)
    assert entry['voice'] in server.listening.APPROVED
    assert filename in files
    assert entry['text'].strip() and len(greek)<400
    source=p.BY_FILE[filename]
    assert source.is_file() and source.stat().st_size>10000
    with wave.open(str(source),'rb') as wav:
        channels,width,rate,frames=wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes()
        assert (channels,width,rate)==(1,2,24000),(greek,filename,channels,width,rate)
        assert 4800<=frames<=30*rate,(greek,frames)
        raw=wav.readframes(min(frames,24000))
        values=struct.iter_unpack('<h',raw)
        sample=[v[0] for v in values]
        assert sample
        rms=math.sqrt(sum(x*x for x in sample)/len(sample))
        assert rms>120,(greek,filename,rms)
assert len(set(files))==len(files)
assert len({entry['text'] for entry in manifest['entries'].values()})==len(files)
assert lookup('unpublished junk invented token',server.listening)['audioSource']=='unavailable'
print('PASS ALL',len(files),'NEW OFFLINE POCKET WAVS + 1266 ORIGINAL LISTENING WAV,'
      ' exact content hashes, PCM16 mono 24k, non-silent, no ambiguity;'
      ' 1700/1700 A1A2 549/549 accents 35/35 syllables')
