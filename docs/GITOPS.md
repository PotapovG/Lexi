# Lexi GitOps rollout — Core (pre-activation)

**Status: scaffolded, not yet activated.** Merging into `main` must not touch the existing live app until the prerequisites below are explicitly completed and tested. The current Core path `/opt/greek-trainer` is **not** a Git checkout. This is a deliberately separate deployment from the self-hostable Docker Compose example.

## Intended data flow

Contributor fork/branch → PR → structural/HTTP/originality checks → maintainer review/merge → GitHub Action packages the **exact merged SHA** using `git archive` → SSH upload with a dedicated low-privilege deploy account → root-owned `lexi-core-deploy` applicator on Core → immutable release → health-gated secondary then primary rollout → optional automatic code rollback, retaining private backup.

The GitHub job is gated on repository variable **`LEXI_DEPLOY_ENABLED=true`** and the GitHub `production` environment. Until configured it is skipped, including after normal merges. Pull requests never get deploy secrets.

## One-time Core migration (operator task, not automatic)

1. Confirm the repository's latest code matches expected live behaviour (the historical Core tree diverged from GitHub even when first backed up); record a safe baseline commit and test it on a temporary port with a copy of the database, not the live state.
2. Make Caddy's `/greek/` reverse proxy **fail over** from `127.0.0.1:18560` to `127.0.0.1:18561`. Use `lb_policy first`, active `health_uri /health` and `lb_try_duration` to mask the failover window. Update the **Potapov Family canonical GitOps template** and generated Caddy config together, validate and reload Caddy, and exercise an actual controlled upstream outage before arming deployment. Do not hand-edit only the generated config (it would drift).
3. Install `ops/lexi-instance.sh` as root-owned `/usr/local/libexec/lexi-instance` (mode 0755) and `ops/lexi-core-deploy.sh` as `/usr/local/sbin/lexi-core-deploy` (mode 0755). Both are host scripts, not served by Lexi.
4. Create root-owned immutable releases under `/opt/lexi-deploy/releases/<sha>`; provide the approved media WAV directories as symlinks under each release's `pocket-*/wav`. Create `/var/lib/lexi-deploy/slots/{primary,secondary}` with the same verified baseline SHA (0644) and the baseline `deployed.sha`.
5. Add systemd **drop-ins** to existing services, preserving `DynamicUser=yes`, `StateDirectory=greek-trainer`, the live DB/pepper paths, network/privilege sandboxing, and their distinct ports:

   Primary:
   ```ini
   [Service]
   ExecStart=
   ExecStart=/usr/local/libexec/lexi-instance primary
   ```

   Secondary:
   ```ini
   [Service]
   ExecStart=
   ExecStart=/usr/local/libexec/lexi-instance secondary
   ```

   Run `systemctl daemon-reload`; restart the **secondary** first, verify 18561, then verify Caddy fallback, then restart the primary and verify 18560. Never perform this cutover as part of an unknown contributor PR.
6. Create unprivileged `lexideploy` account with SSH key access for Actions. Only that account may upload to `/var/lib/lexi-deploy/incoming`. Give it passwordless sudo for the **single audited deploy script**, not general shell/root capabilities; keep the scripts and slot pointers root-owned. Ideally restrict SSH key with a forced command; verify the actual transport before using it. Keep backups directory root-only 0700.
7. Create root-only `/etc/lexi-deploy/ready` **only after** testing proxy fallback, both slot launchers, backup, success and forced-failure rollback. No file = fail closed.

## GitHub owner-only settings

- Enable PR checks and require review + status checks on `main`; block direct push and force-push, restrict who can merge. `CODEOWNERS` alone does **not** enforce review; branch rules do.
- Configure `production` environment controls as supported by the account/plan.
- Repository variables: `LEXI_DEPLOY_HOST` = Core SSH hostname, `LEXI_DEPLOY_USER` = restricted deploy account, `LEXI_DEPLOY_ENABLED` = `true` **last**.
- Secrets: `LEXI_DEPLOY_SSH_KEY` = dedicated deploy private key for that account; `LEXI_DEPLOY_KNOWN_HOSTS` = independently verified, pinned SSH host key (never accept an unverified runtime `ssh-keyscan`).
- Do **not** give the contributor server credentials, Actions secrets, GitHub admin permissions or the ability to bypass approvals.

## Rollback and data

`lexi-core-deploy` verifies the artifact SHA-256, refuses an unarmed host, validates release paths, takes a **SQLite online backup plus the existing login pepper**, keeps the previous release, then rolls the secondary and primary slots forward with health gates. On a failed restart or HTTP check it restores the previous pointers and attempts service rollback. This is a **code rollback**, not an automatic SQL schema downgrade. If a new release changes migrations, check backward compatibility in advance; recovering from an incompatible migration needs an explicitly planned data restore, not blind downgrade.

After activation, the operator can check `/var/lib/lexi-deploy/deployed.sha`, GitHub Actions runs, both local `/health` endpoints, and the public `/greek/api/catalog` before declaring a release healthy.

**Never** put login codes, SQLite WAL/database, password pepper, purchased course PDF or private audio source in GitHub or Actions artifacts. Never turn on auto-deploy on a Core instance whose Caddy fallback or historical source drift has not been resolved.
