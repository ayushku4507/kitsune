import os
import sqlite3
from pathlib import Path
from .config import settings

def connect():
    path = Path(settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL CHECK(role IN ('user','assistant')),
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')

def add_message(role: str, content: str):
    with connect() as db:
        db.execute("INSERT INTO messages(role, content) VALUES (?, ?)", (role, content))

def get_messages(limit: int = 30):
    with connect() as db:
        rows = db.execute("SELECT role, content, created_at FROM messages ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) for row in reversed(rows)]

def add_memory(content: str):
    with connect() as db:
        cur = db.execute("INSERT INTO memories(content) VALUES (?)", (content,))
        return cur.lastrowid

def get_memories():
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT id, content, created_at FROM memories ORDER BY id DESC")]
