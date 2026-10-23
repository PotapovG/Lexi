#!/usr/bin/env bash
# Public-repo pull GitOps. Intentionally fail-closed before protected main + CI.
set -Eeuo pipefail
umask 077
[[ "$EUID" -eq 0 ]] || { echo "root required" >&2; exit 2; }
root=/var/lib/lexi-deploy
[[ -f /etc/lexi-deploy/ready ]] || { echo "not armed"; exit 0; }
install -d -m 0755 "$root"
install -d -m 0700 "$root/incoming"
exec 8>"$root/poll.lock"
flock -n 8 || { echo "poll already in progress"; exit 0; }
url=https://api.github.com/repos/PotapovG/Lexi
agent='Lexi-Core-GitOps/1.0'
get_json() { curl --fail --silent --show-error --location --connect-timeout 5 --max-time 20 -H 'Accept: application/vnd.github+json' -A "$agent" "$1"; }
branch=$(get_json "$url/branches/main")
read -r protected expected < <(printf '%s' "$branch" | python3 -c 'import sys,json; x=json.load(sys.stdin); print(str(x.get("protected",False)).lower(),x.get("commit",{}).get("sha","missing"))')
if [[ "$protected" != true ]]; then echo "SKIP: main is not protected"; exit 0; fi
[[ "$expected" =~ ^[a-f0-9]{40}$ ]] || exit 3
current=$(cat "$root/deployed.sha" 2>/dev/null || true)
[[ "$current" != "$expected" ]] || { echo "up-to-date $expected"; exit 0; }
checks=$(get_json "$url/commits/$expected/check-runs?per_page=100")
printf '%s' "$checks" | python3 -c '
import sys,json
d=json.load(sys.stdin)
v=[c for c in d.get("check_runs",[]) if c.get("name")=="selfhost" and c.get("app",{}).get("slug")=="github-actions" and c.get("head_sha") not in (None,"")]
if not any(c.get("status")=="completed" and c.get("conclusion")=="success" for c in v):
    print("Required GitHub Actions selfhost check not green",file=sys.stderr)
    sys.exit(1)
' || { echo "SKIP: required CI check not green at $expected"; exit 0; }
repo="$root/repo.git"
if [[ ! -d "$repo" ]]; then
    mkdir -p "$repo"; git init --quiet --bare "$repo"
    git --git-dir="$repo" remote add origin https://github.com/PotapovG/Lexi.git
fi
GIT_TERMINAL_PROMPT=0 git --git-dir="$repo" -c protocol.version=2 fetch --quiet --no-tags --depth=1 origin refs/heads/main
actual=$(git --git-dir="$repo" rev-parse FETCH_HEAD)
[[ "$actual" == "$expected" ]] || { echo "SKIP: branch advanced during poll ($actual != $expected)"; exit 0; }
tmp=$(mktemp "$root/incoming/.bundle.XXXXXXXX")
trap 'rm -f -- "$tmp"' EXIT
git --git-dir="$repo" archive --format=tar "$actual" | gzip -n >"$tmp"
digest=$(sha256sum "$tmp" | awk '{print $1}')
dest="$root/incoming/lexi-$actual.tar.gz"
mv -f -- "$tmp" "$dest"
trap - EXIT
/usr/local/sbin/lexi-core-deploy "$actual" "$digest"
