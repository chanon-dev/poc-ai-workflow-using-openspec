# config/load_config.py

"""
Configuration for Salesforce loading.
"""

LOAD_CONFIG = {
    "MAX_RETRIES": 5,
    "BACKOFF_FACTOR": 2,  # Exponential backoff
    "MAX_WORKERS": 10,    # Max concurrent uploads
    "BATCH_SIZE_BYTES": 100 * 1024 * 1024, # 100 MB target
}
