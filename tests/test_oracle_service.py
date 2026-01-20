"""
Unit tests for Oracle Service
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from plugins.oracle_service import (
    DEFAULT_TIMEOUT,
    HealthCheckResult,
    OracleService,
    TableAccessResult,
)


class TestOracleService:
    """Tests for OracleService class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Reset client state before each test
        OracleService.reset_client()
        self.service = OracleService(conn_id="test_oracle", timeout=30)

    def test_init_default_values(self):
        """Test default initialization values."""
        service = OracleService()
        assert service.conn_id == "oracle_kpc"
        assert service.timeout == DEFAULT_TIMEOUT
        assert service.instant_client_path == "/opt/oracle/instantclient"

    def test_init_custom_values(self):
        """Test custom initialization values."""
        service = OracleService(
            conn_id="custom_conn",
            timeout=60,
            instant_client_path="/custom/path",
        )
        assert service.conn_id == "custom_conn"
        assert service.timeout == 60
        assert service.instant_client_path == "/custom/path"

    def test_is_thick_mode_before_init(self):
        """Test thick mode check before initialization."""
        OracleService.reset_client()
        assert OracleService.is_thick_mode() is False

    @patch("plugins.oracle_service.oracledb")
    def test_ensure_client_initialized_success(self, mock_oracledb):
        """Test successful client initialization."""
        OracleService.reset_client()
        OracleService._ensure_client_initialized("/opt/oracle/instantclient")

        mock_oracledb.init_oracle_client.assert_called_once_with(
            lib_dir="/opt/oracle/instantclient"
        )
        assert OracleService._client_initialized is True
        assert OracleService._thick_mode_enabled is True

    @patch("plugins.oracle_service.oracledb")
    def test_ensure_client_initialized_fallback_to_thin(self, mock_oracledb):
        """Test fallback to thin mode when Oracle Client fails."""
        OracleService.reset_client()
        mock_oracledb.init_oracle_client.side_effect = Exception("No Oracle Client")

        OracleService._ensure_client_initialized("/opt/oracle/instantclient")

        assert OracleService._client_initialized is True
        assert OracleService._thick_mode_enabled is False

    @patch("plugins.oracle_service.oracledb")
    def test_ensure_client_initialized_only_once(self, mock_oracledb):
        """Test that client is only initialized once."""
        OracleService.reset_client()

        OracleService._ensure_client_initialized("/opt/oracle/instantclient")
        OracleService._ensure_client_initialized("/opt/oracle/instantclient")
        OracleService._ensure_client_initialized("/opt/oracle/instantclient")

        # Should only be called once
        assert mock_oracledb.init_oracle_client.call_count == 1


class TestGetConnectionParams:
    """Tests for _get_connection_params method."""

    def setup_method(self):
        """Set up test fixtures."""
        OracleService.reset_client()
        self.service = OracleService(conn_id="test_conn")

    @patch("plugins.oracle_service.BaseHook")
    def test_get_connection_params_service_name(self, mock_base_hook):
        """Test connection params with service name."""
        mock_conn = Mock()
        mock_conn.host = "oracle.example.com"
        mock_conn.port = 1521
        mock_conn.schema = "ORCL"
        mock_conn.login = "user"
        mock_conn.password = "pass"
        mock_conn.extra_dejson = {}
        mock_base_hook.get_connection.return_value = mock_conn

        params = self.service._get_connection_params()

        assert params["user"] == "user"
        assert params["password"] == "pass"
        assert params["dsn"] == "oracle.example.com:1521/ORCL"

    @patch("plugins.oracle_service.BaseHook")
    def test_get_connection_params_defaults(self, mock_base_hook):
        """Test connection params with defaults."""
        mock_conn = Mock()
        mock_conn.host = None
        mock_conn.port = None
        mock_conn.schema = None
        mock_conn.login = "user"
        mock_conn.password = "pass"
        mock_conn.extra_dejson = {"service_name": "MYDB"}
        mock_base_hook.get_connection.return_value = mock_conn

        params = self.service._get_connection_params()

        assert params["dsn"] == "localhost:1521/MYDB"

    @patch("plugins.oracle_service.oracledb")
    @patch("plugins.oracle_service.BaseHook")
    def test_get_connection_params_with_sid(self, mock_base_hook, mock_oracledb):
        """Test connection params with SID."""
        mock_conn = Mock()
        mock_conn.host = "oracle.example.com"
        mock_conn.port = 1521
        mock_conn.schema = "ORCL"
        mock_conn.login = "user"
        mock_conn.password = "pass"
        mock_conn.extra_dejson = {"sid": "MYSID"}
        mock_base_hook.get_connection.return_value = mock_conn
        mock_oracledb.makedsn.return_value = "(DESCRIPTION=...)"

        params = self.service._get_connection_params()

        mock_oracledb.makedsn.assert_called_once_with(
            "oracle.example.com", 1521, sid="MYSID"
        )
        assert params["dsn"] == "(DESCRIPTION=...)"


class TestHealthCheck:
    """Tests for health_check method."""

    def setup_method(self):
        """Set up test fixtures."""
        OracleService.reset_client()
        self.service = OracleService(conn_id="test_oracle", timeout=30)

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_health_check_success(self, mock_oracledb, mock_init, mock_get_params):
        """Test successful health check."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            (1,),  # SELECT 1 FROM DUAL
            ("Oracle Database 19c Enterprise Edition",),  # Version query
        ]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        result = self.service.health_check()

        assert result.healthy is True
        assert "Oracle" in result.version
        assert result.error is None

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_health_check_connection_failure(self, mock_oracledb, mock_init, mock_get_params):
        """Test health check with connection failure."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}
        mock_oracledb.connect.side_effect = Exception("Connection refused")

        result = self.service.health_check()

        assert result.healthy is False
        assert result.version is None
        assert "Connection refused" in result.error
        assert "test_oracle" in result.error
        assert "timeout=30" in result.error

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_health_check_unexpected_result(self, mock_oracledb, mock_init, mock_get_params):
        """Test health check with unexpected query result."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        result = self.service.health_check()

        assert result.healthy is False
        assert "Unexpected result" in result.error


class TestVerifyTableAccess:
    """Tests for verify_table_access method."""

    def setup_method(self):
        """Set up test fixtures."""
        OracleService.reset_client()
        self.service = OracleService(conn_id="test_oracle")

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_verify_table_access_all_accessible(self, mock_oracledb, mock_init, mock_get_params):
        """Test all tables accessible."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("row_data",)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        tables = ["TABLE_A", "TABLE_B"]
        results = self.service.verify_table_access(tables)

        assert len(results) == 2
        assert results["TABLE_A"].accessible is True
        assert results["TABLE_B"].accessible is True
        assert results["TABLE_A"].error is None

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_verify_table_access_some_inaccessible(self, mock_oracledb, mock_init, mock_get_params):
        """Test some tables inaccessible."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()

        def execute_side_effect(sql, *args, **kwargs):
            if "TABLE_B" in sql:
                raise Exception("ORA-00942: table or view does not exist")

        mock_cursor.execute.side_effect = execute_side_effect
        mock_cursor.fetchone.return_value = ("row_data",)

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        tables = ["TABLE_A", "TABLE_B"]
        results = self.service.verify_table_access(tables)

        assert results["TABLE_A"].accessible is True
        assert results["TABLE_B"].accessible is False
        assert "ORA-00942" in results["TABLE_B"].error

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_verify_table_access_connection_failure(self, mock_oracledb, mock_init, mock_get_params):
        """Test connection-level failure."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}
        mock_oracledb.connect.side_effect = Exception("Cannot connect")

        tables = ["TABLE_A", "TABLE_B"]
        results = self.service.verify_table_access(tables)

        assert len(results) == 2
        for result in results.values():
            assert result.accessible is False
            assert "Failed to connect" in result.error


class TestRunSampleQuery:
    """Tests for run_sample_query method."""

    def setup_method(self):
        """Set up test fixtures."""
        OracleService.reset_client()
        self.service = OracleService(conn_id="test_oracle")

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_run_sample_query_success(self, mock_oracledb, mock_init, mock_get_params):
        """Test successful sample query."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [("COL1",), ("COL2",), ("COL3",)],  # Column names
            [("val1", "val2", "val3"), ("val4", "val5", "val6")],  # Sample data
        ]
        mock_cursor.fetchone.return_value = (1000,)  # Count

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        result = self.service.run_sample_query("TEST_TABLE", limit=5)

        assert result["success"] is True
        assert result["table_name"] == "TEST_TABLE"
        assert result["columns"] == ["COL1", "COL2", "COL3"]
        assert result["total_count"] == 1000
        assert result["sample_rows"] == 2

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_run_sample_query_failure(self, mock_oracledb, mock_init, mock_get_params):
        """Test failed sample query."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Permission denied")

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        result = self.service.run_sample_query("RESTRICTED_TABLE")

        assert result["success"] is False
        assert "Permission denied" in result["error"]


class TestExecuteQuery:
    """Tests for execute_query method."""

    def setup_method(self):
        """Set up test fixtures."""
        OracleService.reset_client()
        self.service = OracleService(conn_id="test_oracle")

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_execute_query_success(self, mock_oracledb, mock_init, mock_get_params):
        """Test successful query execution."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, "a"), (2, "b")]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        result = self.service.execute_query("SELECT * FROM test")

        assert result == [(1, "a"), (2, "b")]

    @patch.object(OracleService, "_get_connection_params")
    @patch.object(OracleService, "_ensure_client_initialized")
    @patch("plugins.oracle_service.oracledb")
    def test_execute_query_with_columns(self, mock_oracledb, mock_init, mock_get_params):
        """Test query execution with column names."""
        mock_get_params.return_value = {"user": "u", "password": "p", "dsn": "h:1521/s"}

        mock_cursor = MagicMock()
        mock_cursor.description = [("ID",), ("NAME",)]
        mock_cursor.fetchall.return_value = [(1, "a"), (2, "b")]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_oracledb.connect.return_value = mock_conn

        result = self.service.execute_query_with_columns("SELECT * FROM test")

        assert result["columns"] == ["ID", "NAME"]
        assert result["rows"] == [(1, "a"), (2, "b")]


class TestDataclasses:
    """Tests for dataclass structures."""

    def test_health_check_result_healthy(self):
        """Test HealthCheckResult for healthy state."""
        result = HealthCheckResult(healthy=True, version="Oracle 19c")
        assert result.healthy is True
        assert result.version == "Oracle 19c"
        assert result.error is None

    def test_health_check_result_unhealthy(self):
        """Test HealthCheckResult for unhealthy state."""
        result = HealthCheckResult(healthy=False, error="Connection failed")
        assert result.healthy is False
        assert result.version is None
        assert result.error == "Connection failed"

    def test_table_access_result_accessible(self):
        """Test TableAccessResult for accessible table."""
        result = TableAccessResult(table_name="MY_TABLE", accessible=True)
        assert result.table_name == "MY_TABLE"
        assert result.accessible is True
        assert result.error is None

    def test_table_access_result_inaccessible(self):
        """Test TableAccessResult for inaccessible table."""
        result = TableAccessResult(
            table_name="RESTRICTED",
            accessible=False,
            error="Permission denied",
        )
        assert result.accessible is False
        assert result.error == "Permission denied"
