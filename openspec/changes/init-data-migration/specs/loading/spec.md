## ADDED Requirements

### Requirement: Bulk API 2.0 Integration

The system SHALL load data to Salesforce using Bulk API 2.0 for optimal performance.

#### Scenario: Create upsert job

- **GIVEN** a Salesforce object and External ID field
- **WHEN** a load job is created
- **THEN** a Bulk API 2.0 ingest job is created with operation=upsert
- **AND** the externalIdFieldName is set to the configured External ID

#### Scenario: Job completion monitoring

- **GIVEN** a job is submitted
- **WHEN** waiting for completion
- **THEN** the system polls job status every 5 seconds
- **AND** times out after 2 hours if not complete

---

### Requirement: GZIP Compression

The system SHALL compress CSV uploads using GZIP to reduce transfer size.

#### Scenario: Compressed upload

- **GIVEN** a CSV file to upload
- **WHEN** use_gzip=True (default)
- **THEN** the file is compressed before upload
- **AND** Content-Encoding: gzip header is set

---

### Requirement: Parallel Job Execution

The system SHALL support parallel Bulk API jobs for faster loading.

#### Scenario: Concurrent uploads

- **GIVEN** multiple CSV files to load
- **WHEN** parallel loading is enabled
- **THEN** up to 15 jobs run concurrently (configurable)
- **AND** results are collected for all jobs

#### Scenario: Respect Salesforce limits

- **GIVEN** Salesforce concurrent job limit is 100
- **WHEN** configuring max_concurrent_jobs
- **THEN** the value SHALL NOT exceed 15 to maintain safety margin

---

### Requirement: Error Handling

The system SHALL handle and report Bulk API errors.

#### Scenario: Job failure

- **GIVEN** a Bulk API job fails
- **WHEN** results are retrieved
- **THEN** the error state and message are captured
- **AND** the failed file path is recorded

#### Scenario: Partial failure

- **GIVEN** some records in a job fail
- **WHEN** job completes
- **THEN** numberRecordsProcessed and numberRecordsFailed are reported

---

### Requirement: Idempotent Upsert

The system SHALL use upsert operations to ensure idempotency.

#### Scenario: Retry safety

- **GIVEN** a job is retried after failure
- **WHEN** the same records are uploaded again
- **THEN** existing records are updated (not duplicated)
- **AND** new records are inserted
