# plugins/transformers.py

import pandas as pd
from typing import Dict, Any

class DataTransformer:
    """
    Pandas-based data transformer for Oracle to Salesforce migration.
    Handles field mapping and type conversion.
    """

    @staticmethod
    def transform_dataframe(df: pd.DataFrame, mappings: Dict[str, str]) -> pd.DataFrame:
        """
        Apply field mappings and transformations to a DataFrame.
        
        Args:
            df: Input DataFrame from Oracle
            mappings: Dictionary of column renames {"OLD": "NEW"}
            
        Returns:
            Transformed DataFrame ready for CSV export
        """
        # Rename columns based on mapping
        if mappings:
            df = df.rename(columns=mappings)
        
        # Standardize transformations (can be expanded based on specs)
        # Example: Convert datetime objects to Salesforce ISO8601 string
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                
        return df
