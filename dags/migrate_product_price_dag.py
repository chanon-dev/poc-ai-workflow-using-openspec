"""
Execution DAG: Migrate Product & Price Data

Trigger: Schedule or Manual

Pipeline Steps:
1. extract_data - Query Oracle → CSV
2. run_dataloader - Call Data Loader (read-only from Master Config)
3. audit_results - Check error/success logs

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
WHERE ROWNUM <= 100
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
    tags=["salesforce", "migration", "product"],
) as dag:

    # Task 1: Extract data from Oracle
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    # Task 2: Run Data Loader
    # Uses master process-conf.xml (read-only)
    run_dataloader = BashOperator(
        task_id="run_dataloader",
        bash_command=f"/opt/dataloader/process.sh {CONFIG_DIR} {PROCESS_NAME}",
    )

    # Task 3: Audit results
    audit_task = PythonOperator(
        task_id="audit_results",
        python_callable=audit_results,
    )

    # Pipeline flow
    extract_task >> run_dataloader >> audit_task
