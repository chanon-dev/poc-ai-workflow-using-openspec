"""
Migration Logger Plugin

Structured logging สำหรับ track migration progress ใน PostgreSQL.
Fail-safe: ถ้า DB logging fail จะ log warning แต่ไม่ raise exception.

Tables:
    - migration.runs       — 1 row ต่อ 1 DAG run
    - migration.batch_logs — 1 row ต่อ 1 batch/job

Schema: sql/init_migration_logging.sql
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class MigrationRunLog:
    """Migration run metadata."""

    run_id: str
    dag_id: str
    table_name: str = ""
    sf_object: str = ""
    operation: str = "upsert"
    status: str = "running"
    total_records: int = 0
    total_batches: int = 0
    batch_size: int = 0
    total_processed: int = 0
    total_failed: int = 0
    start_batch: int = 1
    error_message: Optional[str] = None


@dataclass
class MigrationBatchLog:
    """Batch upload metadata."""

    run_id: str
    batch_number: int
    job_id: Optional[str] = None
    file_path: Optional[str] = None
    state: str = "pending"
    records_in_batch: int = 0
    records_processed: int = 0
    records_failed: int = 0
    error_message: Optional[str] = None


class MigrationLogger:
    """
    Logger for tracking migration progress in PostgreSQL.

    - Fail-safe: ไม่ raise exception ถ้า DB logging fail
    - Idempotent: ใช้ ON CONFLICT สำหรับ resume/retry
    - Uses PostgresHook (Airflow standard)

    Usage:
        ml = MigrationLogger()
        ml.log_run_start(run_id, dag_id, table_name=..., ...)
        ml.log_batch_start(run_id, batch_number=1, file_path=...)
        ml.log_batch_complete(run_id, batch_number=1, job_id=..., state=...)
        ml.log_run_complete(run_id, status="success", ...)
    """

    def __init__(self, postgres_conn_id: str = "airflow_db"):
        self.postgres_conn_id = postgres_conn_id
        self._hook = None

    def _get_hook(self):
        if self._hook is None:
            from airflow.providers.postgres.hooks.postgres import PostgresHook

            self._hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        return self._hook

    def _execute(self, operation: str, sql: str, parameters: dict) -> bool:
        """Execute SQL with fail-safe. Returns True on success."""
        try:
            hook = self._get_hook()
            hook.run(sql, parameters=parameters)
            return True
        except Exception as e:
            logger.warning(f"Migration log [{operation}] failed: {e}")
            return False

    # ------------------------------------------------------------------
    # Run-level logging
    # ------------------------------------------------------------------

    def log_run_start(
        self,
        run_id: str,
        dag_id: str,
        table_name: str = "",
        sf_object: str = "",
        operation: str = "upsert",
        execution_date: Optional[datetime] = None,
        total_records: int = 0,
        total_batches: int = 0,
        batch_size: int = 0,
        start_batch: int = 1,
        dag_conf: Optional[dict] = None,
    ) -> bool:
        """INSERT migration.runs with status='running'."""
        sql = """
            INSERT INTO migration.runs (
                run_id, dag_id, table_name, sf_object, operation,
                execution_date, start_time, status,
                total_records, total_batches, batch_size, start_batch,
                dag_conf
            ) VALUES (
                %(run_id)s, %(dag_id)s, %(table_name)s, %(sf_object)s, %(operation)s,
                %(execution_date)s, %(start_time)s, 'running',
                %(total_records)s, %(total_batches)s, %(batch_size)s, %(start_batch)s,
                %(dag_conf)s
            )
            ON CONFLICT (run_id) DO UPDATE SET
                table_name      = EXCLUDED.table_name,
                sf_object       = EXCLUDED.sf_object,
                operation       = EXCLUDED.operation,
                start_time      = EXCLUDED.start_time,
                status          = 'running',
                total_records   = EXCLUDED.total_records,
                total_batches   = EXCLUDED.total_batches,
                batch_size      = EXCLUDED.batch_size,
                start_batch     = EXCLUDED.start_batch,
                dag_conf        = EXCLUDED.dag_conf,
                updated_at      = CURRENT_TIMESTAMP
        """
        params = {
            "run_id": run_id,
            "dag_id": dag_id,
            "table_name": table_name,
            "sf_object": sf_object,
            "operation": operation,
            "execution_date": execution_date,
            "start_time": datetime.utcnow(),
            "total_records": total_records,
            "total_batches": total_batches,
            "batch_size": batch_size,
            "start_batch": start_batch,
            "dag_conf": json.dumps(dag_conf) if dag_conf else None,
        }
        return self._execute("log_run_start", sql, params)

    def log_run_complete(
        self,
        run_id: str,
        status: str,
        total_processed: int = 0,
        total_failed: int = 0,
        error_message: Optional[str] = None,
    ) -> bool:
        """UPDATE migration.runs with final status."""
        sql = """
            UPDATE migration.runs
            SET end_time        = %(end_time)s,
                status          = %(status)s,
                total_processed = %(total_processed)s,
                total_failed    = %(total_failed)s,
                error_message   = %(error_message)s,
                updated_at      = CURRENT_TIMESTAMP
            WHERE run_id = %(run_id)s
        """
        params = {
            "run_id": run_id,
            "end_time": datetime.utcnow(),
            "status": status,
            "total_processed": total_processed,
            "total_failed": total_failed,
            "error_message": error_message,
        }
        return self._execute("log_run_complete", sql, params)

    # ------------------------------------------------------------------
    # Batch-level logging
    # ------------------------------------------------------------------

    def log_batch_start(
        self,
        run_id: str,
        batch_number: int,
        file_path: str = "",
        records_in_batch: int = 0,
    ) -> bool:
        """INSERT migration.batch_logs with state='uploading'."""
        sql = """
            INSERT INTO migration.batch_logs (
                run_id, batch_number, file_path, state,
                records_in_batch, start_time
            ) VALUES (
                %(run_id)s, %(batch_number)s, %(file_path)s, 'uploading',
                %(records_in_batch)s, %(start_time)s
            )
            ON CONFLICT ON CONSTRAINT uq_run_batch DO UPDATE SET
                file_path        = EXCLUDED.file_path,
                state            = 'uploading',
                records_in_batch = EXCLUDED.records_in_batch,
                start_time       = EXCLUDED.start_time,
                updated_at       = CURRENT_TIMESTAMP
        """
        params = {
            "run_id": run_id,
            "batch_number": batch_number,
            "file_path": file_path,
            "records_in_batch": records_in_batch,
            "start_time": datetime.utcnow(),
        }
        return self._execute("log_batch_start", sql, params)

    def log_batch_complete(
        self,
        run_id: str,
        batch_number: int,
        job_id: Optional[str] = None,
        state: str = "JobComplete",
        records_processed: int = 0,
        records_failed: int = 0,
        error_message: Optional[str] = None,
    ) -> bool:
        """UPDATE migration.batch_logs with job result."""
        sql = """
            UPDATE migration.batch_logs
            SET job_id            = %(job_id)s,
                state             = %(state)s,
                records_processed = %(records_processed)s,
                records_failed    = %(records_failed)s,
                end_time          = %(end_time)s,
                error_message     = %(error_message)s,
                updated_at        = CURRENT_TIMESTAMP
            WHERE run_id = %(run_id)s AND batch_number = %(batch_number)s
        """
        params = {
            "run_id": run_id,
            "batch_number": batch_number,
            "job_id": job_id,
            "state": state,
            "records_processed": records_processed,
            "records_failed": records_failed,
            "end_time": datetime.utcnow(),
            "error_message": error_message,
        }
        return self._execute("log_batch_complete", sql, params)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_run_summary(self, run_id: str) -> Optional[dict]:
        """Get run summary from migration.v_summary view."""
        try:
            hook = self._get_hook()
            sql = "SELECT * FROM migration.v_summary WHERE run_id = %s"
            rows = hook.get_records(sql, parameters=(run_id,))
            if not rows:
                return None

            columns = [
                "run_id", "dag_id", "table_name", "sf_object", "operation",
                "execution_date", "start_time", "end_time", "duration_minutes",
                "status", "total_records", "total_batches", "batch_size",
                "total_processed", "total_failed", "success_rate_pct",
                "start_batch", "error_message",
                "logged_batches", "completed_batches", "failed_batches",
                "created_at",
            ]
            return dict(zip(columns, rows[0]))
        except Exception as e:
            logger.warning(f"Migration log [get_run_summary] failed: {e}")
            return None
