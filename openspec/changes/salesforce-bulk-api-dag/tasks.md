## 1. OAuth Authentication Plugin

- [x] 1.1 Create `plugins/salesforce_auth.py` with `get_salesforce_token(conn_id)` function
- [x] 1.2 Read `client_id` (login), `client_secret` (password), `host` from Airflow Connection
- [x] 1.3 POST to `{host}/services/oauth2/token` with `grant_type=client_credentials`
- [x] 1.4 Return dict with `access_token`, `instance_url`, `token_type`
- [x] 1.5 Raise descriptive errors for 400/401 responses and missing connection fields

## 2. Status Tracker Plugin

- [x] 2.1 Create `plugins/salesforce_status_tracker.py` with `SalesforceStatusTracker` class
- [x] 2.2 Implement `upsert_status(external_ref, status, **fields)` — PATCH to External ID endpoint (no `updateOnly`)
- [x] 2.3 Implement `update_status(external_ref, status)` — PATCH with `?updateOnly=true`
- [x] 2.4 Handle HTTP 404 (record not found in updateOnly mode) with descriptive error

## 3. Bulk API DAG

- [x] 3.1 Create `dags/migrate_bulk_api_dag.py` with DAG definition and TaskFlow `@task` decorators
- [x] 3.2 Implement `authenticate` task — call `get_salesforce_token("salesforce_api")`, return credentials
- [x] 3.3 Implement `extract_from_oracle` task — reuse Oracle extraction pattern from `migrate_product_price_dag.py`, split into batch CSV files
- [x] 3.4 Implement `upload_batches` task — instantiate `SalesforceBulkLoader(api_version="v66.0")`, call `load_files_parallel()` for batch files
- [x] 3.5 Implement `collect_results` task — fetch successfulResults/failedResults/unprocessedrecords CSVs and save to `salesforce/logs/`
- [x] 3.6 Implement `update_file_status` task — call `SalesforceStatusTracker.update_status()` with "Uploaded" or "In Progress" based on results
- [x] 3.7 Support `start_batch` and `batch_size` config (DAG run config > Airflow Variable > default)
- [x] 3.8 Support `sf_object` and `external_id_field` override via DAG run config, fallback to `tables_config.py`
- [x] 3.9 Wire task dependencies: `authenticate >> extract >> upload >> collect_results >> update_status`
- [x] 3.10 Handle zero-record extraction (skip upload, log warning)

## 4. Verify

- [x] 4.1 Run `python dags/migrate_bulk_api_dag.py` to verify DAG syntax and imports
- [x] 4.2 Verify all 3 new files exist and have correct module structure
