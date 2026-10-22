"""Idempotent committed answer receipts keyed per signed-in student."""
import datetime as dt
import hashlib
import json
import re

REQUEST_ID=re.compile(r"[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\Z")
def schema(db):
    db.execute("""CREATE TABLE IF NOT EXISTS answer_receipts (
         user_id TEXT NOT NULL,
         request_id TEXT NOT NULL,
         request_hash TEXT NOT NULL,
         response TEXT NOT NULL,
         created_at TEXT NOT NULL,
         PRIMARY KEY(user_id,request_id)
       )""")

def score_once(conn_factory,score,user_id,body,validate_attempt=None):
    token=body.get('requestId')
    if token is None:
        with conn_factory() as db:
            db.execute('BEGIN IMMEDIATE')
            if validate_attempt:validate_attempt(db,user_id,body)
            return score(user_id,body,injected_db=db)
    if not isinstance(token,str) or not REQUEST_ID.fullmatch(token) or len(token)!=36:
        raise ValueError('invalid request id')
    fields={k:body.get(k) for k in ('id','direction','selected','lang','srsOptIn')}
    digest=hashlib.sha256(json.dumps(fields,ensure_ascii=False,sort_keys=True,
                    separators=(',',':')).encode('utf-8')).hexdigest()
    with conn_factory() as db:
        db.execute('BEGIN IMMEDIATE')
        seen=db.execute("""SELECT request_hash,response FROM answer_receipts
            WHERE user_id=? AND request_id=?""",(user_id,token)).fetchone()
        if seen:
            if seen['request_hash']!=digest:
                raise ValueError('request id reused for different answer')
            return json.loads(seen['response'])
        if validate_attempt:validate_attempt(db,user_id,body)
        result=score(user_id,body,injected_db=db)
        db.execute("""INSERT INTO answer_receipts
            (user_id,request_id,request_hash,response,created_at) VALUES (?,?,?,?,?)""",
            (user_id,token,digest,json.dumps(result,ensure_ascii=False),
             dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')))
        return result
