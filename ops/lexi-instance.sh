#!/bin/sh
# Installed as /usr/local/libexec/lexi-instance; run by sandboxed systemd user.
set -eu
case "${1:-}" in primary|secondary) slot="$1";; *) echo "invalid slot" >&2; exit 2;; esac
sha=$(cat "/var/lib/lexi-deploy/slots/$slot")
printf '%s' "$sha" | grep -Eq '^[a-f0-9]{40}$' || exit 3
release="/opt/lexi-deploy/releases/$sha"
test -f "$release/server.py" || exit 4
cd "$release"
exec /usr/bin/python3 "$release/server.py"
