# Business Rule: NULL Handling

## Overview

กฎการจัดการ NULL values ในการ migration

---

## Default NULL Handling by Data Type

| Data Type | NULL Handling | Default Value |
|-----------|---------------|---------------|
| Text | Keep NULL | - |
| Number/Currency | Convert to 0 | `NVL(FIELD, 0)` |
| Date | Keep NULL | - |
| Picklist | Map to default | See per-field rules |
| Required Fields | Reject record | Log error |

---

## Field-Specific Rules

### Currency Fields
```sql
-- Always default to 0 for currency
NVL(TAX_AMOUNT, 0) AS Tax_Amount__c
NVL(DISCOUNT_AMOUNT, 0) AS Discount_Amount__c
```

### Picklist Fields

| Field | NULL Maps To |
|-------|--------------|
| `PAYMENT_TYPE` | `Unknown` |
| `STATUS` | `Active` |
| `CARD_TYPE` | `N/A` |

```sql
CASE PAYMENT_TYPE
    WHEN NULL THEN 'Unknown'
    ELSE ...
END
```

### Text Fields
```sql
-- Trim whitespace, NULL stays NULL
TRIM(TEXT_FIELD) AS Text_Field__c
```

---

## Required Field Validation

หาก required field เป็น NULL → **Reject record**

| Table | Required Fields |
|-------|-----------------|
| `KPS_T_SALES_MD` | `SALES_ID`, `TENANT_CODE`, `STORE_CODE`, `SALES_DATE` |
| `KPS_T_SALESPAY_MD` | `SALESPAY_ID`, `SALES_ID`, `PAYMENT_AMOUNT` |

---

## Error Handling

1. **Log rejected records** to error file
2. **Continue processing** other records
3. **Report summary** at end of batch

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-01-19 | Initial spec | System |
