# Lexi UI policy — board launch 2026-10-30

## Primary: game board
- Game board is the default home for new and returning students.
- One primary move, plus a single chapter limit (1–20). Eight quest families per chapter: textbook, A1 lexicon, verbs, grammar, listening, dialogues, clocks, real-life scenarios.
- Server enforces syllabus stage gates, scores with reviewed existing logic, and saves per-account board progress in SQLite independently of legacy quiz sessions.
- Incorrect answers never advance a move. An unverified free-text answer may be skipped without an invented grammar penalty.
- The optional start-at-selected-chapter route skips prior nodes without granting false mastery.

## Classic interface: DEPRECATED but functional
- The original practice-view, page/chapter selections, task filters, session duration, adaptive mode, SRS, timer and answer history remain working.
- Classic is always reachable through the visible navigation toggle and clearly labelled Deprecated, with an easy return to board.
- Do not introduce board-only quest types, story mechanics, new game modes, or XP controls into Classic. Label such capabilities unavailable in Classic and link to the board rather than adding inert controls.
- Shared security changes, data protection, grading correctness and bug fixes must still be applied in both clients.
- Do not change original card IDs or delete user accounts, progress, weak/SRS history, or ongoing legacy sessions.
- Maintain independent automated integration tests for both interfaces.

## Learning content and audio
- The textbook contains 20 chapters. Do not advertise nonexistent chapters.
- A1 supplementary vocabulary is editorial enrichment, not a claim about publisher pages.
- Pre-generated validated Pocket TTS WAV only. No browser speech synthesis, runtime TTS, or unsupported audio.
- Anki, Greek Life, themed vocabulary, review and stats remain accessible as specialist study areas while the game board provides the default guided sequence.
