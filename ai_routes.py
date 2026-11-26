"""Authenticated same-origin optional AI endpoints, separate bounded audio body."""
from __future__ import annotations
import json
import secrets
import threading
from pathlib import Path
from urllib.parse import parse_qs,urlparse
from ai_service import Service,AIError
import ai_audio

_lock=threading.Lock()
# Bound body buffering and decoding across all HTTP handlers in this process.
_audio_preparations=threading.BoundedSemaphore(2)

def engine(app):
    with _lock:
        if not getattr(app,"_lexi_ai_engine",None):
            app._lexi_ai_engine=Service(app.conn,app,Path(app.DB).parent,start_workers=True)
        return app._lexi_ai_engine

def _reply(handler,status,value,new=False,token=None):
    return handler.send_json(status,value,new,token)

def get(handler,app,uid,path,new=False,token=None):
    try:
        service=engine(app)
        parts=path.strip("/").split("/")
        query=parse_qs(urlparse(handler.path).query)
        if path=="/api/ai/capabilities":
            result=service.capabilities(uid)
        elif path=="/api/ai/options":
            result=service.options(uid,query.get("runId",[""])[0],query.get("lang",["ru"])[0])
        elif len(parts)==4 and parts[:3]==["api","ai","jobs"]:
            result=service.get_job(uid,parts[3])
        elif len(parts)==4 and parts[:3]==["api","ai","operations"]:
            result=service.find_operation(uid,parts[3])
            if result is None:
                raise AIError("operation_not_found",404)
        elif len(parts)==4 and parts[:3]==["api","ai","conversations"]:
            result=service.get_conversation(uid,parts[3])
        else:
            raise AIError("not_found",404)
        return _reply(handler,200,result,new,token)
    except AIError as error:
        return _reply(handler,error.status,{"error":error.code},new,token)
    except (ValueError,TypeError,KeyError):
        return _reply(handler,400,{"error":"invalid_ai_request"},new,token)

def post(handler,app,path):
    # Authorization and origin checks precede reading any audio.
    if handler.headers.get("Origin")!=app.ORIGIN:
        handler.close_connection=True
        return _reply(handler,403,{"error":"bad origin"})
    token,new=handler.identity()
    with app.conn() as db:
        account=app.auth.current(db,token)
    if not account:
        handler.close_connection=True
        return _reply(handler,401,{"error":"login_required"},new,token)
    uid=account["user_id"]
    expected_owner=handler.headers.get("X-Lexi-Owner","")
    # A cookie may have changed in another tab while this view still shows the
    # previous account. Validate the displayed owner atomically with this write.
    if not secrets.compare_digest(expected_owner.encode(),app.profile_owner_key(uid).encode()):
        handler.close_connection=True
        return _reply(handler,409,{"error":"account_changed"},new,token)
    old_timeout=handler.connection.gettimeout()
    audio_preparation=False
    try:
        service=engine(app)
        parts=path.strip("/").split("/")
        content_type=handler.headers.get("Content-Type","").split(";",1)[0].strip().lower()
        if handler.headers.get("Transfer-Encoding"):
            raise AIError("body_encoding",400)
        size=int(handler.headers.get("Content-Length","0"))
        maximum=ai_audio.MAX_BYTES if path=="/api/ai/audio" else 16000
        if not 2<=size<=maximum:
            raise AIError("audio_size" if path=="/api/ai/audio" else "body_size",413)
        if path!="/api/ai/audio" and content_type!="application/json":
            raise AIError("json_required",415)
        if path=="/api/ai/audio" and content_type not in ai_audio.MIMES:
            raise AIError("audio_type",415)
        if path=="/api/ai/audio":
            query={k:v[-1] for k,v in parse_qs(urlparse(handler.path).query).items()}
            allowed={"kind","runId","lang","operationId","readingId","conversationId",
                     "revision","sourceJobId","sourceRevision","differenceIndex"}
            if set(query)-allowed:
                raise AIError("invalid_ai_request",400)
            kind=query.get("kind")
            if kind not in ("reading","dialogue"):
                raise AIError("invalid_kind",400)
            # Reject an unavailable feature before accepting a recording. This
            # gate and the fail-fast preparation limit hold no database lock.
            service._permission(uid,kind)
            if not _audio_preparations.acquire(blocking=False):
                raise AIError("ai_preparation_busy",429)
            audio_preparation=True
        handler.connection.settimeout(15)
        data=handler.rfile.read(size)
        if len(data)!=size:
            raise AIError("incomplete_body",400)
        if path=="/api/ai/audio":
            result=service.upload(
                uid,kind,query.get("runId",""),query.get("lang","ru"),
                query.get("operationId",""),data,content_type,
                reading_id=query.get("readingId"),conversation_id=query.get("conversationId"),
                revision=int(query.get("revision",0)),source_job_id=query.get("sourceJobId"),
                source_revision=int(query["sourceRevision"]) if "sourceRevision" in query else None,
                difference_index=int(query["differenceIndex"]) if "differenceIndex" in query else None)
        else:
            body=json.loads(data)
            if not isinstance(body,dict):
                raise AIError("body_type")
            if path=="/api/ai/summary":
                result=service.summary(uid,body.get("runId",""),body.get("lang","ru"),
                                       body.get("operationId",""))
            elif path=="/api/ai/conversations":
                result=service.start_conversation(uid,body.get("runId",""),body.get("lang","ru"),
                    body.get("scenarioId",""),body.get("turns",5),body.get("operationId",""))
            elif len(parts)==5 and parts[:3]==["api","ai","jobs"]:
                jid,action=parts[3:]
                if action=="cancel":
                    result=service.cancel_job(uid,jid)
                elif action=="transcript":
                    result=service.edit_transcript(uid,jid,body.get("transcript"),
                        int(body.get("revision",0)),body.get("operationId",""))
                elif action=="report":
                    result=service.report(uid,jid,body.get("reason"))
                else:
                    raise AIError("not_found",404)
            elif len(parts)==5 and parts[:3]==["api","ai","conversations"]:
                cid,action=parts[3:]
                if action=="finish":
                    result=service.finish_conversation(uid,cid,int(body.get("revision",-1)))
                elif action=="text":
                    result=service.text_turn(uid,cid,int(body.get("revision",-1)),
                                             body.get("transcript"),body.get("operationId",""))
                else:
                    raise AIError("not_found",404)
            elif path=="/api/ai/erase" and body.get("confirm") is True:
                result=service.erase(uid)
            else:
                raise AIError("not_found",404)
        return _reply(handler,200,result,new,token)
    except AIError as error:
        handler.close_connection=True
        return _reply(handler,error.status,{"error":error.code},new,token)
    except (ValueError,TypeError,KeyError,TimeoutError,UnicodeError):
        handler.close_connection=True
        return _reply(handler,400,{"error":"invalid_ai_request"},new,token)
    finally:
        if audio_preparation:
            _audio_preparations.release()
        handler.connection.settimeout(old_timeout)
