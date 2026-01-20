# Change: Add Oracle Connection Test DAG and Service

## Why

Before running data migration, we need a reliable way to:

1. Verify Oracle database connectivity
2. Validate credentials and permissions
3. Test network connectivity from Airflow workers
4. Provide a reusable Oracle connection service following Airflow best practices

## What Changes

- **NEW** `oracle-connectivity` capability — Oracle connection service and test DAG
  - **Callable Service Layer** — OracleService as single entry point for all Oracle operations
  - **Service Interface Methods** — Standardized API: `get_connection()`, `execute_query()`, `get_pandas_df()`, `health_check()`, etc.
  - Health check functionality (SELECT 1 FROM DUAL + version)
  - Table access verification
  - Test DAG for manual connection verification
  - Thick/Thin mode support with multi-architecture (x64/ARM64)

## Impact

- **Affected specs:** oracle-connectivity (NEW)
- **Affected code:**
  - `plugins/oracle_service.py` — Connection service (central abstraction)
  - `plugins/oracle_extractor.py` — Should use OracleService (not OracleHook)
  - `dags/test_oracle_connection_dag.py` — Test DAG
- **Dependencies:** oracledb

## References

- [docs/AIRFLOW_BEST_PRACTICES.md](../../docs/AIRFLOW_BEST_PRACTICES.md) — Connection handling
- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — Oracle connection setup
