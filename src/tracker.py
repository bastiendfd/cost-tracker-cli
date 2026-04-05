import click
from rich.console import Console
from rich.table import Table
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from db import init_db, get_connection
from models import Cost

console = Console()

@click.group()
def cli():
    """Cost Tracker — track maintenance costs from the terminal."""
    init_db()

@cli.command()
@click.argument("label")
@click.argument("amount", type=float)
@click.option("--category", "-c", default="general", help="Cost category")
def add(label, amount, category):
    """Add a new cost entry."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO costs (label, amount, category) VALUES (?, ?, ?)",
        (label, amount, category)
    )
    conn.commit()
    conn.close()
    console.print(f"✅ Added: [bold]{label}[/bold] — {amount}€ [[cyan]{category}[/cyan]]")

@cli.command("list")
def list_costs():
    """List all cost entries."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, date, label, amount, category FROM costs ORDER BY date DESC"
    ).fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]No entries yet. Use 'add' to create one.[/yellow]")
        return

    table = Table(title="Cost Entries")
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Label", style="bold")
    table.add_column("Amount (€)", justify="right", style="green")
    table.add_column("Category", style="cyan")

    for row in rows:
        table.add_row(str(row[0]), row[1], row[2], f"{row[3]:.2f}", row[4])

    console.print(table)

@cli.command()
def summary():
    """Show total costs by category."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT category, SUM(amount), COUNT(*) FROM costs GROUP BY category"
    ).fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]No data yet.[/yellow]")
        return

    table = Table(title="Summary by Category")
    table.add_column("Category", style="cyan")
    table.add_column("Total (€)", justify="right", style="green")
    table.add_column("Entries", justify="right")

    for row in rows:
        table.add_row(row[0], f"{row[1]:.2f}", str(row[2]))

    console.print(table)

if __name__ == "__main__":
    cli()