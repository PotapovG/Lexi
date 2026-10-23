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
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def request(url, data=None, origin=None):
    headers = {}
    if origin is not None:
        headers["Origin"] = origin
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, headers=headers,
        data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()

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
                ("/greek/", "text/html"), ("/greek/app.js", "text/javascript"),
                ("/greek/styles.css", "text/css"),
                ("/greek/api/catalog", "application/json")):
                code, headers, content = request(base + route)
                assert code == 200 and content_type in headers["Content-Type"] and content, route
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
            print("PASS: clean clone, complete vocab, direct /greek/ routes, origin guard, account creation, isolated SQLite")
        finally:
            proc.terminate()
            try:
                proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate(timeout=5)

if __name__ == "__main__":
    main()
