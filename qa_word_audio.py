"""Audio playback feature integration without mic or data mutations."""
import json,re,tempfile,urllib.request
from pathlib import Path
import server,word_audio,advanced_syllables,vocab_lessons
from collections import Counter
assert len(server.ALL)==1795
assert len(server.EXTRA_ALL)==26 and len(server.SYLLABLE_ALL)==35
assert len(server.PRACTICE_ALL)==1978 and len(server.LISTEN_CARDS)==717
assert len(vocab_lessons.VOCAB)==1700
assert len(server.listening.AUDIO)==1266
assert server.VOCAB_OFFLINE_AUDIO==1700
assert len({x['gr'] for x in vocab_lessons.VOCAB})==1700
vocab_matches=[word_audio.lookup(w['gr'],server.listening) for w in vocab_lessons.VOCAB]
syllable_matches=[word_audio.lookup(x['gr'],server.listening) for x in server.SYLLABLE_ALL]
assert sum(bool(meta['audioUrl']) for meta in vocab_matches)==server.VOCAB_OFFLINE_AUDIO
assert sum(bool(meta['audioUrl']) for meta in syllable_matches)==35
assert all(meta['speechText']==w['gr'] for meta,w in zip(vocab_matches,vocab_lessons.VOCAB))
assert all(meta['audioUrl'] is None if meta['audioSource']=='unavailable' else
        meta['audioUrl'].startswith(('/greek/audio/','/greek/pronunciation/')) for meta in vocab_matches)
assert all(meta['audioVoice'] in server.listening.APPROVED for meta in vocab_matches if meta['audioUrl'])
assert all((server.listening.AUDIO.get(m['audioUrl'].split('/')[-1]) or
               word_audio._pronunciation.BY_FILE.get(m['audioUrl'].split('/')[-1])).is_file()
           for m in vocab_matches if m['audioUrl'])
assert word_audio.lookup('not a Greek entry',server.listening)['audioUrl'] is None

lang=('ru','en','zh','ar','es','pt')
for card in server.PRACTICE_ALL:
    if card['kind'] not in ('accent','syllable'):continue
    for locale in lang:
        direction='accent' if card['kind']=='accent' else 'stress_syllable'
        question=server.format_question(card,direction,locale)
        assert question['id']==card['id']
        meta=question['wordAudio']
        expected=card['accented'] if card['kind']=='accent' else card['gr']
        assert meta['speechText']==expected
        assert meta['audioSource']==('pocket' if meta['audioUrl'] else 'unavailable')
        # Answer index must not be exposed by audio metadata.
        assert 'accent_index' not in meta and 'stressedIndex' not in meta

with tempfile.TemporaryDirectory(prefix='lexi-audio-test-') as d:
    orig=server.DB
    try:
        server.DB=str(Path(d)/'student.sqlite3')
        server.init_db()
        for locale in lang:
            for review in (False,):
                with server.conn() as db:
                    lesson=vocab_lessons.lesson(db,'one-learner','all','A1',locale,review=review)
                assert len(lesson['words'])==10
                for card in lesson['words']:
                    card['wordAudio']=word_audio.lookup(card['gr'],server.listening)
                    assert card['wordAudio']['speechText']==card['gr']
                    assert card['wordAudio']['audioSource'] in ('pocket','unavailable')
        with server.conn() as db:
            assert db.execute('pragma quick_check').fetchone()[0]=='ok'
            assert db.execute('select count(*) from attempts').fetchone()[0]==0
    finally:server.DB=orig
s=Path('PEDAGOGY_ROADMAP.md').read_text(encoding='utf-8')
assert 'NOT TO IMPLEMENT' in s and 'microphone' in s
s=Path('greek_word_audio.js').read_text()
assert 'getUserMedia' not in s and 'MediaRecorder' not in s and 'microphone' in s
assert 'SpeechSynthesisUtterance' not in s and 'speechSynthesis' not in s and 'pocket' in s
print('PASS AUDIO INTEGRATION:',server.VOCAB_OFFLINE_AUDIO,'/1700 exact offline vocab, 35/35 offline syllables, '
      'all words Pocket only; no device TTS; 6 locales, 549 accent+35 syllable questions, '
      'isolated vocab 10-word lessons, 1795 core/717 listening unchanged')
