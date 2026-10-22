# Deployment and operations

## Baseline

- Docker Compose + persistent named volume, bound only to 127.0.0.1:18560.
- `docker compose up -d --build` builds one Python 3.11 container.
- Default local URL: http://localhost:18560/greek/
- Production: exact `LEXI_ORIGIN=https://your-host`, Caddy HTTPS
  `handle_path /greek/* { reverse_proxy 127.0.0.1:18560 }`.
- `/health` endpoint for container health checks.

## Back up and restore (private)

Student accounts, codes and progress are in the persistent SQLite database;
the separate generated `login-pepper` is essential for existing login codes.
Back them up together in secure, access-controlled storage, **not GitHub**.
For consistent snapshot either stop the instance or use SQLite's online
backup API rather than copying a live WAL database alone.

```bash
docker compose stop lexi
docker run --rm -v lexi_lexi_data:/from:ro -v "$PWD":/to alpine \
  tar -C /from -czf /to/lexi-private-data.tgz .
docker compose start lexi
```

The volume name depends on the Compose project name, so replace
`lexi_lexi_data` if your Compose project differs. Ensure the backup
archive is encrypted and stored privately. Restore to a stopped instance.

## Upgrade and rollback

Use Git tags/releases, review migrations and then redeploy:
`git pull --ff-only && docker compose up -d --build`.
Before each deploy, take a private data backup. Pin a known-good tag or
commit to roll back code. Do not reuse a newer SQLite schema with old
code without testing compatibility first.

## Security

- TLS and secure cookies are mandatory on public domains.
- The app uses **eight-digit login codes**, which are not high-entropy
  credentials. Apply IP rate limiting and HTTPS at the ingress.
- Keep `GREEK_ORIGIN` exact; never set a wildcard.
- Protect database and login pepper with private filesystem permissions.
- Don't expose the Python backend directly on a public network.
- For production and larger user bases, review authentication hardening,
  monitoring, backups and data retention before inviting strangers.
