# Lexi on Core — protected-main pull GitOps

**Installed 2026-10-23 on Core.** Core's `lexi-gitops-pull.timer` polls every two minutes. Production is currently pinned to the reviewed GitHub `main` commit. **The polling job will not deploy any new commit until GitHub `main` is protected AND that exact commit has a successful `selfhost` GitHub Actions check.** On an unprotected branch it logs `SKIP: main is not protected`.

No GitHub secret, write token, webhook, privileged CI runner, or SSH key is needed. A contributor forks the public repository, opens a PR, CI validates it, the maintainer merges, and Core eventually deploys the precise merged SHA.

## Owner action — required in GitHub UI

Open https://github.com/PotapovG/Lexi/settings/branches and create a branch protection rule for `main`.

1. **Require a pull request before merging**.
2. **Require status checks to pass before merging**; select the GitHub Actions check **`selfhost`**, from workflow **`smoke`**.
3. **Require conversation resolution**; disable force-push and deletion.
4. **Do not allow bypassing the above settings** (where available).
5. Only turn on "Require approvals" when a *second trusted maintainer with write access* can review owner-authored PRs: GitHub does not permit authors to approve their own PRs.

Outsiders should use **Fork → PR**, with no write access to `main`. CODEOWNERS alone does not enforce approval. The puller checks `branches/main.protected=true`; this is a necessary fail-closed prerequisite, but it cannot verify every detail of the protection rule, so also audit the UI settings.

## Production wiring (installed)

- App: `https://potapovfamily.com/greek/`
- Primary: `greek-trainer.service`, port `18560`
- Standby: `greek-trainer-secondary.service`, port `18561`
- Canonical Caddy: `/opt/potapov-family/core/templates/Caddyfile.tmpl`
- Live generated Caddy: `/opt/potapov-family/core/generated/Caddyfile`
- Caddy upstream ordering: primary first, active health checks and standby fallback (primary-down test produced HTTP 200).
- Services use `/usr/local/libexec/lexi-instance {primary|secondary}` with root-owned slot pointers `/var/lib/lexi-deploy/slots/*`.
- Release archives: `/opt/lexi-deploy/releases/<40-hex-sha>`
- Poller: `/usr/local/sbin/lexi-gitops-pull`, systemd `lexi-gitops-pull.timer`
- Applicator: `/usr/local/sbin/lexi-core-deploy`
- Applied SHA: `/var/lib/lexi-deploy/deployed.sha`
- SQLite + pepper remain under `/var/lib/greek-trainer/` and are **never** packaged, uploaded, or reset. Root-only online database backups and pepper copies are stored under `/var/lib/lexi-deploy/backups/`.
- Approved WAV libraries remain on Core and are linked into each immutable release. The old `/opt/greek-trainer` installation remains intact as the emergency legacy fallback.

The applicator verifies SHA-256, rejects unsafe archive members (including symlinks), compiles Python, retains release folders, backs up SQLite online, restarts secondary and checks it, then restarts primary and tests both local health plus the public site/catalog. On failures during service rollover it restores old slot pointers and restarts affected instances. **Schema migrations are not automatically reversible**: verify backward compatibility before merging schema-changing PRs.

## Status and troubleshooting

```bash
systemctl is-active greek-trainer.service greek-trainer-secondary.service
systemctl list-timers lexi-gitops-pull.timer --no-pager
journalctl -u lexi-gitops-pull.service -n 40 --no-pager
cat /var/lib/lexi-deploy/deployed.sha
curl -fsS http://127.0.0.1:18560/health
curl -fsS http://127.0.0.1:18561/health
curl -fsS -o /dev/null -w '%{http_code}\n' https://potapovfamily.com/greek/
```

To suspend automated rollouts without touching the running app: `systemctl disable --now lexi-gitops-pull.timer` or remove the root-owned `/etc/lexi-deploy/ready` gate. The currently served release continues unaffected. Before manual rollback, preserve the database, verify code/schema compatibility, then restore the desired pinned slot pointers and restart standby before primary. Do not blindly restore old DB over active users.

## Verified vs outstanding

**Verified:** isolated GitHub-main canary with temporary SQLite and both host audio libraries; Core's baseline-to-git-main rollout, HTTP 200 on both ports, public catalog, real Caddy primary-down failover, all nine accounts and 2,194 existing attempts preserved; unprotected-main poll blocked. **Not yet verified:** induced malformed-release rollback drill (must be done in a controlled maintenance/test window); end-to-end automatic rollout after owner enables protection; future schema migration compatibility. Do not claim those tests were completed.

## Educational content and intellectual property

The commercial source textbook is not shipped. New exercises must be independently authored and reviewed under `CONTENT_RIGHTS.md`; the MIT code license is not a blanket license for educational data. Pocket TTS attribution is in `THIRD_PARTY_NOTICES.md`.
