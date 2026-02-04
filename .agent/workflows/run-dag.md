---
description: Trigger DAG run on Airflow
---

# /run-dag

Trigger DAG on Airflow with optional config.

## Usage

```bash
/run-dag <dag_id> [--conf <json>]
```

## Steps

1. Validate DAG exists
2. Build trigger command
3. Execute via Airflow CLI
4. Display run info

## Examples

```bash
# Basic run
/run-dag migrate_account

# With config override
/run-dag migrate_account --conf '{"batch_size": 1000}'

# Limited records for testing
/run-dag migrate_account --conf '{"extract_query": "SELECT * FROM KPS_R_SHOP WHERE ROWNUM <= 10"}'
```

## Command Generated

```bash
airflow dags trigger migrate_account --conf '{...}'
```
