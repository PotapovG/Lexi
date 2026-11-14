"""Cyprus Culture content contracts and offline validators (CULT-01).

This module has no web, database or application imports. Content is authored in
versioned JSON; publishing is gated by independent factual and language review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
TOPIC_CODES = (
    "GEO", "GOV", "HIS", "NEWS", "TRAD", "ECON", "HEALTH",
    "HOLIDAYS", "TRANSPORT", "LANG", "ENTRY", "TELECOM",
    "CLIMATE", "CURRENCY",
)
QUESTION_FORMATS = {"DIRECT", "CLOZE", "NEGATIVE", "CHRONOLOGY"}
STATES = {"draft", "reviewed", "published", "archived"}
ORIGINS = {"original", "reconstructed", "official_published"}
FACT_KINDS = {"evergreen", "periodic", "current"}
SOURCE_KINDS = {"official", "institutional", "academic", "journalism", "eyewitness"}
RIGHTS = {"independently_authored", "licensed_with_permission", "public_domain"}
REVIEW_CHECKS = ("greek", "ru", "en", "facts", "rights")
_GREEK = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
_ID = re.compile(r"^[a-z][a-z0-9_]{4,90}$")
_DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _date(value: object) -> date | None:
    if not isinstance(value, str) or not _DAY.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _same_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


def _source(errors: list[str], path: str, source: object) -> None:
    if not isinstance(source, dict):
        errors.append(f"{path}: source must be an object")
        return
    if source.get("kind") not in SOURCE_KINDS:
        errors.append(f"{path}: invalid source kind")
    url = source.get("url")
    if not _is_text(url):
        errors.append(f"{path}: missing source URL")
        return
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        errors.append(f"{path}: source URL must be a public HTTPS URL")
    elif parsed.hostname in {"localhost", "127.0.0.1", "example.com"}:
        errors.append(f"{path}: source URL is not an acceptable publication source")
    if not _is_text(source.get("title")):
        errors.append(f"{path}: source title is required")


def _review(errors: list[str], path: str, row: dict) -> None:
    if row.get("status") not in {"reviewed", "published"}:
        return
    review = row.get("review")
    if not isinstance(review, dict):
        errors.append(f"{path}: reviewed/published content needs human review metadata")
        return
    if not _is_text(review.get("editor")) or _date(review.get("at")) is None:
        errors.append(f"{path}: review editor and ISO review date required")
    checks = review.get("checks")
    if not isinstance(checks, dict) or any(checks.get(k) is not True for k in REVIEW_CHECKS):
        errors.append(f"{path}: Greek/RU/EN/fact/rights editorial checks must all pass")


def _status_and_dates(errors: list[str], path: str, row: dict, today: date) -> None:
    status = row.get("status")
    if status not in STATES:
        errors.append(f"{path}: invalid publication status")
    verified = _date(row.get("verified_at"))
    if verified is None:
        errors.append(f"{path}: verified_at must be an ISO date")
    if status in {"reviewed", "published"} and verified is not None and verified > today:
        errors.append(f"{path}: reviewed/published content verified in the future")
    kind = row.get("freshness")
    if kind not in FACT_KINDS:
        errors.append(f"{path}: freshness must be evergreen/periodic/current")
    until_raw = row.get("valid_until")
    until = _date(until_raw) if until_raw is not None else None
    if until_raw is not None and until is None:
        errors.append(f"{path}: invalid valid_until")
    due_raw = row.get("review_due")
    due = _date(due_raw) if due_raw is not None else None
    if due_raw is not None and due is None:
        errors.append(f"{path}: invalid review_due")
    if kind in {"periodic", "current"} and (until is None or due is None):
        errors.append(f"{path}: changing facts require review_due and valid_until")
    if verified and until and until < verified:
        errors.append(f"{path}: valid_until precedes verified_at")
    if verified and due and due < verified:
        errors.append(f"{path}: review_due precedes verified_at")
    if due and until and due > until:
        errors.append(f"{path}: review_due after valid_until")
    if status == "published" and ((until and today > until) or (due and today > due)):
        errors.append(f"{path}: published content is stale; reverify or archive")
    _review(errors, path, row)
    if row.get("rights") not in RIGHTS:
        errors.append(f"{path}: content rights must be explicitly declared")


def _lang_map(errors: list[str], path: str, obj: object, keys: tuple[str, ...]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: translations must be an object")
        return
    for lang in ("ru", "en"):
        value = obj.get(lang)
        if len(keys) == 1 and keys[0] == "text":
            if not _is_text(value):
                errors.append(f"{path}: {lang} text is missing")
        elif not isinstance(value, dict):
            errors.append(f"{path}: {lang} translation missing")
        else:
            for key in keys:
                if key == "options":
                    if not isinstance(value.get(key), list) or len(value[key]) != 4 or not all(
                        _is_text(v) for v in value[key]
                    ):
                        errors.append(f"{path}: {lang} needs four translated options")
                elif not _is_text(value.get(key)):
                    errors.append(f"{path}: {lang}.{key} translation missing")


def _basic(errors: list[str], row: object, kind: str, idx: int, today: date) -> str | None:
    path = f"{kind}[{idx}]"
    if not isinstance(row, dict):
        errors.append(f"{path}: expected object")
        return None
    identifier = row.get("id")
    if not isinstance(identifier, str) or not _ID.fullmatch(identifier):
        errors.append(f"{path}: invalid stable ID")
        identifier = None
    if row.get("topic") not in TOPIC_CODES:
        errors.append(f"{path}: unknown topic")
    _status_and_dates(errors, path, row, today)
    _source(errors, path, row.get("source"))
    return identifier


def validate(
    config: object,
    facts: list,
    questions: list,
    vocabulary: list,
    lessons: list,
    *,
    today: date | None = None,
) -> list[str]:
    """Return actionable errors; never mutate or silently repair authored content."""
    today = today or date.today()
    errors: list[str] = []

    if not isinstance(config, dict):
        return ["config: expected object"]
    if config.get("schema_version") != SCHEMA_VERSION:
        errors.append("config: unsupported schema_version")
    topics = config.get("topics")
    if not isinstance(topics, list) or {t.get("code") for t in topics if isinstance(t, dict)} != set(TOPIC_CODES) or len(topics) != len(TOPIC_CODES):
        errors.append("config: must define each of the 14 official topic buckets exactly once")
    else:
        for topic in topics:
            if not all(_is_text(topic.get(k)) for k in ("ru", "en", "el")):
                errors.append(f"config: topic {topic['code']} missing translated label")
    weights = config.get("exam_format_weights")
    if not isinstance(weights, dict) or set(weights) != QUESTION_FORMATS or any(
        isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in weights.values()
    ):
        errors.append("config: positive integer weight required for all four question formats")

    for name, values in (("facts", facts), ("questions", questions),
                         ("vocabulary", vocabulary), ("lessons", lessons)):
        if not isinstance(values, list):
            errors.append(f"{name}: expected list")
    if errors and not all(isinstance(v, list) for v in (facts, questions, vocabulary, lessons)):
        return errors

    seen_ids: set[str] = set()
    facts_by_id: dict[str, dict] = {}
    questions_by_id: dict[str, dict] = {}
    prompts: set[str] = set()
    lemmas: set[str] = set()
    for name, records in (("facts", facts), ("questions", questions),
                          ("vocabulary", vocabulary), ("lessons", lessons)):
        for index, row in enumerate(records):
            ident = _basic(errors, row, name, index, today)
            if ident:
                if ident in seen_ids:
                    errors.append(f"{name}[{index}]: duplicate ID {ident}")
                seen_ids.add(ident)
            if not isinstance(row, dict):
                continue
            path = f"{name}[{index}]"
            if name == "facts":
                if ident:
                    facts_by_id[ident] = row
                if not _is_text(row.get("statement_el")) or not _GREEK.search(row["statement_el"]):
                    errors.append(f"{path}: missing Greek fact statement")
            elif name == "questions":
                if ident:
                    questions_by_id[ident] = row
                if not _is_text(row.get("fact_id")):
                    errors.append(f"{path}: fact_id required")
                if row.get("format") not in QUESTION_FORMATS:
                    errors.append(f"{path}: unknown format")
                if type(row.get("difficulty")) is not int or row["difficulty"] not in (1, 2, 3):
                    errors.append(f"{path}: difficulty must be 1..3")
                prompt = row.get("question_el")
                if not _is_text(prompt) or not _GREEK.search(prompt):
                    errors.append(f"{path}: missing Greek question")
                else:
                    if unicodedata.normalize("NFC", prompt) != prompt:
                        errors.append(f"{path}: Greek question must be NFC-normalized")
                    normalized = _same_text(prompt)
                    if normalized in prompts:
                        errors.append(f"{path}: duplicate question prompt")
                    prompts.add(normalized)
                options = row.get("options_el")
                if not isinstance(options, list) or len(options) != 4 or not all(_is_text(v) for v in options):
                    errors.append(f"{path}: four nonempty Greek options required")
                elif len({_same_text(v) for v in options}) != 4:
                    errors.append(f"{path}: duplicate answer options")
                answer = row.get("correct_index")
                if type(answer) is not int or answer not in range(4):
                    errors.append(f"{path}: correct_index must be 0..3")
                _lang_map(errors, f"{path}.translations", row.get("translations"), ("question", "options"))
                _lang_map(errors, f"{path}.explanation", row.get("explanation"), ("text",))
                if row.get("format") == "NEGATIVE":
                    truth = row.get("option_truth")
                    if not isinstance(truth, list) or len(truth) != 4 or any(type(v) is not bool for v in truth):
                        errors.append(f"{path}: NEGATIVE requires four explicit boolean truth values")
                    elif truth.count(False) != 1 or truth.index(False) != answer:
                        errors.append(f"{path}: NEGATIVE must have 3 true and 1 false at correct_index")
                elif "option_truth" in row:
                    errors.append(f"{path}: option_truth is only for NEGATIVE")
                if row.get("origin") not in ORIGINS:
                    errors.append(f"{path}: invalid origin")
                if row.get("origin") == "official_published":
                    if row.get("rights") != "licensed_with_permission" or not isinstance(row.get("source"), dict) or row["source"].get("kind") != "official":
                        errors.append(f"{path}: official wording requires official source and confirmed reuse rights")
                if not isinstance(row.get("version"), int) or isinstance(row.get("version"), bool) or row["version"] < 1:
                    errors.append(f"{path}: positive content version required")
                vocab_ids = row.get("vocab_ids")
                if not isinstance(vocab_ids, list) or any(not _is_text(v) for v in vocab_ids):
                    errors.append(f"{path}: vocab_ids must be a list of stable IDs")
            elif name == "vocabulary":
                lemma = row.get("lemma_el")
                if not _is_text(lemma) or not _GREEK.search(lemma):
                    errors.append(f"{path}: missing Greek lemma")
                else:
                    norm = _same_text(lemma)
                    if norm in lemmas:
                        errors.append(f"{path}: duplicate lemma")
                    lemmas.add(norm)
                _lang_map(errors, f"{path}.translations", row.get("translations"), ("text",))
                if not _is_text(row.get("example_el")):
                    errors.append(f"{path}: example_el required")
                _lang_map(errors, f"{path}.example_translations", row.get("example_translations"), ("text",))
            elif name == "lessons":
                _lang_map(errors, f"{path}.title", row.get("title"), ("text",))
                _lang_map(errors, f"{path}.body", row.get("body"), ("text",))
                if not isinstance(row.get("question_ids"), list):
                    errors.append(f"{path}: question_ids list required")

    vocabulary_ids = {r.get("id") for r in vocabulary if isinstance(r, dict)}
    for index, row in enumerate(questions):
        if not isinstance(row, dict):
            continue
        fact = facts_by_id.get(row.get("fact_id"))
        if not fact:
            errors.append(f"questions[{index}]: unknown fact_id {row.get('fact_id')}")
        elif fact.get("topic") != row.get("topic"):
            errors.append(f"questions[{index}]: question/fact topic mismatch")
        for vid in row.get("vocab_ids", []) if isinstance(row.get("vocab_ids"), list) else []:
            if vid not in vocabulary_ids:
                errors.append(f"questions[{index}]: unknown vocab_id {vid}")
    for index, row in enumerate(lessons):
        if isinstance(row, dict) and isinstance(row.get("question_ids"), list):
            for qid in row["question_ids"]:
                if qid not in questions_by_id:
                    errors.append(f"lessons[{index}]: unknown question_id {qid}")
    return errors


def exam_eligible(row: dict, fact: dict, today: date | None = None) -> bool:
    """Safe pre-filter for future exam selection; server must still verify."""
    today = today or date.today()
    if row.get("status") != "published" or fact.get("status") != "published":
        return False
    for record in (row, fact):
        if record.get("freshness") not in FACT_KINDS:
            return False
        verified = _date(record.get("verified_at"))
        if verified is None or verified > today:
            return False
        for field in ("valid_until", "review_due"):
            value = record.get(field)
            if value is not None and (not _date(value) or today > _date(value)):
                return False
        if record.get("freshness") != "evergreen" and (
            not _date(record.get("valid_until")) or not _date(record.get("review_due"))
        ):
            return False
    return True


def read_bank(root: Path) -> tuple[object, list, list, list, list]:
    """Load explicitly named content trees, avoiding any unapproved user uploads."""
    with (root / "config.json").open(encoding="utf-8") as stream:
        config = json.load(stream)
    out: list[list] = []
    for directory in ("facts", "questions", "vocabulary", "lessons"):
        rows = []
        for path in sorted((root / directory).glob("*.json")):
            with path.open(encoding="utf-8") as stream:
                payload = json.load(stream)
            if not isinstance(payload, list):
                raise ValueError(f"{path}: expected JSON array")
            rows.extend(payload)
        out.append(rows)
    return (config, *out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate independently authored Cyprus Culture JSON")
    parser.add_argument("--root", type=Path, default=Path(__file__).parent / "content" / "culture")
    parser.add_argument("--today", help="ISO YYYY-MM-DD (test/repro only)")
    args = parser.parse_args()
    try:
        day = _date(args.today) if args.today else date.today()
        if day is None:
            raise ValueError("--today must be YYYY-MM-DD")
        errors = validate(*read_bank(args.root), today=day)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"culture validation failed: {exc}", file=sys.stderr)
        return 1
    for problem in errors:
        print(f"ERROR: {problem}", file=sys.stderr)
    if not errors:
        print("Culture content contract: PASS (structure, dates, links; not a human fact/rights review)")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
