"""SQLite layer for FUTURE use. NOT wired into the pages: without real authentication,
a shared database file would mix every visitor's data. Add auth + per-user ids first."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("moneylife.db")


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, user_id TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL)")
    return con
