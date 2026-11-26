#!/usr/bin/env python3
"""Offline AI durability/privacy/budget regressions; no real provider calls."""
import copy
import datetime as dt
import io
import json
import math
import os
from pathlib import Path
import sqlite3
import struct
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch
import wave

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ai_audio
import ai_curriculum
import ai_provider
import ai_service
import lesson_evidence


class Clock:
    def __init__(self):
        self.value = time.time()

    def __call__(self):
        return self.value


class Provider:
    def __init__(self):
        self.text_calls = 0
        self.audio_calls = 0
        self.text_usage = {"input_tokens": 20, "output_tokens": 10}
        self.audio_usage = {"type": "duration", "seconds": 1}
        self.on_text = None
        self.on_audio = None
        self.text_error = None

    def text(self, instructions, context, schema):
        self.text_calls += 1
        if self.on_text:
            self.on_text()
        if self.text_error:
            raise self.text_error
        if "remainingQuestions" in context:
            questions = context["remainingQuestions"]
            result = {"understood": True, "reply": "Ευχαριστώ.",
                      "correction": "", "explanation": "",
                      "nextQuestionId": questions[0]["id"] if questions else "",
                      "finalNote": ""}
        else:
            result = {"observation": {"text": "Synthetic supported observation.",
                                      "evidenceIds": ["e0"], "example": ""},
                      "improvements": [], "nextStep": "", "targetCardId": ""}
        return result, copy.deepcopy(self.text_usage)

    def transcribe(self, audio, mime, extension):
        self.audio_calls += 1
        if self.on_audio:
            self.on_audio()
        return {"transcript": "Καλημέρα.", "origin": "asr", "edited": False}, copy.deepcopy(self.audio_usage)


def wav():
    data = io.BytesIO()
    with wave.open(data, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(16000)
        output.writeframes(b"".join(struct.pack("<h", int(2000 * math.sin(i / 10)))
                                   for i in range(16000)))
    return data.getvalue()


class AIServiceTests(unittest.TestCase):
    uid = "synthetic-owner"
    run_id = "synthetic-run-001"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="lexi-ai-test-")
        self.root = Path(self.temp.name)
        self.clock = Clock()
        self.provider = Provider()
        self.config = ai_service.Config(
            stage="enabled", key="synthetic-never-sent",
            features=frozenset({"summary", "reading", "dialogue"}),
            speech_validated=True, day_limit=2_000_000, daily_jobs=100)
        def connect():
            db = sqlite3.connect(self.root / "test.sqlite3", timeout=10)
            db.row_factory = sqlite3.Row
            return db
        self.connect = connect
        self.app = SimpleNamespace(book_or_audio_card=lambda cid: None)
        self.service = ai_service.Service(
            connect, self.app, self.root, config=self.config,
            provider=self.provider, clock=self.clock)
        self.context = {
            "version": "test", "interfaceLanguage": "ru", "chapter": 1,
            "sourceVersion": "synthetic-source", "rubricVersion": "test-rubric",
            "evidenceComplete": True, "hash": "a" * 64,
            "evidence": [{"evidenceId": "e0", "cardId": "test-card",
                          "correct": True, "skipped": False, "unverified": False,
                          "prompt": "Καλημέρα.", "selected": "Καλημέρα.",
                          "answer": "Καλημέρα.", "hintUsageKnown": False,
                          "assisted": None}],
            "eligibleTargets": [],
            "readings": [{"id": "reading-001", "text": "Καλημέρα.",
                          "sourceVersion": "synthetic-reading-001"},
                         {"id": "reading-002", "text": "Ευχαριστώ.",
                          "sourceVersion": "synthetic-reading-002"}],
            "questions": [
                {"id": "question-%d" % n, "sourceId": "reading-001" if n < 3 else "reading-002",
                 "text": "Synthetic question %d?" % n} for n in range(5)],
            "allowedGreekVocabulary": ai_curriculum.words("Ευχαριστώ. Καλημέρα."),
            "claims": {},
        }
        self.service._context = lambda *args: copy.deepcopy(self.context)
        self.seed_run(self.uid, self.run_id)
        self.audio = wav()

    def tearDown(self):
        self.service.close()
        self.temp.cleanup()

    def seed_run(self, owner, run, age=0, completed=True):
        at = dt.datetime.fromtimestamp(self.clock() - age, dt.timezone.utc).isoformat(timespec="seconds")
        snapshot = {"schema": 1, "runId": run, "lessonIndex": 0, "chapter": 1,
                    "sourceVersion": "test", "rubricVersion": "test",
                    "evidence": [], "evidenceComplete": True}
        with self.service.db(True) as db:
            db.execute("""INSERT INTO lesson_evidence_runs
                (user_id,run_id,lesson_index,chapter,source_version,rubric_version,
                 planned_count,first_recorded_ordinal,started_at,completed_at,completed_snapshot)
                VALUES(?,?,0,1,'test','test',1,0,?,?,?)""",
                (owner, run, at, at if completed else None,
                 json.dumps(snapshot) if completed else None))

    def row(self, job_id):
        with self.service.db() as db:
            return dict(db.execute("SELECT * FROM ai_jobs WHERE id=?", (job_id,)).fetchone())

    def error(self, code, fn, *args, **kwargs):
        with self.assertRaises(ai_service.AIError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def summary(self, operation="summary-operation"):
        return self.service.summary(self.uid, self.run_id, "ru", operation)

    def conversation(self, operation="conversation-operation", turns=4):
        return self.service.start_conversation(
            self.uid, self.run_id, "ru", "reading-001", turns, operation)

    def reading(self, operation="reading-operation", reading_id="reading-001"):
        return self.service.upload(
            self.uid, "reading", self.run_id, "ru", operation,
            self.audio, "audio/wav", reading_id=reading_id)

    def typed_turn(self, conversation, operation="typed-turn-operation", text="Synthetic answer"):
        return self.service.text_turn(
            self.uid, conversation["id"], conversation["revision"], text, operation)

    def test_owner_isolation_and_operation_recovery_for_jobs_and_conversations(self):
        job = self.reading()
        conv = self.conversation()
        self.assertIsNone(self.service.find_operation("another-owner", "reading-operation"))
        self.assertIsNone(self.service.find_operation("another-owner", "conversation-operation"))
        self.error("job_not_found", self.service.get_job, "another-owner", job["id"])
        self.error("conversation_not_found", self.service.get_conversation, "another-owner", conv["id"])
        self.assertEqual(self.service.find_operation(self.uid, "reading-operation")["id"], job["id"])
        recovered = self.service.find_operation(self.uid, "conversation-operation")
        self.assertEqual(recovered["id"], conv["id"])
        self.assertIn("history", recovered)
        self.assertEqual(self.service.list_conversations("another-owner", self.run_id), [])

    def test_concurrent_same_operation_reserves_and_executes_once(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            replies = list(pool.map(lambda _: self.summary(), range(8)))
        self.assertEqual(len({reply["id"] for reply in replies}), 1)
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ai_jobs").fetchone()[0], 1)
        self.assertTrue(self.service.process_one())
        self.assertFalse(self.service.process_one())
        self.assertEqual(self.provider.text_calls, 1)
        original = self.service.get_job(self.uid, replies[0]["id"])
        self.assertEqual(original["status"], "succeeded")
        self.assertEqual(self.summary()["id"], original["id"])
        self.error("operation_conflict", self.service.summary,
                   self.uid, "another-run-001", "ru", "summary-operation")

    def test_unknown_paid_usage_preserves_reservation_for_both_stages(self):
        self.provider.text_usage = {"input_tokens": 10, "output_tokens": 5,
                                    "input_tokens_details": {"cached_tokens": None}}
        job = self.summary()
        self.assertTrue(self.service.process_one())
        row = self.row(job["id"])
        self.assertIsNone(row["actual"])
        self.assertGreater(row["reserved"], 0)
        calls = json.loads(row["usage"])["calls"]
        self.assertEqual(len(calls), 1)
        self.assertIsNone(calls[0]["cost"])
        self.assertEqual(self.provider.text_calls, 1)

        self.provider.audio_usage = {"type": "duration"}
        reading = self.reading()
        self.service.process_one()
        row = self.row(reading["id"])
        self.assertEqual(row["status"], "succeeded")
        self.assertIsNone(row["actual"])
        self.assertEqual(len(json.loads(row["usage"])["calls"]), 1)
        self.assertEqual(self.provider.audio_calls, 1)

    def test_transport_exception_and_mixed_stage_unknown_keep_full_reserve(self):
        self.provider.text_error = RuntimeError("synthetic failure after request")
        job = self.summary()
        self.service.process_one()
        row = self.row(job["id"])
        self.assertIsNone(row["actual"])
        self.assertEqual(len(json.loads(row["usage"])["calls"]), 1)
        self.assertNotIn("synthetic failure", row["usage"])

        self.provider.text_error = None
        self.provider.text_usage = {"input_tokens": 10, "output_tokens": 5,
                                    "input_tokens_details": {"cached_tokens": "unexpected"}}
        conv = self.conversation()
        voice = self.service.upload(
            self.uid, "dialogue", self.run_id, "ru", "mixed-stage-operation",
            self.audio, "audio/wav", conversation_id=conv["id"], revision=0)
        self.service.process_one()
        row = self.row(voice["id"])
        self.assertIsNone(row["actual"])
        calls = json.loads(row["usage"])["calls"]
        self.assertEqual([call["cost"] for call in calls], [75, None])
        self.assertEqual(self.provider.audio_calls, 1)

    def test_budget_reservation_is_atomic_across_distinct_requests(self):
        self.config.day_limit = 100
        payload = {"context": self.context, "lang": "ru"}
        def enqueue(number):
            try:
                return self.service._enqueue(
                    self.uid, "budget-op-%02d" % number, "summary", self.run_id,
                    payload, 75)["id"]
            except ai_service.AIError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=6) as pool:
            responses = list(pool.map(enqueue, range(6)))
        self.assertEqual(responses.count("ai_budget_limit"), 5)
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT SUM(reserved) FROM ai_jobs").fetchone()[0], 75)

    def test_usage_retains_only_numeric_accounting_metadata(self):
        self.provider.text_usage = {
            "input_tokens": 20, "output_tokens": 10, "learner_text": "NEVER RETAIN THIS",
            "input_tokens_details": {"cached_tokens": 1, "raw_prompt": "PRIVATE"},
        }
        job = self.summary()
        self.service.process_one()
        usage = self.row(job["id"])["usage"]
        self.assertNotIn("NEVER RETAIN", usage)
        self.assertNotIn("PRIVATE", usage)
        self.assertIn("cached_tokens", usage)

    def _erase_between_context_and_insert(self, action):
        ready, proceed = threading.Event(), threading.Event()
        captured = copy.deepcopy(self.context)
        results = []
        def blocked_context(*args):
            ready.set()
            if not proceed.wait(5):
                raise RuntimeError("test synchronization timed out")
            return captured
        self.service._context = blocked_context
        def submit():
            try:
                results.append(action())
            except ai_service.AIError as error:
                results.append(error.code)
        thread = threading.Thread(target=submit)
        thread.start()
        try:
            self.assertTrue(ready.wait(5))
            self.service.erase(self.uid)
        finally:
            proceed.set()
            thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(results, ["operation_deleted"])
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ai_jobs").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ai_conversations").fetchone()[0], 0)

    def test_erasure_fences_summary_captured_before_insertion(self):
        self._erase_between_context_and_insert(self.summary)

    def test_erasure_fences_conversation_captured_before_insertion(self):
        self._erase_between_context_and_insert(self.conversation)

    def test_erasure_during_audio_validation_cannot_recreate_job_or_recording(self):
        validate = ai_audio.validate_file
        def erase_after_validation(*args):
            result = validate(*args)
            self.service.erase(self.uid)
            return result
        with patch.object(ai_audio, "validate_file", side_effect=erase_after_validation):
            self.error("operation_deleted", self.reading)
        self.assertEqual(list(self.service.spool.glob("*.audio")), [])
        self.assertEqual(self.provider.audio_calls, 0)

    def test_erasure_after_conversation_snapshot_fences_text_submission(self):
        conv = self.conversation()
        capture = self.service._conversation_payload
        def erase_after_capture(*args, **kwargs):
            result = capture(*args, **kwargs)
            self.service.erase(self.uid)
            return result
        with patch.object(self.service, "_conversation_payload", side_effect=erase_after_capture):
            self.error("operation_deleted", self.typed_turn, conv)
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ai_jobs").fetchone()[0], 0)

    def test_expired_source_is_checked_again_at_commit(self):
        validate = ai_audio.validate_file
        def expire_source(*args):
            result = validate(*args)
            with self.service.db(True) as db:
                lesson_evidence.forget(db, self.uid, self.run_id)
            return result
        with patch.object(ai_audio, "validate_file", side_effect=expire_source):
            self.error("lesson_evidence_unavailable", self.reading)
        self.assertEqual(list(self.service.spool.glob("*.audio")), [])

    def test_cancel_after_asr_draft_prevents_the_next_paid_stage(self):
        conv = self.conversation()
        job = self.service.upload(
            self.uid, "dialogue", self.run_id, "ru", "cancel-between-stages",
            self.audio, "audio/wav", conversation_id=conv["id"], revision=0)
        dialogue = self.service._dialogue
        def cancel_after_draft(row, *args):
            self.assertIn("interpreting", self.row(row["id"])["result"])
            self.service.cancel_job(self.uid, row["id"])
            return dialogue(row, *args)
        with patch.object(self.service, "_dialogue", side_effect=cancel_after_draft):
            self.service.process_one()
        row = self.row(job["id"])
        self.assertEqual((row["status"], row["actual"], row["result"]), ("cancelled", 75, None))
        self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (1, 0))
        self.assertEqual(self.service.get_conversation(self.uid, conv["id"])["turnCount"], 0)

    def test_erase_after_asr_draft_discards_text_and_settles_paid_audio(self):
        conv = self.conversation()
        job = self.service.upload(
            self.uid, "dialogue", self.run_id, "ru", "erase-between-stages",
            self.audio, "audio/wav", conversation_id=conv["id"], revision=0)
        dialogue = self.service._dialogue
        def erase_after_draft(row, *args):
            self.service.erase(self.uid)
            return dialogue(row, *args)
        with patch.object(self.service, "_dialogue", side_effect=erase_after_draft):
            self.service.process_one()
        row = self.row(job["id"])
        self.assertEqual((row["status"], row["actual"], row["payload"], row["result"]),
                         ("deleted", 75, None, None))
        self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (1, 0))
        self.assertEqual(list(self.service.spool.glob("*.audio")), [])

    def test_late_provider_result_never_resurrects_erased_data(self):
        self.provider.on_text = lambda: self.service.erase(self.uid)
        job = self.summary()
        self.service.process_one()
        row = self.row(job["id"])
        self.assertEqual(row["status"], "deleted")
        self.assertIsNone(row["payload"])
        self.assertIsNone(row["result"])
        self.assertEqual(row["actual"], 70)
        self.error("operation_deleted", self.summary)

    def test_reading_edit_is_idempotent_recoverable_and_keeps_source_identity(self):
        job = self.reading()
        self.service.process_one()
        edited = self.service.edit_transcript(
            self.uid, job["id"], "Edited first answer", 0, "reading-edit-first")
        self.assertEqual(edited["result"]["revision"], 1)
        self.assertEqual(edited["result"]["readingId"], "reading-001")
        self.assertEqual(edited["result"]["scopeVersion"], self.context["hash"])
        self.assertEqual(edited["result"]["sourceVersion"], "synthetic-reading-001")
        self.assertEqual(edited["result"]["originalTranscript"], "Καλημέρα.")
        replay = self.service.edit_transcript(
            self.uid, job["id"], "Edited first answer", 0, "reading-edit-first")
        self.assertTrue(replay["replayed"])
        self.assertEqual(replay["result"]["revision"], 1)
        recovered = self.service.find_operation(self.uid, "reading-edit-first")
        self.assertEqual(recovered["id"], job["id"])
        self.assertIsNone(self.service.find_operation("another-owner", "reading-edit-first"))
        self.service.edit_transcript(self.uid, job["id"], "Second edit", 1, "reading-edit-second")
        old_retry = self.service.edit_transcript(
            self.uid, job["id"], "Edited first answer", 0, "reading-edit-first")
        self.assertEqual(old_retry["result"]["revision"], 2)
        self.assertEqual(old_retry["result"]["transcript"], "Second edit")
        self.error("operation_conflict", self.service.edit_transcript,
                   self.uid, job["id"], "Changed replay content", 0, "reading-edit-first")
        self.error("transcript_conflict", self.service.edit_transcript,
                   self.uid, job["id"], "Stale new edit", 0, "reading-edit-stale")
        self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (1, 0))

    def test_finished_partial_conversation_cannot_be_revived_by_edit(self):
        conv = self.conversation()
        job = self.typed_turn(conv)
        self.service.process_one()
        conv = self.service.get_conversation(self.uid, conv["id"])
        finished = self.service.finish_conversation(self.uid, conv["id"], conv["revision"])
        self.assertEqual(finished["status"], "partial")
        retry = self.service.finish_conversation(self.uid, conv["id"], conv["revision"])
        self.assertEqual(retry["revision"], finished["revision"])
        self.error("conversation_finished", self.service.edit_transcript,
                   self.uid, job["id"], "Edited answer", finished["revision"], "partial-edit-operation")
        self.assertEqual(self.provider.text_calls, 1)
        self.assertIsNone(self.service.find_operation(self.uid, "partial-edit-operation"))

    def test_full_dialogue_and_latest_edit_are_replay_safe_and_stay_completed(self):
        conv = self.conversation()
        for number in range(4):
            job = self.typed_turn(conv, "turn-operation-%d" % number)
            original_revision = conv["revision"]
            self.service.process_one()
            self.assertEqual(
                self.service.text_turn(self.uid, conv["id"], original_revision,
                                       "Synthetic answer", "turn-operation-%d" % number)["id"],
                job["id"])
            conv = self.service.get_conversation(self.uid, conv["id"])
        self.assertEqual((conv["status"], conv["turnCount"]), ("completed", 4))
        edited = self.service.edit_transcript(
            self.uid, job["id"], "Final revised answer", conv["revision"], "final-edit-operation")
        self.service.process_one()
        repeated = self.service.edit_transcript(
            self.uid, job["id"], "Final revised answer", conv["revision"], "final-edit-operation")
        self.assertEqual(repeated["id"], edited["id"])
        final = self.service.get_conversation(self.uid, conv["id"])
        self.assertEqual((final["status"], final["turnCount"]), ("completed", 4))
        self.assertEqual(self.provider.text_calls, 5)

    def test_voice_retry_after_revision_advance_has_no_second_transcription(self):
        conv = self.conversation()
        args = (self.uid, "dialogue", self.run_id, "ru", "voice-turn-operation",
                self.audio, "audio/wav")
        job = self.service.upload(*args, conversation_id=conv["id"], revision=0)
        self.service.process_one()
        replay = self.service.upload(*args, conversation_id=conv["id"], revision=0)
        self.assertEqual(replay["id"], job["id"])
        self.assertEqual(self.service.get_conversation(self.uid, conv["id"])["turnCount"], 1)
        self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (1, 1))
        self.assertEqual(list(self.service.spool.glob("*.audio")), [])

    def test_options_have_unique_truthful_scenarios_and_latest_owned_readings(self):
        first = self.reading("first-reading-operation")
        self.service.process_one()
        self.clock.value += 1
        latest = self.reading("latest-reading-operation")
        self.service.process_one()
        other = self.reading("another-reading-operation", "reading-002")
        options = self.service.options(self.uid, self.run_id, "ru")
        scenarios = options["dialogues"]
        self.assertEqual(len({item["id"] for item in scenarios}), len(scenarios))
        self.assertEqual(scenarios[0]["firstQuestion"], self.conversation()["question"]["text"])
        self.assertEqual(options["dialogueTurns"], [4, 5])
        jobs = {item["readingId"]: item for item in options["readingJobs"]}
        self.assertEqual(jobs["reading-001"]["id"], latest["id"])
        self.assertNotEqual(jobs["reading-001"]["id"], first["id"])
        self.assertEqual(jobs["reading-002"]["id"], other["id"])
        self.assertEqual(self.service.options("another-owner", self.run_id, "ru")["readingJobs"], [])
        self.assertEqual(self.service.options(self.uid, self.run_id, "en")["readingJobs"], [])
        self.context["questions"].pop()
        self.assertEqual(self.service.options(self.uid, self.run_id, "ru")["dialogueTurns"], [4])

    def test_disabled_retention_hides_expired_reads_and_purges_all_personal_text(self):
        job = self.reading()
        self.service.process_one()
        self.service.edit_transcript(self.uid, job["id"], "Edited reading", 0, "retention-edit-operation")
        conv = self.conversation()
        self.typed_turn(conv)
        self.service.process_one()
        self.seed_run("legacy-owner", "legacy-abandoned-run", age=31 * 86400, completed=False)
        self.seed_run("legacy-owner", "legacy-completed-run", age=31 * 86400)
        orphan = self.service.spool / "orphan.audio"
        orphan.write_bytes(b"synthetic")
        os.utime(orphan, (self.clock() - 4000, self.clock() - 4000))
        self.clock.value += ai_service.TEXT_RETENTION + 1
        self.config.stage = "disabled"
        self.assertEqual(self.service.get_job(self.uid, job["id"])["status"], "deleted")
        self.assertIsNone(self.service.get_job(self.uid, job["id"])["result"])
        self.assertEqual(self.service.find_operation(self.uid, "retention-edit-operation")["status"], "deleted")
        expired = self.service.get_conversation(self.uid, conv["id"])
        self.assertEqual((expired["status"], expired["history"], expired["question"]), ("deleted", [], None))
        self.assertEqual(self.service.list_conversations(self.uid, self.run_id), [])
        counts = self.service.collect()
        self.assertEqual(counts["evidence"], 3)
        row = self.row(job["id"])
        self.assertEqual((row["status"], row["payload"], row["result"], row["actual"]),
                         ("deleted", None, None, 75))
        self.assertFalse(orphan.exists())
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM lesson_evidence_runs").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM lesson_evidence_tombstones").fetchone()[0], 3)
            state = db.execute("SELECT state FROM ai_conversations WHERE id=?", (conv["id"],)).fetchone()[0]
            self.assertEqual(state, "{}")

    def test_retention_work_is_batched_and_evidence_read_cannot_reveal_old_snapshot(self):
        for number in range(ai_service.MAINTENANCE_BATCH + 2):
            self.seed_run("stale-owner", "stale-run-%03d" % number, age=31 * 86400,
                          completed=bool(number % 2))
        counts = self.service.collect()
        self.assertEqual(counts["evidence"], ai_service.MAINTENANCE_BATCH)
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM lesson_evidence_runs WHERE user_id='stale-owner'").fetchone()[0], 2)
        self.error("lesson_evidence_unavailable", ai_service.Service._context,
                   self.service, "stale-owner", "stale-run-101", "ru")
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM lesson_evidence_runs WHERE user_id='stale-owner'").fetchone()[0], 0)

    def test_maintenance_starts_without_feature_or_provider_key(self):
        observed = threading.Event()
        class MaintenanceProbe(ai_service.Service):
            def collect(inner):
                observed.set()
                return {}
        disabled = ai_service.Config(stage="disabled", key="")
        service = MaintenanceProbe(self.connect, self.app, self.root,
                                   config=disabled, provider=self.provider, start_workers=True)
        try:
            self.assertTrue(observed.wait(2))
            self.assertEqual(len(service.threads), 1)
            self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (0, 0))
        finally:
            service.close()
            for thread in service.threads:
                thread.join(2)
                self.assertFalse(thread.is_alive())

    def test_unknown_assistance_remains_unknown_in_ai_evidence(self):
        snapshot = {
            "chapter": 1, "sourceVersion": "test", "rubricVersion": "test",
            "evidenceComplete": True,
            "evidence": [{"ordinal": 0, "cardId": "synthetic-card",
                          "question": {"prompt": "Test"}, "selected": "Test",
                          "result": {"correct": True, "answer": "Test"},
                          "assisted": None, "hintUsageKnown": False}],
        }
        context = ai_curriculum.build(self.app, snapshot, "ru")
        self.assertIsNone(context["evidence"][0]["assisted"])
        self.assertFalse(context["evidence"][0]["hintUsageKnown"])



    def test_queued_expiry_and_lost_worker_never_retry_paid_requests(self):
        job = self.summary()
        self.clock.value += ai_service.JOB_TTL + 1
        self.assertFalse(self.service.process_one())
        self.assertEqual((self.row(job["id"])["status"], self.row(job["id"])["actual"]), ("failed", 0))
        second = self.reading("lost-worker-operation")
        claimed = self.service._claim()
        self.assertEqual(claimed["id"], second["id"])
        self.clock.value = claimed["lease_until"] + 1
        self.service.collect()
        self.assertEqual(self.row(second["id"])["status"], "unknown")
        self.assertIsNone(self.row(second["id"])["actual"])
        self.assertFalse(self.service.process_one())
        self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (0, 0))
        self.assertEqual(list(self.service.spool.glob("*.audio")), [])

    def test_cancel_observed_after_claim_avoids_even_first_paid_call(self):
        job = self.summary()
        claim = self.service._claim
        def cancel_claim():
            row = claim()
            self.service.cancel_job(self.uid, row["id"])
            return row
        with patch.object(self.service, "_claim", side_effect=cancel_claim):
            self.service.process_one()
        self.assertEqual((self.row(job["id"])["status"], self.row(job["id"])["actual"]), ("cancelled", 0))
        self.assertEqual(self.provider.text_calls, 0)

    def test_feature_daily_and_queue_limits_reject_without_leaked_audio(self):
        self.config.stage = "disabled"
        self.error("ai_unavailable", self.reading)
        self.config.stage = "enabled"
        self.config.per_job_limit = 1
        self.error("ai_budget_limit", self.summary)
        self.config.per_job_limit = 100_000
        self.config.daily_jobs = 1
        self.summary()
        self.error("ai_daily_limit", self.reading)
        self.config.daily_jobs = 100
        self.config.queue_limit = 1
        self.error("ai_queue_full", self.reading)
        self.assertEqual(list(self.service.spool.glob("*.audio")), [])
        self.assertEqual((self.provider.audio_calls, self.provider.text_calls), (0, 0))

    def test_provider_snapshot_is_retained_as_bounded_accounting_metadata(self):
        model = ai_provider.TEXT_MODEL + "-2026-11-01"
        self.provider.text_usage["providerModel"] = model
        job = self.summary()
        self.service.process_one()
        usage = json.loads(self.row(job["id"])["usage"])
        self.assertEqual(usage["calls"][0]["usage"]["providerModel"], model)
        self.assertEqual(usage["model"], ai_provider.TEXT_MODEL)
        self.assertEqual(usage["costBasis"], "conservative_tariff_estimate")



    def test_cached_summary_has_durable_receipt_for_new_operation_id(self):
        first = self.summary("original-summary-op")
        self.service.process_one()
        cached = self.summary("cached-summary-op")
        self.assertEqual(cached["id"], first["id"])
        self.assertEqual(self.service.find_operation(self.uid, "cached-summary-op")["id"], first["id"])
        self.assertIsNone(self.service.find_operation("another-owner", "cached-summary-op"))
        self.assertEqual(self.summary("cached-summary-op")["id"], first["id"])
        self.error("operation_conflict", self.service.summary,
                   self.uid, "different-run-id", "ru", "cached-summary-op")
        with self.service.db() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM ai_jobs").fetchone()[0], 1)
        self.assertEqual(self.provider.text_calls, 1)
        self.service.erase(self.uid)
        self.assertEqual(self.service.find_operation(self.uid, "cached-summary-op")["status"], "deleted")
        self.error("operation_deleted", self.summary, "cached-summary-op")


class UsageParserTests(unittest.TestCase):
    def test_unexpected_usage_is_unknown_and_never_throws(self):
        values = [None, "", [], {}, {"input_tokens": -1, "output_tokens": 2},
                  {"input_tokens": True, "output_tokens": 2},
                  {"input_tokens": 2, "output_tokens": 2, "input_tokens_details": []},
                  {"input_tokens": 2, "output_tokens": 2,
                   "input_tokens_details": {"cached_tokens": None}},
                  {"input_tokens": 2, "output_tokens": 2,
                   "input_tokens_details": {"cached_tokens": 3}},
                  {"input_tokens": 2, "output_tokens": 2,
                   "input_tokens_details": {"cache_write_tokens": "bad"}}]
        for value in values:
            with self.subTest(value=value):
                self.assertIsNone(ai_provider.text_cost(value))
        for value in (None, {}, {"type": "duration"}, {"type": "duration", "seconds": None},
                      {"type": "duration", "seconds": "1"}, {"type": "duration", "seconds": -1},
                      {"type": "duration", "seconds": float("nan")},
                      {"type": "duration", "seconds": float("inf")},
                      {"type": "duration", "seconds": True}):
            with self.subTest(value=value):
                self.assertIsNone(ai_provider.audio_usage_cost(value))
        self.assertEqual(ai_provider.text_cost({"input_tokens": 20, "output_tokens": 10}), 70)
        self.assertEqual(ai_provider.text_cost({"input_tokens": 100, "output_tokens": 10,
                                              "input_tokens_details": {"cached_tokens": 20,
                                                                       "cache_write_tokens": 20}}), 161)
        self.assertEqual(ai_provider.audio_usage_cost({"type": "duration", "seconds": 1}), 75)



    def test_explicit_bad_budget_values_fail_closed(self):
        self.assertEqual(ai_service._usd(None, 123), 123)
        self.assertEqual(ai_service._usd("  ", 123), 123)
        self.assertEqual(ai_service._usd("0.50", 123), 500_000)
        for value in ("invalid", "-1", "nan", "inf", "1e309"):
            with self.subTest(value=value):
                self.assertEqual(ai_service._usd(value, 123), 0)
        with patch.dict(os.environ, {"LEXI_AI_MONTH_USD": "invalid",
                                     "LEXI_AI_DAY_USD": "-1", "LEXI_AI_JOB_USD": "nan"}):
            config = ai_service.Config.environment()
        self.assertEqual((config.month_limit, config.day_limit, config.per_job_limit), (0, 0, 0))

    def test_model_response_metadata_is_captured_without_network(self):
        provider = ai_provider.OpenAIProvider("synthetic-never-sent")
        text_model = ai_provider.TEXT_MODEL + "-2026-11-01"
        response = {"status": "completed", "model": text_model,
                    "usage": {"input_tokens": 3, "output_tokens": 2},
                    "output": [{"content": [{"type": "output_text", "text": "{}"}]}]}
        with patch.object(provider, "_post", return_value=response):
            _, usage = provider.text("test", {}, {})
        self.assertEqual(usage["providerModel"], text_model)
        audio_model = ai_provider.AUDIO_MODEL + "-2026-11-01"
        response = {"model": audio_model, "text": "Καλημέρα.",
                    "usage": {"type": "duration", "seconds": 1}}
        with patch.object(provider, "_post", return_value=response):
            _, usage = provider.transcribe(b"synthetic", "audio/wav", "wav")
        self.assertEqual(usage["providerModel"], audio_model)
        self.assertEqual(ai_provider.audio_usage_cost(usage), 75)

    def test_unknown_billing_shapes_and_model_tariffs_remain_reserved(self):
        for extra in ({"providerModel": {}}, {"providerModel": "different-model"},
                      {"new_billing_tier": 5},
                      {"input_tokens_details": {"cache_write_12h_tokens": 5}}):
            usage = {"input_tokens": 10, "output_tokens": 5, **extra}
            with self.subTest(usage=usage):
                self.assertIsNone(ai_provider.text_cost(usage))
        self.assertIsNone(ai_provider.text_cost({"input_tokens": 10**1000, "output_tokens": 1}))
        self.assertIsNone(ai_provider.audio_usage_cost({"type": "duration", "seconds": 1,
                                                       "providerModel": []}))
        self.assertIsNone(ai_provider.audio_usage_cost({"type": "duration", "seconds": 10**30}))

    def test_reading_alignment_preserves_surface_greek_and_ignores_tonos_only(self):
        result = ai_curriculum.reading_result("Καλημέρα φίλε.", "Καλημέρα κόσμε.")
        self.assertEqual(result["comparison"],
                         [{"type": "replace", "expected": "φίλε", "recognized": "κόσμε"}])
        self.assertFalse(result["pronunciationAssessed"])
        equivalent = ai_curriculum.reading_result("Καλημέρα.", "ΚΑΛΗΜΕΡΑ.")
        self.assertTrue(equivalent["matchingContent"])
        decomposed = ai_curriculum.reading_result("Καλημε\u0301ρα.", "Καλημέρα.")
        self.assertTrue(decomposed["matchingContent"])



    def test_model_metadata_does_not_make_missing_billing_usage_known(self):
        provider = ai_provider.OpenAIProvider("synthetic-never-sent")
        response = {"status": "incomplete", "model": ai_provider.TEXT_MODEL,
                    "output": []}
        with patch.object(provider, "_post", return_value=response):
            with self.assertRaises(ai_provider.ProviderError) as caught:
                provider.text("test", {}, {})
        self.assertTrue(caught.exception.uncertain)
        self.assertIsNone(ai_provider.text_cost(caught.exception.usage))


if __name__ == "__main__":
    unittest.main(verbosity=2)
