# Business Rule: Date Handling

## Overview

กฎการจัดการ Date/DateTime fields ในการ migration จาก Oracle ไป Salesforce

---

## Date Format Rules

### 1. Date Fields (Date Only)

| Oracle Format | Salesforce Format | Example |
|---------------|-------------------|---------|
| `DATE` | `YYYY-MM-DD` | `2024-01-15` |

**SQL Transformation:**
```sql
TO_CHAR(DATE_FIELD, 'YYYY-MM-DD')
```

### 2. DateTime Fields

| Oracle Format | Salesforce Format | Example |
|---------------|-------------------|---------|
| `DATE` (with time) | ISO 8601 UTC | `2024-01-15T14:30:00.000Z` |
| `TIMESTAMP` | ISO 8601 UTC | `2024-01-15T14:30:00.000Z` |

**SQL Transformation:**
```sql
TO_CHAR(DATETIME_FIELD, 'YYYY-MM-DD"T"HH24:MI:SS".000Z"')
```

---

## Timezone Rules

### Source (Oracle)
- Oracle stores dates in **Thailand timezone (GMT+7)**
- No timezone info stored in DATE fields

### Target (Salesforce)
- Salesforce expects **UTC (GMT+0)**
- Must convert TH time to UTC

### Conversion Formula
```sql
-- Convert Thailand time (GMT+7) to UTC (GMT+0)
TO_CHAR(
    DATE_FIELD - INTERVAL '7' HOUR,
    'YYYY-MM-DD"T"HH24:MI:SS".000Z"'
) AS Datetime_UTC__c
```

---

## Migration Date Range

| Parameter | Value |
|-----------|-------|
| Start Date | `2022-01-01` |
| End Date | `2024-12-31` |
| Total Range | 3 years |

**Filter Clause:**
```sql
WHERE SALES_DATE BETWEEN TO_DATE('2022-01-01', 'YYYY-MM-DD')
                     AND TO_DATE('2024-12-31', 'YYYY-MM-DD')
```

---

## NULL Handling

| Scenario | Rule |
|----------|------|
| NULL Date | Keep as NULL (don't migrate blank dates) |
| Invalid Date | Log error, skip record |
| Future Date (> today) | Flag for review |

---

## Validation Rules

1. **Date Range Check**: All dates must be within migration range
2. **Logical Order**: `CREATED_DATE` <= `UPDATED_DATE`
3. **Business Logic**: `PAYMENT_DATE` >= `SALES_DATE`

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-01-19 | Initial spec | System |
