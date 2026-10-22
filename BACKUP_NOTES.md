# Lexi source backup

Snapshot copied from the running Greek trainer on Core VPS at `/opt/greek-trainer` on 2026-10-22.

This repository captures application source code, educational content tables, translations, tests, documentation, Pocket TTS generation scripts, and audio manifests.

**Not a full machine/deployment backup:** the production SQLite database and learner accounts/progress, secrets, systemd/Caddy configuration, package dependencies, pretrained model binaries, and generated WAV recordings are intentionally omitted. The recorded WAV media must be preserved separately for a full offline restoration. Do not commit the live student database or credentials, especially while this repository is public.

`SNAPSHOT_MANIFEST.json` lists each source file's original SHA-256 so that this snapshot can be checked against the source. Future deployments should operate from version-controlled source, not rewrite production files in place.

The live service was not restarted or changed for this backup.

**Known missing source file:** `vocab_curated_1700.tsv` was not transferred to GitHub and remains on Core VPS. The repository is therefore not independently sufficient to restore this vocabulary module. The snapshot manifest explicitly records its hash and size.

**2026-10-22 follow-up:** this note documents the initial import only. The missing vocabulary TSV is included in the subsequent community/self-hosting commit, along with deployment and contribution tooling. Use the repository main branch rather than the initial snapshot for full current source.
