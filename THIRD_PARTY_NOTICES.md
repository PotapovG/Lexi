# Third-party acknowledgements and license notices

## Greek speech synthesis — Myned AI Pocket TTS Greek

Lexi uses pre-rendered synthetic Greek speech produced using:

- **Model:** [Myned AI — pocket-tts-greek](https://huggingface.co/myned-ai/pocket-tts-greek)
- **Original model/architecture:** [Kyutai — Pocket TTS](https://huggingface.co/kyutai/pocket-tts)
- **Model weights license:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Greek voices:** the model card describes the bundled voice prompts as excerpts from [Mozilla Common Voice](https://commonvoice.mozilla.org/) recordings (CC0).
- **How used:** Lexi generated Greek WAV recordings offline for educational listening and pronunciation. The text and voice selection are Lexi's, not an endorsement by the model authors. The resulting WAV is synthetic speech, not an authentic human recording.
- **Changes and transformations:** Greek model weights are used for inference, not modified or redistributed as part of Lexi's application source. Audio is generated, cut and packaged into hash-addressed WAV files and manifests; no original speaker recording is presented as genuine speech.
- **Redistribution:** Git source contains manifests/scripts, not upstream model weights or reference voice samples. A separately distributed WAV bundle may require its own license and source-content review.

The underlying Kyutai implementation uses a separate software license, as documented at [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts); do not confuse that code license with the **CC BY 4.0 model weights**.

Attribution should be retained in third-party notices and the application's footer by forks that reuse these recordings or generate new ones with the same model.

## Commercial textbook reference

*Ελληνικά Α΄ · Μέθοδος εκμάθησης της ελληνικής ως ξένης γλώσσας*, Patakis, ISBN 9789601628158, is a separately copyrighted commercial work.

Lexi may refer to its educational subject progression, grammatical topics and approximate printed chapter/page structure for compatibility. No textbook PDF, photographs, scans, publisher-owned exercises or dialogues are provided under the Lexi source license. Curriculum ordering is not a grant of permission to reproduce the publisher's original expression.

See [docs/CONTENT_AUDIT.md](docs/CONTENT_AUDIT.md) for the overlap methodology and audit limits.
