#!/usr/bin/env python3
"""Privacy-preserving textbook literal-overlap review; never stores publisher text.

Requires user-owned PDF and local pdftotext; prints only Lexi card IDs and
word counts/page indexes. No licensed excerpts are printed or uploaded.
"""
import argparse
import collections
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


def words(value):
    cleaned = "".join(c for c in unicodedata.normalize("NFKD", value).lower()
                      if not unicodedata.combining(c))
    return re.findall(r"[^\W_]+", cleaned, flags=re.UNICODE)


def source_fragments():
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))
    import server
    records = []
    for card in server.PRACTICE_ALL:
        key = str(card.get("id"))
        label = str(card.get("kind", "?"))
        for field in ("gr", "prompt"):
            s = card.get(field)
            if isinstance(s, str) and len(words(s)) >= 5:
                records.append((key, label, field, s))
        for field in ("lines", "gaps", "bank", "options"):
            for idx, s in enumerate(card.get(field, []) or []):
                if isinstance(s, str) and len(words(s)) >= 5:
                    records.append((key, label, f"{field}[{idx}]", s))
    # The separate vocabulary is one or two headwords, not publisher prose.
    return records


def reference_pages(pdf=None, text=None):
    if pdf is not None:
        binary = shutil.which("pdftotext")
        if not binary:
            raise RuntimeError("pdftotext missing (install poppler-utils)")
        content = subprocess.check_output([binary, "-layout", str(pdf), "-"])
    else:
        content = Path(text).read_bytes()
    return [words(t) for t in content.decode("utf-8", errors="replace").split("\f")]


def review(reference, snippets, minimum=5):
    lookup = collections.defaultdict(list)
    for page_no, p in enumerate(reference, 1):
        for i in range(0, len(p) - minimum + 1):
            lookup[tuple(p[i:i + minimum])].append((page_no, i))
    matches = []
    for key, kind, field, raw in snippets:
        ws = words(raw)
        best = (0, 0)
        for i in range(0, len(ws) - minimum + 1):
            for pageno, offset in lookup.get(tuple(ws[i:i + minimum]), ()):
                ref = reference[pageno - 1]
                n = minimum
                while i + n < len(ws) and offset + n < len(ref) and ws[i + n] == ref[offset + n]:
                    n += 1
                if n > best[0]:
                    best = (n, pageno)
        if best[0] >= minimum:
            matches.append(dict(card=key, kind=kind, field=field,
                                consecutive_words=best[0], pdf_page=best[1]))
    return sorted(matches, key=lambda x: (-x["consecutive_words"], x["card"], x["field"]))


def main():
    ap = argparse.ArgumentParser()
    ref = ap.add_mutually_exclusive_group(required=True)
    ref.add_argument("--pdf", type=Path)
    ref.add_argument("--reference-text", type=Path)
    ap.add_argument("--strict", action="store_true", help="fail on >=5 words (default fail >=7)")
    args = ap.parse_args()
    pages = reference_pages(args.pdf, args.reference_text)
    records = source_fragments()
    found = review(pages, records)
    print(json.dumps({"pdf_pages":len(pages), "source_fragments":len(records),
                      "candidates":found, "review_note":"manual review needed; no copyrighted passages emitted"},
                     ensure_ascii=False, indent=2))
    return 1 if any(x["consecutive_words"] >= (5 if args.strict else 7) for x in found) else 0


if __name__ == "__main__":
    sys.exit(main())
