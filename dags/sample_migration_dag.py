import csv
import os
import logging
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
# Airflow 3.x Providers
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.models import Variable
import oracledb

# Initialize Oracle Client to enable Thick Mode (supports older password verifiers)
try:
    oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")
except Exception as e:
    logging.warning(f"Oracle Client Init Failed (Might already be init): {e}")

# Import project configurations
from dags.config.field_mappings import FIELD_MAPPINGS
from dags.config.tables_config import get_table_config

# Constants
DAG_ID = "migrate_sample_kps_t_sales_md"
TABLE_NAME = "KPS_T_SALES_MD"
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
SALESFORCE_DIR = os.path.join(AIRFLOW_HOME, "salesforce")
DATA_DIR = os.path.join(SALESFORCE_DIR, "data")
LOG_DIR = os.path.join(SALESFORCE_DIR, "logs")
CONFIG_DIR = os.path.join(SALESFORCE_DIR, "dataloader_conf")
PROCESS_NAME = f"{TABLE_NAME}_Process"

def extract_data_from_oracle(**context):
    """Extract sample data from Oracle to CSV."""
    logging.info(f"Extracting data for {TABLE_NAME}...")
    
    # Get table config and mappings
    table_config = get_table_config(TABLE_NAME)
    field_mapping = FIELD_MAPPINGS.get(TABLE_NAME)
    
    if not table_config or not field_mapping:
        raise ValueError(f"Configuration not found for {TABLE_NAME}")

    # Build Query
    # Note: Simplified query for sample. limit 100
    columns = list(field_mapping.mappings.keys())
    col_str = ", ".join(columns)
    query = f"SELECT {col_str} FROM {TABLE_NAME} WHERE ROWNUM <= 100"
    
    logging.info(f"Executing query: {query}")
    
    # Execute Query via Hook
    oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
    df = oracle_hook.get_pandas_df(query)
    
    # Basic Preprocessing (Date formatting usually required for Data Loader)
    # Salesforce expects yyyy-MM-dd'T'HH:mm:ss.SSS'Z' or simple yyyy-MM-dd depending on field
    # For this sample, we assume standard ISO format or rely on Data Loader format maps
    
    # Ensure Output Directory Exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Write to CSV
    # Data Loader typically expects comma separated, double quoted
    output_path = os.path.join(DATA_DIR, f"{TABLE_NAME}.csv")
    df.to_csv(output_path, index=False, quoting=csv.QUOTE_ALL)
    
    logging.info(f"Extracted {len(df)} records to {output_path}")

def audit_results(**context):
    """Check Data Loader logs for errors."""
    error_log_path = os.path.join(LOG_DIR, f"{TABLE_NAME}_error.csv")
    success_log_path = os.path.join(LOG_DIR, f"{TABLE_NAME}_success.csv")
    
    if not os.path.exists(error_log_path):
        logging.warning("Error log not found. Data Loader might not have run or generated output.")
        return

    # Check for errors (skip header)
    try:
        with open(error_log_path, 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                # We have errors
                error_count = len(lines) - 1
                raise ValueError(f"Data Loader found {error_count} errors! See {error_log_path}")
            else:
                logging.info("No errors found in error log.")
    except Exception as e:
        # If file is empty or other issue
        logging.warning(f"Could not read error log: {e}")

    # Log success count
    if os.path.exists(success_log_path):
        with open(success_log_path, 'r') as f:
            success_count = sum(1 for _ in f) - 1
            logging.info(f"Successfully loaded {success_count} records.")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

with DAG(
    DAG_ID,
    default_args=default_args,
    description="Sample ETL for KPS_T_SALES_MD using Data Loader",
    schedule=None,
    catchup=False,
    tags=["salesforce", "migration", "sample"],
) as dag:

    # 1. Generate Configurations (Ensure XML/SDL are up to date)
    generate_configs = BashOperator(
        task_id="generate_configs",
        bash_command=f"python {SALESFORCE_DIR}/generate_configs.py --table {TABLE_NAME}",
    )

    # 2. Extract from Oracle
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data_from_oracle,
    )

    # 3. Run Data Loader
    # Using the process.sh wrapper we created in Dockerfile
    # CLI Usage: process.sh <config_dir> <process_name>
    run_dataloader = BashOperator(
        task_id="run_dataloader",
        bash_command=f"/opt/dataloader/process.sh {CONFIG_DIR} {PROCESS_NAME}",
    )

    # 4. Audit Results
    audit_task = PythonOperator(
        task_id="audit_results",
        python_callable=audit_results,
    )

    # Dependency Chain
    generate_configs >> extract_task >> run_dataloader >> audit_task
