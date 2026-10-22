# Copyright / curriculum originality audit — 2026-10-22

## Scope and private reference

- Reference: the maintainer's purchased *Ελληνικά Α΄* PDF (314 PDF pages),
  SHA256 `49e83dde91dcef9568c9a5e733a3c5034b8f650d2d7ed943db463eb3fe12f282`.
- Checked Greek text spans in Lexi, including full original practice cards,
  sentence/order/dialogue content, dialogue turns and answers, and grammar
  prompts and Greek response options, plus independent A1/A2 vocabulary.
- **1110 multiword text-field occurrences** (including intentional repetitions
  across fields) compared with a normalized private PDF text-layer extraction.
  Normalization removes Greek accents, case and punctuation, and looks for
  contiguous strings of five or more words.
- Results before remediation: one unique five-word contiguous overlap
  (the first question in `dlg064`, about a flat's floor); none at seven, nine,
  or twelve consecutive words in the extracted text. That question has been
  **rewritten** to ask where a new apartment is located while keeping chapter
  11 and the answer structure intact.
- Similarity assessment here covers **machine-readable Greek wording**, not
  pictures or exercise designs, and does not prove rights in every entry.
  Short greetings, inflected forms, named places, number words and individual
  vocabulary headwords are functional language facts; matches of those
  alone are not evidence that a publisher exercise was copied.
- Historical in-repo source-page metadata verifies topic alignment, not
  originality or legal clearance. The app makes independently authored
  exercises *following* the curriculum; it must never pretend to reproduce
  printed exercises or complete copyrighted source pages.

## Reproducible local review with the purchased PDF

Keep the purchased PDF private and **never** upload it to GitHub, CI, release
assets or staging servers.

```bash
# Requires poppler-utils (pdftotext) locally; NOT part of app runtime.
python3 scripts/audit_textbook_overlap.py --pdf ~/private/purchased-book.pdf
# or use an already extracted local .txt reference:
python3 scripts/audit_textbook_overlap.py --reference-text ~/private/book.txt
```

The CLI outputs only Lexi card IDs, approximate PDF page indices and match
lengths, never copyrighted excerpts. Five-word candidates require manual
review; seven or more consecutive words trigger a nonzero default exit code.
Use `--strict` for nonzero exit on *any* five-word candidate. For re-review
look at the actual private textbook on your own machine, not screenshots in PR.

## Editorial policy

1. **Allowed:** independent everyday Greek vocabulary, grammatical facts,
   communicative goals, CEFR-style topic sequencing, approximate curriculum
   chapters and **newly composed** sentences/dialogues/stories.
2. **Not allowed:** publisher's dialogues, example sentences, exercise wording,
   comprehension stories, passage translations, exercise answer keys or
   recreated/closely paraphrased structured drills from the purchased book.
3. Longer phrase similarities: rewrite the *full communicative situation*,
   names, setting and syntax, not merely replace one or two words.
4. Learning exercises must keep stable IDs where possible to preserve student
   learning records. Update related sentence-order material if derived.
5. A contributor should document authored provenance and affirm that their
   submitted text is original and licensed for inclusion; independent QA must
   review suspicious matches.
6. Additional visual/manual review remains necessary: automatic text checks
   cannot rule out copying in scanned portions of the PDF, paraphrased
   content, illustrations or non-Greek translations.

## Limitations

This is **a reproducible similarity screen, not a definitive copyright
clearance or legal opinion**. No publisher exercise is assumed to be licensed
just because its chapter, lemma or topic was verified. The educational corpus
is pending final human attribution and licensing review. Software MIT rights
do not confer permission to reproduce third-party teaching content.
