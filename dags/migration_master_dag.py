"""
KPC TMS Data Migration - Master DAG

Orchestrates the complete migration pipeline across all tables.
Triggers table-specific DAGs in the correct order based on dependencies.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "email_on_failure": True,
    "email": ["data-team@company.com"],
}

with DAG(
    dag_id="kpc_migration_master",
    default_args=default_args,
    description="Master orchestration for KPC TMS data migration",
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["migration", "kpc", "master"],
    max_active_runs=1,
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # Phase 1: Reference Data (parallel - no dependencies)
    phase1_tables = [
        "kps_r_email_supplier",
        "kps_r_email_tenant",
        "kps_r_pos_supplier",
    ]
    phase1_triggers = []
    for table in phase1_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"trigger_{table}",
            trigger_dag_id=f"migrate_{table}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase1_triggers.append(trigger)

    phase1_complete = EmptyOperator(task_id="phase1_complete")

    # Phase 2: Pre-Invoice tables (parallel)
    phase2_tables = [
        "kps_t_preinv",
        "kps_t_preinv_min",
        "kps_t_preinv_revgua",
    ]
    phase2_triggers = []
    for table in phase2_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"trigger_{table}",
            trigger_dag_id=f"migrate_{table}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase2_triggers.append(trigger)

    phase2_complete = EmptyOperator(task_id="phase2_complete")

    # Phase 3: Pre-Invoice Details (depends on Phase 2)
    phase3_tables = [
        "kps_t_preinv_detail",
        "kps_t_preinv_revsales_d",
        "kps_t_preinv_revsales_m",
    ]
    phase3_triggers = []
    for table in phase3_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"trigger_{table}",
            trigger_dag_id=f"migrate_{table}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase3_triggers.append(trigger)

    phase3_complete = EmptyOperator(task_id="phase3_complete")

    # Phase 4: Main Sales Master (sequential - largest table)
    trigger_sales_m = TriggerDagRunOperator(
        task_id="trigger_kps_t_sales_m",
        trigger_dag_id="migrate_kps_t_sales_m",
        wait_for_completion=True,
        poke_interval=60,
    )

    # Phase 5: Sales Details (sequential - largest table)
    trigger_sales_md = TriggerDagRunOperator(
        task_id="trigger_kps_t_sales_md",
        trigger_dag_id="migrate_kps_t_sales_md",
        wait_for_completion=True,
        poke_interval=60,
    )

    # Phase 6: Sales Payment (sequential)
    trigger_salespay_md = TriggerDagRunOperator(
        task_id="trigger_kps_t_salespay_md",
        trigger_dag_id="migrate_kps_t_salespay_md",
        wait_for_completion=True,
        poke_interval=60,
    )

    # Phase 7: Supporting tables (parallel)
    phase7_tables = [
        "kps_t_sales_apprv",
        "kps_t_sales_apprv_detail",
        "kps_t_salesbank_md",
        "kps_web_sales",
    ]
    phase7_triggers = []
    for table in phase7_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"trigger_{table}",
            trigger_dag_id=f"migrate_{table}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase7_triggers.append(trigger)

    # Phase 8: Reconciliation
    trigger_reconciliation = TriggerDagRunOperator(
        task_id="trigger_reconciliation",
        trigger_dag_id="reconciliation",
        wait_for_completion=True,
        poke_interval=60,
    )

    # Define task dependencies
    start >> phase1_triggers >> phase1_complete
    phase1_complete >> phase2_triggers >> phase2_complete
    phase2_complete >> phase3_triggers >> phase3_complete
    phase3_complete >> trigger_sales_m >> trigger_sales_md >> trigger_salespay_md
    trigger_salespay_md >> phase7_triggers
    phase7_triggers >> trigger_reconciliation >> end
