---
description: Create entity configuration file
---

# /add-entity-config

Create entity configuration that combines mapping and runtime settings.

## Usage

```bash
/add-entity-config <entity>
```

## Steps

1. Read mapping from `center_docs/...datadic.md`
2. Generate entity config with:
   - Source table info
   - Target object info
   - SQL query
   - Batch settings
3. Output to `configs/entities/<entity>.yaml`

## Output Format

```yaml
# configs/entities/01_account.yaml
entity:
  name: 01_Account
  display_name: Account
  status: ready  # ready | pending | finalize

source:
  sql: |
    SELECT 
      CON_CODE,
      SHOP_CODE,
      ...
    FROM KPS_R_SHOP
    WHERE ROWNUM <= :limit

target:
  object: Account
  operation: upsert
  external_id_field: TMS_Company_Code__c

batch:
  size: 40000
  parallel: true

mapping_file: configs/mappings/01_account.yaml
gx_suite: source_01_account  # optional
```

## Example

```bash
/add-entity-config 01_Account
```
