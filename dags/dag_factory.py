"""
DAG Factory for KPC TMS Data Migration

Auto-generates migration DAGs for each table based on configuration.
Uses TaskFlow API for Airflow 3.x.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add plugins to path
sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from airflow.sdk import DAG, task

from config.extract_config import get_extract_config, get_staging_path
from config.field_mappings import get_field_mapping
from config.tables_config import TABLES, TableConfig


def create_migration_dag(table_config: TableConfig) -> DAG:
    """
    Create a migration DAG for a single table.

    Args:
        table_config: Table configuration

    Returns:
        Configured Airflow DAG
    """
    table_name = table_config.table_name
    extract_config = get_extract_config(table_name)
    field_mapping = get_field_mapping(table_name)

    default_args = {
        "owner": "data-team",
        "retries": 3,
        "retry_delay": timedelta(minutes=10),
        "email_on_failure": True,
    }

    dag = DAG(
        dag_id=f"migrate_{table_name.lower()}",
        default_args=default_args,
        description=f"Migrate {table_name} to Salesforce",
        schedule=None,  # Triggered by master DAG
        start_date=datetime(2024, 1, 1),
        catchup=False,
        max_active_tasks=extract_config.parallel_workers,
        tags=["migration", "kpc", table_config.priority],
    )

    with dag:

        @task()
        def get_record_count(
            start_date: str | None = None,
            end_date: str | None = None,
        ) -> dict:
            """Get total records to migrate."""
            from plugins.oracle_extractor import OracleExtractor
            from airflow.providers.oracle.hooks.oracle import OracleHook

            hook = OracleHook(oracle_conn_id="oracle_kpc")
            extractor = OracleExtractor(
                oracle_hook=hook,
                table_name=table_name,
                chunk_size=extract_config.chunk_size,
            )

            start = datetime.fromisoformat(start_date) if start_date else None
            end = datetime.fromisoformat(end_date) if end_date else None

            total = extractor.get_record_count(start, end)
            chunks = extractor.calculate_chunks(total)

            return {
                "total_records": total,
                "num_chunks": len(chunks),
                "chunks": [
                    {"chunk_id": c.chunk_id, "start": c.start_row, "end": c.end_row}
                    for c in chunks
                ],
            }

        @task()
        def extract_chunk(chunk_info: dict, **context) -> dict:
            """Extract a single chunk from Oracle."""
            from plugins.oracle_extractor import OracleExtractor, ChunkInfo
            from airflow.providers.oracle.hooks.oracle import OracleHook

            hook = OracleHook(oracle_conn_id="oracle_kpc")
            extractor = OracleExtractor(
                oracle_hook=hook,
                table_name=table_name,
                chunk_size=extract_config.chunk_size,
                use_parallel_hint=extract_config.use_parallel_hint,
                parallel_degree=extract_config.parallel_degree,
            )

            chunk = ChunkInfo(
                chunk_id=chunk_info["chunk_id"],
                start_row=chunk_info["start"],
                end_row=chunk_info["end"],
            )

            staging_path = get_staging_path(table_name, chunk.chunk_id)
            order_by = table_config.order_by or "ROWID"

            result = extractor.extract_chunk(
                chunk=chunk,
                order_by=order_by,
                staging_path=staging_path,
            )

            return {
                "chunk_id": result.chunk_id,
                "file_path": result.file_path,
                "record_count": result.record_count,
            }

        @task()
        def transform_chunk(extract_result: dict) -> dict:
            """Transform extracted data for Salesforce."""
            import gzip
            import pandas as pd
            from plugins.transformers import transform_for_salesforce

            file_path = extract_result["file_path"]

            # Read CSV (handle gzip)
            if file_path.endswith(".gz"):
                with gzip.open(file_path, "rt") as f:
                    df = pd.read_csv(f)
            else:
                df = pd.read_csv(file_path)

            # Transform
            if field_mapping:
                df = transform_for_salesforce(
                    df,
                    mappings=field_mapping.mappings,
                    transformations=field_mapping.transformations,
                )

            # Save back (overwrite)
            if file_path.endswith(".gz"):
                with gzip.open(file_path, "wt") as f:
                    df.to_csv(f, index=False)
            else:
                df.to_csv(file_path, index=False)

            return {
                "chunk_id": extract_result["chunk_id"],
                "file_path": file_path,
                "record_count": len(df),
            }

        @task()
        def load_chunk(transform_result: dict) -> dict:
            """Load chunk to Salesforce."""
            from plugins.salesforce_bulk_loader import SalesforceBulkLoader
            from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

            sf_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
            conn = sf_hook.get_conn()

            loader = SalesforceBulkLoader(
                instance_url=conn.sf_instance,
                access_token=conn.session_id,
            )

            if field_mapping:
                result = loader.load_file(
                    object_name=field_mapping.sf_object,
                    csv_file_path=transform_result["file_path"],
                    external_id_field=field_mapping.external_id,
                )

                return {
                    "chunk_id": transform_result["chunk_id"],
                    "job_id": result.job_id,
                    "state": result.state,
                    "records_processed": result.records_processed,
                    "records_failed": result.records_failed,
                }

            return {"error": "No field mapping found"}

        @task()
        def summarize_results(load_results: list[dict]) -> dict:
            """Summarize migration results."""
            total_processed = sum(r.get("records_processed", 0) for r in load_results)
            total_failed = sum(r.get("records_failed", 0) for r in load_results)

            return {
                "table": table_name,
                "total_chunks": len(load_results),
                "total_processed": total_processed,
                "total_failed": total_failed,
                "success_rate": (
                    total_processed / (total_processed + total_failed) * 100
                    if total_processed + total_failed > 0
                    else 0
                ),
            }

        # DAG Flow
        record_info = get_record_count()

        # Dynamic task mapping for parallel processing
        extract_results = extract_chunk.expand(
            chunk_info=record_info["chunks"]
        )
        transform_results = transform_chunk.expand(extract_result=extract_results)
        load_results = load_chunk.expand(transform_result=transform_results)

        summarize_results(load_results)

    return dag


# Auto-generate DAGs for all tables
for table in TABLES:
    dag_id = f"migrate_{table.table_name.lower()}"
    globals()[dag_id] = create_migration_dag(table)
