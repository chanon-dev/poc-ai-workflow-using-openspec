# Salesforce CLI Commands

คู่มือคำสั่ง Salesforce CLI สำหรับตรวจสอบ Schema, Fields และข้อมูลต่างๆ

## สารบัญ

- [1. Installation](#1-installation)
- [2. Login & Authentication](#2-login--authentication)
- [3. ตรวจสอบ Object Schema](#3-ตรวจสอบ-object-schema)
- [4. External ID Fields](#4-external-id-fields)
- [5. Lookup & Reference Fields](#5-lookup--reference-fields)
- [6. Required Fields](#6-required-fields)
- [7. Picklist Values](#7-picklist-values)
- [8. Field Data Types](#8-field-data-types)
- [9. Record Counts & Limits](#9-record-counts--limits)
- [10. Data Validation](#10-data-validation)
- [11. Bulk API & Jobs](#11-bulk-api--jobs)
- [12. Troubleshooting](#12-troubleshooting)

---

## 1. Installation

### macOS

```bash
# Homebrew (แนะนำ)
brew install sf

# หรือ npm
npm install -g @salesforce/cli
```

### Windows

```powershell
# npm
npm install -g @salesforce/cli

# หรือ download installer จาก
# https://developer.salesforce.com/tools/salesforcecli
```

### Linux

```bash
# npm
npm install -g @salesforce/cli

# หรือ download tarball
curl -fsSL https://developer.salesforce.com/media/salesforce-cli/sf/channels/stable/sf-linux-x64.tar.xz | tar xJ
```

### ตรวจสอบ version

```bash
sf --version
```

---

## 2. Login & Authentication

### Login ผ่าน Browser (แนะนำ)

```bash
# Production org
sf org login web --alias prod

# Sandbox org
sf org login web --instance-url https://test.salesforce.com --alias sandbox

# Developer org
sf org login web --instance-url https://login.salesforce.com --alias devorg
```

### Login ด้วย JWT (สำหรับ CI/CD)

```bash
sf org login jwt \
  --username user@example.com \
  --jwt-key-file /path/to/server.key \
  --client-id <connected-app-consumer-key> \
  --instance-url https://test.salesforce.com \
  --alias myorg
```

### ตรวจสอบ Org ที่ Login

```bash
# List orgs ทั้งหมด
sf org list

# ดูรายละเอียด org
sf org display --target-org myorg

# ดู org ที่เป็น default
sf config get target-org

# Set default org
sf config set target-org=myorg
```

### Logout

```bash
# Logout จาก org
sf org logout --target-org myorg

# Logout ทุก org
sf org logout --all
```

---

## 3. ตรวจสอบ Object Schema

### List Objects ทั้งหมด

```bash
# List ทุก objects
sf sobject list --target-org myorg

# List เฉพาะ custom objects
sf sobject list --target-org myorg --sobject custom

# Search หา object
sf sobject list --target-org myorg | grep -i "product"
```

### Describe Object (ดู Schema ทั้งหมด)

```bash
# Describe object (output เป็น table)
sf sobject describe --sobject Product2 --target-org myorg

# Export เป็น JSON
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null > schema/Product2.json
```

### ดู Field Names ทั้งหมด

```bash
# List field names
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[].name'

# Filter เฉพาะ custom fields (ลงท้าย __c)
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[] | select(.name | endswith("__c")) | .name'

# Filter ด้วย keyword
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[].name' | grep -i "tms"
```

### ดู Field Details

```bash
# Field name + type
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | {name, type}'

# Field name + type + length + label
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | {name, type, length, label}'

# Export เป็น CSV
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[] | [.name, .type, .length, .label] | @csv' > Product2_fields.csv
```

---

## 4. External ID Fields

External ID ใช้สำหรับ Upsert operations - ต้องตรวจสอบก่อน Data Loader

### ดู External ID Fields ทั้งหมด

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.externalId == true) | {name, type, unique}'
```

### ตรวจสอบว่า field เป็น External ID หรือไม่

```bash
# ตรวจสอบ field เฉพาะ
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.name == "ProductCode") | {name, externalId, unique, idLookup}'
```

### Fields ที่ใช้สำหรับ Upsert ได้

```bash
# Fields ที่เป็น External ID หรือ idLookup
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.externalId == true or .idLookup == true) | {name, externalId, idLookup}'
```

### ตรวจสอบหลาย Objects พร้อมกัน

```bash
for obj in Product2 Account Contact KPS_Sales__c; do
  echo "=== $obj ==="
  sf sobject describe --sobject $obj --target-org myorg --json 2>/dev/null | \
    jq -r '.result.fields[] | select(.externalId == true) | .name' || echo "No External ID fields"
  echo ""
done
```

---

## 5. Lookup & Reference Fields

ตรวจสอบ Lookup relationships สำหรับ mapping

### ดู Lookup Fields ทั้งหมด

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "reference") | {name, referenceTo, relationshipName}'
```

### ดู Relationship Details

```bash
# ดู child relationships
sf sobject describe --sobject Account --target-org myorg --json 2>/dev/null | \
  jq '.result.childRelationships[] | {childSObject, field, relationshipName}'
```

### Master-Detail vs Lookup

```bash
# ดู field relationships พร้อม type
sf sobject describe --sobject KPS_Sales__c --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "reference") | {
    name,
    referenceTo,
    cascadeDelete: .cascadeDelete,
    restrictedDelete: .restrictedDelete
  }'
```

---

## 6. Required Fields

ตรวจสอบ Required fields ก่อน insert/upsert

### ดู Required Fields (ไม่ nillable และไม่มี default)

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.nillable == false and .defaultedOnCreate == false) | {name, type, nillable, defaultedOnCreate}'
```

### ดู Fields ที่ต้องใส่เมื่อ Create

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.createable == true and .nillable == false and .defaultedOnCreate == false) | .name'
```

### สรุป Required Fields พร้อม Type

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[] | select(.nillable == false and .defaultedOnCreate == false and .createable == true) | "\(.name) (\(.type))"'
```

---

## 7. Picklist Values

### ดู Picklist Fields

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "picklist") | .name'
```

### ดู Picklist Values ทั้งหมด

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "picklist") | {
    name,
    values: [.picklistValues[] | {value, label, active}]
  }'
```

### ดู Active Values เท่านั้น

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.name == "Family") | {
    name,
    activeValues: [.picklistValues[] | select(.active == true) | .value]
  }'
```

### Export Picklist Values เป็น CSV

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[] | select(.type == "picklist") as $f | $f.picklistValues[] | [$f.name, .value, .label, .active] | @csv' > picklist_values.csv
```

---

## 8. Field Data Types

### สรุป Field Types ทั้งหมด

```bash
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[].type' | sort | uniq -c | sort -rn
```

### ดู Fields ตาม Type

```bash
# String fields
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "string") | {name, length}'

# Date/DateTime fields
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "date" or .type == "datetime") | {name, type}'

# Number fields
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "double" or .type == "currency" or .type == "int" or .type == "percent") | {name, type, precision, scale}'

# Boolean fields
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.type == "boolean") | .name'
```

### ตรวจสอบ Field Length

```bash
# Fields ที่มี length > 0 (text fields)
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.length > 0) | {name, type, length}' | head -50
```

---

## 9. Record Counts & Limits

### นับ Records

```bash
# Count records
sf data query --query "SELECT COUNT() FROM Product2" --target-org myorg

# Count with filter
sf data query --query "SELECT COUNT() FROM Product2 WHERE IsActive = true" --target-org myorg
```

### ดู Org Limits

```bash
# ดู limits ทั้งหมด
sf limits api display --target-org myorg

# ดู Data Storage
sf limits api display --target-org myorg | grep -i "storage"

# ดู API Requests
sf limits api display --target-org myorg | grep -i "api"
```

### ดู Record Limits

```bash
# ดู storage usage
sf data query --query "SELECT UsedStorage, DataStorageMB FROM Organization" --target-org myorg --json 2>/dev/null | jq '.result.records[0]'
```

---

## 10. Data Validation

### Query Sample Data

```bash
# Query sample records
sf data query --query "SELECT Id, Name, ProductCode FROM Product2 LIMIT 5" --target-org myorg

# Query with specific fields
sf data query --query "SELECT Id, Name, TMS_Concession__c, TMS_Start_Date__c FROM Product2 WHERE TMS_Concession__c != null LIMIT 5" --target-org myorg

# Export to CSV
sf data query --query "SELECT Id, Name, ProductCode FROM Product2 LIMIT 100" --target-org myorg --result-format csv > sample_data.csv
```

### ตรวจสอบ Duplicates

```bash
# หา duplicate ProductCode
sf data query --query "SELECT ProductCode, COUNT(Id) cnt FROM Product2 GROUP BY ProductCode HAVING COUNT(Id) > 1" --target-org myorg
```

### ตรวจสอบ Null Values

```bash
# Records ที่ field เป็น null
sf data query --query "SELECT COUNT() FROM Product2 WHERE ProductCode = null" --target-org myorg
```

---

## 11. Bulk API & Jobs

### ดู Bulk Jobs

```bash
# List recent bulk jobs
sf data bulk list --target-org myorg

# ดู job status
sf data bulk status --job-id <job-id> --target-org myorg
```

### Resume Failed Jobs

```bash
# Resume bulk job
sf data bulk resume --job-id <job-id> --target-org myorg
```

---

## 12. Troubleshooting

### Error: No org configuration found

```bash
# ตรวจสอบ org list
sf org list

# Login ใหม่
sf org login web --alias myorg
```

### Error: Object not found

```bash
# List ทุก objects
sf sobject list --target-org myorg

# Search object
sf sobject list --target-org myorg | grep -i "keyword"
```

### jq not installed

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Windows (chocolatey)
choco install jq
```

### Permission Errors

```bash
# ตรวจสอบ user permissions
sf data query --query "SELECT Id, Name, Profile.Name FROM User WHERE Username = 'your-user@example.com'" --target-org myorg

# ตรวจสอบ field-level security
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq '.result.fields[] | select(.name == "TMS_Concession__c") | {name, createable, updateable}'
```

### Debug API Calls

```bash
# Enable debug logging
SF_LOG_LEVEL=debug sf sobject describe --sobject Product2 --target-org myorg
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Login | `sf org login web --alias myorg` |
| List objects | `sf sobject list --target-org myorg` |
| Describe object | `sf sobject describe --sobject Product2 --target-org myorg --json` |
| External ID fields | `jq '.result.fields[] \| select(.externalId == true)'` |
| Required fields | `jq '.result.fields[] \| select(.nillable == false)'` |
| Lookup fields | `jq '.result.fields[] \| select(.type == "reference")'` |
| Picklist values | `jq '.result.fields[] \| select(.type == "picklist")'` |
| Count records | `sf data query --query "SELECT COUNT() FROM Object"` |
| Query data | `sf data query --query "SELECT Id, Name FROM Object LIMIT 10"` |
| Org limits | `sf limits api display --target-org myorg` |

---

## สร้าง Mapping Template

สร้าง SDL mapping file จาก Salesforce schema:

```bash
# สร้าง mapping template
sf sobject describe --sobject Product2 --target-org myorg --json 2>/dev/null | \
  jq -r '.result.fields[] | select(.createable == true) | "\(.name)=ORACLE_COLUMN  # \(.type) - \(.label)"' > Product2_mapping_template.sdl
```

---

## Batch Describe Script

Script สำหรับ describe หลาย objects:

```bash
#!/bin/bash
ORG="myorg"
OBJECTS="Product2 Account Contact KPS_Sales__c KPS_SalesPay__c"
OUTPUT_DIR="./schema"

mkdir -p $OUTPUT_DIR

for obj in $OBJECTS; do
  echo "Describing $obj..."
  sf sobject describe --sobject $obj --target-org $ORG --json 2>/dev/null > "$OUTPUT_DIR/${obj}.json"

  # Create field summary
  jq -r '.result.fields[] | [.name, .type, .length, .externalId, .nillable] | @csv' \
    "$OUTPUT_DIR/${obj}.json" > "$OUTPUT_DIR/${obj}_fields.csv"
done

echo "Done! Check $OUTPUT_DIR"
```
