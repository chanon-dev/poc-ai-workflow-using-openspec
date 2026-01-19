"""
Salesforce Bulk API 2.0 Loader Plugin

Provides high-performance loading to Salesforce using Bulk API 2.0.
REQ: openspec/specs/loading/spec.md#bulk-api-20-integration
REQ: openspec/specs/loading/spec.md#gzip-compression
REQ: openspec/specs/loading/spec.md#parallel-job-execution
REQ: openspec/specs/loading/spec.md#error-handling
REQ: openspec/specs/loading/spec.md#idempotent-upsert
"""

from __future__ import annotations

import gzip
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)


class JobState(str, Enum):
    """Bulk API 2.0 job states."""

    OPEN = "Open"
    UPLOAD_COMPLETE = "UploadComplete"
    IN_PROGRESS = "InProgress"
    JOB_COMPLETE = "JobComplete"
    FAILED = "Failed"
    ABORTED = "Aborted"


@dataclass
class JobResult:
    """Result of a Bulk API job."""

    job_id: str
    state: str
    records_processed: int = 0
    records_failed: int = 0
    file_path: str = ""
    error_message: str = ""


class SalesforceBulkLoader:
    """
    High-performance Salesforce Bulk API 2.0 loader.

    Features:
    - GZIP compression for uploads
    - Parallel job execution
    - Upsert operations (idempotent)
    - Error tracking and reporting
    """

    def __init__(
        self,
        instance_url: str,
        access_token: str,
        api_version: str = "v59.0",
        max_concurrent_jobs: int = 15,
        poll_interval: int = 5,
        job_timeout: int = 7200,
    ):
        """
        Initialize the Bulk API loader.

        Args:
            instance_url: Salesforce instance URL
            access_token: OAuth access token
            api_version: API version (default v59.0)
            max_concurrent_jobs: Max parallel jobs (default 15, max safe limit)
            poll_interval: Seconds between status polls
            job_timeout: Max seconds to wait for job completion
        """
        self.instance_url = instance_url.rstrip("/")
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"{self.instance_url}/services/data/{api_version}"

        # REQ: parallel-job-execution - limit to 15 for safety
        self.max_concurrent_jobs = min(max_concurrent_jobs, 15)
        self.poll_interval = poll_interval
        self.job_timeout = job_timeout

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
        )

    def create_job(
        self,
        object_name: str,
        operation: str = "upsert",
        external_id_field: str | None = None,
    ) -> str:
        """
        Create a new Bulk API 2.0 ingest job.

        REQ: openspec/specs/loading/spec.md#bulk-api-20-integration

        Args:
            object_name: Salesforce object name
            operation: insert, update, upsert, delete
            external_id_field: Required for upsert

        Returns:
            Job ID
        """
        job_data: dict[str, Any] = {
            "object": object_name,
            "operation": operation,
            "contentType": "CSV",
            "lineEnding": "LF",
        }

        # REQ: idempotent-upsert
        if operation == "upsert" and external_id_field:
            job_data["externalIdFieldName"] = external_id_field

        response = self._session.post(
            f"{self.base_url}/jobs/ingest",
            json=job_data,
        )
        response.raise_for_status()

        job_id = response.json()["id"]
        logger.info(f"Created job {job_id} for {object_name} ({operation})")
        return job_id

    def upload_data(
        self,
        job_id: str,
        csv_file_path: str,
        use_gzip: bool = True,
    ) -> None:
        """
        Upload CSV data to the job.

        REQ: openspec/specs/loading/spec.md#gzip-compression

        Args:
            job_id: Bulk API job ID
            csv_file_path: Path to CSV file
            use_gzip: Whether to GZIP compress the upload
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "text/csv",
            "Accept": "application/json",
        }

        file_path = Path(csv_file_path)

        # Handle already-compressed files
        if file_path.suffix == ".gz":
            headers["Content-Encoding"] = "gzip"
            with open(csv_file_path, "rb") as f:
                data = f.read()
        elif use_gzip:
            headers["Content-Encoding"] = "gzip"
            with open(csv_file_path, "rb") as f:
                data = gzip.compress(f.read())
        else:
            with open(csv_file_path, "rb") as f:
                data = f.read()

        response = requests.put(
            f"{self.base_url}/jobs/ingest/{job_id}/batches",
            headers=headers,
            data=data,
        )
        response.raise_for_status()

        logger.info(
            f"Uploaded {len(data)} bytes to job {job_id} "
            f"(GZIP: {use_gzip or file_path.suffix == '.gz'})"
        )

    def close_job(self, job_id: str) -> None:
        """Close the job to start processing."""
        response = self._session.patch(
            f"{self.base_url}/jobs/ingest/{job_id}",
            json={"state": JobState.UPLOAD_COMPLETE.value},
        )
        response.raise_for_status()
        logger.info(f"Closed job {job_id}, processing started")

    def get_job_status(self, job_id: str) -> dict[str, Any]:
        """Get job processing status."""
        response = self._session.get(f"{self.base_url}/jobs/ingest/{job_id}")
        response.raise_for_status()
        return response.json()

    def wait_for_job(self, job_id: str) -> JobResult:
        """
        Wait for job to complete.

        REQ: openspec/specs/loading/spec.md#bulk-api-20-integration

        Args:
            job_id: Bulk API job ID

        Returns:
            JobResult with final state and counts
        """
        start_time = time.time()

        while time.time() - start_time < self.job_timeout:
            status = self.get_job_status(job_id)
            state = status["state"]

            if state in (
                JobState.JOB_COMPLETE.value,
                JobState.FAILED.value,
                JobState.ABORTED.value,
            ):
                return JobResult(
                    job_id=job_id,
                    state=state,
                    records_processed=status.get("numberRecordsProcessed", 0),
                    records_failed=status.get("numberRecordsFailed", 0),
                    error_message=status.get("errorMessage", ""),
                )

            logger.debug(f"Job {job_id} state: {state}, waiting...")
            time.sleep(self.poll_interval)

        # Timeout
        return JobResult(
            job_id=job_id,
            state="Timeout",
            error_message=f"Job did not complete within {self.job_timeout} seconds",
        )

    def load_file(
        self,
        object_name: str,
        csv_file_path: str,
        external_id_field: str,
        use_gzip: bool = True,
    ) -> JobResult:
        """
        Load a single CSV file to Salesforce.

        REQ: openspec/specs/loading/spec.md#idempotent-upsert

        Args:
            object_name: Salesforce object
            csv_file_path: Path to CSV file
            external_id_field: External ID field for upsert
            use_gzip: Whether to GZIP compress

        Returns:
            JobResult with outcome
        """
        try:
            job_id = self.create_job(object_name, "upsert", external_id_field)
            self.upload_data(job_id, csv_file_path, use_gzip)
            self.close_job(job_id)
            result = self.wait_for_job(job_id)
            result.file_path = csv_file_path
            return result

        except requests.HTTPError as e:
            logger.error(f"HTTP error loading {csv_file_path}: {e}")
            return JobResult(
                job_id="",
                state=JobState.FAILED.value,
                file_path=csv_file_path,
                error_message=str(e),
            )
        except Exception as e:
            logger.error(f"Error loading {csv_file_path}: {e}")
            return JobResult(
                job_id="",
                state=JobState.FAILED.value,
                file_path=csv_file_path,
                error_message=str(e),
            )

    def load_files_parallel(
        self,
        object_name: str,
        csv_files: list[str],
        external_id_field: str,
        use_gzip: bool = True,
        max_workers: int | None = None,
    ) -> list[JobResult]:
        """
        Load multiple CSV files in parallel.

        REQ: openspec/specs/loading/spec.md#parallel-job-execution

        Args:
            object_name: Salesforce object
            csv_files: List of CSV file paths
            external_id_field: External ID field
            use_gzip: Whether to GZIP compress
            max_workers: Override max concurrent jobs

        Returns:
            List of JobResult for all files
        """
        workers = min(max_workers or self.max_concurrent_jobs, len(csv_files))
        results: list[JobResult] = []

        logger.info(f"Loading {len(csv_files)} files with {workers} parallel workers")

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    self.load_file, object_name, f, external_id_field, use_gzip
                ): f
                for f in csv_files
            }

            for future in as_completed(futures):
                csv_file = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(
                        f"Completed {csv_file}: {result.state} "
                        f"({result.records_processed} processed, "
                        f"{result.records_failed} failed)"
                    )
                except Exception as e:
                    logger.error(f"Exception loading {csv_file}: {e}")
                    results.append(
                        JobResult(
                            job_id="",
                            state=JobState.FAILED.value,
                            file_path=csv_file,
                            error_message=str(e),
                        )
                    )

        # Summary
        total_processed = sum(r.records_processed for r in results)
        total_failed = sum(r.records_failed for r in results)
        logger.info(
            f"Parallel load complete: {total_processed} processed, {total_failed} failed"
        )

        return results


# Configuration for Salesforce loading
LOAD_CONFIG = {
    "api_version": "v59.0",
    "max_concurrent_jobs": 15,
    "poll_interval_seconds": 5,
    "job_timeout_seconds": 7200,
    "use_gzip_compression": True,
}
