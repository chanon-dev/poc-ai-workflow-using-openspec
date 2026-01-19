# Spec: Salesforce Loading

## ADDED Requirements

### Requirement: Bulk API 2.0 Ingest

The system MUST use Salesforce Bulk API 2.0 to ingest CSV data.

#### Scenario: Create Upload Job

Given a set of CSV files
When the loader is triggered
Then it should create a Bulk API 2.0 "ingest" job with `operation="upsert"`
And capture the Job ID for monitoring

### Requirement: GZIP Compression

The system MUST compress CSV files using GZIP before uploading to Salesforce to reduce network transfer time.

#### Scenario: Compress Payload

Given a staging file `chunk_001.csv` of size 100MB
When uploaded to Salesforce
Then the payload content-encoding must be `gzip`
And the file size should be significantly reduced
