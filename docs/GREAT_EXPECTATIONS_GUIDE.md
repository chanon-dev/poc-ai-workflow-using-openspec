# Great Expectations (GX) Integration Guide

## Overview: ใช้ GX ตอนไหน?

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         DATA MIGRATION WITH GREAT EXPECTATIONS                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ORACLE                                                              SALESFORCE    │
│   ┌─────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────┐    ┌─────┐      │
│   │SOURCE│───▶│ EXTRACT │───▶│TRANSFORM│───▶│  STAGE  │───▶│ LOAD │───▶│TARGET│     │
│   └─────┘    └─────────┘    └─────────┘    └─────────┘    └─────┘    └─────┘      │
│      │            │              │              │                         │         │
│      ▼            ▼              ▼              ▼                         ▼         │
│   ┌─────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐              ┌─────────┐   │
│   │ GX  │    │   GX    │    │   GX    │    │   GX    │              │   GX    │   │
│   │CHECK│    │  CHECK  │    │  CHECK  │    │  CHECK  │              │  CHECK  │   │
│   │POINT│    │  POINT  │    │  POINT  │    │  POINT  │              │  POINT  │   │
│   │  1  │    │    2    │    │    3    │    │    4    │              │    5    │   │
│   └─────┘    └─────────┘    └─────────┘    └─────────┘              └─────────┘   │
│                                                                                      │
│   Pre-Mig    Post-Extract  Post-Transform  Pre-Load                 Post-Mig       │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## GX Checkpoints Summary

| Checkpoint | เมื่อไหร่ | ทำไม | ต้องทำ? |
| --- | --- | --- | --- |
| **1. Source Validation** | ก่อน Extract | รู้ data quality ของ source | ✅ MUST |
| **2. Post-Extract** | หลัง Extract | ตรวจ extract ครบไหม | 🟡 Recommended |
| **3. Post-Transform** | หลัง Transform | ตรวจ mapping ถูกไหม | ✅ MUST |
| **4. Pre-Load** | ก่อน Load to SF | ตรวจ SF constraints | ✅ MUST |
| **5. Post-Migration** | หลัง Load เสร็จ | Final reconciliation | ✅ MUST |

---

## Installation & Setup

### 1. Install Great Expectations

```bash
# Install GX
pip install great_expectations

# With Airflow provider
pip install airflow-provider-great-expectations

# Initialize GX project
cd /opt/airflow
great_expectations init
```

### 2. Project Structure

```text
kpc-tms-data-migration/
├── great_expectations/
│   ├── great_expectations.yml      # Main config
│   ├── expectations/               # Expectation suites
│   │   ├── source_kps_t_sales_md.json
│   │   ├── transform_kps_t_sales_md.json
│   │   ├── preload_kps_t_sales_md.json
│   │   └── postmig_kps_t_sales_md.json
│   ├── checkpoints/                # Checkpoint configs
│   │   ├── source_checkpoint.yml
│   │   ├── transform_checkpoint.yml
│   │   └── preload_checkpoint.yml
│   ├── plugins/                    # Custom expectations
│   │   └── salesforce_expectations.py
│   └── uncommitted/
│       └── data_docs/              # Generated reports
├── dags/
└── ...
```

### 3. Configure Data Sources

```yaml
# great_expectations/great_expectations.yml

datasources:
  # Oracle Source
  oracle_kpc:
    class_name: Datasource
    execution_engine:
      class_name: SqlAlchemyExecutionEngine
      connection_string: oracle+cx_oracle://user:pass@host:1521/?service_name=KPCPROD
    data_connectors:
      default_inferred_data_connector:
        class_name: InferredAssetSqlDataConnector

  # Staging CSV Files
  staging_filesystem:
    class_name: Datasource
    execution_engine:
      class_name: PandasExecutionEngine
    data_connectors:
      staging_connector:
        class_name: InferredAssetFilesystemDataConnector
        base_directory: /data/staging
        default_regex:
          pattern: (.*)\.csv
          group_names:
            - data_asset_name

  # Salesforce (via exported data)
  salesforce_export:
    class_name: Datasource
    execution_engine:
      class_name: PandasExecutionEngine
    data_connectors:
      sf_connector:
        class_name: ConfiguredAssetFilesystemDataConnector
        base_directory: /data/sf_exports
```

---

## Checkpoint 1: Source Validation (Pre-Migration)

### Purpose

- Understand data quality before migration
- Identify issues early (nulls, duplicates, invalid values)
- Create baseline metrics

### Expectation Suite

```python
# scripts/create_source_expectations.py

import great_expectations as gx

context = gx.get_context()

# Create expectation suite for KPS_T_SALES_MD
suite = context.add_expectation_suite("source_kps_t_sales_md")

# Get batch for profiling
batch_request = {
    "datasource_name": "oracle_kpc",
    "data_connector_name": "default_inferred_data_connector",
    "data_asset_name": "KPS_T_SALES_MD",
}

validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="source_kps_t_sales_md"
)

# ==================== Primary Key Expectations ====================

# SALES_ID must not be null (required for External ID)
validator.expect_column_values_to_not_be_null(
    column="SALES_ID",
    meta={"severity": "critical", "notes": "Required for SF External ID"}
)

# SALES_ID must be unique
validator.expect_column_values_to_be_unique(
    column="SALES_ID",
    meta={"severity": "critical"}
)

# ==================== Foreign Key Expectations ====================

# TENANT_CODE should exist (for lookup)
validator.expect_column_values_to_not_be_null(
    column="TENANT_CODE",
    mostly=0.99,  # Allow 1% null
    meta={"severity": "warning"}
)

# ==================== Data Type Expectations ====================

# SALES_AMOUNT should be numeric
validator.expect_column_values_to_be_of_type(
    column="SALES_AMOUNT",
    type_="NUMBER"
)

# SALES_AMOUNT should be positive (or zero)
validator.expect_column_values_to_be_between(
    column="SALES_AMOUNT",
    min_value=0,
    max_value=999999999.99,
    mostly=0.999,
    meta={"severity": "warning", "notes": "Negative amounts may be returns"}
)

# ==================== Date Expectations ====================

# SALES_DATE should be within valid range
validator.expect_column_values_to_be_between(
    column="SALES_DATE",
    min_value="2020-01-01",
    max_value="2025-12-31",
    parse_strings_as_datetimes=True,
    meta={"severity": "warning"}
)

# CREATED_DATE should not be in future
validator.expect_column_values_to_be_between(
    column="CREATED_DATE",
    max_value="{{current_date}}",
    parse_strings_as_datetimes=True
)

# ==================== String Length Expectations ====================

# Description should fit SF field (32KB limit)
validator.expect_column_value_lengths_to_be_between(
    column="DESCRIPTION",
    max_value=32000,
    mostly=0.999,
    meta={"severity": "warning", "notes": "Will be truncated if exceeds"}
)

# ==================== Table Level Expectations ====================

# Table should have expected row count (sanity check)
validator.expect_table_row_count_to_be_between(
    min_value=80000000,  # 80M minimum
    max_value=300000000,  # 300M maximum
    meta={"notes": "Expected ~87M per year, 3 years = ~261M"}
)

# Column set should match expected
validator.expect_table_columns_to_match_set(
    column_set=[
        "SALES_ID", "TENANT_CODE", "STORE_CODE", "SALES_DATE",
        "SALES_AMOUNT", "TAX_AMOUNT", "DISCOUNT_AMOUNT", "NET_AMOUNT",
        "PAYMENT_TYPE", "DESCRIPTION", "CREATED_DATE", "UPDATED_DATE"
    ],
    exact_match=False  # Allow additional columns
)

# Save the suite
validator.save_expectation_suite(discard_failed_expectations=False)
```

### Run Source Validation

```python
# dags/tasks/source_validation.py

from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator
)

source_validation = GreatExpectationsOperator(
    task_id="validate_source_data",
    data_context_root_dir="/opt/airflow/great_expectations",
    checkpoint_name="source_kps_t_sales_md_checkpoint",
    return_json_dict=True,
    fail_task_on_validation_failure=True,  # Stop migration if critical fails
)
```

---

## Checkpoint 2: Post-Extract Validation

### Purpose

- Verify extraction completeness
- Compare counts with source
- Check for truncation issues

```python
# scripts/create_extract_expectations.py

suite = context.add_expectation_suite("extract_kps_t_sales_md")

validator = context.get_validator(
    batch_request={
        "datasource_name": "staging_filesystem",
        "data_connector_name": "staging_connector",
        "data_asset_name": "KPS_T_SALES_MD_chunk_*",
    },
    expectation_suite_name="extract_kps_t_sales_md"
)

# Row count should match source (pass via parameter)
validator.expect_table_row_count_to_equal(
    value={"$PARAMETER": "source_count"},
    meta={"notes": "Must match Oracle source count"}
)

# All chunks should have data
validator.expect_table_row_count_to_be_between(
    min_value=1,
    meta={"severity": "critical", "notes": "Empty chunk indicates extraction failure"}
)

# Key columns preserved
validator.expect_column_values_to_not_be_null(
    column="SALES_ID"
)

validator.save_expectation_suite()
```

---

## Checkpoint 3: Post-Transform Validation

### Purpose

- Verify field mappings correct
- Check data type conversions
- Validate SF-specific formats

```python
# scripts/create_transform_expectations.py

suite = context.add_expectation_suite("transform_kps_t_sales_md")

validator = context.get_validator(
    batch_request={
        "datasource_name": "staging_filesystem",
        "data_connector_name": "staging_connector",
        "data_asset_name": "KPS_T_SALES_MD_transformed",
    },
    expectation_suite_name="transform_kps_t_sales_md"
)

# ==================== Column Mapping Validation ====================

# Columns should be renamed to SF field names
validator.expect_table_columns_to_match_set(
    column_set=[
        "External_ID__c", "Tenant_Code__c", "Store_Code__c",
        "Sales_Date__c", "Sales_Amount__c", "Tax_Amount__c",
        "Discount_Amount__c", "Net_Amount__c", "Payment_Type__c",
        "Description__c", "Oracle_Created_Date__c", "Oracle_Updated_Date__c"
    ]
)

# ==================== Date Format Validation ====================

# Dates should be in SF ISO format
validator.expect_column_values_to_match_regex(
    column="Sales_Date__c",
    regex=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$",
    mostly=0.999,
    meta={"notes": "SF datetime format: YYYY-MM-DDTHH:MM:SS.000Z"}
)

# ==================== Numeric Precision Validation ====================

# Amounts should have max 2 decimal places
validator.expect_column_values_to_match_regex(
    column="Sales_Amount__c",
    regex=r"^-?\d+(\.\d{1,2})?$",
    mostly=0.999
)

# ==================== Text Length Validation (SF Limits) ====================

# Text fields should not exceed SF limits
validator.expect_column_value_lengths_to_be_between(
    column="Description__c",
    max_value=32000,  # SF Long Text Area limit
    meta={"severity": "critical"}
)

validator.expect_column_value_lengths_to_be_between(
    column="Tenant_Code__c",
    max_value=255,  # SF Text field limit
)

# ==================== Row Count Preservation ====================

# No records lost during transform
validator.expect_table_row_count_to_equal(
    value={"$PARAMETER": "extract_count"}
)

validator.save_expectation_suite()
```

---

## Checkpoint 4: Pre-Load Validation (SF Constraints)

### Purpose

- Validate data meets ALL Salesforce requirements
- Prevent load failures
- Check lookup references exist

```python
# scripts/create_preload_expectations.py

suite = context.add_expectation_suite("preload_kps_t_sales_md")

validator = context.get_validator(
    batch_request={
        "datasource_name": "staging_filesystem",
        "data_connector_name": "staging_connector",
        "data_asset_name": "KPS_T_SALES_MD_final",
    },
    expectation_suite_name="preload_kps_t_sales_md"
)

# ==================== Salesforce Required Fields ====================

# External ID is mandatory
validator.expect_column_values_to_not_be_null(
    column="External_ID__c",
    meta={"severity": "critical", "sf_error": "REQUIRED_FIELD_MISSING"}
)

# ==================== Salesforce Field Types ====================

# Checkbox fields must be true/false
validator.expect_column_values_to_be_in_set(
    column="Is_Void__c",
    value_set=[True, False, "true", "false", None],
    meta={"sf_field_type": "Checkbox"}
)

# Picklist values must be valid
validator.expect_column_values_to_be_in_set(
    column="Payment_Type__c",
    value_set=["Cash", "Credit Card", "Transfer", "QR", "Other", None],
    mostly=0.999,
    meta={"sf_field_type": "Picklist"}
)

# ==================== Salesforce Lookup References ====================

# Tenant lookup should have valid reference
# (Pre-check: load tenant External IDs from SF)
validator.expect_column_values_to_be_in_set(
    column="Tenant_Code__c",
    value_set={"$PARAMETER": "valid_tenant_codes"},
    mostly=0.999,
    meta={"severity": "warning", "sf_error": "INVALID_CROSS_REFERENCE_KEY"}
)

# ==================== Salesforce String Limits ====================

SF_FIELD_LIMITS = {
    "External_ID__c": 255,
    "Tenant_Code__c": 255,
    "Store_Code__c": 80,
    "Payment_Type__c": 255,
}

for field, limit in SF_FIELD_LIMITS.items():
    validator.expect_column_value_lengths_to_be_between(
        column=field,
        max_value=limit,
        meta={"sf_error": "STRING_TOO_LONG"}
    )

# ==================== Salesforce Number Limits ====================

# Currency fields: 16 digits, 2 decimal places
validator.expect_column_values_to_be_between(
    column="Sales_Amount__c",
    min_value=-9999999999999.99,
    max_value=9999999999999.99,
    meta={"sf_field_type": "Currency"}
)

# ==================== No Duplicate External IDs ====================

validator.expect_column_values_to_be_unique(
    column="External_ID__c",
    meta={"severity": "critical", "sf_error": "DUPLICATE_EXTERNAL_ID"}
)

validator.save_expectation_suite()
```

---

## Checkpoint 5: Post-Migration Validation

### Purpose

- Final reconciliation
- Verify data integrity
- Business rule validation

```python
# scripts/create_postmig_expectations.py

# Export SF data for validation
# sf data export -q "SELECT Id, External_ID__c, Sales_Amount__c FROM KPS_Sales__c"

suite = context.add_expectation_suite("postmig_kps_t_sales_md")

validator = context.get_validator(
    batch_request={
        "datasource_name": "salesforce_export",
        "data_connector_name": "sf_connector",
        "data_asset_name": "KPS_Sales__c_export",
    },
    expectation_suite_name="postmig_kps_t_sales_md"
)

# ==================== Record Count Match ====================

validator.expect_table_row_count_to_equal(
    value={"$PARAMETER": "source_count"},
    meta={"severity": "critical", "notes": "SF count must match Oracle source"}
)

# ==================== Aggregate Match ====================

# Sum of amounts should match
validator.expect_column_sum_to_be_between(
    column="Sales_Amount__c",
    min_value={"$PARAMETER": "source_sum * 0.9999"},  # Allow 0.01% variance
    max_value={"$PARAMETER": "source_sum * 1.0001"},
)

# ==================== Distribution Match ====================

# Record distribution by date should be similar
validator.expect_column_median_to_be_between(
    column="Sales_Amount__c",
    min_value={"$PARAMETER": "source_median * 0.95"},
    max_value={"$PARAMETER": "source_median * 1.05"},
)

validator.save_expectation_suite()
```

---

## Airflow Integration

### GX Operator in DAG

```python
# dags/migrate_with_gx.py

from datetime import datetime
from airflow.sdk import DAG, task
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator
)
from airflow.operators.python import BranchPythonOperator

GX_ROOT_DIR = "/opt/airflow/great_expectations"

default_args = {
    "owner": "data-team",
    "retries": 1,
}

with DAG(
    dag_id="migrate_kps_t_sales_md_with_gx",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["migration", "gx"],
) as dag:

    # ==================== Checkpoint 1: Source Validation ====================

    validate_source = GreatExpectationsOperator(
        task_id="validate_source",
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="source_kps_t_sales_md_checkpoint",
        return_json_dict=True,
        fail_task_on_validation_failure=False,  # Continue but log
    )

    @task()
    def check_source_validation(validation_result: dict) -> str:
        """Decide whether to proceed based on validation results"""
        success = validation_result.get("success", False)
        stats = validation_result.get("statistics", {})

        critical_failures = [
            r for r in validation_result.get("results", [])
            if not r["success"] and r.get("meta", {}).get("severity") == "critical"
        ]

        if critical_failures:
            # Log critical issues
            for failure in critical_failures:
                print(f"CRITICAL: {failure['expectation_config']['expectation_type']}")
            return "abort_migration"

        if stats.get("success_percent", 0) < 95:
            return "review_and_proceed"

        return "proceed_extraction"

    source_decision = check_source_validation(validate_source.output)

    # ==================== Extract Phase ====================

    @task()
    def extract_data():
        """Extract data from Oracle"""
        # ... extraction logic
        return {"count": 261000000, "file_path": "/data/staging/extracted.csv"}

    extracted = extract_data()

    # ==================== Checkpoint 2: Post-Extract Validation ====================

    validate_extract = GreatExpectationsOperator(
        task_id="validate_extract",
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="extract_checkpoint",
        checkpoint_kwargs={
            "expectation_suite_parameters": {
                "source_count": "{{ ti.xcom_pull(task_ids='extract_data')['count'] }}"
            }
        },
        fail_task_on_validation_failure=True,
    )

    # ==================== Transform Phase ====================

    @task()
    def transform_data(extract_result: dict):
        """Transform data for Salesforce"""
        # ... transformation logic
        return {"count": extract_result["count"], "file_path": "/data/staging/transformed.csv"}

    transformed = transform_data(extracted)

    # ==================== Checkpoint 3: Post-Transform Validation ====================

    validate_transform = GreatExpectationsOperator(
        task_id="validate_transform",
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="transform_checkpoint",
        fail_task_on_validation_failure=True,
    )

    # ==================== Checkpoint 4: Pre-Load Validation ====================

    @task()
    def fetch_sf_lookup_values():
        """Fetch valid lookup values from Salesforce"""
        # Query SF for valid Tenant codes, Store codes, etc.
        return {
            "valid_tenant_codes": ["T001", "T002", "T003", ...],
            "valid_store_codes": ["S001", "S002", ...],
        }

    lookup_values = fetch_sf_lookup_values()

    validate_preload = GreatExpectationsOperator(
        task_id="validate_preload",
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="preload_checkpoint",
        checkpoint_kwargs={
            "expectation_suite_parameters": {
                "valid_tenant_codes": "{{ ti.xcom_pull(task_ids='fetch_sf_lookup_values')['valid_tenant_codes'] }}"
            }
        },
        fail_task_on_validation_failure=True,  # MUST pass before loading
    )

    # ==================== Load Phase ====================

    @task()
    def load_to_salesforce(transform_result: dict):
        """Load data to Salesforce"""
        # ... Bulk API loading
        return {"success_count": 260995000, "failed_count": 5000}

    loaded = load_to_salesforce(transformed)

    # ==================== Checkpoint 5: Post-Migration Validation ====================

    @task()
    def export_sf_data_for_validation():
        """Export SF data for final validation"""
        # Use sf data export or Bulk API query
        return "/data/sf_exports/KPS_Sales__c_export.csv"

    sf_export = export_sf_data_for_validation()

    validate_postmig = GreatExpectationsOperator(
        task_id="validate_postmigration",
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="postmig_checkpoint",
        fail_task_on_validation_failure=False,  # Log results, don't fail
    )

    # ==================== Generate Report ====================

    @task()
    def generate_gx_report(validation_results: list):
        """Generate final GX Data Docs report"""
        context = gx.get_context()
        context.build_data_docs()
        return "http://localhost:8080/great_expectations/data_docs/index.html"

    report = generate_gx_report([
        validate_source.output,
        validate_extract.output,
        validate_transform.output,
        validate_preload.output,
        validate_postmig.output,
    ])

    # ==================== DAG Flow ====================

    validate_source >> source_decision
    source_decision >> extracted >> validate_extract
    validate_extract >> transformed >> validate_transform
    validate_transform >> lookup_values >> validate_preload
    validate_preload >> loaded >> sf_export >> validate_postmig
    validate_postmig >> report
```

---

## Custom Salesforce Expectations

```python
# great_expectations/plugins/salesforce_expectations.py

from great_expectations.expectations.expectation import ColumnMapExpectation
from great_expectations.expectations.metrics import column_map_metric

class ExpectColumnValuesToBeValidSalesforceId(ColumnMapExpectation):
    """Expect column values to be valid Salesforce 15 or 18 character IDs"""

    expectation_type = "expect_column_values_to_be_valid_salesforce_id"

    @column_map_metric
    def _validate(cls, column, **kwargs):
        import re
        sf_id_pattern = re.compile(r'^[a-zA-Z0-9]{15}([a-zA-Z0-9]{3})?$')
        return column.apply(lambda x: bool(sf_id_pattern.match(str(x))) if x else True)


class ExpectColumnValuesToBeValidExternalId(ColumnMapExpectation):
    """Expect column values to be valid for SF External ID field"""

    expectation_type = "expect_column_values_to_be_valid_external_id"

    @column_map_metric
    def _validate(cls, column, **kwargs):
        def is_valid(value):
            if value is None:
                return False
            s = str(value)
            # No leading/trailing spaces
            if s != s.strip():
                return False
            # Max 255 chars
            if len(s) > 255:
                return False
            # No newlines
            if '\n' in s or '\r' in s:
                return False
            return True

        return column.apply(is_valid)


class ExpectColumnSumToMatchSource(ColumnMapExpectation):
    """Expect column sum to match source system within tolerance"""

    expectation_type = "expect_column_sum_to_match_source"

    def _validate(
        self,
        metrics,
        runtime_configuration=None,
        execution_engine=None,
    ):
        source_sum = self.configuration.expectation_config.kwargs.get("source_sum")
        tolerance = self.configuration.expectation_config.kwargs.get("tolerance", 0.0001)

        actual_sum = metrics["column.sum"]

        variance = abs(actual_sum - source_sum) / source_sum if source_sum else 0

        return {
            "success": variance <= tolerance,
            "result": {
                "actual_sum": actual_sum,
                "source_sum": source_sum,
                "variance_percent": variance * 100,
                "tolerance_percent": tolerance * 100,
            }
        }
```

---

## GX Data Docs Report

### Auto-Generated Documentation

GX generates beautiful HTML reports showing:

1. **Validation Results** - Pass/Fail for each expectation
2. **Data Profiling** - Column statistics, distributions
3. **Historical Runs** - Compare across migration runs
4. **Expectation Docs** - What each check validates

### Access Data Docs

```bash
# Build data docs
great_expectations docs build

# Serve locally
great_expectations docs serve

# Or access via Airflow web server
# http://localhost:8080/great_expectations/data_docs/index.html
```

---

## Summary: When to Use GX

| Checkpoint | Required | Blocks Migration? | Severity |
| --- | --- | --- | --- |
| **1. Source Validation** | ✅ Yes | ⚠️ Warning only | Know your data |
| **2. Post-Extract** | 🟡 Optional | ✅ Yes if fails | Extraction issues |
| **3. Post-Transform** | ✅ Yes | ✅ Yes if fails | Mapping errors |
| **4. Pre-Load** | ✅ Yes | ✅ Yes if fails | Prevent SF errors |
| **5. Post-Migration** | ✅ Yes | ⚠️ Warning only | Final verification |

### Benefits of Using GX

| Benefit | Description |
| --- | --- |
| **Early Detection** | Find issues before they cause load failures |
| **Documentation** | Auto-generated data docs for audit |
| **Reusability** | Same expectations for all migration runs |
| **CI/CD Integration** | Run validations in pipelines |
| **Historical Tracking** | Compare quality across runs |

### GX vs Manual Validation

| Aspect | Manual SQL | Great Expectations |
| --- | --- | --- |
| Setup time | Low | Medium |
| Maintenance | High | Low |
| Documentation | Manual | Auto-generated |
| Reusability | Copy-paste | Built-in |
| Reporting | Custom | Data Docs |
| Historical | Manual | Built-in |
| Integration | Custom | Airflow provider |
