"""Cyprus Culture -> existing Lexi quiz card adapter (no new quiz backend).

The content is authored/validated by culture_content.py (CULT-01).
The adapter does not change A1/A2 card IDs, SQLite, SRS or authentication.
"""
import random
from datetime import date

import culture_content as contract

CULTURE_KIND = "culture"
CULTURE_DIRECTION = "culture_select"
CULTURE_UNIT = -100


def to_card(question: dict, fact: dict) -> dict:
    """Adapt a four-option Culture record to a small shared Quiz card."""
    return {
        "id": question["id"],
        "kind": CULTURE_KIND,
        "direction": CULTURE_DIRECTION,
        "unit": CULTURE_UNIT,
        "chapter": CULTURE_UNIT,
        "page": 0,
        "topic": question["topic"],
        "factId": question["fact_id"],
        "semanticId": question["fact_id"],
        "gr": question["question_el"],
        "options": tuple(question["options_el"]),
        "answerIndex": question["correct_index"],
        "format": question["format"],
        "difficulty": question["difficulty"],
        "translations": question["translations"],
        "explanations": question["explanation"],
        "source": question["source"],
        "contentVersion": question["version"],
        "vocabIds": tuple(question["vocab_ids"]),
        "verifiedAt": question["verified_at"],
    }


def load(root, *, today: date | None = None):
    """Load only verified eligible items; never import synthetic test fixtures."""
    today = today or date.today()
    config, facts, questions, vocabulary, lessons = contract.read_bank(root / "content" / "culture")
    errors = contract.validate(config, facts, questions, vocabulary, lessons, today=today)
    # Fail closed on malformed real content; publication review is validated
    # before the server can serve any part of a changed content batch.
    if errors:
        raise ValueError("invalid Cyprus Culture content: " + "; ".join(errors[:6]))
    by_fact = {row["id"]: row for row in facts}
    cards = {}
    for q in questions:
        fact = by_fact[q["fact_id"]]
        if contract.exam_eligible(q, fact, today=today):
            cards[q["id"]] = to_card(q, fact)
    return config, cards


def format_card(card: dict, lang: str, *, shuffle=random.sample) -> dict:
    """Safe pre-answer payload; NEVER include answer index/translations/feedback."""
    if lang not in ("ru", "en"):
        raise ValueError("culture requires ru/en language")
    return {
        "id": card["id"],
        "direction": CULTURE_DIRECTION,
        "kind": CULTURE_KIND,
        "unit": card["unit"],
        "chapter": card["chapter"],
        "page": card["page"],
        "topic": card["topic"],
        "prompt": card["gr"],
        "note": "",
        "lang": lang,
        "semanticId": card["semanticId"],
        "factId": card["factId"],
        "cultureFormat": card["format"],
        "difficulty": card["difficulty"],
        "choices": shuffle(list(card["options"]), k=4),
        "sourcePageVerified": False,
    }


def after_answer(card: dict, lang: str, selected: str, correct: bool, assisted: bool) -> dict:
    translation = card["translations"][lang]
    return {
        "correct": correct,
        "answer": card["options"][card["answerIndex"]],
        "assisted": assisted,
        "independentCorrect": correct and not assisted,
        "factId": card["factId"],
        "cultureFormat": card["format"],
        "translation": translation["question"],
        "translationChoices": list(translation["options"]),
        "translationLang": lang,
        "explanation": card["explanations"][lang],
        "source": card["source"],
        "vocabIds": list(card["vocabIds"]),
    }


def topic_counts(config: dict, cards: dict) -> list[dict]:
    return [
        dict(topic, count=sum(c["topic"] == topic["code"] for c in cards.values()))
        for topic in config["topics"]
    ]
