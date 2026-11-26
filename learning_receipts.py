"""Atomic account-owned receipts for learning actions.

Only the caller's existing scoring transaction is used. Full responses are
bounded; compacted receipts keep their hash so an old retry can never score
again. Legacy callers without a requestId remain accepted but cannot retry a
vocabulary answer idempotently until they adopt the request ID contract.
"""
import datetime as dt
import hashlib
import json
from uuid import UUID, uuid4

FULL_RECEIPTS = 64
RETENTION_DAYS = 30


def schema(db):
    db.execute("""CREATE TABLE IF NOT EXISTS learning_action_receipts (
        user_id TEXT NOT NULL, namespace TEXT NOT NULL, request_id TEXT NOT NULL,
        request_hash TEXT NOT NULL, response TEXT, receipt TEXT,
        created_at TEXT NOT NULL,
        PRIMARY KEY(user_id,namespace,request_id)
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS learning_feedback_pending (
        user_id TEXT NOT NULL, namespace TEXT NOT NULL, scope_id TEXT NOT NULL,
        request_id TEXT NOT NULL,
        PRIMARY KEY(user_id,namespace,scope_id)
    )""")
    db.execute("""CREATE INDEX IF NOT EXISTS ix_learning_receipts_recent
        ON learning_action_receipts(user_id,namespace,created_at)""")


def request_id(value):
    if not isinstance(value, str) or len(value) != 36:
        raise ValueError("invalid_request_id")
    try:
        if str(UUID(value)) != value.lower():
            raise ValueError("invalid_request_id")
    except (ValueError, AttributeError):
        raise ValueError("invalid_request_id") from None
    return value.lower()


def _hash(body):
    # Revision belongs to the logical attempt: the same card can have several
    # slots in a dialogue. A retry must preserve the complete original body.
    fields = {k: v for k, v in body.items() if k != "requestId"}
    return hashlib.sha256(json.dumps(fields, ensure_ascii=False,
        sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def pending(db, uid, namespace, scope_id=""):
    row = db.execute("""SELECT r.receipt FROM learning_feedback_pending p
        JOIN learning_action_receipts r ON r.user_id=p.user_id
          AND r.namespace=p.namespace AND r.request_id=p.request_id
        WHERE p.user_id=? AND p.namespace=? AND p.scope_id=?""",
        (uid, namespace, scope_id)).fetchone()
    return json.loads(row["receipt"]) if row and row["receipt"] else None


def acknowledge(db, uid, namespace, token, scope_id=""):
    token = request_id(token)
    if not db.in_transaction:
        db.execute("BEGIN IMMEDIATE")
    # ACK is deliberately revision-independent. A delayed ACK for an older
    # receipt cannot erase feedback from a newer answer or another device.
    db.execute("""DELETE FROM learning_feedback_pending
        WHERE user_id=? AND namespace=? AND scope_id=? AND request_id=?""",
        (uid, namespace, scope_id, token))
    return {"acknowledged": True, "requestId": token}


def _compact(db, uid, namespace):
    cutoff = (dt.datetime.now(dt.timezone.utc) -
              dt.timedelta(days=RETENTION_DAYS)).isoformat(timespec="microseconds")
    db.execute("""DELETE FROM learning_feedback_pending
        WHERE user_id=? AND namespace=? AND request_id IN (
          SELECT request_id FROM learning_action_receipts
          WHERE user_id=? AND namespace=? AND created_at<?)""",
        (uid, namespace, uid, namespace, cutoff))
    db.execute("""UPDATE learning_action_receipts SET response=NULL,receipt=NULL
        WHERE user_id=? AND namespace=? AND response IS NOT NULL
          AND (created_at<? OR request_id NOT IN (
            SELECT request_id FROM learning_action_receipts
            WHERE user_id=? AND namespace=?
            ORDER BY created_at DESC,request_id DESC LIMIT ?))
          AND request_id NOT IN (
            SELECT request_id FROM learning_feedback_pending
            WHERE user_id=? AND namespace=?)""",
        (uid, namespace, cutoff, uid, namespace, FULL_RECEIPTS, uid, namespace))


def commit(db, uid, namespace, body, perform, scope_id=None):
    """perform(token) returns (response, optional feedback receipt).

    The caller owns commit/rollback through its connection context manager.
    A receipt lookup and all score writes take the same SQLite write lock.
    """
    if not db.in_transaction:
        db.execute("BEGIN IMMEDIATE")
    explicit = body.get("requestId") is not None
    token = request_id(body["requestId"]) if explicit else str(uuid4())
    digest = _hash(body)
    seen = db.execute("""SELECT request_hash,response
        FROM learning_action_receipts
        WHERE user_id=? AND namespace=? AND request_id=?""",
        (uid, namespace, token)).fetchone()
    if seen:
        if seen["request_hash"] != digest:
            raise ValueError("request_id_reused")
        if seen["response"] is None:
            raise ValueError("receipt_expired")
        result = json.loads(seen["response"])
        result["replayed"] = True
        return result
    result, receipt = perform(token)
    result = dict(result)
    if receipt is not None:
        receipt = dict(receipt, requestId=token)
        result["lastReceipt"] = receipt
    result["requestId"] = token
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")
    # Board replays always rebuild the live course view in server.py. Retain
    # only the original grade/feedback, not 64 copies of the full course map.
    stored = ({k: result[k] for k in ("revision", "feedback", "lastReceipt", "requestId")
               if k in result} if namespace == "board" else result)
    db.execute("""INSERT INTO learning_action_receipts
        (user_id,namespace,request_id,request_hash,response,receipt,created_at)
        VALUES(?,?,?,?,?,?,?)""",
        (uid, namespace, token, digest, json.dumps(stored, ensure_ascii=False),
         json.dumps(receipt, ensure_ascii=False) if receipt is not None else None, stamp))
    if receipt is not None and scope_id is not None:
        db.execute("""INSERT INTO learning_feedback_pending
            (user_id,namespace,scope_id,request_id) VALUES(?,?,?,?)
            ON CONFLICT(user_id,namespace,scope_id)
            DO UPDATE SET request_id=excluded.request_id""",
            (uid, namespace, scope_id, token))
    _compact(db, uid, namespace)
    return result
