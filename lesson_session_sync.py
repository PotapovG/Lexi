"""Account-scoped active lesson snapshots with optimistic revisions and takeover.

Only an authenticated account can read/write. The 8-digit access code is
never stored here. Browser/device UUIDs are not identity credentials:
the HttpOnly session cookie remains mandatory for every operation.
"""
import datetime as dt
import json
import re
import time
from uuid import UUID
MAX_BYTES=245760

def valid_uuid(text):
    try:return isinstance(text,str) and str(UUID(text))==text.lower()
    except (TypeError,ValueError,AttributeError):return False

def schema(db):
    db.execute("""CREATE TABLE IF NOT EXISTS active_lesson_sessions (
      user_id TEXT PRIMARY KEY,
      session_id TEXT NOT NULL,
      owner_device TEXT NOT NULL,
      revision INTEGER NOT NULL,
      payload TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )""")
def validate_snapshot(snapshot):
    if not isinstance(snapshot,dict) or snapshot.get('version')!=2:
        raise ValueError('invalid session snapshot')
    questions=snapshot.get('questions')
    if not isinstance(questions,list) or not 1<=len(questions)<=60:
        raise ValueError('invalid session snapshot')
    index=snapshot.get('index')
    if type(index)!=int or not 0<=index<len(questions):
        raise ValueError('invalid session snapshot')
    if not isinstance(snapshot.get('nickname'),str) or not 3<=len(snapshot['nickname'])<=64:
        raise ValueError('invalid session snapshot')
    if not isinstance(snapshot.get('settings'),dict):
        raise ValueError('invalid session snapshot')
    deadline=snapshot.get('deadline')
    if not isinstance(deadline,(int,float)) or isinstance(deadline,bool):
        raise ValueError('invalid session snapshot')
    now=time.time()*1000
    if not now-60_000<=deadline<=now+2*3600_000:
        raise ValueError('invalid session deadline')
    for question in questions:
        if not isinstance(question,dict):
            raise ValueError('invalid session questions')
        if (not isinstance(question.get('id'),str) or
            not isinstance(question.get('kind'),str) or
            not isinstance(question.get('direction'),str)):
            raise ValueError('invalid session questions')
        if any(len(question.get(k,''))>160 for k in ('id','kind','direction')):
            raise ValueError('invalid session questions')
    raw=json.dumps(snapshot,ensure_ascii=False,separators=(',',':'))
    if len(raw.encode('utf-8'))>MAX_BYTES:
        raise ValueError('session snapshot too large')
    return raw

def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

def row_for(db,uid):
    return db.execute("SELECT * FROM active_lesson_sessions WHERE user_id=?",(uid,)).fetchone()

def read(db,uid):
    row=row_for(db,uid)
    if not row:return {'exists':False}
    payload=json.loads(row['payload'])
    if payload.get('deadline',0)<=time.time()*1000:
        return {'exists':False,'expired':True}
    return {'exists':True,'sessionId':row['session_id'],
            'ownerDevice':row['owner_device'],'revision':row['revision'],
            'snapshot':payload,'updatedAt':row['updated_at']}

def action(db,uid,body):
    op=body.get('op')
    session=body.get('sessionId')
    device=body.get('deviceId')
    if not valid_uuid(session) or not valid_uuid(device):
        raise ValueError('invalid session identifiers')
    if op not in ('start','save','takeover','clear'):
        raise ValueError('invalid session operation')
    revision=body.get('revision')
    if op!='start' and (type(revision)!=int or revision<1):
        raise ValueError('invalid session revision')
    raw=validate_snapshot(body.get('snapshot')) if op in ('start','save') else None
    db.execute('BEGIN IMMEDIATE')
    row=row_for(db,uid)
    if op=='start':
        if row and json.loads(row['payload']).get('deadline',0)>time.time()*1000:
            if row['session_id']==session and row['owner_device']==device:
                # Idempotent first-save retry must never roll back a later
                # snapshot, especially if a slow response arrives late.
                return {'saved':True,'revision':row['revision'],'sessionId':session}
            if row['owner_device']!=device:
                raise ValueError('session_conflict')
        db.execute("""INSERT INTO active_lesson_sessions
          (user_id,session_id,owner_device,revision,payload,updated_at)
          VALUES(?,?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE
          SET session_id=excluded.session_id,owner_device=excluded.owner_device,
          revision=excluded.revision,payload=excluded.payload,updated_at=excluded.updated_at""",
          (uid,session,device,1,raw,now_iso()))
        return {'saved':True,'revision':1,'sessionId':session}
    if not row or row['session_id']!=session:
        raise ValueError('session_conflict')
    # Clearing your own completed session must still work when an in-flight
    # autosave incremented its revision. Another device cannot erase it.
    if op=='clear':
        if row['owner_device']!=device:raise ValueError('session_conflict')
        db.execute("DELETE FROM active_lesson_sessions WHERE user_id=?",(uid,))
        return {'cleared':True}
    if row['revision']!=revision:raise ValueError('session_conflict')
    if op=='takeover':
        if json.loads(row['payload']).get('deadline',0)<=time.time()*1000:
            raise ValueError('session_conflict')
        if row['owner_device']!=device:
            db.execute("""UPDATE active_lesson_sessions SET owner_device=?,
                       revision=revision+1,updated_at=? WHERE user_id=?""",
                       (device,now_iso(),uid))
            return {'takenOver':True,'revision':revision+1,'sessionId':session,
                    'snapshot':json.loads(row['payload'])}
        return {'takenOver':True,'revision':revision,'sessionId':session,
                'snapshot':json.loads(row['payload'])}
    if row['owner_device']!=device:raise ValueError('session_conflict')
    db.execute("""UPDATE active_lesson_sessions SET payload=?,revision=revision+1,
                  updated_at=? WHERE user_id=?""",(raw,now_iso(),uid))
    return {'saved':True,'revision':revision+1,'sessionId':session}

def assert_owner(db,uid,body):
    # Legacy clients without a session ID remain backward-compatible.
    session=body.get('sessionId')
    device=body.get('deviceId')
    if session is None or device is None:return
    if not valid_uuid(session) or not valid_uuid(device):
        raise ValueError('invalid session identifiers')
    row=row_for(db,uid)
    # First answer can precede the first asynchronously committed snapshot;
    # once a row exists, a different device or lesson cannot keep scoring.
    if row and (row['session_id']!=session or row['owner_device']!=device):
        raise ValueError('session_conflict')
