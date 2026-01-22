# Proposal: ETL Data from TMS Oracle to Salesforce (Sample Table)

## Goal

Implement a sample Airflow DAG to demonstrate the end-to-end ETL process from Oracle (On-Premise) to Salesforce (Cloud) using `KPS_T_SALES_MD` as the pilot table.

## Context

The project requires migrating large volumes of data using Salesforce Data Loader. We have already prepared the Data Loader configuration strategy and setup (`salesforce/` directory). This proposal focuses on orchestrating this process in Airflow.

## Scope

- Create a new DAG `migrate_sample_kps_t_sales_md` in `dags/sample_migration_dag.py`.
- Implement Extraction Task: Python execution to query Oracle and save to CSV.
- Implement Transformation Task: Ensure CSV format matches `.sdl` requirements.
- Implement Loading Task: Bash execution of Salesforce Data Loader via `process.sh`.
- Use the configurations defined in `salesforce/dataloader_conf/`.

## Success Criteria

- The DAG runs successfully in Airflow.
- Data from Oracle `KPS_T_SALES_MD` (limited rows for sample) is extracted to CSV.
- Data Loader runs without critical errors.
- Records appear in Salesforce (or staging object).
