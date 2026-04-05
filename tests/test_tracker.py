import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ["DB_PATH"] = ":memory:"

from db import init_db, get_connection

class TestDatabase(unittest.TestCase):

    def setUp(self):
        init_db()

    def test_init_db_creates_table(self):
        conn = get_connection()
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        conn.close()
        self.assertIn(("costs",), tables)

    def test_insert_and_retrieve(self):
        conn = get_connection()
        conn.execute(
            "INSERT INTO costs (label, amount, category) VALUES (?, ?, ?)",
            ("Engine check", 1200.0, "maintenance")
        )
        conn.commit()
        rows = conn.execute("SELECT label, amount FROM costs").fetchall()
        conn.close()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "Engine check")
        self.assertEqual(rows[0][1], 1200.0)

if __name__ == "__main__":
    unittest.main()