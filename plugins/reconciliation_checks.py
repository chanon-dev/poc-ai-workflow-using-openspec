# plugins/reconciliation_checks.py

from typing import Dict, Tuple, Any

class ReconciliationChecks:
    """
    Logic for verifying migration data integrity.
    """

    @staticmethod
    def compare_counts(source_count: int, sf_count: int, failed_count: int) -> Tuple[bool, Dict[str, Any]]:
        """
        Compare extraction count with Salesforce loading results.
        
        Args:
            source_count: Total records in Oracle
            sf_count: Total records currently in Salesforce Object
            failed_count: Records failed during Bulk Load
            
        Returns:
            (match_bool, details_dict)
        """
        # Ideally: Source = Success + Failed
        # Note: sf_count might include pre-existing data, so this check works best 
        # for initial load or if we track specific batch IDs.
        # For simplicity in this migration, we assume table was empty or we trust distinct counts.
        
        expected_success = source_count - failed_count
        difference = abs(expected_success - sf_count)
        
        match = difference == 0
        
        return match, {
            "source_count": source_count,
            "failed_count": failed_count,
            "expected_sf_count": expected_success,
            "actual_sf_count": sf_count,
            "difference": difference
        }
