## Context

The project currently migrates data from Oracle to Salesforce using a Data Loader CLI subprocess (Java). The existing `SalesforceBulkLoader` plugin (`plugins/salesforce_bulk_loader.py`) already wraps the Bulk API 2.0 lifecycle (create job → upload CSV → close → poll → results) but has no DAG wiring it together. The Postman collections document the complete AOT Proxy flow including OAuth authentication, `TMS_Daily_Sales_File__c` status tracking, and dual upload paths (Bulk API for large datasets, Composite REST for small ones).

### Current State

- `migrate_product_price_dag.py` — Oracle extract → CSV batch split → Data Loader CLI upload → audit → reconciliation
- `plugins/salesforce_bulk_loader.py` — `SalesforceBulkLoader` class (create_job, upload_data, close_job, wait_for_job, load_file, load_files_parallel)
- `plugins/oracle_extractor.py`, `plugins/oracle_service.py` — Oracle extraction utilities
- `dags/config/tables_config.py` — `TableConfig` definitions for all 16 source tables

### Constraints

- Salesforce API version: **v66.0** (per Postman collections; existing loader defaults to v59.0 — new DAG must use v66.0)
- OAuth: Client Credentials flow (no user interaction)
- Salesforce Bulk API 2.0 limits: 150MB per CSV upload, 15 concurrent bulk jobs
- Airflow 3.x with TaskFlow API preferred

## Goals / Non-Goals

**Goals:**

- Create a DAG that uses `SalesforceBulkLoader` directly instead of Data Loader CLI
- Implement OAuth 2.0 Client Credentials authentication as a reusable plugin
- Track file upload status via `TMS_Daily_Sales_File__c` upsert/update (per Postman flow)
- Collect and persist successful/failed/unprocessed results as CSV logs
- Support batch splitting and resume (consistent with existing `start_batch` pattern)
- Support parallel bulk job execution for multi-batch uploads

**Non-Goals:**

- Replacing the existing `migrate_product_price_dag.py` (it continues to work with Data Loader CLI)
- Implementing Composite REST API path in the first iteration (Bulk API only)
- Adding Great Expectations validation steps (can be added later, existing pattern available)
- Modifying the existing `SalesforceBulkLoader` class

## Decisions

### Decision 1: Reuse `SalesforceBulkLoader` as-is, configure v66.0 at instantiation

The existing `SalesforceBulkLoader` accepts `api_version` as a constructor parameter. The new DAG will pass `api_version="v66.0"` without modifying the plugin.

**Alternative considered:** Fork the loader to hardcode v66.0 — rejected because the class is already parameterized.

### Decision 2: Separate auth into `plugins/salesforce_auth.py`

Authentication is a cross-cutting concern. A standalone module with a `get_salesforce_token(conn_id)` function keeps it reusable across DAGs. It reads `client_id`, `client_secret`, and `host` from an Airflow Connection (`salesforce_api`).

**Alternative considered:** Inline auth in the DAG — rejected because multiple DAGs will need it.

### Decision 3: Status tracking via `plugins/salesforce_status_tracker.py`

A `SalesforceStatusTracker` class wraps the PATCH upsert to `TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{ref}`. It uses the same `access_token`/`instance_url` from auth and exposes:
- `upsert_status(external_ref, status, **fields)` — create or update
- `update_status(external_ref, status)` — update only (`?updateOnly=true`)

**Alternative considered:** Use simple `requests` calls inline — rejected for reusability and testability.

### Decision 4: DAG structure follows existing pattern with Bulk API swap

```
authenticate → extract_from_oracle → upload_via_bulk_api → collect_results → update_status
```

The DAG uses `@task` decorators (TaskFlow API) and passes data via XCom. The upload step calls `SalesforceBulkLoader.load_files_parallel()` for multi-batch uploads.

### Decision 5: Store results as CSV in `salesforce/logs/`

After job completion, the DAG fetches `successfulResults`, `failedResults`, and `unprocessedrecords` from the Bulk API and writes them to `salesforce/logs/{object}_{jobId}_{type}.csv`. This is consistent with the existing log structure.

**Alternative considered:** Store only counts in XCom — rejected because CSV logs are needed for reconciliation and debugging.

### Decision 6: Bulk API only in first iteration

The Postman collection shows a Composite REST path for ≤ 200 records, but the migration tables have thousands to millions of records. Composite REST can be added later as an optimization for small reference tables.

## Risks / Trade-offs

- **Risk: OAuth token expiry during long uploads** → Mitigation: Token is fetched at DAG start; Bulk API jobs are async so the token is only needed for API calls, not during server-side processing. For very long runs (>1hr), add token refresh logic later.

- **Risk: Bulk API job timeout** → Mitigation: `SalesforceBulkLoader` already has configurable `job_timeout` (default 7200s). The DAG can override this per table.

- **Risk: CSV file exceeds 150MB Bulk API limit** → Mitigation: Existing batch splitting (`batch_size` config) keeps files small. Default 40,000 rows per batch is well under the limit.

- **Trade-off: No Composite REST path yet** → Acceptable because all migration tables have >200 records. Can be added in a follow-up change.

- **Trade-off: No GX validation in this DAG** → The existing DAG has GX validation steps that can be composed into this DAG later. Keeping the first iteration focused on the Bulk API flow.
