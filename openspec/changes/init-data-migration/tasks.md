# Tasks: Initialize Data Migration Pipeline

## 1. Project Structure Setup

- [x] 1.1 Create `dags/` directory structure
- [x] 1.2 Create `plugins/` directory for Airflow plugins
- [x] 1.3 Create `config/` directory for configurations

## 2. Oracle Extraction

- [x] 2.1 Create `config/tables_config.py` with table definitions
- [x] 2.2 Create `config/extract_config.py` with chunking settings
- [x] 2.3 Create `plugins/oracle_extractor.py` with parallel extraction logic
- [x] 2.4 Write unit tests for extraction functions

## 3. Data Transformation

- [x] 3.1 Create `config/field_mappings.py` with Oracle→SF mappings
- [x] 3.2 Create `plugins/transformers.py` with type conversion functions
- [x] 3.3 Write unit tests for transformation functions

## 4. Salesforce Loading

- [x] 4.1 Create `plugins/salesforce_bulk_loader.py` with Bulk API 2.0 client
- [x] 4.2 Implement GZIP compression for uploads
- [x] 4.3 Implement parallel job execution
- [x] 4.4 Write unit tests for loader functions

## 5. Reconciliation

- [x] 5.1 Create `plugins/reconciliation.py` with validation logic
- [x] 5.2 Implement count comparison
- [x] 5.3 Implement aggregate validation
- [x] 5.4 Implement sample checksum validation
- [x] 5.5 Write unit tests for reconciliation functions

## 6. DAG Implementation

- [x] 6.1 Create `dags/dag_factory.py` for auto-generating table DAGs
- [x] 6.2 Create `dags/migration_master_dag.py` for orchestration
- [x] 6.3 Create `dags/reconciliation_dag.py` for validation
- [ ] 6.4 Test DAG syntax with `python dags/<file>.py`

## 7. Verification

- [ ] 7.1 Run `ruff check dags/ plugins/` for linting
- [ ] 7.2 Run unit tests with `pytest tests/`
- [ ] 7.3 Validate DAG loading with DagBag test
- [ ] 7.4 Dry run with sample data (1% of smallest table)

## Dependencies

- Tasks 2.x, 3.x, 4.x, 5.x can run in parallel
- Task 6.x depends on completion of 2.x, 3.x, 4.x, 5.x
- Task 7.x depends on all previous tasks

## Summary

**Completed:** 23/27 tasks (85%)

**Remaining:** Verification tasks require environment setup (Python, pytest, ruff, Airflow)
