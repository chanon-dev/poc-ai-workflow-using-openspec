"""
Execution DAG: Migrate Product & Price Data

Trigger: Schedule or Manual

Pipeline Steps:
1. validate_source - GX validation on Oracle source
2. extract_data - Query Oracle → CSV
3. validate_extract - GX validation on extracted CSV
4. run_dataloader - Call Data Loader (read-only from Master Config)
5. audit_results - Check error/success logs
6. validate_postmig - GX reconciliation check

Source Tables (per Data Dictionary 12_Product & Price):
- KPS_T_REQPROD_MD (Main - Product Request)
- KPS_T_APPRV_M (Approval Master)
- KPS_R_UNIT (Reference: Unit)

Target: Salesforce Product2 object

Oracle Columns (mapped via SDL to SF fields):
- BARCODE, UNIT_DESC, KPS_EFF_SDATE, KPS_EFF_EDATE
- STD_CATE_CODE, PROD_SERV_CODE, PROD_SERV_NAME
- KPS_PRICE_EXC_VAT, KPS_PRICE_INC_VAT
"""

import csv
import os
import logging
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.oracle.hooks.oracle import OracleHook
import oracledb

# Initialize Oracle Client (Thick Mode for older password verifiers)
try:
    oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")
except Exception as e:
    logging.warning(f"Oracle Client Init: {e}")

# Constants
DAG_ID = "migrate_product_price"
PROCESS_NAME = "Product2_Process"
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
SALESFORCE_DIR = os.path.join(AIRFLOW_HOME, "salesforce")
DATA_DIR = os.path.join(SALESFORCE_DIR, "data")
LOG_DIR = os.path.join(SALESFORCE_DIR, "logs")
CONFIG_DIR = os.path.join(SALESFORCE_DIR, "dataloader_conf")
OUTPUT_FILE = os.path.join(DATA_DIR, "Product2.csv")

# Batch Configuration
DEFAULT_BATCH_SIZE = 40000
BATCH_PREFIX = "Product2_batch"


def get_batch_config(**context):
    """Get batch configuration from DAG config > Airflow Variable > Default.

    Priority: DAG run config > Airflow Variable > Default value

    Returns:
        dict: {"batch_size": int, "start_batch": int}
    """
    from airflow.models import Variable

    dag_run = context.get("dag_run")
    dag_conf = dag_run.conf if dag_run and dag_run.conf else {}

    # Batch size: DAG config > Airflow Variable > Default
    batch_size = dag_conf.get("batch_size")
    if batch_size is None:
        batch_size = int(Variable.get("batch_size", default_var=DEFAULT_BATCH_SIZE))
    batch_size = int(batch_size)

    # Warn if batch size is too small
    if batch_size < 1000:
        logging.warning(f"Batch size {batch_size} is very small. Recommended minimum: 1000")

    # Start batch: DAG config > Default (1)
    start_batch = int(dag_conf.get("start_batch", 1))

    return {"batch_size": batch_size, "start_batch": start_batch}


def split_dataframe_to_batches(df, batch_size):
    """Split DataFrame into batches using numpy.array_split.

    Args:
        df: pandas DataFrame to split
        batch_size: Number of rows per batch

    Returns:
        list: List of DataFrame batches
    """
    import math
    import numpy as np

    if len(df) == 0:
        return []

    n_batches = math.ceil(len(df) / batch_size)
    batches = np.array_split(df, n_batches)

    logging.info(f"Split {len(df)} records into {len(batches)} batches (batch_size={batch_size})")
    return batches


def write_batch_files(batches, prefix, data_dir):
    """Write batch DataFrames to CSV files with zero-padded naming.

    Args:
        batches: List of DataFrame batches
        prefix: File prefix (e.g., "Product2_batch")
        data_dir: Output directory path

    Returns:
        list: List of created file paths
    """
    import csv

    os.makedirs(data_dir, exist_ok=True)
    batch_files = []

    for i, batch_df in enumerate(batches, start=1):
        filename = f"{prefix}_{i:03d}.csv"
        filepath = os.path.join(data_dir, filename)
        batch_df.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)
        logging.info(f"Wrote batch {i:03d}: {len(batch_df)} records to {filename}")
        batch_files.append(filepath)

    return batch_files


# SQL Query following Data Dictionary 12_Product & Price
# Uses Oracle column names directly (mapped via SDL)
EXTRACT_QUERY = """
SELECT
    r.BARCODE,
    u.UNIT_DESC,
    a.KPS_EFF_SDATE,
    a.KPS_EFF_EDATE,
    r.STD_CATE_CODE,
    r.PROD_SERV_CODE,
    r.PROD_SERV_NAME,
    a.KPS_PRICE_EXC_VAT,
    a.KPS_PRICE_INC_VAT
FROM KPS_T_REQPROD_MD r
JOIN KPS_T_APPRV_M a
    ON  r.CON_CODE = a.CON_CODE
    AND r.SHOP_CODE = a.SHOP_CODE
    AND r.PROD_SERV_CODE = a.PROD_SERV_CODE
LEFT JOIN KPS_R_UNIT u
    ON a.UNIT_CODE = u.UNIT_CODE
WHERE ROWNUM <= 80000
"""


def format_datetime(val):
    """Format datetime for Salesforce (ISO 8601)."""
    if val is None:
        return ""
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%dT%H:%M:%S.000+0700")
    if isinstance(val, str):
        # Try to parse and reformat
        for fmt in ["%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]:
            try:
                dt = datetime.strptime(val.strip(), fmt)
                return dt.strftime("%Y-%m-%dT%H:%M:%S.000+0700")
            except ValueError:
                continue
        return val
    return str(val)


def format_decimal(val, precision=2):
    """Format decimal for Salesforce."""
    if val is None:
        return ""
    try:
        return f"{float(val):.{precision}f}"
    except (ValueError, TypeError):
        return str(val)


def extract_data(**context):
    """Extract data from Oracle and split into batch files.

    Returns via XCom:
        dict: {
            "total_records": int,
            "batch_count": int,
            "batch_size": int,
            "batch_files": list[str]
        }
    """
    logging.info("Extracting Product & Price data from Oracle...")

    # Get batch configuration
    batch_config = get_batch_config(**context)
    batch_size = batch_config["batch_size"]

    # Execute query via OracleHook
    oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
    df = oracle_hook.get_pandas_df(EXTRACT_QUERY)

    total_records = len(df)
    logging.info(f"Extracted {total_records} records")

    # Handle empty extraction
    if total_records == 0:
        logging.warning("No records extracted from Oracle. Skipping batch file creation.")
        return {
            "total_records": 0,
            "batch_count": 0,
            "batch_size": batch_size,
            "batch_files": []
        }

    # Oracle returns uppercase column names, convert to uppercase for matching
    df.columns = [col.upper() for col in df.columns]

    # Apply transformations (use Oracle column names - uppercase)
    datetime_cols = ["KPS_EFF_SDATE", "KPS_EFF_EDATE"]
    decimal_cols = ["KPS_PRICE_EXC_VAT", "KPS_PRICE_INC_VAT"]

    for col in datetime_cols:
        if col in df.columns:
            df[col] = df[col].apply(format_datetime)

    for col in decimal_cols:
        if col in df.columns:
            df[col] = df[col].apply(format_decimal)

    # Split into batches and write files
    batches = split_dataframe_to_batches(df, batch_size)
    batch_files = write_batch_files(batches, BATCH_PREFIX, DATA_DIR)

    logging.info(f"Created {len(batch_files)} batch files from {total_records} records")

    return {
        "total_records": total_records,
        "batch_count": len(batch_files),
        "batch_size": batch_size,
        "batch_files": batch_files
    }


def upload_batch(batch_file, config_dir, process_name):
    """Upload a single batch file using Data Loader.

    Args:
        batch_file: Path to batch CSV file
        config_dir: Path to Data Loader config directory
        process_name: Name of the Data Loader process

    Returns:
        dict: {"success_count": int, "error_count": int, "batch_file": str}
    """
    import subprocess

    batch_name = os.path.basename(batch_file).replace(".csv", "")
    logging.info(f"Uploading batch: {batch_name}")

    # Run Data Loader
    # Define batch-specific log files
    success_log = os.path.join(LOG_DIR, f"{batch_name}_success.csv")
    error_log = os.path.join(LOG_DIR, f"{batch_name}_error.csv")

    # Run Data Loader (Direct Java call to support dynamic arguments)
    cmd = [
        "java",
        "--enable-native-access=ALL-UNNAMED",
        "-cp",
        "/opt/dataloader/dataloader-64.1.0.jar",
        "com.salesforce.dataloader.process.DataLoaderRunner",
        "run.mode=batch",
        f"salesforce.config.dir={config_dir}",
        f"process.name={process_name}",
        f"dataAccess.name={batch_file}",
        f"process.outputSuccess={success_log}",
        f"process.outputError={error_log}",
        "sfdc.debugMessages=true"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"Batch {batch_name} upload failed: {result.stderr}")
        raise RuntimeError(f"Data Loader failed for {batch_name}: {result.stderr}")

    # Read batch-specific logs
    success_log = os.path.join(LOG_DIR, f"{batch_name}_success.csv")
    error_log = os.path.join(LOG_DIR, f"{batch_name}_error.csv")

    success_count = 0
    error_count = 0

    if os.path.exists(success_log):
        with open(success_log) as f:
            success_count = max(0, len(f.readlines()) - 1)

    if os.path.exists(error_log):
        with open(error_log) as f:
            error_count = max(0, len(f.readlines()) - 1)

    logging.info(f"Batch {batch_name}: {success_count} success, {error_count} errors")

    return {
        "success_count": success_count,
        "error_count": error_count,
        "batch_file": batch_file
    }


def upload_all_batches(batch_files, start_batch=1):
    """Upload all batch files sequentially.

    Args:
        batch_files: List of batch file paths
        start_batch: Batch number to start from (for resume)

    Returns:
        list: Results from each batch upload
    """
    results = []
    total_success = 0
    total_errors = 0

    for i, batch_file in enumerate(batch_files, start=1):
        # Skip batches before start_batch (for resume)
        if i < start_batch:
            logging.info(f"Skipping batch {i:03d} (start_batch={start_batch})")
            continue

        try:
            result = upload_batch(batch_file, CONFIG_DIR, PROCESS_NAME)
            results.append(result)
            total_success += result["success_count"]
            total_errors += result["error_count"]
        except RuntimeError as e:
            logging.error(f"Batch {i:03d} failed completely. Stopping upload.")
            raise RuntimeError(f"Upload stopped at batch {i:03d}: {e}")

    logging.info(f"Upload complete: {total_success} total success, {total_errors} total errors")
    return results


def aggregate_logs(batch_files, log_dir):
    """Aggregate success and error logs from all batches.

    Args:
        batch_files: List of batch file paths
        log_dir: Directory containing log files

    Returns:
        dict: {"success_file": str, "error_file": str, "success_count": int, "error_count": int}
    """
    import pandas as pd

    all_success = []
    all_errors = []

    for batch_file in batch_files:
        batch_name = os.path.basename(batch_file).replace(".csv", "")
        success_log = os.path.join(log_dir, f"{batch_name}_success.csv")
        error_log = os.path.join(log_dir, f"{batch_name}_error.csv")

        if os.path.exists(success_log):
            df = pd.read_csv(success_log)
            all_success.append(df)

        if os.path.exists(error_log):
            df = pd.read_csv(error_log)
            all_errors.append(df)

    # Write aggregated logs
    success_file = os.path.join(log_dir, "Product2_success.csv")
    error_file = os.path.join(log_dir, "Product2_error.csv")

    if all_success:
        pd.concat(all_success).to_csv(success_file, index=False)
        logging.info(f"Aggregated {sum(len(df) for df in all_success)} success records to {success_file}")
    else:
        pd.DataFrame().to_csv(success_file, index=False)

    if all_errors:
        pd.concat(all_errors).to_csv(error_file, index=False)
        logging.info(f"Aggregated {sum(len(df) for df in all_errors)} error records to {error_file}")
    else:
        pd.DataFrame().to_csv(error_file, index=False)

    return {
        "success_file": success_file,
        "error_file": error_file,
        "success_count": sum(len(df) for df in all_success) if all_success else 0,
        "error_count": sum(len(df) for df in all_errors) if all_errors else 0
    }


def run_dataloader_batches(**context):
    """Run Data Loader for all batch files sequentially.

    Returns:
        dict: Aggregated upload results
    """
    ti = context["ti"]
    extract_result = ti.xcom_pull(task_ids="extract_data")

    batch_files = extract_result.get("batch_files", [])
    if not batch_files:
        logging.warning("No batch files to upload")
        return {"total_success": 0, "total_errors": 0, "batch_results": []}

    # Get start_batch config for resume
    batch_config = get_batch_config(**context)
    start_batch = batch_config["start_batch"]

    # Upload all batches
    batch_results = upload_all_batches(batch_files, start_batch)

    # Aggregate logs
    log_result = aggregate_logs(batch_files, LOG_DIR)

    return {
        "total_success": log_result["success_count"],
        "total_errors": log_result["error_count"],
        "batch_results": batch_results
    }


def run_gx_validation(df, suite_name, context_root, run_name="validation",
                      evaluation_parameters=None):
    """Run GX validation on a dataframe and persist results to data docs.

    Args:
        df: pandas DataFrame to validate
        suite_name: Name of the expectation suite
        context_root: Path to GX context directory
        run_name: Identifier for this validation run
        evaluation_parameters: Dict of runtime parameters for $PARAMETER references
    """
    import great_expectations as gx
    from great_expectations.core.batch import RuntimeBatchRequest
    from great_expectations.core import ExpectationSuiteValidationResult
    from great_expectations.data_context.types.resource_identifiers import (
        ValidationResultIdentifier,
        ExpectationSuiteIdentifier,
        BatchIdentifier,
    )
    from great_expectations.core.run_identifier import RunIdentifier

    logging.info(f"Running GX validation with suite: {suite_name}")
    if evaluation_parameters:
        logging.info(f"Evaluation parameters: {evaluation_parameters}")

    # Get GX context
    gx_context = gx.get_context(context_root_dir=context_root)

    # Add runtime datasource if not exists
    try:
        gx_context.get_datasource("runtime_datasource")
    except Exception:
        datasource_config = {
            "name": "runtime_datasource",
            "class_name": "Datasource",
            "module_name": "great_expectations.datasource",
            "execution_engine": {
                "class_name": "PandasExecutionEngine",
                "module_name": "great_expectations.execution_engine",
            },
            "data_connectors": {
                "runtime_connector": {
                    "class_name": "RuntimeDataConnector",
                    "module_name": "great_expectations.datasource.data_connector",
                    "batch_identifiers": ["batch_id"],
                }
            },
        }
        gx_context.add_datasource(**datasource_config)

    # Create batch request
    batch_request = RuntimeBatchRequest(
        datasource_name="runtime_datasource",
        data_connector_name="runtime_connector",
        data_asset_name=run_name,
        runtime_parameters={"batch_data": df},
        batch_identifiers={"batch_id": run_name},
    )

    # Get validator
    validator = gx_context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
    )

    # Run validation with evaluation parameters (for $PARAMETER references)
    results = validator.validate(
        result_format="COMPLETE",
        evaluation_parameters=evaluation_parameters or {}
    )

    # Create validation result identifier for storing
    run_id = RunIdentifier(run_name=run_name)
    validation_result_id = ValidationResultIdentifier(
        expectation_suite_identifier=ExpectationSuiteIdentifier(
            expectation_suite_name=suite_name
        ),
        run_id=run_id,
        batch_identifier=run_name,
    )

    # Store validation result
    gx_context.validations_store.set(validation_result_id, results)

    # Build data docs to include validation results
    gx_context.build_data_docs()

    logging.info(f"GX Validation success: {results.success}")
    return results


def validate_source_data(**context):
    """Validate source data in Oracle using Great Expectations."""
    import pandas as pd

    logging.info("Validating source data in Oracle...")

    # Get data from Oracle
    oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
    validation_query = """
    SELECT BARCODE, STD_CATE_CODE, PROD_SERV_CODE
    FROM KPS_T_REQPROD_MD
    WHERE ROWNUM <= 1000
    """
    df = oracle_hook.get_pandas_df(validation_query)
    df.columns = [col.upper() for col in df.columns]

    row_count = len(df)
    logging.info(f"Fetched {row_count} rows for validation")

    # Run GX validation
    context_root = os.path.join(AIRFLOW_HOME, "great_expectations")
    results = run_gx_validation(
        df=df,
        suite_name="source_product_price",
        context_root=context_root,
        run_name="source_validation",
    )

    # Log results
    for result in results.results:
        status = "PASS" if result.success else "FAIL"
        exp_type = result.expectation_config.expectation_type
        logging.info(f"Source Validation: {status} - {exp_type}")

    if not results.success:
        failed = [r.expectation_config.expectation_type for r in results.results if not r.success]
        raise ValueError(f"Source validation failed: {failed}")

    logging.info("Source validation passed")
    return {"success": True, "row_count": row_count}


def validate_extract_data(**context):
    """Validate each extracted batch file using Great Expectations.

    Returns:
        dict: Aggregated validation results across all batches
    """
    import pandas as pd

    # Get extract result from XCom
    ti = context["ti"]
    extract_result = ti.xcom_pull(task_ids="extract_data")

    total_records = extract_result.get("total_records", 0)
    batch_files = extract_result.get("batch_files", [])

    if not batch_files:
        logging.warning("No batch files to validate")
        return {"success": True, "total_validated": 0, "batch_results": []}

    logging.info(f"Validating {len(batch_files)} batch files (total {total_records} records)...")

    context_root = os.path.join(AIRFLOW_HOME, "great_expectations")
    batch_results = []
    failed_batches = []

    # Validate each batch individually
    for i, batch_file in enumerate(batch_files, start=1):
        df = pd.read_csv(batch_file)
        batch_row_count = len(df)

        logging.info(f"Validating batch {i:03d}: {batch_row_count} records")

        results = run_gx_validation(
            df=df,
            suite_name="extract_product_price",
            context_root=context_root,
            run_name=f"extract_validation_batch_{i:03d}",
            evaluation_parameters={
                "batch_row_count": batch_row_count,
                "source_count": total_records
            }
        )

        batch_results.append({
            "batch": i,
            "file": batch_file,
            "row_count": batch_row_count,
            "success": results.success
        })

        if not results.success:
            failed_batches.append(i)
            logging.warning(f"Batch {i:03d} validation failed")

    # Log summary
    total_validated = sum(br["row_count"] for br in batch_results)
    overall_success = len(failed_batches) == 0

    if failed_batches:
        logging.warning(f"Extract validation: WARN - batches failed: {failed_batches}")
    else:
        logging.info(f"Extract validation: PASS - all {len(batch_files)} batches validated")

    logging.info(f"Total validated: {total_validated} records")

    # Extract validation is non-blocking (warn only)
    return {
        "success": overall_success,
        "total_validated": total_validated,
        "batch_results": batch_results,
        "failed_batches": failed_batches
    }


def validate_postmig_data(**context):
    """Validate post-migration reconciliation using Great Expectations.

    Provides per-batch reconciliation and overall summary.
    """
    import pandas as pd

    # Get extract result from XCom
    ti = context["ti"]
    extract_result = ti.xcom_pull(task_ids="extract_data")

    total_records = extract_result.get("total_records", 0)
    batch_files = extract_result.get("batch_files", [])

    logging.info(f"Running post-migration reconciliation (expected {total_records} rows)...")

    # Use aggregated success log
    success_log = os.path.join(LOG_DIR, "Product2_success.csv")

    if not os.path.exists(success_log) or os.stat(success_log).st_size <= 1:
        logging.warning(f"Success log not found or empty: {success_log}")
        return {
            "success": False,
            "message": "Success log not found or empty",
            "source_count": total_records,
            "loaded_count": 0,
            "difference": total_records,
        }

    # Read aggregated success log
    df = pd.read_csv(success_log)
    loaded_count = len(df)
    total_difference = total_records - loaded_count

    # Per-batch reconciliation logging
    batch_reconciliation = []
    for i, batch_file in enumerate(batch_files, start=1):
        batch_df = pd.read_csv(batch_file)
        batch_extracted = len(batch_df)

        # Read per-batch success log if exists
        batch_name = os.path.basename(batch_file).replace(".csv", "")
        batch_success_log = os.path.join(LOG_DIR, f"{batch_name}_success.csv")
        batch_loaded = 0
        if os.path.exists(batch_success_log):
            batch_loaded = max(0, len(pd.read_csv(batch_success_log)))

        batch_diff = batch_extracted - batch_loaded
        batch_reconciliation.append({
            "batch": i,
            "extracted": batch_extracted,
            "loaded": batch_loaded,
            "difference": batch_diff
        })
        logging.info(f"Batch {i:03d}: {batch_extracted} extracted, {batch_loaded} loaded, {batch_diff} diff")

    # Log summary
    logging.info(f"Total: {total_records} extracted, {loaded_count} loaded, {total_difference} diff")

    # Run GX validation with evaluation parameters
    context_root = os.path.join(AIRFLOW_HOME, "great_expectations")
    results = run_gx_validation(
        df=df,
        suite_name="postmig_product_price",
        context_root=context_root,
        run_name="postmig_validation",
        evaluation_parameters={"source_count": total_records}
    )

    # Log results
    for result in results.results:
        status = "PASS" if result.success else "WARN"
        exp_type = result.expectation_config.expectation_type
        logging.info(f"PostMig Validation: {status} - {exp_type}")

    return {
        "success": results.success,
        "source_count": total_records,
        "loaded_count": loaded_count,
        "difference": total_difference,
        "batch_reconciliation": batch_reconciliation
    }


def audit_results(**context):
    """Check Data Loader logs for errors."""
    error_log = os.path.join(LOG_DIR, "Product2_error.csv")
    success_log = os.path.join(LOG_DIR, "Product2_success.csv")

    # Check error log
    error_count = 0
    if os.path.exists(error_log):
        with open(error_log, "r") as f:
            lines = f.readlines()
            error_count = max(0, len(lines) - 1)  # Exclude header

    # Check success log
    success_count = 0
    if os.path.exists(success_log):
        with open(success_log, "r") as f:
            lines = f.readlines()
            success_count = max(0, len(lines) - 1)  # Exclude header

    logging.info(f"Audit Results: {success_count} success, {error_count} errors")

    if error_count > 0:
        raise ValueError(
            f"Data Loader found {error_count} errors! "
            f"Check {error_log} for details."
        )

    return {"success": success_count, "errors": error_count}


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "retries": 0,
}

with DAG(
    DAG_ID,
    default_args=default_args,
    description="Migrate Product & Price data from Oracle to Salesforce",
    schedule=None,  # Manual or configure schedule
    catchup=False,
    tags=["salesforce", "migration", "product", "gx"],
) as dag:

    # Task 1: Validate Source (blocks on failure)
    validate_source = PythonOperator(
        task_id="validate_source",
        python_callable=validate_source_data,
    )

    # Task 2: Extract data from Oracle
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    # Task 3: Validate Extracted Data
    validate_extract = PythonOperator(
        task_id="validate_extract",
        python_callable=validate_extract_data,
    )

    # Task 4: Run Data Loader for all batches
    run_dataloader = PythonOperator(
        task_id="run_dataloader",
        python_callable=run_dataloader_batches,
    )

    # Task 5: Audit results
    audit_task = PythonOperator(
        task_id="audit_results",
        python_callable=audit_results,
    )

    # Task 6: Validate Post-Migration (Reconciliation - alert only, no failure)
    validate_postmig = PythonOperator(
        task_id="validate_postmig",
        python_callable=validate_postmig_data,
    )

    # Pipeline flow
    validate_source >> extract_task >> validate_extract >> run_dataloader >> audit_task >> validate_postmig
