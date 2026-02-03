## ADDED Requirements

### Requirement: DAG orchestrates end-to-end Bulk API upload

The system SHALL provide an Airflow DAG that orchestrates: authenticate → extract from Oracle → split into batches → upload via Bulk API 2.0 → collect results → update status.

#### Scenario: Successful full pipeline run

- **WHEN** the DAG is triggered (manually or scheduled)
- **THEN** the system SHALL execute the following tasks in order:
  1. Authenticate to Salesforce (OAuth 2.0)
  2. Extract data from Oracle into CSV batches
  3. Upload each batch via `SalesforceBulkLoader`
  4. Collect successful/failed/unprocessed results
  5. Update `TMS_Daily_Sales_File__c` status to "Uploaded"

#### Scenario: Extract returns zero records

- **WHEN** the Oracle extraction query returns zero rows
- **THEN** the system SHALL skip upload and result collection tasks
- **AND** log a warning message

### Requirement: Upload CSV batches via SalesforceBulkLoader

The system SHALL use the existing `SalesforceBulkLoader` plugin with `api_version="v66.0"` to upload CSV batch files.

#### Scenario: Single batch upload

- **WHEN** extraction produces a single batch file
- **THEN** the system SHALL call `SalesforceBulkLoader.load_file()` with the batch file path, object name, and external ID field

#### Scenario: Multiple batch parallel upload

- **WHEN** extraction produces multiple batch files
- **THEN** the system SHALL call `SalesforceBulkLoader.load_files_parallel()` to upload batches concurrently

#### Scenario: Batch upload failure

- **WHEN** a bulk job returns state `Failed` or `Aborted`
- **THEN** the system SHALL log the error, update `TMS_Daily_Sales_File__c` status to "In Progress" (reset), and raise an exception

### Requirement: Collect and persist bulk job results

The system SHALL fetch result CSVs from completed bulk jobs and persist them as local files for auditing and reconciliation.

#### Scenario: Collect successful results

- **WHEN** a bulk job completes with state `JobComplete`
- **THEN** the system SHALL GET `/jobs/ingest/{jobId}/successfulResults` and save the CSV to `salesforce/logs/{object}_{jobId}_success.csv`

#### Scenario: Collect failed results

- **WHEN** a bulk job has `numberRecordsFailed > 0`
- **THEN** the system SHALL GET `/jobs/ingest/{jobId}/failedResults` and save the CSV to `salesforce/logs/{object}_{jobId}_failed.csv`

#### Scenario: Collect unprocessed records

- **WHEN** a bulk job has unprocessed records (e.g., job was aborted)
- **THEN** the system SHALL GET `/jobs/ingest/{jobId}/unprocessedrecords` and save the CSV to `salesforce/logs/{object}_{jobId}_unprocessed.csv`

### Requirement: Support batch resume via start_batch config

The system SHALL support resuming from a specific batch number, consistent with the existing batch configuration pattern.

#### Scenario: Resume from batch 3

- **WHEN** the DAG is triggered with config `{"start_batch": 3}`
- **THEN** the system SHALL skip batches 1 and 2 and begin uploading from batch 3

#### Scenario: Default start batch

- **WHEN** no `start_batch` is specified in config
- **THEN** the system SHALL start from batch 1

### Requirement: DAG uses configurable table settings

The system SHALL read the target Salesforce object name and external ID field from `dags/config/tables_config.py` or DAG run config.

#### Scenario: Table config from tables_config.py

- **WHEN** the DAG is triggered without explicit object config
- **THEN** the system SHALL use `TableConfig.sf_object` and `TableConfig.external_id_field` for the configured table

#### Scenario: Override via DAG run config

- **WHEN** the DAG is triggered with config `{"sf_object": "MyObject__c", "external_id_field": "ExtId__c"}`
- **THEN** the system SHALL use those values instead of the table config defaults
