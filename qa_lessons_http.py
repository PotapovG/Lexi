"""Real HTTP tests for long Lexi lessons, locked futures, and unchanged Classic."""
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
                with urllib.request.urlopen(ORIGIN+"/greek/health",timeout=.5) as r:
                    if r.status==200:break
            except (TimeoutError,urllib.error.URLError):
                if proc.poll() is not None:raise RuntimeError(proc.stderr.read().decode()[-1800:])
                time.sleep(.1)
        else:raise RuntimeError("HTTP service failed")
        jar=http.cookiejar.CookieJar()
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        try:
            call(opener,"/board")
            raise AssertionError("anonymous board state accessible")
        except urllib.error.HTTPError as exc:assert exc.code==401
        reg,_=call(opener,"/auth/register",{"nickname":"Lesson HTTP QA"})
        assert reg["registered"] and reg["code"]
        token=next(x.value for x in jar if x.name=="greek_session")
        opener.addheaders=[("Cookie","greek_session="+token)]
        board,_=call(opener,"/board?lang=ru")
        assert board["position"]==0 and len(board["nodes"])==8
        assert board["lesson"] is None
        assert all(x["state"]=="locked" and "name" not in x for x in board["nodes"][1:])
        try:
            call(opener,"/board",{"action":"lesson_start","revision":board["revision"]},origin=False)
            raise AssertionError("CSRF bypass")
        except urllib.error.HTTPError as e:assert e.code==403
        lesson,_=call(opener,"/board",{"action":"lesson_start","revision":board["revision"],"lang":"ru"})
        assert lesson["lesson"]["count"]>=10 and lesson["lesson"]["question"]
        assert lesson["nodes"][1]["state"]=="locked" and "name" not in lesson["nodes"][1]
        question=lesson["lesson"]["question"]
        assert "answer" not in question
        try:
            call(opener,"/board",{"action":"answer","selected":"not-an-option",
                "lessonIndex":0,"questionId":question["id"],
                "revision":lesson["revision"],"lang":"ru"})
            raise AssertionError("invalid option scored")
        except urllib.error.HTTPError as e:assert e.code==400
        same,_=call(opener,"/board?lang=ru")
        assert same["revision"]==lesson["revision"]
        assert same["lesson"]["question"]==question
        paused,_=call(opener,"/board",{"action":"pause","revision":same["revision"],"lang":"ru"})
        assert paused["lesson"]["paused"]
        resumed,_=call(opener,"/board",{"action":"lesson_start",
              "revision":paused["revision"],"lang":"ru"})
        assert not resumed["lesson"]["paused"] and resumed["lesson"]["at"]==0
        try:
            call(opener,"/board",{"action":"lesson_start","revision":paused["revision"],"lang":"ru"})
            raise AssertionError("replayed state transition")
        except urllib.error.HTTPError as e:assert e.code==409
        classic,_=call(opener,"/quiz?scope=chapters&chapters=1&types=word&lang=ru&count=5")
        assert len(classic["questions"])==5
        print("PASS HTTP auth/CSRF, locked future lessons, pause/resume, no answer leak, Classic unaffected")
    finally:
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):proc.wait(timeout=4)
        if proc.poll() is None:proc.kill()
