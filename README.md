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

## 2026-10-20 — Stage-safe Greek dialogue answer banks

`dialogue_quality.py` modifies only distracting (incorrect) choices for
35 of 36 previously flagged Greek-only dialogue items. Correct gap
answers, the scripts themselves, original IDs and all user histories remain
unchanged. The original 100 dialogues and 8 choices per item remain; the
remaining `dlg024` needs a versioned semantic replacement rather than
silently changing existing graded answers. This is not a claim of full
native-language proofreading.

QA: 100 original dialogue IDs and 15/77/8 gap layouts, all six locales
per-gap scoring, no premature later-stage vocabulary in curated banks,
additional SRS weak-repeat QA, 20-chapter alignment, 717 listening cards
and 1,266 WAV coverage, staged authenticated HTTP. See
`editorial-audit/dialogue-curation-20261020.json`.
Rollback archives: `backups/pre-dialogue-curation-20261020T1349Z.tgz`
and `/var/lib/greek-trainer/progress.sqlite3.pre-dialogue-20261020T1349Z`.
The user's purchased textbook PDF was consulted privately and NOT deployed.

---

## 2026-10-20 — Follow-up PDF-aligned content and analytics release

- Verified source milestones from user's purchased 314-page PDF *privately*:
  Greek interrogative ποια is unit 3, question πόσων χρονών is introduced
  with housing/age in unit 11, printed p137. Corrected *only metadata*
  of original dialog IDs dlg027 (unit 2 -> 3) and dlg005 (unit 4 -> 11).
  No textbook PDF, scanned pages or publisher exercises are shipped.
- Curated 42 safe RU/EN alternative-translation sets (previously 11).
  Exact direction and source-card identity remain strict.
- Stats includes honest approximate-page and tested-exercise skill
  breakdown, separate from contextual grammar pattern exposure.
- Wrong-answer guidance now identifies a selected incorrect verb
  paradigm form or article choice in all six UI languages without
  pretending to diagnose all linguistic errors.
- Dialogue QA `editorial-audit/dialogues-20261020.json` reports 36
  *candidate* issues out of 100, primarily late-unit distractors.
  Human/native review is NOT complete; do not silently replace
  plausible Greek alternatives with wrong-only choices.
- QA: temporary SQLite, all 6 locales, previous 11 Python regressions,
  browser 320px and 1440px including Arabic RTL, live health/catalog.
  Restore archive: `backups/pre-editorial-20261020T1320Z.tgz`;
  consistent database backup: `/var/lib/greek-trainer/progress.sqlite3.pre-editorial-20261020T1320Z`.

Remaining: full source-to-lemma concordance and page provenance,
full native proofreading, dialogue-bank context curation, six-locale
translation synonym coverage. No paid APIs or microphone functionality.

---

## 2026-10-20 — User-PDF grounded six-cycle upgrade

The user has reattached their owned 314-page Patakis *Ελληνικά Α΄*.
Contents PDF pp 6–9 anchor all 20 course units and major grammar
milestones. Only independent source-alignment metadata is deployed
(`textbook_evidence.py`, `editorial-audit/`). PDF itself stays private.
Static editorial audit covers 1,618 main/supplementary cards, 516 in
units 1–4 and 100 dialogues; eight same-form/different-gloss review
candidates are not confirmed errors. Detailed per-lemma citations and
independent native proofreading remain editorial work.

Released: `learning_engine.py` opt-in SRS and due mode (separate
`srs_schedule` SQLite table), opt-in answer-based adaptive selection,
deterministic per-mistake six-locale guidance, 20-chapter provisional
mastery heatmap, observed-pace duration estimates when enough attempts
are available. Existing 1,795 card IDs and answers preserved; old
review/SQLite history untouched. 717-card Pocket listening BETA remains
available. No paid API or microphone.

Release smoke verifies health, 1,795/717 catalogs, static assets,
SQLite quick_check, and systemd healthy; new-feature Chromium 320px
and 1440px including Arabic RTL and previous core QA passed.
Backups: `backups/pre-20261020-sixcycle.tgz` and
`/var/lib/greek-trainer/progress.sqlite3.pre-sixcycle-20261020`;
candidate backup: `backups/sixcycle-candidate-20261020.tgz`.

Still incomplete: native proofreading of all 1,795 questions,
a complete lexical inventory and item-to-book-page evidence,
100-dialogue naturalness audit, more curated correct translations
across all six languages, page/grammar mastery and detailed
contrastive explanations.

---

## 2026-10-20 — Final six-voice Pocket roster (NO Meta MMS)

- User approved all the candidate Pocket voice profiles and explicitly
  requested dropping Meta MMS. **Six final profiles:** Athina, Eleni,
  Katerina (female), Kostas, Spyros, Nikos (male). All voice presets come
  with the model. No user-supplied recordings, accounts, API keys, or paid
  services. Meta MMS remains only in historical experiment directory, not
  in the approved active roster, comparison gallery or current ZIP.
- Accepted two styles per Pocket voice: sentence-chunked `temp=0.3,
  sampler_decode_steps=5` (clear), and `temp=0.6, steps=5` (lively), with
  220ms gaps. `tts-evaluation-pocket/voice_roster.py` is the canonical
  approved offline set. `build_roster_gallery.py` now renders SIX Pocket
  voice profiles and 12 same-paragraph samples, no Meta audio. Public: 
  `https://potapovfamily.com/greek/tts-demo/pocket-long/`.
- **Short utterance QA:** one isolated word (`ελεύθερη`), phrase and
  sentence in two styles with each of the six voices = 36 private-generation
  samples. Generator `test_short_cards.py`, all files 24kHz mono WAV. New
  read-only public evaluation page `/greek/tts-demo/pocket-short/` and 36-WAV
  ZIP to assess possible swallowed/blurred short words before production.
- **Important:** Whole-course audio not regenerated; student listening remains
  ALPHA-disabled until short-utterance articulation passes human evaluation.
  Existing original 1795 cards, student history and sign-in unaffected.

---

## 2026-10-20 — Diversified voice candidates (listening ALPHA still OFF)

- User approved Pocket TTS Athina female and Kostas male in **two specific**
  synthesis settings: `temp=.3, sampler_decode_steps=5` with each sentence
  spoken independently, and `temp=.6, sampler_decode_steps=5` with the same
  sentence chunking. Silence between sentences = 220 ms. Do not confuse
  different presets with tempo/pitch effects. Each full paragraph is identical.
- Locally generated matching samples for **Eleni and Katerina female** and
  **Spyros male**, plus **Nikos male as a same-engine fallback**. The separate
  previous Meta MMS male from the user's approved original style 04/05 has
  also been rendered on the *identical Greek text* as an optional sixth voice;
  it uses the existing offline CPU model with no always-on service.
- Candidate roster: 3 women Athina/Eleni/Katerina; 3 men Kostas/Spyros/Meta;
  optional all-Pocket sixth voice = Nikos. Only Athina and Kostas were already
  user-approved at this point; all other voices require listening verification.
- `tts-evaluation-pocket/test_candidates.py` is isolated CPU generation;
  `tts-evaluation-mms/render_match.py` is the two-settings Meta match.
  `tts-evaluation-pocket/build_roster_gallery.py` builds the 14-clip gallery,
  `all-voices.zip`, and a private `ensemble-manifest.json`.
- Public **testing** only: `https://potapovfamily.com/greek/tts-demo/pocket-long/`.
  The `serve_pocket_long_demo()` handler allowlists just the WAV filenames,
  CSS/HTML and ZIP. Underlying weights, generation scripts, and the manifest
  cannot be read via the public route. Existing old demos are preserved.
  All clips are offline-precomputed and cost no per-user API fees. Mixing the
  two model pipelines increases *batch setup* complexity only; audio on Core
  is ordinary static WAV, so Mac mini M1 never needs real-time TTS.
- **Do not reenable listening ALPHA or mass-generate the curriculum** before
  learner verifies the new candidates' enunciation and approves the roster.
  Existing original 1795 book cards and all accounts/progress unchanged.

---

## 2026-10-20 — ALPHA audio disabled + desktop layout repaired

- Bad Piper Greek recordings rejected; listening ALPHA temporarily unavailable on both client and server. Direct quiz calls return 503, old audio HTTP 410; no listening scoring. Backup saved before deleting all 2 listening attempts and 2 associated progress records, preserving all other accounts/progress.
- Desktop chapter selector fixed: previous flex layout squeezed long chapter titles into a letter per line. Now explicit 3-row CSS grid. Real Chromium verified widths 1440,1200,1024,900,760,390 with non-overlapping content and zero overflow.
- JOY (Greek native-speaker CC BY-NC model) is gated on Hugging Face; user must accept repository terms. Google Chirp3 HD has free monthly quota but requires enabled billing. Apple system voices are not licensed for public redistribution; macOS Melina sample kept private only. No new TTS voice published.
- Previous backups: /opt/greek-trainer/backups/pre-listening-alpha-20261020T091642Z.tgz and /var/lib/greek-trainer/progress.sqlite3.pre-alpha-20261020T091643Z.
- User permanently excludes microphone recording, speech recognition and pronunciation evaluation from this free public app.

---

## 2026-10-20 — Offline Greek listening mode, no paid APIs

User chose listening comprehension ONLY. User microphone, speech recognition
and pronunciation assessment are explicitly out of scope for this free public
product. No per-user paid API, donation flow, or recurring expense added.

- Local Piper el_GR-rapunzelina-medium Greek voice; checked its downloaded
  MODEL_CARD shows the training dataset license CC0. Generated once using
  disposable piper-tts 1.3 container, model stored privately in voice-model,
  dependencies offline under tts-deps; no synthesis on web requests.
- 717 independent audio question IDs from self-authored existing textbook
  words/phrases/sentences, spanning all 20 printed book sections. 633 distinct
  immutable SHA-addressed mono PCM 22,050Hz WAV files total ~69MB, same
  Greek sentence shared by multiple cards. Source PDF and publisher exercises
  were not uploaded or served; model and build tools not publicly served.
- Original 1795 textbook cards and 1700 independent A1/A2 vocabulary items
  keep their IDs and meaning. Listening virtual cards are a separate catalog.
  New setup scope chooses printed chapters, defaults units1-4 and shows count
  of prepared audio per chapter; duration/capacity preview uses semantic
  uniqueness as before. Six interface languages localize all controls.
- Listening question GET contains translated generic prompt, eight possible
  meanings, audio URL, but NO Greek transcript until scoring. Learner first
  clicks Play or Slow (0.8x) to unlock choices; failed playback cannot create
  a wrong answer. Greek transcript is shown only on graded answer, and
  mistakes return through existing SQLite weak review (same two-correct
  settlement). Separate kind stats/leaderboard integrated without migration.
- Public audio endpoint only serves allowlisted hash-named WAV assets, with
  audio/wav, nosniff, one-year immutable browser caching and media-src same
  origin CSP. Arbitrary paths and voice-model access remain blocked.
- qa_listening.py covers 717 IDs, 633 valid WAV assets, first-four-unit
  capacity, six locale grading, hidden transcript, multi-batch de-dup,
  all 20 chapter scopes, weak review, historical data isolation and invalid
  audio names. qa_listening_dom.js verifies UI gating/controls/reveal and
  qa_listening_chromium.js verifies real Chromium 320px playback including
  Arabic RTL and speed switch. All 11 earlier Python, 11 DOM and four
  existing mobile browser regressions passed on isolated test DBs.
- Source archive before edits:
  /opt/greek-trainer/backups/pre-listening-20261020T083602Z.tgz
  SQLite backup:
  /var/lib/greek-trainer/progress.sqlite3.pre-listening-20261020T083602Z
- Audio is synthetic, not native-speaker-certified; teachers should review
  stress and prosody. Files require regeneration if the authored text changes.
  There are VPS bandwidth/storage costs but NO metered third-party calls.

---

## 2026-10-20 — Stage 3: stress pedagogy, gradual verb scope, capacity preview

- Accent practice: 549 original stress cards keep IDs and user progress; consonants are shown as word skeleton but disabled as tonos targets. Six-language feedback explains stressed vowel and second-vowel written accent in ει/οι/αι/ου, plus curated semantic contrasts πότε/ποτέ, πόσο/ποσό, μέτρο/μετρό when the source word matches. No fabricated Greek forms are created.
- Verb conjugations: introducedUnit in the separate 17-lemma present-tense course, book-unit selector 2–20 (default 4) and filtered reference tables. The purchased PDF grounds μένω in unit2, δουλεύω unit3 and γράφω/διαβάζω/μιλάω/ρωτάω/απαντάω in unit4; later milestones are cautious editorial stages, not exact word-first-occurrence citations. Stage2 = 6 questions; stage4 = 42; unit20 = 102 available person forms. B1 accepted alternates were confirmed correct and left unchanged.
- Capacity preview: authenticated, read-only capacity API with unique semantic fingerprints, page/chapter/verb/topic filters and learned personalized words. Setup button provides current count, required count for selected duration at 20 secs/item and translated low-supply guidance in six languages. Not a guarantee; actual pace and multi-step answers vary.
- Tests: qa_stage3.py checks the 2/4/20 unit gate, count estimate, all six stress notes and historical IDs. qa_stage3_dom.js covers real login, stage selector, shortage warning and vowel-only stress. qa_stage3_chromium.js confirms 320px mobile stage control. Nine legacy Python suites, eight older DOM flows and mobile Chrome (RU/AR × 320/390) passed on isolated databases. No production DB migrations.
- Backups prior to code change: /opt/greek-trainer/backups/pre-stage3-pedagogy-20261020T080423Z.tgz and /var/lib/greek-trainer/progress.sqlite3.pre-stage3-20261020T080423Z.
- Future: native audio/listening, actual-pace duration planning, adaptive progression, SRS, heatmaps and comprehensive linguistic audit.

---

## 2026-10-20 — Pedagogical final -ν: acceptable forms are not mistakes

- Reported learner pain: article cloze “Ξέρεις ___ Μαρία;” graded `την` wrong against book-preferred `τη`. The Greek school orthographic convention generally omits the feminine article's final `-ν` before μ/λ/φ/ζ, but the longer feminine accusative retains the correct gender/case. This article-grammar trainer now **accepts both with full credit and zero miss debt**, while clearly labelling the book-preferred spelling and displaying a six-language explanation after answering. The alternate is **not** promoted as equally preferred standard orthography.
- `form_exercises.py` has **five explicit scoped** article/preposition cards with accepted forms: `στη/στην Λευκωσία`, `τη/την Μαρία`, `τη/την λέξη`, `τη/την φίλη`, `τη/την ζάχαρη`. Other targets preserve the school rule: e.g. `την Άννα` (vowel) and `στην Κύπρο` (κ) remain strict; masculine `τον`, neuter `το`, wrong cases and genders remain strict. No blanket text replacements or grade inference.
- The server exposes `acceptedAnswers`, `preferredAnswer`, `spellingNote`, `acceptedVariant` only for the appropriate Greek-only article task, with no changes to permanent question IDs or scoring table. In the browser both valid forms highlight green, with a subtle “По учебнику” marker on the preferred form and a real explanatory note. All six locales RU/EN/ZH/AR/ES/PT are translated; initial question only says alternative spelling may exist, without revealing the correct article.
- Existing historical failed attempts cannot be selectively regraded: the old answers table records correct/incorrect but **not the exact selected option**. Future retained-ν answers are correct and can close any existing miss debt normally. No historical data was deleted or altered, and no DB schema migration.
- Regression `qa_final_n.py` covers all five contexts times six languages, wrong-vowel/κ/case/gender cases and miss-debt resolution; `qa_final_n_dom.js` covers actual selected `την` on Μαρία plus rejected `τη` on Άννα; updated `qa_forms_chromium.js` taps `στην` on 320px mobile and checks both green, source note and Arabic RTL. Existing Python tests and browser regression flows pass in isolated temporary DBs.
- Backups: `/opt/greek-trainer/backups/pre-final-n-20261020-20261020T075149Z.tgz` and `/var/lib/greek-trainer/progress.sqlite3.pre-final-n-20261020-20261020T075149Z`. Only greek-trainer.service is to be restarted.

---

## 2026-10-20 — Pedagogy phase 2: reviewed alternatives, article/case and sentence-building exercises

- Grounded specific grammar milestones in the user's purchased Ελληνικά Α΄ PDF (reviewed native page text): printed book unit 2 has μένω/στον/στην/στο, unit 3 contains family/ο/η/το, unit 4 contains ξέρεις τον/τη/την/το, unit 8 contains purchases/articles. **Only independent custom exercise text is deployed**; the PDF stays private in ChatGPT.
- New `form_exercises.py`: 24 carefully written, chapter- and page-scoped article/preposition cloze cards using exactly eight Greek form choices, introduced only at units 2/3/4/8; 17 tap-to-reassemble Greek sentence cards reusing already authored application sentences. Added new `article` and `order` types to setup, quiz/stats/weak modes; IDs stable and separate from original 1,754 and A1/A2 course. Main course count **1,795**, separate vocabulary remains exactly **1,700**.
- Order sentence UI in six interface languages: press original Greek word tiles in order, composed preview, Undo, Reset, Check. Multiple repeated identical Greek tokens are distinct selectable positions. The task asks to reproduce the given model sentence; other grammatically possible word orders are not yet auto-approved.
- `accepted_glosses.py`: human-curated alternative translations for eleven stable existing RU/EN cards, source direction only. A second accepted variant is displayed among eight options. Both it and the original are graded correct; additional pre-reviewed aliases are accepted server-side. Same card progress ID is preserved; different register (e.g. ты vs вы) still graded separately. No blanket lexical-similarity acceptance.
- Client changes clear word-order CSS/layout on every new question, prevent partial phrase submissions, show six-locale labels and a subtle notice for tasks with multiple right translations. Mobile has Greek left-to-right text inside Arabic RTL layout.
- `qa_form_exercises.py`: validates 41 new cards, real chapter placement, 8 unique answer options on article tasks, six language prompts, full original token banks with duplicates, answer/weak debt and account isolation, acceptance/rejection of curated alternatives in RU/EN. `qa_forms_dom.js` E2E covers 8-choice Greek article, tap-to-compose, undo/reset, correct answer, styling reset, reviewed alternative; `qa_forms_chromium.js` verifies actual Chromium mobile 320px with Arabic RTL. All prior Python and DOM regressions and mobile Chromium 320/390 RU/AR plus six-language locale switching pass. No DB schema changes or unrelated service restarts.
- Backups before change: `/opt/greek-trainer/backups/pre-phase2-cards-20261020T072939Z.tgz`, consistent SQLite `/var/lib/greek-trainer/progress.sqlite3.pre-phase2-20261020T072939Z`.
- Still pending on roadmap: complete 1,795-card Greek/Russian proofreading, source-linked detailed lexicon index, more curated valid translations on all six languages, accent pedagogy, staged conjugations, listening/audio, SRS, skill-level analytics, and individual wrong-answer explanations.

---

## 2026-10-20 — Pedagogical quality pass #1 (PDF-aligned Greek + session uniqueness)

This is the **first implemented stage** of the approved 18-item improvement roadmap, NOT a claim that all 18 items or all 1,754 questions have been linguistically proofread.

- Grounding: the user-provided, purchased 314-page Ελληνικά Α΄ PDF, with native text checked for printed pp14–58. Specifically confirmed book unit 3's printed «Τη λένε Ελένη» (PDF p42), unit 4's μιλάω conjugation and ξέρεις τον/την/το (PDF pp51–56), introductory numbers, and actual printed lesson/review boundaries. The PDF and OCR extracts were **never sent to Core or served**; only original independently authored questions and pedagogical metadata are deployed.
- `pedagogy_rules.py` adds high-confidence introduction milestones for early grammar (greetings/είμαι, μένω/έχω, family/ποιος, languages/μιλάω, plural nouns, aorist, future θα, subjunctive να, imperative, doctor conditional), semantic fingerprints based on canonical Greek lemma, and a reproducible documented set of out-of-context original dialogue IDs. `textbook_alignment.py` relocates inappropriate early dialogs (forms καλώς ήρθες, μαθαίνω, passive γράφεται) and additional 10 later-grammar dialogs/phrases (future θα and late να) into appropriate printed teaching units without altering permanent question IDs or histories. The unit-3 age dialog is also moved to unit 4 where that expression appears. `qa_pedagogy_upgrade.py` checks that early dialogue/phrase/sentence questions no longer require unattested later grammar, and no book card has a later grammar prerequisite than its assigned unit.
- Corrected `w034` Greek from `την λένε` to standard `τη λένε` in accordance with printed book p40. **The old book-derived A1/A2 vocabulary-course identifier is deliberately retained** by an explicit historical spelling alias, so no existing vocabulary progress is lost. This is one documented source-supported correction, not silent broad proofreading.
- `server.generate_options` ranks distractors by studied-unit readiness, same-unit and part-of-speech characteristics, Greek morphology and surface similarity. It avoids identical English glosses as falsely incorrect synonyms. Eight distinct answer choices remain across all six supported languages. Sentence/phrase pools may cross-kind as fallback when the first chapters have fewer than eight genuine distractors; this is not a professional ambiguity-proof guarantee.
- **Normal practice is now repeat-free by Greek lexical/semantic target**, not just by answer direction: one card's meaning cannot return as a different card ID, accent card, review clone or reverse-language translation in subsequent 60-card batches. Individual verb-person drills retain distinct IDs, and **global/scoped weak-review mode deliberately still repeats failed answers** until their miss debt is cleared. Personalized learned word cards use the same semantic fingerprint as textbook words. For the first five printed sections, tests confirm at least 240 distinct no-repeat answer cards across four API batches, exceeding a 30-minute session at one item/20 seconds; dialogues may still have several legitimate blanks as one activity. A six-language explanatory note was added near session duration.
- QA: `qa_pedagogy_upgrade.py`, `qa_patakis_alignment.py`, `qa_vocab_1700.py`, `qa_localizations_1700.py`, `qa_new_features.py`, `qa_dialogues_100.py`, `qa_weak_global.py`, six browser jsdom scenarios and real mobile Chromium Russian/Arabic 320/390 px checks. `qa_dialogues_dom.js` was retargeted from obsolete p78 to an intact three-gap restaurant exercise p198 following the editorial grammar move. No DB schema migration, history wipe or unrelated service changes.
- Code archive: `/opt/greek-trainer/backups/pre-pedagogy-audit-20261020T065925Z.tgz`. Consistent DB snapshot: `/var/lib/greek-trainer/progress.sqlite3.pre-pedagogy-audit-20261020T065925Z`.
- Still **outstanding**: comprehensive item-by-item Russian/Greek linguistic proofread of all 1,754 cards, a verified complete lemma-to-page index for every page, native audio/listening, alternate-correct-answer acceptance, grammar fill/build exercises, spacing algorithm, interactive error explanations, SRS, skill heatmaps, and proactive course-length estimation. These are later separate roadmap phases; do not describe them as completed.

---

## 2026-10-20 — Real Patakis PDF curriculum reconciliation (20 printed units)

Reviewed the **user-provided complete purchased** 314-page PDF of Ελληνικά Α΄ (the book has 312 printed pages). The print-to-PDF page offset is +2. It has **20 numbered printed sections** (four are review/test units 5,10,15,20) plus alphabet introduction and appendix, whereas the earlier app mistakenly called the 16 teaching topics “chapters 1–16”. Source is the actual PDF table of contents and selected grammar and example pages, NOT Google Books or synthetic estimates.

- Added textbook_alignment.py: 20 printed units, verified start/end page ranges, subject/grammar focus for each in Greek, four review units and explicit OLD internal 16-to-PRINTED mapping. The original 1,680 cards keep every prior ID, Greek text, all six-language translations, answer choice and progress key (verified byte-equivalent core source/answer fields against the pre-release code backup). About 900 existing exercise records had their chapter labels corrected; page anchors are normalized to the actual printed unit (approximate within-unit for independently authored exercises). All historic stats are re-grouped by current card ID, without mutating historical attempts.unit in SQLite.
- Redistributed existing noticeably out-of-place examples: original coffee/store dialogues removed from languages unit 4 and placed in everyday purchases unit 8; bus directions and tickets moved to travel unit 6; apartment/rent to unit 11; hotel/leisure to unit 16; pharmacy to doctor unit 18; old daily groceries to unit 8 rather than clothes unit 9; travel-in-present placed under holidays where appropriate. Noun plural exercises from premature early units move to printed unit 8 (their morphology is introduced there). Numbers 1–10 are unit 1, interrogative ποιος is unit 3, μιλάω is unit 4.
- Added 74 **independently written** situation-appropriate supplementary translation cards (IDs patk*, no copied publisher content): six examples each for printed units 1–4; 20 clothing/colours/adjective-agreement examples for unit 9, four home/comparative examples in unit 11, four past-tense travel items in unit 12, six tavern/future examples in unit 14, four να-subjunctive examples in unit 16, four job/imperative examples in unit 17, four doctor/conditional examples in unit 18, and four public-service examples in unit 19. New localized RU/EN/AR/ZH/ES/PT glosses are machine-assisted candidates, with separate repeatable editorial overrides for obvious sense mistakes. The purchased PDF itself is not uploaded to Core, bundled, served, or made public.
- The separate **1700-word A1/A2 vocabulary course** stays separate and all 1700 word IDs/levels/translations unchanged; new textbook supplemental words are deliberately excluded from its source pool. New overall textbook-card count is **1754** versus 1680.
- Browser chapter navigation now shows the real book title, printed page span, and short Greek grammar/function focus for every section (including 5,10,15,20 marked as review). Saved 16-section selections from older browsers migrate once by old-to-printed semantic identity. Main/footer 16 chapter labels replaced with 20 printed units, static asset versions bumped (app.js v20, css v18).
- Coverage tests qa_patakis_alignment.py prove printed 20 section spans, exact quiz chapters and page selectors (5=review, 6=transport), all original IDs, all 74 new questions in 6 UI languages and two translation directions with 8 choices, legacy per-card accent relocation, archival stats recomputed by ID, and independent vocab 1700 unchanged. Existing QA and JS browser regressions retained. Full semantic human proofreading of all previously existing 1,680 items is a **separate editorial follow-up**; the mapping and selected content mismatches are comprehensively addressed here.
- Pre-deployment code backup: /opt/greek-trainer/backups/pre-real-patakis-toc-20261020T061228Z.tgz; consistent SQLite: /var/lib/greek-trainer/progress.sqlite3.pre-real-patakis-toc-20261020. No changes to database schema or unrelated services.

---

## 2026-10-20 — Dialogue last-gap continuation fix

- Fixed the mobile screenshot bug after answering gap 2/2: button previously kept the stale 'Next gap' label from the first gap. `renderDialogueGap()` now resets the button state at every new gap and `choose()` explicitly uses a localized Continue label after the last gap (all six languages).
- On grading any dialogue gap, the Greek line is filled immediately, the active placeholder loses its highlight, and the chosen/correct Greek answer appears in the dialogue as a completed span. On the final gap the instruction changes to a localized 'All gaps filled; Continue' message.
- The separate early-termination action explicitly reads 'End practice' / 'Завершить тренировку' instead of ambiguous 'Finish'. After Continue, normal practice advances to a new unseen card, or automatically shows results if the selected material is exhausted; no silently restarting an already completed single-dialogue session to fill the timer. Weak practice retains the necessary second pass to clear mistakes.
- Added qa_dialogues_2gap_dom.js (both normal 2-gap and gap1-only weak cases; test 2-pass debt reduction and correct auto-finish), tightened qa_dialogues_dom.js assertions for 1/3 gaps, and added mobile Chromium assertions to qa_mobile_chromium.js. All Python regression suites, four legacy DOM tests, both new DOM scenarios, and real Chromium 320px Russian/Arabic 3-gap touch tests passed. No DB schema/progress change.
- Backups before change: /opt/greek-trainer/backups/pre-dialogue-next-fix-20261020T034325Z.tgz; /var/lib/greek-trainer/progress.sqlite3.pre-dialogue-next-20261020. Only greek-trainer.service should be restarted.

---

## 2026-10-20 — Account-wide weak practice button

- Fixed My Mistakes showing global count while its practice button unexpectedly inherited selected page/chapter/type and UI language filters, producing empty sessions. The My Mistakes button now starts mode=weak_all, selecting every actionable saved weak answer independently of current textbook scope. Normal textbook/scoped weak API modes remain unchanged.
- Saved answer language and direction is preserved on each review card; three Spanish failed answers and one Greek dialogue are reviewable from a Russian UI without writing mistakes under the wrong language. Verb conjugation and translation stages are independently reviewable. UI indicates the original language when different from the selected one.
- Old/unsupported/orphaned card keys are still preserved in SQLite but excluded from reviewable count, with a localized warning. Stats reports weak (actionable), weakOverall, weakUnavailable. No user progress or schema mutation.
- Localized weak-tab explanation and warnings in RU/EN/ZH/AR/ES/PT; main JS asset version bumped to v18.
- New tests qa_weak_global.py (isolated DB) and qa_weak_global_dom.js (isolated web browser DOM) reproduce four cross-language mistakes under mismatching filters and their resolution after two correct reviews. Prior Python regression suites and baseline DOM browser tests pass.
- Backups: /opt/greek-trainer/backups/pre-weak-global-20261020T024505Z.tgz and /var/lib/greek-trainer/progress.sqlite3.pre-weak-global-20261020.

---

## 2026-10-19 — Complete UI locale refresh and leak prevention

- Fixed the real Portuguese screenshot regression: the catalogue summary was computed once on initial load and retained its original Russian value on language switches. updateLanguage() now always re-renders it from the active locale, and a real Chromium test verifies RU -> PT -> AR -> ZH -> ES -> EN -> PT -> RU, including the Portuguese wording of all 1680 textbook cards.
- Systematically inventoried all six UI dictionaries: all 155 keys are now populated in RU, EN, ZH, AR, ES, PT. Future missing non-Russian translations fall back to English, not Russian. The inventory QA fails for missing keys. English parenthetical learning hints remain separate from ordinary interface translations.
- Localized registration nickname placeholder, footer and browser tab title, plus the unused-but-defined topic-mode labels previously shown in English under ZH/AR/ES/PT. Standalone vocabulary UI remains translated on language switches, and Greek dialogue content/answers remain Greek-only.
- New automated tests qa_locale_inventory.js, qa_ui_locales_dom.js and qa_ui_locale_chromium.js; all former Python and browser regressions passed on isolated test databases. No changes to accounts, authentication code, user progress or card IDs.
- Backups: /opt/greek-trainer/backups/pre-ui-locale-audit-20261019T201341Z.tgz; /var/lib/greek-trainer/progress.sqlite3.pre-ui-locale-audit-20261019.

---

## 2026-10-19 — 100 Greek-only dialogues

Expanded 20 original conversations to 100, adding 80 new exercises (five per chapter across all 16 book chapters). 15 dialogues have one gap, 77 two and 8 three; each exercise presents eight unique Greek-only options, with contextually unrelated distractors. New stable IDs dlg021–dlg100, original 20 cards unchanged. Server and browser now score and show an arbitrary number of gaps; weak practice can target only gap2 if earlier blanks were correct. Source: dialogues_extra.py; tests: qa_dialogues_100.py, qa_dialogues_dom.js, and previous regression suites.

The Russian translation completeness check found 1,700 non-empty Cyrillic glosses. This is a basic integrity review, NOT full linguistic proofreading of all entries; that remains an editorial follow-up. No existing Russian translations or account progress were changed. Code backup: /opt/greek-trainer/backups/pre-dialogues100-20261019T191113Z.tgz. SQLite backup: /var/lib/greek-trainer/progress.sqlite3.pre-dialogues100-20261019. Only greek-trainer.service was restarted.

---

## 2026-10-19 — Complete non-English translations across 1,700 A1/A2 entries

- All **1,700 course headwords** now have nonempty localized teaching glosses in **Arabic, Simplified Chinese, Spanish and European Portuguese** (4 × 1,700 = 6,800 locale values), in addition to the already-complete English and Russian. Previous baseline: Arabic 393, Chinese/Spanish/Portuguese 498 each. No English fallback is used as the *sole* translated answer for a vocabulary-course card. English remains an optional parenthetical learning hint in translation questions and answer choices only, as requested.
- Saved by immutable course card ID in `vocab_translations_1700.json`; the original Greek/Russian/English, levels, IDs, per-account answer history and vocabulary batches are unchanged. `vocab_lessons.py` verifies total ID coverage and all values when importing, to avoid silently offering missing glosses. `personalized.py` reuses exactly this card atlas.
- Translations are machine-assisted drafts from existing contextualized English glosses, not an assertion of professional proofreading of all 6,800 values. Spot-checked sense/part of speech and directly corrected **153 target-language glosses across 51 ambiguous Greek headwords**, recorded in `vocab_manual_corrections.json`. Generators and repeatable review overlay: `fill_vocab_locales.py` and `apply_reviewed_locales.py`.
- Supplemented **511** missing English-gloss keys for textbook Arabic-only translations in `textbook_ar_complete.json`, while preserving any prior Arabic translations. Alphabet, accent, sentence and vocabulary type exercises continue with the original Greek answer validation. Greek-only dialogues have intentionally no non-Greek translations.
- Replaced temporary English fallback for the 102 contextual Greek verb sentences in each of Chinese, Spanish and Portuguese with **306 explicit, present-tense, six-person reviewed translations**: `curate_verb_phrase_locales.py` outputs `verb_phrase_locales.json`. All six distinct pronoun/person forms are represented in Spanish and Portuguese. Arabic already had 102 phrase translations and is retained. Tests ensure eight distinct choices and correct answer alignment.
- `vocab.js` now exits an active standalone lesson on UI language change, preventing old-language choices from being graded as responses in the newly selected language. It does not clear stored progress.
- `qa_localizations_1700.py` checks entire 6,800-translation atlas, script presence, source field correctness, 13 themes × 2 levels × 6 languages = 156 ten-word quiz scenarios, answer matching and 102 verb sentence options across all locales. Original `qa_vocab_1700.py`, `qa_new_features.py`, `qa_dom_test.js`, `qa_new_dom.js` regressions preserved and run. New PDF/doc tools not used. This release makes no database changes.
- Pre-update backups: `/opt/greek-trainer/backups/pre-locales1700-20261019T185155Z.tgz` and consistent SQLite backup `/var/lib/greek-trainer/progress.sqlite3.pre-locales1700-20261019`. No unrelated VPS, VPN, Matrix or telemetry components are changed.


---

## 2026-10-19 — Expanded independent vocabulary corpus: A1 700 + A2 1000 (current)

- Deployed the lexical curriculum target as **1,700 learner-facing Greek headword records**: A1 **700**, A2 **1,000**. Added **249 A1 + 623 A2** on top of the previous 828 records. The existing earlier 828 records, identifiers, original RU/EN glosses, topics, and level labels were verified byte-for-byte equivalent; no account or SQLite data migrations.
- The added **872 entries have manually authored Greek headwords (with accents), Russian and English meaning glosses**. Editors seeded candidate sources in `vocab_expansion_a1.tsv` (558 authored candidates) and `vocab_expansion_a2.tsv` (1,752 authored candidates). Offline deterministic selector `build_curated_vocab.py` filters near-duplicates and compositional phrases; the output `vocab_curated_1700.tsv` is the **only expansion source used by production**. No raw Kelly frequency list copied into serving data; Kelly corpus data has distinct original research terms. Editor selected entries with fixed per-topic quotas, 13 topics total, at least 80 unique lexical headword records per topic across levels. All 623 new A2 entries are single-token lexical headwords after removing the noun article, not inflections or arbitrary multiword expressions.
- Stable IDs: new IDs `lexi_<sha256(Greek NFC)[:20]>`. Existing `book_...` and `vx...` IDs are not modified. There is one **pre-existing gender homograph** for spouse `ο/η σύζυγος` in the former 828 entries, so 1700 headword records reduce to 1699 base lemmas if Greek noun articles are ignored. This legacy teaching distinction was retained to avoid orphaning any user progress. Level tags are **editorial learner estimates**, not official CEFR-certified 700/1000 quotas (CEFR itself is skill-based).
- Greek source/topic cross-checks for editorial selection, **not bulk imports**: Kelly Greek learner frequency reference (https://github.com/kotoshu/frequency-list-kelly; scholarly sources/usage terms there), Democritus University of Thrace Modern Greek A1/A2 syllabus (https://hellenicstudies.duth.gr/wp-content/uploads/2023/05/MG1-Modern-Greek-language-%CE%99.pdf) and Hellenic American Union sample exam preparation (https://www.hau.gr/el-gr/exams/support/individuals/center-for-the-greek-language/free-preparation-material). Authored source data has its own independent RU/EN wording.
- The Arabic/Chinese/Spanish/Portuguese glosses on **new items** intentionally use the app's already existing **explicitly marked English fallback** when no validated translation exists. English and Russian are complete on all 1,700 entries. This release does *not* claim completion of Arabic or other gloss localisation.
- QA: `qa_vocab_1700.py` asserts 1700 total/700 A1/1000 A2/13 themes, 156 combinations of 13 themes × 2 levels × 6 UI languages yielding exactly ten distinct eight-option quiz cards, independent per-user learned/weak tracking, and SQLite integrity. Old and new DOM end-to-end flows in `qa_dom_test.js` and `qa_new_dom.js` pass. Previous 828 headword ID/content diff was checked against archived `pre-vocab1700` source in a temporary isolated directory.
- Backups immediately preceding release: code `/opt/greek-trainer/backups/pre-vocab1700-20261019T181203Z.tgz`, consistent production DB `/var/lib/greek-trainer/progress.sqlite3.pre-vocab1700-20261019`. Only restart `greek-trainer.service`; no VPN/Matrix infrastructure changes.

---

## 2026-10-19 — Textbook/personalized practice and Greek-only dialogues (current release)

- **Two practice strategies:** textbook-only on selected pages or chapters, or personalized. Personalized drills combine the selected textbook range with only the authenticated user's word records from the independent A1/A2 word course where vocab_progress.correct >= 1 and miss_debt = 0. User-level readiness can change with misses and two successful reviews. Newly introduced/unanswered or currently weak words are never personalized question targets. Vocab course progress remains stored in vocab_progress; drills accrue ordinary attempts/progress, both backed up and unchanged historically. Personalized status endpoint is `/api/personalized/status`, auth-required. Greek verbs remain a separate exercise scope in textbook mode.
- **English double glosses** shown only when an exercise translates Greek to another language (translation answer buttons, feedback on wrong answer), or translates another language into Greek (source prompt). For any non-English UI language, target/source displays `native translation (English gloss)`. User-facing buttons submit the unchanged raw answer, so assessment/stats are not polluted by display helpers. English UI shows no redundant hints. Normal navigation, explanation, account details, native Greek choices, plurals, tonos, conjugation-stage options and Greek-only dialogue distractors do NOT receive English glosses. Vocabulary-course ten-word *preview* remains uncluttered; its quiz cards apply the rule.
- **20 original Greek-only contextual dialogues** added as cards under chapters 1-16 with approximately located pages. Each contains two inline blanks and an eight-choice bank with two correct Greek replies and six distractors. Every gap is graded independently, progress stored using `dlgXXX:gap0` and `dlgXXX:gap1` language-independent card keys. Weak reviews only quiz the still-weak gap and prefill the other one. Localized learner instruction appears above the otherwise Greek-only dialogue. Dedicated checkbox `Диалоги` in normal and personalized textbook drill setup; it is enabled by default.
- All six previously supported locales RU/EN/ZH/AR/ES/PT have explicit localized mode/dialogue instructions. Page/chapter selection, 8-answer UX, staged verbs, user registration, original textbook card corpus and standalone A1/A2 vocabulary remain operational.
- Source files: `dialogues.py`, `personalized.py`, `server.py`, `catalog_v2.py`, `app.js`, `vocab.js`, `vocab_lessons.py`, `verb_phrase.py`, `index.html`, `styles.css`.
- Isolated Python suite `qa_new_features.py` covers account isolation, unlocking/locking learned words, dialogue gap validation/weak reviews, all locale metadata, previous stats. Isolated DOM/HTTP browser-flow suite `qa_new_dom.js` exercises bilingual prompts/buttons, both strategies, studied course words and 2-gap Greek dialogue. Legacy auth/vocab/verb DOM tests retained in `qa_dom_test.js`.
- Before release, code archive: `/opt/greek-trainer/backups/pre-personal-dialog-20261019T174936Z.tgz`; consistent DB backup `/var/lib/greek-trainer/progress.sqlite3.pre-personal-dialog-20261019`. New features add **no schema migrations** to prior SQLite. Never change VPN/Matrix/Gateway dataplane for this app.


---

## 2026-10-19 — Arabic, isolated A1/A2 ten-word lessons, two-stage verb exercises

**Current deployed state** (this section supersedes earlier release notes about Somali and old A1/A2 topic modes):
- Production: https://potapovfamily.com/greek/ ; only `greek-trainer.service` was changed.
- User-selectable UI languages **RU/EN/ZH/AR/ES/PT**. Somali is removed from language switch, all public language metadata and quiz language acceptance. Legacy Somali translation JSON remains as an inert archival resource for old progress; do not drop user stats or progress keys.
- First-screen registration/login modal contains a synced locale select. Auth HMAC pepper, registered users, codes, leaderboard opt-in and existing history unchanged.
- Independent **A1/A2 vocabulary** is its own main navigation tab, never mixed into chapter/page questions. `vocab_lessons.py` + `vocab_more.tsv` compile **828 unique lexical entries** across 13 themes: **451 editorial A1 and 377 editorial A2**. Entries are original / independently authored and book-aligned exercises, with approximate CEFR classification; 828 includes several multiword lexical units, not 828 certified dictionary lemmas. Official CEFR has **no fixed A1/A2 word counts**. Do not claim target 700 A1 + 1000 A2 is complete.
- Vocabulary flow: select a theme (or all) and level; preview exactly ten not-yet-answered entries with translations; then alternate Greek→translation and translation→Greek 8-choice cards. Persist incomplete batches in SQLite, next batch only once all ten have an answer; individual answers update `vocab_progress`. Mistakes accrue `miss_debt` and review via dedicated `review=1` flow, with two correct reviews clearing a first miss. This is separate from old stats/progress. `/api/vocab/meta`, `/api/vocab/lesson`, `/api/vocab/answer`.
- Verb mode remains an explicitly selected non-book scope. For each personal pronoun `εγώ / εσύ / αυτός-αυτή / εμείς / εσείς / αυτοί-αυτές`, stage 1 chooses the conjugated verb (Α, Β1, Β2) and displays the six-person table. Stage 2 **must** translate a full contextual Greek sentence; both answers are independently checked and tracked in SQLite under distinct direction keys.
- Arabic UI labels mostly translated manually. Arabic contextual translations of 102 verb/person sentences stored in `verb_phrases_ar.json` (machine-assisted, some imperfect), plus offline Arabic lexical glosses in `translations_ar.json`. Arabic word translations are **partial** (approximately 390 of 828 unique entries as deployed; calculate dynamically after updates); missing target-language translations are labelled **EN** and displayed as English, never silently masquerading as Arabic. Other languages use verified historical translations for existing cards, with marked EN fallback for new entries. No online translation requests are made by user browsers.
- Source notes: Council of Europe CEFR descriptors (https://www.coe.int/en/web/common-european-framework-reference-languages/introduction-and-context); CEFR vocabulary range (https://rm.coe.int/cefr-companion-volume-%20with-new-descriptors-2018/1680787989); public themed Modern Greek syllabi (https://helleniccentre.org/wp-content/uploads/2017/02/SYLLABUS.pdf). These informed category choice, not bulk copied word data.
- Isolated SQLite API tests passed: auth register, Arabic 10-word batch, answer persistence, next batch, wrong-answer review, 2-stage verbs, normal textbook questions, all public assets. Both JS files syntax-checked in offline Node 24 container; not a full end-to-end visual mobile test.
- Consistent backup before service update: `/var/lib/greek-trainer/progress.sqlite3.pre-arabic-lessons-consistent-20261019`, code backup `/opt/greek-trainer/backups/pre-arabic-lessons-20261019T170739Z.tgz`. Additive new SQLite tables only. Production docs/assets are served with no-store; versioned JS/CSS links updated.
- Important deployment detail: tool-created files default to 0660; `greek-trainer.service` user cannot read these. Ensure new Python/TSV/JSON/JS files are **0644** and do not log secrets before restart.

---

# Λέξη — Greek practice (accounts + A1/A2 topics + Greek verb paradigms)

Public URL: https://potapovfamily.com/greek/

## Course
Ελληνικά Α΄ by Patakis (ISBN 9789601628158), 312 pages.
16 teaching chapters, alphabet, reviews and appendix in the selectable contents.

This website contains INDEPENDENT ORIGINAL practice exercises organized by the 
published textbook chapter topics. It DOES NOT contain the full book's lexical
content. Page tags on individual cards are approximate; chapter boundaries are
from the published TOC. A licensed full copy is needed to map vocabulary to
exact page numbers. Do not present approximate card tags as verified book pages.

## Features
- Select 1–312 page range or one/many chapters.
- Checkboxes for words, numbers, alphabet, phrases, noun plurals, sentences, and Greek tonos placement.
- Greek <-> Russian / English / Simplified Chinese / Somali / Spanish / European Portuguese, bidirectional for translation drills.
- Accent drill: show a single Greek word without tonos, tap the letter carrying the tonos (position-sensitive); reveal correct accented spelling after the answer. 549 derived cards, including είναι -> ειναι (stress on first ι); skips unaccented/multi-accent entries.
- Accent progress is shared between RU and EN UI, since Greek accent placement does not depend on translation language.
- Russian, English, Simplified Chinese (Mandarin), standard Somali, Spanish and European Portuguese UI and Greek translations, selected using the same language switch.
- Offline static Chinese/Somali teaching translations in translations_zh_so.json, covering 628 distinct English glosses used across 1,340 translation/accent cards. Plural drills compare Greek word forms and require no translated gloss. No live external translation calls or secrets on the site.
- Somali language content is machine-produced and **experimental / not native-speaker-reviewed**; Chinese translations are also machine-assisted and may contain ambiguous glosses. UI discloses the quality limitation whenever Chinese or Somali is selected. Do not describe those translations as vetted.
- Chinese/Somali progress debt keys use :zh and :so; preexisting RU/EN keys remain unchanged. Accent progress is language-independent.
- Timed 10, 15, 20, 30, 45 or 60-minute sessions; fetch fresh card batches
  while time remains. Single or resolved weak-card pools may end early.
- Eight unique multiple-choice options for translations; clickable letter buttons for accents. Keys 1–9 where applicable, Enter to continue.
- Weak repeat queue with two required correct repeats, independent per direction
  and per translation language.
- Preferences are stored in the browser; answers/stats and leaderboard membership are stored in server SQLite per registered account, restorable on other devices by its eight-digit access code.

## Infrastructure
Only Core VPS, /opt/greek-trainer, systemd greek-trainer.service enabled.
Python 3 standard library, bound localhost 127.0.0.1:18560.
Public HTTPS served through existing Gateway -> Core mTLS /greek/ route.
No VPN/Matrix services or routes changed.
SQLite at /var/lib/greek-trainer/progress.sqlite3; do not delete on upgrade.

## App files
- data.py: original lessons 1–4 content
- english_legacy.py: English glosses for original cards
- curriculum.py: chapter titles and original teaching corpus for lessons 5–16
- catalog_v2.py: 1,580 cards including 75 supplemental topic words, 102 present-tense conjugation questions, 549 tonos questions; original 1,403 cards preserved.
- server.py: JSON API /api/catalog /api/quiz /api/answer /api/stats and /health
- index.html app.js styles.css: responsive, no build step

## Operations
systemctl status greek-trainer.service
journalctl -u greek-trainer.service -n 80 --no-pager
curl http://127.0.0.1:18560/health
curl https://potapovfamily.com/greek/api/catalog

All added .py files must have 0644 permissions for DynamicUser.
Service reload: systemctl restart greek-trainer.service

## TOC references
https://www.patakis.gr/books/9789601628158-ellinika-a%CE%84-methodos-ekmathisis-tis-ellinikis-os-xenis-glossas-epipeda-a1-a2/
https://books.google.com/books/about/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AC_%CE%91_%CE%9C%CE%AD%CE%B8%CE%BF%CE%B4%CE%BF%CF%82_%CE%B5%CE%BA.html?id=1Ue3EAAAQBAJ


## Chinese translation and smartphone layout QA (2026-10-19)
- Inspected all 628 offline Simplified Chinese English-gloss translations; made 141 concrete corrections (semantic errors, Greek alphabet letters, tense, key/orange/stop/floor/application, pronoun conjugations and over-specific family relationship terms). One identical target remains intentionally: English `work` and `the job` both translate to Chinese 工作.
- Machine translations remain independent original teaching aids, not certified native-speaker-reviewed textbook translations. Somali is still experimental.
- Tested rendered pages and interactions in real headless Chromium with installed Cyrillic/CJK fonts, simulated touch viewports 320, 360, 375, 390, 430, 768 px. Locale groups RU, ZH, SO; test coverage setup, chapters, quiz, next-answer, accent placement, stats, no horizontal overflow and no JavaScript errors.
- Updated mobile navigation for 320 px, readable single-column long translation/phrase/sentence choices, sticky quiz action bar, accent letters in a compact wrapping row, chapter selection and touch targets >= 44px. Confirmed interactions and layout after final asset release (CSS v7, JS v5).
- Public API regression checked RU, EN, ZH, SO x all seven training types, eight distinct translation choices, server health status. Original SQLite and 1,403-card catalog preserved.
- This tests simulated mobile Chromium, not a physical iPhone Safari or Android handset. Device-specific visual issues can still exist.

## Anonymous student nicknames, rolling leaderboard and ES/PT (2026-10-19)
- Each browser receives an anonymous HttpOnly session cookie. A deterministic BLAKE2s digest of the random cookie ID maps to a funny two-word school/study-themed pseudonym plus a four-digit public suffix and school emoji. Nickname stable across restarts and across previously known sessions, without names, emails, or cookie IDs in any public leaderboard response. Display names Russian for RU UI, English otherwise.
- Public GET /api/profile returns the caller's anonymous nickname only. GET /api/leaderboard returns top 40 learners active over the rolling past seven days and the caller's own rank even when outside top 40. Weekly answer count, right/wrong counts, accuracy, current unresolved error cards, and inferred active seconds/minutes. No raw identifiers, card IDs, IP addresses or private answer history in other users' results.
- Time is explicitly ESTIMATED from server-recorded correct/incorrect answer timestamps: 20 seconds for the first answer after a break longer than 120 seconds; subsequent adjacent intervals count actual gap capped at 90 seconds. No idle time is counted; this is not a literal stopwatch, and public ratings are not cheat-proof. Existing answers automatically appear in the recent-week standings without DB resets. Index attempts(created_at,user_id) added; SQLite backup saved before migration.
- Spanish (es) and European Portuguese (pt-PT) translation and entire interface localization added. Offline cache translations_es_pt.json has 628 distinct translated values per language, all non-empty (Greek plural-form drills need no separate translation); some ambiguous glosses manually corrected. Machine-assisted teaching translations may still require native-speaker review. Six languages RU/EN/ZH/SO/ES/PT, each translation-language key has independent mistake progress; Greek tonos progress remains shared across languages.
- Front-end fourth tab for leaderboard plus student-identity strip, responsive mobile leaderboard rows/metrics, loading state, no exposed cookie IDs. UI asset versions JS v9, CSS v8.
- Tests: temporary SQLite verified six languages × seven task types with distinct eight options, bidirectional, nickname uniqueness/stability, rolling-week math, no identifier leak, ES/PT wrong → two correct debt clearing. Gateway HTTPS public tests 6 × 7 combinations, persistent profile, leaderboard, live write-and-correct flow. Headless Chromium with CJK fonts and simulated touch tested 320/360/390/430/768 px × five UI languages (RU/ES/PT/ZH/SO), quiz start/finish and leader row layout with no horizontal overflows, no JavaScript errors, tab touch targets >=44px. Exact mobile devices and Safari not yet checked.
- No VPN/Matrix, Gateway, other system services, or existing progress database erased.

## Leaderboard enrollment correction (2026-10-19)
- Production data audit after a user asked why 62 people showed up when they were the only real user: 63 distinct anonymous user cookies, 107 historical attempts in SQLite, 55 cookie profiles with exactly one answer, 7 profiles with 2–6 answers and 1 profile with 26. These were largely caused by automated browser smoke tests starting a fresh cookie per run, not by real distinct students. The prior count of 62 was misrepresented as real users.
- FIX: leaderboard participation now requires an explicit one-click opt-in in the leaderboard tab. Public leaderboard uses a dedicated SQLite `leaderboard_members` table, populated only by same-origin POST /api/leaderboard/join; POST /api/leaderboard/leave opts out without deleting any personal progress. Existing history can count retroactively after joining. No existing cookie users were auto-enrolled; fresh public member count is 0.
- Current GET /api/leaderboard returns `joined`, `members`, `activeMembers`, top rows and personal rank only for enrolled users; otherwise results are private. Nicknames continue to exist individually outside the leaderboard. Six languages support new opt-in UI. No raw cookie IDs published.
- Also fixed HTTP/1.1 early-denied POST handling: reject with `Connection: close` to avoid leaking unread request bodies into the next reused request (previously causing spurious HTTP 501 after a 403).
- Smoke-tested isolated join/leave retention and public join/leave, CSRF Origin denial, zero real enrolled count after removing only two zero-answer diagnostic enrollments. Preserved all 107 historic attempts and progress records. This system cannot distinguish all historic QA cookie profiles from genuine people automatically; DO NOT interpret distinct session IDs as human counts or blindly delete historical rows.

## Login + vocabulary topic learning + verb inflection release (2026-10-19)
- PUBLIC URL: https://potapovfamily.com/greek/ . New users see a mandatory register/sign-in modal: register a unique nickname (3-28 Unicode letters/numbers/spaces/-/_/.) or sign in with the unique eight-digit numeric access code. Old unregistered same-browser sessions that register retain their attempts/progress (account ID inherits original 128-bit anonymous cookie ID). New device login gets a fresh random session cookie mapped to the original account. Logout invalidates only that session. Login code is highlighted in RED on registration and remains visible in the account bar via browser localStorage on the device used to register or log in. Keep offline copies. Server cannot recover forgotten code.
- SECURITY CAVEAT: eight decimal digits (~26.6 bits) are a WEAK sole credential by modern standards. No server-side plain code or code embedded in logs. Only HMAC-SHA256 over code with separate random 256-bit pepper (mode 0600) stored under /var/lib/greek-trainer/login-pepper, not in DB or code. Unique index prevents code collisions. All API writes require same-Origin HTTPS; login limited to 5 failed guesses/15min/IP plus global 100/15min; registration limited to 4/hour/IP, global 100/hour. Authentication sessions held in SQLite. Client code in localStorage is exposed to same-origin JS and anyone seeing the phone/screenshot; do not show screenshots publicly. Production site contains no external JS/CDN.
- Registration is enforced on quiz, stats, leaderboard, topic study list, and answer endpoints. Public course metadata remains readable; attempts cannot accrue under unauthenticated test cookies. Public leaderboard remains OPT-IN and displays the custom registered nickname rather than synthetic pseudonym.
- Course remains textbook chapters 1-16 and approximate page tags, plus a new independent CEFR A1/A2 topic track (not textbook page-aligned). Twelve themes: shop, road/car, house/kitchen, food, family, work, city, health, time, travel, leisure, nature/weather. New original 75 vocabulary entries + preexisting thematic words tagged by English gloss, each marked A1/A2. Preview selected words and translations before quizzes. Four newer language glosses of the extra words are machine assisted; Somali still needs native review.
- Dedicated present-indicative verb conjugation track: groups A (= Α΄ συζυγία, γράφω), B1 (μιλάω/μιλώ), B2 (μπορώ); 17 independently selected verbs, six person inflections each = 102 inflection cards. Choose A1/A2 proficiency levels and one or several groups. Four-person choice? NO: 8 answer options per Greek verb/person, one or more valid alternatives in group B1 are accepted. Each answer reveals correct form and complete six-person paradigm. On the setup page there are three visible reference paradigms under expandable disclosure.
- Test coverage: isolated SQLite API + HTTP tests for new registration, legacy-history preservation, unique nickname and hashed 8-digit code, cross-device login, logout, 5-fail 429, 6-language topical vocabulary lists and 8-choice quizzes, valid B1 alternatives and full verb paradigms; all pass. Public service health/catalog/topics 200, catalogue count 1,580. Real Chromium mobile page interaction tested 320,360,375,390,430,768 px with six languages (registration dialog, red code, topic selection, vocabulary preview, first quiz, switching to conjugations and answer+table); all no overflow or JS exceptions; tests used mocked auth + isolated backend and did not create production test users.
- SQLite backup before release: search progress.sqlite3.before-accounts-* in StateDirectory. No unrelated VPN/Matrix or Gateway services were changed.
