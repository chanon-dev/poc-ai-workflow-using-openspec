## Context

ปัจจุบัน `migrate_product_price_dag.py` สร้างไฟล์ CSV เดียว (`Product2.csv`) สำหรับ upload ไป Salesforce ซึ่งมีปัญหาเมื่อข้อมูลมีจำนวนมาก (หลายแสน - หลายล้าน records):

- Salesforce Data Loader timeout (default 60 minutes)
- Memory pressure เมื่อ load ไฟล์ใหญ่เข้า pandas
- ไม่สามารถ retry เฉพาะ batch ที่ fail

**Current Flow:**
```
Oracle → [extract_data] → Product2.csv → [run_dataloader] → Salesforce
                              │
                         (single file)
```

**Proposed Flow:**
```
Oracle → [extract_data] → Product2_batch_001.csv → [run_dataloader] → Salesforce
                        → Product2_batch_002.csv →
                        → Product2_batch_003.csv →
                              │
                         (multiple files)
```

## Goals / Non-Goals

**Goals:**

- แบ่งไฟล์ export เป็น batch ตาม configurable row count
- Upload ทีละ batch เพื่อหลีกเลี่ยง timeout
- รองรับ retry จาก batch ที่ fail
- รักษา GX validation และ reconciliation ที่มีอยู่

**Non-Goals:**

- Parallel upload (ทำ sequential เพื่อความง่ายและหลีกเลี่ยง rate limit)
- Dynamic batch sizing ตาม file size
- Compression/encryption ของ batch files

## Decisions

### Decision 1: Batch splitting using pandas chunking

**Approach:** ใช้ `numpy.array_split()` เพื่อแบ่ง DataFrame เป็น chunks

**Rationale:**
- ง่ายต่อการ implement และ debug
- รักษา order ของ data
- Memory efficient (ไม่ต้อง copy data)

**Alternatives considered:**
- `df.iloc[start:end]` - ต้องจัดการ index เอง
- `itertools.batched` (Python 3.12+) - ไม่รองรับ Python version ที่ใช้

```python
def split_dataframe(df, batch_size):
    n_batches = math.ceil(len(df) / batch_size)
    return np.array_split(df, n_batches)
```

### Decision 2: Configuration via Airflow Variable with DAG config override

**Approach:**
1. Default value in code: `BATCH_SIZE = 10000`
2. Override via Airflow Variable: `Variable.get("batch_size", default_var=10000)`
3. Override via DAG config: `dag_run.conf.get("batch_size")`

**Rationale:**
- ยืดหยุ่น - ปรับได้ทั้ง global และ per-run
- ไม่ต้อง redeploy DAG เพื่อเปลี่ยน batch size
- ตาม Airflow best practices

**Priority:** DAG config > Airflow Variable > Default

### Decision 3: Sequential upload with aggregated logs

**Approach:** Loop upload ทีละ batch แล้วรวม success/error logs

```python
all_success = []
all_errors = []
for batch_file in batch_files:
    run_dataloader(batch_file)
    all_success.extend(read_success_log())
    all_errors.extend(read_error_log())

write_aggregated_logs(all_success, all_errors)
```

**Rationale:**
- หลีกเลี่ยง Salesforce API rate limiting
- Debug ง่าย - เห็นว่า batch ไหน fail
- รองรับ resume จาก batch ที่ค้าง

**Alternatives considered:**
- Parallel upload - เสี่ยง rate limit, ซับซ้อนกว่า
- TaskGroup dynamic mapping - over-engineering สำหรับ use case นี้

### Decision 4: Per-batch GX validation with aggregated results

**Approach:** Validate แต่ละ batch แยก แล้วรวมผลลัพธ์

```python
batch_results = []
for i, batch_df in enumerate(batches):
    result = run_gx_validation(
        df=batch_df,
        suite_name="extract_product_price",
        run_name=f"extract_validation_batch_{i+1:03d}",
        evaluation_parameters={"batch_row_count": len(batch_df)}
    )
    batch_results.append(result)

overall_success = all(r.success for r in batch_results)
```

**Rationale:**
- เห็น validation result ของแต่ละ batch ใน Data Docs
- สามารถระบุได้ว่า batch ไหนมีปัญหา
- ใช้ GX infrastructure ที่มีอยู่แล้ว

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Batch size เล็กเกินไป → หลายไฟล์เกินไป | แนะนำ minimum 10000, warn ถ้าต่ำกว่า 1000 |
| Upload กลางทาง fail → ข้อมูลไม่ครบ | รองรับ `start_batch` config สำหรับ resume |
| Data Loader process-conf ต้องปรับ | ใช้ template หรือ dynamic config generation |
| Disk space สำหรับหลาย batch files | Cleanup batch files หลัง upload สำเร็จ (optional) |

## Implementation Notes

### File Structure

```
salesforce/data/
├── Product2_batch_001.csv
├── Product2_batch_002.csv
├── Product2_batch_003.csv
└── ...

salesforce/logs/
├── Product2_batch_001_success.csv
├── Product2_batch_001_error.csv
├── Product2_batch_002_success.csv
├── ...
├── Product2_success.csv       # Aggregated
└── Product2_error.csv         # Aggregated
```

### XCom Data Structure

```python
{
    "total_records": 25000,
    "batch_count": 3,
    "batch_size": 10000,
    "batch_files": [
        "/opt/airflow/salesforce/data/Product2_batch_001.csv",
        "/opt/airflow/salesforce/data/Product2_batch_002.csv",
        "/opt/airflow/salesforce/data/Product2_batch_003.csv"
    ]
}
```
