"""
Oracle Data Extractor Plugin

Provides parallel extraction from Oracle with chunking support.
REQ: openspec/specs/extraction/spec.md#parallel-data-extraction
REQ: openspec/specs/extraction/spec.md#date-based-partitioning
REQ: openspec/specs/extraction/spec.md#oracle-parallel-hints
REQ: openspec/specs/extraction/spec.md#staging-file-output
"""

from __future__ import annotations

import gzip
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from airflow.providers.oracle.hooks.oracle import OracleHook

logger = logging.getLogger(__name__)


@dataclass
class ChunkInfo:
    """Information about an extraction chunk."""

    chunk_id: int
    start_row: int
    end_row: int
    record_count: int = 0
    file_path: str = ""


class OracleExtractor:
    """
    Parallel data extractor for Oracle databases.

    Supports:
    - Chunked extraction for large tables
    - Date-based partitioning
    - Oracle parallel query hints
    - GZIP compressed output
    """

    def __init__(
        self,
        oracle_hook: OracleHook,
        table_name: str,
        chunk_size: int = 500_000,
        use_parallel_hint: bool = False,
        parallel_degree: int = 8,
        use_gzip: bool = True,
    ):
        self.oracle_hook = oracle_hook
        self.table_name = table_name
        self.chunk_size = chunk_size
        self.use_parallel_hint = use_parallel_hint
        self.parallel_degree = parallel_degree
        self.use_gzip = use_gzip

    def get_record_count(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        partition_column: str = "CREATED_DATE",
    ) -> int:
        """Get total records matching the date filter."""
        sql = f"SELECT COUNT(*) FROM {self.table_name}"

        parameters: dict[str, Any] = {}
        if start_date and end_date:
            sql += f" WHERE {partition_column} BETWEEN :start_date AND :end_date"
            parameters = {"start_date": start_date, "end_date": end_date}

        result = self.oracle_hook.get_first(sql, parameters=parameters)
        return result[0] if result else 0

    def calculate_chunks(self, total_records: int) -> list[ChunkInfo]:
        """Calculate chunk ranges for parallel extraction."""
        chunks = []
        num_chunks = (total_records // self.chunk_size) + (
            1 if total_records % self.chunk_size else 0
        )

        for i in range(num_chunks):
            start_row = i * self.chunk_size + 1
            end_row = min((i + 1) * self.chunk_size, total_records)
            chunks.append(
                ChunkInfo(
                    chunk_id=i,
                    start_row=start_row,
                    end_row=end_row,
                )
            )

        return chunks

    def generate_extract_query(
        self,
        order_by: str,
        chunk_start: int,
        chunk_end: int,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        partition_column: str = "CREATED_DATE",
    ) -> tuple[str, dict[str, Any]]:
        """Generate optimized Oracle extraction query with chunking."""
        parallel_hint = (
            f"/*+ PARALLEL(t, {self.parallel_degree}) */"
            if self.use_parallel_hint
            else ""
        )

        # Build WHERE clause for date filter
        date_filter = ""
        parameters: dict[str, Any] = {
            "chunk_start": chunk_start,
            "chunk_end": chunk_end,
        }

        if start_date and end_date:
            date_filter = f"WHERE {partition_column} BETWEEN :start_date AND :end_date"
            parameters["start_date"] = start_date
            parameters["end_date"] = end_date

        sql = f"""
            SELECT * FROM (
                SELECT {parallel_hint} t.*, ROW_NUMBER() OVER (ORDER BY {order_by}) as rn
                FROM {self.table_name} t
                {date_filter}
            )
            WHERE rn BETWEEN :chunk_start AND :chunk_end
        """

        return sql.strip(), parameters

    def extract_chunk(
        self,
        chunk: ChunkInfo,
        order_by: str,
        staging_path: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        partition_column: str = "CREATED_DATE",
    ) -> ChunkInfo:
        """Extract a single chunk and save to staging."""
        sql, parameters = self.generate_extract_query(
            order_by=order_by,
            chunk_start=chunk.start_row,
            chunk_end=chunk.end_row,
            start_date=start_date,
            end_date=end_date,
            partition_column=partition_column,
        )

        logger.info(
            f"Extracting chunk {chunk.chunk_id} "
            f"(rows {chunk.start_row}-{chunk.end_row}) from {self.table_name}"
        )

        # Execute query and get DataFrame
        df = self.oracle_hook.get_pandas_df(sql, parameters=parameters)

        # Remove the row number column
        if "RN" in df.columns:
            df = df.drop(columns=["RN"])
        if "rn" in df.columns:
            df = df.drop(columns=["rn"])

        # Save to staging
        chunk.record_count = len(df)
        chunk.file_path = self._save_to_staging(df, staging_path)

        logger.info(
            f"Chunk {chunk.chunk_id} extracted: {chunk.record_count} records "
            f"saved to {chunk.file_path}"
        )

        return chunk

    def _save_to_staging(self, df: pd.DataFrame, staging_path: str) -> str:
        """Save DataFrame to staging file (optionally GZIP compressed)."""
        # Ensure directory exists
        Path(staging_path).parent.mkdir(parents=True, exist_ok=True)

        if self.use_gzip:
            # Ensure .gz extension
            if not staging_path.endswith(".gz"):
                staging_path += ".gz"

            with gzip.open(staging_path, "wt", encoding="utf-8") as f:
                df.to_csv(f, index=False)
        else:
            df.to_csv(staging_path, index=False)

        return staging_path

    def extract_full_table(
        self,
        order_by: str,
        staging_base_path: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        partition_column: str = "CREATED_DATE",
    ) -> list[ChunkInfo]:
        """Extract entire table (or date range) with chunking."""
        # Get total record count
        total_records = self.get_record_count(start_date, end_date, partition_column)
        logger.info(f"Total records to extract from {self.table_name}: {total_records}")

        if total_records == 0:
            return []

        # Calculate chunks
        chunks = self.calculate_chunks(total_records)
        logger.info(f"Splitting into {len(chunks)} chunks of {self.chunk_size} each")

        # Extract each chunk
        results = []
        for chunk in chunks:
            ext = ".csv.gz" if self.use_gzip else ".csv"
            staging_path = f"{staging_base_path}/{self.table_name}_chunk_{chunk.chunk_id:04d}{ext}"

            result = self.extract_chunk(
                chunk=chunk,
                order_by=order_by,
                staging_path=staging_path,
                start_date=start_date,
                end_date=end_date,
                partition_column=partition_column,
            )
            results.append(result)

        return results
