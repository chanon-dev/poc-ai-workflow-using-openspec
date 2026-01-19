# Center Docs - KPC TMS Data Migration

Single Source of Truth สำหรับ Data Migration Specifications

## Directory Structure

```
center-docs/
├── specs/                      # Specifications (Business Truth)
│   ├── field-mappings/         # Field mapping specs per table
│   │   ├── KPS_Sales.md        # KPS_T_SALES_MD -> KPS_Sales__c
│   │   ├── KPS_SalesPay.md     # KPS_T_SALESPAY_MD -> KPS_SalesPay__c
│   │   └── KPS_SalesM.md       # KPS_T_SALES_M -> KPS_SalesM__c
│   ├── business-rules/         # Transformation & validation rules
│   │   ├── date-handling.md    # Date format, timezone rules
│   │   ├── null-handling.md    # NULL value handling
│   │   └── validation-rules.md # Data validation rules
│   └── constraints/            # Technical constraints
│       ├── salesforce-limits.md
│       └── oracle-settings.md
├── changes/                    # Change requests (pending)
│   └── YYYY-MM-DD-<name>.md    # Change request files
├── templates/                  # Templates for new specs
│   └── change-request.md       # Change request template
├── CHANGELOG.md                # Version history
└── README.md                   # This file
```

## Workflow

### 1. Business/SA แก้ไข Spec
```bash
# แก้ไข field mapping
vim specs/field-mappings/KPS_Sales.md

# บันทึก change ใน CHANGELOG
vim CHANGELOG.md
```

### 2. AI Detect Changes
```bash
# Sync และ detect changes
../scripts/sync-center-docs.sh

# หรือ manual
claude "อ่าน center-docs/CHANGELOG.md และสรุปว่ามีอะไรเปลี่ยน"
```

### 3. AI Create Proposal
```bash
claude "/openspec:proposal จาก center-docs/changes/2025-01-15-*.md"
```

### 4. Team Review & Approve
```bash
openspec validate <change-id> --strict
```

### 5. AI Implement
```bash
claude "/openspec:apply <change-id>"
```

### 6. Archive
```bash
openspec archive <change-id> --yes
```

## Conventions

### Field Mapping Format
- ใช้ Markdown table format
- ระบุ transformation rules ชัดเจน
- ระบุ data type mapping

### Change Request Format
- ใช้ template จาก `templates/change-request.md`
- ตั้งชื่อไฟล์: `YYYY-MM-DD-<brief-description>.md`
- ระบุ Priority: Critical, High, Medium, Low

### Version Control
- ทุกการแก้ไขต้องบันทึกใน CHANGELOG.md
- ใช้ format: `[YYYY-MM-DD] <description>`
- Link ไปยัง change request file

## Contact

- **Solution Architect**: [Name]
- **Data Engineer Lead**: [Name]
- **DBA Lead**: [Name]
