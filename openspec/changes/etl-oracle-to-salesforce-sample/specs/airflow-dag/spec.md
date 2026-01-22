# Spec: Airflow DAG for Sample ETL

## ADDED Requirements

### Requirement: Orchestrated Migration Flow

The system MUST provide an Airflow DAG that manages the end-to-end migration process for a sample table, ensuring all steps from extraction to archiving are executed in order.

#### Scenario: Sample Migration Execution

Given the Airflow environment is running
And the Oracle database is accessible
And the Salesforce Data Loader is configured
When the `migrate_sample_kps_t_sales_md` DAG is triggered
Then it should extract data from `KPS_T_SALES_MD` table
And transform it to a CSV file in `${AIRFLOW_HOME}/salesforce/data/`
And generate the Data Loader configuration files
And execute the Salesforce Data Loader `process.sh`
And archive the result logs

## ADDED Requirements (Error Handling)

### Requirement: Failure Detection

The system MUST detect failures at both the Airflow task level and the Data Loader application level (e.g., partial failures in CSV logs) and report them appropriately.

#### Scenario: Extraction Failure

Given the Oracle connection is down
When the extraction task runs
Then the task should fail
And an alert should be logged

#### Scenario: Data Loader Failure

Given the Data Loader process exits with specific error messages in `status-error.csv`
Then the `audit_results` task should detect the errors
And fail the DAG run
