# Change: Initialize Data Migration Pipeline

## Why

This is the foundational change that establishes the core data migration capabilities for the KPC TMS Data Migration project. The project needs to migrate 522M-783M records from Oracle Database to Salesforce Cloud, requiring:

- High-performance parallel extraction from Oracle
- Data transformation with field mapping
- Bulk loading to Salesforce via Bulk API 2.0
- Comprehensive reconciliation to ensure data integrity

## What Changes

- **NEW** `extraction` capability — Parallel extraction from Oracle with chunking, date partitioning, and configurable batch sizes
- **NEW** `transformation` capability — Field mapping, type conversion, and data preparation for Salesforce
- **NEW** `loading` capability — Salesforce Bulk API 2.0 integration with GZIP compression and parallel uploads
- **NEW** `reconciliation` capability — Count, checksum, and aggregate validation between source and target

## Impact

- **Affected specs:** extraction, transformation, loading, reconciliation (all NEW)
- **Affected code:**
  - `dags/` — Airflow DAG definitions
  - `plugins/` — Custom Airflow operators and hooks
  - `config/` — Table configurations and field mappings
- **Dependencies:** Apache Airflow 3.x, cx_Oracle, pandas, requests

## Design Decisions

See [design.md](design.md) for:

- ETL architecture choices
- Chunking strategy for large tables
- Bulk API 2.0 vs 1.0 trade-offs
- Reconciliation approach

## References

- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — System architecture
- [docs/PIPELINE_DESIGN.md](../../docs/PIPELINE_DESIGN.md) — Detailed pipeline design
- [docs/MIGRATION_CHECKLIST.md](../../docs/MIGRATION_CHECKLIST.md) — Expert checklist
