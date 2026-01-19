"""
Oracle Connection Service (Thin Mode)

Provides reusable Oracle connection management using oracledb in thin mode.
No Oracle Instant Client required.
REQ: openspec/changes/add-oracle-connection-test/specs/oracle-connectivity/spec.md
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Generator

import oracledb

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30  # seconds


@dataclass
class HealthCheckResult:
    """Result of a health check operation."""

    healthy: bool
    version: str | None = None
    error: str | None = None


@dataclass
class TableAccessResult:
    """Result of table access verification."""

    table_name: str
    accessible: bool
    error: str | None = None


def _get_connection_params(conn_id: str) -> dict[str, Any]:
    """
    Get connection parameters from Airflow Connection.

    Args:
        conn_id: Airflow connection ID

    Returns:
        Dict with user, password, dsn
    """
    from airflow.hooks.base import BaseHook

    conn = BaseHook.get_connection(conn_id)

    # Build DSN: host:port/service_name
    host = conn.host or "localhost"
    port = conn.port or 1521
    service_name = conn.schema or conn.extra_dejson.get("service_name", "ORCL")

    dsn = f"{host}:{port}/{service_name}"

    return {
        "user": conn.login,
        "password": conn.password,
        "dsn": dsn,
    }


class OracleService:
    """
    Oracle connection service using oracledb thin mode.

    Thin mode does not require Oracle Instant Client installation.
    Retrieves credentials from Airflow Connections (not hardcoded).
    Provides health check and table access verification capabilities.
    """

    def __init__(
        self,
        conn_id: str = "oracle_kpc",
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Initialize Oracle service.

        Args:
            conn_id: Airflow connection ID for Oracle database
            timeout: Connection timeout in seconds (default: 30)
        """
        self.conn_id = conn_id
        self.timeout = timeout

    @contextmanager
    def _get_connection(self) -> Generator[oracledb.Connection, None, None]:
        """Get oracledb connection (thin mode)."""
        params = _get_connection_params(self.conn_id)
        conn = oracledb.connect(
            user=params["user"],
            password=params["password"],
            dsn=params["dsn"],
            tcp_connect_timeout=self.timeout,
        )
        try:
            yield conn
        finally:
            conn.close()

    def health_check(self) -> HealthCheckResult:
        """
        Verify Oracle connectivity by executing a simple query.

        Returns:
            HealthCheckResult with healthy status and version info or error details.
            Does not raise exceptions - returns graceful failure.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Execute SELECT 1 FROM DUAL to verify connection
                cursor.execute("SELECT 1 FROM DUAL")
                result = cursor.fetchone()
                if result is None or result[0] != 1:
                    return HealthCheckResult(
                        healthy=False,
                        error="Unexpected result from health check query",
                    )

                # Get Oracle version
                cursor.execute(
                    "SELECT banner FROM v$version WHERE banner LIKE 'Oracle%' AND ROWNUM = 1"
                )
                version_result = cursor.fetchone()
                version = version_result[0] if version_result else "Unknown"

                logger.info(f"Oracle health check passed. Version: {version}")
                return HealthCheckResult(healthy=True, version=version)

        except Exception as e:
            error_msg = f"Connection to '{self.conn_id}' failed (timeout={self.timeout}s): {e}"
            logger.error(error_msg)
            return HealthCheckResult(healthy=False, error=error_msg)

    def verify_table_access(
        self,
        table_names: list[str],
    ) -> dict[str, TableAccessResult]:
        """
        Verify read permissions on specified tables.

        Args:
            table_names: List of table names to verify access

        Returns:
            Dict mapping table_name to TableAccessResult with accessibility status.
        """
        results: dict[str, TableAccessResult] = {}

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                for table_name in table_names:
                    try:
                        # Try to select from the table (limit to 1 row for efficiency)
                        cursor.execute(
                            f"SELECT * FROM {table_name} WHERE ROWNUM = 1"  # noqa: S608
                        )
                        cursor.fetchone()
                        results[table_name] = TableAccessResult(
                            table_name=table_name,
                            accessible=True,
                        )
                        logger.info(f"Table '{table_name}' is accessible")

                    except Exception as e:
                        error_msg = str(e)
                        results[table_name] = TableAccessResult(
                            table_name=table_name,
                            accessible=False,
                            error=error_msg,
                        )
                        logger.warning(f"Table '{table_name}' is not accessible: {error_msg}")

        except Exception as e:
            # Connection-level failure
            error_msg = f"Failed to connect for table access verification: {e}"
            logger.error(error_msg)
            for table_name in table_names:
                results[table_name] = TableAccessResult(
                    table_name=table_name,
                    accessible=False,
                    error=error_msg,
                )

        return results

    def run_sample_query(
        self,
        table_name: str,
        limit: int = 5,
    ) -> dict[str, Any]:
        """
        Run a sample query on a table to verify data retrieval.

        Args:
            table_name: Table name to query
            limit: Maximum number of rows to return (default: 5)

        Returns:
            Dict with columns, row_count, and sample_data or error details.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Get column names
                cursor.execute(
                    """
                    SELECT column_name
                    FROM all_tab_columns
                    WHERE table_name = :table_name
                    ORDER BY column_id
                    """,
                    {"table_name": table_name.upper()},
                )
                columns_result = cursor.fetchall()
                columns = [row[0] for row in columns_result] if columns_result else []

                # Get sample data
                cursor.execute(
                    f"SELECT * FROM {table_name} WHERE ROWNUM <= :limit",  # noqa: S608
                    {"limit": limit},
                )
                sample_data = cursor.fetchall()

                # Get total count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")  # noqa: S608
                count_result = cursor.fetchone()
                total_count = count_result[0] if count_result else 0

                return {
                    "success": True,
                    "table_name": table_name,
                    "columns": columns,
                    "total_count": total_count,
                    "sample_rows": len(sample_data) if sample_data else 0,
                    "sample_data": sample_data[:limit] if sample_data else [],
                }

        except Exception as e:
            error_msg = f"Failed to run sample query on '{table_name}': {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "table_name": table_name,
                "error": error_msg,
            }
