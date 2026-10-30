# Lexi UI policy — eight-lesson course (2026-10-30)

## Default experience: guided lessons

- The default home is an eight-lesson list for each studied textbook chapter.
- Each lesson consists of a persistent sequence of 10–14 tasks (normally ~5–10 minutes), not a single quiz question. The next lesson remains server-locked and its title/content is not disclosed until the previous lesson completes.
- Eight completed lessons close a chapter round; the student sees answers, errors, accuracy, active minutes and wall-clock elapsed time, plus their learning backlog. A completed-round acknowledgment unlocks the next round.
- **First submitted answer is final** for each lesson question, correct or incorrect. The UI immediately shows explanation and correct form, disables all answer inputs, and permits only Next (or Finish lesson on the last question). Retyping/choosing the revealed answer must never upgrade the grade.
- Weaknesses from incorrect answers are recorded in account-owned storage and up to two are recalled in future lessons. A wrong answer still advances the lesson but never counts as correct; mastery is demonstrated only at a future scheduled review. Unverified free-text wording moves ahead without a false error penalty.
- Server verifies answers and account ownership, protects revisions against replay and preserves lesson checkpoints across devices and sessions.
- Optional start-at-selected-chapter skips earlier lessons without falsely granting mastery.
- V1 single-question board progress is archived verbatim on migration; it does not become credit for multi-question lessons. Legacy answer history stays intact.

## Classic interface: deprecated but fully functional

- The prior Classic interface, including filters, duration, timer, weak mode and SRS, remains available with a visible Deprecated label and an easy return to the new course.
- Existing Classic quiz endpoints, session state, user progress, card IDs and scoring remain functional. Shared security or correctness fixes still apply.
- New course-specific features, future lesson types, stats and game mechanics are not backported into Classic. Explain their unavailability there instead of adding inert controls.
- Keep independent API, regression, mobile and classic timed quiz tests in the release gate.

## Other modes / data

- Anki, Greek Life, topical vocabulary and leaderboard remain accessible under More without affecting the main lesson flow.
- Audio is verified pre-generated Pocket Greek WAV only; no browser TTS.
- Chapters are 1–20 per the printed textbook; A1 supplemental vocabulary is editorial enrichment, not a precise publisher quotation.
