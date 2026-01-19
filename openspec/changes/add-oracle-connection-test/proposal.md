# Change: Add Oracle Connection Test DAG and Service

## Why

Before running data migration, we need a reliable way to:

1. Verify Oracle database connectivity
2. Validate credentials and permissions
3. Test network connectivity from Airflow workers
4. Provide a reusable Oracle connection service following Airflow best practices

## What Changes

- **NEW** `oracle-connectivity` capability — Oracle connection service and test DAG
  - Oracle connection service with connection pooling
  - Health check functionality
  - Test DAG for manual connection verification
  - Permission validation for migration tables

## Impact

- **Affected specs:** oracle-connectivity (NEW)
- **Affected code:**
  - `plugins/oracle_service.py` — Connection service
  - `dags/test_oracle_connection_dag.py` — Test DAG
- **Dependencies:** cx_Oracle, Apache Airflow OracleProvider

## References

- [docs/AIRFLOW_BEST_PRACTICES.md](../../docs/AIRFLOW_BEST_PRACTICES.md) — Connection handling
- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — Oracle connection setup
