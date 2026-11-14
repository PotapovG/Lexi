# CULT-06 — Sealed mock exam backend (foundation, not public launch)

This is a minimal server-authoritative **exam session profile** in the
existing Lexi application. Reuses `server.py`, existing authentication,
SQLite and Culture question cards. It adds exactly **one** table,
`culture_exam_sessions`, to store immutable exam selections and
answers. It does **not** introduce another training engine, account,
learning progress ledger, vocabulary store or SRS.

## Endpoints (existing /greek/api/ router)

Authenticated only, existing cookie and Origin / JSON requirements:

- `GET /api/culture/exam` — latest active exam or last finished result.
  Optional `?sessionId=<uuid>` retrieves own historical snapshot.
- `POST /api/culture/exam` with `action=start`,
  `requestId=<uuid>`, `lang=ru|en`, `goal=citizenship`.
- `POST /api/culture/exam` with `action=answer`,
  `sessionId`, `questionId`, `selectedIndex=0..3|null`,
  `revision`, `requestId=<uuid>`. The answer **may be changed**
  before exam completion by a later request with the latest revision.
- `POST /api/culture/exam` with `action=flag`,
  `sessionId`, `questionId`, `flagged=true|false`, `revision`,
  `requestId=<uuid>` for the "return to" marker.
- `POST /api/culture/exam` with `action=finish`, `sessionId`,
  `revision` finishes and releases the review.

The server fixes the question set, shuffled option order, scoring
key, `startedAt` and `deadlineAt` (45 minutes). It always selects
**exactly 25 distinct, fresh `factId`** or refuses to begin (no
fallback to a partial exam). A non-empty Culture question bank must
have already passed the `culture_adapter.load` editorial publication
gate. The currently available authored PR #45 contains **drafts only**,
so there is no public practice or exam yet.

## Information isolation

Before finish, responses include only:

- session id, revision, state, server UTC timestamps and time remaining
  metadata, goal and translated **interface language**;
- Greek question, four shuffled Greek choices, selected option
  index and a manual flag.

**No** `correctIndex`, feedback, RU/EN question/choice translations,
source or explanation until completed. Wrong/unfinished are not scored
client-side. Explicit finish or expiration is handled by SQLite
transaction on the server; completed results cannot be edited.

The existing `/api/answer` path, including replay of already stored
idempotency receipts, is denied for Culture cards while the same
account has an active unexpired exam. `GET /api/quiz?scope=culture`
is also denied during this interval. The ordinary lesson/session
payload cannot change the authoritative exam deadline or hidden
answer key.

This prevents a **same-account API answer side channel**. It is not
proctoring: an independently studying person can look up public facts
outside the simulator. Do not describe it as a secure government exam.

## Persisted schema and race handling

`culture_exam_sessions`: one active row per user (partial unique
index), many completed rows for history. The row holds sealed JSON
snapshot and request receipts. Writes are serialized with
`BEGIN IMMEDIATE` and use optimistic `revision`. Same
`requestId` + same payload is idempotent, reusing it for a different
answer fails. Finish is idempotent.

Expired sessions finalize automatically upon the next exam request.
A new exam can start afterward, with a new unique `start_key`.
All read/write paths filter by the authenticated `user_id`, including
historical sessions. Date arithmetic is in UTC server time.

**No exam answers are automatically written to ordinary SRS or weak
review yet.** That integration must happen only after completion and
must be idempotent, without leaking scores via `/api/answer` during
an exam. It is a remaining #39 deliverable.

## Regulatory and product scope

Citizenship `15/25` is currently the only selectable pass threshold.
Long-term residency `13/25` remains **provisional** in data config
and is **not offered as a certified result**, pending verification of
the current official rule. Source: the project content program, not
an official exam implementation.

Current PR implements **backend and unit/integration tests only**.
It does not enable the disabled mock-exam button in Culture UI.
A follow-up UI PR must reuse the existing Lexi quiz UI styling and
the sealed session API, never ordinary immediate-score `choose()`.
Manual 320px, keyboard/reader tests and bank editorial publication
remain to be performed.

## QA

```bash
python3 qa_culture_exam.py
python3 qa_culture_integration.py
python3 tests/test_selfhost.py
```

QA uses 30 **synthetic** cards in a temporary SQLite database,
never released Culture questions or production student records.
Exercises cover 25 unique facts, no pre-finish leaks, restore,
cross-account isolation, reordering, idempotent response, stale
revision, expiry and unscored study-answer endpoint guards.

**No production/GitOps or branch protection changes.**
