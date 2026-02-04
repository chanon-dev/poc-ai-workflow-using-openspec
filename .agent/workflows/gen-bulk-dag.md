---
description: Generate migration DAG for a single entity (e.g., /gen-dag 01_Account)
---

# /gen-bulk-dag

Generate Bulk API DAG for an entity.

## Usage

```bash
/gen-bulk-dag <entity>
```

## Prerequisites

- Entity config at `configs/entities/<entity>.yaml`
- Mapping config at `configs/mappings/<entity>.yaml`

## Steps

1. Read entity config from `configs/entities/<entity>.yaml`
2. Read mapping config from `configs/mappings/<entity>.yaml`
3. Use template from `dags/migrate_bulk_api_dag.py`
4. Generate DAG with:
   - Entity-specific constants
   - SQL from entity config
   - Column mapping from mapping config
   - Optional GX validation tasks
5. Output to `dags/migrate_<entity>_dag.py`

## Generated DAG Structure

```python
from plugins.oracle_service import OracleService
from plugins.salesforce_bulk_loader import SalesforceBulkLoader
from plugins.transformers import transform_for_salesforce

@dag(dag_id="migrate_account", ...)
def migrate_account():
    # Load configs
    # Extract from Oracle
    # Transform with mapping
    # Load via Bulk API
    # Reconcile
```

## Example

```bash
/gen-bulk-dag 01_Account
```

Creates `dags/migrate_account_dag.py`
