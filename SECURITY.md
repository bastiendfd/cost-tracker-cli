# Security Policy

Cost Tracker CLI is a local educational tool, not accounting or production software.

## Do not commit

- real cost records, invoices, customer data or ERP exports;
- credentials, API keys, tokens or private keys;
- local SQLite database files.

## Storage

The local database path can be set with `DB_PATH`. Database files are ignored by Git by default. Use a location and access controls appropriate to your own environment.

## Reporting

Do not publish sensitive details in public issues. Use private GitHub security reporting once configured.
