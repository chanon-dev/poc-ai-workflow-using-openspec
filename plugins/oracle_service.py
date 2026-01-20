"""
Oracle Connection Service

Provides reusable Oracle connection management using oracledb.
Supports both thin mode (no dependencies) and thick mode (requires Oracle Instant Client).
REQ: openspec/changes/add-oracle-connection-test/specs/oracle-connectivity/spec.md
"""

from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, ClassVar, Generator

import oracledb

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_INSTANT_CLIENT_PATH = "/opt/oracle/instantclient"


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


class OracleService:
    """
    Oracle connection service using oracledb.

    Features:
    - Lazy initialization of Oracle Client (only when first connection is made)
    - Supports thick mode (with Oracle Instant Client) and thin mode fallback
    - Retrieves credentials from Airflow Connections (not hardcoded)
    - Provides health check and table access verification capabilities
    - Thread-safe client initialization

    Usage:
        service = OracleService(conn_id="oracle_kpc")
        result = service.health_check()
        if result.healthy:
            print(f"Connected to Oracle: {result.version}")
    """

    # Class-level state for Oracle Client initialization
    _client_initialized: ClassVar[bool] = False
    _client_init_lock: ClassVar[threading.Lock] = threading.Lock()
    _thick_mode_enabled: ClassVar[bool] = False

    def __init__(
        self,
        conn_id: str = "oracle_kpc",
        timeout: int = DEFAULT_TIMEOUT,
        instant_client_path: str = DEFAULT_INSTANT_CLIENT_PATH,
    ):
        """
        Initialize Oracle service.

        Args:
            conn_id: Airflow connection ID for Oracle database
            timeout: Connection timeout in seconds (default: 30)
            instant_client_path: Path to Oracle Instant Client (default: /opt/oracle/instantclient)
        """
        self.conn_id = conn_id
        self.timeout = timeout
        self.instant_client_path = instant_client_path

    @classmethod
    def _ensure_client_initialized(cls, instant_client_path: str) -> None:
        """
        Initialize Oracle Client for thick mode (lazy, thread-safe).

        This method is called automatically before the first connection.
        It only runs once per process, regardless of how many OracleService instances exist.

        Args:
            instant_client_path: Path to Oracle Instant Client libraries
        """
        if cls._client_initialized:
            return

        with cls._client_init_lock:
            # Double-check after acquiring lock
            if cls._client_initialized:
                return

            try:
                oracledb.init_oracle_client(lib_dir=instant_client_path)
                cls._thick_mode_enabled = True
                logger.info(
                    f"Oracle Client initialized (thick mode) from: {instant_client_path}"
                )
            except Exception as e:
                cls._thick_mode_enabled = False
                logger.warning(
                    f"Failed to initialize Oracle Client: {e}. Using thin mode."
                )

            cls._client_initialized = True

    @classmethod
    def is_thick_mode(cls) -> bool:
        """Check if thick mode is enabled."""
        return cls._thick_mode_enabled

    @classmethod
    def reset_client(cls) -> None:
        """
        Reset client initialization state (for testing purposes only).

        Warning: This should only be used in tests. In production,
        Oracle Client can only be initialized once per process.
        """
        with cls._client_init_lock:
            cls._client_initialized = False
            cls._thick_mode_enabled = False

    def _get_connection_params(self) -> dict[str, Any]:
        """
        Get connection parameters from Airflow Connection.

        Supports both Service Name and SID:
        - Service Name: use Schema field or extra.service_name
        - SID: use extra.sid

        Returns:
            Dict with user, password, dsn
        """
        from airflow.hooks.base import BaseHook

        conn = BaseHook.get_connection(self.conn_id)

        host = conn.host or "localhost"
        port = conn.port or 1521
        extra = conn.extra_dejson or {}

        # Check if SID is specified (takes priority)
        sid = extra.get("sid")
        if sid:
            # SID format: use makedsn
            dsn = oracledb.makedsn(host, port, sid=sid)
        else:
            # Service Name format: host:port/service_name
            service_name = conn.schema or extra.get("service_name", "ORCL")
            dsn = f"{host}:{port}/{service_name}"

        return {
            "user": conn.login,
            "password": conn.password,
            "dsn": dsn,
        }

    @contextmanager
    def get_connection(self) -> Generator[oracledb.Connection, None, None]:
        """
        Get oracledb connection with automatic client initialization.

        Yields:
            oracledb.Connection: Active database connection

        Example:
            with service.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM dual")
        """
        # Ensure Oracle Client is initialized (lazy, thread-safe)
        self._ensure_client_initialized(self.instant_client_path)

        params = self._get_connection_params()
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
            with self.get_connection() as conn:
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
            with self.get_connection() as conn:
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
            with self.get_connection() as conn:
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

    def execute_query(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> list[tuple[Any, ...]]:
        """
        Execute a SELECT query and return results.

        Args:
            query: SQL SELECT query to execute
            params: Optional query parameters (use :param_name syntax)

        Returns:
            List of tuples containing query results

        Raises:
            Exception: If query execution fails
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or {})
            return cursor.fetchall()

    def execute_query_with_columns(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a SELECT query and return results with column names.

        Args:
            query: SQL SELECT query to execute
            params: Optional query parameters (use :param_name syntax)

        Returns:
            Dict with 'columns' (list of names) and 'rows' (list of tuples)

        Raises:
            Exception: If query execution fails
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or {})
            columns = [col[0] for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            return {
                "columns": columns,
                "rows": rows,
            }
