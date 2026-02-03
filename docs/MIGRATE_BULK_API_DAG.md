# migrate_bulk_api DAG

Migrate data from Oracle to Salesforce via Bulk API 2.0.

**DAG ID:** `migrate_bulk_api`
**Schedule:** Manual trigger only
**File:** `dags/migrate_bulk_api_dag.py`

## Pipeline Overview

```
authenticate ──┐
                ├──► upload_batches ──► collect_results
extract_data ──┘
```

| Step | Task | Description |
|------|------|-------------|
| 1 | `authenticate` | OAuth 2.0 Client Credentials → access_token |
| 2 | `extract_data` | Query Oracle → CSV batch files |
| 3 | `upload_batches` | Upload CSVs via Bulk API 2.0 (parallel) |
| 4 | `collect_results` | Fetch success/failed/unprocessed result CSVs |

Steps 1 and 2 run in parallel. Steps 3 and 4 run sequentially after both complete.

## Dependencies

| Plugin | Purpose |
|--------|---------|
| `plugins/salesforce_auth.py` | OAuth 2.0 authentication |
| `plugins/salesforce_bulk_loader.py` | Bulk API 2.0 upload |
| `plugins/migration_logger.py` | DB logging to PostgreSQL |

## Airflow Connections

| conn_id | Type | Purpose |
|---------|------|---------|
| `salesforce_api` | HTTP | Salesforce OAuth (client_id / client_secret) |
| `oracle_kpc` | Oracle | Source database |
| `airflow_db` | Postgres | Migration logging tables |

## DAG Config Parameters

Trigger via CLI:

```bash
airflow dags trigger migrate_bulk_api --conf '{
  "sf_object": "TMS_Request__c",
  "operation": "insert",
  "column_mapping": {
    "CON_CODE": "Name",
    "SHOP_CODE": "TMS_Shop_Brand_Name__c",
    "BRANCH_CODE": "TMS_Location__c"
  }
}'
```

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `sf_object` | Target Salesforce object (e.g. `TMS_Request__c`, `KPS_Sales__c`) |

### Conditional Parameters

| Parameter | When Required | Description |
|-----------|---------------|-------------|
| `external_id_field` | `operation = upsert` | External ID field for upsert (e.g. `External_Id__c`) |

### Optional Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `operation` | `upsert` | Bulk API operation: `insert`, `upsert`, `update`, `delete` |
| `table_name` | `KPS_T_SALES_MD` | Oracle source table |
| `batch_size` | `40000` | Records per batch CSV file |
| `start_batch` | `1` | Resume from batch N (skip earlier batches) |
| `extract_query` | `SELECT * FROM {table_name} WHERE ROWNUM <= 10` | Custom SQL query |
| `column_mapping` | `null` | Map Oracle columns to SF fields (see below) |
| `sf_conn_id` | `salesforce_api` | Airflow connection ID for Salesforce |

### Column Mapping

When Oracle column names don't match Salesforce field names, use `column_mapping` to rename and filter columns:

```json
{
  "column_mapping": {
    "ORACLE_COLUMN": "SF_Field_API_Name__c",
    "CON_CODE": "Name",
    "SHOP_CODE": "TMS_Shop_Brand_Name__c"
  }
}
```

- Only mapped columns are included in the CSV sent to Salesforce
- Unmapped columns are dropped
- Oracle column names are case-insensitive (auto-uppercased)

## Task Details

### Step 1: authenticate

- Uses `salesforce_auth.get_salesforce_token()` with OAuth 2.0 Client Credentials flow
- Returns `instance_url` and `access_token` via XCom

### Step 2: extract_data

1. Connects to Oracle via `OracleHook` (conn_id: `oracle_kpc`)
2. Executes SQL query → Pandas DataFrame
3. Applies `column_mapping` if provided (rename + filter columns)
4. Splits DataFrame into batch CSV files (size = `batch_size`)
5. Writes CSVs to `salesforce/data/{table_name}_batch_NNN.csv`
6. Logs run start to `migration.runs` table

### Step 3: upload_batches

1. Creates Bulk API 2.0 ingest job per batch file
2. Single batch: direct upload; Multiple batches: parallel upload (max 15 concurrent)
3. Polls job status until `JobComplete` or `Failed`
4. Logs each batch to `migration.batch_logs` table

### Step 4: collect_results

1. Fetches result CSVs from Salesforce for each completed job:
   - `successfulResults` → `{job_id}_success.csv`
   - `failedResults` → `{job_id}_failed.csv`
   - `unprocessedrecords` → `{job_id}_unprocessed.csv`
2. Saves to `salesforce/logs/`
3. Updates `migration.runs` with final status (`success`, `partial`, `failed`)

## Output Files

```
salesforce/
├── data/
│   ├── KPS_T_SALES_MD_batch_001.csv
│   ├── KPS_T_SALES_MD_batch_002.csv
│   └── ...
└── logs/
    ├── {job_id}_success.csv
    ├── {job_id}_failed.csv
    └── {job_id}_unprocessed.csv
```

## Database Logging

Migration progress is tracked in PostgreSQL (`airflow_db` connection):

### migration.runs

| Column | Description |
|--------|-------------|
| `run_id` | Airflow DAG run ID |
| `dag_id` | `migrate_bulk_api` |
| `table_name` | Oracle source table |
| `sf_object` | Target Salesforce object |
| `operation` | insert / upsert / update / delete |
| `status` | running → success / partial / failed |
| `total_records` | Records extracted from Oracle |
| `total_processed` | Records successfully uploaded |
| `total_failed` | Records that failed upload |
| `start_time` / `end_time` | Run duration |

### migration.batch_logs

| Column | Description |
|--------|-------------|
| `run_id` | Airflow DAG run ID |
| `batch_number` | Batch sequence number |
| `job_id` | Salesforce Bulk API job ID |
| `state` | uploading → JobComplete / Failed |
| `records_in_batch` | Records in batch file |
| `records_processed` | Records successfully processed |
| `records_failed` | Records that failed |

## Concerns and Limitations (Bulk API 2.0)

### Salesforce Official Limits

| Limit | Value | Note |
|-------|-------|------|
| Records per 24h (rolling) | **100,000,000** | ทุก ingest job รวมกันทั้ง org |
| Batches per 24h (rolling) | **15,000** | shared ระหว่าง Bulk API 1.0 และ 2.0 |
| Data size per job | **150 MB** | CSV format, 1 record per line |
| Concurrent jobs | **25** | Bulk API 1.0 + 2.0 รวมกัน |
| Total jobs (all states) | **100,000** | Open, InProgress, Complete, Failed, Aborted |
| Internal batch size | **10,000 records** | SF สร้างเองอัตโนมัติภายใน job |
| Internal batch timeout | **10 min / batch** | retry สูงสุด 10 ครั้ง ถ้า fail ทั้ง 10 ครั้ง job จะ fail |
| Job open timeout | **24 hours** | job ต้อง close ภายใน 24h หลังสร้าง |
| Job result retention | **7 days** | ต้องดึง result CSV ภายใน 7 วัน |
| CPU time (governor) | **60,000 ms** | per transaction on SF server |

> Source: [Salesforce Bulk API 2.0 Limits](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/asynch_api_concepts_limits.htm), [Bulk API Limits & Allocations](https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_bulkapi.htm)

### Concerns สำหรับโปรเจกต์นี้

#### 1. Volume vs Daily Limit

โปรเจกต์นี้มีข้อมูล **522M - 783M records** รวมทุกตาราง:

- Daily limit = 100M records / 24h
- ต้องใช้เวลาอย่างน้อย **6-8 วัน** ในการ migrate ข้อมูลทั้งหมด (ถ้า run เต็ม capacity)
- ควรวางแผน migration window ที่ชัดเจน

#### 2. Batch Allocation (15,000 / 24h)

- SF สร้าง internal batch ทุก 10,000 records
- ถ้า `batch_size` = 40,000 → SF สร้าง ~4 internal batches ต่อ job
- ตาราง `KPS_T_SALES_MD` (87M/year) → ~2,175 jobs × 4 batches = **~8,700 batches/year**
- ต้องระวังไม่ให้เกิน 15,000 batches ต่อ 24h เมื่อ migrate หลายตารางพร้อมกัน

#### 3. Concurrent Job Limit (25 jobs)

- DAG ปัจจุบัน parallel สูงสุด 15 jobs พร้อมกัน
- ถ้ามี integration อื่นใช้ Bulk API อยู่ด้วย จะ share limit 25 jobs กัน
- ควร check กับทีม SF admin ว่ามี process อื่นใช้ Bulk API อยู่หรือไม่

#### 4. Job Size (150 MB limit)

- `batch_size` = 40,000 records ต้องตรวจสอบว่า CSV ไม่เกิน 150 MB
- ตาราง `KPS_T_SALES_MD` มี 60 columns → แต่ละ row ประมาณ 500-800 bytes
- 40,000 × 800 bytes = ~32 MB ต่อ job → อยู่ในเกณฑ์ปลอดภัย
- ถ้ามี column ที่เป็น text ยาว ควรลด `batch_size`

#### 5. Trigger and Automation

- Salesforce Triggers, Workflows, Process Builder, Flows จะ **ทำงานทุก record** ที่ insert/upsert
- ถ้ามี trigger ที่ทำงานหนัก (เช่น callout, complex logic) จะทำให้ CPU time เกิน governor limit
- **แนะนำ:** ปิด trigger/automation ที่ไม่จำเป็นระหว่าง migration หรือใช้ custom setting เป็น kill switch

#### 6. Duplicate Rules & Validation Rules

- Salesforce Validation Rules จะ **reject records** ที่ไม่ผ่าน → records จะอยู่ใน `failedResults`
- Duplicate Rules อาจ block insert ถ้าตรวจพบ duplicate
- ควร review rules ทั้งหมดก่อน migration และพิจารณาปิดชั่วคราว

#### 7. Storage Limits

- Salesforce org มี data storage limit (ขึ้นอยู่กับ edition และ license)
- 522M-783M records จะใช้ storage มาก → ต้อง confirm กับ SF admin ว่า storage เพียงพอ

#### 8. Token Expiry

- OAuth access token มีอายุจำกัด (ปกติ ~2 hours สำหรับ connected app)
- Migration ที่ใช้เวลานาน (หลายชั่วโมง) token อาจหมดอายุระหว่าง upload
- DAG ปัจจุบัน authenticate ครั้งเดียวตอนเริ่ม → ถ้า upload นาน token อาจ expire
- **แนะนำ:** เพิ่ม token refresh logic สำหรับ long-running migrations

#### 9. Network & Timeout

- Upload ผ่าน internet → อาจเกิด timeout หรือ connection drop
- ควรมี retry mechanism และใช้ `start_batch` เพื่อ resume จาก batch ที่ fail

#### 10. Sandbox vs Production

- **ต้อง test ใน sandbox ก่อนเสมอ** (official recommendation)
- Sandbox อาจมี limit ต่ำกว่า production
- Processing time ใน production อาจแตกต่างจาก sandbox

### Checklist ก่อน Migration

- [ ] Confirm SF storage เพียงพอสำหรับข้อมูลทั้งหมด
- [ ] Review และปิด Triggers / Workflows / Validation Rules ที่ไม่จำเป็น
- [ ] วางแผน migration window (6-8 วัน minimum สำหรับ full load)
- [ ] Confirm ไม่มี integration อื่นใช้ Bulk API concurrent อยู่
- [ ] Test full pipeline ใน sandbox ก่อน production
- [ ] เตรียม rollback plan (delete records ถ้า migration ผิดพลาด)
- [ ] Monitor daily limits ระหว่าง migration (`/services/data/v66.0/limits`)
- [ ] พิจารณา token refresh สำหรับ long-running jobs

> Reference: [General Guidelines for Data Loads](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/asynch_api_planning_guidelines.htm), [Bulk API 2.0 Developer Guide v66.0](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_asynch.pdf)

## Bulk API Data Formats

### Bulk API 2.0 (โปรเจกต์นี้ใช้)

| ใช้งาน | Format | Content-Type |
|--------|--------|--------------|
| **Upload data (ingest)** | **CSV เท่านั้น** | `text/csv` |
| Job management (create/close/status) | JSON | `application/json` |
| Query results | CSV | `text/csv` |

Bulk API 2.0 **รองรับแค่ CSV** สำหรับ data upload — ไม่รับ XML หรือ JSON

### Bulk API v1 (เวอร์ชันเก่า)

| Format | Ingest | Query |
|--------|--------|-------|
| **CSV** | รองรับ | รองรับ |
| **XML** | รองรับ | รองรับ |
| **JSON** | รองรับ | รองรับ |

### เปรียบเทียบ v1 vs v2

| | Bulk API v1 | Bulk API 2.0 |
|--|-------------|--------------|
| Data formats | CSV, XML, JSON | **CSV only** |
| Batch management | Manual (สร้าง/ติดตาม batch เอง) | Automatic (SF จัดการให้) |
| Line ending | LF | LF หรือ CRLF |
| Max data per unit | 10 MB / batch | 150 MB / job |
| Complexity | สูงกว่า (ต้อง manage batches) | ง่ายกว่า (upload CSV แล้ว SF จัดการ) |
| Recommended | Legacy use cases | **New implementations** |

> Salesforce แนะนำให้ใช้ Bulk API 2.0 สำหรับ implementation ใหม่ ใช้ v1 เฉพาะกรณีที่ต้องการ XML/JSON format
>
> Source: [Prepare CSV Files](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/datafiles_prepare_csv.htm), [Prepare XML and JSON Files](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/datafiles_xml_preparing.htm), [Content Type Header](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/async_api_headers_content_type.htm)

### Composite REST vs Bulk API 2.0

Salesforce มี 2 แนวทางหลักสำหรับส่งข้อมูลเข้า:

```text
Composite REST (Sync)              Bulk API 2.0 (Async)
─────────────────────              ─────────────────────
Client ──POST JSON──► SF           Client ──Create Job──► SF
       ◄──Response───              Client ──Upload CSV──► SF
       (รอจนเสร็จ)                 Client ──Close Job───► SF
                                          (SF ประมวลผล background)
                                   Client ──Poll Status─► SF
                                   Client ──Get Results─► SF
```

| | Composite REST | Bulk API 2.0 |
|--|----------------|--------------|
| Processing | **Sync** (รอ response ทันที) | **Async** (poll ทีหลัง) |
| Format | **JSON** | **CSV** |
| Max records / call | 25 subrequests หรือ 5,000 (Collection) | **150 MB / job** (~ล้าน records) |
| Daily limit | API call quota (org-wide) | 100M records / 24h |
| Use case | ข้อมูลน้อย (< 2,000), real-time | **ข้อมูลมาก (> 2,000), migration** |
| Error handling | Response ทันทีใน JSON | ดึง failedResults CSV ทีหลัง |
| Complexity | ง่าย (1 call = done) | ต้อง create job → upload → poll → get results |

**สำหรับโปรเจกต์นี้** (522M-783M records) → ใช้ **Bulk API 2.0** เท่านั้น เพราะ Composite REST ส่งได้ทีละ 5,000 records สูงสุด จะต้องเรียก API หลายแสนครั้ง ซึ่งเกิน API call quota

## Usage Examples

### Insert with column mapping

```bash
airflow dags trigger migrate_bulk_api --conf '{
  "sf_object": "TMS_Request__c",
  "operation": "insert",
  "column_mapping": {
    "CON_CODE": "Name",
    "SHOP_CODE": "TMS_Shop_Brand_Name__c",
    "BRANCH_CODE": "TMS_Location__c"
  }
}'
```

### Upsert with external ID

```bash
airflow dags trigger migrate_bulk_api --conf '{
  "sf_object": "KPS_Sales__c",
  "operation": "upsert",
  "external_id_field": "External_Id__c",
  "batch_size": 10000
}'
```

### Custom query with resume

```bash
airflow dags trigger migrate_bulk_api --conf '{
  "sf_object": "KPS_Sales__c",
  "operation": "upsert",
  "external_id_field": "External_Id__c",
  "table_name": "KPS_T_SALES_MD",
  "extract_query": "SELECT * FROM KPS_T_SALES_MD WHERE SALE_DATE >= DATE '\''2024-01-01'\''",
  "start_batch": 5
}'
```
