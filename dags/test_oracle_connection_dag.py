"""
Oracle Connection Test DAG

Manual test DAG for verifying Oracle database connectivity.
REQ: openspec/changes/add-oracle-connection-test/specs/oracle-connectivity/spec.md
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Add plugins to path
sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from airflow.sdk import DAG, task

from config.tables_config import TABLES

# Default connection ID
ORACLE_CONN_ID = "oracle_kpc"

# Tables to verify (get from config)
TABLES_TO_VERIFY = [t.table_name for t in TABLES]


with DAG(
    dag_id="test_oracle_connection",
    description="Test Oracle database connectivity and table access",
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["test", "oracle", "connectivity"],
    default_args={
        "owner": "data-team",
    },
) as dag:

    @task()
    def check_connection() -> dict:
        """
        Verify Oracle database connectivity.

        Executes health check to verify:
        - Connection can be established
        - Credentials are valid
        - Network connectivity works
        """
        from oracle_service import OracleService

        service = OracleService(conn_id=ORACLE_CONN_ID)
        result = service.health_check()

        if result.healthy:
            print(f"Connection successful!")
            print(f"Oracle version: {result.version}")
        else:
            print(f"Connection failed: {result.error}")

        return {
            "healthy": result.healthy,
            "version": result.version,
            "error": result.error,
        }

    @task()
    def verify_tables(health_result: dict) -> dict:
        """
        Verify read access to migration tables.

        Checks SELECT permission on all configured migration tables.
        """
        from oracle_service import OracleService

        if not health_result.get("healthy"):
            print("Skipping table verification - connection is not healthy")
            return {
                "skipped": True,
                "reason": "Connection not healthy",
            }

        service = OracleService(conn_id=ORACLE_CONN_ID)
        results = service.verify_table_access(TABLES_TO_VERIFY)

        accessible_count = sum(1 for r in results.values() if r.accessible)
        total_count = len(results)

        print(f"Table access verification: {accessible_count}/{total_count} accessible")
        print("-" * 50)

        for table_name, result in results.items():
            status = "OK" if result.accessible else "FAILED"
            print(f"  {table_name}: {status}")
            if result.error:
                print(f"    Error: {result.error}")

        return {
            "total_tables": total_count,
            "accessible_tables": accessible_count,
            "results": {
                name: {"accessible": r.accessible, "error": r.error}
                for name, r in results.items()
            },
        }

    @task()
    def run_sample_query(health_result: dict) -> dict:
        """
        Run sample queries on a few tables to verify data retrieval.

        Selects first table from each priority level for testing.
        """
        from oracle_service import OracleService

        if not health_result.get("healthy"):
            print("Skipping sample query - connection is not healthy")
            return {
                "skipped": True,
                "reason": "Connection not healthy",
            }

        service = OracleService(conn_id=ORACLE_CONN_ID)

        # Get one table per priority for testing
        test_tables = []
        seen_priorities = set()
        for table in TABLES:
            if table.priority not in seen_priorities:
                test_tables.append(table.table_name)
                seen_priorities.add(table.priority)

        results = {}
        for table_name in test_tables:
            result = service.run_sample_query(table_name, limit=3)
            results[table_name] = result

            if result["success"]:
                print(f"Sample query on {table_name}:")
                print(f"  Total records: {result['total_count']:,}")
                print(f"  Columns: {len(result['columns'])}")
                print(f"  Sample rows retrieved: {result['sample_rows']}")
            else:
                print(f"Sample query on {table_name} failed:")
                print(f"  Error: {result['error']}")

            print("-" * 50)

        success_count = sum(1 for r in results.values() if r.get("success"))
        return {
            "tables_tested": len(test_tables),
            "successful": success_count,
            "results": results,
        }

    # DAG Flow
    health = check_connection()
    verify_tables(health)
    run_sample_query(health)
