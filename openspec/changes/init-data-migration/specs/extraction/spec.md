## ADDED Requirements

### Requirement: Parallel Data Extraction

The system SHALL extract data from Oracle Database in parallel chunks to optimize throughput.

#### Scenario: Large table extraction with chunking

- **GIVEN** a table with more than 1 million records
- **WHEN** extraction is initiated
- **THEN** data is extracted in chunks of 500,000 records maximum
- **AND** multiple worker processes extract chunks concurrently

#### Scenario: Configurable chunk size

- **GIVEN** a table configuration with custom chunk_size setting
- **WHEN** extraction is executed
- **THEN** the specified chunk size is used for that table

---

### Requirement: Date-Based Partitioning

The system SHALL support date-based partitioning for incremental extraction.

#### Scenario: Extract by date range

- **GIVEN** a date range (start_date, end_date) is specified
- **WHEN** extraction runs
- **THEN** only records within the date range are extracted
- **AND** the partition column (e.g., CREATED_DATE) is used for filtering

#### Scenario: Full table extraction

- **GIVEN** no date range is specified
- **WHEN** extraction runs
- **THEN** all records from the table are extracted

---

### Requirement: Oracle Parallel Hints

The system SHALL use Oracle parallel query hints for large table extraction.

#### Scenario: Parallel hint enabled

- **GIVEN** a table configuration with use_parallel_hint=True
- **WHEN** the extraction query is generated
- **THEN** the query includes `/*+ PARALLEL(t, N) */` hint
- **AND** N equals the configured parallel_degree

#### Scenario: Parallel hint disabled

- **GIVEN** a table configuration with use_parallel_hint=False
- **WHEN** the extraction query is generated
- **THEN** no parallel hint is included

---

### Requirement: Staging File Output

The system SHALL save extracted data as CSV files in a configurable staging directory.

#### Scenario: CSV file creation

- **GIVEN** extraction completes for a chunk
- **WHEN** the data is saved
- **THEN** a CSV file is created at `{STAGING_PATH}/{table_name}_chunk_{chunk_id}.csv`

#### Scenario: GZIP compression

- **GIVEN** GZIP compression is enabled
- **WHEN** the CSV file is saved
- **THEN** the file is compressed and saved as `.csv.gz`
