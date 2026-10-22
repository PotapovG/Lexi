"""Minimal account authentication for Λέξη.
8-digit codes are bearer credentials, NOT high entropy passwords.
Never log codes or persist plaintext server-side. TLS and rate limits are mandatory.
"""
import datetime as dt
import hashlib,hmac,os,secrets,sqlite3,time,re,unicodedata
from pathlib import Path

SECRET_FILE=Path(os.environ.get("GREEK_PEPPER","/var/lib/greek-trainer/login-pepper"))
CODE_RE=re.compile(r"[0-9]{8}\Z")
def ensure_secret():
    SECRET_FILE.parent.mkdir(parents=True,exist_ok=True)
    try:
        fd=os.open(str(SECRET_FILE),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError:
        pass
    else:
        with os.fdopen(fd,"wb") as f:f.write(secrets.token_bytes(32))
    return SECRET_FILE.read_bytes()

def schema(db):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS accounts(
      user_id TEXT PRIMARY KEY,
      nickname TEXT COLLATE NOCASE NOT NULL UNIQUE,
      code_mac TEXT NOT NULL UNIQUE,
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS auth_sessions(
      token TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES accounts(user_id)
    );
    CREATE INDEX IF NOT EXISTS ix_auth_sessions_user ON auth_sessions(user_id);
    CREATE TABLE IF NOT EXISTS auth_failures(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ip_hash TEXT NOT NULL,
      attempt_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS ix_auth_failures_ip ON auth_failures(ip_hash,attempt_at);
    CREATE TABLE IF NOT EXISTS auth_signups(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ip_hash TEXT NOT NULL,
      attempt_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS ix_auth_signups_ip ON auth_signups(ip_hash,attempt_at);
    """)
    ensure_secret()

def code_mac(code):
    return hmac.new(ensure_secret(),code.encode("ascii"),hashlib.sha256).hexdigest()

def valid_nick(s):
    if not isinstance(s,str):return None
    n=unicodedata.normalize("NFC",s).strip()
    if not 3<=len(n)<=28 or not re.fullmatch(r"[\w .-]+",n,re.UNICODE):return None
    if not any(ch.isalpha() for ch in n):return None
    return n

def current(db,token):
    row=db.execute("""SELECT a.user_id,a.nickname FROM auth_sessions s
                      JOIN accounts a ON a.user_id=s.user_id WHERE s.token=?""",(token,)).fetchone()
    return dict(row) if row else None

def register(db,legacy_id,nickname,ip="local"):
    nick=valid_nick(nickname)
    if not nick:raise ValueError("nickname_invalid")
    if current(db,legacy_id):raise ValueError("already_registered")
    stamp=int(time.time())
    ip_hash=hmac.new(ensure_secret(),ip.encode("utf-8"),hashlib.sha256).hexdigest()
    db.execute("DELETE FROM auth_signups WHERE attempt_at<?",(stamp-3600,))
    per_ip=db.execute("SELECT COUNT(*) FROM auth_signups WHERE ip_hash=?",(ip_hash,)).fetchone()[0]
    total=db.execute("SELECT COUNT(*) FROM auth_signups").fetchone()[0]
    if per_ip>=4 or total>=100:raise ValueError("rate_limited")
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    for _ in range(24):
        code=f"{secrets.randbelow(100000000):08d}"
        mac=code_mac(code)
        if db.execute("SELECT 1 FROM accounts WHERE code_mac=?",(mac,)).fetchone():continue
        token=secrets.token_hex(16)
        try:
            db.execute("INSERT INTO accounts(user_id,nickname,code_mac,created_at) VALUES(?,?,?,?)",
                       (legacy_id,nick,mac,now))
            db.execute("INSERT INTO auth_sessions(token,user_id,created_at) VALUES(?,?,?)",
                       (token,legacy_id,now))
            db.execute("INSERT INTO auth_signups(ip_hash,attempt_at) VALUES (?,?)",(ip_hash,stamp))
        except sqlite3.IntegrityError:
            raise ValueError("nickname_taken")
        return {"nickname":nick,"code":code,"token":token}
    raise RuntimeError("code_exhausted")

def login(db,code,ip):
    if not isinstance(code,str) or not CODE_RE.fullmatch(code):
        raise ValueError("invalid_credentials")
    now=int(time.time())
    hashed_ip=hmac.new(ensure_secret(),ip.encode("utf8"),hashlib.sha256).hexdigest()
    db.execute("DELETE FROM auth_failures WHERE attempt_at<?",(now-900,))
    local=db.execute("SELECT COUNT(*) FROM auth_failures WHERE ip_hash=?",(hashed_ip,)).fetchone()[0]
    global_total=db.execute("SELECT COUNT(*) FROM auth_failures").fetchone()[0]
    if local>=5 or global_total>=100:raise ValueError("rate_limited")
    row=db.execute("SELECT user_id,nickname FROM accounts WHERE code_mac=?",(code_mac(code),)).fetchone()
    if not row:
        db.execute("INSERT INTO auth_failures(ip_hash,attempt_at) VALUES (?,?)",(hashed_ip,now))
        db.commit()  # Failure counters must survive the caller's transaction.
        raise ValueError("invalid_credentials")
    token=secrets.token_hex(16)
    db.execute("INSERT INTO auth_sessions(token,user_id,created_at) VALUES (?,?,?)",
               (token,row["user_id"],dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
    db.execute("DELETE FROM auth_failures WHERE ip_hash=?",(hashed_ip,))
    return {"nickname":row["nickname"],"token":token,"user_id":row["user_id"]}

def logout(db,token):
    db.execute("DELETE FROM auth_sessions WHERE token=?",(token,))

