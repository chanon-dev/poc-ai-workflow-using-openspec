# Great Expectations (GX) Usage Guide

คู่มือการใช้งาน Great Expectations สำหรับ Data Quality Validation

## What is Great Expectations?

Great Expectations (GX) คือ framework สำหรับตรวจสอบคุณภาพข้อมูล (Data Quality) โดย:
- กำหนด **Expectations** (กฎที่ข้อมูลต้องผ่าน)
- รัน **Validation** (ตรวจสอบข้อมูลจริงกับกฎ)
- สร้าง **Data Docs** (รายงาน HTML แสดงผลการตรวจสอบ)

## Project Structure

```
great_expectations/
├── great_expectations.yml     # Config หลัก
├── expectations/              # Expectation Suites (กฎ)
│   ├── source_product_price.json
│   ├── extract_product_price.json
│   └── postmig_product_price.json
├── checkpoints/               # Checkpoint configs
├── plugins/                   # Custom expectations
└── uncommitted/               # ไม่ commit เข้า git
    ├── data_docs/             # HTML Reports
    │   └── local_site/
    │       └── index.html     # <-- เปิดไฟล์นี้ดู report
    └── validations/           # Validation results (JSON)
```

## Quick Start

### 1. View Data Docs (HTML Report)

```bash
# เปิด report ใน browser
open great_expectations/uncommitted/data_docs/local_site/index.html
```

### 2. Run Validation via DAG

Validation จะรันอัตโนมัติเมื่อ trigger DAG `migrate_product_price`:

```
Pipeline Flow:
validate_source → extract_data → validate_extract → run_dataloader → audit_results → validate_postmig
```

### 3. Run Validation Manually (ใน Docker)

```bash
# เข้าไปใน container
docker compose exec airflow-worker bash

# รัน Python script
python -c "
import great_expectations as gx
context = gx.get_context(context_root_dir='/opt/airflow/great_expectations')
print(context.list_expectation_suite_names())
"
```

## Understanding Expectation Suites

### Suite 1: `source_product_price`
**Purpose:** ตรวจสอบ source data ใน Oracle ก่อน extract

| Expectation | Description |
|-------------|-------------|
| `expect_column_values_to_not_be_null(BARCODE)` | BARCODE ต้องไม่เป็น NULL |
| `expect_column_values_to_not_be_null(STD_CATE_CODE)` | STD_CATE_CODE ต้องไม่เป็น NULL |
| `expect_table_row_count_to_be_between(min=1)` | ต้องมีข้อมูลอย่างน้อย 1 row |

### Suite 2: `extract_product_price`
**Purpose:** ตรวจสอบ CSV หลัง extract

| Expectation | Description |
|-------------|-------------|
| `expect_table_row_count_to_equal(source_count)` | จำนวน row ต้องตรงกับ source |
| `expect_column_values_to_be_between(KPS_PRICE_EXC_VAT, min=0)` | ราคาต้อง >= 0 |

### Suite 3: `postmig_product_price`
**Purpose:** Reconciliation หลัง load เข้า Salesforce

| Expectation | Description |
|-------------|-------------|
| `expect_table_row_count_to_equal(source_count)` | จำนวน row ที่ load สำเร็จต้องตรงกับ source |

## How to Add New Expectations

### Step 1: Edit Expectation Suite JSON

```bash
# เปิดไฟล์ suite
code great_expectations/expectations/source_product_price.json
```

### Step 2: Add New Expectation

```json
{
    "expectation_suite_name": "source_product_price",
    "expectations": [
        // ... existing expectations ...
        {
            "expectation_type": "expect_column_values_to_match_regex",
            "kwargs": {
                "column": "BARCODE",
                "regex": "^[0-9]{13}$"
            },
            "meta": {
                "notes": "BARCODE must be 13 digits"
            }
        }
    ]
}
```

### Step 3: Test the New Expectation

```bash
# Trigger DAG เพื่อทดสอบ
docker compose exec airflow-worker airflow dags test migrate_product_price
```

## Common Expectation Types

| Type | Description | Example |
|------|-------------|---------|
| `expect_column_values_to_not_be_null` | Column ต้องไม่มี NULL | `{"column": "ID"}` |
| `expect_column_values_to_be_unique` | ค่าใน column ต้องไม่ซ้ำ | `{"column": "EMAIL"}` |
| `expect_column_values_to_be_between` | ค่าต้องอยู่ในช่วง | `{"column": "AGE", "min_value": 0, "max_value": 150}` |
| `expect_column_values_to_match_regex` | ค่าต้องตรง pattern | `{"column": "PHONE", "regex": "^0[0-9]{9}$"}` |
| `expect_table_row_count_to_be_between` | จำนวน row ต้องอยู่ในช่วง | `{"min_value": 1, "max_value": 1000000}` |
| `expect_column_values_to_be_in_set` | ค่าต้องอยู่ใน list ที่กำหนด | `{"column": "STATUS", "value_set": ["A", "I"]}` |

See full list: https://greatexpectations.io/expectations/

## Reading the HTML Report

### Main Dashboard (`index.html`)
- **Expectation Suites:** รายการ suite ทั้งหมด
- **Validation Results:** ผลการ validate แต่ละครั้ง

### Validation Result Page
- **Status:** PASS (สีเขียว) / FAIL (สีแดง)
- **Statistics:** จำนวน expectations ที่ผ่าน/ไม่ผ่าน
- **Details:** รายละเอียดแต่ละ expectation
  - `element_count`: จำนวน row ทั้งหมด
  - `unexpected_count`: จำนวน row ที่ไม่ผ่าน
  - `unexpected_percent`: เปอร์เซ็นต์ที่ไม่ผ่าน
  - `partial_unexpected_list`: ตัวอย่างค่าที่ไม่ผ่าน

## Troubleshooting

### Report ไม่ update หลังรัน validation

```bash
# Rebuild data docs manually
docker compose exec airflow-worker python -c "
import great_expectations as gx
context = gx.get_context(context_root_dir='/opt/airflow/great_expectations')
context.build_data_docs()
print('Data docs rebuilt!')
"
```

### ดู validation results ใน container

```bash
# List validation files
docker compose exec airflow-worker ls -la /opt/airflow/great_expectations/uncommitted/validations/
```

### Expectation suite not found

ตรวจสอบว่า:
1. ไฟล์ JSON อยู่ใน `great_expectations/expectations/`
2. ชื่อ suite ใน JSON ตรงกับที่เรียกใน code
3. Volume mount ถูกต้องใน `docker-compose.yaml`

## Integration with Airflow DAG

### Validation Flow in DAG

```python
# 1. validate_source - ก่อน extract
validate_source_data()
  └── run_gx_validation(df, "source_product_price")
        └── validator.validate()
        └── store validation result
        └── build_data_docs()

# 2. validate_extract - หลัง extract
validate_extract_data()
  └── run_gx_validation(df, "extract_product_price")

# 3. validate_postmig - หลัง load
validate_postmig_data()
  └── run_gx_validation(df, "postmig_product_price")
```

### Validation Behavior

| Task | On Failure |
|------|------------|
| `validate_source` | **Blocks pipeline** - ไม่ให้ extract ถ้า source data มีปัญหา |
| `validate_extract` | **Warning only** - log warning แต่ไม่ block |
| `validate_postmig` | **Warning only** - log reconciliation alert |

## Best Practices

1. **Start Simple:** เริ่มจาก expectations พื้นฐาน (not null, row count) แล้วค่อยเพิ่ม
2. **Document Expectations:** ใส่ `meta.notes` อธิบายว่าทำไมต้องมี expectation นี้
3. **Monitor Reports:** ดู data docs เป็นประจำเพื่อ track data quality trends
4. **Version Control:** Commit expectation suites เข้า git (แต่ไม่ commit `uncommitted/`)

## References

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Expectation Gallery](https://greatexpectations.io/expectations/)
- [GX GitHub](https://github.com/great-expectations/great_expectations)
