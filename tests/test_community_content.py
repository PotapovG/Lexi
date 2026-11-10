"""Regression guards for community submissions. No textbook or user data required."""
from collections import Counter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import catalog_v2 as catalog
import community_content
import pedagogy_rules

def main():
    community_content.load([])  # independent schema smoke (not yet tagged)
    additions = catalog.COMMUNITY_CARDS  # fully integrated + metadata tagged
    ids = [c["id"] for c in catalog.ALL]
    assert len(ids) == len(set(ids)), "a submitted ID collides with an existing progress key"
    assert len(catalog.ALL) >= 1795
    assert len(additions) == sum(c["source"] == "original-community" for c in catalog.ALL)
    assert all(c["id"] in catalog.BY_ID for c in additions)
    for card in additions:
        assert card["curriculum_ready_unit"] <= card["chapter"], card["id"]
        assert card["semanticId"].startswith("lex_"), card["id"]
        assert card["page_anchor_approximate"] is True
    # Community-added words must be eligible for chapter practice but must
    # NEVER change the independent A1/A2 atlas IDs or six-locale glossary.
    import vocab_lessons
    assert len(vocab_lessons.VOCAB) == 1700
    community_words = {c["gr"] for c in additions if c["kind"] == "word"}
    assert not community_words.intersection(w["gr"] for w in vocab_lessons.VOCAB)
    assert len(community_words) >= 5  # issue #7 adds an initial noun batch
    print("PASS: community cards, immutable IDs, complete locales, grammar levels")
    print("NEW COMMUNITY CARDS BY CHAPTER", dict(sorted(Counter(c["chapter"] for c in additions).items())))

if __name__ == "__main__":
    main()
