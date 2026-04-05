\# Cost Tracker CLI



A command-line tool to track and analyze maintenance costs, built with Python and SQLite.



\## Features

\- Add cost entries with label, amount and category

\- List all entries in a formatted table

\- Summary view grouped by category



\## Tech Stack

!\[Python](https://img.shields.io/badge/Python-3.x-blue)

!\[SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)

!\[Click](https://img.shields.io/badge/CLI-Click-green)



\## Installation

```bash

git clone https://github.com/bastiendfd/cost-tracker-cli.git

cd cost-tracker-cli

pip install -r requirements.txt

```



\## Usage

```bash

\# Add a cost entry

python src/tracker.py add "Engine inspection" 1200 --category maintenance



\# List all entries

python src/tracker.py list



\# Summary by category

python src/tracker.py summary

```



\## Project Structure

```

cost-tracker-cli/

├── src/

│   ├── db.py        # SQLite connection and schema

│   ├── models.py    # Cost dataclass

│   └── tracker.py   # CLI commands (Click)

├── tests/

│   └── test\_tracker.py

└── requirements.txt

```

