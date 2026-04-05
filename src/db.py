import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "costs.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT 'general',
            date TEXT DEFAULT (date('now'))
        )
    """)
    conn.commit()
    conn.close()