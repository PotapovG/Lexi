"""Optional, owner-scoped durable AI jobs; ordinary Lexi never depends on it.

SQLite reserves a bounded budget before the connection is closed for the
upstream call. Ambiguous calls are never automatically paid for a second time.
No acoustic score, second SRS, provider tools or automatic rollout.
"""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import secrets
import sqlite3
import threading
import time

import ai_audio
import ai_curriculum as curriculum
import lesson_evidence
from ai_provider import (OpenAIProvider, ProviderError, TEXT_MODEL, AUDIO_MODEL,
                         text_cost, audio_cost, audio_usage_cost, reserve_text_cost)

PROMPT_VERSION = "lexi-ai-prompt-1"
JOB_TTL = 3600
TEXT_RETENTION = 30 * 86400
TERMINAL = ("succeeded", "failed", "unknown", "cancelled", "deleted")
ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{8,160}$")
MAINTENANCE_BATCH = 100

class AIError(Exception):
    def __init__(self, code, status=400):
        super().__init__(code)
        self.code, self.status = code, status

def _dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def _hash(value):
    return hashlib.sha256(_dump(value).encode()).hexdigest()

def _id(value):
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise AIError("invalid_operation")
    return value

def _usd(value, fallback):
    if value is None or (isinstance(value,str) and not value.strip()):
        return fallback
    try:
        x = float(value)
        amount = x * 1_000_000
        return int(amount) if math.isfinite(amount) and x >= 0 else 0
    except (TypeError, ValueError, OverflowError):
        return 0


def _usage_metadata(usage):
    """Keep numerical accounting facts, never provider text or arbitrary fields."""
    if not isinstance(usage, dict):
        return None
    result = {}
    model = usage.get("providerModel")
    if isinstance(model,str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,160}",model):
        result["providerModel"] = model
    if usage.get("type") in ("duration", "tokens"):
        result["type"] = usage["type"]
    for key in ("input_tokens", "output_tokens", "total_tokens", "seconds"):
        value = usage.get(key)
        if type(value) in (int, float):
            try:
                if math.isfinite(value) and value >= 0:
                    result[key] = value
            except (TypeError, ValueError, OverflowError):
                pass
    for key, allowed in (("input_tokens_details", ("cached_tokens", "cache_write_tokens", "audio_tokens", "text_tokens")),
                         ("output_tokens_details", ("reasoning_tokens", "audio_tokens", "text_tokens"))):
        details = usage.get(key)
        if isinstance(details, dict):
            result[key] = {name: details[name] for name in allowed
                           if type(details.get(name)) is int and details[name] >= 0}
    return result

@dataclass
class Config:
    stage: str = "disabled"
    key: str = field(default="", repr=False)
    features: frozenset = field(default_factory=frozenset)
    cohort: frozenset = field(default_factory=frozenset)
    speech_validated: bool = False
    month_limit: int = 10_000_000
    day_limit: int = 500_000
    per_job_limit: int = 100_000
    concurrency: int = 2
    queue_limit: int = 16
    daily_jobs: int = 40
    text_model: str = TEXT_MODEL
    audio_model: str = AUDIO_MODEL
    timeout: int = 30

    @classmethod
    def environment(cls):
        return cls(
            stage=os.getenv("LEXI_AI_STAGE", "disabled"),
            key=os.getenv("LEXI_OPENAI_API_KEY", ""),
            features=frozenset(filter(None, os.getenv("LEXI_AI_FEATURES", "").split(","))),
            cohort=frozenset(filter(None, os.getenv("LEXI_AI_COHORT", "").split(","))),
            speech_validated=os.getenv("LEXI_AI_SPEECH_VALIDATED") == "1",
            month_limit=_usd(os.getenv("LEXI_AI_MONTH_USD"), 10_000_000),
            day_limit=_usd(os.getenv("LEXI_AI_DAY_USD"), 500_000),
            per_job_limit=_usd(os.getenv("LEXI_AI_JOB_USD"), 100_000))

    def permits(self, uid, kind):
        if self.stage not in ("internal", "pilot", "enabled") or not self.key:
            return False
        if self.stage != "enabled" and uid not in self.cohort:
            return False
        feature = "dialogue" if kind in ("dialogue", "dialogue_edit") else kind
        return feature in self.features and (feature == "summary" or self.speech_validated)

def schema(db):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS ai_owner_generation(
      owner TEXT PRIMARY KEY,generation INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS ai_jobs(
      id TEXT PRIMARY KEY,owner TEXT NOT NULL,operation_id TEXT NOT NULL,
      kind TEXT NOT NULL,run_id TEXT NOT NULL,conversation_id TEXT,
      fingerprint TEXT NOT NULL,cache_key TEXT,status TEXT NOT NULL,
      payload TEXT,result TEXT,error_code TEXT,generation INTEGER NOT NULL,
      reserved INTEGER NOT NULL,actual INTEGER,usage TEXT,
      created REAL NOT NULL,updated REAL NOT NULL,lease_until REAL,
      worker_id TEXT,reported INTEGER NOT NULL DEFAULT 0,
      UNIQUE(owner,operation_id),UNIQUE(owner,cache_key));
    CREATE INDEX IF NOT EXISTS ai_jobs_queue ON ai_jobs(status,created);
    CREATE INDEX IF NOT EXISTS ai_jobs_budget ON ai_jobs(created,owner);
    CREATE TABLE IF NOT EXISTS ai_conversations(
      id TEXT PRIMARY KEY,owner TEXT NOT NULL,operation_id TEXT NOT NULL,
      run_id TEXT NOT NULL,state TEXT NOT NULL,status TEXT NOT NULL,
      revision INTEGER NOT NULL DEFAULT 0,pending_job TEXT,
      created REAL NOT NULL,updated REAL NOT NULL,
      UNIQUE(owner,operation_id));
    CREATE TABLE IF NOT EXISTS ai_feedback_reports(
      owner TEXT NOT NULL,job_id TEXT NOT NULL,reason TEXT NOT NULL,created REAL NOT NULL,
      PRIMARY KEY(owner,job_id));
    CREATE TABLE IF NOT EXISTS ai_reading_edits(
      owner TEXT NOT NULL,operation_id TEXT NOT NULL,job_id TEXT NOT NULL,
      fingerprint TEXT NOT NULL,revision INTEGER NOT NULL,created REAL NOT NULL,
      PRIMARY KEY(owner,operation_id));
    CREATE TABLE IF NOT EXISTS ai_operation_aliases(
      owner TEXT NOT NULL,operation_id TEXT NOT NULL,job_id TEXT NOT NULL,created REAL NOT NULL,
      PRIMARY KEY(owner,operation_id));
    CREATE INDEX IF NOT EXISTS ai_jobs_retention ON ai_jobs(created,status);
    CREATE INDEX IF NOT EXISTS ai_conversations_retention ON ai_conversations(created,status);
    """)

class Service:
    def __init__(self, connect, app, data_directory, config=None, provider=None,
                 clock=time.time, start_workers=False):
        self.connect, self.app, self.clock = connect, app, clock
        self.config = config or Config.environment()
        self.provider = provider or OpenAIProvider(
            self.config.key, self.config.text_model, self.config.audio_model,
            self.config.timeout)
        self.spool = Path(data_directory) / "ai-spool"
        self.stop = threading.Event()
        self.worker_id = secrets.token_hex(16)
        self.threads = []
        with self.db() as db:
            schema(db)
            lesson_evidence.schema(db)
        if start_workers:
            # Retention is independent of paid-feature availability and API keys.
            thread = threading.Thread(target=self._maintenance_loop, daemon=True)
            thread.start()
            self.threads.append(thread)
        if start_workers and self.config.stage != "disabled" and self.config.key:
            for _ in range(max(1, min(2, self.config.concurrency))):
                thread = threading.Thread(target=self._loop, daemon=True)
                thread.start()
                self.threads.append(thread)

    @contextmanager
    def db(self, write=False):
        db = self.connect()
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _permission(self, uid, kind):
        if not self.config.permits(uid, kind):
            raise AIError("ai_unavailable", 503)

    def capabilities(self, uid):
        return {"enabled": any(self.config.permits(uid, k) for k in ("summary","reading","dialogue")),
                "features": {k: self.config.permits(uid,k) for k in ("summary","reading","dialogue")},
                "pronunciation": False, "audioDecoder": ai_audio.available(),
                "limits": {"uploadBytes": ai_audio.MAX_BYTES, "readingSeconds": 90,
                           "dialogueSeconds": 45, "dialogueTurns": [4,5]},
                "textRetentionDays": 30, "audioRetentionHours": 1}

    def _owner_generation(self, uid):
        with self.db() as db:
            row = db.execute("SELECT generation FROM ai_owner_generation WHERE owner=?", (uid,)).fetchone()
        return row[0] if row else 0

    def _require_generation(self, db, uid, expected):
        row = db.execute("SELECT generation FROM ai_owner_generation WHERE owner=?", (uid,)).fetchone()
        generation = row[0] if row else 0
        if expected is not None and generation != expected:
            raise AIError("operation_deleted", 410)
        return generation

    def _require_evidence(self, db, uid, run_id):
        cutoff=dt.datetime.fromtimestamp(self.clock()-TEXT_RETENTION,dt.timezone.utc).isoformat(timespec="seconds")
        row=db.execute("""SELECT 1 FROM lesson_evidence_runs
            WHERE user_id=? AND run_id=? AND completed_at>?
            AND completed_snapshot IS NOT NULL""",(uid,run_id,cutoff)).fetchone()
        if not row:
            raise AIError("lesson_evidence_unavailable",404)

    def _expired(self, row):
        return row["status"] == "deleted" or row["created"] <= self.clock() - TEXT_RETENTION

    def _context(self, uid, run_id, lang):
        run_id = _id(run_id)
        with self.db(True) as db:
            lesson_evidence.prune(db, uid, now=dt.datetime.fromtimestamp(self.clock(), dt.timezone.utc))
            snapshot = lesson_evidence.get_snapshot(db, uid, run_id)
        if not snapshot:
            raise AIError("lesson_evidence_unavailable", 404)
        return curriculum.build(self.app, snapshot, lang)

    def options(self, uid, run_id, lang):
        context = self._context(uid, run_id, lang)
        if not any(self.config.permits(uid,k) for k in ("summary","reading","dialogue")):
            raise AIError("ai_unavailable", 503)
        allowed_turns = [count for count in (4, 5) if len(context["questions"]) >= count]
        first_questions = {}
        for question in context["questions"]:
            first_questions.setdefault(question["sourceId"], question)
        scenarios = [{"id": material["id"], "firstQuestion": first_questions[material["id"]]["text"]}
                     for material in context["readings"] if material["id"] in first_questions]
        return {"runId":run_id, "chapter":context["chapter"], "scopeVersion":context["hash"],
                "readings":context["readings"], "dialogues":scenarios[:6] if allowed_turns else [],
                "dialogueTurns":allowed_turns,
                "existingSummary":self._existing_summary(uid,run_id,lang),
                "readingJobs":self._reading_jobs(uid,run_id,lang),
                "conversations":self.list_conversations(uid,run_id)}

    def _existing_summary(self, uid, run_id, lang):
        with self.db() as db:
            rows = db.execute("""SELECT * FROM ai_jobs WHERE owner=? AND run_id=?
                AND kind='summary' AND status!='deleted' AND created>?
                ORDER BY created""", (uid,run_id,self.clock()-TEXT_RETENTION)).fetchall()
        for row in rows:
            payload = json.loads(row["payload"] or "{}")
            if payload.get("lang")==lang:
                return self._public_job(row)
        return None

    def _reading_jobs(self, uid, run_id, lang):
        with self.db() as db:
            rows = db.execute("""SELECT * FROM ai_jobs WHERE owner=? AND run_id=?
                AND kind='reading' AND status!='deleted' AND created>?
                ORDER BY created DESC,rowid DESC""", (uid,run_id,self.clock()-TEXT_RETENTION)).fetchall()
        result, seen = [], set()
        for row in rows:
            payload = json.loads(row["payload"] or "{}")
            reading_id = payload.get("readingId")
            if payload.get("lang") != lang or not reading_id or reading_id in seen:
                continue
            seen.add(reading_id)
            result.append(self._public_job(row))
            if len(result) >= 20:
                break
        return result

    def _public_job(self, row):
        deleted = self._expired(row)
        payload = json.loads(row["payload"] or "{}") if not deleted else {}
        return {"id":row["id"],"kind":row["kind"],"runId":row["run_id"],
                "conversationId":row["conversation_id"],"status":"deleted" if deleted else row["status"],
                "readingId":payload.get("readingId") if row["kind"]=="reading" else None,
                "result":json.loads(row["result"]) if row["result"] and not deleted else None,
                "error":row["error_code"] if not deleted else None,
                "reported":bool(row["reported"]) if not deleted else False,
                "usageState":"known" if row["actual"] is not None else
                    "reserved" if row["status"] in ("queued","running") and not deleted else "unknown"}

    def get_job(self, uid, job_id):
        with self.db() as db:
            row=db.execute("SELECT * FROM ai_jobs WHERE id=? AND owner=?",(_id(job_id),uid)).fetchone()
        if not row:
            raise AIError("job_not_found",404)
        return self._public_job(row)

    def _operation_job(self, db, uid, operation_id):
        row=db.execute("SELECT * FROM ai_jobs WHERE owner=? AND operation_id=?",
                       (uid,operation_id)).fetchone()
        if row:
            return row
        return db.execute("""SELECT j.* FROM ai_operation_aliases a
            JOIN ai_jobs j ON j.id=a.job_id AND j.owner=a.owner
            WHERE a.owner=? AND a.operation_id=?""",(uid,operation_id)).fetchone()

    def _alias_existing_job(self, uid, operation_id, job_id, generation):
        with self.db(True) as db:
            self._require_generation(db,uid,generation)
            prior=self._operation_job(db,uid,operation_id)
            if prior and prior["id"]!=job_id:
                raise AIError("operation_conflict",409)
            if (db.execute("SELECT 1 FROM ai_conversations WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()
                    or db.execute("SELECT 1 FROM ai_reading_edits WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()):
                raise AIError("operation_conflict",409)
            row=db.execute("SELECT * FROM ai_jobs WHERE owner=? AND id=?",(uid,job_id)).fetchone()
            if not row or self._expired(row):
                raise AIError("operation_deleted",410)
            if not prior:
                db.execute("INSERT INTO ai_operation_aliases VALUES(?,?,?,?)",
                           (uid,operation_id,job_id,self.clock()))
            return self._public_job(row)

    def find_operation(self, uid, operation_id):
        operation_id = _id(operation_id)
        with self.db() as db:
            row=self._operation_job(db,uid,operation_id)
            if row:
                return self._public_job(row)
            conversation=db.execute("SELECT * FROM ai_conversations WHERE owner=? AND operation_id=?",
                                    (uid,operation_id)).fetchone()
            if conversation:
                return self._public_conversation(conversation)
            edited=db.execute("""SELECT j.* FROM ai_reading_edits e
                JOIN ai_jobs j ON j.id=e.job_id AND j.owner=e.owner
                WHERE e.owner=? AND e.operation_id=?""",(uid,operation_id)).fetchone()
        return self._public_job(edited) if edited else None

    def summary(self, uid, run_id, lang, operation_id):
        self._permission(uid,"summary")
        run_id, operation_id = _id(run_id), _id(operation_id)
        generation = self._owner_generation(uid)
        replay = self._replay(uid,operation_id,"summary",run_id,{"lang":lang})
        if replay:
            return replay
        existing=self._existing_summary(uid,run_id,lang)
        if existing:
            return self._alias_existing_job(uid,operation_id,existing["id"],generation)
        context=self._context(uid,run_id,lang)
        if not context["evidence"]:
            raise AIError("lesson_evidence_unavailable",422)
        compact={k:context[k] for k in ("version","interfaceLanguage","chapter",
                 "sourceVersion","rubricVersion","evidenceComplete","evidence","eligibleTargets","hash")}
        payload={"context":compact,"lang":lang,"promptVersion":PROMPT_VERSION,
                 "model":self.config.text_model}
        reserve=reserve_text_cost(len((_dump(compact)+curriculum.SUMMARY_INSTRUCTIONS+_dump(curriculum.summary_schema(compact))).encode())+512)
        return self._enqueue(uid,operation_id,"summary",run_id,payload,reserve,
                             cache_key="summary:"+_hash([run_id,lang,context["hash"],PROMPT_VERSION]),
                             expected_generation=generation)

    def _replay(self,uid,operation_id,kind,run_id,fields,conversation_id=None):
        with self.db() as db:
            operation_id = _id(operation_id)
            row=self._operation_job(db,uid,operation_id)
            if not row and (
                db.execute("SELECT 1 FROM ai_conversations WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()
                or db.execute("SELECT 1 FROM ai_reading_edits WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()):
                raise AIError("operation_conflict",409)
        if not row:
            return None
        if self._expired(row):
            raise AIError("operation_deleted",410)
        payload=json.loads(row["payload"] or "{}")
        if (row["kind"]!=kind or (run_id is not None and row["run_id"]!=run_id)
                or row["conversation_id"]!=conversation_id
                or any(payload.get(key)!=value for key,value in fields.items())):
            raise AIError("operation_conflict",409)
        return self._public_job(row)

    def _budget(self, db, uid, amount):
        now=self.clock()
        current=dt.datetime.fromtimestamp(now,dt.timezone.utc)
        month=current.replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp()
        day=current.replace(hour=0,minute=0,second=0,microsecond=0).timestamp()
        total=db.execute("SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM ai_jobs WHERE created>=?",
                         (month,)).fetchone()[0]
        daily=db.execute("""SELECT COALESCE(SUM(COALESCE(actual,reserved)),0),COUNT(*)
            FROM ai_jobs WHERE owner=? AND created>=?""",(uid,day)).fetchone()
        queue=db.execute("SELECT COUNT(*) FROM ai_jobs WHERE status IN ('queued','running')").fetchone()[0]
        account_queue=db.execute("""SELECT COUNT(*) FROM ai_jobs
            WHERE owner=? AND status IN ('queued','running')""",(uid,)).fetchone()[0]
        if amount>self.config.per_job_limit or total+amount>self.config.month_limit or daily[0]+amount>self.config.day_limit:
            raise AIError("ai_budget_limit",429)
        if daily[1]>=self.config.daily_jobs:
            raise AIError("ai_daily_limit",429)
        if queue>=self.config.queue_limit or account_queue>=2:
            raise AIError("ai_queue_full",429)

    def _enqueue(self, uid, operation_id, kind, run_id, payload, reserve,
                 cache_key=None, conversation_id=None, expected_revision=None,
                 expected_generation=None):
        self._permission(uid,kind)
        operation_id=_id(operation_id)
        comparable={k:v for k,v in payload.items() if k!="audioPath"}
        fingerprint=_hash([kind,run_id,conversation_id,comparable])
        now=self.clock()
        if type(reserve) is not int or reserve < 0:
            raise AIError("ai_usage_unavailable",503)
        with self.db(True) as db:
            generation = self._require_generation(db,uid,expected_generation)
            if expected_generation is not None:
                self._require_evidence(db,uid,run_id)
            existing=self._operation_job(db,uid,operation_id)
            if existing:
                if self._expired(existing):
                    raise AIError("operation_deleted",410)
                if existing["fingerprint"]!=fingerprint:
                    raise AIError("operation_conflict",409)
                return self._public_job(existing)
            if (db.execute("SELECT 1 FROM ai_reading_edits WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()
                    or db.execute("SELECT 1 FROM ai_conversations WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()):
                raise AIError("operation_conflict",409)
            if cache_key:
                existing=db.execute("SELECT * FROM ai_jobs WHERE owner=? AND cache_key=?",(uid,cache_key)).fetchone()
                if existing:
                    if self._expired(existing):
                        raise AIError("operation_deleted",410)
                    db.execute("INSERT INTO ai_operation_aliases VALUES(?,?,?,?)",
                               (uid,operation_id,existing["id"],self.clock()))
                    return self._public_job(existing)
            if conversation_id:
                conversation=db.execute("SELECT * FROM ai_conversations WHERE id=? AND owner=?",
                                        (conversation_id,uid)).fetchone()
                if not conversation:
                    raise AIError("conversation_not_found",404)
                if conversation["revision"]!=expected_revision or conversation["pending_job"]:
                    raise AIError("conversation_conflict",409)
                allowed_status = ("active","completed") if kind=="dialogue_edit" else ("active",)
                if self._expired(conversation) or conversation["status"] not in allowed_status:
                    raise AIError("conversation_finished",409)
                attempts=db.execute("SELECT COUNT(*) FROM ai_jobs WHERE conversation_id=?",
                                    (conversation_id,)).fetchone()[0]
                if attempts>=12:
                    raise AIError("conversation_attempt_limit",429)
            self._budget(db,uid,reserve)
            db.execute("INSERT OR IGNORE INTO ai_owner_generation(owner) VALUES(?)",(uid,))
            job_id=secrets.token_hex(16)
            db.execute("""INSERT INTO ai_jobs(id,owner,operation_id,kind,run_id,conversation_id,
                fingerprint,cache_key,status,payload,generation,reserved,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (job_id,uid,operation_id,kind,run_id,conversation_id,fingerprint,cache_key,
                 "queued",_dump(payload),generation,reserve,now,now))
            if conversation_id:
                db.execute("UPDATE ai_conversations SET pending_job=?,updated=? WHERE id=?",
                           (job_id,now,conversation_id))
            row=db.execute("SELECT * FROM ai_jobs WHERE id=?",(job_id,)).fetchone()
        return self._public_job(row)

    def _start_replay(self, row, run_id, lang, scenario_id, turns):
        if self._expired(row):
            raise AIError("operation_deleted",410)
        state=json.loads(row["state"])
        if (row["run_id"]!=run_id or state.get("scenarioId")!=scenario_id
                or state.get("targetTurns")!=turns
                or state.get("context",{}).get("interfaceLanguage")!=lang):
            raise AIError("operation_conflict",409)
        return self._public_conversation(row)

    def start_conversation(self, uid, run_id, lang, scenario_id, turns, operation_id):
        self._permission(uid,"dialogue")
        run_id, operation_id = _id(run_id), _id(operation_id)
        generation = self._owner_generation(uid)
        if type(turns) is not int or turns not in (4,5):
            raise AIError("invalid_turn_limit")
        with self.db() as db:
            existing=db.execute("SELECT * FROM ai_conversations WHERE owner=? AND operation_id=?",
                                (uid,operation_id)).fetchone()
            if existing:
                return self._start_replay(existing,run_id,lang,scenario_id,turns)
        context=self._context(uid,run_id,lang)
        questions=context["questions"]
        first=next((x for x in questions if x["sourceId"]==scenario_id),None)
        if not first or len(questions)<turns:
            raise AIError("scenario_unavailable",422)
        compact={k:context[k] for k in ("version","interfaceLanguage","chapter",
                  "hash","questions","allowedGreekVocabulary","claims")}
        state={"context":compact,"scenarioId":scenario_id,"targetTurns":turns,
               "question":first,"history":[],"asked":[first["id"]],"revision":0,
               "assisted":False,"started":self.clock()}
        with self.db(True) as db:
            self._require_generation(db,uid,generation)
            self._require_evidence(db,uid,run_id)
            row=db.execute("SELECT * FROM ai_conversations WHERE owner=? AND operation_id=?",
                           (uid,operation_id)).fetchone()
            if row:
                return self._start_replay(row,run_id,lang,scenario_id,turns)
            if (self._operation_job(db,uid,operation_id)
                    or db.execute("SELECT 1 FROM ai_reading_edits WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()):
                raise AIError("operation_conflict",409)
            count=db.execute("SELECT COUNT(*) FROM ai_conversations WHERE owner=? AND created>?",
                             (uid,self.clock()-86400)).fetchone()[0]
            if count>=10:
                raise AIError("ai_daily_limit",429)
            cid=secrets.token_hex(16)
            db.execute("""INSERT INTO ai_conversations
              (id,owner,operation_id,run_id,state,status,created,updated)
              VALUES(?,?,?,?,?,'active',?,?)""",
              (cid,uid,operation_id,run_id,_dump(state),self.clock(),self.clock()))
            row=db.execute("SELECT * FROM ai_conversations WHERE id=?",(cid,)).fetchone()
        return self._public_conversation(row)

    def _public_conversation(self,row):
        deleted = self._expired(row)
        state=json.loads(row["state"]) if not deleted else {}
        status="deleted" if deleted else row["status"]
        return {"id":row["id"],"runId":row["run_id"],"status":status,
                "revision":row["revision"],"pendingJob":row["pending_job"] if not deleted else None,
                "targetTurns":state.get("targetTurns",5),"history":state.get("history",[]),
                "question":state.get("question") if status=="active" else None,
                "turnCount":len(state.get("history",[])),
                "scopeVersion":state.get("context",{}).get("hash")}

    def get_conversation(self,uid,cid):
        with self.db() as db:
            row=db.execute("SELECT * FROM ai_conversations WHERE owner=? AND id=?",(uid,_id(cid))).fetchone()
        if not row:
            raise AIError("conversation_not_found",404)
        return self._public_conversation(row)

    def list_conversations(self,uid,run_id):
        with self.db() as db:
            rows=db.execute("""SELECT * FROM ai_conversations WHERE owner=? AND run_id=?
                AND status!='deleted' AND created>? ORDER BY created DESC LIMIT 10""",
                (uid,run_id,self.clock()-TEXT_RETENTION)).fetchall()
        return [self._public_conversation(row) for row in rows]

    def _conversation_payload(self,uid,cid,revision,allow_completed=False):
        with self.db() as db:
            row=db.execute("SELECT * FROM ai_conversations WHERE owner=? AND id=?",(uid,_id(cid))).fetchone()
        if not row:
            raise AIError("conversation_not_found",404)
        if self._expired(row):
            raise AIError("conversation_deleted",410)
        allowed_status=("active","completed") if allow_completed else ("active",)
        if row["status"] not in allowed_status:
            raise AIError("conversation_finished",409)
        if row["revision"]!=revision:
            raise AIError("conversation_conflict",409)
        state=json.loads(row["state"])
        if self.clock()-state["started"]>1800:
            raise AIError("conversation_expired",409)
        return row,state

    def upload(self,uid,kind,run_id,lang,operation_id,data,mime,
               reading_id=None,conversation_id=None,revision=0):
        if kind not in ("reading","dialogue"):
            raise AIError("invalid_kind")
        self._permission(uid,kind)
        _id(operation_id)
        generation = self._owner_generation(uid)
        prior=self._replay(uid,operation_id,kind,run_id,
            {"audioHash":hashlib.sha256(data).hexdigest(),
             "audioMime":mime.split(";",1)[0].strip().lower(),
             **({"readingId":reading_id,"lang":lang} if kind=="reading" else
                {"conversationRevision":revision})},conversation_id)
        if prior:
            return prior
        if len(data)>ai_audio.MAX_BYTES:
            raise AIError("audio_size",413)
        if kind=="reading":
            context=self._context(uid,run_id,lang)
            reading=next((x for x in context["readings"] if x["id"]==reading_id),None)
            if not reading:
                raise AIError("reading_unavailable",422)
            payload={"reference":reading["text"],"readingId":reading_id,
                     "scopeVersion":context["hash"],"sourceVersion":reading["sourceVersion"],"lang":lang}
        else:
            row,state=self._conversation_payload(uid,conversation_id,revision)
            if row["run_id"]!=run_id:
                raise AIError("conversation_conflict",409)
            payload={"conversation":state,"conversationRevision":revision,
                     "lang":state["context"]["interfaceLanguage"]}
        self.spool.mkdir(mode=0o700,parents=True,exist_ok=True)
        os.chmod(self.spool,0o700)
        filename=self.spool/(secrets.token_hex(16)+".audio")
        fd=os.open(filename,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        try:
            with os.fdopen(fd,"wb") as out:
                out.write(data)
            info=ai_audio.validate_file(filename,mime,90 if kind=="reading" else 45)
            payload.update({"audioPath":str(filename),"audioMime":info["mime"],
                            "audioExtension":info["extension"],"audioSeconds":info["seconds"],
                            "audioHash":hashlib.sha256(data).hexdigest()})
            reserve=audio_cost(info["seconds"])
            if kind=="dialogue":
                reserve+=reserve_text_cost(len((_dump(state)+curriculum.DIALOGUE_INSTRUCTIONS).encode())+24000)
            result=self._enqueue(uid,operation_id,kind,run_id,payload,reserve,
                                 conversation_id=conversation_id,expected_revision=revision,
                                 expected_generation=generation)
            with self.db() as db:
                kept=db.execute("SELECT payload FROM ai_jobs WHERE id=?",(result["id"],)).fetchone()
            if json.loads(kept["payload"] or "{}").get("audioPath")!=str(filename):
                filename.unlink(missing_ok=True)
            return result
        except ValueError as error:
            filename.unlink(missing_ok=True)
            raise AIError(str(error),422) from None
        except Exception:
            filename.unlink(missing_ok=True)
            raise

    def edit_transcript(self,uid,job_id,text,revision,operation_id):
        if not isinstance(text,str) or not 1<=len(text.strip())<=2000:
            raise AIError("invalid_transcript")
        operation_id = _id(operation_id)
        generation = self._owner_generation(uid)
        with self.db() as db:
            row=db.execute("SELECT * FROM ai_jobs WHERE id=? AND owner=?",(_id(job_id),uid)).fetchone()
        if not row:
            raise AIError("job_not_editable",409)
        if self._expired(row):
            raise AIError("operation_deleted",410)
        if row["status"]!="succeeded":
            raise AIError("job_not_editable",409)
        if row["kind"]=="reading":
            fingerprint = _hash(["reading_edit",job_id,revision,text.strip()])
            with self.db(True) as db:
                self._require_generation(db,uid,generation)
                fresh=db.execute("SELECT * FROM ai_jobs WHERE id=? AND owner=?",(job_id,uid)).fetchone()
                if self._expired(fresh):
                    raise AIError("operation_deleted",410)
                receipt=db.execute("SELECT * FROM ai_reading_edits WHERE owner=? AND operation_id=?",
                                   (uid,operation_id)).fetchone()
                if receipt:
                    if receipt["job_id"]!=job_id or receipt["fingerprint"]!=fingerprint:
                        raise AIError("operation_conflict",409)
                    result=self._public_job(fresh)
                    result["replayed"]=True
                    return result
                if (self._operation_job(db,uid,operation_id)
                        or db.execute("SELECT 1 FROM ai_conversations WHERE owner=? AND operation_id=?", (uid,operation_id)).fetchone()):
                    raise AIError("operation_conflict",409)
                current=json.loads(fresh["result"] or "{}")
                if fresh["status"]!="succeeded" or current.get("revision",0)!=revision:
                    raise AIError("transcript_conflict",409)
                original=current.get("originalTranscript",current["transcript"])
                updated=curriculum.reading_result(current["reference"],text.strip(),True)
                updated.update({key:current[key] for key in ("readingId","scopeVersion","sourceVersion") if key in current})
                updated.update({"originalTranscript":original,"revision":revision+1,
                                "previousComparison":current["comparison"]})
                db.execute("UPDATE ai_jobs SET result=?,updated=? WHERE id=?",
                           (_dump(updated),self.clock(),job_id))
                db.execute("""INSERT INTO ai_reading_edits
                    (owner,operation_id,job_id,fingerprint,revision,created) VALUES(?,?,?,?,?,?)""",
                    (uid,operation_id,job_id,fingerprint,revision+1,self.clock()))
            return self.get_job(uid,job_id)
        if row["kind"] not in ("dialogue","dialogue_edit"):
            raise AIError("job_not_editable",409)
        prior=self._replay(uid,operation_id,"dialogue_edit",row["run_id"],
                           {"editedTranscript":text.strip(),"conversationRevision":revision,
                            "originalJob":job_id},row["conversation_id"])
        if prior:
            return prior
        conversation,state=self._conversation_payload(uid,row["conversation_id"],revision,allow_completed=True)
        if not state["history"] or state["history"][-1]["jobId"]!=job_id:
            raise AIError("only_latest_turn_editable",409)
        payload={"conversation":state,"conversationRevision":revision,
                 "editedTranscript":text.strip(),"originalJob":job_id,
                 "lang":state["context"]["interfaceLanguage"]}
        reserve=reserve_text_cost(len((_dump(state)+curriculum.DIALOGUE_INSTRUCTIONS).encode())+24000)
        return self._enqueue(uid,operation_id,"dialogue_edit",row["run_id"],payload,reserve,
                             conversation_id=row["conversation_id"],expected_revision=revision,
                             expected_generation=generation)

    def cancel_job(self,uid,job_id):
        with self.db(True) as db:
            row=db.execute("SELECT * FROM ai_jobs WHERE owner=? AND id=?",(uid,_id(job_id))).fetchone()
            if not row:
                raise AIError("job_not_found",404)
            if row["status"] in ("queued","running"):
                db.execute("""UPDATE ai_jobs SET status='cancelled',result=NULL,
                  actual=CASE WHEN status='queued' THEN 0 ELSE actual END,updated=? WHERE id=?""",
                  (self.clock(),job_id))
                db.execute("UPDATE ai_conversations SET pending_job=NULL WHERE pending_job=?",(job_id,))
        self._delete_audio(row)
        return self.get_job(uid,job_id)

    def finish_conversation(self,uid,cid,revision):
        pending=None
        with self.db(True) as db:
            row=db.execute("SELECT * FROM ai_conversations WHERE owner=? AND id=?",(uid,_id(cid))).fetchone()
            if not row:
                raise AIError("conversation_not_found",404)
            if self._expired(row):
                raise AIError("conversation_deleted",410)
            if row["status"] in ("partial","completed"):
                return self._public_conversation(row)
            if row["revision"]!=revision:
                raise AIError("conversation_conflict",409)
            if row["pending_job"]:
                pending=db.execute("SELECT * FROM ai_jobs WHERE id=?",(row["pending_job"],)).fetchone()
                db.execute("""UPDATE ai_jobs SET status='cancelled',result=NULL,
                   actual=CASE WHEN status='queued' THEN 0 ELSE actual END,updated=? WHERE id=?""",
                   (self.clock(),row["pending_job"]))
            db.execute("""UPDATE ai_conversations SET status='partial',revision=revision+1,
                pending_job=NULL,updated=? WHERE id=?""",(self.clock(),cid))
        if pending:
            self._delete_audio(pending)
        return self.get_conversation(uid,cid)

    def report(self,uid,job_id,reason):
        if reason not in ("incorrect","irrelevant","unclear"):
            raise AIError("invalid_report")
        with self.db(True) as db:
            if not db.execute("SELECT 1 FROM ai_jobs WHERE owner=? AND id=?",(uid,_id(job_id))).fetchone():
                raise AIError("job_not_found",404)
            db.execute("INSERT OR REPLACE INTO ai_feedback_reports VALUES(?,?,?,?)",
                       (uid,job_id,reason,self.clock()))
            db.execute("UPDATE ai_jobs SET reported=1 WHERE id=?",(job_id,))
        return {"reported":True}

    def erase(self,uid):
        import lesson_evidence
        with self.db(True) as db:
            rows=db.execute("SELECT * FROM ai_jobs WHERE owner=?",(uid,)).fetchall()
            db.execute("INSERT OR IGNORE INTO ai_owner_generation(owner) VALUES(?)",(uid,))
            db.execute("UPDATE ai_owner_generation SET generation=generation+1 WHERE owner=?",(uid,))
            db.execute("""UPDATE ai_jobs SET status='deleted',payload=NULL,result=NULL,error_code=NULL,
               actual=CASE WHEN status='queued' THEN 0 ELSE actual END,updated=? WHERE owner=?""",
               (self.clock(),uid))
            db.execute("""UPDATE ai_conversations SET status='deleted',state='{}',
                pending_job=NULL,revision=revision+1 WHERE owner=?""",(uid,))
            db.execute("DELETE FROM ai_feedback_reports WHERE owner=?",(uid,))
            runs=db.execute("SELECT run_id FROM lesson_evidence_runs WHERE user_id=?",(uid,)).fetchall()
            for run in runs:
                lesson_evidence.forget(db,uid,run["run_id"])
        for row in rows:
            self._delete_audio(row)
        return {"deleted":True,"ordinaryProgressPreserved":True}

    def text_turn(self,uid,cid,revision,text,operation_id):
        """Explicit meaning-only fallback; never masquerades as voice evidence."""
        self._permission(uid,"dialogue")
        if not isinstance(text,str) or not 1<=len(text.strip())<=2000:
            raise AIError("invalid_transcript")
        generation = self._owner_generation(uid)
        prior=self._replay(uid,operation_id,"dialogue",None,
                           {"typedTranscript":text.strip(),"conversationRevision":revision},cid)
        if prior:
            return prior
        row,state=self._conversation_payload(uid,cid,revision)
        payload={"conversation":state,"conversationRevision":revision,
                 "typedTranscript":text.strip(),"lang":state["context"]["interfaceLanguage"]}
        reserve=reserve_text_cost(len((_dump(state)+curriculum.DIALOGUE_INSTRUCTIONS).encode())+24000)
        return self._enqueue(uid,operation_id,"dialogue",row["run_id"],payload,reserve,
                             conversation_id=cid,expected_revision=revision,
                             expected_generation=generation)

    def _delete_audio(self,row):
        payload=json.loads(row["payload"] or "{}")
        path=payload.get("audioPath")
        if path:
            candidate=Path(path)
            if candidate.parent==self.spool:
                candidate.unlink(missing_ok=True)

    def collect(self):
        """Bounded retention/lease maintenance, including when paid AI is off."""
        now=self.clock()
        cutoff=dt.datetime.fromtimestamp(now-TEXT_RETENTION,dt.timezone.utc).isoformat(timespec="seconds")
        with self.db(True) as db:
            expired=db.execute("""SELECT * FROM ai_jobs WHERE
               (status='queued' AND created<?) OR (status='running' AND lease_until<?)
               ORDER BY created LIMIT ?""",
               (now-JOB_TTL,now,MAINTENANCE_BATCH)).fetchall()
            for row in expired:
                state="unknown" if row["status"]=="running" else "failed"
                db.execute("""UPDATE ai_jobs SET status=?,result=NULL,error_code=?,
                   actual=CASE WHEN status='queued' THEN 0 ELSE actual END,updated=? WHERE id=?""",
                   (state,"worker_interrupted" if state=="unknown" else "job_expired",now,row["id"]))
                db.execute("UPDATE ai_conversations SET pending_job=NULL WHERE pending_job=?",(row["id"],))
            old=db.execute("""SELECT * FROM ai_jobs WHERE created<=? AND status!='deleted'
                ORDER BY created LIMIT ?""",(now-TEXT_RETENTION,MAINTENANCE_BATCH)).fetchall()
            for row in old:
                db.execute("""UPDATE ai_jobs SET status='deleted',payload=NULL,result=NULL,
                  error_code=NULL,updated=? WHERE id=?""",(now,row["id"]))
            conversations=db.execute("""SELECT id FROM ai_conversations
                WHERE created<=? AND status!='deleted' ORDER BY created LIMIT ?""",
                (now-TEXT_RETENTION,MAINTENANCE_BATCH)).fetchall()
            for row in conversations:
                db.execute("""UPDATE ai_conversations SET state='{}',status='deleted',
                    pending_job=NULL,revision=revision+1 WHERE id=?""",(row["id"],))
            # Includes abandoned and legacy runs without completed_at. Tombstones
            # prevent later lesson continuation from recreating expired evidence.
            evidence=db.execute("""SELECT user_id,run_id FROM lesson_evidence_runs
                WHERE COALESCE(completed_at,started_at)<=?
                ORDER BY COALESCE(completed_at,started_at) LIMIT ?""",
                (cutoff,MAINTENANCE_BATCH)).fetchall()
            for row in evidence:
                lesson_evidence.forget(db,row["user_id"],row["run_id"])
        for row in [*expired,*old]:
            self._delete_audio(row)
        removed=0
        if self.spool.exists():
            # Random server names only. Concurrent worker deletion is expected.
            for path in self.spool.glob("*.audio"):
                try:
                    if path.is_file() and path.stat().st_mtime<=now-JOB_TTL:
                        path.unlink(missing_ok=True)
                        removed+=1
                        if removed>=MAINTENANCE_BATCH:
                            break
                except FileNotFoundError:
                    pass
        return {"jobs":len(old),"expired":len(expired),"conversations":len(conversations),
                "evidence":len(evidence),"orphanAudio":removed}

    def _maintenance_loop(self):
        while not self.stop.is_set():
            try:
                self.collect()
            except Exception:
                # Do not include learner data or filesystem details in logs.
                pass
            self.stop.wait(60)

    def _claim(self):
        self.collect()
        with self.db(True) as db:
            running=db.execute("SELECT COUNT(*) FROM ai_jobs WHERE status='running'").fetchone()[0]
            if running>=self.config.concurrency:
                return None
            row=db.execute("SELECT * FROM ai_jobs WHERE status='queued' ORDER BY created LIMIT 1").fetchone()
            if not row:
                return None
            if not self.config.permits(row["owner"],row["kind"]):
                db.execute("""UPDATE ai_jobs SET status='cancelled',actual=0,
                   error_code='ai_unavailable',updated=? WHERE id=?""",(self.clock(),row["id"]))
                db.execute("UPDATE ai_conversations SET pending_job=NULL WHERE pending_job=?",(row["id"],))
                return None
            db.execute("""UPDATE ai_jobs SET status='running',worker_id=?,lease_until=?,
               updated=? WHERE id=? AND status='queued'""",
               (self.worker_id,self.clock()+max(90,self.config.timeout*2+20),self.clock(),row["id"]))
            return dict(db.execute("SELECT * FROM ai_jobs WHERE id=?",(row["id"],)).fetchone())

    def _live(self,row):
        with self.db() as db:
            current=db.execute("SELECT status,generation,worker_id,lease_until FROM ai_jobs WHERE id=?",(row["id"],)).fetchone()
            generation=db.execute("SELECT generation FROM ai_owner_generation WHERE owner=?",(row["owner"],)).fetchone()
        return bool(current and generation and current["status"]=="running" and
                    current["worker_id"]==self.worker_id and
                    current["lease_until"] is not None and current["lease_until"]>self.clock() and
                    current["generation"]==generation[0]==row["generation"] and
                    self.config.permits(row["owner"],row["kind"]))

    def _text_call(self,instructions,context,schema,calls,row=None):
        if row is not None and not self._live(row):
            raise AIError("cancelled",409)
        # Record the attempted paid stage before invoking or parsing the provider.
        call={"kind":"text","usage":None,"cost":None}
        calls.append(call)
        try:
            value,usage=self.provider.text(instructions,context,schema)
            call.update({"usage":_usage_metadata(usage),"cost":text_cost(usage)})
            return value
        except ProviderError as error:
            cost=text_cost(error.usage)
            if cost is None and error.code in ("provider_auth","provider_access","provider_limit"):
                cost=0
            call.update({"usage":_usage_metadata(error.usage),"cost":cost,"error":error.code})
            raise
        except Exception:
            call["error"]="transport_unknown"
            raise

    def _asr_call(self,payload,calls,row=None):
        audio=Path(payload["audioPath"]).read_bytes()
        if row is not None and not self._live(row):
            raise AIError("cancelled",409)
        call={"kind":"audio","usage":None,"cost":None,"measuredSeconds":payload["audioSeconds"]}
        calls.append(call)
        try:
            value,usage=self.provider.transcribe(audio,payload["audioMime"],payload["audioExtension"])
            call.update({"usage":_usage_metadata(usage),"cost":audio_usage_cost(usage)})
            return value
        except ProviderError as error:
            cost=audio_usage_cost(error.usage)
            if cost is None and error.code in ("provider_auth","provider_access","provider_limit"):
                cost=0
            call.update({"usage":_usage_metadata(error.usage),"cost":cost,"error":error.code})
            raise
        except Exception:
            call["error"]="transport_unknown"
            raise

    def _dialogue(self,row,payload,speech,calls):
        state=json.loads(_dump(payload["conversation"]))
        context=state["context"]
        history=state["history"][:]
        is_edit=row["kind"]=="dialogue_edit"
        previous=history.pop() if is_edit else None
        question=previous["question"] if is_edit else state["question"]
        used=[x["question"]["id"] for x in history]+[question["id"]]
        remaining={x["id"]:x for x in context["questions"] if x["id"] not in used}
        final=len(history)+1>=state["targetTurns"]
        if is_edit and not final and previous.get("nextQuestion"):
            next_question=previous["nextQuestion"]
            remaining={next_question["id"]:next_question}
        request={"interfaceLanguage":context["interfaceLanguage"],
                 "chapter":context["chapter"],"allowedGreekVocabulary":context["allowedGreekVocabulary"],
                 "history":[{"question":x["question"]["text"],"answer":x["transcript"],
                             "reply":x["reply"]} for x in history],
                 "question":question["text"],"answer":speech["transcript"],
                 "origin":speech["origin"],"remainingTurns":state["targetTurns"]-len(history)-1,
                 "remainingQuestions":[] if final else list(remaining.values())}
        if not final and not remaining:
            raise AIError("scenario_exhausted",422)
        value=self._text_call(curriculum.DIALOGUE_INSTRUCTIONS,request,
                             curriculum.dialogue_schema(list(remaining),final),calls,row=row)
        value=curriculum.validate_dialogue(value,context,remaining,final)
        if not value["understood"]:
            return {"kind":"dialogue","status":"recognition_uncertain",
                    "transcript":speech["transcript"],"origin":speech["origin"],
                    "languageErrors":None},None
        next_question=None if final else remaining[value["nextQuestionId"]]
        entry={"ordinal":len(history)+1,"question":question,"transcript":speech["transcript"],
               "originalTranscript":previous.get("originalTranscript",previous["transcript"]) if previous else speech["transcript"],
               "origin":speech["origin"],"edited":speech["edited"],
               "reply":value["reply"],"correction":value["correction"],
               "explanation":value["explanation"],"nextQuestion":next_question,
               "finalNote":value["finalNote"] if final else "",
               "jobId":row["id"],"revision":previous.get("revision",0)+1 if previous else 0,
               "replacesJobId":previous["jobId"] if previous else None}
        history.append(entry)
        state.update({"history":history,"asked":used+([next_question["id"]] if next_question else []),
                      "question":next_question,"revision":payload["conversationRevision"]+1})
        result={"kind":"dialogue","status":"evaluated","turn":entry,"turnCount":len(history),
                "targetTurns":state["targetTurns"],"complete":final,
                "conversationRevision":state["revision"],"pronunciationAssessed":False}
        return result,{"state":state,"status":"completed" if final else "active",
                       "expectedRevision":payload["conversationRevision"]}

    def process_one(self):
        row=self._claim()
        if not row:
            return False
        payload=json.loads(row["payload"])
        calls=[]
        result=None
        conversation_update=None
        error=None
        status="succeeded"
        started=self.clock()
        try:
            if row["kind"]=="summary":
                context=payload["context"]
                result=self._text_call(curriculum.SUMMARY_INSTRUCTIONS,context,
                                       curriculum.summary_schema(context),calls,row=row)
                result=curriculum.validate_summary(result,context)
                result.update({"kind":"summary","evidenceComplete":context["evidenceComplete"],
                               "scopeVersion":context["hash"],"advisory":True})
            else:
                if "editedTranscript" in payload:
                    speech={"transcript":payload["editedTranscript"],"origin":"edited_transcript","edited":True}
                elif "typedTranscript" in payload:
                    speech={"transcript":payload["typedTranscript"],"origin":"typed","edited":False}
                else:
                    speech=self._asr_call(payload,calls,row=row)
                if not self._live(row):
                    raise AIError("cancelled",409)
                # Persist ASR draft separately from committing a conversation turn.
                with self.db(True) as db:
                    db.execute("UPDATE ai_jobs SET result=?,updated=? WHERE id=? AND status='running'",
                               (_dump({"stage":"interpreting",**speech}),self.clock(),row["id"]))
                if row["kind"]=="reading":
                    result=curriculum.reading_result(payload["reference"],speech["transcript"])
                    result.update({"readingId":payload["readingId"],"scopeVersion":payload["scopeVersion"],
                                   "sourceVersion":payload["sourceVersion"]})
                else:
                    result,conversation_update=self._dialogue(row,payload,speech,calls)
        except ProviderError as failure:
            error=failure.code
            status="unknown" if failure.uncertain else "failed"
        except AIError as failure:
            error=failure.code
            status="cancelled" if error=="cancelled" else "failed"
        except ValueError:
            error,status="invalid_model_result","failed"
        except Exception:
            # No payload/exception details in logs or public API.
            error,status="ai_processing_error","failed"
        finally:
            self._delete_audio(row)
        actual=sum(x["cost"] for x in calls) if all(x["cost"] is not None for x in calls) else None
        usage={"calls":calls,"model":self.config.text_model,"audioModel":self.config.audio_model,
               "costBasis":"conservative_tariff_estimate",
               "promptVersion":PROMPT_VERSION,"latencySeconds":max(0,self.clock()-started)}
        with self.db(True) as db:
            current=db.execute("SELECT * FROM ai_jobs WHERE id=?",(row["id"],)).fetchone()
            generation=db.execute("SELECT generation FROM ai_owner_generation WHERE owner=?",(row["owner"],)).fetchone()
            live=(current["status"]=="running" and current["worker_id"]==self.worker_id and
                  current["lease_until"] is not None and current["lease_until"]>self.clock() and
                  current["generation"]==generation[0]==row["generation"])
            if live and conversation_update:
                conversation=db.execute("SELECT * FROM ai_conversations WHERE id=? AND owner=?",
                                        (row["conversation_id"],row["owner"])).fetchone()
                if not conversation or conversation["pending_job"]!=row["id"] or conversation["revision"]!=conversation_update["expectedRevision"]:
                    status,error,result="cancelled","conversation_conflict",None
                else:
                    db.execute("""UPDATE ai_conversations SET state=?,status=?,revision=revision+1,
                       pending_job=NULL,updated=? WHERE id=?""",
                       (_dump(conversation_update["state"]),conversation_update["status"],self.clock(),
                        row["conversation_id"]))
            if live:
                db.execute("""UPDATE ai_jobs SET status=?,result=?,error_code=?,actual=?,usage=?,
                   lease_until=NULL,updated=? WHERE id=?""",
                   (status,_dump(result) if result is not None else None,error,actual,
                    _dump(usage),self.clock(),row["id"]))
            else:
                # Usage is settled even after cancellation/deletion; text never resurfaces.
                db.execute("""UPDATE ai_jobs SET actual=?,usage=?,lease_until=NULL,
                    status=CASE WHEN status='running' THEN 'unknown' ELSE status END,
                    result=CASE WHEN status='running' THEN NULL ELSE result END,
                    error_code=CASE WHEN status='running' THEN 'worker_interrupted' ELSE error_code END
                    WHERE id=?""",(actual,_dump(usage),row["id"]))
            db.execute("UPDATE ai_conversations SET pending_job=NULL WHERE pending_job=?",(row["id"],))
        return True

    def _loop(self):
        while not self.stop.is_set():
            try:
                worked=self.process_one()
            except Exception:
                worked=False
            self.stop.wait(.15 if worked else 1)

    def close(self):
        self.stop.set()
