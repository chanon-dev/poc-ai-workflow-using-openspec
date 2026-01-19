# Changelog - Center Docs

บันทึกการเปลี่ยนแปลงทั้งหมดของ Migration Specifications

Format: `[YYYY-MM-DD] <description> [STATUS]`
Status: `PENDING` | `IN_PROGRESS` | `IMPLEMENTED` | `DEPLOYED`

---

## [Unreleased]

### Pending Changes
<!-- เพิ่ม change requests ที่รอ implement ที่นี่ -->

---

## [2025-01-19] - Initial Setup

### Added
- Initial field mapping specs for critical tables
  - `KPS_Sales.md` - KPS_T_SALES_MD mapping [PENDING]
  - `KPS_SalesPay.md` - KPS_T_SALESPAY_MD mapping [PENDING]
  - `KPS_SalesM.md` - KPS_T_SALES_M mapping [PENDING]
- Business rules specifications
  - `date-handling.md` - Date format and timezone rules
  - `null-handling.md` - NULL value handling rules
  - `validation-rules.md` - Data validation rules
- Constraints specifications
  - `salesforce-limits.md` - Salesforce API limits
  - `oracle-settings.md` - Oracle extraction settings

### Changed
<!-- ระบุสิ่งที่แก้ไข -->

### Removed
<!-- ระบุสิ่งที่ลบออก -->

---

## Template for New Entries

```markdown
## [YYYY-MM-DD] - Brief Description

### Added
- Description [STATUS]
- See: `changes/YYYY-MM-DD-change-name.md`

### Changed
- Description [STATUS]

### Removed
- Description [STATUS]
```
