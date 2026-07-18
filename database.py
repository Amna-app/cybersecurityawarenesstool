from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


APP_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("RESEARCH_DB_PATH", str(APP_DIR / "research_data.db")))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Open a short-lived SQLite connection suitable for Streamlit reruns."""
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT PRIMARY KEY,
                age_group TEXT NOT NULL,
                gender TEXT NOT NULL,
                education_level TEXT NOT NULL,
                employment_status TEXT NOT NULL,
                previous_training TEXT NOT NULL,
                computer_use TEXT NOT NULL,
                consent_given INTEGER NOT NULL CHECK(consent_given IN (0,1)),
                consent_version TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS questionnaire_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participant_id TEXT NOT NULL,
                stage TEXT NOT NULL CHECK(stage IN ('pre','post')),
                question_key TEXT NOT NULL,
                question_text TEXT NOT NULL,
                response TEXT NOT NULL,
                submitted_at TEXT NOT NULL,
                UNIQUE(participant_id, stage, question_key),
                FOREIGN KEY(participant_id) REFERENCES participants(participant_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participant_id TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percentage REAL NOT NULL,
                answers_json TEXT NOT NULL,
                submitted_at TEXT NOT NULL,
                FOREIGN KEY(participant_id) REFERENCES participants(participant_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS module_progress (
                participant_id TEXT NOT NULL,
                module_key TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 1 CHECK(completed IN (0,1)),
                completed_at TEXT NOT NULL,
                PRIMARY KEY(participant_id, module_key),
                FOREIGN KEY(participant_id) REFERENCES participants(participant_id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_questionnaire_stage
                ON questionnaire_responses(stage);
            CREATE INDEX IF NOT EXISTS idx_quiz_participant
                ON quiz_results(participant_id);
            """
        )


def create_participant(data: dict[str, Any]) -> None:
    init_db()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO participants (
                participant_id, age_group, gender, education_level,
                employment_status, previous_training, computer_use,
                consent_given, consent_version, started_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["participant_id"], data["age_group"], data["gender"],
                data["education_level"], data["employment_status"],
                data["previous_training"], data["computer_use"],
                1, data.get("consent_version", "1.0"), utc_now(),
            ),
        )


def participant_exists(participant_id: str) -> bool:
    init_db()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM participants WHERE participant_id = ?",
            (participant_id,),
        ).fetchone()
    return row is not None


def save_questionnaire(
    participant_id: str,
    stage: str,
    responses: dict[str, tuple[str, Any]],
) -> None:
    """Save or update one complete questionnaire atomically."""
    if stage not in {"pre", "post"}:
        raise ValueError("stage must be 'pre' or 'post'")
    now = utc_now()
    with get_connection() as conn:
        for key, (question_text, response) in responses.items():
            conn.execute(
                """
                INSERT INTO questionnaire_responses (
                    participant_id, stage, question_key, question_text,
                    response, submitted_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(participant_id, stage, question_key)
                DO UPDATE SET
                    question_text = excluded.question_text,
                    response = excluded.response,
                    submitted_at = excluded.submitted_at
                """,
                (participant_id, stage, key, question_text, str(response), now),
            )


def questionnaire_completed(participant_id: str, stage: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM questionnaire_responses
            WHERE participant_id = ? AND stage = ?
            """,
            (participant_id, stage),
        ).fetchone()
    return bool(row and row["count"] > 0)


def mark_module_complete(participant_id: str, module_key: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO module_progress (
                participant_id, module_key, completed, completed_at
            ) VALUES (?, ?, 1, ?)
            ON CONFLICT(participant_id, module_key)
            DO UPDATE SET completed = 1, completed_at = excluded.completed_at
            """,
            (participant_id, module_key, utc_now()),
        )


def completed_modules(participant_id: str) -> set[str]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT module_key FROM module_progress
            WHERE participant_id = ? AND completed = 1
            """,
            (participant_id,),
        ).fetchall()
    return {row["module_key"] for row in rows}


def save_quiz_result(
    participant_id: str,
    score: int,
    total: int,
    answers_json: str,
) -> int:
    percentage = round((score / total) * 100, 2) if total else 0.0
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO quiz_results (
                participant_id, score, total, percentage,
                answers_json, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (participant_id, score, total, percentage, answers_json, utc_now()),
        )
        return int(cursor.lastrowid)


def latest_quiz_result(participant_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT * FROM quiz_results
            WHERE participant_id = ?
            ORDER BY submitted_at DESC, id DESC
            LIMIT 1
            """,
            (participant_id,),
        ).fetchone()
    return dict(row) if row else None


def mark_study_complete(participant_id: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE participants SET completed_at = ? WHERE participant_id = ?",
            (utc_now(), participant_id),
        )


def fetch_table(table_name: str) -> list[dict[str, Any]]:
    allowed = {
        "participants", "questionnaire_responses", "quiz_results", "module_progress"
    }
    if table_name not in allowed:
        raise ValueError("Invalid table name")
    with get_connection() as conn:
        rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
    return [dict(row) for row in rows]


def summary_counts() -> dict[str, int]:
    with get_connection() as conn:
        participants = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]
        completed = conn.execute(
            "SELECT COUNT(*) FROM participants WHERE completed_at IS NOT NULL"
        ).fetchone()[0]
        pre = conn.execute(
            "SELECT COUNT(DISTINCT participant_id) FROM questionnaire_responses WHERE stage='pre'"
        ).fetchone()[0]
        post = conn.execute(
            "SELECT COUNT(DISTINCT participant_id) FROM questionnaire_responses WHERE stage='post'"
        ).fetchone()[0]
        quizzes = conn.execute("SELECT COUNT(*) FROM quiz_results").fetchone()[0]
    return {
        "participants": participants,
        "completed": completed,
        "pre_responses": pre,
        "post_responses": post,
        "quiz_attempts": quizzes,
    }
