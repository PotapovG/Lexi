# Content and audio rights

- The MIT license covers Lexi application software written for this project.
- Greek learning texts, headword lists, translations, and textbook-aligned
  exercises are **not asserted to be MIT-licensed** until their authorship and
  redistribution rights are independently confirmed. Please do not submit
  verbatim publisher-owned textbook passages, screenshots, or purchased PDFs.
- Lexi is not affiliated with or endorsed by any textbook publisher. Unit and
  page references are for interoperability and reference; they are not a grant
  of permission to reproduce textbook content.
- Greek Pocket TTS model by **Myned AI**, based on **Kyutai Pocket TTS**, is
  distributed upstream under CC BY 4.0. See:
  https://huggingface.co/myned-ai/pocket-tts-greek
  Attribution is required if redistributing model assets. Generated speech is
  synthetic; never present it as a recording of a real speaker.
- Generated WAVs are not in the Git repository. The optional audio bootstrap
  fetches the project's own existing pre-rendered outputs, not model weights.
  Rights to redistribute source texts in a media bundle should be confirmed
  before publishing it as a third-party release.

## Specific Greek model attribution

Greek synthetic audio is made with the **Myned AI** fine-tuned
[pocket-tts-greek model](https://huggingface.co/myned-ai/pocket-tts-greek),
based on [Kyutai Pocket TTS](https://huggingface.co/kyutai/pocket-tts).
The model weights are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Its card credits Mozilla Common Voice (CC0) sources for the voice prompts.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for all acknowledgements
and modification details. Model attribution appears in Lexi's visible footer.

## Status of learning-content rights

Our own instructional sentence/dialogue corpus is being screened for
unlicensed overlap with a privately purchased commercial textbook.
[Read the methods and limitations](docs/CONTENT_AUDIT.md).
**Do not assume that the MIT license for software automatically grants a
license to republish the teaching corpus**. A separate explicit data/content
license can be granted after the copyright/authorial provenance review.
