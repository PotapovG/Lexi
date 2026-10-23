# Contributing to Lexi

Thanks for helping improve accessible Greek practice.

1. Fork this repository and open a focused pull request against `main`.
2. Include a short description, screenshots for UI changes, and tests for new
   learning rules; preserve existing stable card IDs and progress compatibility.
3. Run `python3 tests/test_selfhost.py` and any relevant `qa_*.py` tests.
   Some old QA checks require the full recorded audio library; note skips.
4. Add Greek accents carefully (tonos, final nu, enclitic stress), preserve
   the six supported locales (ru, en, zh, ar, es, pt), and give accepted
   spelling variants fair treatment.
5. No microphone or speech-recognition feature. Keep sound Pocket TTS
   pre-rendered only, with no device TTS fallback or paid API dependency.
6. Do not upload a purchased textbook, copied publisher exercises, user
   database, student names, access codes, generated model weights or huge WAV
   files. See CONTENT_RIGHTS.md.
7. For security reports involving authentication, credentials or private
   learner data, contact the maintainer privately; do not publish exploits
   or leaked data in an issue.
8. For large architectural changes, open an issue first. Do not commit
   direct changes to another person's production instance.

## Design

Backend: Python standard library HTTP server + SQLite.
Frontend: vanilla HTML/CSS/JavaScript.
Learning catalogs: root `*.py`, `*.tsv` and `*.json` files.
Persistent state: configured via `GREEK_DB` and `GREEK_PEPPER`.
Optional Pocket recordings: `pocket-*/wav/` (not tracked).
Public deployment must use HTTPS and a restricted upstream listener.

PR review emphasizes learner correctness, accessibility, privacy, security,
migration safety and zero production dependency for self-hosting.

## Authorship affirmation for teaching-content PRs

Every contribution adding educational text must state in the PR that:
- its Greek sentences/dialogues/exercises were written independently,
  **not copied or minimally paraphrased** from any commercial textbook;
- examples follow topic/grammar objectives only (not publisher exercises);
- the contributor has authority to license their original submitted work
  under the repository's applicable content terms when those are specified;
- no uploaded/private textbook PDF, images, or answer sheets are included.

Where the reviewer owns the commercial reference personally, they can run
`scripts/audit_textbook_overlap.py` locally. No commercial book goes into CI.
See `docs/CONTENT_AUDIT.md`.

## AI-assisted lesson batches

For content-only additions, follow [AGENTS.md](AGENTS.md) and
[the independent authoring guide](docs/CONTENT_AUTHORING.md). Add new records
to `content/community/*.json` rather than editing legacy indexed question arrays.
Keep PRs small and show per-chapter counts. Automatic checks catch structure,
not subtle translation errors or third-party copyrights. Production deployment
and merge rights remain with the maintainer.
