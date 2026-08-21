# Cost Tracker CLI

> A local Python and SQLite command-line tool for **fictional maintenance-cost** tracking.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-local-003B57?logo=sqlite)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC)

## What it demonstrates

- local SQLite persistence;
- CLI design with Click;
- maintenance-cost categories;
- integer minor-unit storage for financial values;
- reproducible tests across database connections.

## Run locally

```bash
git clone https://github.com/bastiendfd/cost-tracker-cli.git
cd cost-tracker-cli

python -m venv .venv
# Windows Git Bash
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
```

## Usage

```bash
# Use a local database path explicitly.
DB_PATH=demo-costs.sqlite .venv/Scripts/python.exe src/tracker.py add "Demo pump inspection" 1200.50 --category maintenance

DB_PATH=demo-costs.sqlite .venv/Scripts/python.exe src/tracker.py list
DB_PATH=demo-costs.sqlite .venv/Scripts/python.exe src/tracker.py summary
```

Amounts are converted from decimal input to integer cents before SQLite storage. Negative amounts are rejected by the CLI.

## Data boundary

This project is a learning/portfolio tool. Use only fictional or explicitly authorised local data.

- Local SQLite files are ignored by Git.
- Do not commit cost records, customer information, invoices, ERP exports, credentials or secrets.
- This is not accounting software and should not be used as a system of record.

## Test command

```bash
python -m pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
