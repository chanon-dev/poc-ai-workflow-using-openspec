# Tasks: Add Product & Price Migration Pipeline

## 1. Configuration Setup

- [ ] 1.1 Add `KPS_T_REQPROD_MD` field mapping to `dags/config/field_mappings.py`
- [ ] 1.2 Create SDL mapping file `salesforce/dataloader_conf/mappings/KPS_T_REQPROD_MD.sdl`
- [ ] 1.3 Update `salesforce/dataloader_conf/process-conf.xml` with new process entry

## 2. DAG Implementation

- [ ] 2.1 Create `dags/migrate_product_price_dag.py` with simple 4-step pipeline:
  - Generate configs
  - Extract from Oracle
  - Run Data Loader
  - Audit results
- [ ] 2.2 Add SQL query for joining `KPS_T_REQPROD_MD` with `KPS_T_APPRV_M` tables

## 3. Validation

- [ ] 3.1 Test DAG syntax (`python dags/migrate_product_price_dag.py`)
- [ ] 3.2 Verify field mappings match sample CSV structure
- [ ] 3.3 Dry run with sample data (limit 100 records)
