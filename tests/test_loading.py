"""
Unit tests for Salesforce Bulk Loader
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "plugins"))

from plugins.salesforce_bulk_loader import (
    SalesforceBulkLoader,
    JobResult,
    JobState,
)


class TestSalesforceBulkLoader:
    """Tests for SalesforceBulkLoader class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.loader = SalesforceBulkLoader(
            instance_url="https://test.salesforce.com",
            access_token="test_token",
            max_concurrent_jobs=5,
            poll_interval=1,
            job_timeout=10,
        )

    def test_init_max_concurrent_jobs_limit(self):
        """Test that max_concurrent_jobs is capped at 15."""
        loader = SalesforceBulkLoader(
            instance_url="https://test.salesforce.com",
            access_token="test_token",
            max_concurrent_jobs=50,  # Should be capped to 15
        )
        assert loader.max_concurrent_jobs == 15

    def test_base_url_construction(self):
        """Test base URL is constructed correctly."""
        assert "v59.0" in self.loader.base_url
        assert "test.salesforce.com" in self.loader.base_url

    def test_base_url_trailing_slash(self):
        """Test trailing slash is removed from instance URL."""
        loader = SalesforceBulkLoader(
            instance_url="https://test.salesforce.com/",
            access_token="test_token",
        )
        assert not loader.instance_url.endswith("/")

    @patch("requests.Session.post")
    def test_create_job(self, mock_post):
        """Test job creation."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "job123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        job_id = self.loader.create_job(
            object_name="Account",
            operation="upsert",
            external_id_field="External_ID__c",
        )

        assert job_id == "job123"
        mock_post.assert_called_once()

    @patch("requests.Session.get")
    def test_get_job_status(self, mock_get):
        """Test job status retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "job123",
            "state": "JobComplete",
            "numberRecordsProcessed": 1000,
            "numberRecordsFailed": 5,
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        status = self.loader.get_job_status("job123")

        assert status["state"] == "JobComplete"
        assert status["numberRecordsProcessed"] == 1000


class TestJobResult:
    """Tests for JobResult dataclass."""

    def test_job_result_creation(self):
        """Test JobResult creation."""
        result = JobResult(
            job_id="job123",
            state="JobComplete",
            records_processed=1000,
            records_failed=5,
        )
        assert result.job_id == "job123"
        assert result.state == "JobComplete"
        assert result.records_processed == 1000
        assert result.records_failed == 5

    def test_job_result_defaults(self):
        """Test JobResult default values."""
        result = JobResult(job_id="job123", state="InProgress")
        assert result.records_processed == 0
        assert result.records_failed == 0
        assert result.file_path == ""
        assert result.error_message == ""


class TestJobState:
    """Tests for JobState enum."""

    def test_job_states(self):
        """Test all job states are defined."""
        assert JobState.OPEN.value == "Open"
        assert JobState.UPLOAD_COMPLETE.value == "UploadComplete"
        assert JobState.IN_PROGRESS.value == "InProgress"
        assert JobState.JOB_COMPLETE.value == "JobComplete"
        assert JobState.FAILED.value == "Failed"
        assert JobState.ABORTED.value == "Aborted"
