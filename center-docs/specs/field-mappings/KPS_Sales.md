# Field Mapping: KPS_T_SALES_MD -> KPS_Sales__c

## Overview

| Property | Value |
|----------|-------|
| Source Table | `KPS_T_SALES_MD` |
| Target Object | `KPS_Sales__c` |
| External ID Field | `External_ID__c` |
| Estimated Records | ~261,000,000 (3 years) |
| Size Category | Critical |
| Priority | 1 |
| Dependencies | None |

---

## Field Mappings

| # | Oracle Column | SF Field API Name | Type (Oracle) | Type (SF) | Transformation | Req | Notes |
|---|---------------|-------------------|---------------|-----------|----------------|-----|-------|
| 1 | `SALES_ID` | `External_ID__c` | NUMBER(18) | Text(18) | `TO_CHAR()` | Yes | PK |
| 2 | `TENANT_CODE` | `Tenant_Code__c` | VARCHAR2(10) | Text(10) | Direct | Yes | |
| 3 | `STORE_CODE` | `Store_Code__c` | VARCHAR2(20) | Text(20) | Direct | Yes | |
| 4 | `SALES_DATE` | `Sales_Date__c` | DATE | Date | `YYYY-MM-DD` | Yes | |
| 5 | `SALES_AMOUNT` | `Sales_Amount__c` | NUMBER(15,2) | Currency | Direct | Yes | |
| 6 | `TAX_AMOUNT` | `Tax_Amount__c` | NUMBER(15,2) | Currency | `NVL(,0)` | No | |
| 7 | `DISCOUNT_AMOUNT` | `Discount_Amount__c` | NUMBER(15,2) | Currency | `NVL(,0)` | No | |
| 8 | `NET_AMOUNT` | `Net_Amount__c` | NUMBER(15,2) | Currency | Direct | Yes | |
| 9 | `PAYMENT_TYPE` | `Payment_Type__c` | VARCHAR2(20) | Picklist | See below | No | |
| 10 | `STATUS` | `Status__c` | VARCHAR2(1) | Picklist | See below | Yes | |
| 11 | `CREATED_DATE` | `Oracle_Created_Date__c` | DATE | DateTime | ISO 8601 | Yes | |

---

## Picklist Mappings

### PAYMENT_TYPE

| Oracle | Salesforce | Description |
|--------|------------|-------------|
| `CASH` | `Cash` | Cash payment |
| `CREDIT` | `Credit Card` | Credit card |
| `DEBIT` | `Debit Card` | Debit card |
| `QR` | `QR Payment` | QR code |
| `NULL` | `Unknown` | Default |

### STATUS

| Oracle | Salesforce | Description |
|--------|------------|-------------|
| `A` | `Active` | Active |
| `V` | `Void` | Voided |
| `C` | `Cancelled` | Cancelled |
| `NULL` | `Active` | Default |

---

## Change History

| Date | Change | Author | Status |
|------|--------|--------|--------|
| 2025-01-19 | Initial spec | System | PENDING |
