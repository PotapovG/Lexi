# Lexi — agent instructions

These are **instructions to AI coding assistants and human contributors**, not an invitation to deploy autonomously.

## Work boundaries
- One branch/PR per coherent batch. Never push directly to `main`, rewrite history or access production. A coding assistant may merge only when the repository owner explicitly delegates that authority; the owner delegated merging of passing Lexi PRs on 2026-11-10. Respect required checks and branch protection.
- **Owner's permanent rule (2026-11-10): NO NEW LEARNER MODES.** Expand only existing exercise kinds, vocabulary, grammatical explanations, dialogue cards and exercises inside current UI modes. Never create an extra mode/tab/course/parallel trainer; reuse existing SRS, weak review, lesson filtering and progress.
- **Owner-approved narrow exception (2026-11-14, [CULT epic #33](https://github.com/PotapovG/Lexi/issues/33)):** build exactly one learner-facing **Cyprus Culture** section with internal study/vocabulary/mistake/mock-exam views. Use separate namespace for citizenship-exam questions and progress, while reusing existing auth/UI/SRS infrastructure. This exception does **not** authorize any other new modes or changes to A1/A2 learning stages. Scope and acceptance are tracked in #34–#42; no production deployment is authorized by this exception.
- For course expansion, edit **only** `content/community/*.json` unless the maintainer specifically requests backend changes.
- Existing dialogue exercises may be extended with independently authored material in `content/conversations/*.json` through the current dialogue-kind loader. That does NOT authorize adding a new learner mode or changing historic IDs.
- Read `CONTRIBUTING.md`, `docs/CONTENT_AUTHORING.md` and `CONTENT_RIGHTS.md` first.
- Never read, upload or reproduce a purchased Patakis PDF or its exercises, dialogues, translated passages, images, answer keys or screenshots. Follow only the independently described chapter learning goals.
- Do not include student records, names, access codes, database/pepper, secrets, model weights or generated WAVs.
- Original Greek text and independent translations only. Do not assert that MIT grants rights to lesson content. Contributor affirms rights in every PR.
- Keep Greek tonos, final ν, natural modern Greek, and register (formal/informal) correct; account for accepted spelling variants.
- Supported locales are `ru en zh ar es pt`. Never substitute English text as the translation for another locale. Require reviewed translations rather than guesses.
- Never introduce future grammar early. Printed chapters 1–4 cover introductions, addresses, family/jobs and languages; printed chapter 5 reviews chapters 1–4. **No** future tense, aorist, subjunctive `να` or plural-noun drills in these chapters.
- New cards get `cmNN_NNNN` IDs. IDs and answer text of existing cards must not be changed. A phrase with just a different proper name is not enough new pedagogical value.
- Do not add microphone recognition, device TTS, paid model APIs, ads or a production dependency.

## Validate before PR
```bash
python3 tests/test_community_content.py
python3 tests/test_content_guard.py
python3 tests/test_selfhost.py
```
The PR must include per-chapter/card-type counts, coverage goals, grammar limitations, content originality affirmation, and anything not reviewed. Tests are structural checks, **not linguistic or copyright certification**.
