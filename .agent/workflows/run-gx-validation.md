---
description: Run GX validation on entity data
---

# /run-gx-validation

Run Great Expectations validation on source or extracted data.

## Usage

```bash
/run-gx-validation <entity> [--type source|extract]
```

## Steps

1. Load GX suite from `great_expectations/expectations/<type>_<entity>.json`
2. Run validation on data
3. Generate data docs
4. Display results

## Example

```bash
/run-gx-validation 01_Account --type source
```
