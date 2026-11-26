# Lexi UI policy — guided learning experience (updated 2026-11-26)

## Default experience: guided lessons

- The default home is an eight-lesson list for each studied textbook chapter.
- Each lesson is a persistent sequence drawn from existing eligible material. Targets are usually 10–14 graded responses, but a short lesson is valid when the chapter lacks suitable material. Show the actual response count and distinguish it from logical cards (a dialogue can have several responses). Time is an estimate. Never fill a lesson with future grammar or meaningless duplicates to meet a number. The next lesson remains server-locked and its title/content is not disclosed until the previous lesson completes.
- Eight completed lessons close a chapter round; the student sees answers, errors, accuracy, active minutes and wall-clock elapsed time, plus their learning backlog. A completed-round acknowledgment unlocks the next round.
- **First submitted answer is final** for each lesson question, correct or incorrect. In the guided course, vocabulary and choice-card practice, choosing an option is an editable draft; the explicit Check action submits it. Existing typed/order tasks use the same boundary. After submission, show explanation/correct form and lock the answer until Next (or Finish lesson). Retyping/choosing a revealed answer must never upgrade the grade. Classic retains its established submission semantics.
- Keep feedback visible until the learner continues. A lost response enters recovery, preserving the exact operation and input; do not silently submit a new answer or restart the lesson. Distinguish pending, unknown outcome, revision conflict, unverified, paused and completed states.
- Home prioritizes the current lesson and a single Continue/Start action. The lesson screen reduces navigation; the completion screen reports that lesson's scope and the next available step. Detailed chapter/material settings remain available without competing with the main action.
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

- Lessons and the existing vocabulary catalog are primary navigation destinations. More exposes the existing practice/review/progress surfaces, including Classic, Anki, Greek Life and the owner-approved Cyprus Culture section. This navigation does not create a new learner mode.
- Preserve light/dark themes, visible focus, reduced motion, 320px layouts and the six real interface locales. Greek content is explicitly Greek/LTR inside Arabic RTL; a saved lesson's source/translation language is identified when it differs from the interface.
- Loading, signed-out and temporary network/server failure are different states. Authentication owns focus while required; a failed profile fetch is not proof of logout.
- Display Board backlog, Classic mistakes, SRS, vocabulary and Life with explicit scopes. Do not add unlike counts into a fictional global mastery score.
- Greek playback uses verified pre-generated Pocket WAV only; no browser TTS. The narrowly authorized optional AI completion panel (#54–65, 2026-11-26) may record learner audio for reading/dialogue practice. It defaults off, requires explicit sending, stops microphone/playback on exit, and cannot affect first-attempt grades or ordinary SRS. ASR text is not a pronunciation assessment. See docs/AI.md.
- Chapters are 1–20 per the printed textbook; A1 supplemental vocabulary is editorial enrichment, not a precise publisher quotation.
