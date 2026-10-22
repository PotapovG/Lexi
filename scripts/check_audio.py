#!/usr/bin/env python3
"""Verify independent Pocket TTS offline audio assets against source checksums."""
import argparse
import hashlib
import json
import re
import sys
import wave
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent


def expected_paths(root):
    expected = set()
    listening = json.loads((root / "pocket-listening/manifest.json").read_text())
    pronunciation = json.loads((root / "pocket-pronunciation/manifest.json").read_text())
    assert listening["engine"] == pronunciation["engine"] == "myned-ai/pocket-tts-greek"
    for entry in listening["entries"].values():
        for variant in entry["variants"].values():
            expected.add("pocket-listening/wav/" + variant["file"])
    for entry in pronunciation["entries"].values():
        expected.add("pocket-pronunciation/wav/" + entry["file"])
    if any(not re.fullmatch(r"pocket-(?:listening|pronunciation)/wav/[a-f0-9]{32}\.wav", name) for name in expected):
        raise RuntimeError("Invalid filename in Pocket audio manifest")
    return expected


def checksums(root):
    result = {}
    for line in (root / "media.sha256").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or relative in result:
            raise RuntimeError("Corrupt media checksum manifest")
        result[relative] = digest
    expected = expected_paths(root)
    if set(result) != expected:
        raise RuntimeError(f"Manifest/checksum mismatch: expected={len(expected)}, found={len(result)}")
    return result


def valid_audio(file, digest):
    if not file.is_file():
        return False
    try:
        h = hashlib.sha256()
        with file.open("rb") as fh:
            for block in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(block)
        if h.hexdigest() != digest:
            return False
        with wave.open(str(file), "rb") as wav:
            return (wav.getnchannels() == 1 and wav.getsampwidth() == 2
                    and wav.getframerate() == 24000
                    and 6000 <= wav.getnframes() <= 24000 * 120)
    except (OSError, EOFError, wave.Error):
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--allow-partial", action="store_true")
    args = ap.parse_args()
    manifest = checksums(args.root)
    failed = [name for name, digest in manifest.items() if not valid_audio(args.root / name, digest)]
    print(f"Pocket media: {len(manifest) - len(failed)}/{len(manifest)} verified")
    if failed and not args.allow_partial:
        print(f"Missing or corrupt: {len(failed)}. Examples: {failed[:3]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
