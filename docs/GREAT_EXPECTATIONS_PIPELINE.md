# Great Expectations Pipeline Documentation

> การทำงานของ Great Expectations ใน `migrate_product_price_dag.py`

## Table of Contents

- [Pipeline Overview](#pipeline-overview)
- [Batch Configuration](#batch-configuration)
- [GX Validation Points](#gx-validation-points)
- [Core Function: run_gx_validation()](#core-function-run_gx_validation)
- [Validation Details](#validation-details)
  - [Source Validation](#1-source-validation---ตรวจสอบขอมูลตนทาง-oracle)
  - [Extract Validation (Per-Batch)](#2-extract-validation---ตรวจสอบไฟล-csv-ที่-extract-per-batch)
  - [Post-Migration Validation (Per-Batch)](#3-post-migration-validation---reconciliation-per-batch)
- [Expectation Suites Reference](#expectation-suites-reference)
- [Expectation Suite JSON Structure](#expectation-suite-json-structure)
- [Data Quality Gates Summary](#data-quality-gates-summary)

---

## Pipeline Overview

```
┌─────────────────┐    ┌─────────────┐    ┌──────────────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────────┐
│ validate_source │ -> │ extract_data│ -> │ validate_extract │ -> │ run_dataloader│ -> │ audit_results│ -> │ validate_postmig │
│     (GX)        │    │   (Oracle)  │    │      (GX)        │    │  (Salesforce) │    │   (Logs)    │    │      (GX)        │
└─────────────────┘    └─────────────┘    └──────────────────┘    └───────────────┘    └─────────────┘    └──────────────────┘
      ❶                     ❷                    ❸                      ❹                   ❺                    ❻
                       (Batch Split)        (Per-Batch)           (Sequential)                            (Aggregated)
```

**Pipeline Steps:**

1. **validate_source** - GX validation on Oracle source data
2. **extract_data** - Query Oracle → Split into batch CSV files
3. **validate_extract** - GX validation on each batch file
4. **run_dataloader** - Upload batches sequentially to Salesforce
5. **audit_results** - Check aggregated error/success logs
6. **validate_postmig** - GX reconciliation check with per-batch breakdown

---

## Batch Configuration

> **New Feature:** Batch splitting สำหรับ handle ข้อมูลจำนวนมาก

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `batch_size` | 40,000 | จำนวน records ต่อ batch file |
| `start_batch` | 1 | Batch ที่จะเริ่มต้น (สำหรับ resume) |

### How to Configure

**Option 1: DAG Run Config** (highest priority)

```bash
airflow dags trigger migrate_product_price --conf '{"batch_size": 10000}'
```

**Option 2: Airflow Variable**

```bash
airflow variables set batch_size 50000
```

**Option 3: Default** (in DAG code)

```python
DEFAULT_BATCH_SIZE = 40000
```

### Batch Output Files

```
salesforce/data/
├── Product2_batch_001.csv    # Batch 1: rows 1-40000
├── Product2_batch_002.csv    # Batch 2: rows 40001-80000
└── ...
```

### Resume Functionality

หาก upload ล้มเหลว สามารถ resume จาก batch ที่ต้องการ:

```bash
# Resume จาก batch 3 (ข้าม batch 1-2 ที่ upload สำเร็จแล้ว)
airflow dags trigger migrate_product_price --conf '{"start_batch": 3}'
```

---

## GX Validation Points

Great Expectations ถูกเรียกใช้ที่ 3 จุดใน pipeline:

| Step | Task | Suite Name | Function | Location |
|------|------|------------|----------|----------|
| ❶ | `validate_source` | `source_product_price` | `validate_source_data()` | `migrate_product_price_dag.py:239-244` |
| ❸ | `validate_extract` | `extract_product_price` | `validate_extract_data()` | `migrate_product_price_dag.py:276-281` |
| ❻ | `validate_postmig` | `postmig_product_price` | `validate_postmig_data()` | `migrate_product_price_dag.py:328-333` |

---

## Core Function: run_gx_validation()

> Location: `migrate_product_price_dag.py:141-215`

ทุก validation เรียกผ่าน function นี้:

```python
def run_gx_validation(df, suite_name, context_root, run_name="validation",
                      evaluation_parameters=None):
    """Run GX validation on a dataframe and persist results to data docs."""
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `df` | `pandas.DataFrame` | DataFrame ที่ต้องการ validate |
| `suite_name` | `str` | ชื่อ Expectation Suite (ไฟล์ JSON) |
| `context_root` | `str` | Path ไปยัง GX context directory |
| `run_name` | `str` | ชื่อ run สำหรับ identifier |
| `evaluation_parameters` | `dict` | Runtime parameters สำหรับ `$PARAMETER` references |

### Flow Diagram

```
                    ┌──────────────────────────────────────────────────────────┐
                    │                 run_gx_validation()                      │
                    └──────────────────────────────────────────────────────────┘
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
┌───────────────────┐             ┌─────────────────────┐             ┌───────────────────┐
│ 1. Get GX Context │             │ 2. Setup Datasource │             │ 3. Create Batch   │
│                   │             │    (Runtime)        │             │    Request        │
│ gx.get_context()  │             │                     │             │                   │
│   (line 156)      │             │ PandasExecutionEngine│            │ RuntimeBatchRequest│
└───────────────────┘             │   (line 162-178)    │             │   (line 181-187)  │
                                  └─────────────────────┘             └───────────────────┘
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
┌───────────────────┐             ┌─────────────────────┐             ┌───────────────────┐
│ 4. Get Validator  │             │ 5. Run Validation   │             │ 6. Store Results  │
│                   │             │                     │             │    & Build Docs   │
│ Links DataFrame   │ ──────────► │ validator.validate()│ ──────────► │                   │
│ + Expectation Suite│            │   (line 196)        │             │ build_data_docs() │
│   (line 190-193)  │             │                     │             │   (line 212)      │
└───────────────────┘             └─────────────────────┘             └───────────────────┘
```

### Step-by-Step Explanation

#### Step 1: Get GX Context

```python
gx_context = gx.get_context(context_root_dir=context_root)
```

โหลด Great Expectations context จาก directory ที่กำหนด (`great_expectations/`)

#### Step 2: Setup Runtime Datasource

```python
datasource_config = {
    "name": "runtime_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine",
    },
    "data_connectors": {
        "runtime_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["batch_id"],
        }
    },
}
gx_context.add_datasource(**datasource_config)
```

สร้าง datasource แบบ runtime สำหรับรับ DataFrame โดยตรง

#### Step 3: Create Batch Request

```python
batch_request = RuntimeBatchRequest(
    datasource_name="runtime_datasource",
    data_connector_name="runtime_connector",
    data_asset_name=run_name,
    runtime_parameters={"batch_data": df},
    batch_identifiers={"batch_id": run_name},
)
```

สร้าง batch request โดยส่ง DataFrame เข้าไปใน `runtime_parameters`

#### Step 4: Get Validator

```python
validator = gx_context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=suite_name,
)
```

เชื่อม DataFrame กับ Expectation Suite ที่ต้องการ

#### Step 5: Run Validation

```python
results = validator.validate(
    result_format="COMPLETE",
    evaluation_parameters=evaluation_parameters or {}
)
```

รัน validation พร้อมส่ง Evaluation Parameters สำหรับ `$PARAMETER` references และ return ผลลัพธ์แบบ COMPLETE (รวมทุก details)

#### Step 6: Store Results & Build Docs

```python
gx_context.validations_store.set(validation_result_id, results)
gx_context.build_data_docs()
```

บันทึกผลลัพธ์และ generate Data Docs (HTML reports)

---

## Validation Details

### 1. Source Validation - ตรวจสอบข้อมูลต้นทาง (Oracle)

> Location: `migrate_product_price_dag.py:218-257`

**Purpose:** ป้องกัน garbage in → garbage out

**Timing:** ก่อน extract ข้อมูล

**Behavior:** **BLOCKING** - ถ้า fail จะหยุด pipeline ทันที

```python
def validate_source_data(**context):
    # Get data from Oracle
    oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
    df = oracle_hook.get_pandas_df(validation_query)

    # Run GX validation
    results = run_gx_validation(
        df=df,
        suite_name="source_product_price",
        context_root=context_root,
        run_name="source_validation",
    )

    # BLOCKING: Raise error if validation fails
    if not results.success:
        failed = [r.expectation_config.expectation_type for r in results.results if not r.success]
        raise ValueError(f"Source validation failed: {failed}")
```

**Expectation Suite:** `source_product_price.json`

| Expectation | Column | Description |
|-------------|--------|-------------|
| `expect_column_values_to_not_be_null` | BARCODE | BARCODE ห้ามเป็น NULL |
| `expect_column_values_to_not_be_null` | STD_CATE_CODE | STD_CATE_CODE ห้ามเป็น NULL |
| `expect_table_row_count_to_be_between` | - | ต้องมีข้อมูลอย่างน้อย 1 row |

---

### 2. Extract Validation - ตรวจสอบไฟล์ CSV ที่ Extract (Per-Batch)

> Location: `migrate_product_price_dag.py:566-637`

**Purpose:** ตรวจสอบว่า extract ถูกต้อง ข้อมูลไม่เพี้ยนระหว่าง transformation

**Timing:** หลัง extract ก่อน load เข้า Salesforce

**Behavior:** **NON-BLOCKING** - Warning เท่านั้น ไม่หยุด pipeline

**Batch Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Per-Batch Extract Validation                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   batch_001.csv ──► GX validate ──► extract_validation_batch_001│
│   batch_002.csv ──► GX validate ──► extract_validation_batch_002│
│   batch_003.csv ──► GX validate ──► extract_validation_batch_003│
│   ...                                                            │
│                                                                  │
│   Final: Aggregate results ──► Log summary + failed batches     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

```python
def validate_extract_data(**context):
    # Get extract result from XCom
    ti = context["ti"]
    extract_result = ti.xcom_pull(task_ids="extract_data")
    batch_files = extract_result.get("batch_files", [])

    # Validate each batch individually
    for i, batch_file in enumerate(batch_files, start=1):
        df = pd.read_csv(batch_file)

        results = run_gx_validation(
            df=df,
            suite_name="extract_product_price",
            context_root=context_root,
            run_name=f"extract_validation_batch_{i:03d}",  # Per-batch run name
            evaluation_parameters={
                "batch_row_count": len(df),
                "source_count": total_records
            }
        )

        if not results.success:
            failed_batches.append(i)

    # NON-BLOCKING: Log warning with failed batch numbers
    if failed_batches:
        logging.warning(f"Extract validation: WARN - batches failed: {failed_batches}")
```

**Per-Batch Data Docs:**

แต่ละ batch จะมี validation result แยกกันใน Data Docs:

```
great_expectations/uncommitted/validations/
└── extract_product_price/
    ├── extract_validation_batch_001/
    ├── extract_validation_batch_002/
    └── extract_validation_batch_003/
```

**Expectation Suite:** `extract_product_price.json`

| Expectation | Column | Description |
|-------------|--------|-------------|
| `expect_table_row_count_to_be_between` | - | batch มีข้อมูลอย่างน้อย 1 row |
| `expect_column_values_to_be_between` | KPS_PRICE_EXC_VAT | ราคาต้อง >= 0 |

---

### 3. Post-Migration Validation - Reconciliation (Per-Batch)

> Location: `migrate_product_price_dag.py:640-721`

**Purpose:** ตรวจสอบว่า load ครบ ไม่มีข้อมูลหาย (Reconciliation)

**Timing:** หลัง load ขึ้น Salesforce

**Behavior:** **NON-BLOCKING** - Alert เท่านั้น แจ้งเตือนแต่ไม่หยุด pipeline

**Per-Batch Reconciliation:**

```
┌─────────────────────────────────────────────────────────────────┐
│              Per-Batch Reconciliation Report                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Batch   Extracted    Loaded    Difference                     │
│   ─────   ─────────    ──────    ──────────                     │
│   001     40,000       39,998    2                              │
│   002     40,000       40,000    0                              │
│   003     800          800       0                              │
│   ─────   ─────────    ──────    ──────────                     │
│   TOTAL   80,800       80,798    2                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

```python
def validate_postmig_data(**context):
    # Get extract result from XCom
    ti = context["ti"]
    extract_result = ti.xcom_pull(task_ids="extract_data")
    batch_files = extract_result.get("batch_files", [])

    # Per-batch reconciliation logging
    batch_reconciliation = []
    for i, batch_file in enumerate(batch_files, start=1):
        batch_df = pd.read_csv(batch_file)
        batch_extracted = len(batch_df)

        # Read per-batch success log
        batch_name = os.path.basename(batch_file).replace(".csv", "")
        batch_success_log = os.path.join(LOG_DIR, f"{batch_name}_success.csv")
        batch_loaded = len(pd.read_csv(batch_success_log))

        batch_diff = batch_extracted - batch_loaded
        logging.info(f"Batch {i:03d}: {batch_extracted} extracted, {batch_loaded} loaded, {batch_diff} diff")

    # Use aggregated success log for GX validation
    success_log = os.path.join(LOG_DIR, "Product2_success.csv")
    df = pd.read_csv(success_log)

    results = run_gx_validation(
        df=df,
        suite_name="postmig_product_price",
        context_root=context_root,
        run_name="postmig_validation",
        evaluation_parameters={"source_count": total_records}
    )
```

**Log Aggregation:**

```
salesforce/logs/
├── Product2_batch_001_success.csv   # Per-batch logs
├── Product2_batch_001_error.csv
├── Product2_batch_002_success.csv
├── Product2_batch_002_error.csv
├── ...
├── Product2_success.csv             # Aggregated success log
└── Product2_error.csv               # Aggregated error log
```

**Expectation Suite:** `postmig_product_price.json`

| Expectation | Column | Description |
|-------------|--------|-------------|
| `expect_table_row_count_to_equal` | - | จำนวน row ที่ load = source_count |

---

## Expectation Suites Reference

### File Locations

```
great_expectations/
└── expectations/
    ├── source_product_price.json    # Source validation
    ├── extract_product_price.json   # Extract validation
    └── postmig_product_price.json   # Post-migration validation
```

### Suite Structure (JSON Format)

```json
{
    "expectation_suite_name": "suite_name",
    "data_asset_type": null,
    "expectations": [
        {
            "expectation_type": "expect_column_values_to_not_be_null",
            "kwargs": {
                "column": "COLUMN_NAME"
            },
            "meta": {}
        }
    ],
    "meta": {
        "great_expectations_version": "0.18.8"
    }
}
```

### Common Expectations Used

| Expectation | Description | Official Docs |
|-------------|-------------|---------------|
| `expect_column_values_to_not_be_null` | Column ต้องไม่มีค่า NULL | [Link](https://greatexpectations.io/expectations/expect_column_values_to_not_be_null/) |
| `expect_table_row_count_to_be_between` | จำนวน row อยู่ในช่วงที่กำหนด | [Link](https://greatexpectations.io/expectations/expect_table_row_count_to_be_between/) |
| `expect_table_row_count_to_equal` | จำนวน row เท่ากับค่าที่กำหนด | [Link](https://greatexpectations.io/expectations/expect_table_row_count_to_equal/) |
| `expect_column_values_to_be_between` | ค่าใน column อยู่ในช่วงที่กำหนด | [Link](https://greatexpectations.io/expectations/expect_column_values_to_be_between/) |

---

## Expectation Suite JSON Structure

### วิธีหา Documentation สำหรับ JSON Structure

#### 1. โครงสร้างหลักของ Expectation Suite

| Field | คำอธิบาย | Official Docs |
|-------|----------|---------------|
| `expectation_suite_name` | ชื่อ suite (unique) | [ExpectationSuite](https://docs.greatexpectations.io/docs/0.18/reference/api/core/expectationsuite_class/) |
| `data_asset_type` | ประเภท data asset (optional) | - |
| `expectations` | Array ของ expectations | - |
| `meta` | Metadata (GX version, etc.) | - |

#### 2. โครงสร้างของแต่ละ Expectation

```json
{
    "expectation_type": "expect_column_values_to_not_be_null",
    "kwargs": { ... },
    "meta": {}
}
```

| Field | คำอธิบาย | Official Docs |
|-------|----------|---------------|
| `expectation_type` | ชื่อ expectation (snake_case) | [ExpectationConfiguration](https://docs.greatexpectations.io/docs/0.18/reference/api/expectations/expectation_configuration/expectationconfiguration_class/) |
| `kwargs` | Parameters สำหรับ expectation นั้นๆ | ดูจาก Expectation Gallery |
| `meta` | Metadata เพิ่มเติม (optional) | - |

#### 3. วิธีหา `kwargs` ของแต่ละ Expectation

**ใช้ Expectation Gallery:** [https://greatexpectations.io/expectations/](https://greatexpectations.io/expectations/)

ตัวอย่าง: ค้นหา `expect_column_values_to_be_between`

```
https://greatexpectations.io/expectations/expect_column_values_to_be_between/
```

จะแสดง:

- **Required kwargs:** `column`
- **Optional kwargs:** `min_value`, `max_value`, `mostly`, `strict_min`, `strict_max`

#### 4. Evaluation Parameters (`$PARAMETER`)

ใช้สำหรับส่งค่า dynamic ตอน runtime:

```json
{
    "expectation_type": "expect_table_row_count_to_equal",
    "kwargs": {
        "value": {
            "$PARAMETER": "source_count"
        }
    }
}
```

เมื่อ validate ต้องส่งค่าเข้าไป:

```python
results = validator.validate(
    evaluation_parameters={"source_count": 1000}
)
```

**Official Docs:** [Evaluation Parameter](https://docs.greatexpectations.io/docs/0.18/reference/learn/terms/evaluation_parameter/)

#### 5. Quick Reference: kwargs ที่ใช้บ่อย

| Expectation | Required kwargs | Optional kwargs |
|-------------|-----------------|-----------------|
| `expect_column_values_to_not_be_null` | `column` | `mostly` |
| `expect_column_values_to_be_between` | `column` | `min_value`, `max_value`, `mostly` |
| `expect_table_row_count_to_equal` | `value` | - |
| `expect_table_row_count_to_be_between` | - | `min_value`, `max_value` |
| `expect_column_values_to_be_in_set` | `column`, `value_set` | `mostly` |
| `expect_column_values_to_match_regex` | `column`, `regex` | `mostly` |

#### 6. Documentation Resources

| Resource | URL | ใช้ทำอะไร |
|----------|-----|----------|
| **Expectation Gallery** | [greatexpectations.io/expectations](https://greatexpectations.io/expectations/) | หา kwargs ของแต่ละ expectation |
| **ExpectationConfiguration API** | [docs](https://docs.greatexpectations.io/docs/0.18/reference/api/expectations/expectation_configuration/expectationconfiguration_class/) | โครงสร้าง expectation_type, kwargs, meta |
| **ExpectationSuite API** | [docs](https://docs.greatexpectations.io/docs/0.18/reference/api/core/expectationsuite_class/) | โครงสร้าง suite |
| **Evaluation Parameter** | [docs](https://docs.greatexpectations.io/docs/0.18/reference/learn/terms/evaluation_parameter/) | วิธีใช้ $PARAMETER |

---

## Data Quality Gates Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Data Quality Gates                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Oracle           CSV                 Salesforce          Success Log      │
│     │               │                      │                    │           │
│     ▼               ▼                      ▼                    ▼           │
│  ┌──────┐       ┌──────┐              ┌──────┐            ┌──────┐         │
│  │ GX 1 │ ───►  │ GX 2 │  ──────────► │ Load │  ────────► │ GX 3 │         │
│  │Source│       │Extract│             │      │            │PostMig│         │
│  └──────┘       └──────┘              └──────┘            └──────┘         │
│     │               │                                          │           │
│     │               │                                          │           │
│  BLOCKING       NON-BLOCKING                              NON-BLOCKING     │
│  (fail = stop)  (warn only)                               (alert only)     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Gate Behaviors

| Gate | Suite | Purpose | On Failure |
|------|-------|---------|------------|
| **GX 1 (Source)** | `source_product_price` | ไม่ดึงข้อมูลเสียเข้ามา | **BLOCK** - หยุด pipeline |
| **GX 2 (Extract)** | `extract_product_price` | ตรวจสอบ transformation | **WARN** - บันทึก log |
| **GX 3 (PostMig)** | `postmig_product_price` | Reconciliation check | **ALERT** - แจ้งเตือน |

### Design Rationale

1. **Source Validation (Blocking)**
   - ถ้าข้อมูลต้นทางไม่ดี ไม่ควร extract ออกมา
   - ป้องกันการ load ข้อมูลเสียเข้า Salesforce

2. **Extract Validation (Non-blocking)**
   - ตรวจสอบ data transformation
   - ไม่ block เพราะอาจมี edge cases ที่ยอมรับได้

3. **Post-Migration Validation (Non-blocking)**
   - เป็น reconciliation check
   - แจ้งเตือนเพื่อให้ทีมตรวจสอบ แต่ไม่ fail pipeline
   - บาง records อาจ fail ด้วยเหตุผลที่ยอมรับได้ (duplicate, validation rules)

---

## Related Documentation

- [GREAT_EXPECTATIONS_GUIDE.md](GREAT_EXPECTATIONS_GUIDE.md) - GX integration guide
- [PIPELINE_DESIGN.md](PIPELINE_DESIGN.md) - Complete pipeline implementation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Migration architecture design

## Official Resources

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Expectation Gallery](https://greatexpectations.io/expectations/)
- [GX 0.18 Reference](https://docs.greatexpectations.io/docs/0.18/reference/learn/terms/expectation_suite/)
