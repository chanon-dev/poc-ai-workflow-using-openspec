# dags/reconciliation.py

from datetime import datetime
from airflow.sdk import DAG, task
from airflow.providers.salesforce.hooks.salesforce import SalesforceHook
from airflow.providers.oracle.hooks.oracle import OracleHook
from plugins.reconciliation_checks import ReconciliationChecks

DEFAULT_ARGS = {
    "owner": "data-team",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    "reconciliation_daily",
    default_args=DEFAULT_ARGS,
    schedule="@daily",
    catchup=False,
    tags=["reconciliation", "maintenance"]
) as dag:

    @task()
    def check_sales_counts():
        source_hook = OracleHook(oracle_conn_id="oracle_kpc")
        target_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
        
        # Oracle Count
        source_count = source_hook.get_first("SELECT COUNT(*) FROM KPS_T_SALES_MD")[0]
        
        # Salesforce Count
        conn = target_hook.get_conn()
        res = conn.query("SELECT COUNT(Id) FROM KPS_Sales__c")
        target_count = res["totalSize"]
        
        # Simple comparison for automated alert
        # In a real scenario, we'd query the audit log to know how many failed
        print(f"Oracle: {source_count}, Salesforce: {target_count}")
        
        if source_count != target_count:
            # This might be expected if some records failed permanently
            print("WARNING: Count mismatch!")
            return "MISMATCH"
        
        return "MATCH"

    check_sales_counts()
