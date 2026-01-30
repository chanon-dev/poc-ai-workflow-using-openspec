## Why

ปัจจุบัน DAG `migrate_product_price` สร้างไฟล์ CSV เดียว (`Product2.csv`) สำหรับ upload ไป Salesforce ทำให้เกิดปัญหาเมื่อมีข้อมูลจำนวนมาก:
- Salesforce Data Loader timeout เมื่อ upload ไฟล์ขนาดใหญ่
- ไม่สามารถ retry เฉพาะ batch ที่ fail ได้
- Memory issue เมื่อ load ไฟล์ใหญ่มากเข้า pandas

## What Changes

- **เพิ่ม batch splitting**: แบ่งไฟล์ CSV เป็นหลาย batch ตาม row count ที่กำหนด
- **Configurable batch size**: สามารถกำหนด batch size ผ่าน Airflow Variable หรือ DAG config
- **Sequential upload**: Upload ทีละ batch ตามลำดับ
- **Per-batch validation**: GX validate แต่ละ batch แยกกัน
- **Aggregated reconciliation**: รวมผลลัพธ์ทุก batch สำหรับ final reconciliation

## Capabilities

### New Capabilities

- `batch-extraction`: แบ่ง DataFrame เป็น chunks และเขียนเป็นหลายไฟล์ CSV
- `batch-upload`: Upload หลายไฟล์ไปยัง Salesforce ทีละไฟล์
- `batch-validation`: Validate และรวมผลลัพธ์จากหลาย batch files

### Modified Capabilities

<!-- No existing specs being modified -->

## Impact

- `dags/migrate_product_price_dag.py`: เปลี่ยน extract_data และ run_dataloader logic
- `config/`: อาจต้องเพิ่ม process-conf สำหรับแต่ละ batch หรือ template
- `great_expectations/expectations/`: อาจต้องปรับ suite สำหรับ per-batch validation

## Configuration

```python
# Default values (overridable via Airflow Variable)
BATCH_SIZE = 10000  # records per file
BATCH_PREFIX = "Product2_batch"
# Output: Product2_batch_001.csv, Product2_batch_002.csv, ...
```
