"""
Data Reconciliation DAG

Runs validation checks between Oracle and Salesforce after migration.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add plugins to path
sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from airflow.sdk import DAG, task

from config.tables_config import TABLES
from config.field_mappings import get_field_mapping

default_args = {
    "owner": "data-team",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}

with DAG(
    dag_id="reconciliation",
    default_args=default_args,
    description="Data reconciliation between Oracle and Salesforce",
    schedule=None,  # Triggered by master DAG
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["reconciliation", "kpc"],
) as dag:

    @task()
    def reconcile_table(table_name: str, sf_object: str, key_column: str) -> dict:
        """Run reconciliation for a single table."""
        from airflow.providers.oracle.hooks.oracle import OracleHook
        from airflow.providers.salesforce.hooks.salesforce import SalesforceHook
        from plugins.reconciliation import DataReconciliation

        oracle_hook = OracleHook(oracle_conn_id="oracle_kpc")
        sf_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")

        reconciler = DataReconciliation(oracle_hook, sf_hook)
        report = reconciler.generate_report(
            oracle_table=table_name,
            sf_object=sf_object,
            key_column=key_column,
        )

        return {
            "table": report.table_name,
            "sf_object": report.sf_object,
            "overall_status": report.overall_status,
            "checks": {
                name: {"status": check.status, "details": check.details}
                for name, check in report.checks.items()
            },
        }

    @task()
    def generate_summary(results: list[dict]) -> dict:
        """Generate reconciliation summary."""
        passed = sum(1 for r in results if r["overall_status"] == "PASS")
        failed = sum(1 for r in results if r["overall_status"] == "FAIL")

        failed_tables = [r["table"] for r in results if r["overall_status"] == "FAIL"]

        return {
            "total_tables": len(results),
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / len(results) * 100) if results else 0,
            "failed_tables": failed_tables,
            "overall_status": "PASS" if failed == 0 else "FAIL",
        }

    @task()
    def alert_on_failure(summary: dict) -> None:
        """Send alert if reconciliation failed."""
        if summary["overall_status"] == "FAIL":
            message = (
                f"⚠️ Reconciliation FAILED\n"
                f"Failed tables: {', '.join(summary['failed_tables'])}\n"
                f"Pass rate: {summary['success_rate']:.1f}%"
            )
            # In production, send to Slack/Email
            print(message)

    # Build reconciliation tasks
    table_configs = []
    for table in TABLES:
        mapping = get_field_mapping(table.table_name)
        if mapping:
            table_configs.append({
                "table_name": table.table_name,
                "sf_object": mapping.sf_object,
                "key_column": table.order_by or "ROWID",
            })

    # Run reconciliation for all tables
    results = reconcile_table.expand_kwargs(table_configs)

    # Summarize and alert
    summary = generate_summary(results)
    alert_on_failure(summary)
