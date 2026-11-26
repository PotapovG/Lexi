#!/usr/bin/env python3
"""Independent install smoke test. Never touches /var/lib/greek-trainer."""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent

def request(url, data=None, origin=None, method=None):
    headers = {}
    if origin is not None:
        headers["Origin"] = origin
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, headers=headers,
        data=json.dumps(data).encode() if data is not None else None, method=method)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()

class AssetReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        reference = attrs.get("src") if tag == "script" else attrs.get("href") if tag == "link" else None
        if reference and urllib.parse.urlsplit(reference).path.endswith((".js", ".css")):
            self.references.add(reference)


def check_referenced_assets(base, html):
    parser = AssetReferences()
    parser.feed(html.decode("utf-8"))
    assert parser.references, "Served index must expose its script/style references"
    for reference in sorted(parser.references):
        parsed = urllib.parse.urlsplit(urllib.parse.urljoin(base + "/greek/", reference))
        assert parsed.netloc == urllib.parse.urlsplit(base).netloc, reference
        paths = {parsed.path}
        if parsed.path.startswith("/greek/"):
            paths.add(parsed.path[len("/greek"):])
        content_type = "text/javascript" if parsed.path.endswith(".js") else "text/css"
        for path in sorted(paths):
            route = urllib.parse.urlunsplit(("", "", path, parsed.query, ""))
            code, headers, content = request(base + route)
            assert code == 200 and content, ("GET", route, code)
            assert content_type in headers.get("Content-Type", ""), ("GET MIME", route, headers)
            code, headers, body = request(base + route, method="HEAD")
            assert code == 200 and not body, ("HEAD", route, code)
            assert content_type in headers.get("Content-Type", ""), ("HEAD MIME", route, headers)
            assert int(headers["Content-Length"]) == len(content), ("HEAD length", route)
    return len(parser.references)


def main():
    # Imports must work when no WAV files have been provisioned.
    sys.path.insert(0, str(ROOT))
    import server
    assert len(server.ALL) >= 1795 and len(server.vocab.VOCAB) == 1700
    assert not server.LISTENING_ENABLED or (
        len(server.LISTEN_CARDS) == 717 and len(server.listening.AUDIO) == 1266)
    with tempfile.TemporaryDirectory(prefix="lexi-open-source-test-") as folder:
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        origin = f"http://localhost:{port}"
        env = dict(os.environ,
            GREEK_HOST="127.0.0.1", GREEK_PORT=str(port), GREEK_ORIGIN=origin,
            GREEK_DB=str(Path(folder) / "progress.sqlite3"),
            GREEK_PEPPER=str(Path(folder) / "pepper"))
        proc = subprocess.Popen([sys.executable, str(ROOT / "server.py")],
            cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        base = f"http://127.0.0.1:{port}"
        try:
            for _ in range(60):
                try:
                    status, _, data = request(base + "/greek/health")
                    if status == 200:
                        break
                except (ConnectionError, OSError):
                    pass
                time.sleep(0.2)
            else:
                raise AssertionError("App did not start; stderr=" + proc.stderr.read().decode()[:1200])
            assert json.loads(data)["status"] == "ok"
            for route, content_type in (
                ("/greek/", "text/html"), ("/greek/api/catalog", "application/json")):
                code, headers, content = request(base + route)
                assert code == 200 and content_type in headers["Content-Type"] and content, route
                if content_type == "text/html":
                    asset_count = check_referenced_assets(base, content)
            code, _, _ = request(base + "/greek/api/auth/register",
                {"nickname": "CommunityTest"}, origin="https://wrong.example")
            assert code == 403
            code, headers, data = request(base + "/greek/api/auth/register",
                {"nickname": "CommunityTest"}, origin=origin)
            assert code == 200, data
            payload = json.loads(data)
            assert payload["registered"] and len(payload["code"]) == 8
            assert "Secure" in headers["Set-Cookie"]
            assert (Path(folder) / "progress.sqlite3").exists()
            assert (Path(folder) / "pepper").exists()
            print(f"PASS: clean clone, complete vocab, {asset_count} referenced assets GET+HEAD (prefixed/direct), origin guard, account creation, isolated SQLite")
        finally:
            proc.terminate()
            try:
                proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate(timeout=5)

if __name__ == "__main__":
    main()
