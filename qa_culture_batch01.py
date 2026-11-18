"""CULT-02 first content-batch regression (facts/coverage, NOT human review)."""
from collections import Counter
from pathlib import Path
import json

import culture_content

root = Path(__file__).parent / "content" / "culture"
config, facts, questions, vocabulary, lessons = culture_content.read_bank(root)
errors = culture_content.validate(config, facts, questions, vocabulary, lessons)
assert not errors, "Culture schema errors:\n" + "\n".join(errors)

def batch_records(folder):
    out = []
    for path in sorted((root / folder).glob("20261114_batch01*.json")):
        out.extend(json.loads(path.read_text(encoding="utf-8")))
    return out

batch_facts = batch_records("facts")
batch_questions = batch_records("questions")
assert len(batch_questions) == len(batch_facts) == 20
assert set(q["topic"] for q in batch_questions) == set(culture_content.TOPIC_CODES)
assert set(q["format"] for q in batch_questions) == culture_content.QUESTION_FORMATS
assert len({q["id"] for q in batch_questions}) == 20
assert len({q["fact_id"] for q in batch_questions}) == 20
assert all(q["origin"] == "original" for q in batch_questions)
assert all(q["source"]["url"].startswith("https://") for q in batch_questions)

by_id = {f["id"]: f for f in batch_facts}
assert all(q["fact_id"] in by_id for q in batch_questions)
published = [q for q in batch_questions if q["status"] == "published"]
assert all(culture_content.exam_eligible(q, by_id[q["fact_id"]]) for q in published)
# Draft records are intentionally not learner-visible. Later human-approved
# publication must not break this test or require a test rewrite.
print("PASS CULT-02 initial batch:",len(batch_questions),"questions /",
      len(batch_facts),"facts /",len({q["topic"] for q in batch_questions}),
      "topics /",len(published),"published;",
      dict(Counter(q["format"] for q in batch_questions)))
