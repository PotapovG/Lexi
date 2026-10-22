## 21 October 2026 — Four functional backlog priorities (grammar, sentences, distractors, cross-device)

**Priority 1 — Grammar 2.0 RELEASED.** `grammar2_cards.py` contains 56
independently authored four-option Greek-only cloze/morphology questions:
10 article/case, 10 adjective agreement, 10 comparisons, 10 past/irregular
verb forms, 8 future and 8 subjunctive να. All six locale instructions,
unit gates (4/9/11/12/14/16), analytics, wrong review and SRS.
Original textbook 1795 immutable card IDs and historical progress untouched.
QA: 672 correct/incorrect grades in isolated SQLite; account HTTP
end-to-end, original unit/stress and Pocket regression pass.

**Priority 2 — Sentence builder 2.0 RELEASED.** `order2_cards.py` adds
40 Greek-ordering tasks derived from existing authorial six-locale
sentence items, preserving their taught stages and translations.
Total 65 tap-to-compose tasks. `order_valid_permutations.py` includes
19 additional hand-vetted accepted Greek word orders (33 across old
and new collection). Non-vetted arbitrary permutations remain wrong.
QA: all six language render/score, exact words and existing source
relation, isolated HTTP/SRS, no ID/provenance migration.

**Priority 3 — Distractors 2.0 RELEASED.** `distractor_quality.py` ranks
stored responses by already taught stage, grammatical markers,
article/gender-form hints, topic, similarity and length. Known
accepted Greek spelling variants, duplicate translations and
equal English glosses are excluded from wrong answer candidates.
Still eight distinct options for normal translation drills, no
automatic unreviewed synonym acceptance. QA: 1524 option banks
across five task kinds, two directions, six UI locales.

**Priority 4 — Cross-device active lesson handoff RELEASED.**
`lesson_session_sync.py` creates only `active_lesson_sessions`
in existing account-backed SQLite. Stores at most one active lesson
(<=60 issued question payloads, <=240 KiB), bounded to session
deadline (up to two hours) with revision number and device owner UUID.
`GET/POST /api/session` require a valid registered HttpOnly cookie;
the eight-digit account code is not copied into lesson snapshots.
Local browser still saves progress for reload/offline safety.
On another logged-in device the user explicitly confirms a takeover;
the new owner resumes exact question queue, index, elapsed time,
dialogue/verb stage, pending request UUID and stats. Former owner
gets HTTP409 on new answers/saves after transfer; replay of an
already committed answer is idempotent and safe. Concurrent takeover
uses SQLite optimistic revision CAS and only one winner. Safe
completion clears only own exact session; old clients without
UUID session fields remain compatible for historic practice.
Server per-user snapshot is the active device's latest save
(debounced ~200ms) and cross-device resume is available only
before the original lesson timer expires. No indefinite sync.

**Tests and release:** `qa_cross_device.py` rejects malformed and
oversize snapshots and tests isolated user scope, idempotent starts,
CAS, legacy and clear. `qa_cross_device_http.py` uses two browser
login cookies into one disposable account and another unrelated
account; validates takeover, stale-device denial, safe replay,
stats and parallel takeover. Existing `qa_answer_http.py` validates
24 concurrent same-ID retried writes across two independent backend
workers. All other original catalog, 717 audio, 1700 Pocket A1/A2,
mixed lesson (20% listening), stress, JS grammar and UI regressions
pass. No direct modifications to users' stored progress or IDs.

**Production safety:** source archives
`backups/pre-grammar2-20261021.tgz`,
`backups/pre-order2-20261021.tgz`,
`backups/pre-distractor2-20261021.tgz`,
`backups/pre-cross-device-20261021.tgz` plus consistent read-only
copy of student SQLite in
`backups/pre-cross-device-20261021.sqlite3` (0600, quick_check OK).
All live migrations are additive (one active session table),
deployed through Caddy blue-green; no direct active service restart.
Final production cutover 18561 -> 18560, previous active worker retained;
Caddy rollback: backups/caddy-greek-bluegreen-20261021T095605Z.
Production SQLite PRAGMA quick_check PASS; anonymous
GET /api/session HTTP401. Public catalog 1978 exercise cards,
56 grammar +40 derived builder tasks, 1795 original unchanged.
After deployment: 100 GET HTTP200 +50 expected anonymous POST HTTP401,
zero 502/5xx. Chromium 320px and 1440px loaded login/recovery/grammar
controls. Backend account-handoff workflow tested on isolated HTTP
servers; full two-browser clickthrough was not executed.

**Known limits / next optional editorial work:** New tasks and
translations are authorial pedagogy examples with approximate
source-page anchors and no invented publisher exercise identities.
Not a native-speaker certification or a blanket lexicon proofreading.
Device handoff uses a single active lesson per account, does not
merge two devices' independent progress, and requires same account
code on the second device. Pronunciation via microphone and non-Pocket
TTS remain permanently excluded by owner instruction.

---
## 21 October 2026 — Enclitic additional stress + 20% listening in ordinary sessions

**Status:** implemented, tested, blue-green released. Original textbook
1795-card audit, separate 1700 A1/A2 vocabulary, 717 listening tasks,
all old progress/SRS/due/weak card IDs remain unchanged.

**Authorial double-stress exercise (26 cards):** separate selectable
`enclitic` kind, 9 antepenultimate-stressed noun stems and 4 contrast
stems without the additional accent, each with both possessives
`μου`/`σου`. A student sees article + originally accented bare noun +
possessive and picks the correct complete Greek spelling from four
carefully differentiated accent placements. Models include
`το τηλέφωνο` → `το τηλέφωνό μου`, `το όνομα` → `το όνομά σου`
and non-additional `το βιβλίο` → `το βιβλίο μου`.
Do not confuse possessive clitics with accented indirect-object pronouns
in sentences containing following verbs. Each exercise has explanatory
feedback translated into six languages, own grammar milestone
`enclitic_stress` (after introduction of possessives), dedicated
statistics/weak/SRS support and stable `en261021_NNN` IDs. These
are independent teaching examples with approximate syllabus anchors,
not a claim of exact printed publisher examples/pages.

**Pocket-only word audio:** all 26 complete correct Greek possessive
phrases rendered locally with approved Pocket TTS voices, exact
content-hash manifests, 24kHz mono PCM16, validated non-silent WAVs.
No system voice, microphone or live synthesis. Existing 1555 Pocket
pronunciation recordings and old 1266 listening WAVs remain preserved.

**Embedded listening in normal chapter/page sessions:** configurable
checked-by-default `listenMix=1` introduces up to 1 existing approved
`LISTEN_CARDS` item per 5 answer positions (~20%) when the selected
chapter/page and word/phrase/sentence kinds include eligible audio.
Same lesson length, no repeated card IDs or lexical target doubles.
Users can uncheck to restore pure written practice. Existing standalone
`scope=listening` is unchanged. Dedicated weak/SRS/topics/verbs modes
do not automatically inject extra listening. Capacity endpoint reports
the current listening pool count; server defaults to no mixing for
legacy/API clients not sending the opt-in flag.

**UI:** `app.js?v=40` supports new four-choice Greek orthography
question, proper feedback including why extra tonos appears or doesn't
appear, pocket phrase replay, all six localized mode/settings labels,
skill mapping and persistence of audio-toggle per browser. One-time
saved-materials preference upgrade shows the new kind to returning
learners while keeping the existing material choices. Regular listening
quiz audio still must be played before submitting the translation.

**QA:** `qa_enclitic_listening_mix.py` 26 curated examples x six locales x
both correct and incorrect answers =312 grades in a disposable SQLite;
no leaked answer in question metadata, 26 exact Pocket WAVs and
audios mixed 12/60 without repeats while keeping chapter/page limits.
`qa_enclitic_mix_http.py` tested isolated registered HTTP account,
mixed quiz, 4-choice enclitic, answer replay and counts/statistics.
Original 1795 source ledger, seven-language vocabulary catalog,
full Pocket 1700 corpus, 717 listening, syllable/accent, grammar
mastery, JS syntax, 24-concurrent idempotency, and resume regressions
all passed. Release is blue-green, student SQLite records untouched.

Limitations: this first deck focuses on noun + possessive clitic
combinations (`μου`, `σου`); other enclitic classes/verbs or additional
possessives remain potential separate expansions with explicit review.
Listening proportion is target rather than a hard guarantee for narrow
chapter ranges or when selected materials have fewer eligible WAVs.

---
## 21 October 2026 — COMPLETED: 100% Pocket TTS audio, no device fallback

**Owner rule implemented and enforced:** all audible content in Λέξη uses
only approved Greek Pocket TTS recordings. Browser and device speech
synthesis APIs are removed, including SpeechSynthesis and el-GR TTS.
No microphone capture, speech recording, pronunciation recognition or grading.

**Complete Pocket audio coverage:** 1700 of 1700 independent A1/A2
vocabulary headwords; 549 of 549 original stress-letter exercises;
35 of 35 syllable-stress exercises. Existing 717 listening exercises
continue to use their original 1266 Pocket WAV files and six approved voices.
The separate pronunciation library contains 1529 additional Pocket WAVs
(exact hashes and Greek strings, 24kHz mono 16-bit PCM, non-silent),
with safe media routing /greek/pronunciation/<32-hex>.wav. Shared
exact-match resolver also reuses original listening files and never
substitutes a different word, engine or voice. No entries need device TTS.

**UI:** regular and slower WAV replay in the Greek phonetic exercises
and in A1/A2 ten-word preview / regular and wrong-answer cards. If
a future new word is missing its Pocket recording, playback buttons
are disabled with localized missing-recording message; no fallback.
Both modes and all missing-recording messages work in six UI locales.
Original practice remains available even if a new recording is missing.

**Verification:** qa_all_pocket_audio.py checked all 1529 new files
against exact text SHA256 keys, media filenames, voice allowlist,
RIFF format, nonzero signal, 24kHz mono PCM16 and duration bounds;
fully mapped every original 1700 A1/A2, 549 accent and 35 syllable word.
qa_word_audio.py, qa_word_audio_http.py, qa_word_audio_client.js verified
the removal of device speech, unavailable state and no WAV fallback;
original 1795 source card, 1700 lexical ID, 717 audio and SRS regression
suites remained passing. Public API /api/vocab/meta reports
offlineAudioWords=1700 and audioMode=pocket_offline_only.

**Deployment:** no production SQLite migration or reset; graceful
Caddy blue-green 18561 -> 18560; rollback Caddy snapshot
backups/caddy-greek-bluegreen-20261021T082017Z, code source backup
backups/pre-pocket-only-20261021.tgz. Both backend processes active.
After publication the site, all JS assets and multiple previously
missing vocabulary WAVs returned HTTPS 200, real RIFF audio confirmed.
150 concurrent requests: 100 expected HTTP200 GET and 50 anonymous
HTTP401 POST, zero 502/5xx. Chromium 320 and 1440 pixels loaded
the playback controls and login form.

**Status:** Greek device-voice fallback is permanently removed.
Pocket library coverage for currently shipped playback exercises
is complete. New future Greek text needs a Pocket WAV before it
can be made audible. No future audio generation is pending for
the current 1700 A1/A2 + 549 tonos + 35 syllable targets.

---
## 21 October 2026 — OWNER HARD RULE: AUDIO = POCKET TTS ONLY

**Mandatory:** every audible word, phrase and exercise in Λέξη is
an exact Greek recording generated by the approved local Pocket TTS.
Device speech synthesis (Web Speech API, speechSynthesis, el-GR platform
voice), browser TTS, remote API and Piper are **NEVER fallback options**.
If the exact Greek WAV has not been generated and validated, mark playback
unavailable and keep the button disabled; the rest of the lesson stays
available. This overrides all earlier roadmap entries offering device TTS.

**Also permanently excluded:** microphone recording, speech recognition,
pronunciation grading and microphone permissions.

**Backlog:** finish offline Pocket WAV coverage for the full 1700-word A1/A2
dictionary, without changing original word IDs, answers, SRS, student
progress, source provenance or the 717 listening tasks. Do not claim
100% audio until every file passes WAV validation and is actually served.

---

## 21 October 2026 — Playback audio additional finished batch (LATEST STATUS)

Latest released offline Greek audio coverage: **752 / 1700 A1/A2 vocabulary headwords**, **35 / 35 syllable-stress exercise words**, plus existing recordings for some of the 549 tonos-letter cards. New Pocket TTS pronunciation manifest contains **355** immutable PCM WAVs alongside the original six-voice library; the original **717 listening exercises / 1266 WAV** are unchanged.

Both A1/A2 ten-word preview and regular/review questions offer normal and slowed (0.8x) Greek playback. Phonetics accent-letter and syllable-stress questions also expose playback. For **948** not-yet-recorded A1/A2 words, the browser uses an installed **el-GR** voice when available; missing Greek device voices produce an explicit localized message. Do not substitute English speech or claim those 948 have offline Pocket audio.

**NOT TO IMPLEMENT**: microphone access, voice recording, speech recognition, pronunciation grading, speech comparisons and per-request paid synthesis. This is a permanent product exclusion unless the owner explicitly reverses it, not an open backlog item.

Validation: all 355 new WAVs checked against exact Greek text hashes, 24kHz mono 16-bit PCM and duration; manifest allowlist denies arbitrary file reads. Isolated HTTP and JS tests cover playback, six languages, normal/slow speed, device fallback, denied paths, and unchanged 1795-card IDs, 1700-word IDs, 717 listening activities and student stats.

Blue-green cutover **18561 -> 18560** succeeded; old backend kept for in-flight responses. Caddy rollback backup: backups/caddy-greek-bluegreen-20261021T072316Z; original source archive: backups/pre-pronunciation-playback-20261021.tgz. Live public vocabulary meta reports offlineAudioWords=752 and microphoneEnabled=false. Additional offline recording work, if approved, should be separate explicit batches without disturbing learner progress.

---

## 21 October 2026 — Released: Phonetics + A1/A2 pronunciation playback; microphone excluded

Owner decision: **NEVER IMPLEMENT** microphone input, voice recording, speech recognition, pronunciation grading, or microphone permissions. This is a hard exclusion from current and proposed Λέξη roadmap unless explicitly reversed by the owner.

Implemented playback-only Greek pronunciation buttons: regular + slower audio for all 549 original tonos-letter and 35 stressed-syllable exercises; per-word 🔊 buttons in every independent A1/A2 10-word preview and regular/review card. No audio interaction changes answers, SRS, learner accounts or stats.

Approved Pocket TTS exact-text recordings from original six-voice listening collection are reused. Separate validated offline pronunciation clips are served from manifest-allowlisted /greek/pronunciation/<hash>.wav; the original 1266 Pocket listening WAVs remain untouched. If no exact WAV exists or playback fails, the client uses device Web Speech synthesis only when an el-GR voice is available. Never substitute English and disclose unavailability clearly. Six UI languages and regular/slow speed.

Verified **35/35** phonetics syllable words and **656/1700** A1/A2 headwords have offline recordings at successful cutover. More independent offline clips may be added later; backend startup snapshots count via /api/vocab/meta.offlineAudioWords, and microphoneEnabled=false. Do not misrepresent the remaining vocabulary as 1700 offline Pocket recordings; those need a locally available Greek voice.

QA: qa_word_audio.py, qa_word_audio_http.py, qa_word_audio_client.js (Greek audio playback, slow speed, missing WAV and missing el-GR voice), phonetics and legacy exercises, learner/answer/replay, original 1795 source audit, 717 Pocket listening. Chromium UI loads at 320px and 1440px; 150 external post-release requests (100 GET 200; 50 expected unauthenticated POST 401), no HTTP502 or 5xx.

Release: source backup backups/pre-word-audio-20261021.tgz; Caddy graceful bluegreen latest cutover 18560 -> 18561; backup backups/caddy-greek-bluegreen-20261021T071720Z. Previous backend preserved for in-flight requests. No live SQLite migration, no student data rewrite, no VPN or Matrix changes.

---
## 21 October 2026 — User-approved audio direction / permanent exclusion

**NOT TO IMPLEMENT / PERMANENTLY OUT OF SCOPE**: microphone access, recording student voices, speech-to-text, pronunciation grading, voice comparison, microphone permissions or speech recognition. This is a deliberate product decision, **not a pending task**. Do not reintroduce it in future backlogs unless user reverses this explicit decision.

**IN SCOPE / NEXT**: Phonetics 2.0 should let learners hear Greek words, including in syllable-stress and letter-tonos exercises. Standalone A1/A2 ten-word lessons should include a play control in both preview and quiz/review so users can hear the current Greek headword. Prefer existing offline Greek Pocket TTS WAV library; generate and validate additional offline media in bounded batches as needed; provide an honest missing-audio state, never charge per listen or require a microphone. Keep the 1,795 verified original card IDs, 1,700 independent vocabulary IDs, 717 listening exercises, existing SQLite, and six UI languages stable.

---

## 21 October 2026 — Decision: microphone is NOT TO BE IMPLEMENTED; add passive Greek word audio

**Owner decision — hard exclusion:** recording student speech, microphone capture,
speech recognition, AI pronunciation grading and mic permissions are explicitly
**NOT TO IMPLEMENT** in Λέξη. Do not suggest them in remaining-feature lists
or implement as a future phase without a new explicit owner reversal.

**Approved instead — Phonetics 2.0:** a play/slow-play button that pronounces the
correct complete Greek word in existing tonos-letter and stressed-syllable
exercises. No mic; hearing a pronunciation never scores the answer.

**Approved — independent A1/A2 vocabulary:** play Greek pronunciation in
the 10-word preview and while practising a card, regardless of whether
question direction shows Greek or the user's translation. The available
high-quality offline Pocket TTS archive is reused for exact text matches,
with an honest el-GR device speech-synthesis fallback when a recording does
not yet exist. The player must distinguish cached Pocket audio from
device-generated speech, not silently switch to a different language,
and must signal unavailability rather than promise 1700 offline WAV files.
The 1700 word IDs, mistakes and repetition queue remain unchanged.

**Deferred content expansion:** Native-speaker review of pronunciation and
optional offline Pocket generation for remaining vocabulary can be scheduled
as a separate explicit task; it is not a prerequisite for using the
player and should not stall the UI release. No paid APIs, no Piper.

---

## 21 October 2026 — Advanced stress-by-syllable, grammar-stage gating and better distractors (released)

This is a functional batch; **no lexical, translation or publisher-PDF audit**.

**New independently authored syllable stress mode**: `advanced_syllables.py`
defines 35 syllabified Greek words from existing known accent card forms.
Unlike the original 549 letter-based tonos exercises, these are separate
2–6-syllable choices with the accent suppressed before answering, and
a six-locale explanation with accented segmentation afterwards, e.g.
`ευ · χα · ρι · στω` -> `ευ-χα-ρι-στώ` (fourth syllable). The mode is
an opt-in checkbox `syllable` in normal chapter/page practice and uses
stable `sy261021_NNN` IDs. Its own answer direction is `stress_syllable`
and it supports missed-answer debt, SRS and skill maps. Segmentation
is explicitly curated; the original card list, 717 Pocket audio entries
and 1700 vocabulary words are unchanged. New questions have approximate
chapter/page anchors, no asserted exact publisher exercise identity.

**Grammar stage boundary:** `grammar_scope_guard.py` cross-checks
existing `curriculum_ready_unit` and conservative, specific patterns
for later comparatives (11), aorist/past forms (12), future (14),
selected subjunctive expressions with να (16), and conditionals (18).
It deliberately does not prohibit every bare να, since some phrases
appear earlier in idiomatic contexts. Normal chapter/page practice
and the capacity estimate now withhold cards above the maximum
chosen studied unit and report `grammarDeferred`. SRS/weak_all
continue to find historic learned material without deleting progress.
Verified that selecting chapter 9 alone excludes early-placed
`dlg059` until chapter 16 is also selected, and chapters 17–20 remain
available. All 1795 original catalog metadata and historical IDs stay.

**Distractor quality:** standard 8-choice translation banks now
prefer morphologically relevant candidates no later than the
target teaching stage, including vetted supplementary sentences.
A conservative fallback still supplies 8 distinct answers when the
early lexicon is too small. No auto-created synonym acceptance
or unreviewed meaning changes were made.

Released UI on `app.js?v=35`, with six languages, accent explanations,
explicit `syllable` setup mode and correct skill label in analytics.
Public `/api/catalog` counts: original `cardCount=1795`, authored
`supplementalCount=26`, `supplementalSyllables=35`, overall
`practiceCardCount=1856`, offline audio `listeningCount=717`.

New QA `qa_next_learning_cycle.py`: 35 tasks × 6 languages => 210
question renders, 210 accepted correct answers, 210 correctly
rejected wrong answers on isolated SQLite; zero source page
verification claims; checks grammar gate, capacity and original
letter-based accent scoring. `qa_syllable_http.py` runs real
isolated localhost HTTP registration, syllabus quiz, syllable
answer with idempotent retry, stats, grammar map and filtering.
Original structure/provenance, earlier stage grammar, registration
and session-resume, alternative Greek spellings, vocabulary and
audio regressions passed. Node24 frontend syntax PASS.

Graceful Caddy blue-green cutover 18560 -> 18561 completed with old
worker running for existing requests; rollback backup
`backups/caddy-greek-bluegreen-20261021T062802Z`.
Source backup created before mutation:
`backups/pre-syllable-and-grammar-cycle-20261021.tgz`.
Post-cutover production: 100 GET HTTP200, 50 expected anonymous
same-Origin POST HTTP401; **zero 502/5xx**. Both services active.
Chromium smoke at 320px and 1440px confirms setup syllable
selection, login, grammar analytics and existing retry/resume UI.

Limitations: these 35 syllabifications are curated practice samples,
not a full Greek syllabification engine or a native-speaker certification.
Conditional comparative/irregular-verb detection is intentionally
conservative; fine-grained syllabus/content expansion can be done in
a separate future cycle without restarting mass lexical auditing.

---
## 21 October 2026 — Session resilience + authored sentences + valid Greek word order (released)

**Session resilience:** browser persists active questions, original random option
order, student nickname scope, remaining deadline, answer counts, dialogue
gap state, verb stage, seen semantic IDs and immutable in-flight answer.
Reloading before deadline resumes progress and transparently retries a
pending submission using its original UUID and identical body. A visible
retry control appears if the network/502 response remains unavailable.
Session snapshot is removed on completion or explicit logout; expired
sessions are not resumed. New clients send UUID requestId on /api/answer.
Backwards compatibility: old clients without a UUID still receive
the original non-idempotent scoring semantics.

**Atomic server receipts:** /api/answer adds `answer_receipts` keyed by
(user_id,request_id), with SHA256 of immutable answer contents and
JSON replay of the original response, including SRS metadata.
`BEGIN IMMEDIATE` protects concurrent submits across blue/green
workers and commits receipts, answer progress, attempt and SRS in
one transaction. Reuse of an ID with a different answer returns 400.
Only one new table, no stored attempt/progress reindex/migration.

**Supplementary Greek content:** independent `extra_sentences_20261021.py`
contains 18 more complete/compound sentences on chapters 2–18, and
eight tap-to-arrange cards based on them. All six languages supplied.
Items live in separate `EXTRA_ALL` + `EXTRA_BY_ID` so that the
source-audited 1795-card original catalog and provenance ledgers
remain exactly stable, with 717 Pocket listening exercises unchanged.
Normal scope and due/weak review include these new exercises as
appropriate. Public /api/catalog retains cardCount=1795, adds
supplementalCount=26 and practiceCardCount=1821. The source pages for
new authored sentences are approximate syllabus anchors only.

**Valid Greek sentence reordering:** explicit finite, manually
curated alternatives for 14 of the original 17 order tasks.
The acceptance algorithm checks complete Greek word-sequence
after ignoring only punctuation/case. Tonos, lexemes and word forms
must match, and it does not accept arbitrary anagrams. Original
sentence remains canonical; saved progress IDs unchanged.
The other three keep canonical-only answer unless later curated.

**Related repaired defect:** /api/quiz chapter selector once intersected
with curriculum INDEX containing only 1–16. Changed it to use all
20 published chapter IDs, so chapters 17–20 now work and additional
chapter 18 content is accessible.

QA: `qa_resilient_learning.py` exercised isolated 25-concurrent same-ID
scoring with one persisted attempt, correct SRS, account isolation,
conflict rejection, 14 curated variants, 18+8 new six-locale cards,
and original cardinality. `qa_answer_http.py` used two independent
HTTP servers sharing disposable SQLite with 24 simultaneous retries,
simulating a response lost through a 502; exactly one attempt/receipt
and one SRS update resulted. Original full 1795 source ledger QA,
all Stage3, accepted spelling variants, all 1700 vocabulary,
Patakis unit boundaries and 717 Pocket audio regressions pass.
Node24 JS syntax PASS; Chromium 320px + 1440px can load the
updated retry/resume controls and earlier mastery panels.

Release safety: pre-code backup:
`backups/pre-session-reliability-20261021.tgz`;
consistent online student database copy:
`backups/pre-answer-receipts-20261021.sqlite3` (PRAGMA quick_check PASS,
file restricted to mode 0600). First blue-green attempt correctly
aborted because new Python source module files had too restrictive
permissions under DynamicUser. Fixed source modes 0644 and
completed graceful Caddy cutover 18561 -> 18560, leaving 18561
online for in-flight replies; Caddy rollback snapshot:
`backups/caddy-greek-bluegreen-20261021T044753Z`.
After cutover: 100 external GET requests HTTP200 and 50 anonymous
POST requests expected HTTP401; **zero 502/5xx**. Public
/api/catalog, /greek/ HTTP200, both backends active; production
`answer_receipts` table present, PRAGMA quick_check passes.

Limitations: session recovery applies while the original countdown
is valid and in the same browser/account, not arbitrarily long
after expiry or across devices. Curated alternatives are examples
and do not claim exhaustive Modern Greek word-order acceptability.
New sentence translations are AI/editor-authored teaching material,
not a publisher/native-certified corpus. No textbook PDF or
existing student attempt records were rewritten.

---
## 21 October 2026 — Learning effectiveness upgrade (released): topics, duration and error feedback

Scope: three requested functional improvements; **no additional vocabulary/PDF audits**.

**1. Knowledge map:** Stats now include a separate card-topic map,
direct grammar-pattern evidence map, and an independent A1/A2
ten-word-lesson topic map. Data are account-scoped and sourced from
existing `attempts` and `vocab_progress` only. The same topic may
receive attempts from multiple words; textbook exercises and the
standalone A1/A2 vocabulary course are never double-counted.
Each item reports answer count, correct count, accuracy, distinct
semantic targets, and an explicit **provisional** flag unless at
least **8** answers from **3** different targets exist. Direct grammar
drills (articles, conjugations, accents, plural, word-order) are
separate from mere contextual reading; neither signals formal CEFR
competence. Greek grammar/topic labels and descriptions available
in six interface locales. Existing chapter/skill/page analytics kept.

**2. Realistic session sizing:** `/api/capacity` retains its older
fields for compatibility and now returns `taskAware`,
`requiredUniqueAtEstimatedPace`, `enoughAtEstimatedPace`,
`estimatedMinutes`, `expectedRangeMinutes`, and scoped observed
`paceModel`. Reader-only last-160-attempt timing discounts long breaks
and derives median response time per sufficiently sampled task type.
Fallback per-kind timings are used without adequate observations.
Verb drills are two answer steps; dialogues consume 1–3 gap steps;
simple words, audio, and word-order construction have distinct
timing costs. Unique semantic targets prevent inflation by duplicate
word variants. The UI displays an approximate range and never
promises a guaranteed 10/20/30-minute exercise. None of this
alters quiz selection, stored progress, or actual session timer.

**3. Specific wrong-answer feedback:** Deterministic contrast
messages on RU/EN/ZH/AR/ES/PT now identify the chosen and correct
article, the target noun context, incorrect person form and subject
for conjugation, accent letter position, noun-number target,
contextual dialogue reply, and first mismatched word in the
order-sentence exercise. Unverifiable translation nuances fall back
to a modest meaning comparison; no generative diagnosis or API calls.
Feedback is shown after answering, preserving hints/answer secrecy.

Implementation `learning_upgrade.py`, adjustments to `server.py`,
`app.js?v=33`, `index.html`. No schema/data migration.
Tests: `qa_learning_upgrade.py` (isolated SQLite, six locales,
cross-user isolation), `qa_learning_http.py` (isolated real HTTP
account, vocab progress, stats, capacity, wrong answer),
`qa_learning_ui_contract.py` (UI panels, locale strings).
Baseline QA: stage gates, weak review, dialogues, previous
grammar forms, listening, pedagogy, and original 1795 card
structural invariants pass. Node 24 Alpine static syntax PASS;
Chromium 320px and 1440px page loads confirm new panels.

Graceful release: Caddy blue-green 18560 -> 18561, previous service
remains alive during handoff; backup
`backups/caddy-greek-bluegreen-20261021T040905Z` and pre-release
source snapshot `backups/pre-learning-upgrade-20261021.tgz`.
Post-release concurrency: 100 GET HTTP200 and 50 expected anonymous
POST HTTP401 (proper Origin), **zero 502/5xx**. Both backends
active. User accounts, cards, training histories, SRS, audio,
VPN and Matrix not modified by the upgrade.

Possible next-phase enhancements remain unrelated to this release:
full lesson-resume reliability, richer lesson content, broader
valid word order recognition, and human editorial work when desired.

---
## 21 October 2026 — Final original catalog provenance audit COMPLETE (#8; indices 1751–1795)

All final **45 original catalog cards** reviewed and individually recorded:
**24** independently authored Greek article/case cloze drills, **17**
word-order rearrangement drills derived from Lexi-authored parent sentences,
and **4** independently authored syllabus-related Greek phrases/sentences.
None is a reproduced/verified publisher exercise. Their chapter/page
labels remain approximate teaching context; **0 new page changes**.
Batch audit saved as `editorial-audit/source-page-batch-008-1751-1795.json`
with deterministic generator `source_page_batch008.py` and
`qa_source_page_batch008.py`. QA: **294** six-locale question renders,
**294** valid answer grades, **30** accepted optional final-n article forms,
**246** correctly rejected wrong answers (all on isolated temporary SQLite).

**Real editorial repair discovered in batch #8:** Two parent-vs-word-order
prompt inconsistencies for Greek female friend `η φίλη μου` in Arabic
and Spanish, plus one for masculine `ο φίλος μου` in Spanish.
`order_translation_sync.py` now copies reviewed parent translations to
its derived word-order exercise *after* locale editorial adjustments:
2 Spanish corrections at catalog stage, 1 Arabic correction after the
server's separate Arabic editorial step. Thus all **17/17** word-order
drills exactly match their Greek parent sentence and six locale prompts.
Unchanged: Greek question text, order token solutions, 1795 card IDs,
learner progress history, student SQLite, and 717 Pocket-TTS audio tasks.

**All-eight-batch reconciliation COMPLETE:**
`editorial-audit/full-source-audit-1795-final.json` with per-card
index/ID/chapter/page/source/evidence records **1795/1795**, no missing,
overlapping, inconsistent page or identity entries, and file SHA256
for each batch ledger. Generated by `full_source_audit.py`, reproduced
and QA-verified by `qa_full_source_audit.py`.
Precisely **321** original Greek source forms/alphabet usages have
attested printed page evidence (142/92/73/0/0/0/14/0 by batch),
**1474** other items are approximate source matches, independent
exercises, or otherwise not attested to a specific printed page.
This **does not** mean the latter 1474 are incorrect: generated accent
exercises, dialogue completions, conjugations and order exercises do not
have matching original-publisher exercise identities by design.
Even the 321 page attestations prove Greek usage on a source page
**not** first occurrence or an actual printed publisher exercise.
Original publisher exercise identities certified: **0**.

Regression passed all 8 source-page audits, full-source reconciliation,
Patakis section boundaries, 1795-card structure, complete 1700-word A1/A2
six-locale translation atlas, curated Greek spelling alternatives,
verb stage gates, listening and prior page anchors.

**Production release:** Caddy graceful blue-green cutover from 18561
to warm 18560, old worker left running for in-flight student requests.
150 external concurrent requests after deployment: **100 GET HTTP200**,
**50 anonymous same-Origin POST HTTP401** (expected auth rejection),
**zero HTTP502/5xx**. Both backends active. Caddy rollback copy:
`backups/caddy-greek-bluegreen-20261020T230858Z`.
Pre-batch and staged code backups:
`backups/pre-source-page-batch008-20261021.tgz` and
`backups/batch008-release-20261021/staged-source-files.tgz`.
No VPN/Matrix restarts or database schema changes.

**Editorial next steps (not part of completed provenance ledger):**
source-page visual/lexical checks for uncertain main-book items as needed,
pedagogical/native review of independently authored Greek and all locales,
and a clear UI distinction between verified occurrence page and
approximate chapter alignment. Provenance coverage complete does not
certify every translation, exercise or original source page.

---
## 21 October 2026 — Original textbook source-page provenance batch #7 (1501–1750)

Completed editorial/source-provenance audit of **250** original catalog cards:
**80** independently authored conjugation/person drills, **100** independently
authored dialogue/gap cards (15 one-gap, 77 two-gap, 8 three-gap),
**54** independent syllabus-theme sentences/phrases, and **16**
extra unit-9 Greek words. All 250 records in
`editorial-audit/source-page-batch-007-1501-1750.json`;
generator/metadata corrections `source_page_batch007.py`,
QA `qa_source_page_batch007.py`.

Original textbook licensed PDF is only in the owner's private Library,
SHA256 49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282.
All 70 `patk` card forms were compared against its imperfect text layer
(printed pp14–289), with selective source-image review on printed
pp108, 109, 114, 115, 116, 186 and 216. No full sentences/phrases
matched literally in the text layer; this is NOT proof of absence,
and no independently authored question is called a publisher exercise.

**14 visually verified Greek headwords** in unit 9: eight clothing
items on printed pp115/116, six adjective forms on printed p108.
Only their source-page metadata is corrected and `book_page_verified`
set for attested Greek word use; publisher exercise identity is NOT
verified. Two remaining word cards (`patk09_009`, `patk09_010`)
retain approximate page 113 without false attestation.
Stable card IDs and original Greek text/translated answers remain identical;
student progress keys and live SQLite untouched.

QA: 250/250 ledger identity/provenance checks, **2958** six-locale
question-render checks, **493** correct answer grades in disposable
SQLite, full source batches #1–#6, variants, Patakis alignment,
all 1795 cards' structural QA, verb-stage tests, and complete 1700-word
six-locale vocabulary regression PASS. Pocket-TTS 717 audio questions
and recordings unchanged.

**Production publication** through two-backend Caddy graceful blue-green:
old active 18560 -> warmed 18561; old still online for in-flight replies.
External post-cutover 150-request concurrent smoke proof:
100 GET HTTP200, 50 authorization-rejected POST HTTP401 (correct Origin),
zero 502/5xx. A missing-Origin POST correctly yields HTTP403 under
existing CSRF protection and is not an application failure.
No VPN or Matrix changes, no student SQLite/schema migrations.
Pre-release app files backed up in
`backups/pre-source-page-batch007-20261021.tgz`,
Caddy configuration in
`backups/caddy-greek-bluegreen-20261020T225512Z`.

**Cumulative:** **1750 / 1795 original cards** have explicit source and
authorship provenance audit. **45 remain**, final batch #8 indices
1751–1795. Additional 14 attested headword usage pages were confirmed
in #7 (first three batches had 307 earlier such source records).

---
## 20 October 2026 — Source-PDF provenance batch #6 (1251–1500)

All **250 catalog cards** checked: **153** app-derived accent drills,
**75** supplemental topical vocabulary cards, and **22** original
app conjugation/translation drills covering four verb paradigms.

Accent parent lineage: **130** derive from app-created review clones
(publisher exercise identity not claimed); **23** derive from regular
book word cards, of which **14** have already source-attested parent
headword occurrence pages (**10** exact PDF text, **4** visual),
**9** have unconfirmed approximations. All 153 generated accent task
pages correctly remain unverified as publisher exercises.

Topical vocabulary: independently authored topic cards have chapter -8,
page 0. A fresh search of the user's privately owned 314-page
Ελληνικά Α΄ PDF text layer (printed pp14–289) found **18** exact
article+headword strings, another **23** headword-only literal strings,
and **34** without literal text-layer hits. OCR/text-layer omissions
are *not* evidence a lexeme is absent from the source. Printed pages
104, 208 and 258 were visually inspected as spotchecks of contextual
usage. Lexical occurrence never certifies publisher exercise identity;
no topical card was misleadingly assigned a printed book exercise page.

All **22** conjugation drills (γράφω, μένω, διαβάζω, δουλεύω)
remain app-authored chapter -9, page 0. Source book contains all four
verb lemmas; exact app exercise identity is not claimed. Four source
lexeme sample page lists and hit counts are included for provenance.

Source PDF SHA256: 49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282.
Owned PDF is private, no source PDF bytes/pages/images or extracts copied
to Core. Full per-card provenance at
editorial-audit/source-page-batch-006-1251-1500.json, reproducible
report generator source_page_batch006.py, standalone regression
qa_source_page_batch006.py.

Verified **2082** six-language question renders and **347** graded
answers against a disposable SQLite; earlier source audits #1–#5,
Greek accepted spellings, stage-gated verbs, general card integrity,
Patakis unit alignment, and complete 1700-word vocabulary audit all PASS.
Both backend services active; public site and API catalog HTTP 200.
**Report-only change**: no application code deployment, no restart,
no progress DB writes, no student ID/history remapping, no audio,
VPN or Matrix changes.

**Cumulative:** **1500 / 1795** original catalog cards have individual
provenance ledgers. Remaining **295**: #7 indices 1501–1750,
and final #8 indices 1751–1795.

---
## 20 October 2026 — Source-PDF provenance batch #5 (1001–1250)

Catalog positions **1001–1250** audited (250/250). All 250 are
independently generated **accent / tonos letter-choice drills**,
not original exercises from the bought Ελληνικά Α΄ textbook.
Parent word usage already attested in prior source audits for **137**
headwords (**103** exact PDF text occurrences, **34** visually confirmed),
while **113** parent words retain approximate/unverified page links.
The 137 parent headword attestations are inherited evidence, NOT new
publisher exercise attestations. **133** exercises appropriately omit
articles (e.g., το) from the accented target but retain same parent ID.

All 250 publisher-exercise-verified flags remain false. No false page
claims, page remapping, Greek content changes, card ID churn, or history
migration. Full ID-by-ID provenance in
editorial-audit/source-page-batch-005-1001-1250.json;
generator: source_page_batch005.py; regression: qa_source_page_batch005.py.

Evidence policy: licensed PDF stays in the owner's private Library;
verified SHA256 matches earlier source audit. No PDF pages/images or
publisher exercise text copied to Core, and no fresh line-by-line check
of publisher accent-exercise identity is claimed.

Verified all **1500** six-locale renders, **250** correct grade operations
against an isolated SQLite, Greek vowel targets, parent IDs/chapters/pages,
semantic lineage, and previous source-ledger evidence. Regressions
#1–#5, valid Greek spelling alternatives, 1795-card structure,
and Patakis alignment pass. **No restart or deployment needed** for
report-only audit; both backends active and HTTPS site/catalog return 200.
No changes to VPN, Matrix, TTS, audio or user SQLite.

**Cumulative**: **1250/1795** original catalog cards audited. Remaining
**545**: batch #6 indices 1251–1500, #7 1501–1750, and final #8
1751–1795. First three audits' **307** source-attested parent headwords
remain unchanged; derivative review/accent items don't add attestations.

---
## 20 October 2026 — Source-PDF provenance batch #4 (751–1000) and Greek variants

All 250 original-book exercise cards #751–1000 inspected for exact source
identity and parent-page lineage. This range contains **104 independently
authored review clones** plus **146 auto-generated tonos exercises**:
105 accent parents have already attested word-form occurrence pages from
earlier private-PDF batches, and 41 do not. No matching publisher accent
exercise or review exercise is certified, so all 250 exercise page labels
correctly remain unverified. **No source page metadata changed**. Full
per-card provenance ledger is
`editorial-audit/source-page-batch-004-751-1000.json`.
Owner's licensed PDF remains private, no publisher PDF/page/excerpt on Core.

Greek word-form variants are now curated as equal-answer spelling
alternatives with the owner's book form preserved as the main spelling:
επτά/εφτά, οκτώ/οχτώ, αδελφός/αδερφός, αδελφή/αδερφή,
and relevant inflections/phrases. Ministry of Education Greek-language
grammar also validates δύο/δυο, μία/μια, εννέα/εννιά, ένδεκα/έντεκα,
δεκαέξι/δεκάξι, δεκαεπτά/δεκαεφτά, δεκαοκτώ/δεκαοχτώ,
δεκαεννέα/δεκαεννιά. These pairs are exact curated lexemes, not
substring replacement in unrelated words. Normal book RU/EN/ZH/AR/ES/PT
reverse-translation and separate A1/A2 vocabulary grade both accepted
forms correctly, include both of those Greek forms as answer choices,
and never put a valid sibling spelling among wrong distractors.
The learner sees alternate Greek forms in the preparatory vocabulary
list and after answering; reverse translation and accent questions
do not leak the Greek answer before the student attempts it.
Canonical source Greek, stressed-letter evaluation, publisher/printed
card IDs, SRS, user answer history, TTS/717 listening items and
1,700 independent vocab words remain unchanged.

Cumulative printed-book provenance first four batches: **1000 of 1795**
reviewed; **307 Greek word-form source-page attestations**, **443 unproven
source-page matches in first three batches**, plus 250 derivative review
and accent exercises with unverified publisher exercise identity;
**204 earlier page corrections**. Do not interpret parent-word occurrence
as verification of an independently generated accent or review exercise.

QA: `qa_greek_variants.py`, `qa_source_page_batch004.py`, original
full-card/six-locale/vocabulary/audio/page-provenance suites. Production
publishes via two-backend graceful Caddy switch without active-worker stop.

---

## 20 October 2026 — Source-PDF page evidence batch #3 (501–750)

Independent full textbook catalog cards #501–750 (250) examined against
the user's privately owned Ελληνικά Α΄ PDF. **73 attested Greek source
form usage pages**: 32 visually verified including all 24 Greek alphabet
letters on printed p9, plus 41 literal text-layer form matches within
their printed teaching unit. **177 remain approximate**: 76 no reliable
OCR text match, 34 independently authored plural drills, 11 independently
authored sentences, 56 independent review-card clones. No such
independently authored exercise is certified as a publisher exercise
from vocabulary overlap. **61 page anchors corrected**. Exact audit:
`editorial-audit/source-page-batch-003-501-750.json`. Original PDF,
page screenshots and published-book question text are NOT on Core.

Combined #1–#3: **750/1795 cards reviewed**, **307 form/page
attestations**, **443 uncertain**, **204 page-label corrections**.
This is evidence of *word-form use* on a printed page, NOT first
introduction and NOT semantic proofreading in any language.
The user's and fellow learners' user progress, all stable card IDs,
scoring answers, 717 Pocket listening items and 1266 WAVs unchanged.
Production release through two-backend warmed blue-green Caddy
switch, no planned 502 outage.

---

## 20 October 2026 — Source-PDF page evidence batch #2 (251–500)

250 more independent original-catalog Greek exercise records (positions
251–500) checked against the owner's privately licensed Ελληνικά Α΄ PDF.
18 additional cards visually confirmed from selected actual printed pages
(68,87,104,132,170); 74 card Greek word/phrase forms had literal
Greek surface-form matches in the PDF text layer and matching unit.
**92 usage-page attestations, 158 still unconfirmed**, including 26
independently authored sentences and 29 plural exercise templates.
**74 page labels adjusted**, never asserting they are first textbook
occurrence or publisher-authored equivalent exercises. PDF itself is not
on Core. Full item/old/new/verification-state audit saved in
editorial-audit/source-page-batch-002-251-500.json.

Combined batches #1 + #2: 500/1795 cards inspected; 234 source-form page
attestations, 266 unverified page labels, 143 revised page anchors.
Stable IDs, Greek source/answers, student progress SQLite and 717 Pocket
listening cards/1266 WAV remain unchanged; TTS teacher-approved.

### Operations — graceful, two-backend release

The Greek Trainer no longer requires cutting off Caddy's only upstream.
Both DynamicUser systemd units are enabled and share systemd's protected
SQLite StateDirectory (WAL, busy_timeout): greek-trainer.service on 18560
and greek-trainer-secondary.service on 18561. Caddy serves only one.
After editing backward-compatible on-disk content, run test suite first,
then `/usr/local/sbin/greek-bluegreen-deploy`. The deploy tool restarts
ONLY the route-inactive backend, waits for local index and catalog
readiness, validates and gracefully reloads Caddy, and leaves old
backend alive for ongoing requests. Caddy changes are backed up;
config/templates restored on cutover failure. Do not run
`systemctl restart greek-trainer` or restart the current active
backend during student sessions. Old processes need not restart
immediately after switching; on the next release they are the idle
candidate to warm. Both services start on boot.

---

## 20 October 2026 — Owner PDF source page batch #1 (1–250)

The teacher approved Pocket six-voice listening; no outstanding teacher
approval is required. PDF original remains exclusively in the owner's
private ChatGPT Library, not on public Core.

Original course items #1–250 reviewed against privately inspected textbook
PDF pages. **142 cards have source-use page evidence** (58 previously visual,
46 newly visually checked, 38 exact PDF text-layer Greek matches). **108 lack
sufficient evidence** (101 OCR unmatched plus 7 independently authored
sentences); those keep clearly approximate pages. **69 approximate page
labels replaced with attested usage page labels**; never assert first
introduction, publisher question identity or completeness. The source
evidence ledger is editorial-audit/source-page-batch-001-1-250.json.
Original card Greek, answer keys, ID, chapter, SQLite progress, listening
audio and copyrighted source PDF unchanged. Remaining: 1545 source cards.

---

## 2026-10-20 — Fourth 250-headword review batch (751–1000)

Follows Translator, Educational Content Reviewer and Course
Localization Specialist rubrics. Original **250 Greek words × six
target-language glosses = 1,500 localization cells** inspected in the
independent A1/A2 course. Saved the original content and the completed
six-locale per-word, per-answer audit ledger in
`editorial-audit/vocab-batch-004-751-1000.json`.

AI first-pass resulted in **124 exact-value-guarded corrections on
75 unique words** (European Portuguese 47, Spanish 30,
Modern Standard Arabic 29, Simplified Chinese 18).
**25 contextual items** remain marked ambiguous rather than forcibly
rewritten. Examples: `το τελωνείο` customhouse, not "habits"
(ES/PT); `η πρωτεύουσα` city capital, not financial capital
(ZH/AR/PT); `η βρύση` water tap vs button; `το νύχι` human nail,
not metal nail in PT/ZH/AR; `η πεδιάδα` geographic plain, not
plain/ordinary adjective; `το κλαδί` tree branch not bank branch.
Greek originals, Russian and English reference anchors, IDs, levels,
user SQLite rows, 717 listening cards and audio files all preserved.

Deterministic diff gate verified exactly 124 changed atlas cells and
**no localized content changes outside frozen word IDs 751–1000**.
Cumulative first pass: **1,000 / 1,700 Greek source words, 6,000
six-language fields read, 415 corrected translated fields across
283 words**. Remaining 700 source words; next batch **1001–1250**.
This is an AI editorial first pass **not native-speaker sign-off**.

---
## 2026-10-20 — Third 250-word, six-locale A1/A2 review batch

Third fixed-ID source review covers independent-vocabulary items
**501–750 (250 Greek headwords × 6 language glosses = 1500
inspected translation fields)**. Guided by Translator, Educational
Content Reviewer, and Course Localization Specialist rubrics. AI
first-pass inspected all displayed Greek/RU/EN/ES/PT-PT/ZH/MSA Arabic
records. Source meaning prioritized over English ambiguity.

Corrected **111 distinct target-locale cells across 70 Greek words**:
ES 35, ZH 33, PT-PT 23, AR 20. Logged **24 contextual/ambiguous
cases** without making unwarranted categorical replacements. The
source-anchored complete ledger
`editorial-audit/vocab-batch-003-501-750.json` contains all 250
original Greek headwords, six localized final glosses, 111 exact
old/new changes with rationale, and per-word review status.
Not a certified native translation pass.

Examples: `η μπλούζα` means clothing, not 'top' as spatial above;
`η βρύση` means water tap, not 'touch/click';
`το φως` means light illumination, not lightweight;
`ο μαθητής` is a school pupil, not a pupil of the eye in ZH/AR;
`βάζω` is **present** 'I put', not past 'puse/coloquei';
`πετυχαίνω` present succeeds, not Portuguese past consegui;
`η άνοιξη` is spring season, not mechanical spring;
`ο πίνακας` here classroom board, not company board of directors.
Exact diff gate verified **111 edits exclusively within the 250
pre-frozen word IDs**; the other 1450 words are untouched this batch.

Cumulative **750 of 1700 headwords** passed AI first-pass
(4500 target fields checked), **291 translated fields corrected
across 208 different headwords**; 950 words remain.
Next fixed-ID batch: **751–1000**. Greek originals, RU/EN anchors,
permanent IDs, topics/levels, user SQLite and Pocket audio untouched.

---
## 2026-10-20 — Second 250-headword editorial batch completed

The second frozen batch (`editorial-audit/vocab-batch-002-251-500.json`)
reviews Greek headwords **251–500 × 6 target languages = 1,500
source-target language cells** in the independent A1/A2 course, using
Translator, Educational Content Reviewer and Course Localization
Specialist rubrics. It documents each of the 250 words, all final
localized glosses, **78 exact confirmed before/after revisions across
63 different source headwords**, and **17 context-dependent flags**.
Distribution ES 18, PT-PT 35, Arabic 16, ZH 9; Russian and English were
examined as original meaning anchors and unchanged.

Examples of corrected mistakes:
- `ο όροφος` is 'building storey'; Arabic `الكلمة` ('word')
  was changed to `الطابق`.
- `το τρένο`, `το ψυγείο`, `το μπάνιο` use proper PT-PT
  `comboio`, `frigorífico`, `casa de banho`.
- `όταν` Greek subordinate 'when', rather than Arabic question
  `متى`: corrected to `عندما`.
- `θα έρθω` is `eu virei`, not `eu irei`.
- `η κατσαρόλα` is a saucepan/pot, not a frying pan in Chinese.
- `η πλατεία` [previous batch] and `ο νεροχύτης` [this batch]
  distinguish urban square from geometric square and sink from drain.

Immutable source IDs and the Greek/RU/EN headwords, CEFR levels, topics,
account progress, WAV library are unchanged. Diff QA proved all 78
new locale changes lie within word IDs in batch #002. Separate A1/A2
course still exactly 1,700 unique Greek words and 8-choice lessons on
all 6 locales pass. This is an **AI first pass**, not certified native
linguist proofreading.

Cumulative editorial progress: **500/1700 Greek source words**
and **3000 6-locale cells examined; 180 localized fields edited
across 138 words**. Remaining 1200 words; next fixed batch
**501–750**. The frozen source ID plan is updated from the candidate
in `editorial-audit/vocab-review-plan-v1.json`.

---
## 2026-10-20 — Review in 250-word editorial batches

Per user's request, a "run" is **250 Greek source words × 6
locales (RU/EN/ZH/AR/ES/PT)**, rather than a count of changed fields.
Do not count structural tests as semantic proofreads. Track the frozen
stable-ID order in `editorial-audit/vocab-review-plan-v1.json`;
seven nonoverlapping batches cover 1,700 unique word IDs:
1–250, 251–500, 501–750, 751–1000, 1001–1250,
1251–1500 and 1501–1700.

Batch 1: AI-first-pass linguistic inspection of **250** source headwords
and **1,500** target-language fields, using Translator, Educational
Content Reviewer and Course Localization Specialist rubrics. Manual,
exact-value-confirmed changes: **102 translation fields across 75 words**
(ES 44, PT-PT 37, MSA Arabic 21). Seven additional lexical cases
were marked for contextual human review. Examples include Greek
`δεξιά` direction corrected from ES `correcto`, PT `certo` and
Arabic `صحيح`; Greek `η πλατεία` city square corrected from
Arabic geometric `المربع`; orange fruit vs colour, gendered Arabic
verb forms, 2sg/2pl inflection, Spanish accents and PT-PT lexical
variants. Chinese target fields and original RU/EN source fields were
checked at first pass and did not receive edits in this batch.

Deterministic complete ledger: `editorial-audit/vocab-batch-001-250.json`
contains all 250 headwords, six final localized glosses, explicit 102
before/after edits, per-word review status and notes. The new JSON atlas
has exactly **102** cell-level changes, and none outside the 250
ordered word IDs; no Greek lemma, permanent vocab ID, CEFR level,
topic, original user history or audio changed. **Not** native-speaker
certification. The full remaining 1,450 words are pending this review
style; technical coverage of all 1,700 ≠ linguistic proofread.

---
## 2026-10-20 — Editor round 2 + linked independent vocabulary fixes

Reviewed with the open Translator, Educational Content Reviewer and Course
Localization Specialist rubrics (full protocol in
`editorial-audit/translation-skill-protocol-20261020.md`). Exact Greek
source and grammatical person/gender are authoritative, with European
Portuguese (PT-PT), Spanish, Simplified Chinese and Arabic targets.

The second batch provides 37 explicit, prior-value-guarded, reasoned
translation changes: **PT 16, ES 10, ZH 9, AR 2**. Corrections include
Greek εσύ vs εσείς register in PT-PT, Spanish usted vs tú,
Chinese 您 vs 你, Arabic gender agreement in "he/she lives",
and concrete male/female friend mismatches. The first 25 correct
locale edits remain untouched; cumulative book course: **62 fields**.

The separate 1,700-item A1/A2 mode had stale copies of the same
headwords. For 17 exact Greek-word matches from the previously
reviewed first-round atlas, their original (wrong) target glosses
were validated and replaced by the same verified target gloss in
`vocab_translations_1700.json`; no independent words or IDs were
created or removed. The 1,700 entries remain 700 A1 + 1,000 A2.

Source translations and Greek text remain unchanged. Existing accepted
valid synonyms remain accepted, but prior incorrect register/gender
and stress spelling are not accepted. Per-answer direction,
eight-option integrity, stats and user SQLite are retained.

Proof: `editorial-audit/translation-skill-review-round2-20261020.json`,
`editorial-audit/independent-vocab-linked-corrections-20261020.json`,
`qa_editorial_localization_round2.py`, `qa_vocab_exact_sync.py`.
Fully certified translation/native review of all 1,795 textbook cards
and all 1,700 themed words is **not complete**. Purchased book PDF stays
private, no paid API used.

---
## 2026-10-20 — Skill-guided editorial localization QA

Translator, Educational Content Reviewer and Course Localization
Specialist instructions were read and applied as review checklists,
documented in editorial-audit/translation-skill-protocol-20261020.md.

First-four-unit original card text reviewed: exact, independently
audited correction of 25 locale fields (ES 12, PT-PT 8, AR 4,
ZH 1). Greek, Russian and English card source remains unchanged.
Corrected Spanish question accents and formal usted vs informal tu;
PT-PT informal tu vs formal register and European conjugation;
Chinese honorific 您 and Arabic masculine/feminine spouse glosses.
Four prior translations that are still semantically valid remain
accepted as aliases, but past erroneous register/orthography isn't
declared correct.

Per-field editor ledger:
editorial-audit/translation-skill-review-20261020.json
No original purchased PDF hosted or copied to Core. No paid API.
The pass is AI-assisted and is not certified native-speaker review.
Full 1795 original cards and 1700 A1/A2 themed words are NOT
meaning-by-meaning reviewed yet.

---
## 2026-10-20 — Keep Greek object pronouns and gendered nouns distinct

The generic headword normalization used by normal practice to avoid
repeating definite-article variants accidentally merged distinct
Greek constructions: `τον λένε` and `τη λένε` both reduced to `λένε`.
It also merged masculine `ο σύζυγος` and feminine `η σύζυγος`
despite their gender-sensitive teaching meanings. The targeted
`pedagogy_rules.canonical_greek` exception preserves these four
independently taught headwords while keeping common article+ordinary-noun
deduplication unchanged (e.g. `ο υπάλληλος` / `υπάλληλος`).

Only derived in-session `semanticId` grouping changes, not stored
SQLite card_key/answer history, source Greek text or audio WAV. The
first-four-unit listening capacity changes from 245 to 247 distinct
semantic targets, reflecting two previously suppressed distinctions.
Existing Pocket 717 cards, 633 texts, 1266 WAV all unchanged.
`qa_semantic_pronouns.py` verifies both forms appear within one
page 40 unit; six-locale, existing error replay and source-page
regressions remain green.

---
## 2026-10-20 — Source-verified printed pages (58 starter headwords)

The owner's purchased PDF was inspected privately; no PDF, publisher page
image or original publisher exercise is hosted. The editor checked seven
actual printed pages: **15, 19, 25, 34, 40, 49, 50**, and verified
specific *worked examples, paradigm entries or thematic word forms*
for **58 existing word cards**. The page metadata is stored in
`verified_lesson_pages.py` and applied after the original approximate
chapter mapping without changing permanent IDs or student answers.
**40 accent exercises** inherit their verified parent headword page
but are *not* falsely marked as literal source exercises.

Previous work mistakenly assigned `w023,w024,w033,w034` to printed
**p39**. The book uses p38 as a chapter topic outline; the actual
worked explanations of these forms are on **p40**, confirmed by
looking at the published page image. All five `w023,w024,w025,w033,w034`
are now explicitly anchored to p40. Only these verified IDs receive
a `sourcePageVerified=true` flag in the API. Quiz UI renders
`p. 40 ✓` and a localized tooltip rather than `p. 40 ~` used
for remaining approximate tags. This is **evidence of occurrence/teaching
on a page, not a claim of first occurrence**, native proofreading or
a complete word concordance. Read
`editorial-audit/manual-page-evidence-20261020.json`.

QA: stable active 1,795 cards and 1,796 lookup IDs including archived
`dlg024`, 717 original Pocket listening items/1,266 WAV preserved.
Chapter alignment, early content, all 100 dialogues, error repetition
and all six locales tested, with Playwright at 320px and 1440px.
Before and after state preserved by backup. No paid APIs.

Pending: remaining first-four unit explicit word-by-word page evidence,
complete six-language linguistic curation, 1,795-item human review,
more accepted translations and per-option contrastive feedback.

---

## 2026-10-20 — Versioned legacy dialogue and page-evidence release

- Ambiguous legacy `dlg024` has two answers differing only in letter
  case. Its exact original card remains in the ID lookup for scoring
  legacy user answers, global weak review and SRS due items; it is no
  longer served to *new* ordinary learners.
- New independently authored `dlg024_v2` occupies the one active
  dialogue slot instead. It asks for distinct conversational replies
  «Χαίρω πολύ» and «Πού μένεις». Existing IDs, answer history and
  SQLite rows are not renamed or migrated. Active catalog still has
  **1,795** cards (100 active dialogues); legacy addressable lookup has
  **1,796** entries.
- The owner-purchased 314-page textbook PDF was read privately, with
  159 lexical page anchors sampled in printed units 1–4. 126 were
  detected by literal accent-folded PDF text search, 36 happened to
  match the app's approximate page and 33 could not be found in
  the incomplete text layer. **These counts do not certify first word
  introduction or prove lexical absence.** A visual check confirmed
  four real teaching forms `w023,w024,w033,w034` on printed p39,
  and only those four page tags have been changed. See compact
  `editorial-audit/first-four-verified-anchors-20261020.json`;
  no licensed PDF or page images are published.
- Staged QA: 100 active dialogues, six-locale old/new scoring,
  old-debt preserving weak review, source chapter tests, all 717
  listening items and 1,266 WAV, registered HTTP API, phone 320px
  and desktop 1440px Playwright tests including RTL Arabic. No
  external paid API or original publisher exercise reproduction.

Remaining: first four units full human-confirmed lexical inventory,
item-level six-language proofreading, evidence-backed complete page
concordance, broad curated synonym/contrastive explanation expansion.

---

## Dialogue-scoring followup (2026-10-20)

All 100 dialogue response banks are now shuffled independently for each
quiz generation, rather than exposing correct responses at predictable
positions. Existing card IDs, dialogue text, correct gap answers and user
statistics remain unchanged. The legacy dlg024 is still pedagogically
ambiguous; until a versioned replacement is authored, both casing-only
variants count as correct in either gap, so students receive no false
penalty. Verified all six locales using throwaway SQLite and full dialogue
QA; public health/catalog intact.

# Λέξη · curriculum and learning-engine roadmap

Agreed improvement plan, updated 2026-10-20. Status is a factual release state,
not an intention to perform work autonomously between chat turns. The purchased
Patakis PDF stays outside public Core; only derived bibliographic/grammatical
milestones and independently-authored questions may be deployed.

## 20 October 2026 — User-supplied PDF cross-check and new release

The user's licensed 314-page *Ελληνικά Α΄* PDF was reattached and inspected
privately. Source contents on PDF pp 6–9 establish printed units 1–20,
four review units, and grammar/topic introduction milestones. The PDF itself
is NOT hosted on Core and no publisher exercise is reproduced. Evidence
metadata lives in `textbook_evidence.py` and
`editorial-audit/source-alignment-20261020.json`.

Released: offline Pocket listening (717 cards / 1,266 WAV), optional adaptive
difficulty, opt-in per-answer SRS with separate SQLite schedule, deterministic
six-language wrong-answer hints, 20-chapter proficiency heatmap, personalized
pace estimate after ≥12 answers. Production mobile + desktop Chromium and
isolated SQLite/HTTP tests passed. Existing user history preserved.

**Unfinished editorial work**: per-card exact lexical-to-page source
attestation, complete first-four-unit lexical inventory, 1,795-item native
Greek/translations proofread, 100-dialogue naturalness review, multi-language
synonym expansion beyond 42 RU/EN items, skill/page-level heatmap and
individual contrastive mistake explanations. The audit of 1,618
main/supplementary items produced eight same-Greek / different-gloss
review candidates, not eight confirmed mistakes. These remain pending.

## 2026-10-20 — Second source-backed editorial release

Source check: the user's owned 314-page Patakis PDF (locally inspected,
never put on Core) introduces interrogative ποιος / ποια in unit 3 and ages via
Πόσων χρονών in unit 11 (printed p137, PDF p139). Independently
authored `dlg027` moves from unit 2 to 3, and `dlg005` from unit 4
to 11. Only chapter/page metadata change; no old exercise IDs, Greek
answers, user attempts or audio files are modified.

42 per-card hand-curated RU/EN alias mappings (previously 11), including
early greetings, person/gender-specific translations and profession
questions, are gated strictly Greek -> language; other directions stay
exact. Every alias is explicitly registered, never fuzzy. Six-language
wrong-answer notes improve direct verb-conjugation and article-form
comparisons. A separate `details` statistics field now measures:
- provisional per-page accuracy from the trainer's approximate page tags
  (not a claim that the authored sentence appears on the printed page);
- direct article, verb, stress, plural, word order, dialogue and audio drills;
- contextual grammar pattern examples separately from direct knowledge.
Mobile RTL + desktop Chromium and isolated API/DB and previous QA passes.

All 100 dialogue banks passed structural review; the heuristic difficulty
lint currently flags **36** candidates (typically later-unit vocabulary in
distractors), not 36 confirmed errors. A *native* contextual review and
replacement of ambiguous, misleading or premature alternatives remains open.
Full book-text lexical inventory and native six-language proofread of all
1,795 questions remain open; avoid claiming these are completed.

## Dialogue choice-bank refinement (20 October 2026)

After a systematic 100-dialogue heuristic QA (36 flagged cards), 35
stage-inappropriate option banks were hand-replaced with A1/A2-admissible
independently written Greek responses. Each keeps the same original question
text, all original correct answers, 8 distinct bank items, permanently stable
IDs and per-gap SQLite history. Changes are implemented in the
`dialogue_quality.py` stage-gated final catalog pass, not by editing
publisher material or existing student results. Staged HTTP chapter scope,
six-locale grading and regression tests passed.

One legacy card, **dlg024**, remains in a *manual versioning queue*:
«Χαίρω πολύ» and «χαίρω πολύ» are identical answers apart from case.
Changing the two graded answer meanings under the existing ID would rewrite
the educational interpretation of historical attempts. Do not mark this
item or the entire 100-card native-speaker dialogue review complete.

Full textbook lexical/page matching and 1,795-card human linguistic
proofreading remain uncompleted. Page metadata remains approximate.

## Phase 1 — Content correctness and source-alignment

1. **Full card-to-page content cross-check** — PARTIAL. Verified textbook
   20-unit/4-review TOC and early pp14–58 from the purchased PDF. Unit
   anchors for the remainder are topic-level, not exact card-by-card page
   citations. Finish source-backed per-lemma/page evidence, flag unverified.
2. **Prerequisite grammar enforcement** — IMPLEMENTED v1. Milestones in
   `pedagogy_rules.py`; remapped premature early dialogues and future/να
   constructs, with executable tests. Extend to irregular conjugations,
   comparative/adjective morphology and every chapter.
3. **First-four-unit vocabulary inventory** — PARTIAL. Source inspected,
   annotated milestones, corrected Greek form. Need systematic OCR-derived
   *human-reviewed* lexical inventory with missing/extra lemma report.
4. **Dialogue curation** — PARTIAL. 100 unchanged IDs, several premature
   dialogues reclassified. Need native/editor reading of all 100 for plausible
   alternatives, correctness and age appropriateness per unit.
5. **Greek/Russian editorial review** — PARTIAL. Printed text confirms
   one correction (`την λένε` -> `τη λένε`) with old A1/A2 vocabulary ID
   preserved. Full independent proofreading of 1,754 questions remains.

## Phase 2 — Question quality

6. **Plausible distractors** — IMPLEMENTED v1. Same-unit, same grammatical
   form, similarity and studied-stage prioritization; avoids equal EN gloss.
   Follow up with semantic alternative validation and adversarial sample QA.
7. **Multiple correct translations** — IMPLEMENTED v1 for 42 curated
   legacy cards on RU/EN: explicitly reviewed synonyms are accepted and one
   alternate appears alongside the original in the 8-option choice bank.
   Existing history keys remain stable, and all valid answers are highlighted.
   Other locales/old cards require staged human-reviewed gloss expansion.
8. **Article/case micro-exercises** — IMPLEMENTED v1.1: 24 Greek-only
   eight-choice cloze cards; five feminine-accusative final-ν spelling
   variants now count as correct in grammar practice, with localized school
   orthography explanations and preferred form noted. Strict contrasts
   before vowel/κ and wrong gender/case remain incorrect. Per-card progress,
   weak review and six-locale instructions tested.
9. **Word order / sentence construction** — IMPLEMENTED v1: 17 new
   tap-to-compose cards based on independently authored Lexi sentences,
   with undo/reset/submit, 6-language prompts and mobile RTL layout.
   Reconstruct-the-model phrasing is intentionally exact; broader valid
   word-order permutations remain an editorial follow-up.
10. **Accent pedagogy** — IMPLEMENTED v1. The original 549 stress cards
    now allow only vowel targets for written tonos, include six-locale
    feedback on stressed vowels/digraphs, and show verified sense contrasts
    πότε/ποτέ, πόσο/ποσό and μέτρο/μετρό when relevant. No fake options;
    richer syllabic exercises remain future work.
11. **Stage-gated conjugations** — IMPLEMENTED v1. Stage selector 2–20,
    default printed unit 4. Seven verbs and 42 person-form exercises
    available by unit 4; all 17 paradigms by unit 20. Early grouping
    grounded in the owned PDF; later gates are conservative teaching
    milestones, not claims of exact first printed use. Same verb IDs.
12. **Listening comprehension — RELEASED BETA.** Pocket TTS:
    6 approved voices, 633 authored unique texts, 1,266 WAVs and
    717 word/phrase/sentence listening exercises with chapter/page scope
    and per-user weak review. Rejected Piper legacy disabled. No
    microphone/recognition or paid external TTS API.

## Phase 3 — Session design and learning efficiency

13. **Strict no repeated word within normal session** — IMPLEMENTED v1.
    Canonical `semanticId` across translation, stress and source duplicates,
    including personalized words and 60-item API boundaries. Weak review still
    intentionally repeats to close debts. 240-disjoint-items proof in
    `qa_pedagogy_upgrade.py`.
14. **Guarantee duration/capacity** — PARTIAL v2. The read-only capacity
    endpoint counts semantic-unique cards under current scope/level filters;
    a six-locale setup button shows whether material is likely sufficient
    for selected duration at an assumed 20 sec/item. Thirty minutes = about
    90 answers; first five printed chapters expose about 304 unique targets
    with broad types. This is not a time guarantee or actual user pace model;
    multi-step cards and long-session bounds need further engineering.
15. **Adaptive difficulty — IMPLEMENTED opt-in v1.** Uses up to 40 recent
    answer outcomes to prioritize word/form/phrase/sentence difficulty
    strictly within the student's already selected curriculum scope.
16. **Spaced repetition — IMPLEMENTED opt-in v1.** Separate
    `srs_schedule` table, 1/3/7/14/30/60/120/180-day expanding schedule,
    ten-minute retry after a miss, user-specific due button. No
    retroactive opt-in or rewrite of historical scores.

## Phase 4 — Feedback/analytics

17. **Page/topic mastery heatmap — PARTIAL v1.** Twenty-chapter accuracy
    grid available; under eight answers explicitly provisional.
    Verified page/topic/grammar skill details remain unfinished.
18. **Explanations of wrong answers — IMPLEMENTED limited v1.**
    Deterministic six-language feedback for articles, conjugations,
    accent, plural, word-order and dialogues, generic gloss reminder for
    other kinds. Does not claim fully diagnosed contrastive explanations.

## Release and safety boundaries

- Current released textbook catalog: 1,795; independent A1/A2: 1,700.
- Permanent card IDs and old answer history retained; the single Greek
  correction keeps legacy `book_d37c2e558c331d` vocabulary ID.
- Last code and consistent DB backups:
  `/opt/greek-trainer/backups/pre-phase2-cards-20261020T072939Z.tgz`;
  `/var/lib/greek-trainer/progress.sqlite3.pre-phase2-20261020T072939Z`.
- Phase 1 Python QA, seven isolated jsdom scenarios, Chromium RU/AR 320/390
  passed; only `greek-trainer.service` restarted. No changes to VPN/Matrix.
