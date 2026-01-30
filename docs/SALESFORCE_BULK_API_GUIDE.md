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
