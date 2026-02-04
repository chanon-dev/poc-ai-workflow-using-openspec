---
description: Test DAG syntax and validate imports
---

# /test-dag

Validate DAG file syntax and imports.

## Usage

```bash
/test-dag <dag_id>
```

## Steps

1. Find DAG file in `dags/`
2. Run Python syntax check
3. Validate imports
4. Run Airflow DAG validation
5. Display results

## Example

```bash
/test-dag migrate_account

# Output:
# ✅ Syntax: OK
# ✅ Imports: OK
# ✅ DAG Parse: OK
# ✅ Tasks: 4 tasks found
```
