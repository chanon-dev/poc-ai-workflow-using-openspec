"""
Test DAG Integrity
Checks if all DAGs can be loaded without errors.
"""
import pytest
from airflow.models import DagBag

def test_dag_integrity():
    """
    Load all DAGs and check for import errors.
    """
    dag_bag = DagBag(include_examples=False)
    
    # Assert no import errors
    if dag_bag.import_errors:
        error_messages = []
        for filepath, error in dag_bag.import_errors.items():
            error_messages.append(f"{filepath}:\n{error}")
        
        pytest.fail(f"DAG Import Errors:\n" + "\n\n".join(error_messages))
    
    # Assert DAGs exist
    assert len(dag_bag.dags) > 0, "No DAGs found in the project"

def test_dag_tags():
    """
    Ensure all DAGs have tags for better filtering.
    """
    dag_bag = DagBag(include_examples=False)
    for dag_id, dag in dag_bag.dags.items():
        assert dag.tags, f"DAG {dag_id} has no tags. Please add tags for better organization."
