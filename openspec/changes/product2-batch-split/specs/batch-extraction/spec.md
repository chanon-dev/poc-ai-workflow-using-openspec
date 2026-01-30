## ADDED Requirements

### Requirement: Configurable batch size

The system SHALL allow configuration of batch size through Airflow Variable `batch_size` or DAG run config parameter.

#### Scenario: Batch size from Airflow Variable

- **WHEN** Airflow Variable `batch_size` is set to 10000
- **THEN** the system SHALL split extracted data into files of 10000 records each

#### Scenario: Batch size from DAG config

- **WHEN** DAG is triggered with config `{"batch_size": 50000}`
- **THEN** the system SHALL use 50000 as batch size, overriding Airflow Variable

#### Scenario: Default batch size

- **WHEN** no batch_size is configured
- **THEN** the system SHALL use default value of 10000 records per batch

### Requirement: Split DataFrame into batch files

The system SHALL split the extracted DataFrame into multiple CSV files based on configured batch size.

#### Scenario: Data larger than batch size

- **WHEN** extracted data has 25000 records
- **AND** batch size is 10000
- **THEN** the system SHALL create 3 files:
  - `Product2_batch_001.csv` (10000 records)
  - `Product2_batch_002.csv` (10000 records)
  - `Product2_batch_003.csv` (5000 records)

#### Scenario: Data smaller than batch size

- **WHEN** extracted data has 5000 records
- **AND** batch size is 10000
- **THEN** the system SHALL create 1 file:
  - `Product2_batch_001.csv` (5000 records)

#### Scenario: Empty data

- **WHEN** extracted data has 0 records
- **THEN** the system SHALL NOT create any batch files
- **AND** SHALL log a warning message

### Requirement: Batch file naming convention

The system SHALL name batch files with zero-padded sequential numbering.

#### Scenario: File naming format

- **WHEN** creating batch files
- **THEN** files SHALL be named `{prefix}_batch_{NNN}.csv`
- **AND** NNN SHALL be zero-padded to 3 digits (001, 002, ..., 999)

### Requirement: Return batch metadata

The extract function SHALL return metadata about created batches via XCom.

#### Scenario: Batch metadata structure

- **WHEN** batch extraction completes
- **THEN** the function SHALL return a dictionary containing:
  - `total_records`: total number of records extracted
  - `batch_count`: number of batch files created
  - `batch_files`: list of created file paths
  - `batch_size`: configured batch size used
