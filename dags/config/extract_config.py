"""
Oracle Extraction Configuration

Defines chunking and parallel extraction settings per table.
REQ: openspec/specs/extraction/spec.md#parallel-data-extraction
REQ: openspec/specs/extraction/spec.md#date-based-partitioning
REQ: openspec/specs/extraction/spec.md#oracle-parallel-hints
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExtractConfig:
    """Extraction configuration for a table."""

    chunk_size: int = 500_000  # Records per chunk
    parallel_workers: int = 1  # Concurrent extractions
    fetch_size: int = 10_000  # Oracle fetch size
    use_parallel_hint: bool = False  # Oracle parallel query hint
    parallel_degree: int = 4  # Oracle parallel degree


# Table-specific extraction configurations
EXTRACT_CONFIG: dict[str, ExtractConfig] = {
    # Large tables - need parallel chunking
    "KPS_T_SALES_MD": ExtractConfig(
        chunk_size=500_000,
        parallel_workers=10,
        fetch_size=50_000,
        use_parallel_hint=True,
        parallel_degree=8,
    ),
    "KPS_T_SALESPAY_MD": ExtractConfig(
        chunk_size=500_000,
        parallel_workers=8,
        fetch_size=50_000,
        use_parallel_hint=True,
        parallel_degree=8,
    ),
    "KPS_T_SALES_M": ExtractConfig(
        chunk_size=500_000,
        parallel_workers=8,
        fetch_size=50_000,
        use_parallel_hint=True,
        parallel_degree=8,
    ),
    # Medium tables - single worker with larger chunks
    "KPS_T_SALES_APPRV_DETAIL": ExtractConfig(
        chunk_size=500_000,
        parallel_workers=2,
        fetch_size=20_000,
        use_parallel_hint=True,
        parallel_degree=4,
    ),
    "KPS_T_SALESBANK_MD": ExtractConfig(
        chunk_size=500_000,
        parallel_workers=2,
        fetch_size=20_000,
        use_parallel_hint=True,
        parallel_degree=4,
    ),
    "KPS_T_PREINV_REVSALES_D": ExtractConfig(
        chunk_size=500_000,
        parallel_workers=2,
        fetch_size=20_000,
        use_parallel_hint=True,
        parallel_degree=4,
    ),
}

# Default configuration for small tables
DEFAULT_CONFIG = ExtractConfig(
    chunk_size=1_000_000,
    parallel_workers=1,
    fetch_size=10_000,
    use_parallel_hint=False,
    parallel_degree=4,
)


def get_extract_config(table_name: str) -> ExtractConfig:
    """Get extraction configuration for a table."""
    return EXTRACT_CONFIG.get(table_name, DEFAULT_CONFIG)


# Staging configuration
STAGING_CONFIG = {
    "base_path": "/data/staging",
    "use_gzip": True,
    "file_extension": ".csv.gz",
    "cleanup_after_load": True,
}


def get_staging_path(table_name: str, chunk_id: int) -> str:
    """Generate staging file path for a chunk."""
    base = STAGING_CONFIG["base_path"]
    ext = STAGING_CONFIG["file_extension"] if STAGING_CONFIG["use_gzip"] else ".csv"
    return f"{base}/{table_name}_chunk_{chunk_id:04d}{ext}"
