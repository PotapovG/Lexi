"""Run Chromium mobile interaction QA against disposable Lexi server/database."""
import contextlib
import os
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

PORT=18632
BASE=f"http://127.0.0.1:{PORT}"
ROOT=Path(__file__).parent

with tempfile.TemporaryDirectory(prefix="lexi-tracks-browser-") as tmp:
    path=Path(tmp)/"test.sqlite3"
    env=os.environ.copy()
    env.update(GREEK_PORT=str(PORT),GREEK_HOST="127.0.0.1",GREEK_DB=str(path),
        GREEK_ORIGIN=BASE,GREEK_LISTENING="off",PYTHONDONTWRITEBYTECODE="1")
    proc=subprocess.Popen([sys.executable,"server.py"],cwd=str(ROOT),
        env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    try:
        for _ in range(80):
            try:
                with urllib.request.urlopen(BASE+"/greek/health",timeout=0.5) as response:
                    if response.status==200:break
            except (TimeoutError,urllib.error.URLError):
                if proc.poll() is not None:raise RuntimeError(proc.stderr.read().decode()[-2000:])
                time.sleep(0.1)
        else:raise RuntimeError("Test HTTP server unavailable")
        token=secrets.token_hex(16)
        with sqlite3.connect(path) as db:
            db.execute("INSERT INTO accounts(user_id,nickname,code_mac,created_at) VALUES (?,?,?,?)",
                ("browser_test","Browser QA","test-only-mac","2026-10-30T00:00:00Z"))
            db.execute("INSERT INTO auth_sessions(token,user_id,created_at) VALUES (?,?,?)",
                (token,"browser_test","2026-10-30T00:00:00Z"))
        command=["docker","run","--rm","-i","--network","host",
            "-e","QA_TOKEN",
            "-v",str(ROOT)+":/app:ro",
            "mcr.microsoft.com/playwright:v1.56.1-noble",
            "node","-"]
        result=subprocess.run(command,cwd=str(ROOT),
            env={**env,"QA_TOKEN":token},
            input=(ROOT/"qa_tracks_browser.js").read_text(),capture_output=True,text=True,timeout=85)
        if result.stdout:print(result.stdout.strip())
        if result.returncode:
            raise RuntimeError(result.stderr[-3500:])
    finally:
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):proc.wait(timeout=4)
        if proc.poll() is None:proc.kill()
