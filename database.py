from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DB_PATH = Path(__file__).resolve().parent / "database.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                organisation TEXT NOT NULL,
                job_title TEXT NOT NULL,
                country TEXT NOT NULL,
                employee_id TEXT DEFAULT '',
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percentage REAL NOT NULL,
                passed INTEGER NOT NULL,
                attempted_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                certificate_id TEXT NOT NULL UNIQUE,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percentage REAL NOT NULL,
                issued_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_user(**data: Any) -> dict:
    init_db()
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (
                    full_name, email, organisation, job_title, country,
                    employee_id, password_hash, password_salt, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["full_name"],
                    data["email"],
                    data["organisation"],
                    data["job_title"],
                    data["country"],
                    data.get("employee_id", ""),
                    data["password_hash"],
                    data["password_salt"],
                    _now(),
                ),
            )
            return {"success": True, "user_id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "An account with this email already exists."}


def authenticate_user(email: str) -> dict | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, full_name, email, organisation, job_title, country,
                   employee_id, created_at
            FROM users WHERE id = ?
            """,
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def save_quiz_attempt(user_id: int, score: int, total: int, passed: bool) -> int:
    percentage = round((score / total) * 100, 2)
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO quiz_attempts (
                user_id, score, total, percentage, passed, attempted_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, score, total, percentage, int(passed), _now()),
        )
        return int(cursor.lastrowid)


def get_best_attempt(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT * FROM quiz_attempts
            WHERE user_id = ?
            ORDER BY percentage DESC, attempted_at DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


def get_certificate(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM certificates WHERE user_id = ?", (user_id,)
        ).fetchone()
    return dict(row) if row else None


def create_certificate(
    user_id: int,
    certificate_id: str,
    score: int,
    total: int,
    percentage: float,
) -> dict:
    existing = get_certificate(user_id)
    if existing:
        return existing

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO certificates (
                user_id, certificate_id, score, total, percentage, issued_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, certificate_id, score, total, percentage, _now()),
        )
    return get_certificate(user_id)
