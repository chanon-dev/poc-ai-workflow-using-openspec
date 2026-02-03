# Salesforce Bulk API 2.0 - Data Upload Guide

คู่มือการส่งข้อมูลขึ้น Salesforce ผ่าน REST API และ Bulk API 2.0 สำหรับ KPC TMS Data Migration

อ้างอิงจาก Postman Collections:
- `KP TMS Services`
- `From AOT Proxy API To Salesforce`

---

## Overview

```
┌─────────────────────────────────────────────────────────┐
│                  AOT Proxy → Salesforce                  │
│                                                          │
│  Step 1: OAuth2 Authentication (ได้ access_token)        │
│                    ↓                                     │
│  Step 2: Upsert TMS_Daily_Sales_File__c (สร้าง/อัพเดต)  │
│                    ↓                                     │
│  Step 3: เลือกวิธี Upload ตามจำนวน records               │
│          ┌────────┴────────┐                             │
│     ≤ 200 records     > 10k records                     │
│          │                 │                             │
│   Composite REST      Bulk API 2.0                      │
│   (Sync, JSON)       (Async, CSV)                       │
│          │                 │                             │
│          └────────┬────────┘                             │
│                   ↓                                      │
│  Step 4: Update TMS_Daily_Sales_File__c status           │
└─────────────────────────────────────────────────────────┘
```

---

## Airflow DAG Pipeline

DAG `migrate_bulk_api` จัดการ end-to-end pipeline ดังนี้:

```
┌──────────────┐   ┌──────────────┐   ┌────────────────┐   ┌─────────────────┐   ┌────────────────────┐
│  authenticate │   │ extract_data │   │ upload_batches  │   │ collect_results │   │ update_file_status │
│              │   │              │   │                │   │                 │   │                    │
│  Salesforce  │   │    Oracle    │   │  Salesforce    │   │   Salesforce    │   │   Salesforce       │
│  OAuth 2.0   │   │   → CSV     │   │  Bulk API 2.0  │   │   GET results   │   │   PATCH status     │
└──────┬───────┘   └──────┬───────┘   └───────┬────────┘   └────────┬────────┘   └────────────────────┘
       │                  │                    │                     │                        ▲
       │  access_token    │  batch CSV files   │  job results        │  result CSVs           │
       └──────────────────┴────────┬───────────┘                     │                        │
                                   │                                 │                        │
                                   └─────────────────────────────────┴────────────────────────┘
```

### Task Dependencies

```
authenticate ──┐
               ├──▶ upload_batches ──▶ collect_results ──▶ update_file_status
extract_data ──┘
```

- `authenticate` และ `extract_data` ทำงานพร้อมกันได้ (parallel)
- `upload_batches` ต้องรอทั้ง credentials และ batch files
- `collect_results` ดึงผลลัพธ์จาก Salesforce jobs
- `update_file_status` อัพเดตสถานะเป็น "Uploaded" หรือ "In Progress" (retry)

### Pipeline Flow

```
[Airflow Trigger]
       │
       ▼
 ┌─────────────┐    POST /services/oauth2/token
 │ authenticate │───────────────────────────────────▶ Salesforce
 │             │◀─────────── access_token ──────────  OAuth Server
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐    SELECT * FROM table WHERE ...
 │ extract_data │───────────────────────────────────▶ Oracle DB
 │             │◀─────────── DataFrame ─────────────  (10.0.0.23)
 │             │
 │  Split into │──▶ salesforce/data/TABLE_batch_001.csv
 │  CSV batches│──▶ salesforce/data/TABLE_batch_002.csv
 └──────┬──────┘──▶ salesforce/data/TABLE_batch_NNN.csv
        │
        ▼
 ┌──────────────┐   สำหรับแต่ละ batch file:
 │upload_batches │
 │              │   1. POST /jobs/ingest         → สร้าง job
 │  Bulk API    │   2. PUT  /jobs/ingest/{id}/batches → upload CSV
 │  2.0         │   3. PATCH /jobs/ingest/{id}   → close job
 │              │   4. GET  /jobs/ingest/{id}     → poll จน JobComplete
 │              │
 │  (parallel   │   ถ้ามีหลาย batch → ใช้ ThreadPool (max 15 concurrent)
 │   upload)    │   ถ้ามี batch เดียว → เรียก load_file() ตรง
 └──────┬───────┘
        │
        ▼
 ┌───────────────┐  สำหรับแต่ละ job:
 │collect_results │
 │               │  GET /jobs/ingest/{id}/successfulResults   → _success.csv
 │  Fetch CSVs   │  GET /jobs/ingest/{id}/failedResults       → _failed.csv
 │               │  GET /jobs/ingest/{id}/unprocessedrecords  → _unprocessed.csv
 │               │
 │  Save to:     │  salesforce/logs/{jobId}_success.csv
 │               │  salesforce/logs/{jobId}_failed.csv
 └──────┬────────┘  salesforce/logs/{jobId}_unprocessed.csv
        │
        ▼
 ┌────────────────────┐
 │update_file_status   │
 │                    │  ถ้า upload สำเร็จ:
 │  PATCH             │  PATCH /sobjects/TMS_Daily_Sales_File__c/
 │  TMS_Daily_Sales_  │        TMS_External_File_Ref__c/{ref}
 │  File__c           │  Body: {"TMS_Status__c": "Uploaded"}
 │                    │
 │                    │  ถ้า upload ล้มเหลว:
 │                    │  Body: {"TMS_Status__c": "In Progress"}
 └────────────────────┘  → raise RuntimeError เพื่อ retry
```

---

## Sequence Diagram — Bulk API 2.0 Upload

```
┌────────┐          ┌───────────┐          ┌────────────┐          ┌──────────────┐
│Airflow │          │Salesforce │          │  Oracle    │          │  Local FS    │
│  DAG   │          │  REST API │          │  Database  │          │  (CSV files) │
└───┬────┘          └─────┬─────┘          └──────┬─────┘          └──────┬───────┘
    │                     │                       │                       │
    │  ① POST /oauth2/token                       │                       │
    │  (client_credentials)                       │                       │
    │────────────────────▶│                       │                       │
    │                     │                       │                       │
    │  access_token,      │                       │                       │
    │  instance_url       │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │                       │
    │  ② SELECT * FROM KPS_T_SALES_MD             │                       │
    │     WHERE ROWNUM <= N                       │                       │
    │─────────────────────────────────────────────▶                       │
    │                     │                       │                       │
    │  DataFrame (N rows) │                       │                       │
    │◀─────────────────────────────────────────────                       │
    │                     │                       │                       │
    │  ③ Split DataFrame into CSV batches                                 │
    │─────────────────────────────────────────────────────────────────────▶
    │                     │                       │   batch_001.csv       │
    │                     │                       │   batch_002.csv       │
    │                     │                       │   ...                 │
    │                     │                       │                       │
    │                     │                       │                       │
    │  ═══════════════════════════════════════                             │
    │  ║ Loop: สำหรับแต่ละ batch file           ║                        │
    │  ═══════════════════════════════════════                             │
    │                     │                       │                       │
    │  ④ POST /jobs/ingest│                       │                       │
    │  {object, operation,│                       │                       │
    │   externalIdField,  │                       │                       │
    │   contentType: CSV} │                       │                       │
    │────────────────────▶│                       │                       │
    │                     │                       │                       │
    │  {id: jobId,        │                       │                       │
    │   state: "Open"}    │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │                       │
    │  ⑤ PUT /jobs/ingest/{jobId}/batches                                 │
    │  Content-Type: text/csv                                             │
    │  (GZIP compressed)  │                       │                       │
    │────────────────────▶│                       │                       │
    │                     │                       │                       │
    │  201 Created        │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │                       │
    │  ⑥ PATCH /jobs/ingest/{jobId}               │                       │
    │  {state: "UploadComplete"}                  │                       │
    │────────────────────▶│                       │                       │
    │                     │                       │                       │
    │  {state:"InProgress"}                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │                       │
    │  ⑦ GET /jobs/ingest/{jobId}                 │                       │
    │  (poll ทุก 5 วินาที)│                       │                       │
    │────────────────────▶│                       │                       │
    │  {state:"InProgress"}                       │                       │
    │◀────────────────────│                       │                       │
    │         ...         │                       │                       │
    │────────────────────▶│                       │                       │
    │  {state:"JobComplete",                      │                       │
    │   numberRecordsProcessed: N,                │                       │
    │   numberRecordsFailed: 0}                   │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │                       │
    │  ═══════════════════════════════════════                             │
    │  ║ End Loop                               ║                        │
    │  ═══════════════════════════════════════                             │
    │                     │                       │                       │
    │                     │                       │                       │
    │  ═══════════════════════════════════════                             │
    │  ║ Loop: สำหรับแต่ละ jobId               ║                         │
    │  ═══════════════════════════════════════                             │
    │                     │                       │                       │
    │  ⑧ GET /jobs/ingest/{jobId}/successfulResults                       │
    │────────────────────▶│                       │                       │
    │  CSV (sf__Id,       │                       │                       │
    │   sf__Created, ...) │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │   {jobId}_success.csv │
    │─────────────────────────────────────────────────────────────────────▶
    │                     │                       │                       │
    │  ⑨ GET /jobs/ingest/{jobId}/failedResults                           │
    │────────────────────▶│                       │                       │
    │  CSV (sf__Error,..) │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │   {jobId}_failed.csv  │
    │─────────────────────────────────────────────────────────────────────▶
    │                     │                       │                       │
    │  ⑩ GET /jobs/ingest/{jobId}/unprocessedrecords                      │
    │────────────────────▶│                       │                       │
    │  CSV               │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │ {jobId}_unprocessed.csv
    │─────────────────────────────────────────────────────────────────────▶
    │                     │                       │                       │
    │  ═══════════════════════════════════════                             │
    │  ║ End Loop                               ║                        │
    │  ═══════════════════════════════════════                             │
    │                     │                       │                       │
    │                     │                       │                       │
    │  ⑪ PATCH /sobjects/TMS_Daily_Sales_File__c/                        │
    │     TMS_External_File_Ref__c/{ref}                                 │
    │  {TMS_Status__c:    │                       │                       │
    │    "Uploaded" หรือ   │                       │                       │
    │    "In Progress"}   │                       │                       │
    │────────────────────▶│                       │                       │
    │                     │                       │                       │
    │  200 OK (updated)   │                       │                       │
    │◀────────────────────│                       │                       │
    │                     │                       │                       │
    ▼                     ▼                       ▼                       ▼
```

### API Calls สรุปตาม Sequence

| # | Method | Endpoint | Task | Description |
| --- | --- | --- | --- | --- |
| ① | `POST` | `/services/oauth2/token` | `authenticate` | ขอ access_token (Client Credentials) |
| ② | — | Oracle SQL query | `extract_data` | ดึงข้อมูลจาก Oracle DB |
| ③ | — | Local filesystem | `extract_data` | แบ่ง DataFrame เป็น CSV batches |
| ④ | `POST` | `/services/data/v66.0/jobs/ingest` | `upload_batches` | สร้าง Bulk Ingest Job |
| ⑤ | `PUT` | `/services/data/v66.0/jobs/ingest/{jobId}/batches` | `upload_batches` | Upload CSV data (GZIP) |
| ⑥ | `PATCH` | `/services/data/v66.0/jobs/ingest/{jobId}` | `upload_batches` | Close job → เริ่ม processing |
| ⑦ | `GET` | `/services/data/v66.0/jobs/ingest/{jobId}` | `upload_batches` | Poll สถานะ → JobComplete |
| ⑧ | `GET` | `/services/data/v66.0/jobs/ingest/{jobId}/successfulResults` | `collect_results` | ดึง records ที่สำเร็จ |
| ⑨ | `GET` | `/services/data/v66.0/jobs/ingest/{jobId}/failedResults` | `collect_results` | ดึง records ที่ fail |
| ⑩ | `GET` | `/services/data/v66.0/jobs/ingest/{jobId}/unprocessedrecords` | `collect_results` | ดึง records ที่ยังไม่ process |
| ⑪ | `PATCH` | `/services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{ref}` | `update_file_status` | อัพเดตสถานะ → "Uploaded" หรือ "In Progress" |

### Files ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
| --- | --- |
| `dags/migrate_bulk_api_dag.py` | DAG หลัก — orchestrate pipeline ทั้งหมด |
| `plugins/salesforce_auth.py` | OAuth 2.0 Client Credentials authentication |
| `plugins/salesforce_bulk_loader.py` | Bulk API 2.0 lifecycle (create → upload → close → poll) |
| `plugins/salesforce_status_tracker.py` | Upsert/Update status บน TMS_Daily_Sales_File__c |

### Output Files

| Path | Description |
| --- | --- |
| `salesforce/data/{TABLE}_batch_NNN.csv` | CSV batch files ที่ส่งขึ้น Salesforce |
| `salesforce/logs/{jobId}_success.csv` | Records ที่ insert/upsert สำเร็จ (มี sf__Id) |
| `salesforce/logs/{jobId}_failed.csv` | Records ที่ fail (มี sf__Error) |
| `salesforce/logs/{jobId}_unprocessed.csv` | Records ที่ยังไม่ถูก process |

### Target Objects

| Object | ใช้กับ | วัตถุประสงค์ |
| --- | --- | --- |
| `TMS_Daily_Sales_File__c` | REST API (PATCH) | Tracking สถานะไฟล์ |
| `TMS_Temp_Sales_Transaction_Item__c` | Bulk API 2.0 | ข้อมูล Transaction Items (> 10k records) |
| `Temp_Shop_Unit_Summary_Sales_Trn__c` | Composite REST | ข้อมูล Summary Sales (≤ 200 records) |

### API Version

ใช้ **v66.0** สำหรับทุก endpoint

### Base URL

```
# Sandbox (tmsdev)
https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com
```

---

## Step 1: Authentication - OAuth 2.0 Client Credentials Flow

ขอ access token สำหรับ server-to-server integration (ไม่ต้องมี user interaction)

### Request

```
POST {baseUrl}/services/oauth2/token
```

**Headers:**

| Key | Value |
| --- | --- |
| Content-Type | `application/x-www-form-urlencoded` |
| Accept | `application/json` |

**Body (form-urlencoded):**

| Key | Value | Description |
| --- | --- | --- |
| `grant_type` | `client_credentials` | OAuth grant type |
| `client_id` | `3MVG9...` | Consumer Key จาก Connected App |
| `client_secret` | `621DDF...` | Consumer Secret จาก Connected App |

### Response (200 OK)

```json
{
  "access_token": "00D...xyz!ARsAQA...",
  "instance_url": "https://yourInstance.my.salesforce.com",
  "token_type": "Bearer",
  "issued_at": "1622547891234",
  "signature": "abcdef1234567890"
}
```

### สิ่งที่ต้องเก็บไว้ใช้

- **`access_token`** → ใช้ใน Authorization header ของทุก request ถัดไป
- **`instance_url`** → ใช้เป็น base URL สำหรับ API calls

### Error Responses

| Code | Error | สาเหตุ |
| --- | --- | --- |
| 400 | `invalid_grant` | Parameter ไม่ถูกต้องหรือขาด required fields |
| 401 | `invalid_client` | Client credentials ไม่ถูกต้อง |

---

## Step 2: Upsert TMS_Daily_Sales_File__c (Tracking สถานะไฟล์)

สร้างหรืออัพเดต record สำหรับ tracking สถานะการ upload ไฟล์ โดยใช้ External ID

### Request

```
PATCH {baseUrl}/services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{externalFileRef}
```

**Headers:**

| Key | Value |
| --- | --- |
| Content-Type | `application/json` |
| Accept | `application/json` |
| Authorization | `Bearer {access_token}` |

**Body (Validation ผ่าน → status "New"):**

```json
{
  "TMS_File_Name__c": "0901001_042_Sales_20251127042907.txt",
  "TMS_Business_Type__c": "bu",
  "TMS_Comapny_Code__c": "0901001",
  "TMS_Shop_Code__c": "042",
  "TMS_Branch_Code__c": "042",
  "TMS_Sales_Date__c": "2025-11-27",
  "TMS_Status__c": "New",
  "TMS_External_File_Ref__c": "0901001_042_Sales_20251127042907"
}
```

**Body (Validation ไม่ผ่าน → status "Failed"):**

```json
{
  "TMS_File_Name__c": "0901001_042_Sales_20251127042907.txt",
  "TMS_Business_Type__c": "bu",
  "TMS_Comapny_Code__c": "0901001",
  "TMS_Shop_Code__c": "042",
  "TMS_Branch_Code__c": "042",
  "TMS_Sales_Date__c": "2025-11-27",
  "TMS_Status__c": "Failed",
  "TMS_External_File_Ref__c": "0901001_042_Sales_20251127042907",
  "TMS_Errors__c": ["error#1", "error#2"]
}
```

### Status Flow

```
Validation ผ่าน   → "New" (หรือ "Uploading")
Validation ไม่ผ่าน → "Failed"
Upload สำเร็จ     → "Uploaded"
Upload ล้มเหลว    → "In Progress" (reset เพื่อ retry)
```

### Response

| Code | Description |
| --- | --- |
| 200 | Record อัพเดตสำเร็จ |
| 201 | สร้าง record ใหม่สำเร็จ (upsert created) |
| 400 | ข้อมูลไม่ถูกต้อง / ขาด required field |
| 401 | Token ไม่ถูกต้องหรือหมดอายุ |
| 404 | ไม่พบ record (เมื่อใช้ `?updateOnly=true`) |

---

## Step 3A: Bulk API 2.0 (สำหรับ > 10,000 records)

ใช้สำหรับ upload ข้อมูลจำนวนมาก แบบ asynchronous ผ่าน CSV

### 3A.1 - Create Bulk Ingest Job

```
POST {baseUrl}/services/data/v66.0/jobs/ingest
```

**Headers:**

| Key | Value |
| --- | --- |
| Content-Type | `application/json` |
| Accept | `application/json` |
| Authorization | `Bearer {access_token}` |

**Body:**

```json
{
  "object": "TMS_Temp_Sales_Transaction_Item__c",
  "operation": "upsert",
  "externalIdFieldName": "TMS_External_Sequence_Ref__c",
  "contentType": "CSV",
  "lineEnding": "LF"
}
```

| Field | Description |
| --- | --- |
| `object` | Salesforce object ที่จะ upsert |
| `operation` | `upsert` (insert ถ้าไม่มี, update ถ้ามีแล้ว) |
| `externalIdFieldName` | External ID field สำหรับ matching records |
| `contentType` | รูปแบบข้อมูล (`CSV`) |
| `lineEnding` | Line ending format (`LF` สำหรับ Unix/Mac) |

**Response (200):**

```json
{
  "id": "750xx000000ABCD",
  "object": "TMS_Temp_Sales_Transaction_Item__c",
  "operation": "upsert",
  "state": "Open",
  "contentType": "CSV",
  "createdDate": "2024-01-15T10:30:00.000+0000"
}
```

> เก็บค่า **`id`** (jobId) ไว้ใช้ใน step ถัดไป

---

### 3A.2 - Upload CSV Data

```
PUT {baseUrl}/services/data/v66.0/jobs/ingest/{jobId}/batches
```

**Headers:**

| Key | Value |
| --- | --- |
| Content-Type | `text/csv` |
| Authorization | `Bearer {access_token}` |

**Body (raw CSV):**

```csv
TMS_External_Sequence_Ref__c,TMS_Business_Type__c,TMS_Shop_Code__c,TMS_Sale_No__c,TMS_Sale_Date__c,TMS_Seq__c,TMS_Prod_Serv_Code__c,TMS_Prod_Serv_Name__c,TMS_Prod_Serv_Qty__c,TMS_Total_Net_Amt_Inc_Vat__c
a1kfc000002wq6jAAA_251127-7934-37791_1,bank,7934,37791,2025-11-27,1,PROD001,Product A,2,16050.54
a1kfc000002wq6jAAA_251127-7934-37791_2,bank,7934,37791,2025-11-27,2,PROD002,Product B,1,5000.00
```

**CSV Fields:**

| Column | Description |
| --- | --- |
| `TMS_External_Sequence_Ref__c` | External ID สำหรับ upsert matching |
| `TMS_Business_Type__c` | ประเภทธุรกิจ (เช่น `bank`, `bu`) |
| `TMS_Shop_Code__c` | รหัสร้านค้า |
| `TMS_Sale_No__c` | เลขที่การขาย |
| `TMS_Sale_Date__c` | วันที่ขาย (YYYY-MM-DD) |
| `TMS_Seq__c` | ลำดับรายการ |
| `TMS_Prod_Serv_Code__c` | รหัสสินค้า/บริการ |
| `TMS_Prod_Serv_Name__c` | ชื่อสินค้า/บริการ |
| `TMS_Prod_Serv_Qty__c` | จำนวน |
| `TMS_Total_Net_Amt_Inc_Vat__c` | ยอดรวมสุทธิ (รวม VAT) |

**Response:** `201 Created`

> สามารถเรียก PUT batches หลายครั้งได้สำหรับ job เดียวกัน (ก่อน close job)

---

### 3A.3 - Close Job (เริ่ม Processing)

หลัง upload CSV เสร็จ ต้อง close job เพื่อให้ Salesforce เริ่ม process

```
PATCH {baseUrl}/services/data/v66.0/jobs/ingest/{jobId}
```

**Headers:**

| Key | Value |
| --- | --- |
| Content-Type | `application/json` |
| Accept | `application/json` |
| Authorization | `Bearer {access_token}` |

**Body:**

```json
{
  "state": "UploadComplete"
}
```

**Response (200):**

```json
{
  "id": "750xx000000ABCD",
  "state": "InProgress"
}
```

> หลัง close แล้ว state จะเปลี่ยนเป็น `InProgress` โดยอัตโนมัติ

---

### 3A.4 - Poll Job Status

Poll สถานะจนกว่า job จะเสร็จ

```
GET {baseUrl}/services/data/v66.0/jobs/ingest/{jobId}
```

**Headers:**

| Key | Value |
| --- | --- |
| Accept | `application/json` |
| Authorization | `Bearer {access_token}` |

**Response (200):**

```json
{
  "id": "750xx000000ABCD",
  "state": "JobComplete",
  "numberRecordsProcessed": 12500,
  "numberRecordsFailed": 3,
  "totalProcessingTime": 45000
}
```

**Job States:**

| State | Description |
| --- | --- |
| `Open` | Job ถูกสร้างแล้ว รอ upload data |
| `UploadComplete` | Data upload เสร็จ รอ processing |
| `InProgress` | กำลัง process data |
| `JobComplete` | Process เสร็จสมบูรณ์ |
| `Failed` | Job ล้มเหลว |
| `Aborted` | Job ถูกยกเลิก |

> แนะนำให้ poll ทุก 5-10 วินาที จนกว่า state จะเป็น `JobComplete` หรือ `Failed`

---

### 3A.5 - ดึงผลลัพธ์

หลัง job เสร็จ (`JobComplete`) สามารถดึงผลลัพธ์ได้ 3 ประเภท:

#### Successful Records

```
GET {baseUrl}/services/data/v66.0/jobs/ingest/{jobId}/successfulResults
Accept: text/csv
Authorization: Bearer {access_token}
```

**Response (CSV):**

```csv
sf__Id,sf__Created,TMS_External_Sequence_Ref__c,TMS_Business_Type__c,TMS_Shop_Code__c,...
a0Y5f000001ABC1,true,a1kfc000002wq6jAAA_251127-7934-37791_1,bank,7934,...
a0Y5f000001ABC2,true,a1kfc000002wq6jAAA_251127-7934-37791_2,bank,7934,...
```

- `sf__Id` = Salesforce Record ID ที่ถูกสร้าง/อัพเดต
- `sf__Created` = `true` (สร้างใหม่) หรือ `false` (อัพเดต)

#### Failed Records

```
GET {baseUrl}/services/data/v66.0/jobs/ingest/{jobId}/failedResults
Accept: text/csv
Authorization: Bearer {access_token}
```

**Response (CSV):**

```csv
sf__Id,sf__Error,TMS_External_Sequence_Ref__c,...
,REQUIRED_FIELD_MISSING:Required fields are missing: [TMS_External_Sequence_Ref__c],...
,INVALID_TYPE_ON_FIELD_IN_RECORD:Amount: value not of required type,...
,DUPLICATE_VALUE:duplicate value found: TMS_External_Sequence_Ref__c duplicates value on record,...
```

**Common Errors:**

| Error Code | สาเหตุ |
| --- | --- |
| `REQUIRED_FIELD_MISSING` | ขาด required field |
| `INVALID_TYPE_ON_FIELD_IN_RECORD` | ข้อมูลไม่ตรง data type |
| `DUPLICATE_VALUE` | External ID ซ้ำใน batch เดียวกัน |

#### Unprocessed Records

```
GET {baseUrl}/services/data/v66.0/jobs/ingest/{jobId}/unprocessedrecords
Accept: text/csv
Authorization: Bearer {access_token}
```

Records ที่ยังไม่ถูก process (เช่น job ถูก abort กลางคัน) สามารถนำไป retry ได้

---

## Step 3B: Composite REST API (สำหรับ ≤ 200 records ต่อ batch)

ใช้สำหรับ insert ข้อมูลจำนวนน้อย แบบ synchronous

### Request

```
POST {baseUrl}/services/data/v66.0/composite/sobjects
```

**Headers:**

| Key | Value |
| --- | --- |
| Content-Type | `application/json` |
| Accept | `application/json` |
| Authorization | `Bearer {access_token}` |

**Body:**

```json
{
  "allOrNone": true,
  "records": [
    {
      "attributes": {
        "type": "Temp_Shop_Unit_Summary_Sales_Trn__c",
        "referenceId": "ref1"
      },
      "TMS_File_Name__c": "0903001_SALES_20251127135523.txt",
      "TMS_Concession_Code__c": "00",
      "TMS_Shop_Code__c": "0903001",
      "TMS_Sequence__c": 1,
      "TMS_Branch_Cdoe__c": "3625",
      "TMS_Sales_Date__c": "2025-11-27",
      "TMS_Sales_Type__c": 1,
      "TMS_Sales_Amount__c": 101950.69,
      "TMS_Receipt_Number__c": 179
    }
  ]
}
```

| Field | Description |
| --- | --- |
| `allOrNone` | `true` = ถ้า record ใด fail ทั้ง batch rollback |
| `attributes.type` | Salesforce object name |
| `attributes.referenceId` | Reference ID สำหรับ tracking ใน response |

**Response (200):**

```json
[
  {
    "id": "a0Y5f000001ABC1",
    "success": true,
    "errors": []
  },
  {
    "id": "a0Y5f000001ABC2",
    "success": true,
    "errors": []
  }
]
```

### Composite API Limits

- สูงสุด **200 records** ต่อ request
- ถ้ามีมากกว่า 200 records ต้องแบ่งเป็นหลาย batch requests

---

## Step 4: Update Status หลัง Upload

อัพเดตสถานะไฟล์หลังจาก upload เสร็จ โดยใช้ `?updateOnly=true` เพื่อป้องกันไม่ให้สร้าง record ใหม่

### Upload สำเร็จ

```
PATCH {baseUrl}/services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{externalFileRef}?updateOnly=true
```

```json
{
  "TMS_Status__c": "Uploaded"
}
```

### Upload ล้มเหลว

```
PATCH {baseUrl}/services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{externalFileRef}?updateOnly=true
```

```json
{
  "TMS_Status__c": "In Progress"
}
```

> `updateOnly=true` ทำให้ถ้า record ไม่มีอยู่จะ return 404 แทนที่จะสร้างใหม่

---

## สรุป API Calls ทั้งหมด

```
1. POST /services/oauth2/token                                    → ได้ access_token
2. PATCH /services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/   → สร้าง/อัพเดตสถานะไฟล์
         TMS_External_File_Ref__c/{ref}

--- Bulk API 2.0 (> 10k records) ---
3a. POST  /services/data/v66.0/jobs/ingest                        → สร้าง job (ได้ jobId)
3b. PUT   /services/data/v66.0/jobs/ingest/{jobId}/batches        → อัพโหลด CSV data
3c. PATCH /services/data/v66.0/jobs/ingest/{jobId}                → ปิด job (เริ่ม process)
3d. GET   /services/data/v66.0/jobs/ingest/{jobId}                → poll สถานะ
3e. GET   /services/data/v66.0/jobs/ingest/{jobId}/successfulResults  → ดูผลสำเร็จ
3f. GET   /services/data/v66.0/jobs/ingest/{jobId}/failedResults      → ดูผล error
3g. GET   /services/data/v66.0/jobs/ingest/{jobId}/unprocessedrecords → ดู records ที่ยังไม่ process

--- Composite REST (≤ 200 records) ---
3x. POST /services/data/v66.0/composite/sobjects                  → batch insert (sync)

4. PATCH /services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/   → อัพเดตสถานะสุดท้าย
         TMS_External_File_Ref__c/{ref}?updateOnly=true
```

---

## เลือกใช้ API ไหนดี?

| เงื่อนไข | ใช้ API | เหตุผล |
| --- | --- | --- |
| Records ≤ 200 | Composite REST | Sync, ผลลัพธ์ทันที, allOrNone rollback |
| Records 200 - 10,000 | Composite REST (หลาย batch) | แบ่ง batch ละ 200, ยังเป็น sync |
| Records > 10,000 | Bulk API 2.0 | Async, รองรับข้อมูลจำนวนมาก, CSV format |
| Records > 100,000 | Bulk API 2.0 (หลาย jobs) | แบ่ง CSV เป็นหลาย jobs |

---

## วิธีเช็คและ Debug Salesforce Bulk API - Step by Step

คู่มือการตรวจสอบแต่ละขั้นตอนอย่างละเอียด รวมถึงวิธี debug เมื่อเกิดปัญหา

### Prerequisites

```bash
# Airflow containers ต้อง running
docker compose up -d

# เช็คสถานะ
docker compose ps
# ทุก container ต้องแสดง "healthy"
```

---

### ขั้นตอนที่ 1: เช็ค OAuth Authentication

ทดสอบว่า Connected App ใช้งานได้ และได้ `access_token` กลับมา

```bash
docker compose exec airflow-worker python3 << 'EOF'
import requests

r = requests.post(
    'https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com/services/oauth2/token',
    data={
        'grant_type': 'client_credentials',
        'client_id': '<YOUR_CLIENT_ID>',
        'client_secret': '<YOUR_CLIENT_SECRET>',
    }
)

print(f'Status: {r.status_code}')
if r.status_code == 200:
    creds = r.json()
    print(f'✅ Token: {creds["access_token"][:30]}...')
    print(f'✅ Instance: {creds["instance_url"]}')
else:
    print(f'❌ Error: {r.text}')
EOF
```

**ถ้าสำเร็จ:**
```
Status: 200
✅ Token: 00Dfc000000gGra!AQEAQAmIU3o...
✅ Instance: https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com
```

**ถ้าล้มเหลว - สาเหตุที่พบบ่อย:**

| Error | สาเหตุ | วิธีแก้ |
|-------|--------|---------|
| `invalid_client` | client_id หรือ client_secret ผิด | เช็ค Connected App บน Salesforce Setup |
| `invalid_grant` | grant_type ไม่ถูกต้อง | ต้องใช้ `client_credentials` |
| Connection timeout | URL ไม่ถูกต้อง | เช็ค sandbox URL (ต้องลงท้าย `.sandbox.my.salesforce.com`) |

---

### ขั้นตอนที่ 2: เช็ค Salesforce Objects ที่ใช้ได้

Connected App user อาจไม่มีสิทธิ์เข้าถึงทุก object ต้องเช็คว่ามี object ไหนใช้ได้

#### 2.1 เช็คว่า object ที่ต้องการมีอยู่และเข้าถึงได้

```bash
docker compose exec airflow-worker python3 << 'EOF'
import requests

# Auth
r = requests.post(
    'https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com/services/oauth2/token',
    data={
        'grant_type': 'client_credentials',
        'client_id': '<YOUR_CLIENT_ID>',
        'client_secret': '<YOUR_CLIENT_SECRET>',
    }
)
creds = r.json()
headers = {
    'Authorization': f'Bearer {creds["access_token"]}',
    'Accept': 'application/json',
}

# เช็ค object ที่ต้องการ
objects_to_check = [
    'TMS_Temp_Sales_Transaction_Item__c',
    'TMS_Daily_Sales_File__c',
    'TMS_Request__c',
    'Product2',
    'Account',
]

for obj in objects_to_check:
    url = f'{creds["instance_url"]}/services/data/v66.0/sobjects/{obj}/describe'
    r2 = requests.get(url, headers=headers)
    if r2.status_code == 200:
        fields = r2.json()['fields']
        ext = [f['name'] for f in fields if f.get('externalId')]
        print(f'✅ {obj} — accessible, External IDs: {ext if ext else "(none)"}')
    elif r2.status_code == 404:
        print(f'❌ {obj} — NOT FOUND (object ไม่มี หรือ user ไม่มีสิทธิ์)')
    else:
        print(f'⚠️  {obj} — HTTP {r2.status_code}')
EOF
```

**ถ้า object return 404:**
- Object อาจยังไม่ถูกสร้างบน Salesforce
- Connected App user อาจไม่มี Object Permission
- **วิธีแก้:** ไปที่ Salesforce Setup → Permission Sets → เพิ่ม Object Permission ให้ Connected App user

#### 2.2 ดู custom objects ที่ createable ทั้งหมด

```bash
docker compose exec airflow-worker python3 << 'EOF'
import requests

r = requests.post(
    'https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com/services/oauth2/token',
    data={
        'grant_type': 'client_credentials',
        'client_id': '<YOUR_CLIENT_ID>',
        'client_secret': '<YOUR_CLIENT_SECRET>',
    }
)
creds = r.json()
headers = {
    'Authorization': f'Bearer {creds["access_token"]}',
    'Accept': 'application/json',
}

r2 = requests.get(f'{creds["instance_url"]}/services/data/v66.0/sobjects', headers=headers)
sobjects = r2.json()['sobjects']

custom = [s for s in sobjects if s['createable'] and s['custom']]
print(f'Custom createable objects: {len(custom)}')
for s in sorted(custom, key=lambda x: x['name']):
    print(f'  {s["name"]}')
EOF
```

#### 2.3 ดู fields ของ object

```bash
docker compose exec airflow-worker python3 << 'EOF'
import requests

OBJECT_NAME = 'TMS_Request__c'  # ← เปลี่ยนชื่อ object ที่ต้องการ

r = requests.post(
    'https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com/services/oauth2/token',
    data={
        'grant_type': 'client_credentials',
        'client_id': '<YOUR_CLIENT_ID>',
        'client_secret': '<YOUR_CLIENT_SECRET>',
    }
)
creds = r.json()
headers = {
    'Authorization': f'Bearer {creds["access_token"]}',
    'Accept': 'application/json',
}

url = f'{creds["instance_url"]}/services/data/v66.0/sobjects/{OBJECT_NAME}/describe'
r2 = requests.get(url, headers=headers)

if r2.status_code == 200:
    fields = r2.json()['fields']
    print(f'=== {OBJECT_NAME} Fields ===')
    print()
    print('Createable fields (ใช้ใน CSV header ได้):')
    for f in fields:
        if f['createable']:
            ext = ' ⭐ External ID' if f.get('externalId') else ''
            req = ' (required)' if not f['nillable'] and not f.get('defaultedOnCreate') else ''
            print(f'  {f["name"]} ({f["type"]}){ext}{req}')
else:
    print(f'❌ Cannot describe {OBJECT_NAME}: HTTP {r2.status_code}')
EOF
```

**สิ่งที่ต้องดู:**
- **External ID fields** (⭐) — จำเป็นสำหรับ `upsert` operation
- **Required fields** — ต้องมีใน CSV ไม่งั้น insert/upsert จะ fail
- **Field types** — ข้อมูลใน CSV ต้องตรง type (เช่น date ต้องเป็น `YYYY-MM-DD`)

---

### ขั้นตอนที่ 3: เช็ค Oracle Connectivity

```bash
# เช็คจาก host machine
python3 -c "
import socket
s = socket.socket()
s.settimeout(5)
s.connect(('10.0.0.23', 1521))
print('✅ Oracle reachable from host')
s.close()
"

# เช็คจาก Docker container
docker compose exec airflow-worker python3 -c "
import socket
s = socket.socket()
s.settimeout(5)
s.connect(('10.0.0.23', 1521))
print('✅ Oracle reachable from Docker')
s.close()
"
```

**ถ้า Docker เข้าไม่ได้แต่ host เข้าได้:**
- ปัญหา: VPN tunnel ไม่ forward traffic เข้า Docker bridge network
- **วิธีแก้:** ใช้ `network_mode: host` ใน docker-compose หรือ route traffic ผ่าน host gateway

**ถ้าเจอ `DPY-3015: password verifier type not supported in thin mode`:**
- ต้องใช้ Oracle Instant Client (thick mode)
- ใน DAG ต้องมี:
```python
import oracledb
try:
    oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")
except Exception:
    pass
```

---

### ขั้นตอนที่ 4: เช็ค Airflow Connection

```bash
# ดู connections ที่มี
docker compose exec airflow-worker airflow connections list

# สร้าง salesforce_api connection (ถ้ายังไม่มี)
docker compose exec airflow-worker airflow connections add salesforce_api \
  --conn-type http \
  --conn-host "https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com" \
  --conn-login "<CLIENT_ID>" \
  --conn-password "<CLIENT_SECRET>"
```

**Fields mapping:**

| Airflow Connection Field | Salesforce Value |
|--------------------------|------------------|
| `conn_type` | `http` |
| `host` | Salesforce base URL |
| `login` | Consumer Key (client_id) |
| `password` | Consumer Secret (client_secret) |

---

### ขั้นตอนที่ 5: เช็ค DAG โหลดสำเร็จ

```bash
# ดู DAGs ที่โหลดได้
docker compose exec airflow-worker airflow dags list | grep bulk

# ผลลัพธ์ที่ถูกต้อง:
# migrate_bulk_api | /opt/airflow/dags/migrate_bulk_api_dag.py | airflow | True
```

**ถ้า DAG ไม่แสดง:**
```bash
# เช็ค syntax errors
docker compose exec airflow-worker python /opt/airflow/dags/migrate_bulk_api_dag.py

# ดู import errors
docker compose exec airflow-worker airflow dags list-import-errors
```

---

### ขั้นตอนที่ 6: Trigger DAG และ Monitor

#### 6.1 Trigger DAG

```bash
# Trigger แบบ default (upsert)
docker compose exec airflow-worker airflow dags trigger migrate_bulk_api

# Trigger ด้วย config (insert + custom object)
docker compose exec airflow-worker airflow dags trigger migrate_bulk_api \
  --conf '{
    "sf_object": "TMS_Request__c",
    "operation": "insert",
    "external_id_field": "",
    "extract_query": "SELECT SHOP_CODE AS Name FROM KPS_T_SALES_MD WHERE ROWNUM <= 5"
  }'
```

**Config options:**

| Key | Default | Description |
|-----|---------|-------------|
| `sf_object` | `TMS_Temp_Sales_Transaction_Item__c` | Target Salesforce object |
| `operation` | `upsert` | `insert`, `update`, `upsert`, `delete` |
| `external_id_field` | `TMS_External_Sequence_Ref__c` | External ID (ต้องมีสำหรับ upsert) |
| `extract_query` | `SELECT * FROM KPS_T_SALES_MD WHERE ROWNUM <= 10` | SQL query |
| `batch_size` | `40000` | Records ต่อ batch file |
| `start_batch` | `1` | เริ่มจาก batch ที่เท่าไหร่ (สำหรับ resume) |
| `table_name` | `KPS_T_SALES_MD` | ชื่อ table (ใช้ใน default query) |

> **สำคัญ:** ถ้าใช้ `insert` operation ไม่ต้องมี External ID field ส่ง `""` ได้
> ถ้าใช้ `upsert` ต้องมี External ID field บน Salesforce object

#### 6.2 Monitor task states

```bash
# ดูสถานะ tasks (เปลี่ยน run_id ตาม output จาก trigger)
docker compose exec airflow-worker \
  airflow tasks states-for-dag-run migrate_bulk_api "manual__2026-01-30T10:11:53.932879+00:00"
```

**ผลลัพธ์ที่ถูกต้อง:**
```
task_id         | state
================+========
authenticate    | success
extract_data    | success
upload_batches  | success
collect_results | success
```

#### 6.3 ดู task logs

```bash
# ดู log ของ task ที่ต้องการ (เปลี่ยน run_id และ task_id)
docker compose exec airflow-worker cat \
  "/opt/airflow/logs/dag_id=migrate_bulk_api/run_id=manual__2026-01-30T10:11:53.932879+00:00/task_id=upload_batches/attempt=1.log" \
  | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        if d.get('level') in ('info', 'error', 'warning'):
            print(f'[{d[\"level\"].upper()}] {d[\"event\"]}')
    except: pass
"
```

---

### ขั้นตอนที่ 7: เช็คผลลัพธ์

#### 7.1 ดู result files

```bash
# ดูไฟล์ผลลัพธ์ที่เก็บไว้
docker compose exec airflow-worker ls -la /opt/airflow/salesforce/logs/

# ดู success records
docker compose exec airflow-worker cat /opt/airflow/salesforce/logs/<JOB_ID>_success.csv

# ดู failed records
docker compose exec airflow-worker cat /opt/airflow/salesforce/logs/<JOB_ID>_failed.csv

# ดู unprocessed records
docker compose exec airflow-worker cat /opt/airflow/salesforce/logs/<JOB_ID>_unprocessed.csv
```

#### 7.2 ตัวอย่าง success result

```csv
"sf__Id","sf__Created","NAME","TMS_LOCATION__C"
"a1Mfc000001IKfjEAG","true","0501003","002"
"a1Mfc000001IKfkEAG","true","0501003","002"
```

- `sf__Id` — Salesforce Record ID ที่สร้างขึ้น
- `sf__Created` — `true` = สร้างใหม่, `false` = อัพเดต (upsert)

#### 7.3 ดู batch CSV ที่ส่งขึ้น Salesforce

```bash
# ดู CSV header (columns ต้องตรงกับ Salesforce field API names)
docker compose exec airflow-worker head -2 /opt/airflow/salesforce/data/KPS_T_SALES_MD_batch_001.csv
```

> **สำคัญ:** CSV column headers ต้องตรงกับ Salesforce field API names
> ถ้า extract จาก Oracle ด้วย `SELECT *` จะได้ Oracle column names ซึ่งไม่ตรง
> ต้องใช้ SQL alias: `SELECT SHOP_CODE AS Name, BRANCH_CODE AS TMS_Location__c FROM ...`

---

### Troubleshooting Common Issues

| ปัญหา | สาเหตุ | วิธีแก้ |
|--------|--------|---------|
| `400 Bad Request: Unable to find object` | Object ไม่มีบน Salesforce หรือ user ไม่มีสิทธิ์ | เช็ค object ตาม ขั้นตอนที่ 2 |
| `DPY-3015: password verifier type not supported` | Oracle ต้องใช้ thick mode | เพิ่ม `oracledb.init_oracle_client()` ตาม ขั้นตอนที่ 3 |
| `ORA-12170: TNS:Connect timeout` | Oracle ไม่สามารถเชื่อมต่อได้ | เช็ค VPN/Network ตาม ขั้นตอนที่ 3 |
| `conn_id 'salesforce_api' isn't defined` | ยังไม่สร้าง Airflow Connection | สร้างตาม ขั้นตอนที่ 4 |
| `REQUIRED_FIELD_MISSING` | CSV ขาด required field | เช็ค fields ตาม ขั้นตอนที่ 2.3 |
| `INVALID_TYPE_ON_FIELD_IN_RECORD` | Data type ไม่ตรง | เช็ค field type (date ต้องเป็น YYYY-MM-DD) |
| `Upload: 0 processed, 0 failed` | Job สร้างไม่สำเร็จ (400) | ดู task log สำหรับ error message |
| DAG ไม่แสดงใน Airflow | Import error | รัน `airflow dags list-import-errors` |

---

### ตัวอย่าง Full Test (End-to-End)

```bash
# 1. เช็ค Oracle connectivity
docker compose exec airflow-worker python3 -c "
import socket; s=socket.socket(); s.settimeout(5)
s.connect(('10.0.0.23', 1521)); print('✅ Oracle OK'); s.close()
"

# 2. เช็ค Salesforce auth
docker compose exec airflow-worker python3 -c "
import requests
r = requests.post('https://kingpowerinternationalgroupcoltd2--tmsdev.sandbox.my.salesforce.com/services/oauth2/token',
    data={'grant_type':'client_credentials','client_id':'<ID>','client_secret':'<SECRET>'})
print('✅ SF Auth OK' if r.status_code==200 else f'❌ {r.text}')
"

# 3. เช็ค Airflow connection
docker compose exec airflow-worker airflow connections list | grep salesforce

# 4. เช็ค DAG loaded
docker compose exec airflow-worker airflow dags list | grep bulk

# 5. Trigger DAG
docker compose exec airflow-worker airflow dags trigger migrate_bulk_api \
  --conf '{"sf_object":"TMS_Request__c","operation":"insert","external_id_field":"","extract_query":"SELECT SHOP_CODE AS Name FROM KPS_T_SALES_MD WHERE ROWNUM <= 5"}'

# 6. รอ 60 วินาทีแล้วเช็คผล
sleep 60
docker compose exec airflow-worker airflow tasks states-for-dag-run migrate_bulk_api "<RUN_ID>"

# 7. ดู results
docker compose exec airflow-worker ls /opt/airflow/salesforce/logs/
```
