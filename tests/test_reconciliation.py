"""
Unit tests for Data Reconciliation
"""

import pytest
from unittest.mock import Mock

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from plugins.reconciliation import (
    DataReconciliation,
    ValidationResult,
    ReconciliationReport,
)


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_pass(self):
        """Test passing validation result."""
        result = ValidationResult(
            check_type="count",
            status="PASS",
            details={"oracle_count": 1000, "sf_count": 1000},
        )
        assert result.check_type == "count"
        assert result.status == "PASS"
        assert result.details["oracle_count"] == 1000

    def test_validation_result_fail(self):
        """Test failing validation result."""
        result = ValidationResult(
            check_type="count",
            status="FAIL",
            details={"oracle_count": 1000, "sf_count": 999, "difference": 1},
        )
        assert result.status == "FAIL"
        assert result.details["difference"] == 1


class TestReconciliationReport:
    """Tests for ReconciliationReport dataclass."""

    def test_report_creation(self):
        """Test report creation."""
        report = ReconciliationReport(
            table_name="TEST_TABLE",
            sf_object="Test__c",
            timestamp="2024-01-01T00:00:00",
        )
        assert report.table_name == "TEST_TABLE"
        assert report.sf_object == "Test__c"
        assert report.overall_status == "PENDING"
        assert len(report.checks) == 0

    def test_report_with_checks(self):
        """Test report with validation checks."""
        report = ReconciliationReport(
            table_name="TEST_TABLE",
            sf_object="Test__c",
            timestamp="2024-01-01T00:00:00",
        )
        report.checks["count"] = ValidationResult(
            check_type="count",
            status="PASS",
            details={},
        )
        report.overall_status = "PASS"

        assert len(report.checks) == 1
        assert report.overall_status == "PASS"


class TestDataReconciliation:
    """Tests for DataReconciliation class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_oracle_hook = Mock()
        self.mock_sf_hook = Mock()
        self.mock_sf_conn = Mock()
        self.mock_sf_hook.get_conn.return_value = self.mock_sf_conn

        self.reconciler = DataReconciliation(
            oracle_hook=self.mock_oracle_hook,
            sf_hook=self.mock_sf_hook,
        )

    def test_count_check_match(self):
        """Test count check when counts match."""
        self.mock_oracle_hook.get_first.return_value = (1000,)
        self.mock_sf_conn.query.return_value = {"totalSize": 1000}

        result = self.reconciler.count_check("TEST_TABLE", "Test__c")

        assert result.status == "PASS"
        assert result.details["oracle_count"] == 1000
        assert result.details["sf_count"] == 1000
        assert result.details["difference"] == 0

    def test_count_check_mismatch(self):
        """Test count check when counts differ."""
        self.mock_oracle_hook.get_first.return_value = (1000,)
        self.mock_sf_conn.query.return_value = {"totalSize": 950}

        result = self.reconciler.count_check("TEST_TABLE", "Test__c")

        assert result.status == "FAIL"
        assert result.details["difference"] == 50
        assert result.details["match_percentage"] == 95.0

    def test_count_check_zero_oracle(self):
        """Test count check with zero Oracle records."""
        self.mock_oracle_hook.get_first.return_value = (0,)
        self.mock_sf_conn.query.return_value = {"totalSize": 0}

        result = self.reconciler.count_check("TEST_TABLE", "Test__c")

        assert result.status == "PASS"
        assert result.details["match_percentage"] == 0

    def test_aggregate_check_within_threshold(self):
        """Test aggregate check within variance threshold."""
        self.mock_oracle_hook.get_first.return_value = (10000.0, 100.0, 1.0, 500.0)
        self.mock_sf_conn.query.return_value = {
            "records": [{"expr0": 10000.0, "expr1": 100.0, "expr2": 1.0, "expr3": 500.0}]
        }

        result = self.reconciler.aggregate_check(
            "TEST_TABLE", "Test__c", "AMOUNT", "Amount__c"
        )

        assert result.status == "PASS"
        assert result.details["variance"] == 0

    def test_generate_report(self):
        """Test full report generation."""
        self.mock_oracle_hook.get_first.return_value = (1000,)
        self.mock_sf_conn.query.return_value = {"totalSize": 1000}

        report = self.reconciler.generate_report(
            oracle_table="TEST_TABLE",
            sf_object="Test__c",
        )

        assert report.table_name == "TEST_TABLE"
        assert report.sf_object == "Test__c"
        assert "count" in report.checks
        assert report.overall_status == "PASS"

    def test_generate_report_with_failure(self):
        """Test report generation with a failing check."""
        self.mock_oracle_hook.get_first.return_value = (1000,)
        self.mock_sf_conn.query.return_value = {"totalSize": 500}

        report = self.reconciler.generate_report(
            oracle_table="TEST_TABLE",
            sf_object="Test__c",
        )

        assert report.overall_status == "FAIL"
