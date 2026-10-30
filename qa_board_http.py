"""Real HTTP QA for the independent progressive Lexi board and legacy API."""
import contextlib
import http.cookiejar
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

PORT=18638
BASE=f"http://127.0.0.1:{PORT}/greek/api"
ORIGIN=f"http://127.0.0.1:{PORT}"
ROOT=Path(__file__).parent

def call(opener,path,body=None,origin=True):
    data=json.dumps(body,ensure_ascii=False).encode() if body is not None else None
    req=urllib.request.Request(BASE+path,data=data)
    if body is not None:
        req.add_header("Content-Type","application/json")
        if origin:req.add_header("Origin",ORIGIN)
    with opener.open(req,timeout=8) as resp:return json.loads(resp.read()),resp.status

with tempfile.TemporaryDirectory() as folder:
    env={**os.environ,"GREEK_HOST":"127.0.0.1","GREEK_PORT":str(PORT),
         "GREEK_DB":str(Path(folder)/"test.sqlite3"),"GREEK_ORIGIN":ORIGIN,
         "PYTHONDONTWRITEBYTECODE":"1"}
    proc=subprocess.Popen([sys.executable,"server.py"],cwd=ROOT,env=env,
                          stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    try:
        for _ in range(80):
            try:
                with urllib.request.urlopen(ORIGIN+"/greek/health",timeout=0.5) as r:
                    if r.status==200:break
            except (TimeoutError,urllib.error.URLError):
                if proc.poll() is not None:raise RuntimeError(proc.stderr.read().decode()[-1400:])
                time.sleep(0.1)
        else:raise RuntimeError("HTTP service failed")
        jar=http.cookiejar.CookieJar()
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        try:
            call(opener,"/board")
            raise AssertionError("anonymous board state accessible")
        except urllib.error.HTTPError as exc:assert exc.code==401
        reg,_=call(opener,"/auth/register",{"nickname":"Board HTTP QA"})
        assert reg["registered"] and reg["code"]
        token=next(x.value for x in jar if x.name=="greek_session")
        opener.addheaders=[("Cookie","greek_session="+token)]
        board,_=call(opener,"/board?lang=ru")
        q=board["quest"]["question"]
        assert board["position"]==0 and len(board["nodes"])==48
        assert q["choices"] and "answer" not in q
        try:
            call(opener,"/board",{"action":"scope","chapterLimit":9,
                "revision":board["revision"],"lang":"ru"},origin=False)
            raise AssertionError("CSRF bypass")
        except urllib.error.HTTPError as e:assert e.code==403
        try:
            call(opener,"/board",{"action":"answer","selected":"invented",
                "questId":q["id"],"revision":board["revision"],"lang":"ru"})
            raise AssertionError("non-option answer accepted")
        except urllib.error.HTTPError as e:assert e.code==400
        # Re-reading a board card does not consume it or alter its revision.
        same,_=call(opener,"/board?lang=ru")
        assert same["revision"]==board["revision"] and same["quest"]==board["quest"]
        changed,_=call(opener,"/board",{"action":"scope","revision":board["revision"],
            "chapterLimit":4,"lang":"ru"})
        assert changed["chapterLimit"]==4 and len(changed["nodes"])==32
        try:
            call(opener,"/board",{"action":"scope","revision":board["revision"],
                "chapterLimit":5,"lang":"ru"})
            raise AssertionError("stale revision accepted")
        except urllib.error.HTTPError as e:assert e.code==409
        old,_=call(opener,"/quiz?scope=chapters&chapters=1&types=word&lang=ru&count=5")
        assert len(old["questions"])==5 and old["questions"][0]["kind"]=="word"
        print("PASS real HTTP auth/CSRF, board revision, no answer leak, classic quiz still works")
    finally:
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):proc.wait(timeout=4)
        if proc.poll() is None:proc.kill()
