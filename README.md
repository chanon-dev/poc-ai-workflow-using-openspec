# KPC TMS Data Migration

**Enterprise Data Migration Solution: Oracle to Salesforce**

> **Document Classification**: Internal - Technical Documentation
> **Status**: Proof of Concept (POC)
> **Version**: 1.0.0
> **Last Updated**: January 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Context](#2-business-context)
3. [Solution Architecture](#3-solution-architecture)
4. [Technology Stack](#4-technology-stack)
5. [POC Implementation Status](#5-poc-implementation-status)
6. [Production Roadmap](#6-production-roadmap)
7. [Technical Specifications](#7-technical-specifications)
8. [Data Validation Framework](#8-data-validation-framework)
9. [Security & Compliance](#9-security--compliance)
10. [Risk Assessment](#10-risk-assessment)
11. [Infrastructure Requirements](#11-infrastructure-requirements)
12. [Operations Runbook](#12-operations-runbook)
13. [Appendix](#13-appendix)

---

## 1. Executive Summary

### 1.1 Project Overview

The KPC TMS Data Migration project delivers an enterprise-grade solution for migrating historical transaction data from **KPC Transaction Management System (TMS)** on Oracle Database to **Salesforce Cloud**. This migration enables unified customer data management, improved analytics capabilities, and cloud-native scalability.

### 1.2 Key Metrics

| Metric | Value |
|--------|-------|
| **Total Records** | 522M - 783M records |
| **Source Tables** | 16 Oracle tables |
| **Target Objects** | 16 Salesforce custom objects |
| **Historical Period** | 2-3 years of transactional data |
| **Target Throughput** | ~3,000 records/second |
| **Estimated Duration** | 42-48 hours (full migration) |

### 1.3 Critical Data Volumes

| Source Table | Target Object | Records/Year | 2-3 Year Total |
|--------------|---------------|--------------|----------------|
| `KPS_T_SALES_MD` | `KPS_Sales__c` | 87M | 174M - 261M |
| `KPS_T_SALESPAY_MD` | `KPS_SalesPay__c` | 36M | 73M - 109M |
| `KPS_T_SALES_M` | `KPS_SalesM__c` | 36M | 72M - 108M |
| Others (13 tables) | Various | < 500K | < 1.5M |

### 1.4 POC Achievements

- Validated end-to-end pipeline architecture
- Demonstrated parallel extraction from Oracle (10x throughput improvement)
- Confirmed Salesforce Bulk API 2.0 capacity handling
- Implemented data quality validation with Great Expectations
- Established reconciliation framework for data integrity

---

## 2. Business Context

### 2.1 Migration Objectives

1. **Unified Data Platform**: Consolidate TMS transaction data into Salesforce for 360-degree customer view
2. **Analytics Enablement**: Enable Salesforce-native reporting and Einstein Analytics
3. **Legacy Decommission**: Support eventual decommissioning of on-premise Oracle systems
4. **Compliance**: Maintain data integrity and audit trail during migration

### 2.2 Success Criteria

| Criteria | Target | Validation Method |
|----------|--------|-------------------|
| Data Completeness | 100% record count match | Automated reconciliation |
| Data Accuracy | 99.99% field-level accuracy | Sample checksum validation |
| Performance | Complete within 72-hour window | Execution time monitoring |
| Auditability | Full migration audit trail | Oracle `MIGRATION_AUDIT_LOG` table |

### 2.3 Constraints & Dependencies

- **Salesforce Daily Limits**: 150M records/day, 15,000 Bulk API jobs/day
- **Network Bandwidth**: Requires dedicated 1Gbps+ connection
- **Downtime Window**: Migration during business off-hours preferred
- **Salesforce Org Preparation**: Triggers/Flows must be disabled during load

---

## 3. Solution Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ON-PREMISE INFRASTRUCTURE                         │
│                                                                          │
│  ┌────────────────┐    ┌────────────────────────────────────────────┐   │
│  │                │    │           APACHE AIRFLOW 3.x               │   │
│  │    ORACLE      │    │  ┌──────────────────────────────────────┐  │   │
│  │    DATABASE    │───▶│  │         SCHEDULER + API               │  │   │
│  │                │    │  └──────────────────────────────────────┘  │   │
│  │  - KPS Tables  │    │                    │                       │   │
│  │  - 2-3 Years   │    │  ┌──────────────────────────────────────┐  │   │
│  │  - ~500M rows  │    │  │    CELERY WORKERS (3-5 nodes)        │  │   │
│  │                │    │  │    - Parallel Extraction              │  │   │
│  └────────────────┘    │  │    - Transformation                   │  │   │
│                        │  │    - Loading Coordination             │  │   │
│                        │  └──────────────────────────────────────┘  │   │
│                        └────────────────────────────────────────────┘   │
│                                          │                               │
│                                          ▼                               │
│                        ┌────────────────────────────────────────────┐   │
│                        │          STAGING LAYER (NVMe SSD)          │   │
│                        │  - CSV Files (GZIP Compressed)             │   │
│                        │  - Great Expectations Validation           │   │
│                        │  - ~500GB Storage                          │   │
│                        └────────────────────────────────────────────┘   │
│                                          │                               │
│                        ┌────────────────────────────────────────────┐   │
│                        │      SALESFORCE DATA LOADER CLI            │   │
│                        │  - Bulk API 2.0                            │   │
│                        │  - UPSERT Operations                       │   │
│                        │  - 10-15 Parallel Jobs                     │   │
│                        └────────────────────────────────────────────┘   │
│                                          │                               │
└──────────────────────────────────────────┼───────────────────────────────┘
                                           │
                                           ▼
                            ┌──────────────────────────────┐
                            │      SALESFORCE CLOUD        │
                            │                              │
                            │  - Custom Objects (KPS_*)    │
                            │  - Bulk API 2.0 Endpoint     │
                            │  - Data Storage              │
                            │                              │
                            └──────────────────────────────┘
```

### 3.2 Data Flow Pipeline

```
PHASE 1          PHASE 2          PHASE 3          PHASE 4          PHASE 5
┌─────────┐     ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│ EXTRACT │────▶│TRANSFORM│─────▶│  STAGE  │─────▶│  LOAD   │─────▶│RECONCILE│
└─────────┘     └─────────┘      └─────────┘      └─────────┘      └─────────┘
     │               │                │                │                │
     ▼               ▼                ▼                ▼                ▼
┌─────────┐     ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│   GX    │     │   GX    │      │   GX    │      │   GX    │      │   GX    │
│Validate │     │Validate │      │Validate │      │Validate │      │Validate │
└─────────┘     └─────────┘      └─────────┘      └─────────┘      └─────────┘

Legend: GX = Great Expectations Data Validation
```

### 3.3 DAG Execution Pattern

The migration follows a **phased approach** with dependency management:

```
Phase 1: Reference Data ──────────────────────────┐
         (3 tables, parallel)                     │
                                                  │
Phase 2: Pre-Invoice Tables ──────────────────────┤
         (3 tables, parallel)                     │
                                                  │
Phase 3: Pre-Invoice Details ─────────────────────┤
         (3 tables, parallel)                     │
                                                  │
Phase 4: KPS_T_SALES_M ───────────────────────────┤ Sequential
         (108M records, chunked)                  │ (Large Tables)
                                                  │
Phase 5: KPS_T_SALES_MD ──────────────────────────┤
         (261M records, chunked)                  │
                                                  │
Phase 6: KPS_T_SALESPAY_MD ───────────────────────┤
         (109M records, chunked)                  │
                                                  │
Phase 7: Supporting Tables ───────────────────────┤
         (4 tables, parallel)                     │
                                                  ▼
Phase 8: Reconciliation ──────────────────────────●
         (All tables validation)
```

---

## 4. Technology Stack

### 4.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Orchestration** | Apache Airflow | 3.x | Workflow orchestration, scheduling, monitoring |
| **Execution** | Celery | Latest | Distributed task execution |
| **Message Broker** | Redis | 7.2 | Task queue management |
| **Metadata DB** | PostgreSQL | 16 | Airflow metadata storage |
| **Containerization** | Docker | Latest | Environment consistency |
| **Source DB** | Oracle | 19c+ | Source transaction data |
| **Target** | Salesforce | Latest | Cloud CRM platform |
| **ETL Tool** | SF Data Loader | v64 | Bulk data loading |
| **Validation** | Great Expectations | Latest | Data quality validation |

### 4.2 Key Libraries & Dependencies

```python
# Python Dependencies
cx_Oracle>=8.0.0          # Oracle database connectivity
pandas>=2.0.0             # Data manipulation
great_expectations>=0.18  # Data validation
requests>=2.28.0          # HTTP client
python-dotenv>=1.0.0      # Environment management
```

### 4.3 Integration Points

| System | Integration Method | Protocol |
|--------|-------------------|----------|
| Oracle Database | cx_Oracle driver | SQL*Net / TCP |
| Salesforce | Bulk API 2.0 | HTTPS / REST |
| Airflow Workers | Celery | AMQP (Redis) |
| Monitoring | Airflow Web UI | HTTP |

---

## 5. POC Implementation Status

### 5.1 Completed Components

| Component | Status | Notes |
|-----------|--------|-------|
| Airflow Infrastructure | ✅ Complete | Docker Compose deployment |
| Oracle Extraction Plugin | ✅ Complete | Parallel query support |
| Transformation Framework | ✅ Complete | Field mapping, type conversion |
| SF Bulk Loader Plugin | ✅ Complete | Bulk API 2.0 integration |
| Great Expectations Setup | ✅ Complete | Validation suites configured |
| Product Price Migration DAG | ✅ Complete | Full E2E pipeline |
| Reconciliation Framework | ✅ Complete | Count/Aggregate/Checksum |
| Batch Split Logic | ✅ Complete | Configurable batch sizes |

### 5.2 POC Validated Scenarios

| Scenario | Result | Evidence |
|----------|--------|----------|
| Extract 100K records from Oracle | ✅ Pass | < 30 seconds |
| Parallel extraction (10 workers) | ✅ Pass | 10x throughput |
| GZIP compression (70% reduction) | ✅ Pass | Verified file sizes |
| SF Bulk API 2.0 upsert | ✅ Pass | Success logs |
| Great Expectations validation | ✅ Pass | Data docs generated |
| Batch file splitting | ✅ Pass | Correct file counts |
| Error handling & retry | ✅ Pass | Tested failure scenarios |

### 5.3 Current Limitations (POC Scope)

| Limitation | Impact | Production Resolution |
|------------|--------|----------------------|
| Single-node testing only | Not production-scale | Deploy multi-worker cluster |
| Manual DAG triggering | No automation | Implement scheduling |
| Limited error alerting | Delayed response | Add Slack/Email integration |
| Sample data validation | Partial coverage | Full dataset validation |
| No incremental sync | Full load only | Implement CDC/delta logic |

---

## 6. Production Roadmap

### 6.1 Implementation Phases

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION IMPLEMENTATION ROADMAP                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PHASE 1: Infrastructure Setup                                          │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Provision production Kubernetes/Docker Swarm cluster                 │
│  □ Configure multi-worker Celery setup (5 workers)                      │
│  □ Set up NVMe SSD staging storage (1TB)                                │
│  □ Configure network connectivity (VPN/Direct Connect)                  │
│  □ Deploy monitoring stack (Prometheus/Grafana)                         │
│  □ Set up centralized logging (ELK/CloudWatch)                          │
│                                                                          │
│  PHASE 2: Security & Compliance                                         │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Implement secrets management (HashiCorp Vault/AWS Secrets)           │
│  □ Configure Salesforce Integration User with minimum permissions       │
│  □ Set up credential rotation procedures                                │
│  □ Implement audit logging to Oracle MIGRATION_AUDIT_LOG                │
│  □ Configure encrypted communication (TLS 1.3)                          │
│  □ Document data handling procedures for compliance                     │
│                                                                          │
│  PHASE 3: DAG Development                                               │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Implement all 16 table migration DAGs                                │
│  □ Configure table-specific extraction parameters                       │
│  □ Create field mapping SDL files for all tables                        │
│  □ Implement master orchestration DAG                                   │
│  □ Add comprehensive error handling and retry logic                     │
│  □ Create failed-record recovery DAG                                    │
│                                                                          │
│  PHASE 4: Validation & Testing                                          │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Create Great Expectations suites for all tables                      │
│  □ Implement full reconciliation pipeline                               │
│  □ Execute dry-run with production data sample (1%)                     │
│  □ Performance testing at scale                                         │
│  □ Failure injection testing                                            │
│  □ Document runbooks and troubleshooting guides                         │
│                                                                          │
│  PHASE 5: Cutover Preparation                                           │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Create Salesforce org backup                                         │
│  □ Disable Salesforce triggers/flows/workflows                          │
│  □ Enable "Defer Sharing Calculations"                                  │
│  □ Configure alerting (Slack/PagerDuty)                                 │
│  □ Schedule migration window (off-peak hours)                           │
│  □ Prepare rollback procedures                                          │
│                                                                          │
│  PHASE 6: Migration Execution                                           │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Execute Phase 1-3: Reference & Pre-Invoice data                      │
│  □ Execute Phase 4-6: Large transaction tables                          │
│  □ Execute Phase 7: Supporting tables                                   │
│  □ Execute Phase 8: Final reconciliation                                │
│  □ Generate migration completion report                                 │
│                                                                          │
│  PHASE 7: Post-Migration                                                │
│  ════════════════════════════════════════════════════════════════════   │
│  □ Re-enable Salesforce automation                                      │
│  □ Run sharing rule recalculation                                       │
│  □ Validate data in Salesforce UI                                       │
│  □ Archive migration logs and artifacts                                 │
│  □ Document lessons learned                                             │
│  □ Decommission staging infrastructure                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Outstanding Development Tasks

| Task ID | Task Description | Priority | Effort |
|---------|-----------------|----------|--------|
| PROD-001 | Implement remaining 15 table DAGs | High | Large |
| PROD-002 | Create field mapping SDL files for all tables | High | Medium |
| PROD-003 | Set up Kubernetes deployment manifests | High | Medium |
| PROD-004 | Implement Slack/Email alerting | Medium | Small |
| PROD-005 | Create incremental sync (delta) DAG | Medium | Large |
| PROD-006 | Implement failed-record recovery workflow | Medium | Medium |
| PROD-007 | Create comprehensive test suite | Medium | Medium |
| PROD-008 | Document operational runbooks | Medium | Small |
| PROD-009 | Set up Grafana dashboards | Low | Small |
| PROD-010 | Implement data masking for PII | Low | Medium |

### 6.3 Resource Requirements

| Role | FTE | Duration | Responsibilities |
|------|-----|----------|------------------|
| Data Engineer | 2 | 8 weeks | DAG development, testing |
| DevOps Engineer | 1 | 4 weeks | Infrastructure, CI/CD |
| Salesforce Admin | 1 | 4 weeks | Org prep, validation |
| QA Engineer | 1 | 4 weeks | Testing, validation |
| Project Manager | 0.5 | 12 weeks | Coordination, reporting |

---

## 7. Technical Specifications

### 7.1 Extraction Configuration

```python
# dags/config/extract_config.py
EXTRACT_CONFIG = {
    "KPS_T_SALES_MD": {
        "chunk_size": 500_000,        # Records per chunk
        "parallel_workers": 10,        # Concurrent extract threads
        "fetch_size": 50_000,          # Oracle cursor fetch size
        "use_parallel_hint": True,     # Use /*+ PARALLEL() */ hint
        "parallel_degree": 8,          # Oracle parallel degree
        "partition_column": "CREATED_DATE"
    },
    # ... additional table configs
}
```

### 7.2 Field Mapping Structure

```python
# dags/config/field_mappings.py
FIELD_MAPPINGS = {
    "KPS_T_SALES_MD": {
        "sf_object": "KPS_Sales__c",
        "external_id": "External_ID__c",
        "mappings": {
            "SALES_ID": "External_ID__c",
            "CUSTOMER_ID": "Customer__c",
            "SALE_DATE": "Sale_Date__c",
            "AMOUNT": "Amount__c",
            # ... additional mappings
        },
        "transformations": {
            "SALE_DATE": "to_sf_datetime",
            "AMOUNT": "to_decimal_2",
            # ... additional transformations
        }
    }
}
```

### 7.3 Salesforce Data Loader Configuration

```xml
<!-- salesforce/dataloader_conf/process-conf.xml -->
<bean id="upsertProduct2" class="com.salesforce.dataloader.process.ProcessRunner">
    <property name="name" value="upsertProduct2"/>
    <property name="configOverrideMap">
        <map>
            <entry key="sfdc.entity" value="Product2"/>
            <entry key="process.operation" value="upsert"/>
            <entry key="sfdc.externalIdField" value="ProductCode"/>
            <entry key="process.mappingFile" value="mappings/Product2.sdl"/>
            <entry key="dataAccess.type" value="csvRead"/>
            <entry key="sfdc.useBulkApi" value="true"/>
            <entry key="sfdc.bulkApiSerialMode" value="false"/>
            <entry key="sfdc.loadBatchSize" value="10000"/>
        </map>
    </property>
</bean>
```

### 7.4 Chunking Strategy

```
Large Table Extraction Pattern:
═══════════════════════════════════════════════════════════════════════════

Oracle Table: KPS_T_SALES_MD (261M records)
                    │
                    ▼
    ┌───────────────────────────────────┐
    │     Chunk Calculator              │
    │     chunk_size = 500,000          │
    │     total_chunks = 522            │
    └───────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    ┌───────┐   ┌───────┐   ┌───────┐
    │Chunk 1│   │Chunk 2│   │Chunk N│   ... (522 chunks)
    │ 500K  │   │ 500K  │   │ 500K  │
    └───────┘   └───────┘   └───────┘
        │           │           │
        ▼           ▼           ▼
    ┌───────┐   ┌───────┐   ┌───────┐
    │ GZIP  │   │ GZIP  │   │ GZIP  │
    │ ~50MB │   │ ~50MB │   │ ~50MB │
    └───────┘   └───────┘   └───────┘
        │           │           │
        └───────────┼───────────┘
                    ▼
    ┌───────────────────────────────────┐
    │     Salesforce Bulk API 2.0       │
    │     15 parallel jobs              │
    │     10K records/batch             │
    └───────────────────────────────────┘
```

---

## 8. Data Validation Framework

### 8.1 Great Expectations Integration

```
great_expectations/
├── great_expectations.yml         # Core configuration
├── expectations/                  # Expectation suites
│   ├── source_product_price.json  # Source data validation
│   ├── extract_product_price.json # Post-extract validation
│   └── postmig_product_price.json # Post-migration validation
├── checkpoints/                   # Checkpoint definitions
└── uncommitted/
    ├── data_docs/                 # Generated HTML reports
    └── validations/               # Validation result JSONs
```

### 8.2 Validation Stages

| Stage | Validation Type | Expectations |
|-------|----------------|--------------|
| **Source** | Pre-migration quality | Non-null keys, valid date ranges, referential integrity |
| **Post-Extract** | CSV integrity | Row count match, schema validation, no corrupt data |
| **Pre-Load** | SF compatibility | Field lengths, picklist values, required fields |
| **Post-Migration** | Final reconciliation | Count match, aggregate totals, sample checksums |

### 8.3 Reconciliation Logic

```python
# Three-Level Validation
reconciliation_checks = {
    "level_1_count": {
        "description": "Record count comparison",
        "oracle_query": "SELECT COUNT(*) FROM {table}",
        "salesforce_query": "SELECT COUNT() FROM {object}",
        "tolerance": 0  # Exact match required
    },
    "level_2_aggregate": {
        "description": "Aggregate value comparison",
        "fields": ["SUM(amount)", "AVG(amount)", "MIN(date)", "MAX(date)"],
        "tolerance": 0.001  # 0.1% tolerance for floating point
    },
    "level_3_checksum": {
        "description": "Random sample checksum",
        "sample_size": 1000,
        "hash_fields": ["id", "amount", "date", "status"]
    }
}
```

---

## 9. Security & Compliance

### 9.1 Authentication & Authorization

| System | Authentication | Authorization |
|--------|---------------|---------------|
| Oracle | Database user + password | Role-based (SELECT only) |
| Salesforce | OAuth 2.0 / Security Token | Integration User profile |
| Airflow | Username/Password | Admin role |
| Redis | Password authentication | N/A |

### 9.2 Data Security

| Control | Implementation |
|---------|---------------|
| **Encryption at Rest** | Salesforce native encryption |
| **Encryption in Transit** | TLS 1.3 for all connections |
| **Credential Storage** | Environment variables / Secrets Manager |
| **Access Logging** | Oracle audit trail, Salesforce Event Monitoring |
| **Data Masking** | PII fields masked in logs |

### 9.3 Compliance Considerations

- **Data Residency**: Verify Salesforce data center location
- **Audit Trail**: Maintain `MIGRATION_AUDIT_LOG` for 7 years
- **Data Retention**: Archive source data per retention policy
- **Access Control**: Principle of least privilege for all accounts

### 9.4 Files NOT to Commit (`.gitignore`)

```gitignore
# Sensitive files
config/key.txt
salesforce/dataloader_conf/config.properties
.env
*.pem
*.key

# Generated data
salesforce/data/*.csv
salesforce/logs/
great_expectations/uncommitted/
```

---

## 10. Risk Assessment

### 10.1 Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Salesforce API rate limiting | Medium | High | Implement backoff, monitor limits |
| Network connectivity issues | Medium | High | Retry logic, checkpointing |
| Data corruption during transfer | Low | Critical | Checksum validation, idempotent upsert |
| Oracle performance degradation | Medium | Medium | Off-hours execution, parallel degree tuning |
| Salesforce org capacity | Low | High | Pre-migration storage assessment |
| Migration window overrun | Medium | Medium | Phased execution, rollback plan |

### 10.2 Contingency Plans

| Scenario | Response |
|----------|----------|
| **Bulk API Failure** | Retry failed batches using error logs |
| **Network Timeout** | Resume from last successful chunk |
| **Data Validation Failure** | Halt migration, investigate, remediate |
| **Salesforce Outage** | Pause migration, wait for restoration |
| **Oracle Lock Contention** | Reduce parallel degree, reschedule |

---

## 11. Infrastructure Requirements

### 11.1 Hardware Specifications

| Component | POC | Production |
|-----------|-----|------------|
| **Airflow Scheduler** | 2 vCPU, 4GB RAM | 8 vCPU, 32GB RAM |
| **Airflow Workers** | 1 x (2 vCPU, 4GB) | 5 x (8 vCPU, 32GB) |
| **Redis** | 1 vCPU, 1GB | 2 vCPU, 4GB |
| **PostgreSQL** | 1 vCPU, 2GB | 4 vCPU, 16GB |
| **Staging Storage** | 50GB SSD | 1TB NVMe SSD |
| **Network** | Standard | 1Gbps dedicated |

### 11.2 Salesforce Org Requirements

| Requirement | Specification |
|-------------|---------------|
| **API Version** | 59.0+ |
| **Bulk API** | 2.0 enabled |
| **Daily API Calls** | Monitor usage vs. limits |
| **Data Storage** | Sufficient for ~500M records |
| **Custom Objects** | 16 KPS_* objects deployed |
| **Integration User** | API-only profile with object permissions |

### 11.3 Network Requirements

| Connection | Protocol | Port | Notes |
|------------|----------|------|-------|
| Airflow → Oracle | SQL*Net | 1521 | Firewall rule required |
| Airflow → Salesforce | HTTPS | 443 | *.salesforce.com |
| Airflow → Redis | TCP | 6379 | Internal only |
| Airflow → PostgreSQL | TCP | 5432 | Internal only |

---

## 12. Operations Runbook

### 12.1 Starting the Environment

```bash
# Start all services
docker compose up -d

# Verify services are healthy
docker compose ps

# View logs
docker compose logs -f airflow-scheduler
```

### 12.2 Triggering a Migration

```bash
# Via Airflow CLI
docker compose exec airflow-webserver airflow dags trigger migrate_product_price

# With parameters
docker compose exec airflow-webserver airflow dags trigger migrate_product_price \
  --conf '{"start_date": "2023-01-01", "batch_size": 50000}'
```

### 12.3 Monitoring Progress

1. **Airflow UI**: http://localhost:8080
   - Navigate to DAG → Graph View
   - Monitor task states (green = success, red = failed)

2. **Logs Location**:
   - Airflow: `logs/<dag_id>/<run_id>/<task_id>/`
   - Data Loader: `salesforce/logs/`

3. **Great Expectations Reports**:
   - Open: `great_expectations/uncommitted/data_docs/local_site/index.html`

### 12.4 Handling Failures

```bash
# Check failed task logs
docker compose exec airflow-webserver airflow tasks logs migrate_product_price load_to_salesforce <run_id>

# Retry failed task
docker compose exec airflow-webserver airflow tasks clear migrate_product_price -t load_to_salesforce -s <start_date> -e <end_date>

# Check Data Loader error files
ls -la salesforce/logs/*_error_*.csv
```

### 12.5 Stopping Migration

```bash
# Mark DAG run as failed (stops further tasks)
docker compose exec airflow-webserver airflow dags backfill migrate_product_price --mark_success false --start_date <date>

# Or manually pause DAG
docker compose exec airflow-webserver airflow dags pause migrate_product_price
```

---

## 13. Appendix

### 13.1 Modular Architecture Overview

This project uses a **modular architecture** where each component can be developed, tested, and maintained independently.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODULAR ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        DAG LAYER (Orchestration)                       │  │
│  │   1 Table = 1 DAG  •  Independent execution  •  Parallel processing   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                     │                                        │
│            ┌────────────────────────┼────────────────────────┐              │
│            ▼                        ▼                        ▼              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │  CONFIG MODULE   │    │  MAPPING MODULE  │    │  PLUGIN MODULES  │      │
│  │                  │    │                  │    │                  │      │
│  │  • Table Config  │    │  • Field Mapping │    │  • Extractor     │      │
│  │  • Extract Config│    │  • SDL Files     │    │  • Transformer   │      │
│  │  • GX Config     │    │  • Type Rules    │    │  • Loader        │      │
│  │                  │    │                  │    │  • Validator     │      │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘      │
│            │                        │                        │              │
│            └────────────────────────┼────────────────────────┘              │
│                                     ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     SERVICE LAYER (Connections)                        │  │
│  │           Oracle Service  •  Salesforce Service  •  GX Service        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 13.2 Module Breakdown

#### MODULE A: Configuration (`dags/config/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONFIG MODULE                                │
│                     dags/config/                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  tables_config.py                                        │    │
│  │  ─────────────────                                       │    │
│  │  Purpose: Define source/target table metadata            │    │
│  │                                                          │    │
│  │  TABLE_CONFIG = {                                        │    │
│  │      "KPS_T_SALES_MD": {                                 │    │
│  │          "source_table": "KPS_T_SALES_MD",               │    │
│  │          "sf_object": "KPS_Sales__c",                    │    │
│  │          "external_id": "External_ID__c",                │    │
│  │          "priority": "critical",                         │    │
│  │          "records_per_year": 87_000_000                  │    │
│  │      },                                                  │    │
│  │      ...                                                 │    │
│  │  }                                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  extract_config.py                                       │    │
│  │  ──────────────────                                      │    │
│  │  Purpose: Extraction parameters per table                │    │
│  │                                                          │    │
│  │  EXTRACT_CONFIG = {                                      │    │
│  │      "KPS_T_SALES_MD": {                                 │    │
│  │          "chunk_size": 500_000,                          │    │
│  │          "parallel_workers": 10,                         │    │
│  │          "parallel_degree": 8,      # Oracle hint        │    │
│  │          "fetch_size": 50_000                            │    │
│  │      },                                                  │    │
│  │      ...                                                 │    │
│  │  }                                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Output: Python dict accessible by TABLE_NAME key               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### MODULE B: Field Mapping (`dags/config/` + `salesforce/mappings/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     MAPPING MODULE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  dags/config/field_mappings.py                           │    │
│  │  ──────────────────────────────                          │    │
│  │  Purpose: Oracle → Salesforce field mapping + transforms │    │
│  │                                                          │    │
│  │  FIELD_MAPPINGS = {                                      │    │
│  │      "KPS_T_SALES_MD": {                                 │    │
│  │          "mappings": {                                   │    │
│  │              "SALES_ID": "External_ID__c",               │    │
│  │              "SALE_DATE": "Sale_Date__c",                │    │
│  │              "AMOUNT": "Amount__c",                      │    │
│  │              "CUSTOMER_ID": "Customer__r.External_ID__c" │    │
│  │          },                                              │    │
│  │          "transforms": {                                 │    │
│  │              "SALE_DATE": "to_sf_datetime",              │    │
│  │              "AMOUNT": "to_decimal_2"                    │    │
│  │          }                                               │    │
│  │      },                                                  │    │
│  │      ...                                                 │    │
│  │  }                                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  salesforce/dataloader_conf/mappings/*.sdl               │    │
│  │  ─────────────────────────────────────────               │    │
│  │  Purpose: Data Loader SDL format (auto-generated)        │    │
│  │                                                          │    │
│  │  # KPS_Sales__c.sdl                                      │    │
│  │  SALES_ID=External_ID__c                                 │    │
│  │  SALE_DATE=Sale_Date__c                                  │    │
│  │  AMOUNT=Amount__c                                        │    │
│  │  CUSTOMER_ID=Customer__r.External_ID__c                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Workflow: field_mappings.py → generate_sdl.py → *.sdl files    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### MODULE C: Extraction (`plugins/extractors/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     EXTRACTOR MODULE                             │
│                     plugins/extractors/                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  oracle_extractor.py                                     │    │
│  │  ────────────────────                                    │    │
│  │                                                          │    │
│  │  class OracleExtractor:                                  │    │
│  │      def __init__(self, config: ExtractConfig)           │    │
│  │      def count_records() -> int                          │    │
│  │      def calculate_chunks() -> list[ChunkInfo]           │    │
│  │      def extract_chunk(chunk: ChunkInfo) -> str          │    │
│  │      def extract_to_csv() -> str   # Main entry point    │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Input:   ExtractConfig (chunk_size, parallel_degree, etc.)     │
│  Output:  CSV file path (GZIP compressed)                       │
│                                                                  │
│  Features:                                                       │
│    • Oracle PARALLEL hints for performance                      │
│    • Configurable chunk size (default 500K)                     │
│    • GZIP compression (~70% reduction)                          │
│    • Progress tracking per chunk                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### MODULE D: Transformation (`plugins/transformers/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRANSFORMER MODULE                           │
│                     plugins/transformers/                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  data_transformer.py                                     │    │
│  │  ────────────────────                                    │    │
│  │                                                          │    │
│  │  class DataTransformer:                                  │    │
│  │      def __init__(self, mapping: FieldMapping)           │    │
│  │                                                          │    │
│  │      # Type conversion methods                           │    │
│  │      def to_sf_datetime(val) -> str   # ISO 8601         │    │
│  │      def to_decimal_2(val) -> float   # 2 decimal places │    │
│  │      def to_sf_boolean(val) -> bool   # 1/Y/YES → True   │    │
│  │      def truncate_text(val, max=255) -> str              │    │
│  │                                                          │    │
│  │      # Main entry point                                  │    │
│  │      def transform(csv_path: str) -> str                 │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Input:   CSV file path + FieldMapping config                   │
│  Output:  Transformed CSV file path (SF-ready)                  │
│                                                                  │
│  Transform Rules:                                                │
│    • DateTime: Oracle DATE → 2024-01-15T10:30:00.000Z           │
│    • Decimal: 123.456789 → 123.46                               │
│    • Boolean: 1/Y/YES/TRUE → true                               │
│    • Text: Truncate to max length                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### MODULE E: Loading (`plugins/loaders/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     LOADER MODULE                                │
│                     plugins/loaders/                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  salesforce_bulk_loader.py                               │    │
│  │  ──────────────────────────                              │    │
│  │                                                          │    │
│  │  class SalesforceBulkLoader:                             │    │
│  │      def __init__(self, config: TableConfig)             │    │
│  │                                                          │    │
│  │      # Job management                                    │    │
│  │      def create_job(operation="upsert") -> str           │    │
│  │      def upload_data(job_id: str, csv: str) -> None      │    │
│  │      def close_job(job_id: str) -> None                  │    │
│  │      def poll_status(job_id: str) -> JobStatus           │    │
│  │                                                          │    │
│  │      # Main entry point                                  │    │
│  │      def upsert(csv_path: str) -> LoadResult             │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Input:   CSV file path + TableConfig (sf_object, external_id)  │
│  Output:  LoadResult (success_count, error_count, job_id)       │
│                                                                  │
│  Features:                                                       │
│    • Bulk API 2.0                                               │
│    • UPSERT operation (idempotent)                              │
│    • Parallel jobs (10-15 concurrent)                           │
│    • Auto-retry on failure                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### MODULE F: Validation (`plugins/validators/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                     VALIDATOR MODULE                             │
│                     plugins/validators/                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  reconciliation.py                                       │    │
│  │  ──────────────────                                      │    │
│  │                                                          │    │
│  │  class DataReconciliation:                               │    │
│  │      def __init__(self, table_name: str)                 │    │
│  │                                                          │    │
│  │      # Validation levels                                 │    │
│  │      def count_check() -> ValidationResult               │    │
│  │      def aggregate_check() -> ValidationResult           │    │
│  │      def checksum_sample(n=1000) -> ValidationResult     │    │
│  │                                                          │    │
│  │      # Main entry point                                  │    │
│  │      def run_all_checks() -> ReconciliationReport        │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Input:   table_name (to query both Oracle and Salesforce)      │
│  Output:  ReconciliationReport (pass/fail per check)            │
│                                                                  │
│  Validation Levels:                                              │
│    Level 1: Count match (Oracle vs Salesforce)                  │
│    Level 2: Aggregate match (SUM, AVG, MIN, MAX)                │
│    Level 3: Sample checksum (random 1000 records)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### MODULE G: Great Expectations (`great_expectations/`)

```
┌─────────────────────────────────────────────────────────────────┐
│                  GREAT EXPECTATIONS MODULE                       │
│                  great_expectations/                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Purpose: Validate extracted CSV before loading to Salesforce    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  great_expectations.yml                                  │    │
│  │  ──────────────────────                                  │    │
│  │  Purpose: Core GX configuration                          │    │
│  │                                                          │    │
│  │  datasources:                                            │    │
│  │    - name: csv_staging                                   │    │
│  │      class_name: PandasDatasource                        │    │
│  │      base_directory: salesforce/data/                    │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  expectations/{table}.json                               │    │
│  │  ─────────────────────────                               │    │
│  │  Purpose: CSV validation rules before SF load            │    │
│  │                                                          │    │
│  │  Example: product_price.json                             │    │
│  │  {                                                       │    │
│  │    "expectation_suite_name": "product_price",            │    │
│  │    "expectations": [                                     │    │
│  │      {                                                   │    │
│  │        "expectation_type":                               │    │
│  │            "expect_column_values_to_not_be_null",        │    │
│  │        "kwargs": { "column": "ProductCode" }             │    │
│  │      },                                                  │    │
│  │      {                                                   │    │
│  │        "expectation_type":                               │    │
│  │            "expect_column_values_to_be_unique",          │    │
│  │        "kwargs": { "column": "ProductCode" }             │    │
│  │      },                                                  │    │
│  │      {                                                   │    │
│  │        "expectation_type":                               │    │
│  │            "expect_table_row_count_to_be_between",       │    │
│  │        "kwargs": { "min_value": 1 }                      │    │
│  │      }                                                   │    │
│  │    ]                                                     │    │
│  │  }                                                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  plugins/validators/gx_validator.py (wrapper)            │    │
│  │  ────────────────────────────────────                    │    │
│  │                                                          │    │
│  │  class GXValidator:                                      │    │
│  │      def __init__(self, table_name: str)                 │    │
│  │                                                          │    │
│  │      def validate_csv(csv_path: str) -> GXResult         │    │
│  │      def get_context() -> DataContext                    │    │
│  │      def build_data_docs() -> str                        │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

GX Validation Point in Pipeline:
════════════════════════════════

    ┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
    │  ORACLE  │────────▶│  EXTRACT │────────▶│TRANSFORM │────────▶│   LOAD   │
    │          │         │   CSV    │         │   CSV    │         │    SF    │
    └──────────┘         └──────────┘         └────┬─────┘         └──────────┘
                                                   │
                                                   ▼
                                              ┌──────────┐
                                              │   GX     │
                                              │ VALIDATE │  ← Validate before SF load
                                              │   CSV    │
                                              └──────────┘

Common Expectation Types Used:
══════════════════════════════

    Expectation Type                        Purpose
    ────────────────────────────────────    ─────────────────────────────────
    expect_column_values_to_not_be_null     Required fields (External ID, etc.)
    expect_column_values_to_be_unique       Primary key / External ID uniqueness
    expect_column_values_to_be_between      Numeric range (Amount, Price, etc.)
    expect_column_values_to_match_regex     Date format (ISO 8601), Code format
    expect_column_values_to_be_in_set       Picklist values validation
    expect_table_row_count_to_be_between    Row count sanity check
    expect_column_to_exist                  Ensure required columns exist
```

#### MODULE H: GX Expectation Files (`great_expectations/expectations/`)

```
┌─────────────────────────────────────────────────────────────────┐
│               GX EXPECTATION FILES (per table)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  great_expectations/expectations/                                │
│  │                                                               │
│  ├── 📄 kps_t_sales_md.json           # Sales Detail CSV         │
│  │       • expect_column_values_to_not_be_null: External_ID__c   │
│  │       • expect_column_values_to_be_unique: External_ID__c     │
│  │       • expect_column_values_to_be_between: Amount__c         │
│  │       • expect_column_values_to_match_regex: Sale_Date__c     │
│  │                                                               │
│  ├── 📄 kps_t_salespay_md.json        # Sales Payment CSV        │
│  │       • expect_column_values_to_not_be_null: External_ID__c   │
│  │       • expect_column_values_to_be_unique: External_ID__c     │
│  │                                                               │
│  ├── 📄 kps_t_sales_m.json            # Sales Master CSV         │
│  │       • expect_column_values_to_not_be_null: External_ID__c   │
│  │       • expect_column_values_to_be_unique: External_ID__c     │
│  │                                                               │
│  └── 📄 product_price.json            # Product Price CSV (POC)  │
│          • expect_column_values_to_not_be_null: ProductCode      │
│          • expect_column_values_to_be_unique: ProductCode        │
│          • expect_table_row_count_to_be_between: min=1           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

How to Add GX for a New Table:
══════════════════════════════

STEP 1: Create Expectation Suite
────────────────────────────────
File: great_expectations/expectations/{table}.json

{
  "expectation_suite_name": "{table}",
  "expectations": [
    {
      "expectation_type": "expect_column_values_to_not_be_null",
      "kwargs": { "column": "External_ID__c" }
    },
    {
      "expectation_type": "expect_column_values_to_be_unique",
      "kwargs": { "column": "External_ID__c" }
    },
    {
      "expectation_type": "expect_table_row_count_to_be_between",
      "kwargs": { "min_value": 1 }
    }
    // Add more expectations based on SF field requirements
  ]
}

STEP 2: Create Checkpoint (Optional)
────────────────────────────────────
File: great_expectations/checkpoints/{table}.yml

name: {table}_checkpoint
config_version: 1.0
validations:
  - batch_request:
      datasource_name: csv_staging
      data_asset_name: {table}.csv
    expectation_suite_name: {table}
action_list:
  - name: store_validation_result
    action:
      class_name: StoreValidationResultAction
  - name: update_data_docs
    action:
      class_name: UpdateDataDocsAction
```

---

### 13.3 How Modules Connect (Pipeline Flow)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              MODULE PIPELINE FLOW                                     │
│                                                                                       │
│  Developer A       Developer B       Developer C       Developer D       Developer E  │
│  ───────────       ───────────       ───────────       ───────────       ─────────── │
│  Config Module     Mapping Module    Plugin Modules    GX Module         DAG Layer    │
└──────────────────────────────────────────────────────────────────────────────────────┘

STEP 1: Setup Configuration (can be done independently by different developers)
═══════════════════════════════════════════════════════════════════════════════

  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
  │ tables_config  │  │ extract_config │  │ field_mappings │  │  GX suites     │
  │ ────────────── │  │ ────────────── │  │ ────────────── │  │ ────────────── │
  │                │  │                │  │                │  │                │
  │ Define:        │  │ Define:        │  │ Define:        │  │ Define:        │
  │ • Table name   │  │ • Chunk size   │  │ • Column map   │  │ • Expectations │
  │ • SF object    │  │ • Parallel deg │  │ • Type rules   │  │ • Checkpoints  │
  │ • External ID  │  │ • Fetch size   │  │ • SDL output   │  │ • Data docs    │
  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
          │                   │                   │                   │
          └───────────────────┴───────────────────┴───────────────────┘
                                          │
                                          ▼
STEP 2: Execute Pipeline Tasks (sequential in DAG)
═══════════════════════════════════════════════════

    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
    │          │     │          │     │   GX     │     │          │     │          │
    │ EXTRACT  │────▶│TRANSFORM │────▶│ VALIDATE │────▶│   LOAD   │────▶│ RECONCILE│
    │          │     │          │     │   CSV    │     │          │     │          │
    └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
         │                │                │                │                │
         ▼                ▼                ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ Oracle   │     │  Data    │     │   GX     │     │   SF     │     │  Data    │
    │Extractor │     │Transform │     │Validator │     │  Loader  │     │  Recon   │
    │          │     │          │     │          │     │          │     │          │
    │ Input:   │     │ Input:   │     │ Input:   │     │ Input:   │     │ Input:   │
    │ • config │     │ • csv    │     │ • csv    │     │ • csv    │     │ • table  │
    │          │     │ • mapping│     │ • suite  │     │ • config │     │          │
    │ Output:  │     │ Output:  │     │ Output:  │     │ Output:  │     │ Output:  │
    │ • csv    │     │ • csv    │     │ • result │     │ • result │     │ • report │
    └──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │  GX Data Docs    │
                                  │  (HTML Reports)  │
                                  └──────────────────┘

    GX validates CSV BEFORE loading to Salesforce to catch data quality issues early.

STEP 3: Module Interface Contract
═════════════════════════════════

    Module              Input                    Output                   Config Used
    ──────              ─────                    ──────                   ───────────
    Extractor           extract_config           csv_path (gzip)          extract_config.py
    Transformer         csv_path + mapping       csv_path (transformed)   field_mappings.py
    GX Validator        csv_path + suite_name    GXResult (pass/fail)     {table}.json
    Loader              csv_path + table_config  LoadResult               tables_config.py
    Reconciliation      table_name               ReconciliationReport     tables_config.py
```

---

### 13.4 Project Structure

```
kpc-tms-data-migration/
│
│   ╔═══════════════════════════════════════════════════════════════════════╗
│   ║                         DAG LAYER                                      ║
│   ╚═══════════════════════════════════════════════════════════════════════╝
│
├── 📂 dags/
│   │
│   ├── 📂 config/                              # ┌─────────────────────────┐
│   │   │                                       # │    CONFIG MODULE        │
│   │   ├── 📄 __init__.py                      # │                         │
│   │   ├── 📄 tables_config.py                 # │  • Table definitions    │
│   │   ├── 📄 extract_config.py                # │  • Extract parameters   │
│   │   └── 📄 field_mappings.py                # │  • Field mappings       │
│   │                                           # └─────────────────────────┘
│   │
│   ├── 📂 migrations/                          # ┌─────────────────────────┐
│   │   │                                       # │  TABLE DAGs             │
│   │   ├── 📄 migrate_sales_m_dag.py           # │  (1 Table = 1 DAG)      │
│   │   ├── 📄 migrate_sales_md_dag.py          # │                         │
│   │   ├── 📄 migrate_salespay_dag.py          # │  Each DAG imports:      │
│   │   ├── 📄 migrate_product_dag.py           # │  • config/*             │
│   │   └── 📄 ...                              # │  • plugins/*            │
│   │                                           # └─────────────────────────┘
│   │
│   ├── 📄 master_dag.py                        # Orchestrator DAG
│   └── 📄 reconciliation_dag.py                # Final validation DAG
│
│   ╔═══════════════════════════════════════════════════════════════════════╗
│   ║                       PLUGIN LAYER (Shared Logic)                      ║
│   ╚═══════════════════════════════════════════════════════════════════════╝
│
├── 📂 plugins/
│   │
│   ├── 📂 extractors/                          # ┌─────────────────────────┐
│   │   ├── 📄 __init__.py                      # │  EXTRACTOR MODULE       │
│   │   └── 📄 oracle_extractor.py              # │  • OracleExtractor      │
│   │                                           # │  • Parallel query       │
│   │                                           # │  • Chunking             │
│   │                                           # └─────────────────────────┘
│   │
│   ├── 📂 transformers/                        # ┌─────────────────────────┐
│   │   ├── 📄 __init__.py                      # │  TRANSFORMER MODULE     │
│   │   └── 📄 data_transformer.py              # │  • DataTransformer      │
│   │                                           # │  • Type conversion      │
│   │                                           # │  • Field mapping        │
│   │                                           # └─────────────────────────┘
│   │
│   ├── 📂 loaders/                             # ┌─────────────────────────┐
│   │   ├── 📄 __init__.py                      # │  LOADER MODULE          │
│   │   └── 📄 salesforce_bulk_loader.py        # │  • SalesforceBulkLoader │
│   │                                           # │  • Bulk API 2.0         │
│   │                                           # │  • Job management       │
│   │                                           # └─────────────────────────┘
│   │
│   ├── 📂 validators/                          # ┌─────────────────────────┐
│   │   ├── 📄 __init__.py                      # │  VALIDATOR MODULE       │
│   │   ├── 📄 reconciliation.py                # │  • DataReconciliation   │
│   │   └── 📄 gx_validator.py                  # │  • GXValidator wrapper  │
│   │                                           # │  • Count/Agg/Checksum   │
│   │                                           # └─────────────────────────┘
│   │
│   └── 📂 services/                            # ┌─────────────────────────┐
│       ├── 📄 __init__.py                      # │  SERVICE LAYER          │
│       ├── 📄 oracle_service.py                # │  • DB connections       │
│       └── 📄 salesforce_service.py            # │  • API clients          │
│                                               # └─────────────────────────┘
│
│   ╔═══════════════════════════════════════════════════════════════════════╗
│   ║                       MAPPING LAYER                                    ║
│   ╚═══════════════════════════════════════════════════════════════════════╝
│
├── 📂 salesforce/
│   │
│   ├── 📂 dataloader_conf/
│   │   │
│   │   ├── 📂 mappings/                        # ┌─────────────────────────┐
│   │   │   ├── 📄 Product2.sdl                 # │  SDL MAPPING FILES      │
│   │   │   ├── 📄 KPS_Sales__c.sdl             # │  (Auto-generated from   │
│   │   │   ├── 📄 KPS_SalesM__c.sdl            # │   field_mappings.py)    │
│   │   │   └── 📄 ...                          # │                         │
│   │   │                                       # └─────────────────────────┘
│   │   │
│   │   ├── 📄 process-conf.xml                 # Data Loader config
│   │   ├── 📄 config.properties                # SF connection (gitignored)
│   │   └── 📄 key.txt                          # Encryption key (gitignored)
│   │
│   ├── 📂 data/                                # Staging CSVs (gitignored)
│   └── 📂 logs/                                # Success/Error logs
│
│   ╔═══════════════════════════════════════════════════════════════════════╗
│   ║                   GREAT EXPECTATIONS LAYER (Data Quality)              ║
│   ╚═══════════════════════════════════════════════════════════════════════╝
│
├── 📂 great_expectations/                      # ┌─────────────────────────┐
│   │                                           # │  GX MODULE              │
│   ├── 📄 great_expectations.yml               # │  Core configuration     │
│   │                                           # │                         │
│   ├── 📂 expectations/                        # │  EXPECTATION SUITES     │
│   │   │                                       # │  (1 file per table)     │
│   │   ├── 📄 kps_t_sales_md.json              # │                         │
│   │   ├── 📄 kps_t_salespay_md.json           # │  Purpose:               │
│   │   ├── 📄 kps_t_sales_m.json               # │  Validate CSV before    │
│   │   └── 📄 product_price.json               # │  loading to Salesforce  │
│   │                                           # │                         │
│   │                                           # │  Naming: {table}.json   │
│   │                                           # └─────────────────────────┘
│   │
│   ├── 📂 checkpoints/                         # ┌─────────────────────────┐
│   │   ├── 📄 checkpoint_kps_t_sales_md.yml    # │  CHECKPOINT CONFIGS     │
│   │   ├── 📄 checkpoint_kps_t_salespay_md.yml # │  • Which suite to run   │
│   │   └── 📄 checkpoint_product_price.yml     # │  • Which datasource     │
│   │                                           # │  • Actions to take      │
│   │                                           # └─────────────────────────┘
│   │
│   └── 📂 uncommitted/                         # ┌─────────────────────────┐
│       ├── 📂 data_docs/                       # │  GENERATED OUTPUTS      │
│       │   └── 📂 local_site/                  # │  (gitignored)           │
│       │       ├── 📄 index.html               # │                         │
│       │       ├── 📂 expectations/            # │  • HTML reports         │
│       │       └── 📂 validations/             # │  • Validation results   │
│       │                                       # │                         │
│       └── 📂 validations/                     # │  JSON validation logs   │
│           └── 📂 {suite_name}/                # │                         │
│               └── 📂 {run_id}/                # │                         │
│                   └── 📄 validation.json      # │                         │
│                                               # └─────────────────────────┘
│
│   ╔═══════════════════════════════════════════════════════════════════════╗
│   ║                       INFRASTRUCTURE                                   ║
│   ╚═══════════════════════════════════════════════════════════════════════╝
│
├── 📂 config/
│   └── 📄 airflow.cfg                          # Airflow settings
│
├── 📂 scripts/
│   ├── 📄 generate_sdl.py                      # Generate SDL from mappings
│   ├── 📄 setup_dataloader.sh                  # Initialize Data Loader
│   └── 📄 encrypt_password.sh                  # Encrypt SF password
│
├── 📂 tests/
│   ├── 📄 test_oracle_extractor.py
│   ├── 📄 test_data_transformer.py
│   ├── 📄 test_salesforce_loader.py
│   └── 📄 test_reconciliation.py
│
├── 📂 docs/
│   ├── 📄 ARCHITECTURE.md
│   ├── 📄 PIPELINE_DESIGN.md
│   └── 📄 ...
│
├── 📄 docker-compose.yaml
├── 📄 Dockerfile
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 CLAUDE.md
└── 📄 README.md
```

---

### 13.5 Adding a New Table (Step-by-Step)

To add a new table migration, follow these steps:

```
STEP 1: Add Table Config
════════════════════════
File: dags/config/tables_config.py

    TABLE_CONFIG["NEW_TABLE"] = {
        "source_table": "NEW_TABLE",
        "sf_object": "New_Object__c",
        "external_id": "External_ID__c",
        "priority": "medium"
    }

STEP 2: Add Extract Config
══════════════════════════
File: dags/config/extract_config.py

    EXTRACT_CONFIG["NEW_TABLE"] = {
        "chunk_size": 500_000,
        "parallel_workers": 10,
        "parallel_degree": 8
    }

STEP 3: Add Field Mapping
═════════════════════════
File: dags/config/field_mappings.py

    FIELD_MAPPINGS["NEW_TABLE"] = {
        "mappings": {
            "COL_A": "Field_A__c",
            "COL_B": "Field_B__c"
        },
        "transforms": {
            "COL_A": "to_sf_datetime"
        }
    }

STEP 4: Generate SDL File
═════════════════════════
Command: python scripts/generate_sdl.py NEW_TABLE

    Output: salesforce/dataloader_conf/mappings/New_Object__c.sdl

STEP 5: Create DAG File
═══════════════════════
File: dags/migrations/migrate_new_table_dag.py

    TABLE_NAME = "NEW_TABLE"
    # Copy template from existing DAG

STEP 6: Add GX Expectations (Validates CSV before SF load)
═══════════════════════════════════════════════════════════
File: great_expectations/expectations/new_table.json

    {
      "expectation_suite_name": "new_table",
      "expectations": [
        { "expectation_type": "expect_column_values_to_not_be_null",
          "kwargs": { "column": "External_ID__c" } },
        { "expectation_type": "expect_column_values_to_be_unique",
          "kwargs": { "column": "External_ID__c" } },
        { "expectation_type": "expect_table_row_count_to_be_between",
          "kwargs": { "min_value": 1 } }
      ]
    }

DONE! ✓
```

---

### 13.6 DAG Template

```python
# dags/migrations/migrate_{table}_dag.py

from airflow.sdk import DAG, task
from plugins.extractors.oracle_extractor import OracleExtractor
from plugins.transformers.data_transformer import DataTransformer
from plugins.loaders.salesforce_bulk_loader import SalesforceBulkLoader
from plugins.validators.reconciliation import DataReconciliation
from dags.config.tables_config import TABLE_CONFIG
from dags.config.field_mappings import FIELD_MAPPINGS
from dags.config.extract_config import EXTRACT_CONFIG

# ┌─────────────────────────────────────────────────────────┐
# │  ONLY CHANGE THIS LINE FOR EACH TABLE                   │
# └─────────────────────────────────────────────────────────┘
TABLE_NAME = "KPS_T_SALES_MD"

with DAG(
    dag_id=f"migrate_{TABLE_NAME.lower()}",
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["migration", TABLE_NAME],
):
    @task
    def extract():
        """Extract data from Oracle to CSV."""
        config = EXTRACT_CONFIG[TABLE_NAME]
        extractor = OracleExtractor(config)
        return extractor.extract_to_csv()

    @task
    def transform(csv_path: str):
        """Transform data for Salesforce compatibility."""
        mapping = FIELD_MAPPINGS[TABLE_NAME]
        transformer = DataTransformer(mapping)
        return transformer.transform(csv_path)

    @task
    def load(csv_path: str):
        """Load data to Salesforce via Bulk API 2.0."""
        config = TABLE_CONFIG[TABLE_NAME]
        loader = SalesforceBulkLoader(config)
        return loader.upsert(csv_path)

    @task
    def validate(load_result: dict):
        """Validate data integrity post-migration."""
        recon = DataReconciliation(TABLE_NAME)
        return recon.run_all_checks()

    # Pipeline: extract → transform → load → validate
    csv = extract()
    transformed = transform(csv)
    result = load(transformed)
    validate(result)
```

### 13.2 Key Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yaml` | Service definitions |
| `.env` | Environment variables |
| `config/airflow.cfg` | Airflow settings |
| `dags/config/tables_config.py` | Table definitions |
| `great_expectations/great_expectations.yml` | GX configuration |

### 13.3 Useful Commands Reference

```bash
# Airflow Commands
airflow dags list                    # List all DAGs
airflow dags trigger <dag_id>        # Trigger DAG
airflow tasks list <dag_id>          # List tasks in DAG
airflow tasks test <dag_id> <task>   # Test single task

# Docker Commands
docker compose up -d                 # Start services
docker compose down                  # Stop services
docker compose logs -f <service>     # View logs
docker compose exec <service> bash   # Shell access

# Great Expectations Commands
great_expectations suite list        # List expectation suites
great_expectations checkpoint run    # Run validation checkpoint
great_expectations docs build        # Build data docs
```

### 13.4 Related Documentation

| Document | Location | Description |
|----------|----------|-------------|
| Architecture Design | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design details |
| Pipeline Design | [docs/PIPELINE_DESIGN.md](docs/PIPELINE_DESIGN.md) | Implementation specifics |
| Migration Checklist | [docs/MIGRATION_CHECKLIST.md](docs/MIGRATION_CHECKLIST.md) | Pre/Post tasks |
| GX Guide | [docs/GREAT_EXPECTATIONS_GUIDE.md](docs/GREAT_EXPECTATIONS_GUIDE.md) | Validation setup |
| Airflow Best Practices | [docs/AIRFLOW_BEST_PRACTICES.md](docs/AIRFLOW_BEST_PRACTICES.md) | Coding standards |

### 13.5 Contact & Support

| Role | Responsibility |
|------|----------------|
| Data Engineering Team | Pipeline development, troubleshooting |
| Salesforce Admin | Org configuration, validation |
| Infrastructure Team | Environment provisioning, networking |
| Project Manager | Timeline, coordination, escalation |

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | Jan 2026 | Data Engineering Team | Initial POC documentation |

---

*This document serves as the primary reference for the KPC TMS Data Migration project. For questions or updates, contact the Data Engineering team.*
