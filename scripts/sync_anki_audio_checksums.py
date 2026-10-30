#!/usr/bin/env python3
"""Append pre-rendered Greek Pocket TTS SHA256 entries for a reviewed release.

Requires manifest and generated files already staged; never synthesizes on a
production request or changes user SQLite data. Run only after audio generation.
Existing media hashes are preserved; full check_audio.py verifies them after.
"""
import hashlib
import json
import os
import re
import tempfile
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
MANIFEST=ROOT/"pocket-pronunciation/manifest.json"
FILE=ROOT/"media.sha256"
VALID=re.compile(r"pocket-pronunciation/wav/[0-9a-f]{32}\.wav\Z")
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024),b""):h.update(block)
    return h.hexdigest()

def main():
    manifest=json.loads(MANIFEST.read_text())
    assert manifest["engine"]=="myned-ai/pocket-tts-greek"
    existing={}
    for line in FILE.read_text().splitlines():
        sha,name=line.split("  ",1)
        assert re.fullmatch(r"[0-9a-f]{64}",sha) and name not in existing
        existing[name]=sha
    added=0
    for item in manifest["entries"].values():
        name="pocket-pronunciation/wav/"+item["file"]
        if not VALID.fullmatch(name):raise ValueError("invalid media path")
        path=ROOT/name
        if not path.is_file():raise ValueError("missing audio: "+name)
        if name in existing:continue
        with wave.open(str(path),"rb") as wav:
            if not (wav.getnchannels()==1 and wav.getsampwidth()==2
                    and wav.getframerate()==24000
                    and 4800<=wav.getnframes()<=720000):
                raise ValueError("invalid PCM: "+name)
        existing[name]=digest(path)
        added+=1
    fd,temp=tempfile.mkstemp(prefix=".anki-media-",dir=ROOT)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as stream:
            for name in sorted(existing):
                stream.write(existing[name]+"  "+name+"\n")
        os.replace(temp,FILE)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    print("SHA256 manifest: +",added,"audio files; total",len(existing))

if __name__=="__main__":
    main()
