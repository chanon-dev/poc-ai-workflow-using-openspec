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
from airflow.providers.standard.operators.bash import BashOperator
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
WHERE ROWNUM <= 1
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
    """Extract data from Oracle using multi-table JOIN."""
    logging.info("Extracting Product & Price data from Oracle...")

    # Execute query via OracleHook
    oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
    df = oracle_hook.get_pandas_df(EXTRACT_QUERY)

    logging.info(f"Extracted {len(df)} records")

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

    # Ensure output directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Write to CSV
    df.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_ALL)
    logging.info(f"Wrote {len(df)} records to {OUTPUT_FILE}")

    return len(df)


def run_gx_validation(df, suite_name, context_root, run_name="validation"):
    """Run GX validation on a dataframe and persist results to data docs."""
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

    # Run validation
    results = validator.validate(result_format="COMPLETE")

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
    """Validate extracted CSV using Great Expectations."""
    import pandas as pd

    # Get source count from XCom
    ti = context["ti"]
    source_count = ti.xcom_pull(task_ids="extract_data")

    logging.info(f"Validating extracted CSV (expected {source_count} rows)...")

    # Read the extracted CSV
    df = pd.read_csv(OUTPUT_FILE)
    actual_count = len(df)

    # Run GX validation
    context_root = os.path.join(AIRFLOW_HOME, "great_expectations")
    results = run_gx_validation(
        df=df,
        suite_name="extract_product_price",
        context_root=context_root,
        run_name="extract_validation",
    )

    # Log results
    for result in results.results:
        status = "PASS" if result.success else "WARN"
        exp_type = result.expectation_config.expectation_type
        logging.info(f"Extract Validation: {status} - {exp_type}")

    # Additional row count check
    if actual_count != source_count:
        logging.warning(f"Row count mismatch - Source: {source_count}, CSV: {actual_count}")

    logging.info(f"Extract validation: {actual_count} rows extracted")

    # Extract validation is non-blocking (warn only)
    return {"success": results.success, "row_count": actual_count}


def validate_postmig_data(**context):
    """Validate post-migration reconciliation using Great Expectations."""
    import pandas as pd

    # Get source count from XCom
    ti = context["ti"]
    source_count = ti.xcom_pull(task_ids="extract_data")

    logging.info(f"Running post-migration reconciliation (expected {source_count} rows)...")

    success_log = os.path.join(LOG_DIR, "Product2_success.csv")

    if not os.path.exists(success_log):
        logging.warning(f"Success log not found: {success_log}")
        return {
            "success": False,
            "message": "Success log not found",
            "source_count": source_count,
            "loaded_count": 0,
            "difference": source_count,
        }

    # Read success log
    df = pd.read_csv(success_log)
    actual_count = len(df)
    difference = source_count - actual_count

    # Run GX validation
    context_root = os.path.join(AIRFLOW_HOME, "great_expectations")
    results = run_gx_validation(
        df=df,
        suite_name="postmig_product_price",
        context_root=context_root,
        run_name="postmig_validation",
    )

    # Log results
    for result in results.results:
        status = "PASS" if result.success else "WARN"
        exp_type = result.expectation_config.expectation_type
        logging.info(f"PostMig Validation: {status} - {exp_type}")

    # Log reconciliation results (don't fail on mismatch per proposal)
    if actual_count != source_count:
        logging.warning(
            f"RECONCILIATION ALERT: Source={source_count}, Loaded={actual_count}, "
            f"Diff={difference}"
        )
    else:
        logging.info(f"Reconciliation OK: {actual_count} records loaded")

    return {
        "success": results.success,
        "source_count": source_count,
        "loaded_count": actual_count,
        "difference": difference,
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

    # Task 4: Run Data Loader
    # Uses master process-conf.xml (read-only)
    run_dataloader = BashOperator(
        task_id="run_dataloader",
        bash_command=f"/opt/dataloader/process.sh {CONFIG_DIR} {PROCESS_NAME}",
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
