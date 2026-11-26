"""Bounded, immutable lesson evidence for optional learner feedback.

This is an audit of authoritative lesson outcomes, not another scoring/SRS
engine. Historical answers are never reconstructed. No audio is stored.
"""
import datetime as dt
import hashlib
import json

SCHEMA_VERSION = 1
RETENTION_DAYS = 30


def schema(db):
    db.execute("""CREATE TABLE IF NOT EXISTS lesson_evidence_runs (
        user_id TEXT NOT NULL, run_id TEXT NOT NULL,
        lesson_index INTEGER NOT NULL, chapter INTEGER NOT NULL,
        source_version TEXT NOT NULL, rubric_version TEXT NOT NULL,
        planned_count INTEGER NOT NULL, first_recorded_ordinal INTEGER NOT NULL,
        started_at TEXT NOT NULL, completed_at TEXT, completed_snapshot TEXT,
        PRIMARY KEY(user_id,run_id)
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS lesson_evidence_answers (
        user_id TEXT NOT NULL, run_id TEXT NOT NULL, ordinal INTEGER NOT NULL,
        request_id TEXT NOT NULL, evidence TEXT NOT NULL, created_at TEXT NOT NULL,
        PRIMARY KEY(user_id,run_id,ordinal),
        UNIQUE(user_id,request_id)
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS lesson_evidence_tombstones (
        user_id TEXT NOT NULL, run_id TEXT NOT NULL, deleted_at TEXT NOT NULL,
        PRIMARY KEY(user_id,run_id)
    )""")
    db.execute("""CREATE INDEX IF NOT EXISTS ix_lesson_evidence_completed
        ON lesson_evidence_runs(user_id,completed_at)""")


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _blocked(db, uid, run_id):
    return db.execute("""SELECT 1 FROM lesson_evidence_tombstones
        WHERE user_id=? AND run_id=?""", (uid, run_id)).fetchone() is not None


def _question(q):
    # Catalogue-owned bounded fields only. Never retain arbitrary client
    # snapshots, choices' hidden answer keys, account details, or audio.
    fields = ("id", "kind", "type", "family", "chapter", "lang", "direction",
              "prompt", "promptLang", "review", "activeGap", "gapCount",
              "dialogueGroup", "dialogueLines", "lines", "filledGaps", "typedAnswer")
    return {k: q[k] for k in fields if k in q}


def begin(db, uid, active):
    if not active or not active.get("runId"):
        return None
    run_id = active["runId"]
    if _blocked(db, uid, run_id):
        return None
    items = active.get("items", [])
    source = json.dumps([_question(q) for q in items], ensure_ascii=False,
                        sort_keys=True, separators=(",", ":"))
    version = str(active.get("generatorVersion", 0)) + ":" + hashlib.sha256(
        source.encode()).hexdigest()
    db.execute("""INSERT OR IGNORE INTO lesson_evidence_runs
        (user_id,run_id,lesson_index,chapter,source_version,rubric_version,
         planned_count,first_recorded_ordinal,started_at)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        (uid, run_id, active["index"], active["chapter"], version,
         "lexi-authoritative-v1", len(items), active.get("at", 0),
         active.get("startedAt") or _now()))
    return run_id


def record(db, uid, active, body, result, token):
    run_id = begin(db, uid, active)
    if not run_id:
        return
    row = db.execute("""SELECT completed_at FROM lesson_evidence_runs
        WHERE user_id=? AND run_id=?""", (uid, run_id)).fetchone()
    if row["completed_at"]:
        raise ValueError("lesson_evidence_already_completed")
    ordinal = active["at"]
    q = active["items"][ordinal]
    feedback = result.get("feedback") or {}
    # Only scored outcome facts from the server are trusted here. In
    # particular, a client's assisted/correct/explanation fields are ignored.
    authoritative = {k: feedback[k] for k in
        ("correct", "unverified", "skipped", "answer", "acceptedAnswers",
         "alternatives", "explanation", "orthographyNote", "category",
         "errorCategory", "answerErrorType", "clozeGreek", "clozeTranslation",
         "grammarTip", "accentGuidance", "finalNGuidance")
        if k in feedback}
    evidence = {
        "schema": SCHEMA_VERSION, "ordinal": ordinal,
        "question": _question(q), "cardId": q["id"],
        "printedChapter": q.get("chapter", active["chapter"]),
        "skill": q.get("family") or active["family"],
        "selected": body.get("selected") if body.get("action") == "answer" else None,
        "result": authoritative,
        "assisted": q.get("assisted") if type(q.get("assisted")) is bool else None,
        "hintAvailable": bool(q.get("hint")),
        "hintUsageKnown": type(q.get("assisted")) is bool,
        "skipped": body.get("action") == "skip" or bool(feedback.get("skipped")),
        "unverified": bool(feedback.get("unverified")),
        "firstSubmission": True,
    }
    db.execute("""INSERT INTO lesson_evidence_answers
        (user_id,run_id,ordinal,request_id,evidence,created_at)
        VALUES(?,?,?,?,?,?)""",
        (uid, run_id, ordinal, token, json.dumps(evidence, ensure_ascii=False), _now()))
    completed = feedback.get("lessonComplete")
    if completed:
        rows = db.execute("""SELECT evidence FROM lesson_evidence_answers
            WHERE user_id=? AND run_id=? ORDER BY ordinal""", (uid, run_id)).fetchall()
        metadata = db.execute("""SELECT * FROM lesson_evidence_runs
            WHERE user_id=? AND run_id=?""", (uid, run_id)).fetchone()
        snapshot = {
            "schema": SCHEMA_VERSION, "runId": run_id,
            "lessonIndex": metadata["lesson_index"],
            "chapter": metadata["chapter"], "sourceVersion": metadata["source_version"],
            "rubricVersion": metadata["rubric_version"],
            "summary": dict(completed), "evidence": [json.loads(r["evidence"]) for r in rows],
            "evidenceComplete": (metadata["first_recorded_ordinal"] == 0 and
                                 len(rows) == metadata["planned_count"]),
            "expectedEvidenceCount": metadata["planned_count"],
            "retentionDays": RETENTION_DAYS,
        }
        db.execute("""UPDATE lesson_evidence_runs
            SET completed_at=?,completed_snapshot=?
            WHERE user_id=? AND run_id=? AND completed_at IS NULL""",
            (completed.get("finishedAt") or _now(),
             json.dumps(snapshot, ensure_ascii=False), uid, run_id))


def get_snapshot(db, uid, run_id):
    """Return one immutable completed snapshot owned by uid, or None."""
    row = db.execute("""SELECT completed_snapshot FROM lesson_evidence_runs
        WHERE user_id=? AND run_id=? AND completed_at IS NOT NULL""",
        (uid, run_id)).fetchone()
    return json.loads(row["completed_snapshot"]) if row and row["completed_snapshot"] else None


def list_runs(db, uid, limit=20):
    rows = db.execute("""SELECT run_id,lesson_index,chapter,completed_at,completed_snapshot
        FROM lesson_evidence_runs WHERE user_id=? AND completed_at IS NOT NULL
        ORDER BY completed_at DESC,run_id DESC LIMIT ?""",
        (uid, max(1, min(100, int(limit))))).fetchall()
    return [{"runId": r["run_id"], "lessonIndex": r["lesson_index"],
             "chapter": r["chapter"], "completedAt": r["completed_at"],
             "evidenceComplete": json.loads(r["completed_snapshot"])["evidenceComplete"]}
            for r in rows]


def forget(db, uid, run_id):
    """Delete retained text while keeping a resurrection-prevention marker."""
    db.execute("""INSERT OR IGNORE INTO lesson_evidence_tombstones
        (user_id,run_id,deleted_at) VALUES(?,?,?)""", (uid, run_id, _now()))
    db.execute("DELETE FROM lesson_evidence_answers WHERE user_id=? AND run_id=?", (uid, run_id))
    db.execute("DELETE FROM lesson_evidence_runs WHERE user_id=? AND run_id=?", (uid, run_id))


def prune(db, uid, now=None):
    cutoff = ((now or dt.datetime.now(dt.timezone.utc)) -
              dt.timedelta(days=RETENTION_DAYS)).isoformat(timespec="seconds")
    rows = db.execute("""SELECT run_id FROM lesson_evidence_runs
        WHERE user_id=? AND COALESCE(completed_at,started_at)<?""", (uid, cutoff)).fetchall()
    for row in rows:
        forget(db, uid, row["run_id"])
    return len(rows)
