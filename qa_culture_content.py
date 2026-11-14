"""CULT-01: standalone content contract QA (stdlib only, synthetic fixtures)."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

import culture_content as culture

ROOT = Path(__file__).parent
EXAMPLE = ROOT / "tests" / "fixtures" / "culture" / "sample_corpus.json"
CONFIG = ROOT / "content" / "culture" / "config.json"
TODAY = date(2026, 11, 15)


def fixture():
    obj = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    return (json.loads(CONFIG.read_text(encoding="utf-8")),
            obj["facts"], obj["questions"], obj["vocabulary"], obj["lessons"])


def validate(payload):
    return culture.validate(*payload, today=TODAY)


def assert_error(errors, needle):
    assert any(needle in issue for issue in errors), f"expected {needle!r} in {errors!r}"


class CultureContentContract(unittest.TestCase):
    def setUp(self):
        self.payload = copy.deepcopy(fixture())

    def test_synthetic_four_formats_are_valid_drafts(self):
        self.assertEqual(validate(self.payload), [])
        self.assertEqual({q["format"] for q in self.payload[2]}, culture.QUESTION_FORMATS)
        self.assertEqual({q["origin"] for q in self.payload[2]}, {"original"})

    def test_default_released_bank_starts_empty(self):
        root = ROOT / "content" / "culture"
        result = culture.read_bank(root)
        self.assertEqual(validate(result), [])
        self.assertTrue(all(not entries for entries in result[1:]))

    def test_reject_incomplete_topic_configuration(self):
        self.payload[0]["topics"].pop()
        assert_error(validate(self.payload), "14 official topic")
        self.payload = copy.deepcopy(fixture())
        self.payload[0]["exam_format_weights"]["NEGATIVE"] = 0
        assert_error(validate(self.payload), "positive integer")

    def test_stable_ids_and_cross_reference(self):
        self.payload[2][1]["id"] = self.payload[2][0]["id"]
        assert_error(validate(self.payload), "duplicate ID")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][0]["fact_id"] = "cyf_does_not_exist"
        assert_error(validate(self.payload), "unknown fact_id")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][0]["vocab_ids"] = ["cyv_missing_9999"]
        assert_error(validate(self.payload), "unknown vocab_id")
        self.payload = copy.deepcopy(fixture())
        self.payload[4][0]["question_ids"] = ["cyq_missing_9999"]
        assert_error(validate(self.payload), "unknown question_id")

    def test_all_four_answers_and_all_translations_required(self):
        self.payload[2][0]["options_el"] = ["Ένα", "Ένα", "Δύο", "Τρία"]
        assert_error(validate(self.payload), "duplicate answer options")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][0]["translations"]["ru"]["options"].pop()
        assert_error(validate(self.payload), "four translated options")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][0]["explanation"]["en"] = ""
        assert_error(validate(self.payload), "en text is missing")

    def test_negative_requires_exactly_one_false_at_correct_position(self):
        self.payload[2][1]["option_truth"] = [True, True, False, False]
        assert_error(validate(self.payload), "3 true and 1 false")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][1]["correct_index"] = 2
        assert_error(validate(self.payload), "3 true and 1 false")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][1].pop("option_truth")
        assert_error(validate(self.payload), "four explicit boolean truth values")

    def test_reject_exact_duplicate_prompt_and_non_normalized_greek(self):
        self.payload[2][1]["question_el"] = self.payload[2][0]["question_el"]
        assert_error(validate(self.payload), "duplicate question prompt")
        self.payload = copy.deepcopy(fixture())
        self.payload[2][0]["question_el"] = "Ποια πόλη ε\u0301χει;"
        assert_error(validate(self.payload), "NFC-normalized")

    def test_reviewed_and_published_require_documented_review(self):
        self.payload[2][0]["status"] = "published"
        assert_error(validate(self.payload), "human review metadata")
        review = {"editor": "TEST_ONLY", "at": "2026-11-14", "checks":
                  {name: True for name in culture.REVIEW_CHECKS}}
        self.payload[2][0]["review"] = review
        assert_error(validate(self.payload), "published question requires published reviewed fact")
        self.payload[1][0]["status"] = "published"
        self.payload[1][0]["review"] = copy.deepcopy(review)
        self.payload[1][0]["source"]["url"] = "https://www.gov.cy/"
        self.payload[2][0]["source"]["url"] = "https://www.gov.cy/"
        self.assertEqual(validate(self.payload), [])  # synthetic test-only content
        self.payload[2][0]["review"]["checks"]["facts"] = False
        assert_error(validate(self.payload), "editorial checks")

    def test_current_facts_have_a_freshness_window(self):
        self.payload[1][-1]["valid_until"] = None
        assert_error(validate(self.payload), "require review_due and valid_until")
        self.payload = copy.deepcopy(fixture())
        self.payload[1][-1]["review_due"] = "2026-09-30"
        assert_error(validate(self.payload), "review_due precedes verified_at")
        self.payload = copy.deepcopy(fixture())
        self.payload[1][-1]["status"] = "published"
        self.payload[1][-1]["review"] = {"editor": "TEST_ONLY", "at": "2026-11-14",
                                         "checks": {name: True for name in culture.REVIEW_CHECKS}}
        self.payload[1][-1]["review_due"] = "2026-11-14"
        assert_error(validate(self.payload), "published content is stale")

    def test_official_verbatim_requires_permission_and_official_source(self):
        self.payload[2][0]["origin"] = "official_published"
        assert_error(validate(self.payload), "confirmed reuse rights")

    def test_exam_selection_rejects_unreviewed_or_expired_facts(self):
        q, f = copy.deepcopy(self.payload[2][0]), copy.deepcopy(self.payload[1][0])
        self.assertFalse(culture.exam_eligible(q, f, TODAY))
        q["status"] = f["status"] = "published"
        self.assertTrue(culture.exam_eligible(q, f, TODAY))
        f["freshness"] = "periodic"
        self.assertFalse(culture.exam_eligible(q, f, TODAY))
        f["review_due"] = "2026-11-14"
        f["valid_until"] = "2027-01-01"
        self.assertFalse(culture.exam_eligible(q, f, TODAY))
        f["review_due"] = "2026-12-01"
        self.assertTrue(culture.exam_eligible(q, f, TODAY))
        q["status"] = "archived"
        self.assertFalse(culture.exam_eligible(q, f, TODAY))

    def test_directory_loader_uses_only_curated_json(self):
        config, facts, questions, vocabulary, lessons = self.payload
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.json").write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
            for directory, rows in (("facts", facts), ("questions", questions),
                                    ("vocabulary", vocabulary), ("lessons", lessons)):
                (root / directory).mkdir()
                (root / directory / "demo.json").write_text(
                    json.dumps(rows, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(validate(culture.read_bank(root)), [])
            (root / "questions" / "bad.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expected JSON array"):
                culture.read_bank(root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
