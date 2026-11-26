# Optional AI learning experience

Status: implementation available behind default-off gates; live provider access,
Greek speech quality and the learner pilot are **not yet validated**.
Scope: [#54–65](https://github.com/PotapovG/Lexi/issues/54), authorized by the
owner on 2026-11-26. This extends existing lesson results and practice; it adds
no separate course, mode, grading system or spaced-repetition ledger.

## Learner contract

A completed guided lesson keeps its ordinary deterministic result. The learner
may request a short AI summary, read an eligible existing dialogue aloud, or
answer four or five short questions. Every AI action is optional. Cancelling,
a provider failure, a budget limit or a missing key does not prevent continuing
the course.

A summary uses the completed run's first submitted answers. It distinguishes
graded, skipped, unverified and assisted evidence. Where hint use was not
recorded, that fact remains unknown. Historical aggregate-only lessons do not
receive invented answer evidence. At most two improvement points are shown;
examples must occur in cited evidence, and the proposed review card must be an
existing card within the lesson's chapter scope. These structural checks do not
prove the semantic truth of generated prose: feedback remains advisory and
requires a real pilot.

Reading recognition is independent of the displayed reference: the full
reference and keyword hints are not sent to transcription. The UI shows
recognized text and tentative differences, permits an explicitly marked text
correction, and invites another attempt. Tonos, punctuation, orthographic
homophones and ASR spelling are not pronunciation evidence. There is no
pronunciation percentage, phoneme grade, acoustic diagnosis or invented timing.

A repeat action switches the reference to the selected phrase. The learner
records only that phrase and receives a separate comparison; the original
full-reading result stays unchanged. Saved phrase attempts can be reopened
without another upload or paid request, and the learner can return to the
whole text. A changed or expired source asks the learner to select a current
phrase again instead of silently comparing against a different reference.

A dialogue uses voice input and text output, with explicit text entry as a
meaning-only fallback. A meaningful but grammatically imperfect answer counts;
an uncertain recognition does not silently consume a turn. The server owns the
question, accepted turn count and revision. The fifth answer in a five-turn
conversation ends it. Finishing early creates a partial result. Original and
edited transcripts retain their provenance. AI results never rewrite ordinary
attempts, mastered cards, XP or SRS. The next-step button opens the existing
review surface with a truthful label; it does not promise an exact-card drill
that the existing interface cannot provide.

## Materials and versioning

The pilot reading pool reuses `dlg001` through `dlg006` from the existing
authored corpus. Eligibility checks both the printed chapter and the grammar
milestone. Questions are selected from a server-owned list derived from those
dialogues; the model cannot choose a question outside that list. The immutable run, derived context/hash and job usage metadata together record
source, rubric and prompt versions appropriate to each operation.

This intentionally small pool is not a claim of complete chapter coverage.
Some early completed lessons have reading but insufficient eligible questions
for a four/five-turn dialogue. The UI follows the returned availability. It
does not fill gaps with future grammar. Context explicitly records
`textbookVocabularyFullyVerified=false` and the pilot review requirement.
Independent Greek and six-language editorial review remain open, as does the
precise lexical review in #51. No purchased textbook is used by these modules.

## Configuration

All settings are server-side. Never put keys, access codes, real transcripts,
recordings, learner identities or a database into GitHub or browser storage.

| Variable | Default | Purpose |
|---|---|---|
| `LEXI_AI_STAGE` | `disabled` | `disabled`, `internal`, `pilot`, `enabled` |
| `LEXI_OPENAI_API_KEY` | empty | Dedicated server API key; an empty value disables calls |
| `LEXI_AI_FEATURES` | empty | Comma-separated `summary,reading,dialogue` |
| `LEXI_AI_COHORT` | empty | Explicit account IDs for internal/pilot access |
| `LEXI_AI_SPEECH_VALIDATED` | `0` | Must be `1` for enabled speech features after the relevant A/B decisions |
| `LEXI_AI_MONTH_USD` | `10` | Global monthly admission budget in USD |
| `LEXI_AI_DAY_USD` | `0.50` | Per-account UTC calendar-day admission budget |
| `LEXI_AI_JOB_USD` | `0.10` | Maximum reservation for one job |

The deployment has a maximum of two active provider jobs shared through SQLite,
a bounded queue of sixteen, forty jobs per account per day and ten dialogue
starts per day. Transcription is limited to 90 seconds for reading and 45
seconds per dialogue answer, with a 10 MiB body limit. JSON bodies are limited
to 16,000 bytes; transcript length and model output length are separately bounded.
Each serving process admits at most two audio preparations before reading the
body. Excess requests receive `429 ai_preparation_busy`; disabled features
reject before upload. These short-lived preparation slots are separate from
the globally coordinated provider queue.

The default Docker image needs only Python's standard library and remains
usable without AI. Compressed browser audio additionally requires `ffmpeg`
and `ffprobe`. Build with `--build-arg WITH_AI_AUDIO=1`, or use the provided
opt-in override:

```bash
docker compose -f compose.yaml -f compose.ai.yaml config --quiet
docker compose -f compose.yaml -f compose.ai.yaml up -d --build
```

Keep actual values in a private deployment environment, with owner-only file
permissions. The override defaults to disabled and does not activate billing,
redeem subscriber credits or create a provider project. A ChatGPT subscription
does not itself supply the application with a server API key. Confirm model
access and available project credits before the controlled live probe.

A host install should place the same environment values in its existing
protected service environment and restart both serving processes through the
normal release procedure. Do not print secrets in shell commands, service
status output, screenshots or issue comments. Keep the established exact
`GREEK_ORIGIN`, private upstream and HTTPS configuration.

## Transport, costs and failure handling

The adapter uses the official fixed OpenAI API origin, without arbitrary base
URLs, provider tools, redirects, background responses or automatic paid retries.
Text uses Responses with `store:false`, strict JSON Schema,
`reasoning.effort=none` and a 900-token output cap. Refusal, incomplete
generation, malformed JSON and business-schema failures have separate safe
error states. Recognized learner text is untrusted input, never instructions.

The initial configured models are `gpt-6.1-terra` for text and
`gpt-transcribe` for file transcription. Their documented standard prices on
2026-11-26 are $1 input / $5 output per million text tokens and $0.0045 per
audio minute; caching tariffs differ. See the official model pages below.
Cost accounting is a tariff estimate based on returned usage, not the
provider's invoice. Reconcile a controlled probe against billing before a
learner pilot, and re-check prices and model behavior when changing versions.

Before queueing, a short SQLite write transaction reserves a conservative
amount. Global and account limits include queued/running reservations and
unknown-outcome reservations. A missing or malformed paid usage report never
becomes zero spend. Known usage is settled after a response, including after
cancellation. Actual billed values may differ from estimates.

Submissions and transcript edits have an owner-bound operation identifier and
content fingerprint; cancellation, reporting, early finish and erasure use
ownership and their applicable state/revision checks.
A lost browser response is recovered from the operation receipt before another
submission. Reusing the same identifier with a different body conflicts. A
restart or expired worker lease turns a potentially paid in-flight call into
an unknown outcome; it is not blindly retried. An explicit subsequent attempt
is a new operation and may incur a new charge. The learner can continue the
ordinary course while an AI result is unavailable.

The queue stores leases and revisions in the existing SQLite database. No
network call runs while holding the database write transaction. The same
database coordinates primary/secondary workers. Deleted-owner generations
fence requests that captured context before erasure, as well as late workers.

## Data lifecycle

| Data | Application handling |
|---|---|
| Raw recording | Private temporary spool; removed after terminal processing/cancellation, with orphan cleanup after one hour |
| Transcript, AI result, dialogue context | Owner-scoped, maximum 30-day application retention |
| Completed lesson answer evidence | Immutable per run, retained for 30 days for optional feedback |
| Operation tombstone and cost metadata | May remain without learner text to prevent replay and preserve budget accounting |
| Ordinary course attempts and SRS | Existing retention and semantics; AI erase does not alter them |

Maintenance starts independently of whether paid features are enabled. Reads
also exclude expired payloads, so disabling AI does not make expired feedback
available. Deletion clears AI text/evidence, cancels outstanding work and
prevents late results from restoring it. Provider usage can still be settled
for an already-started request.

The application does not log raw audio, transcripts, prompts, provider error
bodies or API keys. A feedback report stores an owner-bound reason enum, not
a copied conversation. Backups are an operator responsibility: apply matching
expiry/access rules to private database backups, and exclude `ai-spool/`
from backups. Application erasure cannot erase historical backup copies or
content already transmitted to a provider.

OpenAI's independent data controls apply to submitted content.
`store:false` is not a promise that all provider-side retention is zero.
Review the official data-controls page and the actual project's configuration
before the pilot; do not advertise unconfigured Zero Data Retention.

## HTTP surface

All routes are under the existing authenticated `/greek/api/ai/` path.
Every write requires the configured same origin and
`X-Lexi-Owner` equal to the non-secret `accountKey` from `GET /api/profile`,
before the body is read. The server compares that displayed-owner marker with
the account authenticated by the current cookie. A cross-tab account switch
returns `409 account_changed`, including for erase, rather than applying an
old view's action to a new account. Clients invalidate context and refresh the
profile; they must not replay that action under the new account.

| Method and suffix | Purpose |
|---|---|
| GET `capabilities` | Enabled features, device decoder availability, limits |
| GET `options?runId=…&lang=…` | Eligible existing materials and saved results |
| POST `summary` | Request/recover one cached summary per completed run and locale |
| POST `conversations` | Start an eligible four/five-turn conversation |
| POST `audio?…` | Bounded raw audio body; no base64 expansion |
| GET `jobs/:id` | Owner-scoped job/result status |
| GET `operations/:operationId` | Resolve an uncertain submission result |
| POST `jobs/:id/cancel` | Cancel processing and remove queued audio |
| POST `jobs/:id/transcript` | Explicit revision-safe transcript correction |
| POST `jobs/:id/report` | Report incorrect/irrelevant/unclear feedback |
| GET `conversations/:id` | Resume server-owned conversation |
| POST `conversations/:id/text` | Explicit meaning-only typed fallback |
| POST `conversations/:id/finish` | Finish early without inventing accepted turns |
| POST `erase` | Erase AI data with explicit confirmation |

Use the normal account cookie, not a new AI identity. There is no public audio
download endpoint. Audio duration comes from bounded server decoding, not a
client-supplied timer. Unsupported formats and silent recordings fail before
any paid call.

For a phrase repeat, `audio` keeps `kind=reading`, `runId`, `lang` and
`readingId`, and adds `sourceJobId`, `sourceRevision` and `differenceIndex`.
The server derives the phrase from its own successful full-reading result;
client-provided reference text is rejected. Owner, run, locale, source revision,
retention and curriculum versions are checked again inside the short enqueue
transaction after decoding. Operation replay is resolved first, so a committed
retry remains idempotent if the parent transcript was later edited. The child
job preserves a `fragment` descriptor and its own reference. `options` returns
full results in `readingJobs` and phrase attempts separately in `readingRepeats`.

## Pilot and release gates

The delivery does not mark #61 or #65 complete. Automated tests use synthetic
accounts and fake providers; synthetic tone audio checks container handling,
not Greek recognition quality.

1. **Internal text probe:** activate credits/API access, set a small dedicated
   project limit, enable only `summary` for a test account. Confirm real usage,
   refusal handling, latency and evidence accuracy on new completed runs.
2. **Independent speech evaluation (#61):** collect approximately 40–60
   consented real recordings, separate tuning/control material and involve a
   person capable of independently judging Greek. Include correct speech with
   different accents, genuine reading errors, stress changes, accepted variants,
   self-corrections, silence/noise and cut-off audio. Keep recordings and
   transcripts outside public Git.
3. **Decide A/B/C separately:** A is ASR plus meaning for dialogues; B is reading
   alignment; C is acoustic pronunciation guidance. This implementation has no
   C feature. No-go for C does not prevent A or B after their own review. The
   preliminary false-correction target on correct control answers is ≤5%;
   it is not a provider guarantee or broad scientific validation.
4. **Small learner pilot (#65):** 3–5 volunteers, all three features, actual iOS
   Safari and Android Chrome microphones, denied permission, hidden tab,
   interrupted upload, reload, wrong language, repeat, deletion and provider
   outage. Check lesson completion and ordinary SRS alongside AI.
5. **Gradual activation:** retain a small cohort and budget first. Record the
   model identifier, rubric version, observed costs, defects and separate A/B
   decisions in the issues. Only then expand `LEXI_AI_STAGE` and features.

The offline helper aggregates a private evaluation manifest:

```bash
python3 scripts/evaluate_ai_speech.py /private/path/manifest.json > /private/path/aggregate.json
```

Start from `docs/AI_EVALUATION_TEMPLATE.json`. Each sample supplies a unique
anonymous `id`, anonymous `speaker`, `origin:"human"`, `consent:true`,
`referenceReviewed:true`, `split:"tuning"|"control"`, `device`
(`ios_safari`, `android_chrome`, `desktop`), `category` (`correct`,
`reading_error`, `stress_shift`, `accepted_variant`, `self_correction`,
`silence`, `noise`, `cut_off`), human `spoken` transcript, independent
`recognized` transcript, `falseCorrection`, `abstained`,
`latencySeconds` and `costUsd` (null when unknown). The manifest records
`modelSnapshot` and `rubricVersion`.

The helper emits aggregate rates/counts only and always leaves final A/B
decisions to the reviewer. Its coverage thresholds are pilot gates, not
statistical proof. Normalized word error rate ignores tonos/punctuation and
does not measure stress or pronunciation. An empty template reports pending,
and synthetic recordings cannot satisfy the human evaluation gate.

To stop paid features, set stage to `disabled` (or remove the key) and restart
through the established release process. Retention maintenance continues.
Keep existing GitOps protection and green-CI requirements; an unprotected
`main` is a deployment blocker, not a reason to bypass the puller.

## Verification commands

```bash
python3 tests/test_learning_reliability.py
python3 tests/test_ai_curriculum.py
python3 tests/test_ai_service.py
python3 tests/test_ai_routes.py
python3 tests/test_ai_transport.py
python3 tests/test_ai_evaluation.py
node tests/test_learning_ui.cjs
node tests/test_ai_ui.cjs
```

Browser tests use the isolated runner described in `tests/test_learning_ui.cjs`
and mock provider responses for the optional AI UI. CI checks both source/image
catalog parity and the ordinary course while AI is off. Manual linguistic
review and physical mobile-device recording remain distinct requirements.

## Official references

Contracts and prices checked 2026-11-26:

- [GPT-6.1 Terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra)
- [GPT-Transcribe](https://developers.openai.com/api/docs/models/gpt-transcribe)
- [File transcription](https://developers.openai.com/api/docs/guides/speech-to-text)
- [Create transcription API](https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create)
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses)
- [Data controls](https://developers.openai.com/api/docs/guides/your-data)
