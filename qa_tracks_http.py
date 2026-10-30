"""Exercise actual account-authenticated study-track HTTP endpoints on a test DB."""
import contextlib
import http.cookiejar
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

PORT=18631
BASE=f"http://127.0.0.1:{PORT}/greek/api"
ORIGIN=f"http://127.0.0.1:{PORT}"

def open_req(opener,path,payload=None,origin=True):
    data=json.dumps(payload,ensure_ascii=False).encode("utf-8") if payload is not None else None
    req=urllib.request.Request(BASE+path,data=data)
    if payload is not None:
        req.add_header("Content-Type","application/json")
        if origin:req.add_header("Origin",ORIGIN)
    with opener.open(req,timeout=7) as resp:
        return json.loads(resp.read()),resp.status

with tempfile.TemporaryDirectory() as folder:
    env=os.environ.copy()
    env.update(GREEK_PORT=str(PORT),GREEK_HOST="127.0.0.1",GREEK_DB=str(Path(folder)/"db.sqlite3"),
               GREEK_ORIGIN=ORIGIN,GREEK_LISTENING="off",PYTHONDONTWRITEBYTECODE="1")
    proc=subprocess.Popen([sys.executable,"server.py"],cwd=str(Path(__file__).parent),
                         env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    try:
        for _ in range(60):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/greek/health",timeout=0.5) as resp:
                    if resp.status==200:break
            except (urllib.error.URLError,TimeoutError):
                if proc.poll() is not None:raise RuntimeError(proc.stderr.read().decode()[-2500:])
                time.sleep(0.1)
        else:raise RuntimeError("dev server did not start")
        jar=http.cookiejar.CookieJar()
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        try:
            open_req(opener,"/tracks/anki")
            raise AssertionError("anonymous state leaked")
        except urllib.error.HTTPError as e:assert e.code==401
        try:
            open_req(opener,"/auth/register",{"nickname":"Tracks QA"},origin=False)
            raise AssertionError("cross-origin registration accepted")
        except urllib.error.HTTPError as e:assert e.code==403
        reg,_=open_req(opener,"/auth/register",{"nickname":"Tracks QA"})
        assert reg["registered"] and reg["code"]
        # Production uses Secure cookies (HTTPS); plain localhost test must
        # manually attach the returned session cookie without weakening it.
        session=next(x.value for x in jar if x.name=="greek_session")
        opener.addheaders=[("Cookie","greek_session="+session)]
        cfg,_=open_req(opener,"/life?lang=ru")
        assert cfg["maxChapter"]==6
        try:
            open_req(opener,"/tracks/periptero?lang=ru")
            raise AssertionError("market accessible before chapter 8")
        except urllib.error.HTTPError as e:assert e.code in (400,403)
        cfg,_=open_req(opener,"/life",{"lang":"ru","revision":cfg["revision"],"maxChapter":16})
        assert cfg["maxChapter"]==16
        for route in ("anki","route","likes","periptero"):
            state,status=open_req(opener,"/tracks/"+route+"?lang=ru")
            assert status==200 and state["revision"]==0
            assert "expected" not in str(state)
        s,_=open_req(opener,"/tracks/anki?lang=ru")
        s,_=open_req(opener,"/tracks/anki",{"action":"advance","revision":s["revision"],"lang":"ru"})
        assert s["revision"]==1
        try:
            open_req(opener,"/tracks/anki",{"action":"advance","revision":0,"lang":"ru"})
            raise AssertionError("duplicate accepted")
        except urllib.error.HTTPError as e:assert e.code==409
        route,_=open_req(opener,"/tracks/route?lang=ru")
        correct_fields=["number","origin","via1","via2","stop","destination"]
        assert route["fields"]==correct_fields
        likes,_=open_req(opener,"/tracks/likes?lang=ru")
        bad,_=open_req(opener,"/tracks/likes",{"lang":"ru","revision":likes["revision"],"action":"submit","answer":"хочу книгу"})
        assert not bad["feedback"]["correct"] and bad["step"]==1
        store,_=open_req(opener,"/tracks/periptero?lang=ru")
        assert len(store["items"])==4
        bought,_=open_req(opener,"/tracks/periptero",{"lang":"ru","revision":store["revision"],"action":"buy",
           "productId":"apple","phrase":"Θα ήθελα ένα μήλο, παρακαλώ."})
        assert bought["feedback"]["correct"] and "apple" in bought["bought"]
        # Catalog counts are unchanged: these are independent tracks.
        catalog,_=open_req(opener,"/catalog")
        assert catalog["practiceCardCount"]==2132
        print("PASS authenticated HTTP 4 tracks, logged-out denial, CSRF, idempotent revision conflicts, no answer leak")
    finally:
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):proc.wait(timeout=5)
        if proc.poll() is None:proc.kill()
