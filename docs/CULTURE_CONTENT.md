# Cyprus Culture — content contract v1 (CULT-01)

This folder will hold independently authored preparation material for the Cyprus
Culture / civic-knowledge examination. It is **not** an official examination
question bank. Do not copy third-party commercial question banks or private
exam scans. Draft and test fixtures are not published questions.

## Repository layout

- `content/culture/config.json`: 14 study topic buckets and configurable
  *observed* format weights. These are Lexi's editorial categories, **not**
  an assertion of the government's exact category names, scoring allocation,
  or current regulatory requirements.
- `content/culture/facts/*.json`: fact records with a stable `fact_id`
  (stored as the fact's `id`), provenance, status and freshness.
- `content/culture/questions/*.json`: four-option questions that reference
  a `fact_id`, with original Greek, exact RU/EN translations of **question
  and all four alternatives**, localized explanations and vocab links.
- `content/culture/vocabulary/*.json`: independently reviewed EL lemmas,
  RU/EN glosses, examples, source information.
- `content/culture/lessons/*.json`: concise RU/EN teaching notes and
  references to existing question IDs.
- `tests/fixtures/culture/sample_corpus.json`: **synthetic examples only**.
  They are not real Cyprus facts or published learner content.

Each data file inside these four directories is a JSON **array**. Filenames
and batches can change but the authored `id` must remain immutable. New
content should be reviewed in small, focused PRs (typically 15–30 questions).
The entire code and content remain offline-compatible.

## Four question kinds

- `DIRECT`: choose an answer to a direct question.
- `CLOZE`: choose the missing fragment of a sentence.
- `NEGATIVE`: identify **the false statement**. Must declare
  `option_truth: [true, true, true, false]` (order may vary) and the
  `correct_index` must point to the sole false value. Those flags are an
  *author/editor attestation*, not an automated verification of truth.
- `CHRONOLOGY`: choose the correctly ordered sequence, represented by
  four complete candidate sequences as options.

All four use `question_el`, exactly four `options_el`, and a zero-based
`correct_index` in 0…3. The actual UI must display Α/Β/Γ/Δ. Translation
never changes the target answer. In the future exam API, do not serialize
`correct_index`, `option_truth`, fact proofs or localized feedback before
exam completion.

Multiple questions may share `fact_id`; an exam generator **must** ensure
one instance per fact. Avoid trivial paraphrase/answer-position duplicates.

## Common fields and publication gate

Shared base fields for facts, questions, vocabulary and lessons:

| Field | Meaning |
| --- | --- |
| `id` | Immutable lowercase ASCII ID, e.g. `cyq_geo_0123` |
| `topic` | One of the 14 `config.json` topic codes |
| `status` | `draft`, `reviewed`, `published`, `archived` |
| `freshness` | `evergreen`, `periodic` or `current` |
| `verified_at` | Last source verification, ISO `YYYY-MM-DD` |
| `review_due` | Next required recheck for changing information |
| `valid_until` | Last date content remains valid; inclusive |
| `source` | `{kind, title, url}`, public HTTPS |
| `rights` | `independently_authored`, `licensed_with_permission`, or `public_domain` |
| `review` | Required at `reviewed`/`published`, independent editor + checklist |

For `periodic` and `current`, require **both** `review_due` and
`valid_until`; evergreen entries can use `null`. If the review deadline
or validity passes, previously published items fail validation until
reverified or archived and are also excluded by `exam_eligible()`.
Do not rely on this alone to attest the truth of a claim.

Publishing/reviewing requires:

```json
{
  "review": {
    "editor": "reviewer_identifier",
    "at": "2026-11-14",
    "checks": {
      "greek": true, "ru": true, "en": true,
      "facts": true, "rights": true
    }
  }
}
```

The five checks must represent **actual, independently performed** editorial
review, not generated booleans. CI verifies presence but cannot certify
human identity, accurate Greek grammar, a source's factual claims, or IP
rights. Code review must inspect proof links, alternatives, Greek tonos,
negations, nuance of RU/EN, license evidence, and adversarial questions.

An `origin` field on questions distinguishes `original`,
`reconstructed` and `official_published`. The latter requires an
official source **and explicit permission** to reuse the exact published
wording. A government URL does not itself establish public-domain rights.

For stable histories, changes to the right answer or answer options require
a new content version. Do not renumber old IDs, mutate completed exam
snapshots or delete archived source history.

## Source and freshness policy

Preferred verification hierarchy: public Cyprus government pages, official
statistics and primary institutions, followed by reputable journalism.
Participant reports can guide question topics and mark a reconstruction, but
a report alone does not make a fact true.

- `evergreen`: enduring historic/geographic fact, still source-checked.
- `periodic`: named current ministers, fees, office responsibilities,
  working hours, etc.
- `current`: recent news, temporary measures, dated events.

Historical questions about a specific year may remain evergreen once the
wording makes that time frame explicit. Never imply that a historical
government official is still in office.

Citation links should be direct, relevant, accessible and not paywalled.
The validator checks HTTPS and field presence, **not** live URL content.
Rights and factual correctness remain a separate editorial gate.

## Local validation

```bash
python3 culture_content.py
python3 qa_culture_content.py
```

`culture_content.py` has no external dependencies and scans only curated
`*.json` files in four content folders. It does not read private source
PDFs, student accounts, tokens, SQLite state or external web APIs.

Do not fill source fields with placeholders in released content. Synthetic
fixture files deliberately use illustrative domains and `status=draft`;
they must never be moved to the published content folders.

## Scope of CULT-01

This issue supplies schema, checks, examples and docs only; no learner
interface, exam endpoints, persisted personal data, live scraping, mass
question generation, paid API, audio generation or production deployment.
Follow-up: #35 (120 independently reviewed questions), #36 (isolated backend),
#37 (UI), #38 (vocabulary), #39 (25×45 exam), #40 (analytics), #41 (QA),
#42 (full coverage and release readiness).
