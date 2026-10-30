"""Anki audio: pre-rendered Greek Pocket TTS, exact word/audio identity.

No speechSynthesis fallback. The same vetted recording is available at
learning, translation quiz and cumulative review stages.
"""
import re
import tempfile
import wave
from pathlib import Path
import json
import study_tracks
import word_audio
import listening_catalog
import pronunciation_audio as pronunciation
import server

URL=re.compile(r"^/greek/(?:pronunciation|audio)/([a-f0-9]{32})\.wav$")
all_words=study_tracks.WORDS
assert len(all_words)>=1600
available={}
for word in all_words:
    meta=word_audio.lookup(word["gr"],listening_catalog)
    assert meta["speechText"]==word["gr"]
    assert meta["audioSource"]=="pocket",(word["gr"],meta)
    url=meta["audioUrl"]
    assert url and URL.fullmatch(url),(word["gr"],meta)
    filename=URL.fullmatch(url).group(1)+".wav"
    path=(
        pronunciation.WAV/filename
        if url.startswith("/greek/pronunciation/") else
        listening_catalog.DIR/filename
    )
    assert path.is_file(),(word["gr"],path)
    with wave.open(str(path),"rb") as wav:
        assert wav.getnchannels()==1 and wav.getsampwidth()==2
        assert wav.getframerate()==24000
        assert 4800<=wav.getnframes()<=24000*30
    available[word["id"]]=meta

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/"practice.sqlite3")
    server.init_db()
    with server.conn() as db:
        preview=study_tracks.anki_get(db,"anki_audio_test","ru")
    assert preview["phase"]=="preview"
    assert preview["card"]["wordAudio"]==available[preview["card"]["id"]]
    assert preview["card"]["gr"]=="το όνομα"
    for idx in range(30):
        with server.conn() as db:
            preview=study_tracks.anki_action(db,"anki_audio_test","ru",{
                "revision":preview["revision"],"action":"advance"})
    assert preview["phase"]=="quiz"
    assert preview["card"]["wordAudio"]==available[preview["card"]["id"]]
    assert "translation" not in preview["card"]
    # A wrong translation must not grant progress; audio never leaks answer.
    wrong=next(x for x in preview["options"] if x!=study_tracks.BY_ID[preview["card"]["id"]]["ru"])
    with server.conn() as db:
        result=study_tracks.anki_action(db,"anki_audio_test","ru",{
            "revision":preview["revision"],"action":"answer",
            "cardId":preview["card"]["id"],"selected":wrong})
    assert not result["feedback"]["correct"] and result["misses"]==1
    assert result["card"]["wordAudio"]==available[result["card"]["id"]]

js=Path(__file__).with_name("tracks.js").read_text()
assert "window.LexiWordAudio.play(meta" in js
assert 'renderAnkiAudio(panel,anki.card)' in js
assert js.count('renderAnkiAudio(panel,anki.card)')==2
assert "speechSynthesis" not in js
existing_audio=Path(__file__).with_name("greek_word_audio.js").read_text()
assert "clip.playbackRate=slow?0.78:1;" in existing_audio
assert "speechSynthesis" not in existing_audio
assert 'LexiWordAudio?.stop()' in js
print("PASS "+str(len(all_words))+" exact Greek Pocket TTS WAV, 24 kHz mono and server allowlists")
print("PASS Anki study/quiz playback, no translation spoiler, 30-word gate, no browser TTS")
