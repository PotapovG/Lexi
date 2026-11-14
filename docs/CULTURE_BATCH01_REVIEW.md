# Cyprus Culture — CULT-02 batch 01 editorial handoff

**Authored on:** 2026-11-14  
**Issue:** #35  
**Scope:** 20 original **draft** questions and 20 independently keyed factual statements across all 14 Lexi Culture topic buckets. **This is not a published or endorsed exam question set.**

## What was checked

- Core facts researched against Cyprus government, Cyprus Statistical Service, European Union/Council presidency, Visit Cyprus and Cyta primary/institutional sites.
- Complete Greek question, 4 choices, one intended answer, RU/EN translation of the prompt + all choices, RU/EN short explanations, per-record primary source, `verified_at`, `freshness`, `rights=independently_authored`.
- Two NEGATIVE questions include author-declared `option_truth` vectors; one CHRONOLOGY question has four orderings. Their semantic validity **must still be independently reviewed**.
- `NEWS` (EU presidency in 2026) and `ECON` (2025 tourism statistical result) are date-scoped with `review_due=2026-12-15` and `valid_until=2027-06-30`.

## Coverage

| Topic | Draft questions |
| --- | ---: |
| GEO | 2 |
| GOV | 2 |
| HIS | 3 |
| NEWS | 2 |
| TRAD | 2 |
| ECON | 1 |
| HEALTH | 1 |
| HOLIDAYS | 1 |
| TRANSPORT | 1 |
| LANG | 1 |
| ENTRY | 1 |
| TELECOM | 1 |
| CLIMATE | 1 |
| CURRENCY | 1 |
| **Total** | **20** |

**Formats:** DIRECT=10, CLOZE=5, NEGATIVE=2, CHRONOLOGY=1, plus remaining DIRECT counting to 20: automated CI report is authoritative for exact distribution. This draft batch does not claim to match official exam weighting.

## Items needing particular editorial attention

1. `cyq_his_0001` vs `cyq_holidays_0001`: formal independence on 16 August 1960 versus Independence Day on 1 October — distinct facts, don't merge or confuse.
2. `cyq_gov_0001`: the three true and one false options require careful review of Cyprus's presidential constitutional system.
3. `cyq_lang_0001`: two official **Republic of Cyprus** languages versus Greek's status as an **EU** official language; wording must be accurate.
4. `cyq_news_0001` and `cyq_news_0002`: EU **Council** presidency, not Commission/Parliament presidency; year-scoped as 2026/2012.
5. `cyq_currency_0001`: chronology of 2004 EU accession, 2008 euro, 2026 second Council presidency; three primary facts are documented together by Cyprus Presidency of Council.
6. `cyq_entry_0001`: European **Union** citizens using photo ID, not a generic tourist passport-waiver claim; beware future regulation changes.
7. `cyq_econ_0001`: 2025 tourism shares are historical statistics, not an assertion about current 2026 country shares.
8. `cyq_telecom_0001`: distinguish CITA's creation from its 1961 rename to CYTA.
9. Validate native Greek grammar, punctuation, grammatical agreement, proper names/transliteration, negative polarity, sensible distractors and correctness/nuance of both RU/EN translations.

## Publication gate — not yet passed

All records are deliberately `status=draft` with **no manufactured `review` metadata**. Do not bulk-flip these to `reviewed`/`published` on the basis of automated tests, AI-generated explanation or source presence. A person reviewing Greek, RU, EN, facts and redistribution rights must record true completed checks according to `docs/CULTURE_CONTENT.md`. Only published records become learner-visible via `culture_adapter.load`.

## Follow-up

- Independent editorial review of these 20 + correction PR, with evidence by question/fact ID.
- Additional batches of 15–30 original source-backed questions, targeting greater depth in GEO/GOV/NEWS and coverage of commonly seen 2026 question formats.
- Initial goal #35: **120 reviewed/published questions**; this batch contributes **20 authored drafts / 0 published** until reviewed.
- No additional runtime, schema or production change is intended by this content PR.
