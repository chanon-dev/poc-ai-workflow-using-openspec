"""
Utility DAG: Salesforce Migration Setup Pipeline
Usage: Trigger this DAG with config {"password": "your_password_here"}

Pipeline Steps:
1. Encrypt & Save - Encrypt password and save to Airflow Variables
2. Generate Config - Regenerate Data Loader configuration files
3. Run Migration - Execute the migration DAG
"""

import os
import subprocess
import json
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable


# ============================================================================
# Step 1: Encrypt Password
# ============================================================================
KEY_FILE = "/opt/airflow/salesforce/certs/key.txt"

def encrypt_password_task(**context):
    """Generate encryption key and encrypt password."""
    # Try to get password from DAG run config first, then from Variable
    dag_run = context.get("dag_run")
    password = dag_run.conf.get("password", "") if dag_run and dag_run.conf else ""
    
    # If not in config, try to get from Airflow Variable
    if not password:
        try:
            sf_config = json.loads(Variable.get("salesforce_config", default_var="{}"))
            password = sf_config.get("password", "")
            security_token = sf_config.get("security_token", "")
        except:
             pass
            
    # Keep track of raw password for saving back to variables
    raw_password = password
    
    # Prepare password for encryption (append token if available)
    password_to_encrypt = password
    
    # If not in config, try to get from Airflow Variable logic was handled above
    # Now check if we need to append security token
    if security_token and not password.endswith(security_token):
         print(f"📖 Appending security token to password for encryption")
         password_to_encrypt = password + security_token
    elif security_token and password.endswith(security_token):
         print(f"⚠️ Password seems to already contain security token, using as is")
         password_to_encrypt = password
         # In this case, raw_password likely already has token, which is not ideal but safe for encryption
    
    if not raw_password:
        print("=" * 60)
        print("❌ ERROR: No password found!")
        print("")
        print("Options to provide password:")
        print("1. Trigger with config: {\"password\": \"your_password\"}")
        print("2. Set 'password' in Airflow Variable 'salesforce_config'")
        print("=" * 60)
        raise ValueError("No password provided")
    
    # Step 1: Generate encryption key
    print("🔑 Step 1: Generating encryption key...")
    key_cmd = [
        "java",
        "--enable-native-access=ALL-UNNAMED",
        "-cp",
        "/opt/dataloader/dataloader-64.1.0.jar",
        "com.salesforce.dataloader.security.EncryptionUtil",
        "-k",
        KEY_FILE
    ]
    
    key_result = subprocess.run(key_cmd, capture_output=True, text=True)
    if key_result.returncode != 0:
        raise Exception(f"Key generation failed: {key_result.stderr}")
    print(f"✅ Key saved to {KEY_FILE}")
    
    # Step 2: Encrypt password with the key
    print("🔐 Step 2: Encrypting password with key...")
    enc_cmd = [
        "java",
        "--enable-native-access=ALL-UNNAMED",
        "-cp",
        "/opt/dataloader/dataloader-64.1.0.jar",
        "com.salesforce.dataloader.security.EncryptionUtil",
        "-e",
        password_to_encrypt,
        KEY_FILE
    ]
    
    enc_result = subprocess.run(enc_cmd, capture_output=True, text=True)
    if enc_result.returncode != 0:
        raise Exception(f"Encryption failed: {enc_result.stderr}")
    
    output = enc_result.stdout.strip()
    encrypted_password = output.split("\n")[-1].strip()
    print(f"✅ Encrypted: {encrypted_password}")
    
    # Push to XCom for next task
    context["ti"].xcom_push(key="encrypted_password", value=encrypted_password)
    context["ti"].xcom_push(key="plain_password", value=raw_password)
    return encrypted_password


def save_to_variables_task(**context):
    """Save encrypted password to Airflow Variables."""
    ti = context["ti"]
    encrypted_password = ti.xcom_pull(task_ids="step1_encrypt.encrypt_password", key="encrypted_password")
    plain_password = ti.xcom_pull(task_ids="step1_encrypt.encrypt_password", key="plain_password")
    
    print("💾 Saving to Airflow Variables...")
    
    try:
        sf_config = json.loads(Variable.get("salesforce_config", default_var="{}"))
    except:
        sf_config = {}
    
    sf_config["password"] = plain_password  # Keep original plain text password (without token appended if possible)
    sf_config["encrypted_password"] = encrypted_password
    
    Variable.set("salesforce_config", json.dumps(sf_config))
    
    print("✅ Saved to salesforce_config Variable:")
    print(json.dumps(sf_config, indent=2))


# ============================================================================
# DAG Definition
# ============================================================================
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    "utility_encrypt_password",
    default_args=default_args,
    description="Salesforce Migration Setup Pipeline",
    schedule=None,
    catchup=False,
    tags=["utility", "salesforce", "pipeline"],
) as dag:
    
    # ========================================================================
    # Step 1: Encrypt & Save Password
    # ========================================================================
    with TaskGroup(group_id="step1_encrypt", tooltip="Encrypt password") as step1:
        encrypt = PythonOperator(
            task_id="encrypt_password",
            python_callable=encrypt_password_task,
        )
        
        save = PythonOperator(
            task_id="save_to_variables",
            python_callable=save_to_variables_task,
        )
        
        encrypt >> save
    
    # ========================================================================
    # Step 2: Generate Data Loader Config
    # ========================================================================
    with TaskGroup(group_id="step2_generate_config", tooltip="Generate config files") as step2:
        generate_config = BashOperator(
            task_id="generate_dataloader_config",
            bash_command="python /opt/airflow/salesforce/generate_configs.py --table KPS_T_SALES_MD",
        )
    
    # ========================================================================
    # Step 3: Trigger Migration DAG
    # ========================================================================
    with TaskGroup(group_id="step3_run_migration", tooltip="Run migration") as step3:
        trigger_migration = TriggerDagRunOperator(
            task_id="trigger_migration_dag",
            trigger_dag_id="migrate_sample_kps_t_sales_md",
            wait_for_completion=False,
        )
    
    # ========================================================================
    # Pipeline Flow
    # ========================================================================
    step1 >> step2 >> step3
