# dags/dag_factory.py
"""
DAG Factory - Auto-generate DAGs from configuration
สร้าง DAGs อัตโนมัติจาก tables_config.py

Benefits:
- DRY: No code duplication
- Config-driven: Change config, not code
- Consistent: All DAGs have same structure
- Scalable: Add 100 tables by adding config only
"""

from datetime import datetime, timedelta
from airflow.sdk import DAG, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.trigger_rule import TriggerRule

# Import table configurations
from config.tables_config import TABLES_CONFIG, FIELD_MAPPINGS, get_tables_by_priority

# ==================== Default Arguments ====================
DEFAULT_ARGS = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["data-team@company.com"],
    "execution_timeout": timedelta(hours=12),
}


# ==================== DAG Factory Function ====================
def create_migration_dag(table_name: str, config: dict) -> DAG:
    """
    Factory function to create a migration DAG for a single table.

    Args:
        table_name: Oracle table name (e.g., "KPS_T_SALES_MD")
        config: Configuration dict from TABLES_CONFIG

    Returns:
        Configured DAG object
    """

    dag_id = f"migrate_{table_name.lower()}"

    # Determine DAG type based on size
    is_chunked = config.get("chunk_size") is not None

    dag = DAG(
        dag_id=dag_id,
        default_args=DEFAULT_ARGS,
        description=f"Migrate {table_name} to {config['sf_object']}",
        schedule=config.get("schedule"),
        start_date=datetime(2024, 1, 1),
        catchup=False,
        max_active_runs=1,
        max_active_tasks=config.get("parallel_extract", 4),
        tags=["migration", config["size_category"]] + config.get("tags", []),
        doc_md=f"""
        ## {table_name} Migration DAG

        | Property | Value |
        |----------|-------|
        | SF Object | `{config['sf_object']}` |
        | External ID | `{config['external_id']}` |
        | Estimated Records | {config['estimated_records']:,} |
        | Size Category | {config['size_category']} |
        | Chunked | {'Yes' if is_chunked else 'No'} |
        | Dependencies | {config.get('dependencies', [])} |
        """,
    )

    with dag:
        # ==================== Tasks ====================

        @task()
        def start_migration(**context):
            """Log migration start and validate prerequisites"""
            print(f"Starting migration for {table_name}")
            print(f"Run ID: {context['run_id']}")
            print(f"Estimated records: {config['estimated_records']:,}")
            return {
                "table_name": table_name,
                "start_time": datetime.now().isoformat(),
            }

        @task()
        def validate_source(**context):
            """Validate source data exists and is accessible"""
            from airflow.providers.oracle.hooks.oracle import OracleHook

            hook = OracleHook(oracle_conn_id="oracle_kpc")

            # Count records
            count = hook.get_first(f"SELECT COUNT(*) FROM {table_name}")[0]

            if count == 0:
                raise ValueError(f"No records found in {table_name}")

            print(f"Source count: {count:,}")

            return {
                "source_count": count,
                "validated_at": datetime.now().isoformat(),
            }

        if is_chunked:
            # ==================== Chunked Migration (Large Tables) ====================

            @task()
            def calculate_chunks(source_info: dict) -> list:
                """Calculate chunk ranges for parallel extraction"""
                total = source_info["source_count"]
                chunk_size = config["chunk_size"]
                num_chunks = (total // chunk_size) + 1

                chunks = []
                for i in range(num_chunks):
                    chunks.append({
                        "chunk_id": i,
                        "start_row": i * chunk_size + 1,
                        "end_row": (i + 1) * chunk_size,
                    })

                print(f"Created {len(chunks)} chunks of {chunk_size:,} records each")
                return chunks

            @task(max_active_tis_per_dag=config.get("parallel_extract", 4))
            def extract_chunk(chunk: dict, source_info: dict) -> dict:
                """Extract a single chunk from Oracle"""
                from airflow.providers.oracle.hooks.oracle import OracleHook
                import pandas as pd
                import os

                hook = OracleHook(oracle_conn_id="oracle_kpc")

                from include.sql.queries import generate_extract_query

                hook = OracleHook(oracle_conn_id="oracle_kpc")

                sql = generate_extract_query(table_name, config)

                df = hook.get_pandas_df(sql, parameters={
                    "start_row": chunk["start_row"],
                    "end_row": chunk["end_row"],
                })

                # Remove row number column
                if "rn" in df.columns:
                    df = df.drop(columns=["rn"])

                # Apply field mapping
                field_map = FIELD_MAPPINGS.get(table_name, {})
                if field_map:
                    df = df.rename(columns=field_map)

                # Save to staging
                staging_path = f"/data/staging/{table_name.lower()}"
                os.makedirs(staging_path, exist_ok=True)
                output_file = f"{staging_path}/chunk_{chunk['chunk_id']:05d}.csv"
                df.to_csv(output_file, index=False)

                return {
                    "chunk_id": chunk["chunk_id"],
                    "file_path": output_file,
                    "record_count": len(df),
                }

            @task()
            def load_chunks_to_salesforce(extract_results: list) -> dict:
                """Load all chunks to Salesforce using Bulk API"""
                # Import here to avoid top-level import
                from plugins.salesforce_bulk_loader import SalesforceBulkLoader
                from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

                sf_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
                sf = sf_hook.get_conn()

                loader = SalesforceBulkLoader(
                    instance_url=sf.sf_instance,
                    access_token=sf.session_id
                )

                csv_files = [r["file_path"] for r in extract_results]

                results = loader.load_files_parallel(
                    object_name=config["sf_object"],
                    csv_files=csv_files,
                    external_id=config["external_id"],
                    max_workers=config.get("parallel_load", 15)
                )

                total_success = sum(r.get("records_processed", 0) for r in results)
                total_failed = sum(r.get("records_failed", 0) for r in results)

                return {
                    "total_success": total_success,
                    "total_failed": total_failed,
                    "success_rate": total_success / (total_success + total_failed) * 100 if (total_success + total_failed) > 0 else 0,
                }

            # Chunked DAG flow
            start = start_migration()
            source = validate_source()
            chunks = calculate_chunks(source)
            extracted = extract_chunk.expand(chunk=chunks, source_info=[source] * 1000)
            loaded = load_chunks_to_salesforce(extracted)

        else:
            # ==================== Single Batch Migration (Small Tables) ====================

            @task()
            def extract_all(source_info: dict) -> dict:
                """Extract entire table in single batch"""
                from airflow.providers.oracle.hooks.oracle import OracleHook
                import pandas as pd
                import os

                hook = OracleHook(oracle_conn_id="oracle_kpc")

                df = hook.get_pandas_df(f"SELECT * FROM {table_name}")

                # Apply field mapping
                field_map = FIELD_MAPPINGS.get(table_name, {})
                if field_map:
                    df = df.rename(columns=field_map)

                # Save to staging
                staging_path = f"/data/staging/{table_name.lower()}"
                os.makedirs(staging_path, exist_ok=True)
                output_file = f"{staging_path}/full_extract.csv"
                df.to_csv(output_file, index=False)

                return {
                    "file_path": output_file,
                    "record_count": len(df),
                }

            @task()
            def load_to_salesforce(extract_result: dict) -> dict:
                """Load data to Salesforce"""
                from plugins.salesforce_bulk_loader import SalesforceBulkLoader
                from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

                sf_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
                sf = sf_hook.get_conn()

                loader = SalesforceBulkLoader(
                    instance_url=sf.sf_instance,
                    access_token=sf.session_id
                )

                result = loader.load_files_parallel(
                    object_name=config["sf_object"],
                    csv_files=[extract_result["file_path"]],
                    external_id=config["external_id"],
                    max_workers=1
                )[0]

                return {
                    "total_success": result.get("records_processed", 0),
                    "total_failed": result.get("records_failed", 0),
                }

            # Single batch DAG flow
            start = start_migration()
            source = validate_source()
            extracted = extract_all(source)
            loaded = load_to_salesforce(extracted)

        # ==================== Common Tasks ====================

        @task()
        def reconcile(load_result: dict, source_info: dict) -> dict:
            """Reconcile source vs target counts"""
            from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

            sf_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
            sf = sf_hook.get_conn()

            # Get SF count
            result = sf.query(f"SELECT COUNT(Id) FROM {config['sf_object']}")
            sf_count = result["totalSize"]

            source_count = source_info["source_count"]
            difference = source_count - sf_count

            return {
                "source_count": source_count,
                "sf_count": sf_count,
                "difference": difference,
                "match": difference == 0,
                "match_rate": sf_count / source_count * 100 if source_count > 0 else 0,
            }

        @task()
        def log_audit(start_info: dict, source_info: dict, load_result: dict, reconcile_result: dict):
            """Log migration results to audit table"""
            from airflow.providers.oracle.hooks.oracle import OracleHook

            hook = OracleHook(oracle_conn_id="oracle_kpc")

            hook.run("""
                INSERT INTO MIGRATION_AUDIT_LOG
                (BATCH_ID, TABLE_NAME, SOURCE_COUNT, SUCCESS_COUNT, FAILED_COUNT,
                 STATUS, START_TIME, END_TIME, DURATION_SECONDS)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
            """, parameters=[
                start_info["start_time"],
                table_name,
                source_info["source_count"],
                load_result.get("total_success", 0),
                load_result.get("total_failed", 0),
                "SUCCESS" if reconcile_result["match"] else "PARTIAL",
                start_info["start_time"],
                datetime.now().isoformat(),
                0,  # Calculate duration
            ])

        @task()
        def cleanup(load_result: dict):
            """Clean up staging files"""
            import shutil
            staging_path = f"/data/staging/{table_name.lower()}"
            if load_result.get("total_failed", 0) == 0:
                shutil.rmtree(staging_path, ignore_errors=True)
                print(f"Cleaned up {staging_path}")
            else:
                print(f"Keeping staging files due to failures: {staging_path}")

        # Common flow
        reconciled = reconcile(loaded, source)
        audit = log_audit(start, source, loaded, reconciled)
        clean = cleanup(loaded)

        start >> source
        reconciled >> audit >> clean

    return dag


# ==================== Generate All DAGs ====================

# Generate a DAG for each table in config
for table_name, config in TABLES_CONFIG.items():
    dag = create_migration_dag(table_name, config)
    # Register DAG in global namespace so Airflow can find it
    globals()[f"migrate_{table_name.lower()}"] = dag


# ==================== Master Orchestration DAG ====================

with DAG(
    dag_id="migration_master",
    default_args=DEFAULT_ARGS,
    description="Master DAG to orchestrate all table migrations",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["migration", "master", "orchestration"],
    doc_md="""
    ## Migration Master DAG

    Orchestrates migration of all 34 tables in correct order based on:
    1. Priority (reference data first, then transactions)
    2. Dependencies (parent tables before child tables)

    ### Execution Order

    | Priority | Tables |
    |----------|--------|
    | 0 | Reference/Master data |
    | 1-3 | Critical large tables |
    | 4-5 | Medium tables |
    | 6-8 | Small tables |
    """,
) as master_dag:

    @task()
    def start_orchestration():
        """Start master orchestration"""
        from config.tables_config import get_total_estimated_records
        total = get_total_estimated_records()
        print(f"Starting migration of {len(TABLES_CONFIG)} tables")
        print(f"Total estimated records: {total:,}")
        return {"start_time": datetime.now().isoformat()}

    @task()
    def send_completion_notification(results: list):
        """Send Slack/Email notification on completion"""
        # Implement notification logic
        print(f"Migration complete. Results: {results}")

    start = start_orchestration()

    # Create triggers for each priority group
    priority_groups = get_tables_by_priority()
    previous_triggers = [start]

    for priority, tables in sorted(priority_groups.items()):
        current_triggers = []

        for table_name in tables:
            config = TABLES_CONFIG[table_name]

            # Add dependency sensors if needed
            sensors = []
            for dep in config.get("dependencies", []):
                sensor = ExternalTaskSensor(
                    task_id=f"wait_for_{dep.lower()}_in_{table_name.lower()}",
                    external_dag_id=f"migrate_{dep.lower()}",
                    external_task_id=None,
                    mode="reschedule",
                    timeout=3600 * 24,
                    poke_interval=60,
                )
                sensors.append(sensor)

            trigger = TriggerDagRunOperator(
                task_id=f"trigger_{table_name.lower()}",
                trigger_dag_id=f"migrate_{table_name.lower()}",
                wait_for_completion=True,
                poke_interval=60,
                trigger_rule=TriggerRule.ALL_SUCCESS,
            )

            # Connect sensors to trigger
            for sensor in sensors:
                for prev in previous_triggers:
                    prev >> sensor
                sensor >> trigger

            # If no sensors, connect directly
            if not sensors:
                for prev in previous_triggers:
                    prev >> trigger

            current_triggers.append(trigger)

        previous_triggers = current_triggers

    # Final notification
    notify = send_completion_notification(previous_triggers)
    for trigger in previous_triggers:
        trigger >> notify

# Register master DAG
globals()["migration_master"] = master_dag
