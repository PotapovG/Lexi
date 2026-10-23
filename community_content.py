"""Strict loader for independently authored community course cards.

Only simple vocabulary/phrases/sentences. The commercial reference is not
needed here. Cards get immutable IDs for stable learner history.
"""
import json
import re
import unicodedata
from pathlib import Path

LANGUAGES = ("ru", "en", "zh", "ar", "es", "pt")
TYPES = {"word", "phrase", "sentence"}
ID = re.compile(r"cm(0[1-9]|1[0-9]|20)_[0-9]{4}$")
ROOT = Path(__file__).resolve().parent / "content" / "community"

def fingerprint(value):
    """Normalise text for duplicate detection, not for grading Greek answers."""
    s = unicodedata.normalize("NFD", value).casefold()
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.findall(r"[^\W_]+", s, flags=re.UNICODE))

def load(base_cards=()):
    from textbook_alignment import INDEX
    from pedagogy_rules import PREMATURE_TEXT_RULES, GRAMMAR_FIRST_UNIT
    used_ids = {str(c["id"]) for c in base_cards}
    used_text = {fingerprint(c["gr"]) for c in base_cards
                 if c.get("kind") in TYPES and isinstance(c.get("gr"), str)}
    added = []
    for file in sorted(ROOT.glob("*.json")):
        records = json.loads(file.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError(f"{file.name}: expected JSON array")
        for index, raw in enumerate(records, 1):
            where = f"{file.name}:{index}"
            if not isinstance(raw, dict):
                raise ValueError(f"{where}: expected object")
            cid = raw.get("id")
            chapter = raw.get("chapter")
            if not isinstance(cid, str) or not ID.fullmatch(cid):
                raise ValueError(f"{where}: invalid stable ID")
            if type(chapter) is not int or chapter not in INDEX or chapter <= 0:
                raise ValueError(f"{where}: invalid printed chapter")
            if int(cid[2:4]) != chapter:
                raise ValueError(f"{where}: ID/chapter mismatch")
            if cid in used_ids:
                raise ValueError(f"{where}: reused card ID {cid}")
            if raw.get("kind") not in TYPES:
                raise ValueError(f"{where}: unsupported kind")
            page = raw.get("page")
            section = INDEX[chapter]
            if type(page) is not int or not(section["start"] <= page <= section["end"]):
                raise ValueError(f"{where}: page outside printed chapter")
            required = ("id", "chapter", "page", "kind", "topic", "gr", *LANGUAGES)
            for field in required:
                if field in ("chapter", "page", "id", "kind"):
                    continue
                value = raw.get(field)
                if not isinstance(value, str) or not value.strip() or value != value.strip():
                    raise ValueError(f"{where}: invalid {field}")
            greek = raw["gr"]
            if greek != unicodedata.normalize("NFC", greek):
                raise ValueError(f"{where}: Greek text must be NFC")
            if re.search(r"[A-Za-zА-Яа-яЁё]", greek):
                raise ValueError(f"{where}: non-Greek letters in Greek text")
            if chapter <= 5:
                for feature, pattern in PREMATURE_TEXT_RULES:
                    if pattern.search(greek) and GRAMMAR_FIRST_UNIT[feature] > chapter:
                        raise ValueError(f"{where}: premature grammar {feature}")
                if re.search(r"\b(?:να|γράφεται|μαθαίνω|μαθαίνεις)\b", greek, re.I):
                    raise ValueError(f"{where}: grammar beyond early chapters")
            key = fingerprint(greek)
            if key in used_text:
                raise ValueError(f"{where}: duplicate Greek exercise text")
            used_ids.add(cid)
            used_text.add(key)
            card = {k: raw[k] for k in required}
            card.update(unit=chapter, source="original-community",
                        page_anchor_approximate=True)
            added.append(card)
    return added
