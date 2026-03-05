import os
import sqlite3
from werkzeug.security import generate_password_hash


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_plain TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
"""


def init_db(db_path: str):
    # Ensure instance/ directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table
    cur.executescript(SCHEMA_SQL)

    # Seed users (plaintext for vulnerable login, hashed for secure login)
    users = [
        ("admin", "adminpass", generate_password_hash("adminpass"), "admin"),
        ("alice", "password123", generate_password_hash("password123"), "user"),
    ]

    for username, pw_plain, pw_hash, role in users:
        cur.execute(
            """
            INSERT OR IGNORE INTO users
            (username, password_plain, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (username, pw_plain, pw_hash, role),
        )

    conn.commit()
    conn.close()
