"""Independent A1 conversations for existing dialogue gap-fill exercises.

Adds content to the existing dialogue kind; NO new learner mode, route, or
runtime dependency. Private classroom handouts provide learning goals only:
all dialogue text, translations and choices here are newly authored.
"""
import json
import re
import unicodedata
from pathlib import Path

from textbook_alignment import INDEX

SOURCE = "independent_a1_dialogue_20261110"
ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "content/conversations/a1_introductions_20261110.json").read_text(encoding="utf-8"))
LANGUAGES = ("ru", "en", "zh", "ar", "es", "pt")
SLOT = re.compile(r"\[\[(\d+)\]\]")
CARDS = []
assert len(DATA) == 12
for index, raw in enumerate(DATA, 101):
    cid = f"dlg{index:03d}"
    assert raw["id"] == cid, (cid, raw["id"])
    chapter, page = raw["chapter"], raw["page"]
    assert 1 <= chapter <= 4 and INDEX[chapter]["start"] <= page <= INDEX[chapter]["end"]
    lines = raw["lines"]
    gaps = raw["gaps"]
    bank = gaps + raw["wrong"]
    assert len(lines) == 4 and 1 <= len(gaps) <= 3
    assert len(bank) == len(set(bank)) == 8 and len(set(gaps)) == len(gaps)
    assert sorted(int(match) for line in lines for match in SLOT.findall(line)) == list(range(len(gaps)))
    assert all(re.match(r"^[ΑΒΓ]: ", line) for line in lines)
    assert all(unicodedata.normalize("NFC", value) == value
               for value in [*lines, *bank])
    assert all(re.search(r"[Α-Ωα-ωΆ-Ώά-ώ]", value) for value in [*lines, *bank])
    locales = raw["locales"]
    assert set(locales) == set(LANGUAGES)
    for language in LANGUAGES:
        translation = locales[language]
        assert len(translation["lines"]) == len(lines)
        assert len(translation["glosses"]) == len(gaps)
        assert all(isinstance(v, str) and v.strip() for v in
                   translation["lines"] + translation["glosses"])
        for greek, translated in zip(lines, translation["lines"]):
            assert SLOT.findall(greek) == SLOT.findall(translated), (cid, language)
    CARDS.append(dict(
        id=cid, kind="dialogue", chapter=chapter, unit=chapter, page=page,
        topic=raw["title"], gr=" ".join(lines), en="",
        source=SOURCE, curriculum="book", book_page_verified=False,
        page_anchor_approximate=True, lines=lines, gaps=gaps,
        bank=bank, locales=locales
    ))
BY_ID = {c["id"]: c for c in CARDS}
assert len(BY_ID) == len(CARDS) == 12
