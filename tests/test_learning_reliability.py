#!/usr/bin/env python3
"""Synthetic SQLite regression tests. Never uses production learner records."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import copy
import datetime as dt
import json
import http.client
import threading
import os
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server
import learning_receipts as receipts
import lesson_evidence as evidence
import lesson_session_sync as sessions


class IsolatedDatabase(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="lexi-reliability-")
        self.previous_db = server.DB
        server.DB = str(Path(self.folder.name) / "test.sqlite3")
        self.previous_secret=server.auth.SECRET_FILE
        server.auth.SECRET_FILE=Path(self.folder.name)/"synthetic-pepper"
        server.init_db()
        self.uid = "synthetic-student"

    def tearDown(self):
        server.DB = self.previous_db
        server.auth.SECRET_FILE=self.previous_secret
        self.folder.cleanup()

    def word_body(self, **updates):
        body = dict(id=server.vocab.VOCAB[0]["id"], direction="target-gr",
                    lang="ru", selected="synthetic wrong answer", requestId=str(uuid4()))
        body.update(updates)
        return body

    def progress(self, uid=None):
        with server.conn() as db:
            return dict(db.execute("SELECT * FROM vocab_progress WHERE user_id=?",
                                   (uid or self.uid,)).fetchone())


class ReceiptTests(IsolatedDatabase):
    def test_concurrent_vocabulary_duplicate_scores_once(self):
        body = self.word_body()
        def deliver(_):
            with server.conn() as db:
                return server.vocabulary_write(db, self.uid, body)
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(deliver, range(12)))
        self.assertEqual(self.progress()["attempts"], 1)
        self.assertEqual(self.progress()["correct"], 0)
        self.assertEqual(self.progress()["miss_debt"], 2)
        self.assertTrue(all(r["answer"] == results[0]["answer"] for r in results))
        with server.conn() as db:
            with self.assertRaisesRegex(ValueError, "request_id_reused"):
                server.vocabulary_write(db, self.uid, dict(body, selected="different"))
        with server.conn() as db:
            server.vocabulary_write(db, "another-student", body)
        self.assertEqual(self.progress("another-student")["attempts"], 1)

    def test_distinct_concurrent_answers_preserve_debt(self):
        bodies = [self.word_body() for _ in range(8)]
        def deliver(body):
            with server.conn() as db:
                return server.vocabulary_write(db, self.uid, body)
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(deliver, bodies))
        self.assertEqual(self.progress()["attempts"], 8)
        self.assertEqual(self.progress()["miss_debt"], 7)

    def test_failure_before_receipt_rolls_back_score(self):
        body = self.word_body()
        def fail(token):
            server.vocab.answer(db, self.uid, body)
            raise RuntimeError("synthetic interruption before commit")
        with self.assertRaises(RuntimeError):
            with server.conn() as db:
                receipts.commit(db, self.uid, "vocabulary", body, fail)
        with server.conn() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM vocab_progress").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM learning_action_receipts").fetchone()[0], 0)

    def test_compacted_receipt_never_becomes_a_new_attempt(self):
        bodies = [self.word_body() for _ in range(3)]
        with patch.object(receipts, "FULL_RECEIPTS", 2):
            for body in bodies:
                with server.conn() as db:
                    server.vocabulary_write(db, self.uid, body)
        with server.conn() as db:
            with self.assertRaisesRegex(ValueError, "receipt_expired"):
                server.vocabulary_write(db, self.uid, bodies[0])
        self.assertEqual(self.progress()["attempts"], 3)


class ClassicTests(IsolatedDatabase):
    def snapshot(self, count=0, saved_at=1000):
        return dict(version=2, nickname="Synthetic Learner",
                    questions=[dict(id="synthetic-card", kind="word", direction="ru-gr")],
                    index=0, settings={}, deadline=time.time()*1000+600000,
                    count=count, correct=0, wrong=count, savedAt=saved_at)

    def start(self):
        body=dict(op="start",sessionId=str(uuid4()),deviceId=str(uuid4()),
                  revision=0,snapshot=self.snapshot(),requestId=str(uuid4()))
        with server.conn() as db:
            result=sessions.action(db,self.uid,body)
        return body,result

    def test_lost_save_response_and_stale_own_snapshot(self):
        start,_=self.start()
        body=dict(start,op="save",revision=1,snapshot=self.snapshot(1,2000),
                  requestId=str(uuid4()))
        with server.conn() as db:
            result=sessions.action(db,self.uid,body)
        self.assertEqual(result["revision"],2)
        with server.conn() as db:
            retry=sessions.action(db,self.uid,body)
        self.assertTrue(retry["replayed"])
        self.assertEqual(retry["revision"],2)
        with server.conn() as db:
            stale=sessions.action(db,self.uid,dict(body,requestId=str(uuid4()),
                                  snapshot=self.snapshot(0,1000)))
        self.assertTrue(stale["reconciled"])
        self.assertFalse(stale["saved"])
        self.assertEqual(stale["snapshot"]["count"],1)
        with server.conn() as db:
            delayed=sessions.action(db,self.uid,dict(body,revision=2,requestId=str(uuid4()),
                                    snapshot=self.snapshot(0,3000)))
        self.assertFalse(delayed["saved"])
        with server.conn() as db:
            current=sessions.action(db,self.uid,dict(body,revision=2,requestId=str(uuid4()),
                                    snapshot=self.snapshot(2,4000)))
        self.assertEqual(current["revision"],3)

    def test_takeover_prevents_old_receipt_from_reclaiming(self):
        start,result=self.start()
        save=dict(start,op="save",revision=1,snapshot=self.snapshot(1,2000),
                  requestId=str(uuid4()))
        with server.conn() as db:
            sessions.action(db,self.uid,save)
        transfer=dict(op="takeover",sessionId=start["sessionId"],deviceId=str(uuid4()),
                      revision=2,requestId=str(uuid4()))
        with server.conn() as db:
            taken=sessions.action(db,self.uid,transfer)
        self.assertEqual(taken["revision"],3)
        with server.conn() as db:
            with self.assertRaisesRegex(ValueError,"session_conflict"):
                sessions.action(db,self.uid,save)
        with server.conn() as db:
            repeated=sessions.action(db,self.uid,transfer)
        self.assertEqual(repeated["revision"],3)
        self.assertTrue(repeated["replayed"])

    def test_expired_session_can_start_on_another_device(self):
        start,_=self.start()
        with server.conn() as db:
            snapshot=json.loads(sessions.row_for(db,self.uid)["payload"])
            snapshot["deadline"]=0
            db.execute("UPDATE active_lesson_sessions SET payload=? WHERE user_id=?",
                       (json.dumps(snapshot),self.uid))
        replacement=dict(start,sessionId=str(uuid4()),deviceId=str(uuid4()),
                         snapshot=self.snapshot(),requestId=str(uuid4()))
        with server.conn() as db:
            result=sessions.action(db,self.uid,replacement)
        self.assertEqual(result["sessionId"],replacement["sessionId"])


class EvidenceTests(IsolatedDatabase):
    def active(self, first=0):
        return dict(runId=uuid4().hex,index=0,chapter=1,family="book",generatorVersion=4,
                    startedAt=dt.datetime.now(dt.timezone.utc).isoformat(),
                    at=first,items=[dict(id="fixture-a",kind="word",type="quiz",
                    chapter=1,lang="ru",prompt="Synthetic prompt"),
                    dict(id="fixture-b",kind="life",type="life",chapter=1,
                         lang="ru",prompt="Synthetic scene")])

    def test_complete_snapshot_is_immutable_owned_and_tombstoned(self):
        active=self.active()
        with server.conn() as db:
            evidence.begin(db,self.uid,active)
            evidence.record(db,self.uid,active,dict(action="answer",selected="first"),
                            {"feedback":{"correct":False,"answer":"canonical",
                                         "answerErrorType":"spelling"}},str(uuid4()))
            active["at"]=1
            complete=dict(index=0,chapter=1,attempts=1,correct=0,errors=1,skips=1,total=2)
            evidence.record(db,self.uid,active,dict(action="answer",selected="unverified"),
                            {"feedback":{"correct":False,"unverified":True,
                                         "lessonComplete":complete}},str(uuid4()))
        with server.conn() as db:
            snapshot=evidence.get_snapshot(db,self.uid,active["runId"])
            self.assertTrue(snapshot["evidenceComplete"])
            self.assertEqual(snapshot["evidence"][0]["selected"],"first")
            self.assertEqual(snapshot["evidence"][0]["result"]["answerErrorType"],"spelling")
            self.assertIsNone(snapshot["evidence"][0]["assisted"])
            self.assertIsNone(evidence.get_snapshot(db,"another-student",active["runId"]))
            with self.assertRaisesRegex(ValueError,"already_completed"):
                evidence.record(db,self.uid,active,dict(action="answer",selected="changed"),
                                {"feedback":{"correct":True}},str(uuid4()))
        with server.conn() as db:
            evidence.forget(db,self.uid,active["runId"])
        with server.conn() as db:
            self.assertIsNone(evidence.begin(db,self.uid,active))
            self.assertIsNone(evidence.get_snapshot(db,self.uid,active["runId"]))

    def test_legacy_partial_lesson_has_no_invented_answers(self):
        active=self.active(first=1)
        with server.conn() as db:
            evidence.record(db,self.uid,active,dict(action="answer",selected="known"),
                {"feedback":{"correct":True,"lessonComplete":{"index":0,"chapter":1,"total":2}}},
                str(uuid4()))
        with server.conn() as db:
            snapshot=evidence.get_snapshot(db,self.uid,active["runId"])
        self.assertFalse(snapshot["evidenceComplete"])
        self.assertEqual(len(snapshot["evidence"]),1)
        self.assertEqual(snapshot["evidence"][0]["ordinal"],1)


class IntegratedLearningTests(IsolatedDatabase):
    def start_board(self):
        with server.conn() as db:
            return server.board_write(db,self.uid,dict(action="lesson_start",revision=0,
                                      lang="ru",requestId=str(uuid4())))

    def test_board_lost_final_response_restores_feedback_and_one_snapshot(self):
        view=self.start_board()
        count=view["lesson"]["count"]
        for i in range(count):
            lesson=view["lesson"]
            question=lesson["question"]
            body=dict(action="answer",revision=view["revision"],questionId=question["id"],
                      lessonIndex=lesson["index"],selected=question["choices"][0],
                      lang="ru",requestId=str(uuid4()))
            with server.conn() as db:
                result=server.board_write(db,self.uid,body)
            if i==count-1:
                with server.conn() as db:
                    retry=server.board_write(db,self.uid,body)
                self.assertEqual(retry["feedback"],result["feedback"])
                self.assertTrue(retry["replayed"])
                with server.conn() as db:
                    recovered=server.board_read(db,self.uid,"ru")
                    snapshots=evidence.list_runs(db,self.uid)
                    snapshot=evidence.get_snapshot(db,self.uid,snapshots[0]["runId"])
                self.assertIsNone(recovered["lesson"])
                self.assertEqual(recovered["lastReceipt"]["requestId"],body["requestId"])
                self.assertEqual(recovered["lastReceipt"]["lesson"]["at"],count-1)
                self.assertEqual(len(snapshots),1)
                self.assertEqual(len(snapshot["evidence"]),count)
                self.assertTrue(snapshot["evidenceComplete"])
                with server.conn() as db:
                    done=server.board_write(db,self.uid,dict(action="ack_feedback",
                        requestId=body["requestId"],revision=0,lang="ru"))
                self.assertIsNone(done["lastReceipt"])
            view=result

    def test_board_paused_after_commit_replay_uses_current_state(self):
        view=self.start_board();question=view["lesson"]["question"]
        body=dict(action="answer",revision=view["revision"],questionId=question["id"],
                  lessonIndex=view["lesson"]["index"],selected=question["choices"][0],
                  lang="ru",requestId=str(uuid4()))
        with server.conn() as db:
            scored=server.board_write(db,self.uid,body)
        with server.conn() as db:
            paused=server.board_write(db,self.uid,dict(action="pause",revision=scored["revision"],
                                      lang="ru",requestId=str(uuid4())))
        with server.conn() as db:
            replay=server.board_write(db,self.uid,body)
        self.assertEqual(replay["revision"],paused["revision"])
        self.assertTrue(replay["lesson"]["paused"])
        self.assertEqual(replay["feedback"],scored["feedback"])

    def test_life_answer_and_deferral_retry_once(self):
        with server.conn() as db:
            scene=server.life_scene_read(db,self.uid,"ru","meet")
        body=dict(id="meet",lang="ru",revision=scene["revision"],
                  answer=server._life.BY_ID["meet"]["accepted"][0],requestId=str(uuid4()))
        with server.conn() as db:
            first=server.life_scene_write(db,self.uid,body)
        with server.conn() as db:
            retry=server.life_scene_write(db,self.uid,body)
        self.assertEqual(first["feedback"] if "feedback" in first else first["correct"],
                         retry["feedback"] if "feedback" in retry else retry["correct"])
        with server.conn() as db:
            current=server.life_scene_read(db,self.uid,"ru","meet")
        self.assertEqual(current["attempts"],1)
        self.assertEqual(current["lastReceipt"]["requestId"],body["requestId"])
        with server.conn() as db:
            server.life_scene_write(db,self.uid,dict(action="ack_feedback",id="meet",
                                    lang="ru",requestId=body["requestId"]))
        skip=dict(action="skip",id="meet",lang="ru",revision=current["revision"],
                  requestId=str(uuid4()))
        with server.conn() as db:
            deferred=server.life_settings_write(db,self.uid,skip)
        with server.conn() as db:
            repeated=server.life_settings_write(db,self.uid,skip)
        self.assertEqual(repeated["revision"],deferred["revision"])
        with server.conn() as db:
            scopes=server.progress_scopes(db,self.uid)
        self.assertEqual(scopes["life"]["skipped"],1)
        self.assertFalse(scopes["countsAreAdditive"])

    def test_srs_scans_past_unavailable_prefix_and_keeps_locale(self):
        chosen=[(server.GRAMMAR2_ALL[0],"grammar_fill"),
                (server.ENCLITIC_ALL[0],"stress_enclitic"),
                (server.CLOCK_ALL[0],"read")]
        with server.conn() as db:
            for i in range(550):
                db.execute("INSERT INTO srs_schedule(user_id,card_key,due_at,updated_at) VALUES(?,?,?,?)",
                           (self.uid,f"archived-{i}:ru-gr","2000-01-01","2000-01-01"))
            for card,direction in chosen:
                key=server.card_key(card,direction,"ru")
                db.execute("INSERT INTO srs_schedule(user_id,card_key,due_at,updated_at) VALUES(?,?,?,?)",
                           (self.uid,key,"2001-01-01","2001-01-01"))
        with patch.object(server,"format_question",wraps=server.format_question) as formatter:
            result=server.make_srs_due_quiz(self.uid,{},"es",1,set())
        self.assertEqual(result["available"],3)
        self.assertEqual(result["count"],1)
        self.assertEqual(result["questions"][0]["lang"],"es")
        self.assertEqual(formatter.call_count,1)
        for card,direction in chosen:
            with server.conn() as db:
                db.execute("DELETE FROM srs_schedule WHERE user_id=? AND card_key!=?",
                           (self.uid,server.card_key(card,direction,"ru")))
            result=server.make_srs_due_quiz(self.uid,{},"ar",1,set())
            self.assertEqual(result["count"],1)
            self.assertEqual(result["questions"][0]["lang"],"ar")
            # Restore remaining valid cards for the next iteration.
            with server.conn() as db:
                for other,other_direction in chosen:
                    db.execute("INSERT OR IGNORE INTO srs_schedule(user_id,card_key,due_at,updated_at) VALUES(?,?,?,?)",
                               (self.uid,server.card_key(other,other_direction,"ru"),"2001-01-01","2001-01-01"))


class HttpContractTests(IsolatedDatabase):
    def test_authenticated_http_commit_retry_and_scope_contract(self):
        previous_origin=server.ORIGIN
        httpd=server.ThreadingHTTPServer(("127.0.0.1",0),server.Handler)
        server.ORIGIN=f"http://127.0.0.1:{httpd.server_port}"
        thread=threading.Thread(target=httpd.serve_forever,daemon=True)
        thread.start()
        try:
            with server.conn() as db:
                account=server.auth.register(db,"fixture-anonymous","Synthetic HTTP","fixture")
                identity=server.auth.current(db,account["token"])
            self.uid=identity["user_id"]
            def request(method,path,body=None,token=None,origin=None):
                conn=http.client.HTTPConnection("127.0.0.1",httpd.server_port,timeout=5)
                headers={"Content-Type":"application/json","Origin":origin or server.ORIGIN}
                if token:headers["Cookie"]=server.COOKIE+"="+token
                raw=json.dumps(body).encode() if body is not None else None
                conn.request(method,path,body=raw,headers=headers)
                reply=conn.getresponse()
                value=json.loads(reply.read())
                status=reply.status
                conn.close()
                return status,value
            self.assertEqual(request("GET","/api/board")[0],401)
            body=self.word_body()
            status,first=request("POST","/api/vocab/answer",body,account["token"])
            self.assertEqual(status,200)
            self.assertEqual(self.progress()["attempts"],1)
            status,retry=request("POST","/api/vocab/answer",body,account["token"])
            self.assertEqual(status,200)
            self.assertTrue(retry["replayed"])
            self.assertEqual(self.progress()["attempts"],1)
            status,error=request("POST","/api/vocab/answer",
                                 dict(body,selected="another"),account["token"])
            self.assertEqual(status,409)
            self.assertEqual(error["error"],"request_id_reused")
            self.assertEqual(request("POST","/api/vocab/answer",
                            self.word_body(),account["token"],"https://wrong.example")[0],403)
            status,started=request("POST","/api/board",
                dict(action="lesson_start",revision=0,lang="ru",requestId=str(uuid4())),
                account["token"])
            self.assertEqual(status,200)
            q=started["lesson"]["question"]
            status,scored=request("POST","/api/board",
                dict(action="answer",revision=started["revision"],questionId=q["id"],
                     lessonIndex=started["lesson"]["index"],selected=q["choices"][0],
                     lang="ru",requestId=str(uuid4())),account["token"])
            self.assertEqual(status,200)
            status,summary=request("GET","/api/stats",token=account["token"])
            self.assertEqual(status,200)
            self.assertEqual(summary["scope"],"scored_book_cards")
            self.assertEqual(summary["attempts"],1)
            self.assertEqual(summary["progressScopes"]["board"]["answers"],1)
            self.assertEqual(summary["progressScopes"]["vocabulary"]["attempts"],1)
            self.assertFalse(summary["progressScopes"]["countsAreAdditive"])
            self.assertTrue(summary["progressScopes"]["quizIncludesBoardQuizAnswers"])
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=2)
            server.ORIGIN=previous_origin


if __name__ == "__main__":
    unittest.main()
