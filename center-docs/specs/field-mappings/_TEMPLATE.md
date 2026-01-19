# Field Mapping: [SOURCE_TABLE] -> [TARGET_OBJECT]

## Overview

| Property | Value |
|----------|-------|
| Source Table | `KPS_T_XXX` |
| Target Object | `KPS_XXX__c` |
| External ID Field | `External_ID__c` |
| Estimated Records | ~X,XXX,XXX |
| Size Category | Critical / Medium / Small / Reference |
| Priority | X |
| Dependencies | None / [List parent tables] |

---

## Field Mappings

| # | Oracle Column | SF Field API Name | Data Type (Oracle) | Data Type (SF) | Transformation | Required | Notes |
|---|---------------|-------------------|-------------------|----------------|----------------|----------|-------|
| 1 | `ID` | `External_ID__c` | NUMBER(18) | Text(18) | `TO_CHAR(ID)` | Yes | Primary Key |
| 2 | `FIELD_1` | `Field_1__c` | VARCHAR2(50) | Text(50) | Direct | No | |

---

## Picklist Mappings

### FIELD_NAME -> Field_Name__c

| Oracle Value | Salesforce Value | Description |
|-------------|------------------|-------------|
| `A` | `Active` | ... |
| `I` | `Inactive` | ... |
| `NULL` | `Unknown` | Default |

---

## Validation Rules

### Pre-Load Validation
1. Primary key must not be NULL
2. ...

### Data Quality Rules
- ...

---

## SQL Extract Template

```sql
SELECT
    TO_CHAR(ID) AS External_ID__c,
    FIELD_1 AS Field_1__c
FROM TABLE_NAME
WHERE ROWNUM BETWEEN :start_row AND :end_row
ORDER BY ID;
```

---

## Change History

| Date | Change | Author | Status |
|------|--------|--------|--------|
| YYYY-MM-DD | Initial spec | [Name] | Draft |
