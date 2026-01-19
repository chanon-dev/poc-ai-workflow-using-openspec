# Spec: Reconciliation

## ADDED Requirements

### Requirement: Count Comparison

The system MUST compare total record, success, and failure counts between Oracle, Airflow logs, and Salesforce.

#### Scenario: Compare Counts

Given 1000 records extracted from Oracle
And 998 records successfully loaded to Salesforce
And 2 records failed
When reconciliation runs
Then it should flag a 100% accounting match (998 success + 2 failed = 1000 total)

### Requirement: Audit Logging

The system MUST log reconciliation results to a persistent audit table/file.

#### Scenario: Log Result

Given a reconciliation result (Match or Mismatch)
When the check completes
Then it should insert a record into `MIGRATION_AUDIT` table with timestamps and details
