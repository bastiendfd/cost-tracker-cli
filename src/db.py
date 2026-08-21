"""Local SQLite storage for fictional maintenance costs."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

_configured_database_path: Path | None = None


def configure_database(path: Path) -> None:
    """Set the database path explicitly, primarily for tests and local configuration."""
    global _configured_database_path
    _configured_database_path = Path(path)


def _database_path() -> Path:
    if _configured_database_path is not None:
        return _configured_database_path
    return Path(os.getenv("DB_PATH", "costs.sqlite"))


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(_database_path())


def init_db() -> None:
    """Create or safely upgrade the local schema to integer minor units."""
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0),
            category TEXT NOT NULL DEFAULT 'general',
            date TEXT NOT NULL DEFAULT (date('now'))
        )
        """
    )
    columns = {row[1] for row in connection.execute("PRAGMA table_info(costs)").fetchall()}
    if "amount_cents" not in columns:
        connection.execute("ALTER TABLE costs ADD COLUMN amount_cents INTEGER")
        if "amount" in columns:
            connection.execute("UPDATE costs SET amount_cents = ROUND(amount * 100) WHERE amount_cents IS NULL")
    connection.commit()
    connection.close()
