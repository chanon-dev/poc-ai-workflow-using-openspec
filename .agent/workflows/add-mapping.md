---
description: Add or update mapping config for an entity
---

# /add-mapping

Create or update mapping configuration from datadic.md spec.

## Usage

```bash
/add-mapping <entity>
```

## Source

Reads from: `center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md`

- **SFDC Table / SFDC API Name** = Salesforce (Target)
- **KP Table / KP Field Name** = Oracle (Source)

## Steps

1. Find entity section in datadic.md (e.g., `01_Account`)
2. Parse mapping table:
   - KP Field Name → SFDC API Name
3. Identify transformations needed (datetime, decimal, etc.)
4. Generate `configs/mappings/<entity>.yaml`

## Output Format

```yaml
# configs/mappings/01_account.yaml
entity: 01_Account

source:
  tables:
    - KPS_R_SHOP
    - KPS_R_SHOP_COMMITTEE
  primary_key: [CON_CODE, SHOP_CODE]

target:
  object: Account
  operation: upsert
  external_id_field: TMS_Company_Code__c

mapping:
  CON_CODE: TMS_Concession__c
  SHOP_CODE: TMS_Company_Code__c
  REGISTERED_NAME: TMS_Company_Name__c
  # ... more fields

transformations:
  datetime:
    - REG_DATE
    - CREATEDDATE
  decimal:
    - REG_CAP_AMT
```

## Example

```bash
/add-mapping 01_Account
```
