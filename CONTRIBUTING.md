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
