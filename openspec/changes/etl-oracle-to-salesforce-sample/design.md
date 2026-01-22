# Design: Centralized Setup DAG Pattern

## Architecture Overview

แบ่ง DAG ออกเป็น 2 ประเภท:

```text
┌─────────────────────────────────────────────────────────────┐
│                    SETUP PHASE (Manual)                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │          setup_salesforce_pipeline DAG               │    │
│  │  ┌──────────┐  ┌──────────────┐  ┌──────────────┐   │    │
│  │  │ Encrypt  │→ │ Generate     │→ │ Generate     │   │    │
│  │  │ Creds    │  │ process-conf │  │ .sdl files   │   │    │
│  │  └──────────┘  └──────────────┘  └──────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↓                                  │
│            Creates: Master process-conf.xml                  │
│                     All .sdl mapping files                   │
└─────────────────────────────────────────────────────────────┘
                            ↓ (Read-Only)
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTION PHASE (Scheduled)                 │
│  ┌───────────────────────┐  ┌───────────────────────┐       │
│  │ migrate_product_price │  │ migrate_sales_data    │  ...  │
│  │  ┌──────┐ ┌──────┐    │  │  ┌──────┐ ┌──────┐    │       │
│  │  │Extract│→│ Load │    │  │  │Extract│→│ Load │    │       │
│  │  └──────┘ └──────┘    │  │  └──────┘ └──────┘    │       │
│  └───────────────────────┘  └───────────────────────┘       │
│         ↓                           ↓                        │
│    Uses same Master Config (No Race Condition)               │
└─────────────────────────────────────────────────────────────┘
```

## Setup DAG (`setup_salesforce_pipeline`)

**Trigger:** Manual - รันหลังจาก Deploy หรือเปลี่ยน Config

### Setup Tasks

1. **encrypt_credentials**
   - รวม Password + Security Token
   - Encrypt ด้วย Data Loader Key
   - บันทึกลง Airflow Variables

2. **generate_master_config**
   - อ่าน `tables_config.py` + `field_mappings.py`
   - สร้าง `process-conf.xml` รวมทุกตาราง
   - Output: `/opt/airflow/salesforce/dataloader_conf/process-conf.xml`

3. **generate_sdl_mappings**
   - สร้าง `.sdl` files สำหรับทุกตาราง
   - Output: `/opt/airflow/salesforce/dataloader_conf/mappings/*.sdl`

## Execution DAG (`migrate_product_price`)

**Trigger:** Schedule หรือ Manual

### Pipeline Flow

```text
[extract_data] → [run_dataloader] → [audit_results]
```

1. **extract_data**
   - Query: Multi-table JOIN (ตาม Spec)
   - Transform: Format dates, decimals
   - Output: `/opt/airflow/salesforce/data/Product2.csv`

2. **run_dataloader**
   - Command: `/opt/dataloader/process.sh {CONFIG_DIR} Product2_Process`
   - Read-Only จาก Master `process-conf.xml`

3. **audit_results**
   - Check `error.csv` และ `success.csv`
   - Log counts, fail if errors > 0

## Product & Price: Field Mapping ตาม Spec

### Source Tables (ตาม Data Dictionary)

| No | KP Table | Fields | Role |
|----|----------|--------|------|
| 1-3, 5-8 | `KPS_T_APPRV_M` | Approval + Lookups | JOIN |
| 4, 9-17, 20-22 | `KPS_T_REQPROD_MD` | Product Info | Main |
| 1 | `KPS_R_CONCESS` | CON_LNAME | Lookup |
| 2 | `KPS_R_SHOP` | SHOP_NAME_E | Lookup |
| 3 | `KPS_R_BRAND` | SHPBND_NAME_E | Lookup |
| 5 | `KPS_R_UNIT` | UNIT_DESC | Lookup |

### Field Mapping ตาม Spec Row by Row

| Row | SFDC API Name | KP Table | KP Field Name |
|-----|---------------|----------|---------------|
| 1 | TMS_Concession__c | KPS_T_APPRV_M + KPS_R_CONCESS | a.CON_CODE \|\| ' : ' \|\| c.CON_LNAME |
| 2 | TMS_Company_Name__c | KPS_T_APPRV_M + KPS_R_SHOP | a.SHOP_CODE \|\| ' ' \|\| s.SHOP_NAME_E |
| 3 | TMS_Shop_Name__c | KPS_T_APPRV_M + KPS_R_BRAND | a.SHPBND_CODE \|\| ' - ' \|\| b.SHPBND_NAME_E |
| 4 | TMS_Bar_Code__c | KPS_T_REQPROD_MD | r.BARCODE |
| 5 | TMS_Unit__c | KPS_T_APPRV_M + KPS_R_UNIT | a.UNIT_CODE \|\| ' - ' \|\| u.UNIT_DESC |
| 6 | TMS_Start_Date__c | KPS_T_APPRV_M | a.KPS_EFF_SDATE |
| 7 | TMS_End_Date__c | KPS_T_APPRV_M | a.KPS_EFF_EDATE |
| 8 | TMS_Document_No_Ticket_No__c | KPS_T_APPRV_M | a.KPS_REASON |
| 9 | CreatedDate | KPS_T_REQPROD_MD | r.REQUEST_DATE |
| 10 | TMS_Product_Category_Code__c | KPS_T_REQPROD_MD | r.STD_CATE_CODE |
| 11 | ProductCode | KPS_T_REQPROD_MD | r.PROD_SERV_CODE |
| 12 | Name | KPS_T_REQPROD_MD | r.PROD_SERV_NAME |
| 15 | TMS_Product_Type__c | KPS_T_REQPROD_MD | r.TRANS_TYPE |
| 16 | TMS_Price_EXC_VAT__c | KPS_T_REQPROD_MD | r.KPS_PRICE_EXC_VAT |
| 17 | TMS_Price_INC_VAT__c | KPS_T_REQPROD_MD | r.KPS_PRICE_INC_VAT |
| 20 | TMS_Ref_Source__c | KPS_T_REQPROD_MD | r.REF_SOURCE |
| 22 | TMS_Ref_Price__c | KPS_T_REQPROD_MD | r.REF_PRICE |

### SQL Query (Extract) - ตาม Spec

```sql
SELECT
    -- Row 1: Concession (KPS_T_APPRV_M + KPS_R_CONCESS)
    a.CON_CODE || ' : ' || c.CON_LNAME      AS TMS_Concession__c,

    -- Row 2: Company (KPS_T_APPRV_M + KPS_R_SHOP)
    a.SHOP_CODE || ' ' || s.SHOP_NAME_E     AS TMS_Company_Name__c,

    -- Row 3: Shop Brand (KPS_T_APPRV_M + KPS_R_BRAND)
    a.SHPBND_CODE || ' - ' || b.SHPBND_NAME_E AS TMS_Shop_Name__c,

    -- Row 4: Bar Code (KPS_T_REQPROD_MD)
    r.BARCODE                               AS TMS_Bar_Code__c,

    -- Row 5: Unit (KPS_T_APPRV_M + KPS_R_UNIT)
    a.UNIT_CODE || ' - ' || u.UNIT_DESC     AS TMS_Unit__c,

    -- Row 6-8: Approval Info (KPS_T_APPRV_M)
    a.KPS_EFF_SDATE                         AS TMS_Start_Date__c,
    a.KPS_EFF_EDATE                         AS TMS_End_Date__c,
    a.KPS_REASON                            AS TMS_Document_No_Ticket_No__c,

    -- Row 9-12: Product Info (KPS_T_REQPROD_MD)
    r.REQUEST_DATE                          AS CreatedDate,
    r.STD_CATE_CODE                         AS TMS_Product_Category_Code__c,
    r.PROD_SERV_CODE                        AS ProductCode,
    r.PROD_SERV_NAME                        AS Name,

    -- Row 15-17: Transaction & Price (KPS_T_REQPROD_MD)
    r.TRANS_TYPE                            AS TMS_Product_Type__c,
    r.KPS_PRICE_EXC_VAT                     AS TMS_Price_EXC_VAT__c,
    r.KPS_PRICE_INC_VAT                     AS TMS_Price_INC_VAT__c,

    -- Row 20, 22: Reference (KPS_T_REQPROD_MD)
    r.REF_SOURCE                            AS TMS_Ref_Source__c,
    r.REF_PRICE                             AS TMS_Ref_Price__c

FROM KPS_T_REQPROD_MD r
-- JOIN with Approval Master (composite key)
JOIN KPS_T_APPRV_M a
    ON  r.CON_CODE = a.CON_CODE
    AND r.SHOP_CODE = a.SHOP_CODE
    AND r.PROD_SERV_CODE = a.PROD_SERV_CODE
-- Lookup: Concession
LEFT JOIN KPS_R_CONCESS c
    ON a.CON_CODE = c.CON_CODE
-- Lookup: Shop/Company
LEFT JOIN KPS_R_SHOP s
    ON a.CON_CODE = s.CON_CODE
    AND a.SHOP_CODE = s.SHOP_CODE
-- Lookup: Brand
LEFT JOIN KPS_R_BRAND b
    ON a.SHPBND_CODE = b.SHPBND_CODE
-- Lookup: Unit
LEFT JOIN KPS_R_UNIT u
    ON a.UNIT_CODE = u.UNIT_CODE
```

### Join Diagram

```text
┌─────────────────────┐     ┌─────────────────────┐
│  KPS_T_REQPROD_MD   │     │   KPS_T_APPRV_M     │
│  (Product Request)  │────▶│   (Approval)        │
│                     │     │                     │
│  - BARCODE          │     │  - KPS_EFF_SDATE    │
│  - PROD_SERV_CODE   │     │  - KPS_EFF_EDATE    │
│  - PROD_SERV_NAME   │     │  - KPS_REASON       │
│  - STD_CATE_CODE    │     │  - CON_CODE ────────┼──▶ KPS_R_CONCESS
│  - TRANS_TYPE       │     │  - SHOP_CODE ───────┼──▶ KPS_R_SHOP
│  - KPS_PRICE_*      │     │  - SHPBND_CODE ─────┼──▶ KPS_R_BRAND
│  - REF_*            │     │  - UNIT_CODE ───────┼──▶ KPS_R_UNIT
└─────────────────────┘     └─────────────────────┘
         │
         └── JOIN ON (CON_CODE, SHOP_CODE, PROD_SERV_CODE)
```

### Field Mapping Configuration

```python
"Product2": FieldMapping(
    sf_object="Product2",
    external_id="ProductCode",
    mappings={
        # Lookups (from APPRV_M + Reference tables)
        "TMS_Concession__c": "TMS_Concession__c",
        "TMS_Company_Name__c": "TMS_Company_Name__c",
        "TMS_Shop_Name__c": "TMS_Shop_Name__c",
        "TMS_Unit__c": "TMS_Unit__c",
        # Approval Info (from APPRV_M)
        "TMS_Start_Date__c": "TMS_Start_Date__c",
        "TMS_End_Date__c": "TMS_End_Date__c",
        "TMS_Document_No_Ticket_No__c": "TMS_Document_No_Ticket_No__c",
        # Product Info (from REQPROD_MD)
        "TMS_Bar_Code__c": "TMS_Bar_Code__c",
        "TMS_Product_Category_Code__c": "TMS_Product_Category_Code__c",
        "ProductCode": "ProductCode",
        "Name": "Name",
        "TMS_Product_Type__c": "TMS_Product_Type__c",
        "TMS_Price_EXC_VAT__c": "TMS_Price_EXC_VAT__c",
        "TMS_Price_INC_VAT__c": "TMS_Price_INC_VAT__c",
        "TMS_Ref_Source__c": "TMS_Ref_Source__c",
        "TMS_Ref_Price__c": "TMS_Ref_Price__c",
        "CreatedDate": "CreatedDate",
    },
    transformations={
        "TMS_Start_Date__c": "to_sf_datetime",
        "TMS_End_Date__c": "to_sf_datetime",
        "CreatedDate": "to_sf_datetime",
        "TMS_Price_EXC_VAT__c": "to_decimal_2",
        "TMS_Price_INC_VAT__c": "to_decimal_2",
        "TMS_Ref_Price__c": "to_decimal_2",
    },
)
```

## File Structure

```text
/opt/airflow/salesforce/
├── certs/
│   └── key.txt                 # Encryption key (Setup DAG)
├── dataloader_conf/
│   ├── process-conf.xml        # Master Config (Setup DAG)
│   ├── config.properties       # Global settings
│   └── mappings/
│       ├── KPS_T_SALES_MD.sdl
│       └── Product2.sdl        # Product mapping
├── data/
│   └── Product2.csv            # Execution DAG output
└── logs/
    ├── Product2_success.csv
    └── Product2_error.csv
```

## Benefits

1. **No Race Condition** - Execution DAGs อ่าน Config เท่านั้น ไม่เขียน
2. **Parallel Safe** - หลาย DAG รันพร้อมกันได้
3. **Single Source of Truth** - Config อยู่ใน Code (`field_mappings.py`)
4. **Easy Maintenance** - แก้ Mapping แล้วรัน Setup DAG ครั้งเดียว
5. **Spec Compliant** - JOIN ตาม Data Dictionary ทุกประการ
