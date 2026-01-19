# Design: Data Migration Pipeline Architecture

## Context

KPC TMS needs to migrate 2-3 years of historical transaction data from Oracle Database (on-premise) to Salesforce (cloud). Key constraints:

- **Volume:** 522M-783M total records
- **Largest table:** 261M records (KPS_T_SALES_MD)
- **Target throughput:** ~3,000 records/second
- **Environment:** On-premise Airflow with CeleryExecutor

## Goals / Non-Goals

### Goals

- Enable migration of all 16 source tables to Salesforce
- Achieve target throughput of 3,000+ records/second
- Ensure data integrity via reconciliation checks
- Support incremental and full migration modes
- Provide audit trail for compliance

### Non-Goals

- Real-time CDC (change data capture)
- Bi-directional sync
- Schema migration automation

## Decisions

### 1. ETL Orchestration: Apache Airflow 3.x

**Decision:** Use Airflow with CeleryExecutor for parallel task execution.

**Alternatives considered:**

| Option | Pros | Cons |
|--------|------|------|
| Apache Spark | High parallelism | Overkill, complex setup |
| dbt | Great for transforms | Not designed for ETL to Salesforce |
| Custom scripts | Simple | No retry logic, monitoring |

**Rationale:** Airflow provides DAG-based orchestration, built-in retry, monitoring, and CeleryExecutor enables horizontal scaling.

### 2. Extraction: Parallel Chunking with Date Partitioning

**Decision:** Extract in 500K-record chunks using ROW_NUMBER() with date partitioning.

**Key parameters:**

- Chunk size: 500,000 records
- Parallel workers: 10 (for largest tables)
- Oracle parallel hint: `/*+ PARALLEL(t, 8) */`

**Trade-off:** More chunks = more overhead but better memory management.

### 3. Staging: Local CSV with GZIP Compression

**Decision:** Stage extracted data as GZIP-compressed CSV files on local NVMe SSD.

**Alternatives considered:**

| Option | Pros | Cons |
|--------|------|------|
| S3/GCS | Distributed, durable | Added latency, cost |
| In-memory | Fastest | Memory limits |
| Database staging | ACID | Extra DB load |

**Rationale:** Bulk API 2.0 natively accepts GZIP CSV. Local storage minimizes latency.

### 4. Loading: Salesforce Bulk API 2.0

**Decision:** Use Bulk API 2.0 with upsert operations and 15 concurrent jobs.

**Key configuration:**

- Max concurrent jobs: 15
- GZIP compression: Enabled
- Operation: Upsert (idempotent)
- External ID field required on all objects

**Salesforce limits:**

| Limit | Value |
|-------|-------|
| Records per 24hr | 150M |
| File size | 150MB |
| Concurrent jobs | 100 |

### 5. Reconciliation: Three-Level Validation

**Decision:** Implement count, aggregate, and sample checksum validation.

| Level | Method | Speed | Accuracy |
|-------|--------|-------|----------|
| 1 | Count comparison | Fast | Low |
| 2 | Sum/Avg aggregates | Medium | Medium |
| 3 | Sample checksums | Slow | High |

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| SF API rate limiting | Throttle to 15 concurrent jobs |
| Oracle CPU spike | Schedule during off-peak hours |
| Disk space exhaustion | Auto-cleanup after load |
| Data corruption | Checksum validation |

## Migration Plan

1. Start with smallest table (KPS_R_POS_SUPPLIER) for validation
2. Progress through phases (reference → pre-invoice → sales)
3. Run reconciliation after each phase
4. Archive completed chunks
