-- Migration Logging Tables
-- ใช้เก็บ structured log สำหรับ track migration progress
-- รันใน Airflow metadata DB (PostgreSQL)
--
-- Schema: "migration" (แยกจาก public เพื่อไม่ปนกับ Airflow internal tables)
--
-- Usage:
--   docker cp sql/init_migration_logging.sql <postgres-container>:/tmp/
--   docker compose exec postgres psql -U airflow -d airflow -f /tmp/init_migration_logging.sql
--
-- Safe to re-run (uses IF NOT EXISTS)

-- ============================================================
-- Schema: migration
-- ============================================================
CREATE SCHEMA IF NOT EXISTS migration;

-- ============================================================
-- Table: migration.runs (1 row ต่อ 1 DAG run)
-- ============================================================
CREATE TABLE IF NOT EXISTS migration.runs (
    run_id              VARCHAR(250) PRIMARY KEY,
    dag_id              VARCHAR(250) NOT NULL,
    table_name          VARCHAR(100),
    sf_object           VARCHAR(100),
    operation           VARCHAR(50),
    execution_date      TIMESTAMP WITH TIME ZONE,
    start_time          TIMESTAMP WITH TIME ZONE,
    end_time            TIMESTAMP WITH TIME ZONE,
    status              VARCHAR(50) DEFAULT 'running',
    total_records       INTEGER DEFAULT 0,
    total_batches       INTEGER DEFAULT 0,
    batch_size          INTEGER DEFAULT 0,
    total_processed     INTEGER DEFAULT 0,
    total_failed        INTEGER DEFAULT 0,
    start_batch         INTEGER DEFAULT 1,
    error_message       TEXT,
    dag_conf            JSONB,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_runs_dag_id
    ON migration.runs(dag_id);
CREATE INDEX IF NOT EXISTS idx_runs_table_name
    ON migration.runs(table_name);
CREATE INDEX IF NOT EXISTS idx_runs_status
    ON migration.runs(status);
CREATE INDEX IF NOT EXISTS idx_runs_created_at
    ON migration.runs(created_at DESC);

-- ============================================================
-- Table: migration.batch_logs (1 row ต่อ 1 batch/job)
-- ============================================================
CREATE TABLE IF NOT EXISTS migration.batch_logs (
    id                  SERIAL PRIMARY KEY,
    run_id              VARCHAR(250) NOT NULL,
    batch_number        INTEGER NOT NULL,
    job_id              VARCHAR(100),
    file_path           TEXT,
    state               VARCHAR(50) DEFAULT 'pending',
    records_in_batch    INTEGER DEFAULT 0,
    records_processed   INTEGER DEFAULT 0,
    records_failed      INTEGER DEFAULT 0,
    start_time          TIMESTAMP WITH TIME ZONE,
    end_time            TIMESTAMP WITH TIME ZONE,
    error_message       TEXT,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_batch_run
        FOREIGN KEY (run_id) REFERENCES migration.runs(run_id)
        ON DELETE CASCADE
);

-- Unique constraint สำหรับ ON CONFLICT upsert (resume/retry)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'uq_run_batch'
    ) THEN
        ALTER TABLE migration.batch_logs
            ADD CONSTRAINT uq_run_batch UNIQUE (run_id, batch_number);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_batch_logs_run_id
    ON migration.batch_logs(run_id);
CREATE INDEX IF NOT EXISTS idx_batch_logs_job_id
    ON migration.batch_logs(job_id);
CREATE INDEX IF NOT EXISTS idx_batch_logs_state
    ON migration.batch_logs(state);

-- ============================================================
-- View: migration.v_summary
-- ============================================================
CREATE OR REPLACE VIEW migration.v_summary AS
SELECT
    r.run_id,
    r.dag_id,
    r.table_name,
    r.sf_object,
    r.operation,
    r.execution_date,
    r.start_time,
    r.end_time,
    ROUND(
        EXTRACT(EPOCH FROM (COALESCE(r.end_time, CURRENT_TIMESTAMP) - r.start_time)) / 60.0,
        2
    ) AS duration_minutes,
    r.status,
    r.total_records,
    r.total_batches,
    r.batch_size,
    r.total_processed,
    r.total_failed,
    CASE
        WHEN r.total_records > 0 THEN
            ROUND((r.total_processed::NUMERIC / r.total_records) * 100, 2)
        ELSE 0
    END AS success_rate_pct,
    r.start_batch,
    r.error_message,
    COUNT(b.id)                                               AS logged_batches,
    SUM(CASE WHEN b.state = 'JobComplete' THEN 1 ELSE 0 END) AS completed_batches,
    SUM(CASE WHEN b.state = 'Failed'      THEN 1 ELSE 0 END) AS failed_batches,
    r.created_at
FROM migration.runs r
LEFT JOIN migration.batch_logs b ON r.run_id = b.run_id
GROUP BY
    r.run_id, r.dag_id, r.table_name, r.sf_object, r.operation,
    r.execution_date, r.start_time, r.end_time, r.status,
    r.total_records, r.total_batches, r.batch_size,
    r.total_processed, r.total_failed, r.start_batch,
    r.error_message, r.created_at;
