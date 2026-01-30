## ADDED Requirements

### Requirement: Per-batch extract validation

The system SHALL validate each batch file individually using Great Expectations.

#### Scenario: Validate batch file

- **WHEN** batch file is created
- **THEN** the system SHALL run GX validation on that batch
- **AND** SHALL use suite `extract_product_price`
- **AND** SHALL pass `batch_row_count` as evaluation parameter

#### Scenario: Batch validation naming

- **WHEN** validating batch_002
- **THEN** the system SHALL use run_name `extract_validation_batch_002`
- **AND** validation results SHALL be stored separately in Data Docs

### Requirement: Aggregated extract validation

The system SHALL aggregate validation results across all batches.

#### Scenario: All batches pass

- **WHEN** all batch validations pass
- **THEN** overall validation status SHALL be PASS
- **AND** total validated count SHALL equal sum of all batch counts

#### Scenario: Some batches fail

- **WHEN** batch_002 validation fails
- **THEN** overall validation status SHALL be WARN
- **AND** system SHALL log which batches failed
- **AND** system SHALL continue (non-blocking)

### Requirement: Post-migration reconciliation across batches

The system SHALL reconcile total source count against aggregated upload results.

#### Scenario: Reconciliation calculation

- **WHEN** source extracted 25000 records across 3 batches
- **AND** all batches uploaded successfully with total 24950 success
- **THEN** reconciliation SHALL report:
  - `source_count`: 25000
  - `loaded_count`: 24950
  - `difference`: 50

#### Scenario: Reconciliation with evaluation parameters

- **WHEN** running post-migration validation
- **THEN** the system SHALL pass `source_count` (total across all batches)
- **AND** SHALL validate against aggregated success log

### Requirement: Batch-level reconciliation report

The system SHALL provide per-batch reconciliation details.

#### Scenario: Per-batch breakdown

- **WHEN** reconciliation completes
- **THEN** the system SHALL log per-batch results:
  - "Batch 001: 10000 extracted, 10000 loaded, 0 diff"
  - "Batch 002: 10000 extracted, 9950 loaded, 50 diff"
  - "Batch 003: 5000 extracted, 5000 loaded, 0 diff"
- **AND** SHALL provide summary: "Total: 25000 extracted, 24950 loaded, 50 diff"
