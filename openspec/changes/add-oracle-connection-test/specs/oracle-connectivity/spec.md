## ADDED Requirements

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

---

### Requirement: Oracle Health Check

The system SHALL provide a health check to verify Oracle connectivity.

#### Scenario: Successful health check

- **GIVEN** valid Oracle credentials in Airflow connection
- **WHEN** health_check() is called
- **THEN** it executes `SELECT 1 FROM DUAL`
- **AND** returns True with database version info

#### Scenario: Failed health check

- **GIVEN** invalid Oracle credentials or network issue
- **WHEN** health_check() is called
- **THEN** it returns False with error details
- **AND** does not raise an exception (graceful failure)

---

### Requirement: Table Access Verification

The system SHALL verify read permissions on migration tables.

#### Scenario: Check table permissions

- **GIVEN** a list of table names to verify
- **WHEN** verify_table_access() is called
- **THEN** it checks SELECT permission on each table
- **AND** returns a dict with table_name → accessible (bool)

#### Scenario: Missing table permission

- **GIVEN** a table the user cannot access
- **WHEN** verify_table_access() is called
- **THEN** that table is marked as accessible=False
- **AND** the error reason is included in the result

---

### Requirement: Oracle Connection Test DAG

The system SHALL provide a DAG for manual connection testing.

#### Scenario: Run connection test

- **GIVEN** the DAG `test_oracle_connection` exists
- **WHEN** triggered manually
- **THEN** it runs health check, table access verification, and sample query
- **AND** reports results in task logs

#### Scenario: Test DAG structure

- **GIVEN** the test DAG
- **WHEN** parsed by Airflow
- **THEN** it has tasks: `check_connection`, `verify_tables`, `run_sample_query`
- **AND** schedule is set to None (manual trigger only)
