"""
Unit tests for Data Transformers
"""

import pytest
from datetime import datetime

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

import pandas as pd
from plugins.transformers import DataTransformer, transform_for_salesforce


class TestDataTransformer:
    """Tests for DataTransformer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transformer = DataTransformer()

    def test_to_sf_datetime_from_datetime(self):
        """Test datetime conversion from datetime object."""
        dt = datetime(2024, 6, 15, 10, 30, 45)
        result = self.transformer.to_sf_datetime(dt)
        assert result == "2024-06-15T10:30:45.000Z"

    def test_to_sf_datetime_none(self):
        """Test datetime conversion with None."""
        assert self.transformer.to_sf_datetime(None) is None

    def test_to_sf_datetime_nan(self):
        """Test datetime conversion with NaN."""
        assert self.transformer.to_sf_datetime(float("nan")) is None

    def test_to_decimal_2_normal(self):
        """Test decimal conversion."""
        assert self.transformer.to_decimal_2(123.456789) == 123.46
        assert self.transformer.to_decimal_2(100) == 100.0
        assert self.transformer.to_decimal_2("99.999") == 100.0

    def test_to_decimal_2_none(self):
        """Test decimal conversion with None."""
        assert self.transformer.to_decimal_2(None) is None

    def test_to_sf_boolean_true_values(self):
        """Test boolean conversion for true values."""
        true_values = ["1", "Y", "YES", "TRUE", "y", "yes", "true", 1, True]
        for val in true_values:
            assert self.transformer.to_sf_boolean(val) is True

    def test_to_sf_boolean_false_values(self):
        """Test boolean conversion for false values."""
        false_values = ["0", "N", "NO", "FALSE", "", "other"]
        for val in false_values:
            assert self.transformer.to_sf_boolean(val) is False

    def test_to_sf_boolean_none(self):
        """Test boolean conversion with None."""
        assert self.transformer.to_sf_boolean(None) is None

    def test_truncate_text_short(self):
        """Test truncation for short text."""
        result = self.transformer.truncate_text("hello", 255)
        assert result == "hello"

    def test_truncate_text_long(self):
        """Test truncation for long text."""
        long_text = "x" * 300
        result = self.transformer.truncate_text(long_text, 255)
        assert len(result) == 255

    def test_truncate_text_none(self):
        """Test truncation with None."""
        assert self.transformer.truncate_text(None) is None

    def test_transform_dataframe(self):
        """Test full DataFrame transformation."""
        df = pd.DataFrame({
            "SALES_ID": [1, 2, 3],
            "SALES_AMOUNT": [100.456, 200.789, 300.123],
            "CREATED_DATE": [
                datetime(2024, 1, 1),
                datetime(2024, 2, 1),
                datetime(2024, 3, 1),
            ],
            "EXTRA_COLUMN": ["a", "b", "c"],  # Should be dropped
        })

        mappings = {
            "SALES_ID": "External_ID__c",
            "SALES_AMOUNT": "Sales_Amount__c",
            "CREATED_DATE": "Oracle_Created_Date__c",
        }

        transformations = {
            "SALES_AMOUNT": "to_decimal_2",
            "CREATED_DATE": "to_sf_datetime",
        }

        result = self.transformer.transform_dataframe(df, mappings, transformations)

        # Check column renaming
        assert "External_ID__c" in result.columns
        assert "Sales_Amount__c" in result.columns
        assert "Oracle_Created_Date__c" in result.columns
        assert "EXTRA_COLUMN" not in result.columns

        # Check transformations
        assert result["Sales_Amount__c"].tolist() == [100.46, 200.79, 300.12]
        assert result["Oracle_Created_Date__c"].iloc[0] == "2024-01-01T00:00:00.000Z"


class TestTransformForSalesforce:
    """Tests for convenience function."""

    def test_transform_function(self):
        """Test transform_for_salesforce function."""
        df = pd.DataFrame({
            "ID": [1, 2],
            "VALUE": [10.555, 20.666],
        })

        result = transform_for_salesforce(
            df,
            mappings={"ID": "External_ID__c", "VALUE": "Amount__c"},
            transformations={"VALUE": "to_decimal_2"},
        )

        assert len(result.columns) == 2
        assert result["Amount__c"].tolist() == [10.56, 20.67]
