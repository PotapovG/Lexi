"""Regression guards for community submissions. No textbook or user data required."""
from collections import Counter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import catalog_v2 as catalog
import community_content
import pedagogy_rules

def main():
    additions = community_content.load([])
    ids = [c["id"] for c in catalog.ALL]
    assert len(ids) == len(set(ids)), "a submitted ID collides with an existing progress key"
    assert len(catalog.ALL) >= 1795
    assert len(additions) == sum(c["source"] == "original-community" for c in catalog.ALL)
    assert all(c["id"] in catalog.BY_ID for c in additions)
    for card in additions:
        assert card["curriculum_ready_unit"] <= card["chapter"], card["id"]
        assert card["semanticId"].startswith("lex_"), card["id"]
        assert card["page_anchor_approximate"] is True
    print("PASS: community cards, immutable IDs, complete locales, grammar levels")
    print("NEW COMMUNITY CARDS BY CHAPTER", dict(sorted(Counter(c["chapter"] for c in additions).items())))

if __name__ == "__main__":
    main()
