# Bulk API Workflows

การใช้งาน workflows สำหรับ Bulk API Data Migration

## Quick Start

```bash
# 1. ดู entities ที่มี
/gen-bulk-dag-list

# 2. สร้าง mapping config
/add-mapping 01_Account

# 3. สร้าง entity config
/add-entity-config 01_Account

# 4. Generate DAG
/gen-bulk-dag 01_Account

# 5. Test DAG
/test-dag migrate_account

# 6. Run DAG
/run-dag migrate_account
```

---

## Workflow Reference

### Documentation Workflows

| Workflow | Purpose |
|----------|---------|
| `/gen-architecture` | สร้าง architecture doc |
| `/gen-validation-rules` | สร้าง coding/validation rules |
| `/design-pipeline` | ออกแบบ pipeline แต่ละ entity |

### Config Workflows

| Workflow | Purpose | Output |
|----------|---------|--------|
| `/add-service` | สร้าง/แก้ไข service | `plugins/*.py` |
| `/add-mapping` | สร้าง mapping config | `configs/mappings/*.yaml` |
| `/add-entity-config` | สร้าง entity config | `configs/entities/*.yaml` |
| `/add-gx-suite` | สร้าง GX suite | `gx/expectations/*.json` |

### DAG Workflows

| Workflow | Purpose |
|----------|---------|
| `/gen-bulk-dag` | Generate DAG |
| `/gen-bulk-dag-list` | List entities |
| `/test-dag` | Validate DAG |
| `/run-dag` | Trigger on Airflow |

### Validation Workflows

| Workflow | Purpose |
|----------|---------|
| `/run-gx-validation` | Run GX validation |
| `/reconcile` | Compare Oracle vs SF counts |

---

## Config Files Structure

```
configs/
├── entities/         # Entity runtime config
│   └── 01_account.yaml
└── mappings/         # Column mapping
    └── 01_account.yaml

great_expectations/
└── expectations/     # GX suites
    └── source_01_account.json
```

---

## End-to-End Flow

```
/gen-architecture → /gen-validation-rules → /design-pipeline
        ↓
/add-service → /add-entity-config
        ↓
/add-mapping (optional) → /add-gx-suite (optional)
        ↓
/gen-bulk-dag → /test-dag → /run-dag → /reconcile → ✅
```

---

## Mapping Source

ข้อมูล mapping อ่านจาก:

```
center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md
```

| Column | Meaning |
|--------|---------|
| **SFDC Table** | Salesforce Object (Target) |
| **SFDC API Name** | Salesforce Field (Target) |
| **KP Table** | Oracle Table (Source) |
| **KP Field Name** | Oracle Column (Source) |
