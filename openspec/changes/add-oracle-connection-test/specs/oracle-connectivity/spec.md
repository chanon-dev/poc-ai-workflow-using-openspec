# Oracle Connectivity Specification

## ADDED Requirements

### Requirement: Callable Service Layer

The system SHALL provide OracleService as the **single entry point** for all Oracle database operations, following the Service Layer pattern.

#### Scenario: Service instantiation

- **GIVEN** a plugin or DAG needs to interact with Oracle
- **WHEN** it creates an `OracleService` instance
- **THEN** it passes only the Airflow connection ID
- **AND** the service handles all connection details internally
- **AND** no raw connection objects are exposed

#### Scenario: Dependency injection for testing

- **GIVEN** a plugin depends on OracleService
- **WHEN** unit tests are written
- **THEN** OracleService can be mocked or stubbed
- **AND** tests do not require actual Oracle connection

#### Scenario: OracleExtractor uses OracleService

- **GIVEN** `oracle_extractor.py` needs to query Oracle
- **WHEN** it extracts data
- **THEN** it uses `OracleService` (not `OracleHook` directly)
- **AND** connection management is delegated to OracleService

#### Scenario: Consistent error handling

- **GIVEN** any Oracle operation fails
- **WHEN** OracleService catches the exception
- **THEN** it logs the error with context (conn_id, operation, timeout)
- **AND** returns a typed result object (not raw exception)
- **AND** the caller decides how to handle the failure

---

### Requirement: Service Interface Methods

The OracleService SHALL expose these public methods as the API contract.

#### Scenario: Query execution methods

- **GIVEN** a caller needs to query Oracle
- **WHEN** they use OracleService
- **THEN** these methods are available:
  - `get_connection()` — Context manager for raw connection
  - `execute_query(query, params)` — Returns list of tuples
  - `execute_query_with_columns(query, params)` — Returns dict with columns and rows
  - `get_pandas_df(query, params)` — Returns pandas DataFrame

#### Scenario: Health and diagnostics

- **GIVEN** a caller needs to verify connectivity
- **WHEN** they use OracleService
- **THEN** these methods are available:
  - `health_check()` — Returns HealthCheckResult
  - `verify_table_access(tables)` — Returns dict of TableAccessResult
  - `run_sample_query(table, limit)` — Returns sample data dict

#### Scenario: Metadata operations

- **GIVEN** a caller needs table metadata
- **WHEN** they use OracleService
- **THEN** these methods are available:
  - `get_table_columns(table_name)` — Returns list of column names
  - `get_record_count(table_name, where_clause)` — Returns integer count

---

### Requirement: Oracle Connection Service

The system SHALL provide a reusable Oracle connection service following Airflow best practices.

#### Scenario: Get connection from Airflow

- **GIVEN** an Airflow connection ID `oracle_kpc` is configured
- **WHEN** the connection service is instantiated
- **THEN** it retrieves credentials from Airflow Connections (not hardcoded)
- **AND** credentials are never logged or exposed

#### Scenario: Connection timeout handling

- **GIVEN** a connection timeout is configured (default 30 seconds)
- **WHEN** the database is unreachable
- **THEN** the connection attempt fails with a clear timeout error
- **AND** the error message includes the connection ID and timeout duration

#### Scenario: DSN format support

- **GIVEN** an Airflow connection with Oracle details
- **WHEN** the connection is established
- **THEN** it supports Service Name format: `host:port/service_name`
- **AND** it supports SID format via `extra.sid` field
- **AND** Service Name is read from `schema` field or `extra.service_name`

---

### Requirement: Oracle Client Mode Support

The system SHALL support both thin and thick Oracle client modes.

#### Scenario: Thick mode initialization

- **GIVEN** Oracle Instant Client is installed at `/opt/oracle/instantclient`
- **WHEN** the oracle_service module is loaded
- **THEN** it initializes oracledb in thick mode
- **AND** logs "Oracle Client initialized (thick mode)"

#### Scenario: Fallback to thin mode

- **GIVEN** Oracle Instant Client is NOT installed
- **WHEN** the oracle_service module is loaded
- **THEN** it falls back to thin mode gracefully
- **AND** logs a warning about the fallback

#### Scenario: Password verifier support

- **GIVEN** Oracle database uses older password verifier (type 0x939)
- **WHEN** thick mode is enabled
- **THEN** authentication succeeds
- **AND** thin mode would fail with DPY-3015 error

---

### Requirement: Multi-Architecture Support

The system SHALL support multiple CPU architectures for Oracle Instant Client.

#### Scenario: ARM64 architecture (Apple Silicon, AWS Graviton)

- **GIVEN** Docker image is built on ARM64 platform
- **WHEN** `uname -m` returns `aarch64`
- **THEN** symlink `/opt/oracle/instantclient` points to `instantclient-arm64`

#### Scenario: x86_64 architecture (Intel, AMD)

- **GIVEN** Docker image is built on x86_64 platform
- **WHEN** `uname -m` returns `x86_64`
- **THEN** symlink `/opt/oracle/instantclient` points to `instantclient-x64`

#### Scenario: Architecture detection at build time

- **GIVEN** both `instantclient-x64` and `instantclient-arm64` folders exist
- **WHEN** Docker image is built
- **THEN** architecture is detected automatically via `uname -m`
- **AND** correct Oracle Instant Client is selected

---

### Requirement: Oracle Health Check

The system SHALL provide a health check to verify Oracle connectivity.

#### Scenario: Successful health check

- **GIVEN** valid Oracle credentials in Airflow connection
- **WHEN** health_check() is called
- **THEN** it executes `SELECT 1 FROM DUAL`
- **AND** returns HealthCheckResult with `healthy=True`
- **AND** includes Oracle database version from `v$version`

#### Scenario: Failed health check

- **GIVEN** invalid Oracle credentials or network issue
- **WHEN** health_check() is called
- **THEN** it returns HealthCheckResult with `healthy=False`
- **AND** includes error details in `error` field
- **AND** does not raise an exception (graceful failure)

#### Scenario: Unexpected query result

- **GIVEN** connection succeeds but query returns unexpected result
- **WHEN** `SELECT 1 FROM DUAL` returns None or non-1 value
- **THEN** returns `healthy=False` with "Unexpected result" error

---

### Requirement: Table Access Verification

The system SHALL verify read permissions on migration tables.

#### Scenario: Check table permissions

- **GIVEN** a list of table names to verify
- **WHEN** verify_table_access() is called
- **THEN** it executes `SELECT * FROM {table} WHERE ROWNUM = 1` on each table
- **AND** returns dict mapping table_name to TableAccessResult

#### Scenario: All tables accessible

- **GIVEN** user has SELECT permission on all tables
- **WHEN** verify_table_access() is called
- **THEN** all TableAccessResult have `accessible=True`

#### Scenario: Missing table permission

- **GIVEN** a table the user cannot access (ORA-00942)
- **WHEN** verify_table_access() is called
- **THEN** that table has `accessible=False`
- **AND** the Oracle error is included in `error` field

#### Scenario: Connection-level failure

- **GIVEN** database connection fails
- **WHEN** verify_table_access() is called
- **THEN** all tables are marked `accessible=False`
- **AND** error message indicates connection failure

---

### Requirement: Sample Query Execution

The system SHALL provide sample query execution for data verification.

#### Scenario: Successful sample query

- **GIVEN** a valid table name and limit
- **WHEN** run_sample_query(table_name, limit) is called
- **THEN** returns dict with `success=True`
- **AND** includes `columns` list from `all_tab_columns`
- **AND** includes `total_count` from `COUNT(*)`
- **AND** includes `sample_data` with up to `limit` rows

#### Scenario: Failed sample query

- **GIVEN** an inaccessible table or query error
- **WHEN** run_sample_query() is called
- **THEN** returns dict with `success=False`
- **AND** includes `error` field with failure details

---

### Requirement: Oracle Connection Test DAG

The system SHALL provide a DAG for manual connection testing.

#### Scenario: DAG configuration

- **GIVEN** the DAG `test_oracle_connection` exists
- **WHEN** parsed by Airflow
- **THEN** it has `schedule=None` (manual trigger only)
- **AND** has tags: `test`, `oracle`, `connectivity`
- **AND** has `catchup=False`

#### Scenario: Task chain execution

- **GIVEN** the DAG is triggered
- **WHEN** execution starts
- **THEN** tasks run in order: `check_connection` >> `verify_tables` >> `run_sample_query`

#### Scenario: check_connection task

- **GIVEN** the task runs
- **WHEN** health check passes
- **THEN** logs "Connection successful!" with Oracle version
- **AND** returns health check result dict

#### Scenario: check_connection failure

- **GIVEN** health check fails
- **WHEN** the task runs
- **THEN** raises AirflowException with error details
- **AND** DAG run is marked as failed

#### Scenario: verify_tables task

- **GIVEN** tables are configured in `config/tables_config.py`
- **WHEN** the task runs
- **THEN** verifies all configured migration tables
- **AND** logs "Table access verification: X/Y accessible"
- **AND** raises AirflowException if any table is inaccessible

#### Scenario: run_sample_query task

- **GIVEN** tables have different priorities
- **WHEN** the task runs
- **THEN** selects one table per priority level for testing
- **AND** logs total records, column count, sample rows for each
- **AND** raises AirflowException if any query fails

---

### Requirement: Data Classes

The system SHALL use typed data classes for structured results.

#### HealthCheckResult

```python
@dataclass
class HealthCheckResult:
    healthy: bool
    version: str | None = None
    error: str | None = None
```

#### TableAccessResult

```python
@dataclass
class TableAccessResult:
    table_name: str
    accessible: bool
    error: str | None = None
```

---

### Requirement: Dockerfile Configuration

The system SHALL configure Oracle Instant Client in Docker.

#### Scenario: Dependencies installation

- **GIVEN** Dockerfile builds
- **WHEN** apt-get runs
- **THEN** installs `libaio1` for Oracle Client

#### Scenario: Oracle Instant Client installation

- **GIVEN** `files/instantclient-basic-linux-x64/` and `files/instantclient-basic-linux-arm64/` exist
- **WHEN** Docker image builds
- **THEN** both are copied to `/opt/oracle/`
- **AND** symlink is created based on architecture

#### Scenario: Environment variables

- **GIVEN** Oracle Instant Client is installed
- **WHEN** container runs
- **THEN** `LD_LIBRARY_PATH=/opt/oracle/instantclient`
- **AND** `ORACLE_HOME=/opt/oracle/instantclient`

---

## Implementation Files

| File                                 | Purpose                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `plugins/oracle_service.py`          | OracleService class with health check, table verification, sample query |
| `dags/test_oracle_connection_dag.py` | Test DAG with 3 tasks for manual connection testing                     |
| `dags/config/tables_config.py`       | Migration table configuration                                           |
| `tests/test_oracle_service.py`       | Unit tests for OracleService                                            |
| `Dockerfile`                         | Oracle Instant Client installation with multi-arch support              |
| `requirements.txt`                   | oracledb dependency                                                     |

---

## Airflow Connection Configuration

Connection ID: `oracle_kpc`

| Field           | Value              | Description                              |
| --------------- | ------------------ | ---------------------------------------- |
| Connection Type | Oracle             | Or Generic                               |
| Host            | `<oracle-host>`    | Database server hostname                 |
| Schema          | `<service-name>`   | Oracle Service Name                      |
| Login           | `<username>`       | Database username                        |
| Password        | `<password>`       | Database password                        |
| Port            | `1521`             | Oracle listener port                     |
| Extra           | `{"sid": "ORCL"}`  | Optional: Use SID instead of Service Name|
