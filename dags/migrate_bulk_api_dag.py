"""
Execution DAG: Migrate Data via Salesforce Bulk API 2.0

Trigger: Manual or Schedule

Pipeline Steps:
1. authenticate     - OAuth 2.0 Client Credentials → access_token
2. extract_data     - Query Oracle → CSV batch files
3. upload_batches   - Upload CSVs via Bulk API 2.0 (parallel)
4. collect_results  - Fetch success/failed/unprocessed CSVs
Uses:
- plugins/salesforce_auth.py          (OAuth authentication)
- plugins/salesforce_bulk_loader.py   (Bulk API 2.0 upload)
- plugins/migration_logger.py         (DB logging → PostgreSQL)

REQ: openspec/changes/salesforce-bulk-api-dag/specs/bulk-api-dag/spec.md
"""

import csv
import logging
import math
import os
from datetime import datetime

import oracledb

try:
    oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")
except Exception:
    pass

from airflow.decorators import dag, task

# Constants
DAG_ID = "migrate_bulk_api"
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
SALESFORCE_DIR = os.path.join(AIRFLOW_HOME, "salesforce")
DATA_DIR = os.path.join(SALESFORCE_DIR, "data")
LOG_DIR = os.path.join(SALESFORCE_DIR, "logs")

DEFAULT_BATCH_SIZE = 40000
DEFAULT_TABLE_NAME = "KPS_T_SALES_MD"

# Default extraction query (override via DAG config or per-table logic)
DEFAULT_EXTRACT_QUERY = """
SELECT *
FROM {table_name}
WHERE ROWNUM <= 10
"""


def _get_dag_config(context):
    """Get merged config from DAG run conf."""
    dag_run = context.get("dag_run")
    return dag_run.conf if dag_run and dag_run.conf else {}


@dag(
    dag_id=DAG_ID,
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2024, 1, 1),
        "email_on_failure": False,
        "retries": 0,
    },
    description="Migrate data from Oracle to Salesforce via Bulk API 2.0",
    schedule=None,
    catchup=False,
    tags=["salesforce", "migration", "bulk-api"],
)
def migrate_bulk_api():

    @task()
    def authenticate(**context):
        """Authenticate to Salesforce via OAuth 2.0 Client Credentials."""
        from salesforce_auth import get_salesforce_token

        logging.info("=" * 60)
        logging.info("Step 1: authenticate — OAuth 2.0 Client Credentials")
        logging.info("=" * 60)

        dag_conf = _get_dag_config(context)
        conn_id = dag_conf.get("sf_conn_id", "salesforce_api")

        logging.info(f"POST /services/oauth2/token (conn_id={conn_id})")
        credentials = get_salesforce_token(conn_id)
        logging.info(f"Authenticated to {credentials['instance_url']}")
        logging.info(f"Token: {credentials['access_token'][:20]}...")
        logging.info("Step 1 complete: access_token acquired")
        return credentials

    @task()
    def extract_data(**context):
        """Extract data from Oracle and split into batch CSV files."""
        import numpy as np
        import pandas as pd
        from airflow.models import Variable
        from airflow.providers.oracle.hooks.oracle import OracleHook

        logging.info("=" * 60)
        logging.info("Step 2: extract_data — Query Oracle → CSV batch files")
        logging.info("=" * 60)

        dag_conf = _get_dag_config(context)

        # Batch size: DAG config > Airflow Variable > Default
        batch_size = int(
            dag_conf.get(
                "batch_size",
                Variable.get("batch_size", default_var=DEFAULT_BATCH_SIZE),
            )
        )

        # Table name from config
        table_name = dag_conf.get("table_name", DEFAULT_TABLE_NAME)

        # Extract query (allow override)
        query = dag_conf.get(
            "extract_query",
            DEFAULT_EXTRACT_QUERY.format(table_name=table_name),
        )

        logging.info(f"Config: table={table_name}, batch_size={batch_size}")
        logging.info(f"SQL: {query.strip()}")

        oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
        logging.info("Querying Oracle (oracle_kpc)...")
        df = oracle_hook.get_pandas_df(query)
        total_records = len(df)

        logging.info(f"Extracted {total_records} records from Oracle")

        # Handle zero records
        if total_records == 0:
            logging.warning("No records extracted from Oracle. Skipping upload.")
            return {
                "total_records": 0,
                "batch_count": 0,
                "batch_size": batch_size,
                "batch_files": [],
                "table_name": table_name,
            }

        df.columns = [col.upper() for col in df.columns]
        logging.info(f"Columns (Oracle): {list(df.columns)}")

        # Apply column mapping if provided (rename Oracle cols → SF fields)
        column_mapping = dag_conf.get("column_mapping")
        if column_mapping:
            # column_mapping = {"ORACLE_COL": "SF_Field__c", ...}
            # Keep only mapped columns and rename them
            available = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df[list(available.keys())]
            df = df.rename(columns=available)
            logging.info(f"Column mapping applied: {available}")
            logging.info(f"Columns (SF): {list(df.columns)}")

        # Split into batches
        n_batches = math.ceil(total_records / batch_size)
        batches = np.array_split(df, n_batches)

        os.makedirs(DATA_DIR, exist_ok=True)
        batch_files = []

        for i, batch_df in enumerate(batches, start=1):
            filename = f"{table_name}_batch_{i:03d}.csv"
            filepath = os.path.join(DATA_DIR, filename)
            batch_df.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)
            batch_files.append(filepath)
            logging.info(f"Wrote batch {i:03d}: {len(batch_df)} records → {filename}")

        logging.info(
            f"Step 2 complete: {total_records} records → "
            f"{len(batch_files)} batch files (batch_size={batch_size})"
        )

        # --- DB Log: run start ---
        from migration_logger import MigrationLogger

        dag_run = context.get("dag_run")
        ml = MigrationLogger()
        ml.log_run_start(
            run_id=dag_run.run_id,
            dag_id=DAG_ID,
            table_name=table_name,
            sf_object=dag_conf.get("sf_object", ""),
            operation=dag_conf.get("operation", "upsert"),
            execution_date=dag_run.logical_date,
            total_records=total_records,
            total_batches=len(batch_files),
            batch_size=batch_size,
            start_batch=int(dag_conf.get("start_batch", 1)),
            dag_conf=dag_conf or None,
        )

        return {
            "total_records": total_records,
            "batch_count": len(batch_files),
            "batch_size": batch_size,
            "batch_files": batch_files,
            "table_name": table_name,
        }

    @task()
    def upload_batches(credentials, extract_result, **context):
        """Upload batch CSV files to Salesforce via Bulk API 2.0."""
        from salesforce_bulk_loader import SalesforceBulkLoader

        logging.info("=" * 60)
        logging.info("Step 3: upload_batches — Bulk API 2.0 Upload")
        logging.info("=" * 60)

        batch_files = extract_result.get("batch_files", [])
        if not batch_files:
            logging.warning("No batch files to upload. Skipping.")
            return {"job_results": [], "total_processed": 0, "total_failed": 0}

        dag_conf = _get_dag_config(context)

        # SF object: required via DAG config
        sf_object = dag_conf.get("sf_object")
        if not sf_object:
            raise ValueError(
                "DAG config must include 'sf_object'. "
                "Example: --conf '{\"sf_object\": \"TMS_Request__c\"}'"
            )
        operation = dag_conf.get("operation", "upsert")

        # external_id_field: required for upsert, not needed for insert
        external_id_field = dag_conf.get("external_id_field")
        if operation == "upsert" and not external_id_field:
            raise ValueError(
                "DAG config must include 'external_id_field' for upsert operation. "
                "Example: --conf '{\"external_id_field\": \"External_Id__c\"}'"
            )

        # Start batch (for resume)
        start_batch = int(dag_conf.get("start_batch", 1))

        # Filter batch files for resume
        files_to_upload = batch_files[start_batch - 1:]
        if start_batch > 1:
            logging.info(f"Resuming from batch {start_batch}, skipping {start_batch - 1} batches")

        logging.info(f"Target object: {sf_object}")
        logging.info(f"Operation: {operation}")
        logging.info(f"External ID field: {external_id_field}")
        logging.info(f"Batch files to upload: {len(files_to_upload)}")
        logging.info(f"Instance: {credentials['instance_url']}")

        # --- DB Log: batch starts ---
        from migration_logger import MigrationLogger

        dag_run = context.get("dag_run")
        ml = MigrationLogger()
        for idx, fpath in enumerate(files_to_upload, start=start_batch):
            try:
                with open(fpath) as _f:
                    rec_count = sum(1 for _ in _f) - 1
            except Exception:
                rec_count = 0
            ml.log_batch_start(
                run_id=dag_run.run_id,
                batch_number=idx,
                file_path=fpath,
                records_in_batch=rec_count,
            )

        loader = SalesforceBulkLoader(
            instance_url=credentials["instance_url"],
            access_token=credentials["access_token"],
            api_version="v66.0",
        )

        if len(files_to_upload) == 1:
            logging.info(f"Single batch mode: {files_to_upload[0]}")
            logging.info("POST /services/data/v66.0/jobs/ingest → create job")
            result = loader.load_file(
                object_name=sf_object,
                csv_file_path=files_to_upload[0],
                external_id_field=external_id_field,
                operation=operation,
            )
            results = [result]
        else:
            logging.info(f"Parallel mode: {len(files_to_upload)} batches (max 15 concurrent)")
            for f in files_to_upload:
                logging.info(f"  - {os.path.basename(f)}")
            results = loader.load_files_parallel(
                object_name=sf_object,
                csv_files=files_to_upload,
                external_id_field=external_id_field,
                operation=operation,
            )

        total_processed = sum(r.records_processed for r in results)
        total_failed = sum(r.records_failed for r in results)

        # Log per-job results + DB batch completion
        for idx, r in enumerate(results, start=start_batch):
            status_icon = "OK" if r.state == "JobComplete" else "FAIL"
            logging.info(
                f"  [{status_icon}] Job {r.job_id}: "
                f"state={r.state}, processed={r.records_processed}, "
                f"failed={r.records_failed}, file={os.path.basename(r.file_path or '')}"
            )
            if r.error_message:
                logging.error(f"    Error: {r.error_message}")

            ml.log_batch_complete(
                run_id=dag_run.run_id,
                batch_number=idx,
                job_id=r.job_id,
                state=r.state,
                records_processed=r.records_processed,
                records_failed=r.records_failed,
                error_message=r.error_message,
            )

        # Serialize results for XCom
        job_results = [
            {
                "job_id": r.job_id,
                "state": r.state,
                "records_processed": r.records_processed,
                "records_failed": r.records_failed,
                "file_path": r.file_path,
                "error_message": r.error_message,
            }
            for r in results
        ]

        # Check for failures
        failed_jobs = [r for r in results if r.state != "JobComplete"]
        if failed_jobs:
            failed_files = [r.file_path for r in failed_jobs]
            logging.error(f"Failed jobs for files: {failed_files}")

        logging.info(
            f"Step 3 complete: {total_processed} processed, "
            f"{total_failed} failed, {len(results)} jobs"
        )

        return {
            "job_results": job_results,
            "total_processed": total_processed,
            "total_failed": total_failed,
            "has_failures": len(failed_jobs) > 0,
        }

    @task()
    def collect_results(credentials, upload_result, **context):
        """Fetch successful/failed/unprocessed result CSVs from bulk jobs."""
        import requests as req

        logging.info("=" * 60)
        logging.info("Step 4: collect_results — Fetch result CSVs from Salesforce")
        logging.info("=" * 60)

        job_results = upload_result.get("job_results", [])
        if not job_results:
            logging.warning("No job results to collect. Skipping.")
            return {"result_files": []}

        logging.info(f"Collecting results for {len(job_results)} jobs")
        os.makedirs(LOG_DIR, exist_ok=True)

        base_url = f"{credentials['instance_url'].rstrip('/')}/services/data/v66.0"
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "text/csv",
        }

        result_files = []

        for jr in job_results:
            job_id = jr["job_id"]
            if not job_id:
                continue

            logging.info(f"--- Job {job_id} ---")

            # Fetch each result type
            for result_type in ["successfulResults", "failedResults", "unprocessedrecords"]:
                type_short = {
                    "successfulResults": "success",
                    "failedResults": "failed",
                    "unprocessedrecords": "unprocessed",
                }[result_type]

                url = f"{base_url}/jobs/ingest/{job_id}/{result_type}"
                logging.info(f"GET /jobs/ingest/{job_id}/{result_type}")

                try:
                    response = req.get(url, headers=headers)

                    if response.status_code == 200 and response.text.strip():
                        filename = f"{job_id}_{type_short}.csv"
                        filepath = os.path.join(LOG_DIR, filename)

                        with open(filepath, "w") as f:
                            f.write(response.text)

                        # Count lines (minus header)
                        line_count = response.text.strip().count("\n")
                        result_files.append(filepath)
                        logging.info(
                            f"  Saved {result_type} → {filename} ({line_count} records)"
                        )
                    else:
                        logging.info(
                            f"  No {result_type} (HTTP {response.status_code})"
                        )

                except Exception as e:
                    logging.warning(f"  Failed to fetch {result_type}: {e}")

        logging.info(
            f"Step 4 complete: collected {len(result_files)} result files → {LOG_DIR}"
        )

        # --- DB Log: run complete ---
        from migration_logger import MigrationLogger

        dag_run = context.get("dag_run")
        ml = MigrationLogger()

        has_failures = upload_result.get("has_failures", False)
        total_processed = upload_result.get("total_processed", 0)
        total_failed = upload_result.get("total_failed", 0)

        if has_failures:
            run_status = "partial" if total_processed > 0 else "failed"
        else:
            run_status = "success"

        ml.log_run_complete(
            run_id=dag_run.run_id,
            status=run_status,
            total_processed=total_processed,
            total_failed=total_failed,
            error_message=f"{total_failed} records failed" if has_failures else None,
        )
        logging.info(f"DB Log: run status updated to '{run_status}'")

        return {"result_files": result_files}

    # Wire task dependencies
    # Step 1: authenticate (parallel with Step 2)
    # Step 2: extract_data (parallel with Step 1)
    # Step 3: upload_batches (needs creds + batch files)
    # Step 4: collect_results (needs creds + job results)
    creds = authenticate()
    extract_result = extract_data()
    upload_result = upload_batches(creds, extract_result)
    collect_results(creds, upload_result)


# Instantiate DAG
migrate_bulk_api()
