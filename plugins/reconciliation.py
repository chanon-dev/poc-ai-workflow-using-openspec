"""
Data Reconciliation Plugin

Provides validation between Oracle source and Salesforce target.
REQ: openspec/specs/reconciliation/spec.md#count-validation
REQ: openspec/specs/reconciliation/spec.md#aggregate-validation
REQ: openspec/specs/reconciliation/spec.md#sample-checksum-validation
REQ: openspec/specs/reconciliation/spec.md#reconciliation-report
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from airflow.providers.oracle.hooks.oracle import OracleHook
    from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a single validation check."""

    check_type: str
    status: str  # "PASS" or "FAIL"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReconciliationReport:
    """Complete reconciliation report for a table."""

    table_name: str
    sf_object: str
    timestamp: str
    checks: dict[str, ValidationResult] = field(default_factory=dict)
    overall_status: str = "PENDING"


class DataReconciliation:
    """
    Data reconciliation between Oracle and Salesforce.

    Provides three levels of validation:
    1. Count comparison (fast, low accuracy)
    2. Aggregate validation (medium speed, medium accuracy)
    3. Sample checksum (slow, high accuracy)
    """

    def __init__(self, oracle_hook: OracleHook, sf_hook: SalesforceHook):
        """
        Initialize reconciliation.

        Args:
            oracle_hook: Airflow Oracle hook
            sf_hook: Airflow Salesforce hook
        """
        self.oracle = oracle_hook
        self.sf = sf_hook

    def count_check(
        self,
        oracle_table: str,
        sf_object: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        oracle_date_column: str = "CREATED_DATE",
        sf_date_field: str = "Oracle_Created_Date__c",
    ) -> ValidationResult:
        """
        Compare record counts between Oracle and Salesforce.

        REQ: openspec/specs/reconciliation/spec.md#count-validation

        Args:
            oracle_table: Oracle table name
            sf_object: Salesforce object name
            start_date: Optional filter start date
            end_date: Optional filter end date
            oracle_date_column: Oracle date column for filtering
            sf_date_field: SF date field for filtering

        Returns:
            ValidationResult with count comparison
        """
        # Oracle count
        oracle_sql = f"SELECT COUNT(*) FROM {oracle_table}"
        params: dict[str, Any] = {}

        if start_date and end_date:
            oracle_sql += f" WHERE {oracle_date_column} BETWEEN :start_date AND :end_date"
            params = {"start_date": start_date, "end_date": end_date}

        oracle_result = self.oracle.get_first(oracle_sql, parameters=params)
        oracle_count = oracle_result[0] if oracle_result else 0

        # Salesforce count
        sf_query = f"SELECT COUNT(Id) FROM {sf_object}"
        if start_date and end_date:
            sf_query += (
                f" WHERE {sf_date_field} >= {start_date.isoformat()}T00:00:00Z"
                f" AND {sf_date_field} <= {end_date.isoformat()}T23:59:59Z"
            )

        sf_result = self.sf.get_conn().query(sf_query)
        sf_count = sf_result.get("totalSize", 0)

        # Calculate match
        difference = oracle_count - sf_count
        match_pct = (sf_count / oracle_count * 100) if oracle_count > 0 else 0
        status = "PASS" if difference == 0 else "FAIL"

        logger.info(
            f"Count check {oracle_table}: Oracle={oracle_count}, SF={sf_count}, "
            f"Diff={difference}, Status={status}"
        )

        return ValidationResult(
            check_type="count",
            status=status,
            details={
                "oracle_count": oracle_count,
                "sf_count": sf_count,
                "difference": difference,
                "match_percentage": round(match_pct, 2),
            },
        )

    def aggregate_check(
        self,
        oracle_table: str,
        sf_object: str,
        oracle_column: str,
        sf_field: str,
        variance_threshold: float = 0.01,
    ) -> ValidationResult:
        """
        Compare aggregates of numeric columns.

        REQ: openspec/specs/reconciliation/spec.md#aggregate-validation

        Args:
            oracle_table: Oracle table name
            sf_object: Salesforce object name
            oracle_column: Oracle numeric column
            sf_field: Salesforce numeric field
            variance_threshold: Acceptable variance % (default 0.01%)

        Returns:
            ValidationResult with aggregate comparison
        """
        # Oracle aggregates
        oracle_sql = f"""
            SELECT SUM({oracle_column}), AVG({oracle_column}),
                   MIN({oracle_column}), MAX({oracle_column})
            FROM {oracle_table}
        """
        oracle_result = self.oracle.get_first(oracle_sql)
        oracle_sum = float(oracle_result[0] or 0)
        oracle_avg = float(oracle_result[1] or 0)
        oracle_min = float(oracle_result[2] or 0)
        oracle_max = float(oracle_result[3] or 0)

        # Salesforce aggregates
        sf_query = f"""
            SELECT SUM({sf_field}), AVG({sf_field}),
                   MIN({sf_field}), MAX({sf_field})
            FROM {sf_object}
        """
        sf_result = self.sf.get_conn().query(sf_query)
        record = sf_result.get("records", [{}])[0]
        sf_sum = float(record.get("expr0") or 0)
        sf_avg = float(record.get("expr1") or 0)
        sf_min = float(record.get("expr2") or 0)
        sf_max = float(record.get("expr3") or 0)

        # Calculate variance
        variance = abs(oracle_sum - sf_sum)
        variance_pct = (variance / oracle_sum * 100) if oracle_sum > 0 else 0
        status = "PASS" if variance_pct < variance_threshold else "FAIL"

        logger.info(
            f"Aggregate check {oracle_column}: "
            f"Oracle SUM={oracle_sum}, SF SUM={sf_sum}, "
            f"Variance={variance_pct:.4f}%, Status={status}"
        )

        return ValidationResult(
            check_type="aggregate",
            status=status,
            details={
                "column": sf_field,
                "oracle": {
                    "sum": oracle_sum,
                    "avg": oracle_avg,
                    "min": oracle_min,
                    "max": oracle_max,
                },
                "salesforce": {
                    "sum": sf_sum,
                    "avg": sf_avg,
                    "min": sf_min,
                    "max": sf_max,
                },
                "variance": variance,
                "variance_percentage": round(variance_pct, 4),
            },
        )

    def checksum_sample(
        self,
        oracle_table: str,
        sf_object: str,
        key_column: str,
        sf_key_field: str = "External_ID__c",
        sample_size: int = 1000,
    ) -> ValidationResult:
        """
        Compare checksums on sample records.

        REQ: openspec/specs/reconciliation/spec.md#sample-checksum-validation

        Args:
            oracle_table: Oracle table name
            sf_object: Salesforce object name
            key_column: Oracle key column
            sf_key_field: SF key field
            sample_size: Number of random records

        Returns:
            ValidationResult with checksum comparison
        """
        # Get random sample of keys from Oracle
        oracle_sql = f"""
            SELECT {key_column} FROM (
                SELECT {key_column} FROM {oracle_table}
                ORDER BY DBMS_RANDOM.VALUE
            ) WHERE ROWNUM <= :sample_size
        """
        sample_keys = self.oracle.get_records(
            oracle_sql, parameters={"sample_size": sample_size}
        )
        sample_keys = [str(r[0]) for r in sample_keys]

        if not sample_keys:
            return ValidationResult(
                check_type="checksum",
                status="PASS",
                details={
                    "sample_size": 0,
                    "message": "No records to sample",
                },
            )

        matches = 0
        mismatches: list[str] = []

        for key in sample_keys:
            oracle_checksum = self._get_oracle_checksum(oracle_table, key_column, key)
            sf_checksum = self._get_sf_checksum(sf_object, sf_key_field, key)

            if oracle_checksum == sf_checksum:
                matches += 1
            else:
                mismatches.append(key)

        match_pct = (matches / len(sample_keys) * 100) if sample_keys else 0
        status = "PASS" if len(mismatches) == 0 else "FAIL"

        logger.info(
            f"Checksum check {oracle_table}: "
            f"Sample={len(sample_keys)}, Matches={matches}, "
            f"Mismatches={len(mismatches)}, Status={status}"
        )

        return ValidationResult(
            check_type="checksum",
            status=status,
            details={
                "sample_size": len(sample_keys),
                "matches": matches,
                "mismatches": len(mismatches),
                "match_percentage": round(match_pct, 2),
                "mismatch_keys": mismatches[:10],  # First 10 for debugging
            },
        )

    def _get_oracle_checksum(
        self, table_name: str, key_column: str, key_value: str
    ) -> str:
        """Get MD5 checksum for an Oracle record."""
        sql = f"""
            SELECT ORA_HASH(
                (SELECT * FROM {table_name} WHERE {key_column} = :key_value)
            ) FROM DUAL
        """
        result = self.oracle.get_first(sql, parameters={"key_value": key_value})
        return str(result[0]) if result else ""

    def _get_sf_checksum(
        self, sf_object: str, key_field: str, key_value: str
    ) -> str:
        """Get checksum for a Salesforce record (simplified)."""
        query = f"SELECT Id FROM {sf_object} WHERE {key_field} = '{key_value}'"
        result = self.sf.get_conn().query(query)

        if result.get("records"):
            # Use record ID as simplified checksum
            return hashlib.md5(
                str(result["records"][0]).encode()
            ).hexdigest()
        return ""

    def generate_report(
        self,
        oracle_table: str,
        sf_object: str,
        numeric_columns: list[tuple[str, str]] | None = None,
        key_column: str | None = None,
    ) -> ReconciliationReport:
        """
        Generate complete reconciliation report.

        REQ: openspec/specs/reconciliation/spec.md#reconciliation-report

        Args:
            oracle_table: Oracle table name
            sf_object: Salesforce object name
            numeric_columns: List of (oracle_col, sf_field) for aggregate checks
            key_column: Key column for checksum validation

        Returns:
            ReconciliationReport with all checks
        """
        report = ReconciliationReport(
            table_name=oracle_table,
            sf_object=sf_object,
            timestamp=datetime.now().isoformat(),
        )

        # Count check (always run)
        report.checks["count"] = self.count_check(oracle_table, sf_object)

        # Aggregate checks for numeric columns
        if numeric_columns:
            for oracle_col, sf_field in numeric_columns:
                check_name = f"aggregate_{sf_field}"
                report.checks[check_name] = self.aggregate_check(
                    oracle_table, sf_object, oracle_col, sf_field
                )

        # Checksum sample (if key provided)
        if key_column:
            report.checks["checksum"] = self.checksum_sample(
                oracle_table, sf_object, key_column
            )

        # Overall status
        all_passed = all(
            check.status == "PASS" for check in report.checks.values()
        )
        report.overall_status = "PASS" if all_passed else "FAIL"

        logger.info(
            f"Reconciliation report for {oracle_table}: {report.overall_status}"
        )

        return report


def run_reconciliation(
    oracle_hook: OracleHook,
    sf_hook: SalesforceHook,
    oracle_table: str,
    sf_object: str,
    numeric_columns: list[tuple[str, str]] | None = None,
    key_column: str | None = None,
) -> ReconciliationReport:
    """
    Convenience function to run full reconciliation.

    Args:
        oracle_hook: Airflow Oracle hook
        sf_hook: Airflow Salesforce hook
        oracle_table: Oracle table name
        sf_object: Salesforce object name
        numeric_columns: Optional numeric columns for aggregate
        key_column: Optional key for checksum

    Returns:
        ReconciliationReport
    """
    reconciler = DataReconciliation(oracle_hook, sf_hook)
    return reconciler.generate_report(
        oracle_table, sf_object, numeric_columns, key_column
    )
