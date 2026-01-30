## ADDED Requirements

### Requirement: Sequential batch upload

The system SHALL upload batch files to Salesforce sequentially in order.

#### Scenario: Successful sequential upload

- **WHEN** 3 batch files exist (batch_001, batch_002, batch_003)
- **THEN** the system SHALL upload batch_001 first
- **AND** wait for completion before uploading batch_002
- **AND** wait for completion before uploading batch_003

#### Scenario: Upload order

- **WHEN** uploading batch files
- **THEN** files SHALL be uploaded in ascending numerical order (001 → 002 → 003)

### Requirement: Per-batch error handling

The system SHALL track success and error counts per batch file.

#### Scenario: Batch with errors

- **WHEN** batch_002 upload completes with 50 errors
- **THEN** the system SHALL log: "Batch 002: 9950 success, 50 errors"
- **AND** SHALL continue uploading batch_003

#### Scenario: Complete batch failure

- **WHEN** a batch upload fails completely (Data Loader error)
- **THEN** the system SHALL log the error
- **AND** SHALL stop processing remaining batches
- **AND** SHALL raise an exception with batch details

### Requirement: Aggregate upload results

The system SHALL aggregate results from all batch uploads.

#### Scenario: Aggregated success log

- **WHEN** all batch uploads complete
- **THEN** the system SHALL create aggregated success log at `Product2_success.csv`
- **AND** SHALL contain all successful records from all batches

#### Scenario: Aggregated error log

- **WHEN** batch uploads complete with errors
- **THEN** the system SHALL create aggregated error log at `Product2_error.csv`
- **AND** SHALL contain all error records from all batches

### Requirement: Continue from failed batch

The system SHALL support restarting from a specific batch.

#### Scenario: Resume from batch

- **WHEN** DAG is triggered with config `{"start_batch": 3}`
- **THEN** the system SHALL skip batches 001 and 002
- **AND** SHALL start uploading from batch_003
