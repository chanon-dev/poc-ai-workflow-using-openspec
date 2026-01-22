# Spec: Centralized Setup DAG + Product Migration

## ADDED Requirements

### Requirement: Centralized Setup DAG

The system SHALL provide a Setup DAG (`setup_salesforce_pipeline`) that generates all Data Loader configurations ahead of time, preventing race conditions when multiple Execution DAGs run in parallel.

#### Scenario: Setup DAG generates master config

- **WHEN** the `setup_salesforce_pipeline` DAG is triggered
- **THEN** it SHALL generate a master `process-conf.xml` containing beans for all tables
- **AND** it SHALL generate `.sdl` mapping files for each table
- **AND** it SHALL encrypt Salesforce credentials

#### Scenario: Setup DAG runs after deploy

- **WHEN** new code is deployed with updated field mappings
- **THEN** the operator SHALL run `setup_salesforce_pipeline` once
- **AND** all Execution DAGs SHALL use the new configurations

### Requirement: Product Price Migration DAG

The system SHALL provide an Execution DAG (`migrate_product_price`) that migrates Product & Price data from Oracle `KPS_T_REQPROD_MD` to Salesforce `Product2` object.

#### Scenario: Extract product data

- **WHEN** the extract task runs
- **THEN** it SHALL query `KPS_T_REQPROD_MD` table
- **AND** it SHALL format date fields as ISO 8601 datetime
- **AND** it SHALL format decimal fields with 2 decimal places
- **AND** it SHALL output CSV to `${AIRFLOW_HOME}/salesforce/data/KPS_T_REQPROD_MD.csv`

#### Scenario: Load product data

- **WHEN** the load task runs
- **THEN** it SHALL execute Data Loader using the pre-generated master config
- **AND** it SHALL NOT generate any new configuration files
- **AND** it SHALL upsert records to Salesforce `Product2` using `ProductCode` as external ID

### Requirement: Parallel Execution Safety

The system SHALL allow multiple Execution DAGs to run in parallel without file conflicts.

#### Scenario: Parallel migration without race condition

- **WHEN** `migrate_product_price` and `migrate_sales_data` run simultaneously
- **THEN** both DAGs SHALL read from the same master `process-conf.xml`
- **AND** neither DAG SHALL write to the config file
- **AND** both DAGs SHALL complete successfully

### Requirement: Failure Detection

The system SHALL detect failures at both the Airflow task level and the Data Loader application level.

#### Scenario: Data Loader partial failure

- **WHEN** the Data Loader process completes with errors in `error.csv`
- **THEN** the `audit_results` task SHALL count success and error records
- **AND** it SHALL fail the DAG if error count > 0
- **AND** it SHALL log the error file path for retry
