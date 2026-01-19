## ADDED Requirements

### Requirement: Count Validation

The system SHALL compare record counts between Oracle source and Salesforce target.

#### Scenario: Count match

- **GIVEN** migration completed for a table
- **WHEN** count validation runs
- **THEN** Oracle COUNT(*) is compared to Salesforce COUNT(Id)
- **AND** status is PASS if counts match exactly

#### Scenario: Count mismatch

- **GIVEN** Oracle count differs from Salesforce count
- **WHEN** count validation runs
- **THEN** the difference and match percentage are calculated
- **AND** status is FAIL

---

### Requirement: Aggregate Validation

The system SHALL compare aggregates of numeric columns between source and target.

#### Scenario: Sum comparison

- **GIVEN** a numeric column (e.g., SALES_AMOUNT)
- **WHEN** aggregate validation runs
- **THEN** SUM values from Oracle and Salesforce are compared
- **AND** variance percentage is calculated

#### Scenario: Acceptable variance

- **GIVEN** variance is less than 0.01%
- **WHEN** aggregate validation completes
- **THEN** status is PASS

---

### Requirement: Sample Checksum Validation

The system SHALL validate data integrity using checksums on sample records.

#### Scenario: Random sample

- **GIVEN** a sample_size (default 1000)
- **WHEN** checksum validation runs
- **THEN** random records are selected from Oracle
- **AND** corresponding records are retrieved from Salesforce

#### Scenario: Checksum match

- **GIVEN** a sample record
- **WHEN** checksums are compared
- **THEN** field-level checksums are computed for both source and target
- **AND** matches and mismatches are counted

---

### Requirement: Reconciliation Report

The system SHALL generate a comprehensive reconciliation report.

#### Scenario: Report generation

- **GIVEN** all validation checks complete
- **WHEN** report is generated
- **THEN** report includes: table name, SF object, timestamp, all check results
- **AND** overall_status is PASS only if all checks pass

#### Scenario: Alert on failure

- **GIVEN** any validation check fails
- **WHEN** report is generated
- **THEN** alert is triggered with details of failed checks
