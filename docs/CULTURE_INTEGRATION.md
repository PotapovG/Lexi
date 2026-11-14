# CULT-03 — Culture on the existing Lexi engine

This is a deliberately small **adapter**, not a parallel application or second
quiz backend. Completed schema/validation foundation: #34 / PR #43. Feature
tracking: #33; technical integration: #36.

## Reuse / extension matrix

| Existing component | Reused | Minimal extension |
| --- | --- | --- |
| `server.py make_quiz` | Normal shared selection contract | `scope=culture` selection from authored `content/culture`, four answers, distinct `factId` |
| `server.py format_question / shape` | One question payload renderer | Culture card adapter produces safe Greek-only pre-answer payload |
| `server.py mark` | Existing server grader, progress/mistake/SRS updates | Check selected option within four validated choices and store assisted flag; localized explanations only **after** scoring |
| `answer_idempotency.py` | Existing request receipt/replay | Signature includes `assisted` **only when present** so historical hashes stay valid |
| `learning_engine.py` | Existing shared SRS schedule and pace | Optional scope filter on counters; Greek quiz pace excludes culture |
| `server.py stats / weak / leaderboard` | Existing attempts/progress/weak + UI contract | `cyq_*` filter; Culture-only stats projection, A1/A2 remains unchanged |
| `vocab_lessons.py` | Existing vocabulary engine | No changes in CULT-03, future #38 |
| `lesson_session_sync.py` | Existing cross-device lesson progress | No changes; **untrusted for secure exam deadline/answer key**; future #39 |
| `index.html / app.js` | Existing UI | No changes in CULT-03; one Culture mode in #37 |

## Existing endpoints, no second backend

- `GET /api/catalog?scope=culture`: source topic codes, current verified question counts and supported locales.
- `GET /api/quiz?scope=culture&lang=ru&mode=all&count=25`: existing quiz payload, with `kind=culture`, `direction=culture_select`, four Greek alternatives.
- `GET /api/quiz?scope=culture&mode=weak` or `mode=srs_due`: same Lexi weak/SRS engine, filtered to Culture.
- `POST /api/answer`: existing idempotent grading, accepts an authored choice string and optional `assisted` for study. Full localized explanations/source visible **after** scoring only.
- `GET /api/stats?scope=culture`: filtered aggregation of the shared attempts/progress table. Existing `/api/stats` continues to show ordinary A1/A2.
- `GET /api/srs/status?scope=culture`: filtered shared SRS counters; unscoped shows ordinary course counts.

**Important:** no real questions have been published yet. `tests/fixtures/culture/`
contains *draft-only synthetic examples*, loaded only by integration tests and
never returned through the actual live catalog. Content generation #35 is a
separate task.

## Persistence

Same SQLite database and **same** `progress`, `attempts`,
`srs_schedule` and `answer_receipts`. Culture question IDs begin
`cyq_`, and practice key is `cyq_…:culture_select` with no locale suffix
because the Greek question and choices are the same regardless of explanation
language. No additional user progress, SRS, profile or scores tables.

One safe additive schema migration: `attempts.assisted INTEGER NOT NULL DEFAULT 0`.
Existing rows remain independent answers with assisted=0. Correct assisted
answers are recorded as attempts but do **not** add independent mastery,
advance SRS, or clear error debt. (Users can self-declare use of a client hint
in study mode; this is not an anti-cheat mechanism.)

## Security boundary — CULT-06 (#39)

The **existing practice** `POST /api/answer` is intentionally immediate
feedback and cannot be used for a mock-exam secret key. The real 25-question/
45-minute mock must add a server-authoritative session profile and withhold
grading/feedback until final submission. Specifically, for an active mock
question, **block any bypass using the normal `/api/answer` endpoint**;
neither the normal quiz nor the client-provided session snapshot may be trusted
as exam-key or deadline. Exam session snapshot may require one focused
`culture_exam_sessions` table; do not create another quiz engine.

Until #39 exists, `scope=culture` means **study/practice only**, never
a simulated exam. Until #37 exists, it is an API adapter, not a user-visible
mode. Both stay undisplayed before their respective acceptance checks.

## Test / acceptance

```bash
python3 culture_content.py
python3 qa_culture_content.py
python3 qa_culture_integration.py
python3 tests/test_selfhost.py
python3 tests/test_content_guard.py
python3 tests/test_community_content.py
```

`qa_culture_integration.py` uses a new temporary SQLite DB and injects
synthetic fixtures into the test process only; it asserts safe four-choice
payloads, negative answer/repeat, RU/EN, weak/SRS, assisted, idempotency,
no culture attempts in A1/A2 statistics, and no new standalone backend.

No direct production, GitOps, main branch protection or deployed DB change is
part of this issue.
