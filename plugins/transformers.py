"""
Data Transformers Plugin

Provides data transformation functions for Oracle→Salesforce conversion.
REQ: openspec/specs/transformation/spec.md#field-mapping
REQ: openspec/specs/transformation/spec.md#type-conversion
REQ: openspec/specs/transformation/spec.md#text-truncation
REQ: openspec/specs/transformation/spec.md#transformation-pipeline
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class DataTransformer:
    """
    Transform Oracle data for Salesforce compatibility.

    Handles:
    - DateTime format conversion
    - Decimal precision
    - Boolean conversion
    - Text truncation
    - NULL handling
    """

    @staticmethod
    def to_sf_datetime(value: Any) -> str | None:
        """
        Convert Oracle datetime to Salesforce ISO 8601 format.

        REQ: openspec/specs/transformation/spec.md#type-conversion

        Args:
            value: Oracle datetime value

        Returns:
            ISO 8601 formatted string (YYYY-MM-DDTHH:MM:SS.000Z) or None
        """
        if pd.isna(value) or value is None:
            return None

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            except ValueError:
                return value

        return str(value)

    @staticmethod
    def to_decimal_2(value: Any) -> float | None:
        """
        Convert to 2 decimal places.

        REQ: openspec/specs/transformation/spec.md#type-conversion

        Args:
            value: Numeric value

        Returns:
            Float rounded to 2 decimal places or None
        """
        if pd.isna(value) or value is None:
            return None

        try:
            return round(float(value), 2)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def to_sf_boolean(value: Any) -> bool | None:
        """
        Convert to Salesforce boolean.

        REQ: openspec/specs/transformation/spec.md#type-conversion

        Args:
            value: Value to convert (1, Y, YES, TRUE → True)

        Returns:
            Boolean or None
        """
        if pd.isna(value) or value is None:
            return None

        if isinstance(value, bool):
            return value

        str_val = str(value).upper().strip()
        return str_val in ("1", "Y", "YES", "TRUE")

    @staticmethod
    def truncate_text(value: Any, max_length: int = 255) -> str | None:
        """
        Truncate text to specified max length.

        REQ: openspec/specs/transformation/spec.md#text-truncation

        Args:
            value: Text value
            max_length: Maximum characters (default 255)

        Returns:
            Truncated string or None
        """
        if pd.isna(value) or value is None:
            return None

        text = str(value)
        return text[:max_length] if len(text) > max_length else text

    @staticmethod
    def truncate_255(value: Any) -> str | None:
        """Shorthand for truncate to 255 chars."""
        return DataTransformer.truncate_text(value, 255)

    def get_transform_func(self, func_name: str):
        """Get transformation function by name."""
        funcs = {
            "to_sf_datetime": self.to_sf_datetime,
            "to_decimal_2": self.to_decimal_2,
            "to_sf_boolean": self.to_sf_boolean,
            "truncate_255": self.truncate_255,
            "truncate_text": self.truncate_text,
        }
        return funcs.get(func_name)

    def transform_dataframe(
        self,
        df: pd.DataFrame,
        mappings: dict[str, str],
        transformations: dict[str, str] | None = None,
    ) -> pd.DataFrame:
        """
        Apply all transformations to dataframe.

        REQ: openspec/specs/transformation/spec.md#transformation-pipeline

        Args:
            df: Source DataFrame
            mappings: Column rename mapping (Oracle → SF)
            transformations: Column transformation mapping (column → func_name)

        Returns:
            Transformed DataFrame with only mapped columns
        """
        # Step 1: Apply transformations BEFORE renaming
        if transformations:
            for oracle_col, func_name in transformations.items():
                if oracle_col in df.columns:
                    transform_func = self.get_transform_func(func_name)
                    if transform_func:
                        logger.debug(f"Applying {func_name} to {oracle_col}")
                        df[oracle_col] = df[oracle_col].apply(transform_func)

        # Step 2: Rename columns (Oracle → Salesforce)
        df = df.rename(columns=mappings)

        # Step 3: Keep only mapped columns
        sf_columns = list(mappings.values())
        columns_to_keep = [col for col in sf_columns if col in df.columns]
        df = df[columns_to_keep]

        logger.info(f"Transformed DataFrame: {len(df)} rows, {len(columns_to_keep)} columns")
        return df


def transform_for_salesforce(
    df: pd.DataFrame,
    mappings: dict[str, str],
    transformations: dict[str, str] | None = None,
) -> pd.DataFrame:
    """
    Convenience function to transform DataFrame for Salesforce.

    Args:
        df: Source DataFrame
        mappings: Column rename mapping
        transformations: Column transformation mapping

    Returns:
        Transformed DataFrame
    """
    transformer = DataTransformer()
    return transformer.transform_dataframe(df, mappings, transformations)
