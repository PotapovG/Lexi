"""Content-only regression check for CULT-02 batch 01.

Checks authoring structure and coverage, NOT Greek quality, truth or rights.
"""
from pathlib import Path
from collections import Counter

import culture_content

root=Path(__file__).parent / "content" / "culture"
payload=culture_content.read_bank(root)
config, facts, questions, vocabulary, lessons=payload
issues=culture_content.validate(*payload)
assert not issues, "Culture schema errors:\n" + "\n".join(issues)
batch_questions=[q for q in questions if q["id"].startswith("cyq_")]
batch_facts=[f for f in facts if f["id"].startswith("cyf_")]
assert len(batch_questions)>=20 and len(batch_facts)>=20, (len(batch_questions),len(batch_facts))
topics=Counter(q["topic"] for q in batch_questions)
assert set(topics)==set(culture_content.TOPIC_CODES), topics
assert set(q["format"] for q in batch_questions)==culture_content.QUESTION_FORMATS
fact_ids=[q["fact_id"] for q in batch_questions]
assert len(fact_ids)==len(set(fact_ids)), "Unexpected same fact in initial batch"
assert all(q["status"]=="draft" for q in batch_questions), "No automated editorial publication"
assert all(f["status"]=="draft" for f in batch_facts), "No automated editorial publication"
assert all(not culture_content.exam_eligible(q, next(f for f in batch_facts if f["id"]==q["fact_id"])) for q in batch_questions)
print("PASS CULT-02 initial batch:",len(batch_questions),"draft questions,",len(batch_facts),
      "draft facts;",len(topics),"topics;",dict(Counter(q["format"] for q in batch_questions)))
