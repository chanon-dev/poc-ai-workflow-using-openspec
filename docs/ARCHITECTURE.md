# KPC TMS Data Migration Architecture

## Overview

| Item | Detail |
| --- | --- |
| **Source** | Oracle Database (On-Premise) |
| **Target** | Salesforce (Cloud) |
| **Tool** | Salesforce Data Loader CLI |
| **Orchestration** | Apache Airflow (On-Premise) |
| **Data Volume** | ~87M records/year (largest table) |

---

## Data Volume Analysis

> **Note:** Migration includes 2-3 years of historical data (ข้อมูลย้อนหลัง 2-3 ปี)

| Table | Records/Year | 2 Years Total | 3 Years Total | Priority |
| --- | --- | --- | --- | --- |
| KPS_T_SALES_MD | 86,957,568 | **~174M** | **~261M** | Critical |
| KPS_T_SALESPAY_MD | 36,461,318 | **~73M** | **~109M** | Critical |
| KPS_T_SALES_M | 36,164,974 | **~72M** | **~108M** | Critical |
| KPS_T_SALES_APPRV_DETAIL | 178,716 | ~357K | ~536K | Medium |
| KPS_T_SALESBANK_MD | 164,120 | ~328K | ~492K | Medium |
| KPS_T_PREINV_REVSALES_D | 155,830 | ~312K | ~467K | Medium |
| KPS_T_SALES_APPRV | 44,560 | ~89K | ~134K | Low |
| KPS_WEB_SALES | 13,882 | ~28K | ~42K | Low |
| KPS_T_PREINV | 6,118 | ~12K | ~18K | Low |
| KPS_T_PREINV_DETAIL | 6,118 | ~12K | ~18K | Low |
| KPS_T_PREINV_MIN | 3,098 | ~6K | ~9K | Low |
| KPS_T_PREINV_REVGUA | 3,020 | ~6K | ~9K | Low |
| KPS_T_PREINV_REVSALES_M | 3,093 | ~6K | ~9K | Low |
| KPS_R_EMAIL_TENANT | 436 | ~872 | ~1,308 | Low |
| KPS_R_EMAIL_SUPPLIER | 4 | ~8 | ~12 | Low |
| KPS_R_POS_SUPPLIER | 4 | ~8 | ~12 | Low |

### Total Migration Volume

| Migration Scope | Total Records |
| --- | --- |
| 1 Year (Base) | **~261M** |
| 2 Years Historical | **~522M** |
| 3 Years Historical | **~783M** |

### Migration Strategy by Volume

| Volume Range | Strategy | Batch Size |
| --- | --- | --- |
| > 100M records | Parallel chunking + Multiple workers | 500K per chunk |
| 10M - 100M records | Chunking with Bulk API | 500K per chunk |
| 1M - 10M records | Single batch with Bulk API | Full table |
| < 1M records | Direct load | Full table |

---

## Recommended Tech Stack

### 1. Airflow Configuration (On-Premise)

```yaml
# Recommended Executor for On-Premise
executor: CeleryExecutor  # For parallel task execution

# Alternative for smaller setups
executor: LocalExecutor   # Single machine, multiple processes
```

**Why CeleryExecutor?**

- Handles parallel extraction from Oracle
- Scales horizontally with workers
- Better for large data volumes (87M+ records)

### 2. Required Airflow Providers

```bash
# Install required providers
pip install apache-airflow-providers-oracle      # Oracle connection
pip install apache-airflow-providers-salesforce  # Salesforce hooks
pip install apache-airflow-providers-celery      # CeleryExecutor
pip install apache-airflow-providers-redis       # Celery broker
pip install cx_Oracle                            # Oracle driver
```

### 3. Infrastructure Components

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         ON-PREMISE INFRASTRUCTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────┐ │
│  │   Oracle DB  │────▶│   Airflow    │────▶│  Staging Area (NFS/CSV)  │ │
│  │   (Source)   │     │   Workers    │     │                          │ │
│  └──────────────┘     └──────────────┘     └────────────┬─────────────┘ │
│                              │                          │                │
│                              ▼                          ▼                │
│                       ┌──────────────┐     ┌──────────────────────────┐ │
│                       │   Redis      │     │  Salesforce Data Loader  │ │
│                       │   (Broker)   │     │         CLI              │ │
│                       └──────────────┘     └────────────┬─────────────┘ │
│                                                         │                │
└─────────────────────────────────────────────────────────┼────────────────┘
                                                          │
                                                          ▼
                                              ┌──────────────────────┐
                                              │     Salesforce       │
                                              │       (Cloud)        │
                                              └──────────────────────┘
```

---

## Salesforce Data Loader CLI Setup

### Installation

```bash
# Download Data Loader
wget https://developer.salesforce.com/media/salesforce-cli/sf/channels/stable/sf-linux-x64.tar.xz

# Or use Java-based Data Loader
# Download from Salesforce Setup > Data Loader
```

### Configuration Files

**process-conf.xml** - Define operations:

```xml
<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN//EN"
  "http://www.springframework.org/dtd/spring-beans.dtd">
<beans>
  <bean id="KPS_T_SALES_MD_Upsert"
        class="com.salesforce.dataloader.process.ProcessRunner"
        singleton="false">
    <property name="name" value="KPS_T_SALES_MD_Upsert"/>
    <property name="configOverrideMap">
      <map>
        <entry key="sfdc.entity" value="KPS_Sales__c"/>
        <entry key="process.operation" value="upsert"/>
        <entry key="sfdc.externalIdField" value="External_ID__c"/>
        <entry key="dataAccess.type" value="csvRead"/>
        <entry key="dataAccess.name" value="/data/staging/KPS_T_SALES_MD.csv"/>
        <entry key="process.mappingFile" value="/config/KPS_T_SALES_MD_map.sdl"/>
        <entry key="sfdc.loadBatchSize" value="10000"/>
        <entry key="sfdc.useBulkApi" value="true"/>
        <entry key="sfdc.bulkApiSerialMode" value="false"/>
      </map>
    </property>
  </bean>
</beans>
```

**config.properties** - Salesforce connection:

```properties
sfdc.endpoint=https://login.salesforce.com
sfdc.username=your_username@company.com
sfdc.password=encrypted_password_with_token
sfdc.debugMessages=false
sfdc.timeoutSecs=600
sfdc.loadBatchSize=10000
sfdc.useBulkApi=true
process.enableLastRunDate=true
```

---

## DAG Design Pattern

### Master DAG Structure

```python
"""
KPC TMS Data Migration - Master DAG
"""
from datetime import datetime, timedelta
from airflow.sdk import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["data-team@company.com"],
}

with DAG(
    dag_id="kpc_tms_migration_master",
    default_args=default_args,
    schedule="0 2 * * *",  # Daily at 2 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["migration", "kpc", "master"],
) as dag:

    # Trigger table-specific DAGs in parallel
    trigger_sales_md = TriggerDagRunOperator(
        task_id="trigger_sales_md",
        trigger_dag_id="migrate_kps_t_sales_md",
        wait_for_completion=True,
    )

    trigger_salespay = TriggerDagRunOperator(
        task_id="trigger_salespay",
        trigger_dag_id="migrate_kps_t_salespay_md",
        wait_for_completion=True,
    )

    # Reconciliation after all migrations complete
    trigger_reconcile = TriggerDagRunOperator(
        task_id="trigger_reconciliation",
        trigger_dag_id="data_reconciliation",
        wait_for_completion=True,
    )

    [trigger_sales_md, trigger_salespay] >> trigger_reconcile
```

### Table Migration DAG (Large Tables)

```python
"""
KPC TMS - Large Table Migration with Chunking
Handles 87M+ records with batch processing
"""
from datetime import datetime, timedelta
from airflow.sdk import DAG, task
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.operators.bash import BashOperator
import pandas as pd
import os

# Configuration
TABLE_NAME = "KPS_T_SALES_MD"
CHUNK_SIZE = 500_000  # 500K records per batch
STAGING_PATH = "/data/staging"
DATALOADER_PATH = "/opt/dataloader"

default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id=f"migrate_{TABLE_NAME.lower()}",
    default_args=default_args,
    schedule=None,  # Triggered by master DAG
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_tasks=4,  # Parallel chunks
    tags=["migration", "kpc", TABLE_NAME.lower()],
) as dag:

    @task()
    def get_record_count(**context):
        """Get total records to process"""
        hook = OracleHook(oracle_conn_id="oracle_kpc")

        # Use data_interval for incremental load
        data_interval_start = context["data_interval_start"]

        sql = f"""
            SELECT COUNT(*) as cnt
            FROM {TABLE_NAME}
            WHERE UPDATED_DATE >= :start_date
        """
        result = hook.get_first(sql, parameters={"start_date": data_interval_start})
        total_records = result[0]

        # Calculate number of chunks
        num_chunks = (total_records // CHUNK_SIZE) + 1

        return {
            "total_records": total_records,
            "num_chunks": num_chunks,
            "chunk_size": CHUNK_SIZE,
        }

    @task()
    def generate_chunk_ranges(record_info: dict):
        """Generate ROWNUM ranges for parallel extraction"""
        chunks = []
        for i in range(record_info["num_chunks"]):
            start_row = i * CHUNK_SIZE + 1
            end_row = (i + 1) * CHUNK_SIZE
            chunks.append({
                "chunk_id": i,
                "start_row": start_row,
                "end_row": end_row,
            })
        return chunks

    @task()
    def extract_chunk(chunk: dict, **context):
        """Extract a single chunk from Oracle"""
        hook = OracleHook(oracle_conn_id="oracle_kpc")
        data_interval_start = context["data_interval_start"]

        sql = f"""
            SELECT * FROM (
                SELECT t.*, ROWNUM as rn
                FROM {TABLE_NAME} t
                WHERE UPDATED_DATE >= :start_date
                ORDER BY PRIMARY_KEY
            )
            WHERE rn BETWEEN :start_row AND :end_row
        """

        df = hook.get_pandas_df(
            sql,
            parameters={
                "start_date": data_interval_start,
                "start_row": chunk["start_row"],
                "end_row": chunk["end_row"],
            }
        )

        # Transform data for Salesforce
        df = transform_for_salesforce(df)

        # Save to staging
        output_file = f"{STAGING_PATH}/{TABLE_NAME}_chunk_{chunk['chunk_id']}.csv"
        df.to_csv(output_file, index=False)

        return {
            "chunk_id": chunk["chunk_id"],
            "file_path": output_file,
            "record_count": len(df),
        }

    @task()
    def load_to_salesforce(chunk_result: dict):
        """Load chunk to Salesforce using Data Loader CLI"""
        import subprocess

        # Update process-conf.xml with file path
        config_file = f"/config/{TABLE_NAME}_process.xml"

        cmd = f"""
            cd {DATALOADER_PATH} && \
            ./dataloader.sh process {config_file} {TABLE_NAME}_Upsert
        """

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(f"Data Loader failed: {result.stderr}")

        # Parse success/error files
        return parse_dataloader_results(chunk_result["chunk_id"])

    @task()
    def record_reconciliation(load_results: list):
        """Record results for reconciliation"""
        total_success = sum(r["success_count"] for r in load_results)
        total_errors = sum(r["error_count"] for r in load_results)

        # Store in metadata table or XCom
        return {
            "table": TABLE_NAME,
            "total_success": total_success,
            "total_errors": total_errors,
            "timestamp": datetime.now().isoformat(),
        }

    @task()
    def cleanup_staging(load_results: list):
        """Clean up staging files"""
        for result in load_results:
            if os.path.exists(result.get("file_path", "")):
                os.remove(result["file_path"])

    # DAG Flow
    record_info = get_record_count()
    chunks = generate_chunk_ranges(record_info)

    # Dynamic task mapping for parallel extraction
    chunk_results = extract_chunk.expand(chunk=chunks)
    load_results = load_to_salesforce.expand(chunk_result=chunk_results)

    reconciliation = record_reconciliation(load_results)
    cleanup = cleanup_staging(load_results)

    reconciliation >> cleanup
```

---

## Data Reconciliation DAG

```python
"""
Data Reconciliation DAG
Compare source (Oracle) vs target (Salesforce) counts
"""
from datetime import datetime, timedelta
from airflow.sdk import DAG, task
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

TABLES_TO_RECONCILE = [
    {"oracle_table": "KPS_T_SALES_MD", "sf_object": "KPS_Sales__c"},
    {"oracle_table": "KPS_T_SALESPAY_MD", "sf_object": "KPS_SalesPay__c"},
    {"oracle_table": "KPS_T_SALES_M", "sf_object": "KPS_SalesM__c"},
    # Add all tables
]

with DAG(
    dag_id="data_reconciliation",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["reconciliation", "kpc"],
) as dag:

    @task()
    def get_oracle_counts(**context):
        """Get record counts from Oracle"""
        hook = OracleHook(oracle_conn_id="oracle_kpc")
        data_interval_start = context["data_interval_start"]

        counts = {}
        for table_config in TABLES_TO_RECONCILE:
            table = table_config["oracle_table"]
            sql = f"""
                SELECT COUNT(*) FROM {table}
                WHERE UPDATED_DATE >= :start_date
            """
            result = hook.get_first(sql, parameters={"start_date": data_interval_start})
            counts[table] = result[0]

        return counts

    @task()
    def get_salesforce_counts(**context):
        """Get record counts from Salesforce"""
        hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
        sf = hook.get_conn()
        data_interval_start = context["data_interval_start"]

        counts = {}
        for table_config in TABLES_TO_RECONCILE:
            sf_object = table_config["sf_object"]

            # SOQL query
            query = f"""
                SELECT COUNT(Id) cnt
                FROM {sf_object}
                WHERE LastModifiedDate >= {data_interval_start.isoformat()}
            """
            result = sf.query(query)
            counts[sf_object] = result["records"][0]["cnt"]

        return counts

    @task()
    def compare_counts(oracle_counts: dict, sf_counts: dict):
        """Compare and generate reconciliation report"""
        report = []
        discrepancies = []

        for table_config in TABLES_TO_RECONCILE:
            oracle_table = table_config["oracle_table"]
            sf_object = table_config["sf_object"]

            oracle_count = oracle_counts.get(oracle_table, 0)
            sf_count = sf_counts.get(sf_object, 0)
            diff = oracle_count - sf_count
            match_pct = (sf_count / oracle_count * 100) if oracle_count > 0 else 0

            status = "✅ MATCH" if diff == 0 else "❌ MISMATCH"

            record = {
                "oracle_table": oracle_table,
                "sf_object": sf_object,
                "oracle_count": oracle_count,
                "sf_count": sf_count,
                "difference": diff,
                "match_percentage": round(match_pct, 2),
                "status": status,
            }
            report.append(record)

            if diff != 0:
                discrepancies.append(record)

        return {
            "report": report,
            "discrepancies": discrepancies,
            "has_discrepancies": len(discrepancies) > 0,
        }

    @task()
    def save_reconciliation_report(comparison_result: dict, **context):
        """Save report to file and database"""
        import json

        report_date = context["data_interval_start"].strftime("%Y%m%d")
        report_path = f"/data/reports/reconciliation_{report_date}.json"

        with open(report_path, "w") as f:
            json.dump(comparison_result, f, indent=2, default=str)

        # Also insert into audit table
        hook = OracleHook(oracle_conn_id="oracle_kpc")
        for record in comparison_result["report"]:
            hook.run("""
                INSERT INTO MIGRATION_AUDIT
                (TABLE_NAME, ORACLE_COUNT, SF_COUNT, DIFFERENCE, STATUS, CREATED_DATE)
                VALUES (:1, :2, :3, :4, :5, SYSDATE)
            """, parameters=[
                record["oracle_table"],
                record["oracle_count"],
                record["sf_count"],
                record["difference"],
                record["status"],
            ])

        return report_path

    @task()
    def alert_on_discrepancy(comparison_result: dict):
        """Send alert if discrepancies found"""
        if comparison_result["has_discrepancies"]:
            # Send Slack/Email notification
            message = "⚠️ Data Migration Discrepancies Found:\n"
            for d in comparison_result["discrepancies"]:
                message += f"- {d['oracle_table']}: Oracle={d['oracle_count']}, SF={d['sf_count']}, Diff={d['difference']}\n"

            # Use Slack/Email operator here
            print(message)  # Replace with actual notification

    # DAG Flow
    oracle_counts = get_oracle_counts()
    sf_counts = get_salesforce_counts()
    comparison = compare_counts(oracle_counts, sf_counts)

    save_reconciliation_report(comparison) >> alert_on_discrepancy(comparison)
```

---

## Airflow Connections Setup

### 1. Oracle Connection

```bash
# Via Airflow CLI
airflow connections add oracle_kpc \
    --conn-type oracle \
    --conn-host oracle-server.company.com \
    --conn-port 1521 \
    --conn-login kpc_user \
    --conn-password 'secure_password' \
    --conn-schema KPC_DB \
    --conn-extra '{"service_name": "KPCPROD"}'
```

### 2. Salesforce Connection

```bash
airflow connections add salesforce_prod \
    --conn-type salesforce \
    --conn-login your_username@company.com \
    --conn-password 'password+security_token' \
    --conn-extra '{
        "security_token": "your_security_token",
        "domain": "login"
    }'
```

---

## Recommended Airflow Variables

```bash
# Set via CLI or UI
airflow variables set MIGRATION_CHUNK_SIZE 500000
airflow variables set STAGING_PATH /data/staging
airflow variables set DATALOADER_PATH /opt/dataloader
airflow variables set ALERT_EMAIL data-team@company.com
airflow variables set SALESFORCE_BATCH_SIZE 10000
```

---

## Docker Compose Additions (On-Premise)

Add to `docker-compose.yaml`:

```yaml
x-airflow-common:
  &airflow-common
  environment:
    # Oracle Client
    - LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1
    - ORACLE_HOME=/opt/oracle/instantclient_21_1
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    # Staging area for CSV files
    - /data/staging:/data/staging
    # Data Loader installation
    - /opt/dataloader:/opt/dataloader
    # Oracle Instant Client
    - /opt/oracle:/opt/oracle

# Add more workers for parallel processing
airflow-worker-2:
  <<: *airflow-common
  command: celery worker
  environment:
    <<: *airflow-common-env
    DUMB_INIT_SETSID: "0"

airflow-worker-3:
  <<: *airflow-common
  command: celery worker
  environment:
    <<: *airflow-common-env
    DUMB_INIT_SETSID: "0"
```

---

## Performance Recommendations

### For Large Tables (87M+ records)

| Setting | Value | Reason |
| --- | --- | --- |
| `CHUNK_SIZE` | 500,000 | Balance memory vs. API calls |
| `sfdc.loadBatchSize` | 10,000 | Salesforce Bulk API limit |
| `sfdc.useBulkApi` | true | Required for large volumes |
| `max_active_tasks` | 4-8 | Parallel chunk processing |
| Celery Workers | 3-5 | Parallel task execution |

### Oracle Extraction Tips

```python
# Use ROWID for efficient pagination
SELECT * FROM KPS_T_SALES_MD
WHERE ROWID IN (
    SELECT ROWID FROM (
        SELECT ROWID, ROWNUM rn FROM KPS_T_SALES_MD
        WHERE rn BETWEEN :start AND :end
    )
)

# Use parallel hint for large tables
SELECT /*+ PARALLEL(t, 4) */ * FROM KPS_T_SALES_MD t
```

---

## Monitoring & Alerting

```python
# Add to DAGs for monitoring
from airflow.operators.email import EmailOperator

alert_failure = EmailOperator(
    task_id="alert_failure",
    to="{{ var.value.ALERT_EMAIL }}",
    subject="Migration Failed: {{ dag.dag_id }}",
    html_content="Task {{ task_instance.task_id }} failed.",
    trigger_rule="one_failed",
)
```

---

## Summary Checklist

- [ ] Install Oracle Instant Client on Airflow workers
- [ ] Install Salesforce Data Loader CLI
- [ ] Configure Airflow Connections (Oracle, Salesforce)
- [ ] Set up staging directory with sufficient storage
- [ ] Create process-conf.xml for each table
- [ ] Create field mapping files (.sdl)
- [ ] Set up CeleryExecutor with Redis
- [ ] Configure multiple workers for parallel processing
- [ ] Create reconciliation audit table in Oracle
- [ ] Set up alerting (Slack/Email)
- [ ] Test with small table first (KPS_R_POS_SUPPLIER)
