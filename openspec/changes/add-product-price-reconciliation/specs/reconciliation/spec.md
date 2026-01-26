# Product Price Reconciliation Spec

## ADDED Requirements

### Requirement: Oracle Source Data Validation

The system SHALL validate Oracle source data before extraction.

#### Scenario: Verify Oracle Source Data

- **Given** table `KPS_T_REQPROD_MD`
- **When** `validate_source` task runs
- **Then** `BARCODE` should not be null
- **And** `STD_CATE_CODE` should not be null
- **And** Row count should be > 0

---

### Requirement: Extracted Data Validation

The system SHALL validate the extracted CSV data before loading.

#### Scenario: Verify Extracted CSV

- **Given** the extracted `Product2.csv`
- **When** `validate_extract` task runs
- **Then** Row count should match the Oracle source count
- **And** `KPS_PRICE_EXC_VAT` should be a valid number

---

### Requirement: Salesforce Reconciliation

The system SHALL reconcile the migrated data in Salesforce against the source.

#### Scenario: Reconcile Salesforce Load

- **Given** the loaded data in Salesforce
- **When** `validate_postmig` task runs
- **Then** Salesforce record count should match Oracle source count (allow small tolerance if needed)

## MODIFIED Requirements

### Requirement: DAG Workflow Integration

The `migrate_product_price_dag` SHALL be updated to include validation tasks.

#### Scenario: DAG Integration

- **Given** `migrate_product_price_dag.py`
- **When** the DAG is updated
- **Then** it should include `validate_source` before extraction
- **And** `validate_extract` after extraction
- **And** `validate_postmig` after loading audit
