# Design: Init Data Migration

## Architecture

The migration architecture follows a standard ETL pattern orchestrated by **Apache Airflow 3.x** on-premise.

### High-Level Flow

1. **Extract**: Airflow Celery Workers connect to Oracle (On-Prem). Large tables are thoroughly chunked using `ROWNUM` and Oracle Parallel Query Hints (`/*+ PARALLEL(t, 8) */`) to maximize throughput.
2. **Stage**: Data is written to local NVMe SSDs in CSV format and GZIP compressed to minimize I/O and network transfer size.
3. **Load**:
    - Compressed CSVs are uploaded to Salesforce using **Bulk API 2.0**.
    - Jobs are managed in parallel (up to 15 concurrent jobs) to optimize Salesforce throughput.
4. **Reconcile**:
    - Post-migration verification runs to compare record counts.
    - Sample-based checksums are calculated for data integrity verification.

## Implementation Details

### DAG Structure

- **Master DAG**: Triggers dependent DAGs in phases (Reference/Small tables -> Large Sales tables).
- **DAG Factory**: A `dag_factory.py` script checks a configuration file (`config/tables_config.py`) and generates a DAG for each table automatically, ensuring consistency.
- **TaskFlow API**: adoption of Airflow 2.x/3.x `@task` decorator for cleaner Python code.

### Error Handling

- **Idempotency**: All `UPSERT` operations use `External_ID__c` to prevent duplicates on retries.
- **Retry Logic**: Airflow tasks are configured with retries for transient network issues.
- **Dead Letter Queue**: Failed records are logged to a specific error table or file for manual review.

## Alternatives Considered

- **Salesforce Data Loader GUI**: Rejected due to lack of automation and inability to handle parallel chunking effectively.
- **MuleSoft**: Rejected due to high licensing costs and complexity for a one-time historical migration.
- **Heroku Connect**: Rejected as it is better suited for continuous sync rather than bulk historical migration.

## Risks

- **Salesforce Limits**: Hitting the 150M records/24hr limit. Mitigation: Split migration over multiple days.
- **Network Latency**: Slow upload speeds from On-Prem to Cloud. Mitigation: GZIP compression and parallel uploads.
- **Disk I/O**: Staging area bottlenecks. Mitigation: Use high-speed NVMe SSDs for `data/staging`.
