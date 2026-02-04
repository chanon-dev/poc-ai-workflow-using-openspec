---
description: Create GX expectation suite for an entity
---

# /add-gx-suite

Create Great Expectations expectation suite for an entity.

## Usage

```bash
/add-gx-suite <entity> [--type source|extract]
```

## Steps

1. Read entity config from `configs/mappings/<entity>.yaml`
2. Analyze field types and constraints
3. Generate expectations:
   - Not null checks
   - Type validation
   - Value ranges
   - Referential integrity
4. Output to `great_expectations/expectations/<type>_<entity>.json`

## Example

```bash
/add-gx-suite 01_Account --type source
```

Creates `great_expectations/expectations/source_01_account.json`
