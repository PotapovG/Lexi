# Adding original course exercises

## Purpose

Learners report recognising the exact prompts after 3–4 days of practicing the first five printed chapters. More exposure to *new communicative situations*, not superficial name swapping, is the goal.

Start with printed units **1–4 and review unit 5** (not the app's old internal 16-unit numbering):
- 1 (pp. 14–23): greetings, `είμαι`, names, numbers 1–10.
- 2 (pp. 24–37): address, residence, phone, `μένω`, `έχω`, `κάνω`.
- 3 (pp. 38–47): family, work, professions, marital status, `ποιος/ποια`.
- 4 (pp. 48–58): languages, nationalities, `μιλάω`, `ξέρω`.
- 5 (pp. 59–65): review combinations strictly limited to 1–4.

This chapter alignment is *curriculum sequencing*, not a claim that our independent exercises appear on a given book page.

## First expansion target (proposed, not current stock)

Aim for **at least 50 genuinely different exercises per chapter** in the early range before the next large release: approximately 20 context phrases, 20 sentences and 10 short scenarios/transformations each. Start with small, reviewable PRs of 15–30 items. Track **distinct semantic meanings**, not simply number of prompt strings. Existing basic words need not be rewritten or duplicated.

Prefer situations such as introducing another person, confirming where someone lives, exchanging a telephone number, describing family/jobs, and asking which languages people speak. Vary person, polarity, word order, gender and formality only when that creates a real exercise and each answer remains unambiguous.

## File format

Create `content/community/<descriptive_batch>.json` containing an array of flat objects, matching `content/community/early_review_001.json`:

```json
{
  "id": "cm02_0021",
  "chapter": 2,
  "page": 28,
  "kind": "sentence",
  "topic": "Город и контакты",
  "gr": "Η Μαρία μένει στην Ελλάδα.",
  "ru": "Мария живёт в Греции.",
  "en": "Maria lives in Greece.",
  "zh": "玛丽亚住在希腊。",
  "ar": "ماريا تسكن في اليونان.",
  "es": "María vive en Grecia.",
  "pt": "A Maria mora na Grécia."
}
```

This is an illustrative authored example, not additional shipped content. IDs are immutable, unique, `cm<printed chapter two digits>_<four digits>`. Never renumber an existing card. `page` is only an approximate chapter-internal learning anchor; never copy a source page or imply exact textbook correspondence.

Supported kinds for this easy contribution lane: `word`, `phrase`, `sentence`. Complex dialogue and audio exercises require a separate reviewed implementation; never fabricate or use device TTS. All six translations must be provided and semantically checked. For words, include articles where appropriate. Word-level accepted variants should use existing conventions, not hidden aliases.

## Gate / expectations

```bash
python3 tests/test_community_content.py
python3 tests/test_content_guard.py
python3 tests/test_selfhost.py
```

CI rejects duplicate Greek surface text against the current catalog, reused IDs, missing locales, invalid chapter/page and obvious premature grammar. Reviewers still need to examine morphology, stress, translations, plausible alternative answers, and accidental copyrighted material. No private reference materials belong in CI or PR comments.

PR summary: chapter and skill coverage; number of additions; 3–5 examples; how linguistic correctness was checked; confirmation of independent authorship and right to submit; unresolved uncertainties. No direct GitHub merge or deployment rights needed for a contributor.
