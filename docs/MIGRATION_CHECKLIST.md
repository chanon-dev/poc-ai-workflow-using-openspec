# Data Migration Expert Checklist

> จากประสบการณ์ Data Migration มากกว่า 100+ projects

---

## ⚠️ Critical: Audit Log เป็น MUST-HAVE

### ทำไมต้องมี Audit Log?

| เหตุผล | ความสำคัญ |
| --- | --- |
| **Compliance** | SOX, PDPA, GDPR ต้องการ audit trail | 🔴 Critical |
| **Troubleshooting** | หา root cause เมื่อ data หาย | 🔴 Critical |
| **Rollback** | ต้องรู้ว่า record ไหนถูก migrate ไปแล้ว | 🔴 Critical |
| **Reconciliation** | เปรียบเทียบ source vs target | 🟡 High |
| **Performance tuning** | วิเคราะห์ bottleneck | 🟢 Medium |

### Audit Log Schema

```sql
-- Oracle: สร้างตาราง Audit Log
CREATE TABLE MIGRATION_AUDIT_LOG (
    AUDIT_ID            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    BATCH_ID            VARCHAR2(50) NOT NULL,      -- Airflow run_id
    TABLE_NAME          VARCHAR2(100) NOT NULL,
    CHUNK_ID            NUMBER,

    -- Timestamps
    START_TIME          TIMESTAMP DEFAULT SYSTIMESTAMP,
    END_TIME            TIMESTAMP,
    DURATION_SECONDS    NUMBER,

    -- Counts
    SOURCE_COUNT        NUMBER,
    EXTRACTED_COUNT     NUMBER,
    TRANSFORMED_COUNT   NUMBER,
    LOADED_COUNT        NUMBER,
    SUCCESS_COUNT       NUMBER,
    FAILED_COUNT        NUMBER,
    SKIPPED_COUNT       NUMBER,

    -- Status
    STATUS              VARCHAR2(20),  -- RUNNING, SUCCESS, FAILED, PARTIAL
    ERROR_MESSAGE       VARCHAR2(4000),
    ERROR_DETAILS       CLOB,

    -- Metadata
    SF_JOB_ID           VARCHAR2(50),
    SF_BATCH_ID         VARCHAR2(50),
    CSV_FILE_PATH       VARCHAR2(500),
    CSV_FILE_SIZE_MB    NUMBER,

    -- Checksums
    SOURCE_CHECKSUM     VARCHAR2(64),
    TARGET_CHECKSUM     VARCHAR2(64),

    -- Created
    CREATED_BY          VARCHAR2(100) DEFAULT 'AIRFLOW',
    CREATED_DATE        TIMESTAMP DEFAULT SYSTIMESTAMP
);

-- Index for fast queries
CREATE INDEX IDX_AUDIT_BATCH ON MIGRATION_AUDIT_LOG(BATCH_ID);
CREATE INDEX IDX_AUDIT_TABLE ON MIGRATION_AUDIT_LOG(TABLE_NAME);
CREATE INDEX IDX_AUDIT_STATUS ON MIGRATION_AUDIT_LOG(STATUS);
CREATE INDEX IDX_AUDIT_DATE ON MIGRATION_AUDIT_LOG(CREATED_DATE);
```

### Audit Log สำหรับ Failed Records

```sql
-- เก็บ record ที่ fail เพื่อ retry
CREATE TABLE MIGRATION_FAILED_RECORDS (
    FAILED_ID           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    AUDIT_ID            NUMBER REFERENCES MIGRATION_AUDIT_LOG(AUDIT_ID),
    TABLE_NAME          VARCHAR2(100) NOT NULL,
    RECORD_ID           VARCHAR2(100) NOT NULL,     -- Primary key ของ record

    -- Error details
    SF_ERROR_CODE       VARCHAR2(50),
    SF_ERROR_MESSAGE    VARCHAR2(4000),
    SF_ERROR_FIELDS     VARCHAR2(1000),

    -- Retry tracking
    RETRY_COUNT         NUMBER DEFAULT 0,
    LAST_RETRY_DATE     TIMESTAMP,
    RESOLVED            CHAR(1) DEFAULT 'N',
    RESOLVED_DATE       TIMESTAMP,
    RESOLUTION_NOTES    VARCHAR2(4000),

    -- Original data (for debugging)
    RECORD_DATA         CLOB,  -- JSON format

    CREATED_DATE        TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE INDEX IDX_FAILED_TABLE ON MIGRATION_FAILED_RECORDS(TABLE_NAME);
CREATE INDEX IDX_FAILED_RESOLVED ON MIGRATION_FAILED_RECORDS(RESOLVED);
```

---

## 📋 Pre-Migration Checklist

### 1. Data Profiling (ก่อน migrate ต้องรู้จัก data)

```sql
-- Run data profiling script for each table
SELECT
    'KPS_T_SALES_MD' as table_name,
    COUNT(*) as total_rows,
    COUNT(DISTINCT SALES_ID) as unique_keys,
    MIN(CREATED_DATE) as min_date,
    MAX(CREATED_DATE) as max_date,
    SUM(CASE WHEN SALES_ID IS NULL THEN 1 ELSE 0 END) as null_keys,
    SUM(CASE WHEN SALES_AMOUNT IS NULL THEN 1 ELSE 0 END) as null_amounts,
    AVG(LENGTH(DESCRIPTION)) as avg_desc_length,
    MAX(LENGTH(DESCRIPTION)) as max_desc_length
FROM KPS_T_SALES_MD;
```

| Check | ทำไมสำคัญ | Action ถ้าพบปัญหา |
| --- | --- | --- |
| **Null Primary Keys** | SF ต้องการ External ID | Clean data ก่อน migrate |
| **Duplicate Keys** | Upsert จะ update แทน insert | Decide: keep latest or merge? |
| **Data Length** | SF field มี length limit | Truncate หรือ reject |
| **Invalid Dates** | SF ไม่รับ date ก่อน 1700 | Transform to null |
| **Special Characters** | CSV parsing issues | Escape หรือ remove |
| **Encoding Issues** | UTF-8 vs Thai encoding | Convert to UTF-8 |

### 2. Salesforce Preparation

| Task | Command/Action | ตรวจสอบ |
| --- | --- | --- |
| ✅ Check API limits | Setup > Company Info > API Requests | มี quota พอไหม |
| ✅ Check storage | Setup > Storage Usage | มี space พอไหม |
| ✅ Create External ID field | Deploy custom field | Index ถูกสร้างไหม |
| ✅ Disable triggers | Deactivate all triggers | ทุก trigger ถูก disable |
| ✅ Disable workflows | Deactivate workflow rules | ทุก workflow ถูก disable |
| ✅ Disable validation rules | Deactivate validation | ทุก rule ถูก disable |
| ✅ Disable duplicate rules | Deactivate duplicate rules | ทุก rule ถูก disable |
| ✅ Increase field history | Setup > Field History | ถ้าต้องการ track changes |

### 3. Infrastructure Preparation

```bash
# Check disk space
df -h /data/staging

# Check Oracle connectivity
sqlplus kpc_user/password@KPCPROD <<< "SELECT 1 FROM DUAL;"

# Check Salesforce connectivity
sf org display --target-org production

# Check Airflow workers
docker compose exec airflow-worker celery inspect ping

# Check Redis
redis-cli ping
```

### 4. Backup Strategy

```sql
-- Oracle: Create backup table for critical data
CREATE TABLE KPS_T_SALES_MD_BKP_20240115 AS
SELECT * FROM KPS_T_SALES_MD
WHERE CREATED_DATE >= DATE '2022-01-01';

-- Record backup info
INSERT INTO MIGRATION_BACKUP_LOG (TABLE_NAME, BACKUP_TABLE, ROW_COUNT, CREATED_DATE)
VALUES ('KPS_T_SALES_MD', 'KPS_T_SALES_MD_BKP_20240115', 261000000, SYSDATE);
```

---

## 🚨 สิ่งที่ต้องระวัง (Common Pitfalls)

### 1. Data Quality Issues

| ปัญหา | ผลกระทบ | วิธีป้องกัน |
| --- | --- | --- |
| **Orphan records** | FK ไม่มี parent ใน SF | Load parent ก่อน child |
| **Circular references** | A→B→A | Break cycle, load in phases |
| **Duplicate External IDs** | Upsert ทับ data | De-duplicate ก่อน migrate |
| **Future dates** | SF อาจ reject | Validate date range |
| **Negative amounts** | Business logic error? | Verify with business |
| **Empty required fields** | SF validation fail | Default value หรือ reject |

### 2. Performance Pitfalls

| ปัญหา | สัญญาณ | วิธีแก้ |
| --- | --- | --- |
| **Oracle full table scan** | Query > 30 mins | Add index, use partition |
| **Memory overflow** | Worker OOM killed | Reduce chunk size |
| **Network timeout** | Connection reset | Retry with backoff |
| **SF API throttling** | 429 Too Many Requests | Reduce parallel jobs |
| **Disk full** | No space left | Monitor, auto-cleanup |

### 3. Salesforce-Specific Issues

| ปัญหา | Error Message | วิธีแก้ |
| --- | --- | --- |
| **Record locked** | UNABLE_TO_LOCK_ROW | Retry with delay |
| **Governor limits** | Too many SOQL queries | Batch operations |
| **Trigger recursion** | Maximum trigger depth | Disable triggers |
| **Field not writable** | Field is not writeable | Check field permissions |
| **Invalid reference** | INVALID_CROSS_REFERENCE_KEY | Load parent first |
| **Required field** | REQUIRED_FIELD_MISSING | Map or provide default |

---

## 📊 During Migration Monitoring

### Real-time Dashboard Queries

```sql
-- Current migration status
SELECT
    TABLE_NAME,
    STATUS,
    COUNT(*) as chunks,
    SUM(SOURCE_COUNT) as total_source,
    SUM(SUCCESS_COUNT) as total_success,
    SUM(FAILED_COUNT) as total_failed,
    ROUND(SUM(SUCCESS_COUNT) / NULLIF(SUM(SOURCE_COUNT), 0) * 100, 2) as success_rate,
    MIN(START_TIME) as started,
    MAX(END_TIME) as last_update
FROM MIGRATION_AUDIT_LOG
WHERE BATCH_ID = :current_batch_id
GROUP BY TABLE_NAME, STATUS
ORDER BY TABLE_NAME;

-- Failed records summary
SELECT
    TABLE_NAME,
    SF_ERROR_CODE,
    COUNT(*) as error_count,
    MIN(SF_ERROR_MESSAGE) as sample_message
FROM MIGRATION_FAILED_RECORDS
WHERE AUDIT_ID IN (
    SELECT AUDIT_ID FROM MIGRATION_AUDIT_LOG
    WHERE BATCH_ID = :current_batch_id
)
GROUP BY TABLE_NAME, SF_ERROR_CODE
ORDER BY error_count DESC;

-- Performance metrics
SELECT
    TABLE_NAME,
    ROUND(AVG(EXTRACTED_COUNT / NULLIF(DURATION_SECONDS, 0)), 0) as avg_records_per_sec,
    ROUND(AVG(DURATION_SECONDS), 1) as avg_chunk_duration,
    MAX(DURATION_SECONDS) as max_chunk_duration
FROM MIGRATION_AUDIT_LOG
WHERE BATCH_ID = :current_batch_id
  AND STATUS = 'SUCCESS'
GROUP BY TABLE_NAME;
```

### Alert Thresholds

```python
# config/alert_thresholds.py

ALERT_THRESHOLDS = {
    # Fail rate alerts
    "fail_rate_warning": 1.0,      # > 1% failed records
    "fail_rate_critical": 5.0,     # > 5% failed records

    # Performance alerts
    "chunk_duration_warning": 600,  # > 10 minutes per chunk
    "chunk_duration_critical": 1800, # > 30 minutes per chunk

    # Throughput alerts
    "min_records_per_sec": 1000,    # < 1000 records/sec

    # Disk space alerts
    "disk_usage_warning": 80,       # > 80% disk used
    "disk_usage_critical": 95,      # > 95% disk used

    # Queue alerts
    "pending_chunks_warning": 100,  # > 100 chunks waiting

    # Stale job alerts
    "job_stale_minutes": 60,        # No progress for 60 mins
}
```

### Health Check Script

```python
# plugins/health_check.py

def check_migration_health(batch_id: str) -> dict:
    """Run health checks during migration"""

    checks = {
        "timestamp": datetime.now().isoformat(),
        "batch_id": batch_id,
        "status": "HEALTHY",
        "issues": []
    }

    # 1. Check fail rate
    fail_rate = get_current_fail_rate(batch_id)
    if fail_rate > ALERT_THRESHOLDS["fail_rate_critical"]:
        checks["status"] = "CRITICAL"
        checks["issues"].append(f"Fail rate {fail_rate}% exceeds critical threshold")
    elif fail_rate > ALERT_THRESHOLDS["fail_rate_warning"]:
        checks["status"] = "WARNING"
        checks["issues"].append(f"Fail rate {fail_rate}% exceeds warning threshold")

    # 2. Check disk space
    disk_usage = get_disk_usage("/data/staging")
    if disk_usage > ALERT_THRESHOLDS["disk_usage_critical"]:
        checks["status"] = "CRITICAL"
        checks["issues"].append(f"Disk usage {disk_usage}% critical")

    # 3. Check stale jobs
    stale_jobs = get_stale_jobs(batch_id, minutes=60)
    if stale_jobs:
        checks["status"] = "WARNING"
        checks["issues"].append(f"{len(stale_jobs)} stale jobs detected")

    # 4. Check SF API limits
    api_remaining = get_sf_api_remaining()
    if api_remaining < 1000:
        checks["status"] = "WARNING"
        checks["issues"].append(f"Only {api_remaining} API calls remaining")

    return checks
```

---

## ✅ Post-Migration Validation

### Level 1: Count Validation (ต้องทำเสมอ)

```python
def validate_counts(table_name: str, sf_object: str) -> dict:
    """Compare record counts between Oracle and Salesforce"""

    oracle_count = oracle_hook.get_first(
        f"SELECT COUNT(*) FROM {table_name} WHERE CREATED_DATE >= :start",
        {"start": migration_start_date}
    )[0]

    sf_count = sf_hook.query(
        f"SELECT COUNT(Id) FROM {sf_object} WHERE Oracle_Created_Date__c >= {migration_start_date}"
    )["totalSize"]

    return {
        "table": table_name,
        "oracle_count": oracle_count,
        "sf_count": sf_count,
        "difference": oracle_count - sf_count,
        "match": oracle_count == sf_count,
        "match_rate": sf_count / oracle_count * 100 if oracle_count > 0 else 0
    }
```

### Level 2: Aggregate Validation (แนะนำ)

```python
def validate_aggregates(table_name: str, sf_object: str,
                        amount_col: str, sf_amount_field: str) -> dict:
    """Compare sum of numeric fields"""

    oracle_sum = oracle_hook.get_first(
        f"SELECT SUM({amount_col}), AVG({amount_col}) FROM {table_name}"
    )

    sf_result = sf_hook.query(
        f"SELECT SUM({sf_amount_field}), AVG({sf_amount_field}) FROM {sf_object}"
    )

    oracle_total = oracle_sum[0] or 0
    sf_total = sf_result["records"][0].get("expr0") or 0

    variance = abs(oracle_total - sf_total)
    variance_pct = variance / oracle_total * 100 if oracle_total > 0 else 0

    return {
        "table": table_name,
        "oracle_sum": oracle_total,
        "sf_sum": sf_total,
        "variance": variance,
        "variance_pct": variance_pct,
        "acceptable": variance_pct < 0.01  # < 0.01% variance
    }
```

### Level 3: Sample Record Validation (สุ่มตรวจ)

```python
def validate_sample_records(table_name: str, sf_object: str,
                            key_column: str, sample_size: int = 100) -> dict:
    """Compare actual field values for sample records"""

    # Get random sample
    sample_keys = oracle_hook.get_records(
        f"""SELECT {key_column} FROM (
            SELECT {key_column} FROM {table_name} ORDER BY DBMS_RANDOM.VALUE
        ) WHERE ROWNUM <= :size""",
        {"size": sample_size}
    )

    mismatches = []

    for key in sample_keys:
        oracle_record = get_oracle_record(table_name, key_column, key[0])
        sf_record = get_sf_record(sf_object, "External_ID__c", key[0])

        # Compare each field
        for oracle_col, sf_field in FIELD_MAPPINGS[table_name]["mappings"].items():
            oracle_val = oracle_record.get(oracle_col)
            sf_val = sf_record.get(sf_field)

            if not values_match(oracle_val, sf_val):
                mismatches.append({
                    "key": key[0],
                    "field": sf_field,
                    "oracle_value": oracle_val,
                    "sf_value": sf_val
                })

    return {
        "sample_size": sample_size,
        "mismatches": len(mismatches),
        "mismatch_details": mismatches[:10],  # First 10 for review
        "match_rate": (sample_size - len(mismatches)) / sample_size * 100
    }
```

### Level 4: Business Logic Validation (ถ้ามีเวลา)

```python
def validate_business_rules(table_name: str) -> list:
    """Validate business rules are preserved"""

    validations = []

    # Example: Total sales per tenant should match
    oracle_by_tenant = oracle_hook.get_records("""
        SELECT TENANT_CODE, SUM(SALES_AMOUNT) as total
        FROM KPS_T_SALES_MD
        GROUP BY TENANT_CODE
    """)

    for tenant, oracle_total in oracle_by_tenant:
        sf_result = sf_hook.query(f"""
            SELECT SUM(Sales_Amount__c) total
            FROM KPS_Sales__c
            WHERE Tenant_Code__c = '{tenant}'
        """)
        sf_total = sf_result["records"][0].get("total") or 0

        if abs(oracle_total - sf_total) > 0.01:
            validations.append({
                "rule": "tenant_sales_total",
                "tenant": tenant,
                "oracle": oracle_total,
                "sf": sf_total,
                "status": "FAIL"
            })

    return validations
```

---

## 🔄 Rollback Strategy

### When to Rollback?

| Scenario | Threshold | Action |
| --- | --- | --- |
| Fail rate > 10% | 10% of records failed | Pause and investigate |
| Data corruption detected | Any checksum mismatch | Stop immediately |
| SF system down | API unavailable > 30 mins | Pause, wait, retry |
| Wrong data loaded | Business reports wrong | Full rollback |

### Rollback Options

#### Option 1: Delete and Retry (Recommended for partial failure)

```python
def rollback_failed_batch(batch_id: str, sf_object: str):
    """Delete records from failed batch and retry"""

    # Get External IDs from this batch
    records = oracle_hook.get_records("""
        SELECT RECORD_ID FROM MIGRATION_AUDIT_LOG
        WHERE BATCH_ID = :batch_id AND STATUS = 'SUCCESS'
    """, {"batch_id": batch_id})

    # Delete from Salesforce
    external_ids = [r[0] for r in records]

    # Use Bulk API delete
    delete_job = sf_bulk.create_job(sf_object, "delete")
    sf_bulk.upload_data(delete_job, external_ids)
    sf_bulk.close_job(delete_job)

    # Update audit log
    oracle_hook.run("""
        UPDATE MIGRATION_AUDIT_LOG
        SET STATUS = 'ROLLED_BACK', END_TIME = SYSTIMESTAMP
        WHERE BATCH_ID = :batch_id
    """, {"batch_id": batch_id})
```

#### Option 2: Full Table Rollback (Nuclear option)

```python
def full_rollback(sf_object: str, cutoff_date: str):
    """Delete all records after cutoff date"""

    # Query all records to delete
    query = f"""
        SELECT Id FROM {sf_object}
        WHERE Oracle_Created_Date__c >= {cutoff_date}
    """

    # Export IDs
    records = sf_bulk.query(query)

    # Bulk delete
    delete_job = sf_bulk.create_job(sf_object, "hardDelete")
    # ... upload and process

    # Log rollback
    log_rollback_event(sf_object, cutoff_date, len(records))
```

### Rollback Checklist

- [ ] Stop all running migration jobs
- [ ] Document the reason for rollback
- [ ] Identify affected records (batch_id, date range)
- [ ] Export affected SF record IDs
- [ ] Perform delete via Bulk API
- [ ] Verify deletion complete
- [ ] Update audit log status to ROLLED_BACK
- [ ] Fix root cause
- [ ] Re-run migration from checkpoint

---

## 📈 Final Report Template

```markdown
# Data Migration Report

## Executive Summary
- **Project:** KPC TMS Data Migration
- **Date:** 2024-01-15 to 2024-01-17
- **Status:** ✅ SUCCESS / ⚠️ PARTIAL / ❌ FAILED

## Migration Statistics

| Table | Source | Target | Success | Failed | Rate |
|-------|--------|--------|---------|--------|------|
| KPS_T_SALES_MD | 261,000,000 | 260,995,432 | 260,995,432 | 4,568 | 99.998% |
| KPS_T_SALESPAY_MD | 109,000,000 | 109,000,000 | 109,000,000 | 0 | 100% |
| ... | ... | ... | ... | ... | ... |
| **TOTAL** | **481,000,000** | **480,995,432** | **480,995,432** | **4,568** | **99.999%** |

## Reconciliation Results

| Check | Status | Details |
|-------|--------|---------|
| Count Match | ✅ PASS | 99.999% match |
| Sum Match | ✅ PASS | Variance < 0.001% |
| Sample Check | ✅ PASS | 100/100 records matched |

## Issues Encountered

1. **Issue:** 4,568 records failed with INVALID_FIELD_FOR_INSERT
   - **Root Cause:** Description field exceeded 32KB limit
   - **Resolution:** Truncated to 32KB
   - **Records Fixed:** 4,568

## Performance Metrics

| Metric | Value |
|--------|-------|
| Total Duration | 46 hours 23 minutes |
| Average Throughput | 2,883 records/second |
| Peak Throughput | 4,521 records/second |
| SF API Calls Used | 12,847 |

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Data Engineer | | | |
| DBA | | | |
| Business Owner | | | |
| QA Lead | | | |
```

---

## 🎯 Expert Tips

### 1. ทำ Dry Run ก่อนเสมอ

```bash
# Test with 1% of data first
airflow dags trigger migrate_kps_t_sales_md \
  --conf '{"sample_percent": 1, "dry_run": true}'
```

### 2. มี Kill Switch

```python
# Check for stop signal before each chunk
def should_stop_migration():
    return Variable.get("MIGRATION_STOP_FLAG", "false") == "true"

@task()
def process_chunk(chunk):
    if should_stop_migration():
        raise AirflowSkipException("Migration stopped by operator")
    # continue processing...
```

### 3. Incremental Checkpoints

```python
# Save progress every N chunks
@task()
def save_checkpoint(chunk_id: int, batch_id: str):
    Variable.set(f"CHECKPOINT_{batch_id}", chunk_id)

# Resume from checkpoint
def get_resume_point(batch_id: str) -> int:
    return int(Variable.get(f"CHECKPOINT_{batch_id}", 0))
```

### 4. Communication Plan

| Event | Who to Notify | Channel |
| --- | --- | --- |
| Migration Started | Team, Stakeholders | Slack, Email |
| 50% Complete | Team | Slack |
| Error Rate > 1% | Team Lead | Slack, Phone |
| Migration Paused | Everyone | Slack, Email |
| Migration Complete | Everyone | Slack, Email |
| Rollback Initiated | Management | Phone, Email |

---

## Summary Checklist

### Before Migration

- [ ] Data profiling complete
- [ ] Audit tables created
- [ ] Backup taken
- [ ] SF triggers/workflows disabled
- [ ] Dry run successful
- [ ] Stakeholder sign-off

### During Migration

- [ ] Monitor dashboard active
- [ ] Alert thresholds configured
- [ ] On-call person assigned
- [ ] Kill switch ready

### After Migration

- [ ] Count validation passed
- [ ] Aggregate validation passed
- [ ] Sample validation passed
- [ ] Business rules validated
- [ ] SF triggers/workflows re-enabled
- [ ] Final report generated
- [ ] Stakeholder sign-off
