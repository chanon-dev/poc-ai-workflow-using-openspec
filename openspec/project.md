# Project Context

## Purpose

**KPC TMS Data Migration** is a high-volume ETL project designed to migrate 2-3 years of historical sales and payment data (~522M - 783M records) from an on-premise Oracle Database to Salesforce. The system uses **Apache Airflow 3.x** with **CeleryExecutor** for on-premise orchestration, leveraging **Salesforce Data Loader CLI** and **Bulk API 2.0** for efficient loading. The pipeline ensures data integrity through automated reconciliation and checksum validation.

## Tech Stack

- **Orchestration**: Apache Airflow 3.x (Docker Compose + CeleryExecutor + Redis)
- **Language**: Python 3.9+ (Pandas for transformation)
- **Source System**: Oracle Database 19c+ (On-Premise) with Parallel Query
- **Target System**: Salesforce (Cloud) via Bulk API 2.0
- **ETL Tools**: Salesforce Data Loader CLI, Python/Pandas
- **Infrastructure**: Docker, Docker Compose, Local NVMe SSD (Staging)
- **Database**: PostgreSQL (Airflow Metadata), Redis (Message Broker)
- **Validation**: Great Expectations, Custom Reconciliation DAGs

## Project Conventions

### Code Style

- **Linter/Formatter**: [Ruff](https://docs.astral.sh/ruff/) (configured in `pyproject.toml`)
  - Target: Python 3.9
  - Line Length: 100
  - Rules: E, W, F, I, C, B, UP, AIR.
- **Type Hinting**: Strongly recommended for all Python code (`List`, `Dict`, `Any`).
- **Configuration**: Use **Pydantic** models for validating configuration objects.

### Architecture Patterns

- **Airflow DAGs**:
  - **TaskFlow API** (`@task`) is the standard for Python-based tasks.
  - **Environment Isolation**: Expensive imports must be inside task definitions.
  - **Variables**: Access via Jinja templates `{{ var.value.x }}` to avoid top-level DB calls.
  - **Idempotency**: All `INSERT` operations must use `ON CONFLICT` or similar mechanisms.
- **Pipeline Strategy**:
  - **Extract**: Oracle Parallel Query with `ROWNUM` chunking (500K records/chunk).
  - **Stage**: Local CSV files with **GZIP** compression.
  - **Load**: Salesforce Bulk API 2.0 with 10-15 concurrent jobs.
  - **Reconcile**: Count comparison + Sample Checksum validation.

### Testing Strategy

- **Unit Tests**: `pytest` for DAG integrity, structure, and logic.
- **Integration Tests**: `docker compose up` to spin up full stack.
- **Self-Check Tasks**: DAGs should include sensors/checks (e.g., `S3KeySensor`) to verify outputs.

### Git Workflow

- Standard feature branch workflow.
- Commit messages should be descriptive.

## Domain Context

- **Migration Scope**: 2-3 Years Historical Data.
- **Critical Objects**:
  - `KPS_T_SALES_MD` -> `KPS_Sales__c` (~261M records/3yrs)
  - `KPS_T_SALESPAY_MD` -> `KPS_SalesPay__c` (~109M records/3yrs)
  - `KPS_T_SALES_M` -> `KPS_SalesM__c` (~108M records/3yrs)
- **Performance Targets**: ~3,000 records/sec throughput.

## Important Constraints

- **Salesforce Limits**:
  - 150MB max file size (GZIP required).
  - 150M records per 24hr rolling limit.
  - Max 100 concurrent jobs (Limit to 15).
- **On-Premise Constraints**:
  - Disk I/O bottleneck on staging (Use NVMe).
  - Network latency between On-Prem Source and Cloud Target.
- **Security**: Credentials managed via Airflow Connections (Secrets Backend).

## External Dependencies

- **Oracle Instant Client**: Required on Airflow workers.
- **Salesforce Data Loader**: Java runtime required.
- **Docker Registry**: Official `apache/airflow:3.x` images.

## Documentation

For detailed specifications, please refer to the documents in the `docs/` directory.
