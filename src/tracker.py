"""Command-line interface for fictional maintenance-cost tracking."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import os
import sys

import click
from rich.console import Console
from rich.table import Table

sys.path.insert(0, os.path.dirname(__file__))
from db import get_connection, init_db

console = Console()


def _to_cents(value: str) -> int:
    try:
        amount = Decimal(value)
    except InvalidOperation as error:
        raise click.BadParameter("must be a decimal number") from error
    if amount < 0:
        raise click.BadParameter("must not be negative")
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _format_euro(amount_cents: int) -> str:
    return f"{Decimal(amount_cents) / Decimal(100):.2f}"


@click.group()
def cli():
    """Track fictional maintenance costs from the terminal."""
    init_db()


@cli.command()
@click.argument("label")
@click.argument("amount")
@click.option("--category", "-c", default="general", show_default=True, help="Cost category")
def add(label: str, amount: str, category: str) -> None:
    """Add a fictional cost entry."""
    amount_cents = _to_cents(amount)
    connection = get_connection()
    connection.execute(
        "INSERT INTO costs (label, amount_cents, category) VALUES (?, ?, ?)",
        (label, amount_cents, category),
    )
    connection.commit()
    connection.close()
    console.print(f"Added: [bold]{label}[/bold] — {_format_euro(amount_cents)} EUR [{category}]")


@cli.command("list")
def list_costs() -> None:
    """List all local cost entries."""
    connection = get_connection()
    rows = connection.execute(
        "SELECT id, date, label, amount_cents, category FROM costs ORDER BY date DESC, id DESC"
    ).fetchall()
    connection.close()
    if not rows:
        console.print("No entries yet. Use 'add' to create one.")
        return

    table = Table(title="Cost Entries")
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Label", style="bold")
    table.add_column("Amount (EUR)", justify="right", style="green")
    table.add_column("Category", style="cyan")
    for row in rows:
        table.add_row(str(row[0]), row[1], row[2], _format_euro(row[3]), row[4])
    console.print(table)


@cli.command()
def summary() -> None:
    """Show local total costs by category."""
    connection = get_connection()
    rows = connection.execute(
        "SELECT category, SUM(amount_cents), COUNT(*) FROM costs GROUP BY category"
    ).fetchall()
    connection.close()
    if not rows:
        console.print("No data yet.")
        return

    table = Table(title="Summary by Category")
    table.add_column("Category", style="cyan")
    table.add_column("Total (EUR)", justify="right", style="green")
    table.add_column("Entries", justify="right")
    for row in rows:
        table.add_row(row[0], _format_euro(row[1]), str(row[2]))
    console.print(table)


if __name__ == "__main__":
    cli()
