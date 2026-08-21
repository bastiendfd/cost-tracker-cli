import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from click.testing import CliRunner

from db import configure_database, get_connection, init_db
from tracker import cli


@pytest.fixture
def database_path(tmp_path):
    path = tmp_path / "costs.sqlite"
    configure_database(path)
    init_db()
    return path


def test_database_persists_entries_across_connections(database_path):
    first = get_connection()
    first.execute(
        "INSERT INTO costs (label, amount_cents, category) VALUES (?, ?, ?)",
        ("Demo inspection", 120_050, "maintenance"),
    )
    first.commit()
    first.close()

    second = get_connection()
    row = second.execute("SELECT label, amount_cents FROM costs").fetchone()
    second.close()

    assert row == ("Demo inspection", 120_050)


def test_database_uses_integer_minor_units(database_path):
    connection = get_connection()
    columns = connection.execute("PRAGMA table_info(costs)").fetchall()
    connection.close()

    assert "amount_cents" in {column[1] for column in columns}


def test_cli_add_converts_decimal_amount_to_minor_units(database_path):
    result = CliRunner().invoke(cli, ["add", "Demo filter", "12.34", "--category", "parts"])

    assert result.exit_code == 0
    connection = get_connection()
    row = connection.execute("SELECT amount_cents, category FROM costs").fetchone()
    connection.close()
    assert row == (1234, "parts")
