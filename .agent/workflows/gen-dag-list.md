---
description: List all available entities for DAG generation with status
---

List all entities from mapping document that can be used to generate migration DAGs.

## Usage

```
/gen-dag-list
```

## Steps

1. **Read mapping document**
   - Open `center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md`
   - Parse the Summary Mapping table

2. **Extract entity list**
   - Get entity number, name, sheet name, and status
   - Check which entities have SQL queries defined

3. **Display formatted list**

Show table with columns:

| # | Entity | Sheet Name | Tables | Status | Ready |
|---|--------|------------|--------|--------|-------|

Status Legend:

- ✅ **KP Complete** = Ready to generate
- ⏳ **Pending KP** = Missing some info, may need review
- ❓ **Finalize with User** = Needs confirmation

1. **Show usage hint**

```
To generate a DAG, run: /gen-dag <sheet_name>
Example: /gen-dag 01_Account
```

## Available Entities (Quick Reference)

| # | Entity | Sheet Name | Status |
|---|--------|------------|--------|
| 1 | Account | 01_Account | ✅ KP Complete |
| 2 | Concession | 02_Concession | ✅ KP Complete |
| 4 | Shop Brand | 04_Shop Brand | ✅ KP Complete |
| 5 | Shop Branch | 05_Shop Branch | ⏳ Pending KP |
| 6 | Contract | 06_Contract | ⏳ Pending KP |
| 7 | Sub-Contract | 07_Sub Contract | ⏳ Pending KP |
| 8 | Contact Point | 08_Contact | ✅ KP Complete |
| 10 | Reference Product | 10_Reference Products | ❓ Finalize |
| 12 | Product & Price | 12_Product & Price | ✅ KP Complete |
| 13 | Shop Inspection | 13_Shop Inspection | ⏳ Pending KP |
| 14 | Form Template | 14_Form Template(New) | ✅ KP Complete |
| 17 | Unit (Space) | 17_Units | ✅ KP Complete |
| 19 | POS | 19_POS | ✅ KP Complete |
| 20 | Sales Transaction | 20_Sales Transaction | ⏳ Pending KP |
| 21 | Supplier | 21_Supplier Contact | ✅ KP Complete |
| 22 | Invoice | 22_Invoice | ⏳ Pending KP |
| 23 | Promotion | 23_Promotion | ✅ KP Complete |
