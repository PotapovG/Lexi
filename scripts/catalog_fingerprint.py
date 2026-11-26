#!/usr/bin/env python3
"""Compare the shipped authored catalog across source and container installs."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys

def fingerprint(root):
    sys.path.insert(0,str(root))
    import server
    groups={"book":server.ALL,"grammar":server.GRAMMAR2_ALL,
            "extra":server.EXTRA_ALL,"syllable":server.SYLLABLE_ALL,
            "enclitic":server.ENCLITIC_ALL,"order":server.ORDER2_ALL,
            "clock":server.CLOCK_ALL,"culture":list(server.CULTURE_BY_ID.values()),
            "vocabulary":server.vocab.VOCAB}
    serial={name:sorted(cards,key=lambda card:card["id"]) for name,cards in groups.items()}
    content={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted((root/"content").rglob("*.json"))}
    return {"schema":1,"counts":{name:len(cards) for name,cards in groups.items()},
            "catalogSha256":hashlib.sha256(json.dumps(serial,ensure_ascii=False,
                           sort_keys=True,separators=(",",":")).encode()).hexdigest(),
            "contentFiles":content,
            "bookTypes":dict(sorted(collections.Counter(c.get("kind",c.get("type","unknown")) for c in server.ALL).items()))}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-root",type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    print(json.dumps(fingerprint(args.app_root.resolve()),sort_keys=True,ensure_ascii=False,indent=2))
