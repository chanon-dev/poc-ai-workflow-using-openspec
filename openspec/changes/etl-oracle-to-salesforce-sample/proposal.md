# Proposal: ETL Pipeline for Product & Price Migration (Sample)

## Why

เปลี่ยนจาก Just-in-Time Config Generation (แต่ละ DAG สร้าง config เอง) มาเป็น **Centralized Setup DAG Pattern** เพื่อแก้ปัญหา Race Condition เมื่อรัน DAG หลายตัวพร้อมกัน และเพิ่มประสิทธิภาพในการทำงาน

ใช้ตาราง **12_Product & Price** เป็นตัวอย่างการ Implement (Multi-Table JOIN → Salesforce `Product2`)

## What Changes

### Architecture Changes

1. **Setup DAG (`setup_salesforce_pipeline`)** - รันครั้งเดียวหลัง Deploy
   - สร้าง Master `process-conf.xml` รวม Config ทุกตาราง
   - สร้าง `.sdl` Mapping Files ทั้งหมด
   - Encrypt Credentials เก็บใน Airflow Variables

2. **Execution DAG (`migrate_product_price`)** - รันตาม Schedule
   - Extract: ดึงข้อมูลจาก Oracle (JOIN หลาย Table) → CSV
   - Load: เรียก Data Loader (Read-Only จาก Master Config)
   - Audit: ตรวจสอบผลลัพธ์

### New Files

| File | Purpose |
|------|---------|
| `dags/setup_salesforce_pipeline.py` | Setup DAG |
| `dags/migrate_product_price_dag.py` | Execution DAG สำหรับ Product |
| `dags/config/field_mappings.py` | เพิ่ม Product mapping |
| `salesforce/dataloader_conf/mappings/Product2.sdl` | SDL mapping file |

## Impact

- **Affected specs**: airflow-dag
- **Affected code**: `dags/`, `salesforce/dataloader_conf/`
- **Breaking changes**: None (เพิ่ม DAG ใหม่ ไม่กระทบของเดิม)

## Sample Table: 12_Product & Price

### Source Tables (KP Tables)

| Table | Description |
|-------|-------------|
| `KPS_T_REQPROD_MD` | ข้อมูลสินค้าที่ขออนุมัติ (Main) |
| `KPS_T_APPRV_M` | ข้อมูลการอนุมัติ |
| `KPS_R_CONCESS` | Reference: สัมปทาน |
| `KPS_R_SHOP` | Reference: บริษัท |
| `KPS_R_SHOP_BRAND` | Reference: ร้านค้า (มี CON_CODE, SHOP_CODE เป็น composite key) |
| `KPS_R_UNIT` | Reference: หน่วยนับ |

### Field Mapping (KP Table.KP Field Name → Salesforce)

| No | SFDC API Name | KP Table | KP Field Name | Type |
|----|---------------|----------|---------------|------|
| 1 | TMS_Concession__c | KPS_T_APPRV_M + KPS_R_CONCESS | CON_CODE, CON_LNAME | Lookup |
| 2 | TMS_Company_Name__c | KPS_T_APPRV_M + KPS_R_SHOP | SHOP_CODE, SHOP_NAME_E | Lookup |
| 3 | TMS_Shop_Name__c | KPS_T_APPRV_M + KPS_R_SHOP_BRAND | SHPBND_CODE, SHPBND_NAME_E | Lookup |
| 4 | TMS_Bar_Code__c | KPS_T_REQPROD_MD | BARCODE | Text(100) |
| 5 | TMS_Unit__c | KPS_T_APPRV_M + KPS_R_UNIT | UNIT_CODE, UNIT_DESC | Picklist |
| 6 | TMS_Start_Date__c | KPS_T_APPRV_M | KPS_EFF_SDATE | DateTime |
| 7 | TMS_End_Date__c | KPS_T_APPRV_M | KPS_EFF_EDATE | DateTime |
| 8 | TMS_Document_No_Ticket_No__c | KPS_T_APPRV_M | KPS_REASON | Text(100) |
| 9 | CreatedDate | KPS_T_REQPROD_MD | REQUEST_DATE | DateTime |
| 10 | TMS_Product_Category_Code__c | KPS_T_REQPROD_MD | STD_CATE_CODE | Text(100) |
| 11 | ProductCode | KPS_T_REQPROD_MD | PROD_SERV_CODE | Text (External ID) |
| 12 | Name | KPS_T_REQPROD_MD | PROD_SERV_NAME | Text(255) |
| 13 | TMS_Product_Name_TH__c | (New field) | - | Text(255) |
| 14 | TMS_Product_Weight__c | (New field) | - | Number(16,2) |
| 15 | TMS_Product_Type__c | KPS_T_REQPROD_MD | TRANS_TYPE | Picklist |
| 16 | TMS_Price_EXC_VAT__c | KPS_T_REQPROD_MD | KPS_PRICE_EXC_VAT | Number(16,2) |
| 17 | TMS_Price_INC_VAT__c | KPS_T_REQPROD_MD | KPS_PRICE_INC_VAT | Number(16,2) |

### SQL Query (Extract)

```sql
SELECT
    -- จาก KPS_T_REQPROD_MD
    r.BARCODE,
    r.STD_CATE_CODE,
    r.PROD_SERV_CODE,
    r.PROD_SERV_NAME,
    r.TRANS_TYPE,
    r.KPS_PRICE_EXC_VAT,
    r.KPS_PRICE_INC_VAT,
    r.REQUEST_DATE,
    -- จาก KPS_T_APPRV_M
    a.KPS_EFF_SDATE,
    a.KPS_EFF_EDATE,
    a.KPS_REASON,
    -- Lookup: Concession
    c.CON_CODE || ' : ' || c.CON_LNAME AS CONCESSION,
    -- Lookup: Company
    s.SHOP_CODE || ' ' || s.SHOP_NAME_E AS COMPANY_NAME,
    -- Lookup: Shop Brand
    sb.SHPBND_CODE || ' - ' || sb.SHPBND_NAME_E AS SHOP_NAME,
    -- Lookup: Unit
    u.UNIT_CODE || ' - ' || u.UNIT_DESC AS UNIT
FROM KPS_T_REQPROD_MD r
JOIN KPS_T_APPRV_M a ON r.APPRV_ID = a.APPRV_ID
LEFT JOIN KPS_R_CONCESS c ON a.CON_CODE = c.CON_CODE
LEFT JOIN KPS_R_SHOP s ON a.SHOP_CODE = s.SHOP_CODE
LEFT JOIN KPS_R_SHOP_BRAND sb ON a.CON_CODE = sb.CON_CODE AND a.SHOP_CODE = sb.SHOP_CODE AND a.SHPBND_CODE = sb.SHPBND_CODE
LEFT JOIN KPS_R_UNIT u ON a.UNIT_CODE = u.UNIT_CODE
```

### Sample CSV Output Format

```csv
"TMS_Bar_Code__c","TMS_Unit__c","TMS_Start_Date__c","TMS_End_Date__c","TMS_Product_Category_Code__c","ProductCode","Name","TMS_Product_Name_TH__c","TMS_Product_Weight__c","TMS_Price_EXC_VAT__c","TMS_Price_INC_VAT__c"
"1111","Gram","2026-01-20T19:17:15.000+0700","2027-01-19T19:17:15.000+0700","FB","P0200","Latte","ลาเต้","100","100","107"
```
