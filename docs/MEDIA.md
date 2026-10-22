# Pocket TTS media

Two approved pre-rendered Pocket TTS audio libraries are used:

- `pocket-listening/wav/`: two voices per eligible listening item.
- `pocket-pronunciation/wav/`: pre-recorded Greek pronunciation.

Their JSON manifests are in Git. The WAV blobs are deliberately external
to the repository, and the model weights/dependencies are not required for
normal web serving.

## Install from an independent release (preferred)

The media asset is assembled by the
[release workflow](../.github/workflows/publish-media.yml): it fetches all
2821 original approved WAV files and checks each SHA256 before publishing a
compressed bundle as GitHub Release `audio-v1`. The workflow is triggered
when the initial media checksum manifest lands in `main`.

```bash
python3 scripts/install_release_audio.py
python3 scripts/check_audio.py
docker compose restart lexi
```

The release installer verifies the archive digest and every WAV against
`media.sha256` before making files visible to the app.
If the workflow has not completed yet, use the temporary fallback below.

## Fetch and verify from original demo (fallback)

```bash
python3 scripts/fetch_audio.py \
  --source https://potapovfamily.com/greek/ \
  --workers 3
python3 scripts/check_audio.py
docker compose restart lexi
```

The canonical demo is only a temporary migration source: the independent
Release asset is the durable, recommended distribution channel. The script verifies RIFF/WAVE format and mono 24 kHz/16-bit
PCM. It fetches only filenames declared in committed manifests, uses a
temporary file and atomic rename, and skips already-verified files.

For durable distribution, package both folders in a versioned release
asset in GitHub Releases (or another storage provider), with a published
SHA256 checksum. Future deployment should fetch that bundle, then run
`scripts/check_audio.py` before enabling listening. Do not assume
GitHub cloning itself includes audio.

Upstream Greek Pocket TTS by Myned AI is CC BY 4.0 and needs attribution:
https://huggingface.co/myned-ai/pocket-tts-greek
