# include/sql/queries.py

def generate_extract_query(table_name: str, config: dict) -> str:
    """
    Generate optimized Oracle extraction query with Parallel Hints and ROWNUM pagination.
    
    Args:
        table_name: Name of the table to extract
        config: Configuration dictionary containing 'parallel_hint' (optional)
        
    Returns:
        SQL query string with :start_row and :end_row placeholders
    """
    parallel_hint = config.get("parallel_hint", "")
    
    # Base query wrapper for pagination
    sql = f"""
        SELECT * FROM (
            SELECT {parallel_hint} t.*, ROW_NUMBER() OVER (ORDER BY ROWID) as rn
            FROM {table_name} t
        )
        WHERE rn BETWEEN :start_row AND :end_row
    """
    return sql

def generate_count_query(table_name: str) -> str:
    """Generate simple count query"""
    return f"SELECT COUNT(*) FROM {table_name}"
