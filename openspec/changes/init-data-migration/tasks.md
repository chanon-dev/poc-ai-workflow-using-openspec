# Tasks: Init Data Migration

- [x] Oracle Extraction Implementation <!-- id: 0 -->
  - [x] Implement `dags/dag_factory.py` to support Oracle chunking logic <!-- id: 1 -->
  - [x] Implement `include/sql/queries.py` for optimized parallel extraction queries <!-- id: 2 -->
  - [ ] Verify extraction with `KPS_R_POS_SUPPLIER` (small table) <!-- id: 3 --> <!-- requires live Oracle connection -->

- [x] Transformation Implementation <!-- id: 4 -->
  - [x] Implement `plugins/transformers.py` for Pandas-based data mapping <!-- id: 5 -->
  - [x] Implement `config/field_mappings.py` for schema definition <!-- id: 6 -->
  - [ ] Unit test transformation logic with sample data <!-- id: 7 --> <!-- requires test data -->

- [x] Salesforce Loading Implementation <!-- id: 8 -->
  - [x] Implement `plugins/salesforce_bulk_loader.py` wrapper for Bulk API 2.0 <!-- id: 9 -->
  - [x] Configure `config/load_config.py` <!-- id: 10 -->
  - [ ] Verify loading with a test record <!-- id: 11 --> <!-- requires live Salesforce connection -->

- [x] Reconciliation Implementation <!-- id: 12 -->
  - [x] Implement `dags/reconciliation.py` <!-- id: 13 -->
  - [x] Implement `plugins/reconciliation_checks.py` for strategies (Count, Checksum) <!-- id: 14 -->
