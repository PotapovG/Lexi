#!/usr/bin/env python3
"""Safely install a verified Lexi Pocket WAV release without trusting tar paths."""
import argparse
import hashlib
import os
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from check_audio import DEFAULT_ROOT, checksums, valid_audio

RELEASE_BASE = "https://github.com/PotapovG/Lexi/releases/download/audio-v1"
ARCHIVE = "lexi-pocket-audio-v1.tar.gz"
MAX_TOTAL_BYTES = 400 * 1024 * 1024

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=RELEASE_BASE)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    expected = checksums(args.root)
    with tempfile.TemporaryDirectory(prefix="lexi-audio-release-") as folder:
        artifact = Path(folder) / ARCHIVE
        with urllib.request.urlopen(args.url.rstrip("/") + "/" + ARCHIVE + ".sha256", timeout=30) as response:
            expected_digest = response.read(512).decode().split()[0]
        if len(expected_digest) != 64 or any(x not in "0123456789abcdef" for x in expected_digest):
            raise ValueError("Invalid release checksum file")
        hasher = hashlib.sha256()
        size = 0
        with urllib.request.urlopen(args.url.rstrip("/") + "/" + ARCHIVE, timeout=60) as response, artifact.open("wb") as output:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                size += len(block)
                if size > MAX_TOTAL_BYTES:
                    raise RuntimeError("Release download exceeds size limit")
                output.write(block)
                hasher.update(block)
        if hasher.hexdigest() != expected_digest:
            raise RuntimeError("Release archive SHA256 mismatch")
        found = set()
        with tarfile.open(artifact, "r:gz") as archive:
            for entry in archive:
                if entry.isdir():
                    continue
                name = entry.name
                if not entry.isfile() or name not in expected or name in found or entry.size > 10 * 1024 * 1024:
                    raise RuntimeError(f"Unexpected release entry: {name}")
                found.add(name)
                target = args.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                fd, tmp = tempfile.mkstemp(prefix=".release-", suffix=".wav", dir=target.parent)
                try:
                    with os.fdopen(fd, "wb") as output, archive.extractfile(entry) as src:
                        while True:
                            block = src.read(1024 * 1024)
                            if not block: break
                            output.write(block)
                    if not valid_audio(Path(tmp), expected[name]):
                        raise RuntimeError("WAV checksum or format mismatch: " + name)
                    os.replace(tmp, target)
                finally:
                    if os.path.exists(tmp): os.unlink(tmp)
        if found != set(expected):
            raise RuntimeError(f"Release missing {len(set(expected) - found)} media files")
    print(f"Verified and installed {len(found)} Pocket TTS recordings")

if __name__ == "__main__":
    main()
