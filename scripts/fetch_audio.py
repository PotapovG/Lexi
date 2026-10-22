#!/usr/bin/env python3
"""Resumable Pocket TTS WAV transfer, strictly verifying SHA256 against Git."""
import argparse
import concurrent.futures
import hashlib
import os
import tempfile
import urllib.request
from pathlib import Path

from check_audio import DEFAULT_ROOT, checksums, valid_audio


def fetch_one(root, source, relative, digest, timeout):
    target = root / relative
    if valid_audio(target, digest):
        return "cached"
    target.parent.mkdir(parents=True, exist_ok=True)
    # Live demo exposes /audio and /pronunciation under its /greek path.
    url_path = ("audio/" if relative.startswith("pocket-listening/") else "pronunciation/") + target.name
    request = urllib.request.Request(source.rstrip("/") + "/" + url_path, headers={"User-Agent": "LexiCommunityMedia/1.0"})
    fd, tmp = tempfile.mkstemp(prefix=".download-", suffix=".wav", dir=target.parent)
    try:
        hasher = hashlib.sha256()
        with os.fdopen(fd, "wb") as output, urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status}: {url_path}")
            while True:
                data = response.read(1024 * 1024)
                if not data:
                    break
                output.write(data)
                hasher.update(data)
        if hasher.hexdigest() != digest or not valid_audio(Path(tmp), digest):
            raise ValueError(f"Wrong SHA256/WAV format for {relative}")
        os.replace(tmp, target)
        return "downloaded"
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="https://potapovfamily.com/greek/")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="for initial smoke testing")
    ap.add_argument("--timeout", type=int, default=35)
    args = ap.parse_args()
    if not args.source.startswith("https://") and not args.source.startswith("http://localhost:"):
        ap.error("Source must be HTTPS or http://localhost:<port>")
    if not 1 <= args.workers <= 8 or args.limit < 0:
        ap.error("Invalid worker or limit setting")
    expected = sorted(checksums(args.root).items())
    if args.limit:
        expected = expected[:args.limit]
    results = []
    errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(fetch_one, args.root, args.source, name, digest, args.timeout): name
                   for name, digest in expected}
        for n, task in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                results.append(task.result())
            except Exception as exc:
                errors.append(f"{futures[task]}: {exc}")
            if n % 100 == 0:
                print(f"Transferred {n}/{len(expected)}, errors={len(errors)}", flush=True)
    print(f"verified={len(results)}/{len(expected)}, downloaded={results.count('downloaded')}, "
          f"cached={results.count('cached')}, errors={len(errors)}")
    for error in errors[:10]:
        print(error)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
