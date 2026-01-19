# Project Context

## Purpose

KPC TMS Data Migration project for migrating historical transaction data from Oracle Database (On-Premise) to Salesforce (Cloud). The migration handles 2-3 years of historical data (~522M-783M total records) from 16 source tables, with the largest tables containing 87M+ records/year.

**Key Goals:**

- Migrate all KPC TMS transactional data to Salesforce
- Maintain data integrity through reconciliation checks
- Optimize for large-volume batch processing (Bulk API 2.0)
- Enable parallel extraction and loading for performance

## Tech Stack

### Orchestration

- **Apache Airflow 3.x** — CeleryExecutor for parallel task execution
- **Redis** — Celery message broker
- **PostgreSQL** — Airflow metadata database

### Source & Target Systems

- **Source:** Oracle Database (On-Premise)
- **Target:** Salesforce (Cloud) via Bulk API 2.0
- **ETL Tool:** Salesforce Data Loader CLI

### Runtime & Development

- **Python 3.9+** — Primary language for DAGs and plugins
- **Docker & Docker Compose** — Container runtime
- **pandas** — Data transformation
- **cx_Oracle** — Oracle database driver

### Data Quality

- **Great Expectations** — Data validation framework

## Project Conventions

### Code Style

- **Linter/Formatter:** [ruff](https://docs.astral.sh/ruff/) (v0.1.14+)
- **Line length:** 100 characters
- **Quote style:** Double quotes
- **Indent:** Spaces (4)
- **Rules enabled:** pycodestyle (E, W), pyflakes (F), isort (I), convention (C), bugbear (B), pyupgrade (UP), Airflow-specific (AIR)

Run with:

```bash
ruff check dags/
ruff format dags/
```

### Pre-commit Hooks

- ruff (lint + format)
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-added-large-files

### Naming Conventions

- DAG files: `dag_<purpose>.py` or `<table_name>_dag.py`
- DAG IDs: `snake_case` (e.g., `migrate_kps_t_sales_md`)
- Task IDs: `snake_case` verbs (e.g., `extract_chunk`, `load_to_salesforce`)
- Config files: `<purpose>_config.py`

### Architecture Patterns

1. **TaskFlow API** — Preferred pattern for task definitions in Airflow 3.x
2. **DAG Factory Pattern** — Auto-generate DAGs for similar table migrations
3. **Master DAG + Child DAGs** — Master orchestrates table-specific migration DAGs
4. **Chunking Pattern** — Large tables (>100M records) split into 500K-record chunks
5. **Parallel Workers** — CeleryExecutor with 3-5 workers for concurrent processing

### Key Design Decisions

- Use Bulk API 2.0 (not 1.0) for faster, simplified loading
- GZIP compression for CSV uploads to Salesforce
- Idempotent upserts via External ID fields
- Date-based partitioning for incremental loads

### Testing Strategy

1. **DAG Syntax Check:** `python dags/<dag_file>.py`
2. **Parse Time:** `time python dags/<dag_file>.py` (keep <5 seconds)
3. **Unit Tests:** pytest with DagBag assertions
4. **Mock Variables/Connections:** Use `AIRFLOW_VAR_*` and `AIRFLOW_CONN_*` env vars
5. **Dry Runs:** `--conf '{"sample_percent": 1, "dry_run": true}'` for test migrations

### Git Workflow

- **Default branch:** `main`
- **Pre-commit hooks:** Required before pushing
- Run `pre-commit install` to enable hooks

## Domain Context

### Data Volume Summary

| Table | Records/Year | 2-3 Years Total | Priority |
|-------|--------------|-----------------|----------|
| KPS_T_SALES_MD | 87M | 174M-261M | Critical |
| KPS_T_SALESPAY_MD | 36M | 73M-109M | Critical |
| KPS_T_SALES_M | 36M | 72M-108M | Critical |
| Others (13 tables) | <500K each | <1.5M total | Low-Medium |

### Salesforce Objects

- Source tables map to custom Salesforce objects (`KPS_Sales__c`, `KPS_SalesPay__c`, etc.)
- Each object has an `External_ID__c` field for upsert operations

### Migration Phases

1. Reference Data (no dependencies)
2. Pre-Invoice tables
3. Pre-Invoice Details (depends on Phase 2)
4. Main Sales tables
5. Sales Details
6. Sales Payment
7. Supporting tables

## Important Constraints

### Salesforce Limits

| Limit | Value |
|-------|-------|
| Daily Bulk API requests | 15,000 |
| Records per 24hr | 150,000,000 |
| Concurrent jobs | 100 (use 15 to be safe) |
| File size per upload | 150MB |

### Infrastructure Requirements

- **Staging Storage:** ~500GB NVMe SSD recommended
- **Multiple Celery Workers:** 3-5 workers for parallel processing
- **Oracle Instant Client:** Required on Airflow workers

### Performance Targets

- Throughput: ~3,000 records/second
- Largest table (261M records): <24 hours
- Parallel jobs: 10-15 concurrent Bulk API jobs

### Audit & Compliance

- All migrations must log to `MIGRATION_AUDIT_LOG` table
- Failed records tracked in `MIGRATION_FAILED_RECORDS` table
- Reconciliation (count + aggregate validation) is mandatory

## External Dependencies

### Connections (Airflow)

- `oracle_kpc` — Oracle Database connection
- `salesforce_prod` — Salesforce production org

### Key Airflow Variables

- `MIGRATION_CHUNK_SIZE` — Records per chunk (default: 500000)
- `STAGING_PATH` — Path for staging CSV files
- `DATALOADER_PATH` — Salesforce Data Loader CLI path
- `ALERT_EMAIL` — Notification email address
- `SALESFORCE_BATCH_SIZE` — Bulk API batch size (default: 10000)

### Reference Documentation

See the `docs/` directory for detailed specifications:

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — System architecture and DAG designs
- [PIPELINE_DESIGN.md](docs/PIPELINE_DESIGN.md) — Complete pipeline implementation details
- [MIGRATION_CHECKLIST.md](docs/MIGRATION_CHECKLIST.md) — Pre/during/post migration checklists
- [AIRFLOW_BEST_PRACTICES.md](docs/AIRFLOW_BEST_PRACTICES.md) — Airflow coding standards
- [GREAT_EXPECTATIONS_GUIDE.md](docs/GREAT_EXPECTATIONS_GUIDE.md) — Data validation setup
