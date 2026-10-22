"""
LawAI Advisor - Database Layer (SQLite)
Comprehensive schema management, migrations, and query helpers.
"""

import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent

if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/lawai.db"
else:
    DB_PATH = os.environ.get("LAWAI_DB") or str(BASE_DIR / "lawai.db")


def get_db():
    con = sqlite3.connect(DB_PATH, timeout=20)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_db():
    with closing(get_db()) as con, con:
        # 1. Users table
        con.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL DEFAULT 'User',
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                reset_token TEXT,
                reset_token_expiry TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

        # Migration helper for users table in case it was created without full_name
        try:
            con.execute("ALTER TABLE users ADD COLUMN full_name TEXT NOT NULL DEFAULT 'User'")
        except sqlite3.OperationalError:
            pass  # Already exists

        try:
            con.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            con.execute("ALTER TABLE users ADD COLUMN reset_token_expiry TIMESTAMP")
        except sqlite3.OperationalError:
            pass

        # 2. Consultations table
        con.execute(
            """CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                incident_date TEXT,
                incident_location TEXT,
                jurisdiction TEXT DEFAULT 'India',
                involved_parties TEXT,
                desired_outcome TEXT,
                is_ongoing INTEGER DEFAULT 0,
                immediate_danger INTEGER DEFAULT 0,
                evidence_summary TEXT,
                raw_description TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                situation_summary TEXT,
                legal_assessment TEXT,
                applicable_laws TEXT,
                recommended_solution TEXT,
                immediate_actions TEXT,
                step_by_step_plan TEXT,
                evidence_checklist TEXT,
                escalation_options TEXT,
                risks_deadlines TEXT,
                suggested_next_move TEXT,
                disclaimer TEXT,
                raw_full_text TEXT,
                private_notes TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )"""
        )

        # 3. Action Items table
        con.execute(
            """CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consultation_id INTEGER NOT NULL,
                step_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                explanation TEXT,
                where_to_act TEXT,
                required_evidence TEXT,
                verified_deadline TEXT,
                contingency TEXT,
                status TEXT DEFAULT 'pending',
                completed_at TIMESTAMP,
                FOREIGN KEY(consultation_id) REFERENCES consultations(id) ON DELETE CASCADE
            )"""
        )

        # 4. Draft Documents table
        con.execute(
            """CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                consultation_id INTEGER,
                doc_type TEXT NOT NULL,
                title TEXT NOT NULL,
                recipient_name TEXT,
                recipient_org TEXT,
                dispute_amount TEXT,
                draft_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(consultation_id) REFERENCES consultations(id) ON DELETE SET NULL
            )"""
        )

        # 5. Follow-up consultation messages
        con.execute(
            """CREATE TABLE IF NOT EXISTS follow_up_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consultation_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )"""
        )


init_db()

