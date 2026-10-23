#!/usr/bin/env bash
# Core-only GitOps applicator. Trusted SHA artifact from reviewed GitHub main.
set -Eeuo pipefail
umask 077
[[ "$EUID" -eq 0 ]] || { echo 'root via restricted sudo required' >&2; exit 2; }
sha="${1:-}"; digest="${2:-}"
[[ "$sha" =~ ^[a-f0-9]{40}$ && "$digest" =~ ^[a-f0-9]{64}$ ]] || { echo 'bad SHA arguments' >&2; exit 2; }
root=/opt/lexi-deploy
state=/var/lib/lexi-deploy
archive="$state/incoming/lexi-$sha.tar.gz"
ready=/etc/lexi-deploy/ready
[[ -f "$ready" && -f "$archive" ]] || { echo 'not bootstrapped/armed or artifact missing' >&2; exit 3; }
install -d -m 0700 "$state" "$state/backups"
exec 9>"$state/deploy.lock"; flock -n 9 || { echo 'deploy locked' >&2; exit 4; }
echo "$digest  $archive" | sha256sum -c --status || { echo 'artifact checksum failed' >&2; exit 5; }
for slot in primary secondary; do
    [[ -f "$state/slots/$slot" ]] || { echo "uninitialized slot $slot" >&2; exit 6; }
done
old_primary=$(cat "$state/slots/primary")
old_secondary=$(cat "$state/slots/secondary")
[[ "$old_primary" =~ ^[a-f0-9]{40}$ && "$old_secondary" =~ ^[a-f0-9]{40}$ ]] || exit 7
[[ "$old_primary" == "$old_secondary" ]] || { echo 'slots not converged; manual investigation required' >&2; exit 8; }
[[ "$old_primary" != "$sha" ]] || { echo "already deployed $sha"; exit 0; }
# Preconditions: the proxy MUST have working fallback to the secondary and
# systemd must launch pinned slots; these are manually validated before arming.
for unit in greek-trainer.service greek-trainer-secondary.service; do
    systemctl cat "$unit" | grep -q '/usr/local/libexec/lexi-instance' || {
        echo "missing slot-aware systemd override: $unit" >&2; exit 9;
    }
done
if ! grep -q '18561' /opt/potapov-family/core/generated/Caddyfile; then
    echo 'Caddy fallback upstream absent; fail closed' >&2; exit 10
fi
[[ -d "$root/releases/$old_primary" ]] || { echo 'old release missing' >&2; exit 11; }
tmp=$(mktemp -d "$root/.staging-$sha.XXXXXXXX")
cleanup() { rm -rf -- "$tmp"; }
changed_secondary=0
changed_primary=0
rollback() {
    echo 'Deploy failed. Restoring prior slot pointers and restarting affected slot(s).' >&2
    printf '%s\n' "$old_secondary" >"$state/slots/secondary.tmp"
    mv -f "$state/slots/secondary.tmp" "$state/slots/secondary"
    printf '%s\n' "$old_primary" >"$state/slots/primary.tmp"
    mv -f "$state/slots/primary.tmp" "$state/slots/primary"
    if [[ "$changed_secondary" == 1 ]]; then systemctl restart greek-trainer-secondary.service || true; fi
    if [[ "$changed_primary" == 1 ]]; then systemctl restart greek-trainer.service || true; fi
}
trap cleanup EXIT
# Defense in depth: only regular files and directories inside the archive.
# Forbid symbolic links, hard links, special files, absolute and parent paths
# even if a future contributor attempts to sneak them into a commit.
python3 - "$archive" <<'PY'
import pathlib,sys,tarfile
with tarfile.open(sys.argv[1],"r:gz") as t:
    members=t.getmembers()
    if len(members)>10000: raise SystemExit("archive has too many members")
    total=0
    for m in members:
        p=pathlib.PurePosixPath(m.name)
        if p.is_absolute() or '..' in p.parts or not (m.isfile() or m.isdir()):
            raise SystemExit("unsafe archive member: "+m.name)
        total += m.size
        if total > 100*1024*1024: raise SystemExit("archive unexpectedly large")
PY
tar -xzf "$archive" --no-same-owner --no-same-permissions -C "$tmp"
test -s "$tmp/server.py"; test -s "$tmp/catalog_v2.py"
# WAVs are private-ish large immutable host assets, not part of the Git archive.
for group in pocket-listening pocket-pronunciation; do
    test -d "$tmp/$group"
    test ! -e "$tmp/$group/wav"
    ln -s "/opt/greek-trainer/$group/wav" "$tmp/$group/wav"
done
chmod -R a+rX "$tmp"
find "$tmp" -name '*.py' -type f -print0 | xargs -0 -r /usr/bin/python3 -m py_compile
release="$root/releases/$sha"
if [[ -d "$release" ]]; then
    echo "reusing staged release $sha"
    rm -rf -- "$tmp"
else
    mv -T "$tmp" "$release"
fi
trap - EXIT
# Online SQLite backup, not a raw WAL copy. Never upload progress or login pepper.
backup="$state/backups/$(date -u +%Y%m%dT%H%M%SZ)-$old_primary"
install -d -m 0700 "$backup"
DB=/var/lib/greek-trainer/progress.sqlite3
PEPPER=/var/lib/greek-trainer/login-pepper
if [[ -f "$DB" ]]; then
    /usr/bin/python3 -c 'import sqlite3,sys; a=sqlite3.connect("file:"+sys.argv[1]+"?mode=ro",uri=True); b=sqlite3.connect(sys.argv[2]); a.backup(b); b.close();a.close()' "$DB" "$backup/progress.sqlite3"
fi
[[ ! -f "$PEPPER" ]] || cp -p "$PEPPER" "$backup/login-pepper"
health() {
    local port="$1"
    for i in $(seq 1 35); do
        if curl --connect-timeout 1 --max-time 2 -fsS "http://127.0.0.1:$port/health" | grep -q '"ok"'; then return 0; fi
        sleep 1
    done
    return 1
}
# Caddy continues serving the old primary during the secondary restart.
trap 'rollback' ERR
printf '%s\n' "$sha" >"$state/slots/secondary.tmp"
chmod 0644 "$state/slots/secondary.tmp"
mv -f "$state/slots/secondary.tmp" "$state/slots/secondary"
changed_secondary=1
systemctl restart greek-trainer-secondary.service
health 18561
# During primary restart, Caddy's active/passive upstream fallback serves secondary.
printf '%s\n' "$sha" >"$state/slots/primary.tmp"
chmod 0644 "$state/slots/primary.tmp"
mv -f "$state/slots/primary.tmp" "$state/slots/primary"
changed_primary=1
systemctl restart greek-trainer.service
health 18560
curl --connect-timeout 2 --max-time 6 -fsS https://potapovfamily.com/greek/ >/dev/null
curl --connect-timeout 2 --max-time 6 -fsS https://potapovfamily.com/greek/api/catalog >/dev/null
trap - ERR
printf '%s\n' "$sha" > "$state/deployed.sha"
chmod 0644 "$state/deployed.sha"
rm -f -- "$archive"
echo "Deployed Lexi $sha; prior release retained for rollback"
