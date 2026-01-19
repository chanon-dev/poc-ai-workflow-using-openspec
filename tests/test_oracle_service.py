"""
Unit tests for Oracle Service
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

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
        self.service = OracleService(conn_id="test_oracle", timeout=30)

    def test_init_default_values(self):
        """Test default initialization values."""
        service = OracleService()
        assert service.conn_id == "oracle_kpc"
        assert service.timeout == DEFAULT_TIMEOUT

    def test_init_custom_values(self):
        """Test custom initialization values."""
        service = OracleService(conn_id="custom_conn", timeout=60)
        assert service.conn_id == "custom_conn"
        assert service.timeout == 60


class TestHealthCheck:
    """Tests for health_check method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = OracleService(conn_id="test_oracle", timeout=30)

    @patch("plugins.oracle_service.OracleHook")
    def test_health_check_success(self, mock_hook_class):
        """Test successful health check."""
        mock_hook = Mock()
        mock_hook.get_first.side_effect = [
            (1,),  # SELECT 1 FROM DUAL
            ("Oracle Database 19c Enterprise Edition",),  # Version query
        ]
        mock_hook_class.return_value = mock_hook

        result = self.service.health_check()

        assert result.healthy is True
        assert "Oracle" in result.version
        assert result.error is None

    @patch("plugins.oracle_service.OracleHook")
    def test_health_check_connection_failure(self, mock_hook_class):
        """Test health check with connection failure."""
        mock_hook = Mock()
        mock_hook.get_first.side_effect = Exception("Connection refused")
        mock_hook_class.return_value = mock_hook

        result = self.service.health_check()

        assert result.healthy is False
        assert result.version is None
        assert "Connection refused" in result.error
        assert "test_oracle" in result.error
        assert "timeout=30" in result.error

    @patch("plugins.oracle_service.OracleHook")
    def test_health_check_unexpected_result(self, mock_hook_class):
        """Test health check with unexpected query result."""
        mock_hook = Mock()
        mock_hook.get_first.return_value = None
        mock_hook_class.return_value = mock_hook

        result = self.service.health_check()

        assert result.healthy is False
        assert "Unexpected result" in result.error


class TestVerifyTableAccess:
    """Tests for verify_table_access method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = OracleService(conn_id="test_oracle")

    @patch("plugins.oracle_service.OracleHook")
    def test_verify_table_access_all_accessible(self, mock_hook_class):
        """Test all tables accessible."""
        mock_hook = Mock()
        mock_hook.get_first.return_value = ("row_data",)
        mock_hook_class.return_value = mock_hook

        tables = ["TABLE_A", "TABLE_B"]
        results = self.service.verify_table_access(tables)

        assert len(results) == 2
        assert results["TABLE_A"].accessible is True
        assert results["TABLE_B"].accessible is True
        assert results["TABLE_A"].error is None

    @patch("plugins.oracle_service.OracleHook")
    def test_verify_table_access_some_inaccessible(self, mock_hook_class):
        """Test some tables inaccessible."""
        mock_hook = Mock()

        def get_first_side_effect(sql, *args, **kwargs):
            if "TABLE_A" in sql:
                return ("row_data",)
            raise Exception("ORA-00942: table or view does not exist")

        mock_hook.get_first.side_effect = get_first_side_effect
        mock_hook_class.return_value = mock_hook

        tables = ["TABLE_A", "TABLE_B"]
        results = self.service.verify_table_access(tables)

        assert results["TABLE_A"].accessible is True
        assert results["TABLE_B"].accessible is False
        assert "ORA-00942" in results["TABLE_B"].error

    @patch("plugins.oracle_service.OracleHook")
    def test_verify_table_access_connection_failure(self, mock_hook_class):
        """Test connection-level failure."""
        mock_hook_class.side_effect = Exception("Cannot connect")

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
        self.service = OracleService(conn_id="test_oracle")

    @patch("plugins.oracle_service.OracleHook")
    def test_run_sample_query_success(self, mock_hook_class):
        """Test successful sample query."""
        mock_hook = Mock()
        mock_hook.get_records.side_effect = [
            [("COL1",), ("COL2",), ("COL3",)],  # Column names
            [("val1", "val2", "val3"), ("val4", "val5", "val6")],  # Sample data
        ]
        mock_hook.get_first.return_value = (1000,)  # Count
        mock_hook_class.return_value = mock_hook

        result = self.service.run_sample_query("TEST_TABLE", limit=5)

        assert result["success"] is True
        assert result["table_name"] == "TEST_TABLE"
        assert result["columns"] == ["COL1", "COL2", "COL3"]
        assert result["total_count"] == 1000
        assert result["sample_rows"] == 2

    @patch("plugins.oracle_service.OracleHook")
    def test_run_sample_query_failure(self, mock_hook_class):
        """Test failed sample query."""
        mock_hook = Mock()
        mock_hook.get_records.side_effect = Exception("Permission denied")
        mock_hook_class.return_value = mock_hook

        result = self.service.run_sample_query("RESTRICTED_TABLE")

        assert result["success"] is False
        assert "Permission denied" in result["error"]


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
