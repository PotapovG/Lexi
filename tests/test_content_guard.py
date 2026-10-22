"""Protect against regression of one source-matched dialogue question."""
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import server


def normalized(s):
    return " ".join(re.findall(r"[^\W_]+",
       "".join(c for c in unicodedata.normalize("NFKD", s).lower()
               if not unicodedata.combining(c))))


def test_known_match_not_reintroduced():
    # Hash of a privately identified verbatim textbook question.
    # Do not commit the protected source excerpt itself.
    protected_digest = "85d350659c31d2160535257830592f78f8388b1b121fba19e8e1a7129f4ffbae"
    protected_length = 6
    for card in server.PRACTICE_ALL:
        for value in [card.get("gr", ""), card.get("prompt", "")] + list(card.get("lines", [])):
            if not isinstance(value, str):
                continue
            segments = normalized(value).split()
            for offset in range(max(0, len(segments) - protected_length + 1)):
                fragment = " ".join(segments[offset:offset + protected_length])
                assert hashlib.sha256(fragment.encode()).hexdigest() != protected_digest, card["id"]
    assert server.BY_ID["dlg064"]["gaps"] == ["Στον τρίτο όροφο", "Ναι, έχει ασανσέρ"]
    assert server.BY_ID["dlg064"]["semanticId"] == "lex_961c9af921492376"


def test_audit_finds_literal_long_overlap():
    from scripts.audit_textbook_overlap import review, words
    a = "Η Μαρία διαβάζει καθημερινά στο μεγάλο σπίτι με φίλους."
    matches = review([words(a)], [("test01", "sentence", "gr", a)], minimum=5)
    assert len(matches) == 1 and matches[0]["consecutive_words"] >= 9


if __name__ == "__main__":
    test_known_match_not_reintroduced()
    test_audit_finds_literal_long_overlap()
    print("PASS: commercial textbook candidate regression and audit shingle detector")
