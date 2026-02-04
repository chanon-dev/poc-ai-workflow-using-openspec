---
description: List all available entities for DAG generation with status
---

# /gen-bulk-dag-list

List all entities with their status for DAG generation.

## Usage

```bash
/gen-bulk-dag-list
```

## Steps

1. Read `center_docs/...datadic.md` Summary Mapping table
2. Check `configs/entities/` for existing configs
3. Check `configs/mappings/` for existing mappings
4. Check `dags/` for existing DAGs
5. Display status table

## Output

```
| Entity | Mapping | Config | DAG | Status |
|--------|---------|--------|-----|--------|
| 01_Account | ✅ | ✅ | ✅ | Ready |
| 02_Concession | ✅ | ✅ | ❌ | Need DAG |
| 05_Shop_Branch | ⏳ | ❌ | ❌ | Pending KP |
```

## Example

```bash
/gen-bulk-dag-list
```
