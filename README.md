# Λέξη / Lexi

Self-hostable Modern Greek vocabulary, grammar, pronunciation and listening
trainer with A1/A2 practice, six UI languages and local SQLite progress.

**Demo:** https://potapovfamily.com/greek/

## Run locally with Docker

Prerequisites: Docker Engine + Docker Compose v2.

```bash
git clone https://github.com/PotapovG/Lexi.git
cd Lexi
docker compose up -d --build
```

Open **http://localhost:18560/greek/**.

The database and login secret live in the persistent Docker volume `lexi_data`.
The Python app needs no third-party Python packages for ordinary lessons.
The reverse proxy is not required for loopback experimentation, but **HTTPS is
mandatory for a public installation** (session cookies are Secure and login
codes are only eight digits). Never expose port 18560 publicly as plain HTTP.

### Run without Docker

```bash
export GREEK_DB="$(pwd)/local-data/progress.sqlite3"
export GREEK_PEPPER="$(pwd)/local-data/login-pepper"
export GREEK_ORIGIN="http://localhost:18560"
mkdir -p local-data
python3 server.py
```

Open http://localhost:18560/greek/. For any public deployment, run behind
HTTPS, with private writable DB directory and `GREEK_ORIGIN` matching the
exact browser origin.

### Optional Pocket TTS recordings

Source installs do **not** contain ~200 MB of pre-rendered audio.
Greek playback uses pre-rendered Pocket TTS WAV; device speech and paid TTS
fallback are disabled. Optional learner microphone input is a separate,
default-off AI feature and does not replace Pocket playback.

Without audio, **text exercises work** and the separate listening mode is
disabled automatically. Use the [versioned audio release](https://github.com/PotapovG/Lexi/releases/tag/audio-v1)
once published:

```bash
python3 scripts/install_release_audio.py
docker compose restart lexi
```

Before the release is available, the following bootstrap can copy the
already approved offline WAVs from the canonical demo (dependent on
that service being available):

```bash
python3 scripts/fetch_audio.py --source https://potapovfamily.com/greek/
python3 scripts/check_audio.py
docker compose restart lexi
```

All media files are verified against the immutable SHA256 manifest shipped
with the Git repository. See [media distribution](docs/MEDIA.md).
Do not commit WAVs or model weights into ordinary Git history.

### Learning journey and optional AI

The existing lesson board is the main learning path: continue a saved lesson,
choose an answer, check it, read the feedback and then continue. Practice,
mistake review, the vocabulary catalog, Classic and Cyprus Culture remain
available from the existing navigation. Scoped progress labels separate these
learning areas. See [the actual chapter/lesson matrix](docs/LEARNING_PATH.md).

Optional AI can summarize a completed lesson using retained first-answer
evidence, compare a reading with an independently recognized transcript, and
run a short voice-answer/text-response dialogue. It is **disabled by default**.
The free ordinary course does not require an API key. ASR comparisons do not
measure pronunciation; edited transcripts are explicitly identified.

Read [configuration, privacy, limits and pilot gates](docs/AI.md) before enabling
any feature. Real Greek speech quality, mobile microphone behavior and live
provider cost remain release gates; automated fake-provider tests do not
certify them.

### Public HTTPS

Point your DNS at a host with Caddy (or another TLS proxy). See
[Caddyfile.example](Caddyfile.example); change its hostname and run your
proxy on the same machine. Set `LEXI_ORIGIN=https://your-host` in `.env`,
then `docker compose up -d --build`. Keep the app published only on
`127.0.0.1:18560`. Public browser URL is `https://your-host/greek/`.

### Contributing

Community-authored cards belong in `content/community/*.json` and are checked
by `tests/test_community_content.py`. See [the AI contributor instructions](AGENTS.md)
and [authoring guide](docs/CONTENT_AUTHORING.md). Core runs the [guarded GitOps puller](docs/GITOPS.md):
merges become production releases only after `main` branch protection and green CI are verified.


Read [CONTRIBUTING.md](CONTRIBUTING.md), [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md)
and the [deployment guide](docs/DEPLOYMENT.md). Run isolated smoke tests:

```bash
python3 tests/test_selfhost.py
```

The original development notes remain in
[docs/DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md).

## Configuration

| Variable | Default in Docker | Purpose |
|---|---|---|
| `GREEK_HOST` | `0.0.0.0` | Bind address inside container |
| `GREEK_PORT` | `18560` | HTTP listener |
| `GREEK_ORIGIN` | from `LEXI_ORIGIN` | Exact allowed POST Origin |
| `GREEK_DB` | `/data/progress.sqlite3` | SQLite progress and accounts |
| `GREEK_PEPPER` | `/data/login-pepper` | Generated local secret file |
| `GREEK_LISTENING` | `auto` | `auto`, `off`, or `on` (fails if audio incomplete) |

**Privacy:** never commit your SQLite database, login pepper, user
data, access tokens, or runtime files.

**Licensing:** MIT for original application software. This does not license
publisher materials or automatically authorize reuse of all educational data.
See [CONTENT_RIGHTS.md](CONTENT_RIGHTS.md),
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[our content originality audit](docs/CONTENT_AUDIT.md).
Greek Pocket TTS model credits are also linked from the application footer.
