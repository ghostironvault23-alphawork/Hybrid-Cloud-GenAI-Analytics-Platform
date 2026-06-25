import sqlite3
from datetime import datetime, timezone
from typing import List
from .config import get_settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS ai_requests (
    request_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    confidence TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    detail TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    settings = get_settings()
    db_path = settings.db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def save_ai_request(
    request_id: str,
    user_id: str,
    role: str,
    question: str,
    answer: str,
    confidence: str,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO ai_requests
            (request_id, user_id, role, question, answer, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (request_id, user_id, role, question, answer, confidence, datetime.now(timezone.utc).isoformat()),
        )


def add_audit_log(action: str, detail: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_log (action, detail, created_at) VALUES (?, ?, ?)",
            (action, detail, datetime.now(timezone.utc).isoformat()),
        )


def list_ai_requests(limit: int = 20) -> List[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM ai_requests ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
