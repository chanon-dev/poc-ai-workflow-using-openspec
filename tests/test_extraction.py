"""
Unit tests for Oracle Extractor
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from plugins.oracle_extractor import OracleExtractor, ChunkInfo


class TestOracleExtractor:
    """Tests for OracleExtractor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_hook = Mock()
        self.extractor = OracleExtractor(
            oracle_hook=self.mock_hook,
            table_name="TEST_TABLE",
            chunk_size=100_000,
            use_parallel_hint=True,
            parallel_degree=4,
        )

    def test_calculate_chunks_single(self):
        """Test chunking for small table."""
        chunks = self.extractor.calculate_chunks(50_000)
        assert len(chunks) == 1
        assert chunks[0].start_row == 1
        assert chunks[0].end_row == 50_000

    def test_calculate_chunks_multiple(self):
        """Test chunking for large table."""
        chunks = self.extractor.calculate_chunks(250_000)
        assert len(chunks) == 3
        assert chunks[0].start_row == 1
        assert chunks[0].end_row == 100_000
        assert chunks[1].start_row == 100_001
        assert chunks[1].end_row == 200_000
        assert chunks[2].start_row == 200_001
        assert chunks[2].end_row == 250_000

    def test_calculate_chunks_exact(self):
        """Test chunking when records divide evenly."""
        chunks = self.extractor.calculate_chunks(200_000)
        assert len(chunks) == 2
        assert chunks[1].end_row == 200_000

    def test_calculate_chunks_zero(self):
        """Test chunking with zero records."""
        chunks = self.extractor.calculate_chunks(0)
        assert len(chunks) == 0

    def test_generate_query_with_parallel_hint(self):
        """Test query generation with parallel hint."""
        sql, params = self.extractor.generate_extract_query(
            order_by="ID",
            chunk_start=1,
            chunk_end=100_000,
        )
        assert "/*+ PARALLEL(t, 4) */" in sql
        assert ":chunk_start" in sql
        assert ":chunk_end" in sql
        assert params["chunk_start"] == 1
        assert params["chunk_end"] == 100_000

    def test_generate_query_without_parallel_hint(self):
        """Test query generation without parallel hint."""
        extractor = OracleExtractor(
            oracle_hook=self.mock_hook,
            table_name="TEST_TABLE",
            chunk_size=100_000,
            use_parallel_hint=False,
        )
        sql, _ = extractor.generate_extract_query(
            order_by="ID",
            chunk_start=1,
            chunk_end=100_000,
        )
        assert "PARALLEL" not in sql

    def test_generate_query_with_date_filter(self):
        """Test query generation with date filtering."""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)

        sql, params = self.extractor.generate_extract_query(
            order_by="ID",
            chunk_start=1,
            chunk_end=100_000,
            start_date=start,
            end_date=end,
            partition_column="CREATED_DATE",
        )
        assert "CREATED_DATE BETWEEN :start_date AND :end_date" in sql
        assert params["start_date"] == start
        assert params["end_date"] == end

    def test_get_record_count(self):
        """Test record count retrieval."""
        self.mock_hook.get_first.return_value = (1000000,)

        count = self.extractor.get_record_count()

        assert count == 1000000
        self.mock_hook.get_first.assert_called_once()


class TestChunkInfo:
    """Tests for ChunkInfo dataclass."""

    def test_chunk_info_creation(self):
        """Test ChunkInfo creation."""
        chunk = ChunkInfo(chunk_id=0, start_row=1, end_row=500_000)
        assert chunk.chunk_id == 0
        assert chunk.start_row == 1
        assert chunk.end_row == 500_000
        assert chunk.record_count == 0
        assert chunk.file_path == ""
