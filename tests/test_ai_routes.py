"""Real isolated HTTP boundary tests; no provider or production data."""
import http.client
import json
import os
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from pathlib import Path
import sys
import tempfile
import threading
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
from ai_service import Config,Service,AIError

class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.saved=(server.DB,server.ORIGIN,server.auth.SECRET_FILE,getattr(server,"_lexi_ai_engine",None))
        server.DB=str(Path(self.tmp.name)/"db.sqlite3")
        server.auth.SECRET_FILE=Path(self.tmp.name)/"pepper"
        server.init_db()
        server._lexi_ai_engine=Service(server.conn,server,self.tmp.name,Config(),start_workers=False)
        self.httpd=server.ThreadingHTTPServer(("127.0.0.1",0),server.Handler)
        server.ORIGIN=f"http://127.0.0.1:{self.httpd.server_port}"
        self.thread=threading.Thread(target=self.httpd.serve_forever,daemon=True);self.thread.start()
        with server.conn() as db:
            self.account=server.auth.register(db,"synthetic-anonymous","AI HTTP fixture","fixture")
            self.uid=server.auth.current(db,self.account["token"])["user_id"]
            self.owner=server.profile_owner_key(self.uid)
    def tearDown(self):
        self.httpd.shutdown();self.httpd.server_close();self.thread.join(timeout=2)
        server._lexi_ai_engine.close()
        server.DB,server.ORIGIN,server.auth.SECRET_FILE,server._lexi_ai_engine=self.saved
        self.tmp.cleanup()
    def request(self,method,path,body=None,authorized=True,headers=None):
        connection=http.client.HTTPConnection("127.0.0.1",self.httpd.server_port,timeout=3)
        hdr={"Origin":server.ORIGIN,"Content-Type":"application/json"}
        if authorized:
            hdr["Cookie"]=server.COOKIE+"="+self.account["token"]
            hdr["X-Lexi-Owner"]=self.owner
        if headers:
            hdr.update(headers)
        raw=body if isinstance(body,bytes) else json.dumps(body).encode() if body is not None else None
        connection.request(method,"/greek"+path,body=raw,headers=hdr)
        response=connection.getresponse()
        result=(response.status,response.read(),dict(response.headers))
        connection.close()
        return result
    def test_auth_origin_precede_large_audio_body_read(self):
        status,_,_=self.request("GET","/api/ai/capabilities",authorized=False)
        self.assertEqual(status,401)
        # Deliberately incomplete body: the boundary must reject without waiting.
        headers={"Content-Type":"audio/wav","Content-Length":str(11*1024*1024)}
        self.assertEqual(self.request("POST","/api/ai/audio",b"{}",False,headers)[0],401)
        self.assertEqual(self.request("POST","/api/ai/audio",b"{}",True,
                                     dict(headers,Origin="https://foreign.invalid"))[0],403)
    def test_body_type_and_bounds(self):
        self.assertEqual(self.request("POST","/api/ai/summary",b"{}",headers={"Content-Type":"text/plain"})[0],415)
        self.assertEqual(self.request("POST","/api/ai/summary",b"x"*16001)[0],413)
        self.assertEqual(self.request("POST","/api/ai/summary",b"[]")[0],400)
        self.assertEqual(self.request("POST","/api/ai/audio",b"xx",headers={"Content-Type":"application/zip"})[0],415)
        self.assertEqual(self.request("POST","/api/ai/summary",b"{}",headers={"Transfer-Encoding":"chunked"})[0],400)
    def test_ai_off_does_not_break_existing_lessons(self):
        status,body,_=self.request("GET","/api/ai/capabilities")
        self.assertEqual(status,200)
        self.assertFalse(json.loads(body)["enabled"])
        self.assertEqual(self.request("POST","/api/ai/summary",
                         {"runId":"synthetic-run","operationId":"synthetic-operation","lang":"en"})[0],503)
        status,body,_=self.request("GET","/api/board?lang=en")
        self.assertEqual(status,200)
        self.assertEqual(json.loads(body)["progressScope"],"guided_lessons")
        self.assertEqual(self.request("GET","/api/ai/jobs/nonexistent-job")[0],404)
    def test_optional_static_assets_and_blob_playback_csp(self):
        for path in ("/ai_ui.js","/ai_ui.css"):
            status,body,headers=self.request("GET",path)
            self.assertEqual(status,200,path)
            self.assertGreater(len(body),20)
            self.assertIn("media-src 'self' blob:",headers["Content-Security-Policy"])
            self.assertEqual(self.request("HEAD",path)[0],200)


    def enable_audio(self):
        service=server._lexi_ai_engine
        service.config.stage="enabled"
        service.config.key="synthetic-key-never-sent"
        service.config.features=frozenset({"reading","dialogue"})
        service.config.speech_validated=True
        return service

    def test_unavailable_audio_rejects_before_missing_ten_mib_body(self):
        headers={"Content-Type":"audio/wav","Content-Length":str(10*1024*1024)}
        started=time.monotonic()
        status,body,_=self.request(
            "POST","/api/ai/audio?kind=reading&operationId=disabled-audio-operation",
            b"{}",headers=headers)
        self.assertEqual((status,json.loads(body)["error"]),(503,"ai_unavailable"))
        self.assertLess(time.monotonic()-started,2)
        # Invalid headers keep their original semantics even while AI is off.
        self.assertEqual(self.request("POST","/api/ai/audio?kind=reading",b"{}",
                         headers=dict(headers,**{"Content-Length":str(10*1024*1024+1)}))[0],413)
        self.assertEqual(self.request("POST","/api/ai/audio?kind=reading",b"{}",
                         headers=dict(headers,**{"Transfer-Encoding":"chunked"}))[0],400)

    def test_two_audio_preparations_fail_fast_and_leave_lessons_usable(self):
        service=self.enable_audio()
        ready,release=threading.Event(),threading.Event()
        lock=threading.Lock()
        counter={"active":0,"peak":0}
        def prepare(*args,**kwargs):
            with lock:
                counter["active"]+=1
                counter["peak"]=max(counter["peak"],counter["active"])
                if counter["active"]==2:
                    ready.set()
            try:
                if not release.wait(5):
                    raise AIError("synthetic_preparation_timeout",503)
                return {"id":"synthetic-job","status":"queued"}
            finally:
                with lock:
                    counter["active"]-=1
        path="/api/ai/audio?kind=reading&operationId=admission-test-operation"
        with patch.object(service,"upload",side_effect=prepare):
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures=[pool.submit(self.request,"POST",path,b"audio",True,
                                     {"Content-Type":"audio/wav"}) for _ in range(2)]
                try:
                    self.assertTrue(ready.wait(2))
                    started=time.monotonic()
                    status,body,_=self.request("POST",path,b"{}",headers={
                        "Content-Type":"audio/wav","Content-Length":str(10*1024*1024)})
                    self.assertEqual((status,json.loads(body)["error"]),(429,"ai_preparation_busy"))
                    self.assertLess(time.monotonic()-started,2)
                    status,body,_=self.request("GET","/api/board?lang=en")
                    self.assertEqual(status,200)
                    board=json.loads(body)
                    status,body,_=self.request("POST","/api/board",
                        {"action":"lesson_start","revision":board["revision"],"lang":"en"})
                    self.assertEqual(status,200)
                    self.assertIsNotNone(json.loads(body)["lesson"])
                finally:
                    release.set()
                self.assertEqual([future.result(timeout=3)[0] for future in futures],[200,200])
        self.assertEqual(counter["peak"],2)
        with patch.object(service,"upload",return_value={"id":"after-release-job","status":"queued"}):
            self.assertEqual(self.request("POST",path,b"audio",headers={"Content-Type":"audio/wav"})[0],200)

    def test_preparation_slots_release_after_success_and_validation_errors(self):
        service=self.enable_audio()
        path="/api/ai/audio?kind=reading&operationId=release-test-operation"
        with patch.object(service,"upload",side_effect=AIError("audio_invalid",422)) as upload:
            for _ in range(3):
                status,body,_=self.request("POST",path,b"audio",headers={"Content-Type":"audio/wav"})
                self.assertEqual((status,json.loads(body)["error"]),(422,"audio_invalid"))
            self.assertEqual(upload.call_count,3)
        with patch.object(service,"upload",return_value={"id":"success-job","status":"queued"}) as upload:
            for _ in range(3):
                self.assertEqual(self.request("POST",path,b"audio",headers={"Content-Type":"audio/wav"})[0],200)
            self.assertEqual(upload.call_count,3)

    def test_incomplete_audio_body_releases_preparation_slot(self):
        service=self.enable_audio()
        path="/greek/api/ai/audio?kind=reading&operationId=incomplete-audio-operation"
        with patch.object(service,"upload") as upload:
            for _ in range(3):
                connection=http.client.HTTPConnection("127.0.0.1",self.httpd.server_port,timeout=3)
                try:
                    connection.request("POST",path,body=b"xx",headers={
                        "Origin":server.ORIGIN,"Content-Type":"audio/wav","Content-Length":"4",
                        "Cookie":server.COOKIE+"="+self.account["token"],"X-Lexi-Owner":self.owner})
                    connection.sock.shutdown(socket.SHUT_WR)
                    response=connection.getresponse()
                    self.assertEqual((response.status,json.loads(response.read())["error"]),
                                     (400,"incomplete_body"))
                finally:
                    connection.close()
            upload.assert_not_called()


    def test_stale_tab_owner_cannot_erase_a_different_cookie_account(self):
        with server.conn() as db:
            other=server.auth.register(db,"synthetic-other","Other HTTP fixture","other-fixture")
            other_uid=server.auth.current(db,other["token"])["user_id"]
        engine=server._lexi_ai_engine
        with patch.object(engine,"erase",return_value={"deleted":True}) as erase:
            status,body,_=self.request("POST","/api/ai/erase",{"confirm":True},headers={
                "Cookie":server.COOKIE+"="+other["token"],"X-Lexi-Owner":self.owner})
            self.assertEqual(status,409)
            self.assertEqual(json.loads(body)["error"],"account_changed")
            erase.assert_not_called()
            self.assertEqual(self.request("POST","/api/ai/erase",{"confirm":True},
                             headers={"X-Lexi-Owner":""})[0],409)
            erase.assert_not_called()
            self.assertEqual(self.request("POST","/api/ai/erase",{"confirm":True},headers={
                "Cookie":server.COOKIE+"="+other["token"],
                "X-Lexi-Owner":server.profile_owner_key(other_uid)})[0],200)
            erase.assert_called_once_with(other_uid)

    def test_stale_owner_header_rejects_ordinary_writes_without_new_attempt(self):
        status,body,_=self.request("POST","/api/board",
            {"action":"lesson_start","revision":0,"lang":"en","requestId":"owner-bound-operation"},
            headers={"X-Lexi-Owner":"different-owner"})
        self.assertEqual(status,409)
        self.assertEqual(json.loads(body)["error"],"account_changed")
        status,body,_=self.request("GET","/api/board?lang=en")
        self.assertEqual(status,200)
        self.assertIsNone(json.loads(body)["lesson"])


    def test_phrase_audio_route_passes_only_source_locator_and_revision(self):
        service=self.enable_audio()
        path=("/api/ai/audio?kind=reading&runId=owned-run&lang=ru&readingId=dlg001"
              "&operationId=phrase-operation&sourceJobId=owned-parent"
              "&sourceRevision=2&differenceIndex=1")
        with patch.object(service,"upload",return_value={"id":"child","status":"queued"}) as upload:
            status,_,_=self.request("POST",path,b"audio",headers={"Content-Type":"audio/wav"})
            self.assertEqual(status,200)
            self.assertEqual(upload.call_args.kwargs["source_job_id"],"owned-parent")
            self.assertEqual(upload.call_args.kwargs["source_revision"],2)
            self.assertEqual(upload.call_args.kwargs["difference_index"],1)
            self.assertNotIn("reference",upload.call_args.kwargs)
        with patch.object(service,"upload") as upload:
            status,body,_=self.request("POST",path+"&reference=arbitrary",b"audio",
                                     headers={"Content-Type":"audio/wav"})
            self.assertEqual((status,json.loads(body)["error"]),(400,"invalid_ai_request"))
            upload.assert_not_called()


if __name__=="__main__":
    unittest.main(verbosity=2)
