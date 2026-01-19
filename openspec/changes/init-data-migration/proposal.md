# Proposal: Init Data Migration

## Summary

Initialize the KPC TMS Data Migration project by scaffolding the Airflow DAGs, Oracle extraction logic, Salesforce loading integration, and reconciliation processes. This proposal aligns the codebase with the architecture and pipeline design documented in `docs/`.

## Motivation

The project currently requires a robust, scalable ETL pipeline to migrate ~783M historical records from an on-premise Oracle Database to Salesforce. While the architecture and design are documented in `docs/ARCHITECTURE.md` and `docs/PIPELINE_DESIGN.md`, the actual implementation code (DAGs, plugins, scripts) is missing. This proposal aims to implement the core foundation for this migration.

## Goals

- **Extract**: Implement efficient Oracle extraction using Parallel Query and `ROWNUM` chunking.
- **Transform**: Implement Python/Pandas based transformation logic for field mapping and formatting.
- **Load**: Integration with Salesforce Bulk API 2.0 via Data Loader CLI or Python `requests` for high-volume loading.
- **Reconcile**: Implement a reconciliation DAG to compare record counts and sample checksums between Oracle and Salesforce.
- **Orchestrate**: Establish the Master DAG (`kpc_tms_migration_master`) and a DAG Factory pattern for auto-generating table-specific DAGs.

## Non-Goals

- **Real-time Synchronization**: This proposal focuses solely on historical data migration, not day-to-day CDC.
- **UI Development**: No custom UI beyond standard Airflow/Jenkins dashboards.
