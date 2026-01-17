# database.py

import sqlite3
from pathlib import Path

DB_PATH = Path("memo_system.db")


def get_connection():
    """
    Opens (or creates) the SQLite DB file memo_system.db.
    Always remember to conn.close() after use.
    """
    conn = sqlite3.connect(DB_PATH)
    # So we get dict-like rows if we want
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create tables if they do not exist yet.
    Run this once at startup (e.g. in business_memo_system.py).
    """
    conn = get_connection()
    cur = conn.cursor()

    # Table for evaluation logs (like evaluation_log.csv)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            topic TEXT NOT NULL,
            revision_cycles INTEGER NOT NULL,
            final_decision TEXT NOT NULL
        )
        """
    )

    # Table for feedback logs (like feedback_log.csv)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            topic TEXT NOT NULL,
            revision_cycles INTEGER NOT NULL,
            rating_1_to_5 INTEGER,
            feedback_text TEXT
        )
        """
    )

    conn.commit()
    conn.close()
