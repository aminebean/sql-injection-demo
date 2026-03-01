import os
import sqlite3
from werkzeug.security import generate_password_hash

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
"""

def init_db(db_path: str):
    # Ensure the instance/ folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript(SCHEMA_SQL)

    # Seed users (only inserts if they don't already exist)
    users = [
        ("admin", generate_password_hash("adminpass"), "admin"),
        ("alice", generate_password_hash("password123"), "user"),
    ]

    for username, pw_hash, role in users:
        cur.execute(
            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, pw_hash, role),
        )

    conn.commit()
    conn.close()
