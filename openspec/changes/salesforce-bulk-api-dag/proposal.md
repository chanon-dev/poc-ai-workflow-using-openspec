## Why

The current migration DAG (`migrate_product_price_dag.py`) uploads data to Salesforce via the **Data Loader CLI** (Java subprocess). This approach requires a separate Java runtime, config files on disk, and lacks programmatic control over the upload lifecycle. The project already has a `SalesforceBulkLoader` plugin (`plugins/salesforce_bulk_loader.py`) that wraps Salesforce Bulk API 2.0 in Python, but no DAG uses it yet. A new DAG using this plugin would enable native Python control over authentication, job management, status tracking (`TMS_Daily_Sales_File__c`), parallel uploads, and error handling — matching the flow documented in `docs/SALESFORCE_BULK_API_GUIDE.md`.

## What Changes

- Add a new Airflow DAG (`dags/migrate_bulk_api_dag.py`) that implements the end-to-end Salesforce upload flow using Bulk API 2.0
- Add a Salesforce authentication helper (`plugins/salesforce_auth.py`) for OAuth 2.0 Client Credentials flow
- Add a Salesforce status tracker (`plugins/salesforce_status_tracker.py`) for upserting `TMS_Daily_Sales_File__c` records
- Wire the existing `SalesforceBulkLoader` plugin into the DAG for CSV upload, job polling, and result retrieval
- Support both Bulk API 2.0 (> 10k records) and Composite REST API (≤ 200 records) paths
- Collect successful/failed/unprocessed results and store them as CSV logs

## Capabilities

### New Capabilities

- `sf-oauth-auth`: OAuth 2.0 Client Credentials authentication with Salesforce, returning access_token and instance_url
- `sf-status-tracking`: Upsert and update `TMS_Daily_Sales_File__c` status records via External ID, including updateOnly mode
- `bulk-api-dag`: Airflow DAG orchestrating the full pipeline — extract from Oracle, validate, upload via Bulk API 2.0, poll results, update status, reconcile

### Modified Capabilities

_(none — existing specs are not changed)_

## Impact

- **New files:**
  - `dags/migrate_bulk_api_dag.py` — new DAG
  - `plugins/salesforce_auth.py` — OAuth helper
  - `plugins/salesforce_status_tracker.py` — status tracking helper
- **Existing files (read-only dependencies):**
  - `plugins/salesforce_bulk_loader.py` — used as-is for Bulk API upload
  - `plugins/oracle_extractor.py` — used for Oracle extraction
  - `dags/config/tables_config.py` — used for table configuration
- **Airflow Connections:** requires `salesforce_api` connection (client_id, client_secret, host)
- **API:** Salesforce REST API v66.0, Bulk API 2.0
