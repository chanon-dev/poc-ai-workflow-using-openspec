"""
Setup DAG: Centralized Salesforce Pipeline Setup

Trigger: Manual - Run after deploy or configuration changes

Pipeline Steps:
1. encrypt_credentials - Generate key and encrypt SF password
2. generate_master_config - Create process-conf.xml for all tables
3. generate_sdl_mappings - Create .sdl mapping files

This DAG creates all configuration files once. Execution DAGs
(like migrate_product_price) then read from these configs without
modifying them, preventing race conditions in parallel execution.
"""

import os
import subprocess
import json
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.models import Variable

# Constants
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
SALESFORCE_DIR = os.path.join(AIRFLOW_HOME, "salesforce")
KEY_FILE = os.path.join(SALESFORCE_DIR, "certs", "key.txt")
DATALOADER_JAR = "/opt/dataloader/dataloader-64.1.0.jar"


def encrypt_credentials(**context):
    """
    Task 1: Encrypt Salesforce credentials.

    Reads password and security_token from Airflow Variable: salesforce_config
    
    Steps:
    - Reads password and security_token from Variable
    - Generates encryption key
    - Encrypts password+token
    - Saves encrypted_password back to Variable
    """
    import json
    
    # Load config from Airflow Variable
    try:
        sf_config = json.loads(Variable.get("salesforce_config", default_var="{}"))
    except Exception as e:
        raise ValueError(f"Failed to load salesforce_config Variable: {e}")
    
    password = sf_config.get("password", "")
    security_token = sf_config.get("security_token", "")
    
    if not password:
        raise ValueError(
            "No password found in Airflow Variable 'salesforce_config'.\n"
            "Set it via Admin > Variables with JSON value:\n"
            '{"endpoint": "...", "username": "...", "password": "...", "security_token": "..."}'
        )

    # Combine password + security token for Salesforce API
    password_to_encrypt = password + security_token
    print(f"🔐 Password length: {len(password)}, Token length: {len(security_token)}")

    # Step 1: Generate encryption key
    print("🔑 Generating encryption key...")
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)

    key_cmd = [
        "java",
        "--enable-native-access=ALL-UNNAMED",
        "-cp", DATALOADER_JAR,
        "com.salesforce.dataloader.security.EncryptionUtil",
        "-k", KEY_FILE
    ]

    key_result = subprocess.run(key_cmd, capture_output=True, text=True)
    if key_result.returncode != 0:
        raise Exception(f"Key generation failed: {key_result.stderr}")
    print(f"✅ Key saved to {KEY_FILE}")

    # Step 2: Encrypt password
    print("🔒 Encrypting password...")
    enc_cmd = [
        "java",
        "--enable-native-access=ALL-UNNAMED",
        "-cp", DATALOADER_JAR,
        "com.salesforce.dataloader.security.EncryptionUtil",
        "-e", password_to_encrypt, KEY_FILE
    ]

    enc_result = subprocess.run(enc_cmd, capture_output=True, text=True)
    if enc_result.returncode != 0:
        raise Exception(f"Encryption failed: {enc_result.stderr}")

    encrypted_password = enc_result.stdout.strip().split("\n")[-1].strip()
    print(f"✅ Encrypted password: {encrypted_password[:20]}...")

    # Step 3: Save back to Variable
    sf_config["password"] = password
    sf_config["security_token"] = security_token
    sf_config["encrypted_password"] = encrypted_password
    Variable.set("salesforce_config", json.dumps(sf_config))
    print("💾 Saved encrypted_password to salesforce_config Variable")

    return encrypted_password


def verify_configs(**context):
    """Verify that configuration files were generated correctly."""
    config_dir = os.path.join(SALESFORCE_DIR, "dataloader_conf")
    mapping_dir = os.path.join(config_dir, "mappings")

    # Check process-conf.xml
    process_conf = os.path.join(config_dir, "process-conf.xml")
    if not os.path.exists(process_conf):
        raise FileNotFoundError(f"process-conf.xml not found at {process_conf}")

    # Count SDL files
    sdl_files = [f for f in os.listdir(mapping_dir) if f.endswith(".sdl")]
    print(f"Found {len(sdl_files)} SDL mapping files:")
    for sdl in sdl_files:
        print(f"  - {sdl}")

    # Check for Product2.sdl specifically
    if "Product2.sdl" not in sdl_files:
        raise FileNotFoundError("Product2.sdl not found in mappings directory")

    print("Configuration verification passed!")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "retries": 0,
}

with DAG(
    "setup_salesforce_pipeline",
    default_args=default_args,
    description="Centralized setup for Salesforce Data Loader pipeline",
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=["setup", "salesforce", "dataloader"],
) as dag:

    # Task 1: Encrypt credentials
    encrypt_task = PythonOperator(
        task_id="encrypt_credentials",
        python_callable=encrypt_credentials,
    )

    def run_generate_configs(**context):
        """Run generate_configs within Airflow context to access Variables."""
        import sys
        sys.path.insert(0, SALESFORCE_DIR)
        from generate_configs import generate_configs
        generate_configs()

    # Task 2: Generate master config (process-conf.xml + all SDL files)
    generate_config_task = PythonOperator(
        task_id="generate_master_config",
        python_callable=run_generate_configs,
    )

    # Task 3: Verify configs were generated
    verify_task = PythonOperator(
        task_id="verify_configs",
        python_callable=verify_configs,
    )

    # Pipeline flow
    encrypt_task >> generate_config_task >> verify_task
