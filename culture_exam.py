"""Server-authoritative Cyprus Culture mock-exam sessions.

CULT-06 is a *profile* of Lexi's existing question cards, account and SQLite
connection. It does not create another learning progress store or SRS engine.
The single table stores sealed, per-account exam snapshots and attempts.
"""
from __future__ import annotations

import datetime as dt
import json
import random
import re
import secrets
import uuid
from collections import defaultdict

UTC = dt.timezone.utc
DURATION = dt.timedelta(minutes=45)
QUESTION_COUNT = 25
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{4,90}$")


def utc_now():
    return dt.datetime.now(UTC)


def now_at(value=None):
    value = value or utc_now()
    if value.tzinfo is None:
        raise ValueError("exam now must include timezone")
    return value.astimezone(UTC)


def iso(value):
    return value.isoformat(timespec="seconds")


def schema(db):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS culture_exam_sessions (
      session_id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      start_key TEXT NOT NULL,
      revision INTEGER NOT NULL DEFAULT 0,
      status TEXT NOT NULL CHECK(status IN ('active','finished')),
      started_at TEXT NOT NULL,
      deadline_at TEXT NOT NULL,
      finished_at TEXT,
      score INTEGER,
      payload TEXT NOT NULL,
      UNIQUE(user_id,start_key)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS ix_culture_exam_one_active
      ON culture_exam_sessions(user_id) WHERE status='active';
    CREATE INDEX IF NOT EXISTS ix_culture_exam_history
      ON culture_exam_sessions(user_id,started_at DESC);
    """)


def _query(db, user_id, session_id=None):
    if session_id is not None:
        if not isinstance(session_id,str) or len(session_id)>80:
            raise ValueError("invalid exam session ID")
        return db.execute(
            "SELECT * FROM culture_exam_sessions WHERE user_id=? AND session_id=?",
            (user_id,session_id)).fetchone()
    return db.execute("""SELECT * FROM culture_exam_sessions WHERE user_id=?
        ORDER BY CASE status WHEN 'active' THEN 0 ELSE 1 END,started_at DESC LIMIT 1""",
        (user_id,)).fetchone()


def has_live_exam(db, user_id, now=None):
    """Used inside the EXISTING answer idempotency transaction as a guard."""
    stamp=iso(now_at(now))
    return db.execute("""SELECT 1 FROM culture_exam_sessions
        WHERE user_id=? AND status='active' AND deadline_at>? LIMIT 1""",
        (user_id,stamp)).fetchone() is not None


def _finish(db,row,now,reason):
    if row["status"]!="active":
        return row
    payload=json.loads(row["payload"])
    score=sum(
        q.get("selectedIndex") is not None
        and q["selectedIndex"]==q["correctIndex"]
        for q in payload["questions"]
    )
    payload["finishReason"]=reason
    db.execute("""UPDATE culture_exam_sessions
        SET status='finished',finished_at=?,score=?,revision=revision+1,payload=?
        WHERE session_id=? AND user_id=? AND status='active'""",
        (iso(now),int(score),json.dumps(payload,ensure_ascii=False,separators=(",",":")),
         row["session_id"],row["user_id"]))
    return _query(db,row["user_id"],row["session_id"])


def _expire(db,row,now):
    if row is not None and row["status"]=="active" and row["deadline_at"]<=iso(now):
        return _finish(db,row,now,"time_expired")
    return row


def _safe_view(row,now):
    if row is None:
        return {"exists":False}
    payload=json.loads(row["payload"])
    finished=row["status"]=="finished"
    questions=[]
    for q in payload["questions"]:
        item={
            "id":q["id"],"topic":q["topic"],"cultureFormat":q["format"],
            "prompt":q["prompt"],"choices":list(q["choices"]),
            "selectedIndex":q["selectedIndex"],"flagged":bool(q["flagged"]),
        }
        if finished:
            item.update(
                correctIndex=q["correctIndex"],
                correct=q["selectedIndex"] is not None and q["selectedIndex"]==q["correctIndex"],
                translation=q["translations"][payload["lang"]]["question"],
                optionTranslations=list(q["translations"][payload["lang"]]["options"]),
                explanation=q["explanations"][payload["lang"]],
                source=q["source"],
                contentVersion=q["contentVersion"],
            )
        questions.append(item)
    view={
        "exists":True,"sessionId":row["session_id"],"revision":row["revision"],
        "status":row["status"],"mode":"culture_exam","scope":"culture",
        "lang":payload["lang"],"goal":payload["goal"],
        "startedAt":row["started_at"],"deadlineAt":row["deadline_at"],
        "serverNow":iso(now),"durationMinutes":45,
        "total":QUESTION_COUNT,
        "answered":sum(q["selectedIndex"] is not None for q in payload["questions"]),
        "questions":questions,
    }
    if finished:
        view.update(
            finishedAt=row["finished_at"],score=row["score"],
            correct=row["score"],percent=round(row["score"]*100/QUESTION_COUNT),
            passed=(row["score"]>=15) if payload["goal"]=="citizenship" else None,
            passingScore=15 if payload["goal"]=="citizenship" else None,
            reason=payload.get("finishReason","completed"),
            passNote="Study simulator result, not an official examination.",
        )
    return view


def _published_fresh(card,now):
    if not card.get("id","").startswith("cyq_") or not card.get("factId"):
        return False
    verified=card.get("verifiedAt")
    if not isinstance(verified,str) or verified>now.date().isoformat():
        return False
    for field in ("reviewDue","validUntil","factReviewDue","factValidUntil"):
        value=card.get(field)
        if value is not None and (not isinstance(value,str) or value<now.date().isoformat()):
            return False
    return True


def _pick(cards, config, rng, now):
    # Existing culture_adapter.load has already performed the publication gate.
    # Check dates again for processes which run across a review deadline.
    by_fact=defaultdict(list)
    for card in cards.values():
        if _published_fresh(card,now):
            by_fact[card["factId"]].append(card)
    if len(by_fact)<QUESTION_COUNT:
        raise ValueError("not_enough_reviewed_culture_facts")
    candidates=[rng.choice(group) for group in by_fact.values()]
    picked=[]
    topic_counts=defaultdict(int)
    format_counts=defaultdict(int)
    weights=config.get("exam_format_weights",{})
    while len(picked)<QUESTION_COUNT:
        pool=[c for c in candidates if c not in picked]
        probabilities=[
            max(1,weights.get(c["format"],1))
            / (1+format_counts[c["format"]])
            / (1+topic_counts[c["topic"]])
            for c in pool
        ]
        chosen=rng.choices(pool,weights=probabilities,k=1)[0]
        picked.append(chosen)
        topic_counts[chosen["topic"]]+=1
        format_counts[chosen["format"]]+=1
    rng.shuffle(picked)
    snapshot=[]
    for card in picked:
        options=list(card["options"])
        expected=options[card["answerIndex"]]
        rng.shuffle(options)
        snapshot.append({
            "id":card["id"],"factId":card["factId"],
            "topic":card["topic"],"format":card["format"],
            "prompt":card["gr"],"choices":options,
            "correctIndex":options.index(expected),
            "selectedIndex":None,"flagged":False,
            "translations":card["translations"],"explanations":card["explanations"],
            "source":card["source"],"contentVersion":card["contentVersion"],
        })
    return snapshot


def _request_id(body):
    token=body.get("requestId")
    try:
        if not isinstance(token,str) or str(uuid.UUID(token))!=token.lower():
            raise ValueError
    except (ValueError,TypeError,AttributeError):
        raise ValueError("invalid exam request ID") from None
    return token.lower()


def _owned(db,uid,session_id):
    row=_query(db,uid,session_id)
    if row is None:
        raise ValueError("unknown_exam_session")
    return row


def get(db,uid,session_id=None,now=None):
    now=now_at(now)
    db.execute("BEGIN IMMEDIATE")
    row=_expire(db,_query(db,uid,session_id),now)
    return _safe_view(row,now)


def action(db,uid,body,cards,config,now=None,rng=None):
    if not isinstance(body,dict):
        raise ValueError("invalid exam action")
    now=now_at(now)
    rng=rng or secrets.SystemRandom()
    op=body.get("action")
    if op not in ("start","answer","flag","finish"):
        raise ValueError("invalid exam action")
    db.execute("BEGIN IMMEDIATE")
    if op=="start":
        request_id=_request_id(body)
        lang=body.get("lang","ru")
        goal=body.get("goal","citizenship")
        if lang not in ("ru","en") or goal!="citizenship":
            raise ValueError("unsupported exam settings")
        previous=db.execute("SELECT * FROM culture_exam_sessions WHERE user_id=? AND start_key=?",
                            (uid,request_id)).fetchone()
        if previous is not None:
            return _safe_view(_expire(db,previous,now),now)
        current=db.execute("SELECT * FROM culture_exam_sessions WHERE user_id=? AND status='active'",
                           (uid,)).fetchone()
        if current is not None:
            current=_expire(db,current,now)
            if current["status"]=="active":
                return _safe_view(current,now)
        snapshot=_pick(cards,config,rng,now)
        session_id=str(uuid.uuid4())
        payload={"lang":lang,"goal":goal,"questions":snapshot,"receipts":{}}
        db.execute("""INSERT INTO culture_exam_sessions(
            session_id,user_id,start_key,revision,status,started_at,deadline_at,payload)
            VALUES(?,?,?,?,?,?,?,?)""",
            (session_id,uid,request_id,0,"active",iso(now),iso(now+DURATION),
             json.dumps(payload,ensure_ascii=False,separators=(",",":"))))
        return _safe_view(_owned(db,uid,session_id),now)

    session_id=body.get("sessionId")
    row=_expire(db,_owned(db,uid,session_id),now)
    if row["status"]=="finished":
        return _safe_view(row,now) if op=="finish" else _fail("exam_already_finished")
    if op=="finish":
        if type(body.get("revision")) is not int or body["revision"]!=row["revision"]:
            raise ValueError("stale_exam_revision")
        return _safe_view(_finish(db,row,now,"submitted"),now)

    request_id=_request_id(body)
    payload=json.loads(row["payload"])
    qid=body.get("questionId")
    if not isinstance(qid,str) or not ID_PATTERN.fullmatch(qid):
        raise ValueError("invalid exam question")
    matching=next((q for q in payload["questions"] if q["id"]==qid),None)
    if matching is None:
        raise ValueError("question_not_in_exam")
    value=body.get("selectedIndex") if op=="answer" else body.get("flagged")
    if op=="answer":
        if value is not None and (type(value) is not int or value not in range(4)):
            raise ValueError("invalid exam choice")
    elif type(value) is not bool:
        raise ValueError("invalid exam flag")
    fingerprint=json.dumps([op,qid,value],ensure_ascii=False,separators=(",",":"))
    if request_id in payload["receipts"]:
        if payload["receipts"][request_id]!=fingerprint:
            raise ValueError("exam request ID reused")
        return _safe_view(row,now)
    if type(body.get("revision")) is not int or body["revision"]!=row["revision"]:
        raise ValueError("stale_exam_revision")
    if len(payload["receipts"])>=250:
        raise ValueError("exam_request_limit")
    if op=="answer":
        matching["selectedIndex"]=value
    else:
        matching["flagged"]=value
    payload["receipts"][request_id]=fingerprint
    db.execute("""UPDATE culture_exam_sessions SET revision=revision+1,payload=?
        WHERE session_id=? AND user_id=? AND status='active'""",
        (json.dumps(payload,ensure_ascii=False,separators=(",",":")),session_id,uid))
    return _safe_view(_owned(db,uid,session_id),now)


def _fail(message):
    raise ValueError(message)
