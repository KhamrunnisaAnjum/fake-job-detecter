# db.py — SQLite user store with bcrypt passwords
import sqlite3, bcrypt, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def _conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    con = _conn()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS scans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            title       TEXT,
            risk        TEXT,
            score       REAL,
            raw_message TEXT    DEFAULT '',
            input_mode  TEXT    DEFAULT 'structured',
            created_at  TEXT    NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    con.commit()
    con.close()


# ── User operations ──────────────────────────────────────────────────

def register_user(username: str, email: str, password: str):
    """Returns (True, None) on success or (False, error_msg)."""
    email = email.strip().lower()
    if not username.strip():
        return False, "Username is required."
    if len(username.strip()) < 2:
        return False, "Username must be at least 2 characters."
    if "@" not in email:
        return False, "Enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        con = _conn()
        con.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?,?,?,?)",
            (username.strip(), email, pw_hash,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        con.commit()
        con.close()
        return True, None
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."


def login_user(email: str, password: str):
    """Returns user dict on success, or (None, error_msg)."""
    email = email.strip().lower()
    con = _conn()
    row = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    con.close()
    if not row:
        return None, "No account found with that email."
    if not bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
        return None, "Incorrect password."
    return dict(row), None


def get_user_by_id(uid: int):
    con = _conn()
    row = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    con.close()
    return dict(row) if row else None


def update_password(uid: int, new_password: str):
    pw_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    con = _conn()
    con.execute("UPDATE users SET password_hash=? WHERE id=?", (pw_hash, uid))
    con.commit()
    con.close()


# ── Scan operations ──────────────────────────────────────────────────

def save_scan(user_id, title, risk, score, raw_message="", input_mode="structured"):
    safe_title = str(title).replace("\n", " ").replace("\r", "")[:120]
    safe_msg   = str(raw_message).replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    con = _conn()
    con.execute(
        """INSERT INTO scans (user_id, title, risk, score, raw_message, input_mode, created_at)
           VALUES (?,?,?,?,?,?,?)""",
        (user_id, safe_title, risk, round(float(score), 2), safe_msg, input_mode,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    con.commit()
    con.close()


def get_user_scans(user_id: int):
    """Returns DataFrame of scans belonging ONLY to this user."""
    import pandas as pd
    con = _conn()
    rows = con.execute(
        "SELECT * FROM scans WHERE user_id=? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    con.close()
    if not rows:
        return pd.DataFrame(columns=["id","user_id","title","risk","score","raw_message","input_mode","created_at"])
    df = pd.DataFrame([dict(r) for r in rows])
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
    return df


def delete_scan(scan_id: int, user_id: int):
    """Delete only if the scan belongs to this user."""
    con = _conn()
    con.execute("DELETE FROM scans WHERE id=? AND user_id=?", (scan_id, user_id))
    con.commit()
    con.close()
