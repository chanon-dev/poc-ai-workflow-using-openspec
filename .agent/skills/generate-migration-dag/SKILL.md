---
name: generate-migration-dag
description: Generate Airflow DAG for data migration entity. Use when user wants to create a new migration DAG based on mapping document.
license: MIT
metadata:
  author: chanon
  version: "1.0"
---

Generate an Airflow DAG for migrating data from Oracle to Salesforce.

**Input**: Entity name (e.g., `01_Account`, `17_Units`, `12_Product & Price`)

**Reference Files**:

- **Template DAG**: `dags/migrate_product_price_dag.py`
- **Mapping Doc**: `center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md`

**Steps**

1. **Parse Entity Name**

   Extract the entity identifier from input:
   - `01_Account` → sheet `01_Account`, output `account`
   - `17_Units` → sheet `17_Units`, output `units`
   - `12_Product & Price` → sheet `12_Product & Price`, output `product_price`

2. **Read Mapping Document**

   Open `center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md` and find the section for the entity (look for `## <sheet_name>`).

   Extract:
   - **KP Tables**: Source Oracle tables (e.g., `KPS_R_SHOP`, `KPS_R_CONCESS`)
   - **KP Field Names**: Column names and types
   - **SQL Query**: If provided in the Summary Mapping section
   - **SFDC Object**: Target Salesforce object (e.g., `Account`, `Product2`)

3. **Read Template DAG**

   Read `dags/migrate_product_price_dag.py` to understand the structure:
   - Constants section (DAG_ID, PROCESS_NAME, OUTPUT_FILE, etc.)
   - EXTRACT_QUERY SQL
   - Transformation functions (format_datetime, format_decimal)
   - Pipeline tasks (validate_source → extract_data → validate_extract → run_dataloader → audit_results → validate_postmig)

4. **Generate New DAG**

   Create new DAG file at `dags/migrate_<entity>_dag.py` with:

   **a. Header/Docstring:**

   ```python
   """
   Execution DAG: Migrate <Entity Name> Data
   
   Pipeline Steps:
   1. validate_source - GX validation on Oracle source
   2. extract_data - Query Oracle → CSV
   3. validate_extract - GX validation on extracted CSV
   4. run_dataloader - Call Data Loader
   5. audit_results - Check error/success logs
   6. validate_postmig - GX reconciliation check
   
   Source Tables: <list from mapping>
   Target: Salesforce <SFDC Object>
   """
   ```

   **b. Constants:**

   ```python
   DAG_ID = "migrate_<entity>"
   PROCESS_NAME = "<SFDCObject>_Process"
   OUTPUT_FILE = os.path.join(DATA_DIR, "<SFDCObject>.csv")
   BATCH_PREFIX = "<SFDCObject>_batch"
   ```

   **c. EXTRACT_QUERY:**
   - Use the SQL from mapping document if available
   - Otherwise construct SELECT statement from KP Field Names
   - Include proper JOINs based on table relationships

   **d. Transformations:**
   - Identify DATE columns → use `format_datetime()`
   - Identify NUMBER(x,y) columns → use `format_decimal()`

   **e. GX Suite Names:**

   ```python
   suite_name="source_<entity>"
   suite_name="extract_<entity>"
   suite_name="postmig_<entity>"
   ```

5. **Validate Generated DAG**

   After creating the file:
   - Check Python syntax is valid
   - Verify all imports are present
   - Confirm SQL query is syntactically correct

**Output Format**

```
## DAG Generated: migrate_<entity>_dag.py

**File**: `dags/migrate_<entity>_dag.py`

**Source Tables**: 
- KPS_R_<table1>
- KPS_R_<table2>

**Target**: Salesforce <Object>

**Columns Mapped**: <count> columns

**SQL Query Preview**:
```sql
SELECT ...
FROM ...
```

Ready to use! Run with: `airflow dags trigger migrate_<entity>`

```

**Guardrails**
- ALWAYS read the template DAG first to ensure consistency
- ALWAYS read the mapping document for the specific entity
- If SQL query is missing in mapping, construct it from column definitions
- If entity not found in mapping document, inform user and list available entities
- Keep transformations consistent with template (datetime format, decimal precision)
- Use the same pipeline structure for all entities
