# Spec: Oracle Extraction

## ADDED Requirements

### Requirement: Parallel Chunking Extraction

The system MUST support splitting large tables into smaller chunks based on `ROWNUM` or `ROWID` to enable parallel extraction.

#### Scenario: Extract Large Table

Given a table `KPS_T_SALES_MD` with 261M records
When the `extract_task` is triggered
Then it should identify the total record count
And split the range into chunks of 500,000 records
And spawn parallel Airflow tasks to extract these chunks concurrently

### Requirement: Optimized Query Generation

The system MUST generate SQL queries that utilize Oracle Parallel Hints to maximize extraction speed.

#### Scenario: Generate Hints

Given a configuration specifying `parallel_degree: 8`
When the query is generated
Then it should include `/*+ PARALLEL(t, 8) */` in the SELECT statement
