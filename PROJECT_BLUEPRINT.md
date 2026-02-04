# KPC TMS Data Migration - Project Blueprint

> เอกสารนี้อธิบายรายละเอียดทั้งหมดของ project เพื่อใช้ในการสร้างใหม่ (recreate) ตั้งแต่ต้น

---

## 1. Project Overview

**ชื่อ:** KPC TMS Data Migration
**วัตถุประสงค์:** Migration ข้อมูลจาก Oracle Database (On-Premise) ไปยัง Salesforce (Cloud)
**ปริมาณข้อมูล:** ~522M - 783M records (ข้อมูลย้อนหลัง 2-3 ปี)
**Orchestration:** Apache Airflow 3.x (Docker Compose, CeleryExecutor)

### Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Orchestration | Apache Airflow | 3.1.6 |
| Source DB | Oracle Database | On-Premise |
| Target | Salesforce | Cloud (Bulk API 2.0) |
| Metadata DB | PostgreSQL | 16 |
| Message Broker | Redis | 7.2-bookworm |
| Container Runtime | Docker & Docker Compose | - |
| Language | Python | 3.9+ |
| Data Processing | pandas | - |
| Data Quality | Great Expectations | - |
| Oracle Driver | oracledb | - |
| Linter | ruff | >=0.14.10 |

---

## 2. Migration Volume

| Source Table | Target Object | Per Year | 2-3 Years Total | Priority |
|---|---|---|---|---|
| KPS_T_SALES_MD | KPS_Sales__c | ~87M | 174M - 261M | Critical |
| KPS_T_SALESPAY_MD | KPS_SalesPay__c | ~36M | 73M - 109M | Critical |
| KPS_T_SALES_M | KPS_SalesM__c | ~36M | 72M - 108M | Critical |
| KPS_T_SALES_APPRV_DETAIL | KPS_SalesApprvDetail__c | ~179K | - | Medium |
| KPS_T_SALESBANK_MD | KPS_SalesBank__c | ~164K | - | Medium |
| KPS_T_PREINV_REVSALES_D | KPS_PreinvRevsalesD__c | ~156K | - | Medium |
| Product2 | Product2 | ~100K | - | Medium |
| KPS_T_SALES_APPRV | KPS_SalesApprv__c | ~45K | - | Low |
| KPS_WEB_SALES | KPS_WebSales__c | ~14K | - | Low |
| KPS_T_PREINV | KPS_Preinv__c | ~6K | - | Low |
| KPS_T_PREINV_DETAIL | KPS_PreinvDetail__c | ~6K | - | Low |
| KPS_T_PREINV_MIN | KPS_PreinvMin__c | ~3K | - | Low |
| KPS_T_PREINV_REVGUA | KPS_PreinvRevgua__c | ~3K | - | Low |
| KPS_T_PREINV_REVSALES_M | KPS_PreinvRevsalesM__c | ~3K | - | Low |
| KPS_R_EMAIL_TENANT | KPS_EmailTenant__c | ~436 | - | Low |
| KPS_R_EMAIL_SUPPLIER | KPS_EmailSupplier__c | ~4 | - | Low |
| KPS_R_POS_SUPPLIER | KPS_PosSupplier__c | ~4 | - | Low |

---

## 3. Project Structure

```
kpc-tms-data-migration/
├── dags/                              # Airflow DAG files
│   ├── config/
│   │   ├── tables_config.py           # Table configurations (dataclass)
│   │   ├── extract_config.py          # Extraction parameters per table
│   │   └── field_mappings.py          # Oracle→SF field mapping + transformations
│   ├── dag_factory.py                 # Auto-generates migration DAGs from config
│   ├── migration_master_dag.py        # Master orchestrator (8 phases)
│   ├── migrate_bulk_api_dag.py        # Bulk API 2.0 migration DAG
│   ├── reconciliation_dag.py          # Post-migration validation
│   ├── migrate_product_price_dag.py   # POC: Product & Price migration
│   ├── test_oracle_connection_dag.py  # Oracle connection health check
│   ├── debug_oracle_connection.py     # Debug script
│   ├── utility_encrypt_password.py    # SF password encryption
│   ├── setup_salesforce_pipeline.py   # SF org preparation
│   └── sample_migration_dag.py        # Template
│
├── plugins/                           # Custom Airflow plugins
│   ├── oracle_extractor.py            # Parallel extraction from Oracle
│   ├── oracle_service.py              # Oracle connection management
│   ├── transformers.py                # Data transformation (Oracle→SF)
│   ├── salesforce_bulk_loader.py      # Bulk API 2.0 loader
│   ├── salesforce_auth.py             # OAuth 2.0 Client Credentials
│   ├── salesforce_status_tracker.py   # Bulk API job status tracking
│   ├── migration_logger.py            # Structured logging to PostgreSQL
│   └── reconciliation.py              # Data reconciliation (3-level)
│
├── config/                            # Configuration files
│   ├── airflow.cfg                    # Airflow runtime config
│   ├── airflow_variables.json         # Airflow variables
│   └── oracle/                        # Oracle TNS/network config
│
├── salesforce/                        # Salesforce Data Loader
│   ├── dataloader_conf/
│   │   ├── process-conf.xml           # Data Loader process definitions
│   │   ├── config.properties          # SF connection (gitignored)
│   │   ├── key.txt                    # Encryption key (gitignored)
│   │   ├── mappings/                  # Field mapping .sdl files
│   │   │   ├── Product2.sdl
│   │   │   ├── KPS_T_SALES_MD.sdl
│   │   │   ├── KPS_T_SALESPAY_MD.sdl
│   │   │   ├── KPS_T_SALES_M.sdl
│   │   │   └── ... (per table)
│   │   └── *_Process_lastRun.properties
│   ├── data/                          # Staging CSVs (gitignored)
│   └── logs/                          # Success/error logs (gitignored)
│
├── great_expectations/                # Data quality validation
│   ├── great_expectations.yml         # Core GX config (3 datasources)
│   ├── expectations/                  # Expectation suites
│   │   ├── source_product_price.json
│   │   ├── extract_product_price.json
│   │   └── postmig_product_price.json
│   ├── checkpoints/
│   │   └── source_checkpoint.yml
│   ├── plugins/                       # Custom expectations
│   └── uncommitted/                   # Generated reports (gitignored)
│
├── tests/                             # Unit tests
│   ├── test_oracle_service.py
│   ├── test_extraction.py
│   ├── test_transformation.py
│   ├── test_loading.py
│   └── test_reconciliation.py
│
├── docs/                              # Documentation
│   ├── ARCHITECTURE.md
│   ├── PIPELINE_DESIGN.md
│   ├── AIRFLOW_SETUP.md
│   ├── AIRFLOW_BEST_PRACTICES.md
│   ├── GREAT_EXPECTATIONS_GUIDE.md
│   ├── GREAT_EXPECTATIONS_USAGE.md
│   ├── GREAT_EXPECTATIONS_PIPELINE.md
│   ├── SALESFORCE_REQUIREMENTS.md
│   ├── SALESFORCE_BULK_API_GUIDE.md
│   ├── SALESFORCE_CLI_COMMANDS.md
│   ├── MIGRATE_BULK_API_DAG.md
│   └── MIGRATION_CHECKLIST.md
│
├── files/                             # Build dependencies (for Docker)
│   ├── instantclient-basic-linux-x64/ # Oracle Instant Client x86_64
│   ├── instantclient-basic-linux-arm64/ # Oracle Instant Client ARM64
│   └── dataloader_v64/               # Salesforce Data Loader v64
│
├── docker-compose.yaml                # Multi-container orchestration
├── Dockerfile                         # Custom Airflow image
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Ruff linter config
├── .env                               # Environment variables
├── .gitignore                         # Git exclusions
├── CLAUDE.md                          # Claude Code guidance
└── README.md                          # Project documentation
```

---

## 4. Infrastructure (Docker)

### 4.1 Dockerfile

```dockerfile
FROM apache/airflow:3.1.6

USER root

# Dependencies: Oracle Instant Client + Java (Data Loader)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libaio1 \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Oracle Instant Client (multi-arch: x86_64 + ARM64)
RUN mkdir -p /opt/oracle
COPY files/instantclient-basic-linux-x64/instantclient_19_29 /opt/oracle/instantclient-x64
COPY files/instantclient-basic-linux-arm64/instantclient_19_29 /opt/oracle/instantclient-arm64

# Detect architecture and symlink
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
    ln -sf /opt/oracle/instantclient-x64 /opt/oracle/instantclient; \
    elif [ "$ARCH" = "aarch64" ]; then \
    ln -sf /opt/oracle/instantclient-arm64 /opt/oracle/instantclient; \
    fi

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient
ENV ORACLE_HOME=/opt/oracle/instantclient

# Salesforce Data Loader v64
COPY files/dataloader_v64 /opt/dataloader
RUN echo '#!/bin/bash' > /opt/dataloader/process.sh && \
    echo 'java --enable-native-access=ALL-UNNAMED -cp /opt/dataloader/dataloader-64.1.0.jar com.salesforce.dataloader.process.DataLoaderRunner run.mode=batch salesforce.config.dir="$1" process.name="$2"' >> /opt/dataloader/process.sh && \
    chmod +x /opt/dataloader/process.sh

USER airflow
ENV PATH="/home/airflow/.local/bin:${PATH}"
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
```

### 4.2 Docker Compose Services (8 services)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| postgres | postgres:16 | 5432 | Airflow metadata DB |
| redis | redis:7.2-bookworm | 6379 | Celery message broker |
| airflow-apiserver | custom (build .) | 8080 | REST API + Web UI |
| airflow-scheduler | custom | - | DAG scheduling |
| airflow-dag-processor | custom | - | DAG parsing |
| airflow-worker | custom | - | Celery task executor |
| airflow-triggerer | custom | - | Async task triggering |
| flower (optional) | custom | 5555 | Celery monitoring |

### 4.3 Key Environment Variables

```yaml
AIRFLOW__CORE__EXECUTOR: CeleryExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
AIRFLOW__CORE__AUTH_MANAGER: airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
PYTHONPATH: /opt/airflow
SF_ENDPOINT: ${SF_ENDPOINT:-https://test.salesforce.com}
SF_USERNAME: ${SF_USERNAME}
SF_PASSWORD: ${SF_PASSWORD}
```

### 4.4 Volume Mounts

```yaml
volumes:
  - ./dags:/opt/airflow/dags
  - ./logs:/opt/airflow/logs
  - ./config:/opt/airflow/config
  - ./plugins:/opt/airflow/plugins
  - ./salesforce:/opt/airflow/salesforce
  - ./great_expectations:/opt/airflow/great_expectations
  - ./config/oracle:/opt/oracle/instantclient/network/admin
```

### 4.5 Python Dependencies (requirements.txt)

```
apache-airflow-providers-salesforce
apache-airflow-providers-oracle
oracledb
pandas
great_expectations
airflow-provider-great-expectations
```

---

## 5. DAG Architecture

### 5.1 Master DAG (8 Phases)

DAG ID: `kpc_migration_master` | Manual trigger only | max_active_runs=1

```
Phase 1: Reference Data (parallel)
  ├── migrate_kps_r_email_supplier
  ├── migrate_kps_r_email_tenant
  └── migrate_kps_r_pos_supplier

Phase 2: Pre-Invoice Tables (parallel)
  ├── migrate_kps_t_preinv
  ├── migrate_kps_t_preinv_min
  └── migrate_kps_t_preinv_revgua

Phase 3: Pre-Invoice Details (parallel, depends on Phase 2)
  ├── migrate_kps_t_preinv_detail
  ├── migrate_kps_t_preinv_revsales_d
  └── migrate_kps_t_preinv_revsales_m

Phase 4: KPS_T_SALES_M (sequential)
  └── migrate_kps_t_sales_m

Phase 5: KPS_T_SALES_MD (sequential, ~261M records)
  └── migrate_kps_t_sales_md

Phase 6: KPS_T_SALESPAY_MD (sequential, ~109M records)
  └── migrate_kps_t_salespay_md

Phase 7: Supporting Tables (parallel)
  ├── migrate_kps_t_sales_apprv
  ├── migrate_kps_t_sales_apprv_detail
  ├── migrate_kps_t_salesbank_md
  └── migrate_kps_web_sales

Phase 8: Reconciliation
  └── reconciliation
```

### 5.2 DAG Factory (Auto-generated DAGs)

ไฟล์ `dag_factory.py` สร้าง DAG อัตโนมัติ 17 ตัว จาก `TABLES` config

**Flow ของแต่ละ DAG:**

```
get_record_count → extract_chunk (dynamic expand) → transform_chunk → load_chunk → summarize_results
```

- ใช้ TaskFlow API (`@task()`)
- Dynamic task mapping (`expand()`) สำหรับ parallel chunk processing
- แต่ละ DAG ถูก trigger โดย Master DAG ผ่าน `TriggerDagRunOperator`

### 5.3 Bulk API DAG

DAG ID: `migrate_bulk_api` | 4 steps:

```
authenticate (OAuth 2.0) ──┐
                           ├── upload_batches (Bulk API 2.0) → collect_results
extract_data (Oracle→CSV) ─┘
```

**Config parameters (via `--conf`):**

```json
{
  "sf_object": "TMS_Request__c",
  "external_id_field": "External_Id__c",
  "operation": "upsert",
  "table_name": "KPS_T_SALES_MD",
  "batch_size": 40000,
  "start_batch": 1,
  "sf_conn_id": "salesforce_api",
  "extract_query": "SELECT * FROM ...",
  "column_mapping": {"ORACLE_COL": "SF_Field__c"}
}
```

---

## 6. Plugin Details

### 6.1 Oracle Extractor (`oracle_extractor.py`)

**Class:** `OracleExtractor`

```python
@dataclass
class ChunkInfo:
    chunk_id: int
    start_row: int
    end_row: int
    record_count: int = 0
    file_path: str = ""

class OracleExtractor:
    def __init__(self, oracle_hook, table_name, chunk_size=500_000,
                 use_parallel_hint=False, parallel_degree=8, use_gzip=True)

    def get_record_count(start_date, end_date, partition_column) -> int
    def calculate_chunks(total_records) -> list[ChunkInfo]
    def extract_chunk(chunk, order_by, staging_path, ...) -> ChunkInfo
    def extract_full_table(order_by, staging_base_path, ...) -> list[ChunkInfo]
```

**Features:**
- Chunked extraction (configurable chunk size)
- Oracle `PARALLEL(t, N)` hints
- `ROW_NUMBER()` based pagination
- GZIP compression output (~70% size reduction)
- Date-based partitioning filter

### 6.2 Data Transformer (`transformers.py`)

**Class:** `DataTransformer`

```python
class DataTransformer:
    @staticmethod
    def to_sf_datetime(value) -> str | None      # Oracle DATE → ISO 8601
    @staticmethod
    def to_decimal_2(value) -> float | None       # round to 2 decimal places
    @staticmethod
    def to_sf_boolean(value) -> bool | None       # 1/Y/YES/TRUE → true
    @staticmethod
    def truncate_text(value, max_length=255)      # truncate to max length
    @staticmethod
    def truncate_255(value) -> str | None         # shorthand for 255

    def transform_dataframe(df, mappings, transformations) -> pd.DataFrame
```

**Pipeline:**
1. Apply transformations (before rename)
2. Rename columns (Oracle → SF)
3. Keep only mapped columns

### 6.3 Salesforce Bulk Loader (`salesforce_bulk_loader.py`)

**Class:** `SalesforceBulkLoader`

```python
class JobState(str, Enum):
    OPEN, UPLOAD_COMPLETE, IN_PROGRESS, JOB_COMPLETE, FAILED, ABORTED

@dataclass
class JobResult:
    job_id: str
    state: str
    records_processed: int = 0
    records_failed: int = 0
    file_path: str = ""
    error_message: str = ""

class SalesforceBulkLoader:
    def __init__(self, instance_url, access_token, api_version="v59.0",
                 max_concurrent_jobs=15, poll_interval=5, job_timeout=7200)

    def create_job(object_name, operation="upsert", external_id_field) -> str
    def upload_data(job_id, csv_file_path, use_gzip=True) -> None
    def close_job(job_id) -> None
    def wait_for_job(job_id) -> JobResult
    def load_file(object_name, csv_file_path, ...) -> JobResult
    def load_files_parallel(object_name, csv_files, ...) -> list[JobResult]
```

**Features:**
- Bulk API 2.0 (not 1.0)
- GZIP compression for uploads
- Parallel job execution (max 15 concurrent)
- Upsert operations (idempotent)
- Auto-retry on failure
- ThreadPoolExecutor for parallel loading

### 6.4 Salesforce Auth (`salesforce_auth.py`)

```python
class SalesforceAuthError(Exception): ...

def get_salesforce_token(conn_id="salesforce_api") -> dict:
    # Returns: {access_token, instance_url, token_type}
    # Auth flow: OAuth 2.0 Client Credentials
    # Reads from Airflow Connection:
    #   - login = client_id
    #   - password = client_secret
    #   - host = Salesforce base URL
```

### 6.5 Oracle Service (`oracle_service.py`)

**Class:** `OracleService`

```python
@dataclass
class HealthCheckResult:
    healthy: bool
    version: str | None = None
    error: str | None = None

@dataclass
class TableAccessResult:
    table_name: str
    accessible: bool
    error: str | None = None

class OracleService:
    def __init__(self, conn_id="oracle_kpc", timeout=30,
                 instant_client_path="/opt/oracle/instantclient")

    def get_connection() -> Generator[oracledb.Connection]  # context manager
    def health_check() -> HealthCheckResult
    def verify_table_access(table_names: list[str]) -> dict[str, TableAccessResult]
    def run_sample_query(table_name, limit=5) -> dict
    def execute_query(query, params) -> list[tuple]
    def execute_query_with_columns(query, params) -> dict
```

**Features:**
- Lazy initialization (thread-safe, double-check locking)
- Thick mode (Oracle Instant Client) + thin mode fallback
- Airflow Connection credentials (not hardcoded)
- Supports both Service Name and SID

### 6.6 Migration Logger (`migration_logger.py`)

**Class:** `MigrationLogger`

```python
@dataclass
class MigrationRunLog:
    run_id, dag_id, table_name, sf_object, operation, status,
    total_records, total_batches, batch_size, total_processed, total_failed,
    start_batch, error_message

@dataclass
class MigrationBatchLog:
    run_id, batch_number, job_id, file_path, state,
    records_in_batch, records_processed, records_failed, error_message

class MigrationLogger:
    def __init__(self, postgres_conn_id="airflow_db")

    def log_run_start(run_id, dag_id, table_name, ...) -> bool
    def log_run_complete(run_id, status, total_processed, ...) -> bool
    def log_batch_start(run_id, batch_number, file_path, ...) -> bool
    def log_batch_complete(run_id, batch_number, job_id, ...) -> bool
    def get_run_summary(run_id) -> dict | None
```

**DB Tables:**
- `migration.runs` — 1 row per DAG run (ON CONFLICT upsert)
- `migration.batch_logs` — 1 row per batch (ON CONFLICT upsert)
- `migration.v_summary` — View for summary queries

**Fail-safe:** logs warning แต่ไม่ raise exception ถ้า DB logging fail

### 6.7 Salesforce Status Tracker (`salesforce_status_tracker.py`)

**Class:** `SalesforceStatusTracker`

```python
class SalesforceStatusTracker:
    def __init__(self, instance_url, access_token)
    # Tracks via TMS_Daily_Sales_File__c upsert/update
    # External ID: TMS_External_File_Ref__c

    def upsert_status(external_ref, status, **fields) -> dict
    def update_status(external_ref, status) -> dict  # updateOnly=true
```

### 6.8 Data Reconciliation (`reconciliation.py`)

**Class:** `DataReconciliation`

```python
@dataclass
class ValidationResult:
    check_type: str     # "count", "aggregate", "checksum"
    status: str         # "PASS" or "FAIL"
    details: dict

@dataclass
class ReconciliationReport:
    table_name, sf_object, timestamp, checks, overall_status

class DataReconciliation:
    def __init__(self, oracle_hook, sf_hook)

    def count_check(oracle_table, sf_object, ...) -> ValidationResult
    def aggregate_check(oracle_table, sf_object, oracle_column, sf_field, variance_threshold=0.01) -> ValidationResult
    def checksum_sample(oracle_table, sf_object, key_column, sample_size=1000) -> ValidationResult
    def generate_report(oracle_table, sf_object, numeric_columns, key_column) -> ReconciliationReport
```

**3-Level Validation:**
1. **Count** — exact record count match (Oracle vs Salesforce)
2. **Aggregate** — SUM, AVG, MIN, MAX comparison (variance threshold 0.01%)
3. **Checksum** — hash-based validation on 1,000 random samples

---

## 7. Configuration Layer

### 7.1 Table Config (`dags/config/tables_config.py`)

```python
@dataclass
class TableConfig:
    table_name: str
    sf_object: str
    external_id_field: str
    priority: str              # "critical", "medium", "low"
    records_per_year: int
    partition_column: str = "CREATED_DATE"
    order_by: Optional[str] = None

    @property
    def is_large_table(self) -> bool:
        return self.records_per_year > 10_000_000
```

Helper functions:
- `get_table_config(table_name)` → `TableConfig | None`
- `get_tables_by_priority(priority)` → `list[TableConfig]`
- `get_large_tables()` → tables with >10M records/year

### 7.2 Extract Config (`dags/config/extract_config.py`)

```python
@dataclass
class ExtractConfig:
    chunk_size: int = 500_000
    parallel_workers: int = 1
    fetch_size: int = 10_000
    use_parallel_hint: bool = False
    parallel_degree: int = 4
```

| Table | Chunk Size | Workers | Fetch Size | Parallel Degree | Hints |
|-------|-----------|---------|-----------|-----------------|-------|
| KPS_T_SALES_MD | 500K | 10 | 50K | 8 | Yes |
| KPS_T_SALESPAY_MD | 500K | 8 | 50K | 8 | Yes |
| KPS_T_SALES_M | 500K | 8 | 50K | 8 | Yes |
| Medium tables | 500K | 2 | 20K | 4 | Yes |
| Default (small) | 1M | 1 | 10K | 4 | No |

**Staging Config:**
```python
STAGING_CONFIG = {
    "base_path": "/data/staging",
    "use_gzip": True,
    "file_extension": ".csv.gz",
    "cleanup_after_load": True,
}
```

### 7.3 Field Mappings (`dags/config/field_mappings.py`)

```python
@dataclass
class FieldMapping:
    sf_object: str
    external_id: str
    mappings: dict[str, str]                    # Oracle col → SF field
    transformations: dict[str, str]             # Column → transform func name
    lookups: dict[str, tuple[str, str, str]]    # Column → (target_obj, match_field, ref_field)
```

**Transformation Functions:**
- `to_sf_datetime` — Oracle DATE → `YYYY-MM-DDTHH:MM:SS.000Z`
- `to_decimal_2` — Float → 2 decimal places
- `to_sf_boolean` — `1/Y/YES/TRUE` → `true`
- `truncate_255` — Truncate to 255 chars

**KPS_T_SALES_MD Mapping:**

| Oracle Column | Salesforce Field | Transform |
|---|---|---|
| SALE_NO | External_ID__c | - |
| CO_TENT_CODE | Tenant_Code__c | - |
| SHOP_CODE | Store_Code__c | - |
| SALE_DATE | Sales_Date__c | to_sf_datetime |
| TOTAL_AMT_EXC_VAT | Sales_Amount__c | to_decimal_2 |
| TOTAL_AMT_VAT | Tax_Amount__c | to_decimal_2 |
| TOTAL_DISC_AMT_EXC_VAT | Discount_Amount__c | to_decimal_2 |
| TOTAL_NET_AMT_EXC_VAT | Net_Amount__c | to_decimal_2 |
| SALE_TYPE | Payment_Type__c | - |
| CREATEDDATE | Oracle_Created_Date__c | to_sf_datetime |
| UPDATEDDATE | Oracle_Updated_Date__c | to_sf_datetime |

**Lookups:**
- `CO_TENT_CODE` → Account (Tenant_Code__c → Account__c)
- `SHOP_CODE` → Store__c (Store_Code__c → Store__c)

**KPS_T_SALESPAY_MD Mapping:**

| Oracle Column | Salesforce Field | Transform |
|---|---|---|
| SALESPAY_ID | External_ID__c | - |
| SALES_ID | Sales__c | - (lookup) |
| PAYMENT_METHOD | Payment_Method__c | - |
| PAYMENT_AMOUNT | Payment_Amount__c | to_decimal_2 |
| CARD_NUMBER | Card_Number__c | - |
| CREATED_DATE | Oracle_Created_Date__c | to_sf_datetime |

**KPS_T_SALES_M Mapping:**

| Oracle Column | Salesforce Field | Transform |
|---|---|---|
| SALES_M_ID | External_ID__c | - |
| TENANT_CODE | Tenant_Code__c | - |
| STORE_CODE | Store_Code__c | - |
| SALES_MONTH | Sales_Month__c | to_sf_datetime |
| TOTAL_AMOUNT | Total_Amount__c | to_decimal_2 |
| TOTAL_TRANSACTIONS | Total_Transactions__c | - |
| CREATED_DATE | Oracle_Created_Date__c | to_sf_datetime |

**Reference Tables (simple mappings):**
- KPS_R_EMAIL_TENANT: TENANT_CODE → External_ID__c, EMAIL_ADDRESS, TENANT_NAME, ACTIVE (boolean)
- KPS_R_EMAIL_SUPPLIER: SUPPLIER_CODE → External_ID__c, EMAIL_ADDRESS, SUPPLIER_NAME
- KPS_R_POS_SUPPLIER: SUPPLIER_CODE → External_ID__c, POS_ID, SUPPLIER_NAME

**Product2 Mapping (Multi-table JOIN):**

| Field | SF Field | Transform |
|---|---|---|
| TMS_Concession__c | TMS_Concession__c | - |
| TMS_Company_Name__c | TMS_Company_Name__c | - |
| TMS_Shop_Name__c | TMS_Shop_Name__c | - |
| TMS_Unit__c | TMS_Unit__c | - |
| TMS_Start_Date__c | TMS_Start_Date__c | to_sf_datetime |
| TMS_End_Date__c | TMS_End_Date__c | to_sf_datetime |
| TMS_Bar_Code__c | TMS_Bar_Code__c | - |
| ProductCode | ProductCode | - |
| Name | Name | - |
| TMS_Price_EXC_VAT__c | TMS_Price_EXC_VAT__c | to_decimal_2 |
| TMS_Price_INC_VAT__c | TMS_Price_INC_VAT__c | to_decimal_2 |

---

## 8. Great Expectations (Data Quality)

### 8.1 Configuration (`great_expectations.yml`)

**3 Datasources:**

```yaml
# 1. Oracle source (SqlAlchemy)
oracle_kpc:
  engine: SqlAlchemyExecutionEngine
  connection_string: oracle+cx_oracle://kpc:kpc@localhost:1521/

# 2. Staging filesystem (Pandas)
staging_filesystem:
  engine: PandasExecutionEngine
  base_directory: /opt/airflow/salesforce/data

# 3. Runtime (Pandas - for in-memory DataFrames)
runtime_datasource:
  engine: PandasExecutionEngine
```

### 8.2 Validation Stages

1. **Source Validation** — Pre-migration Oracle data quality
2. **Post-Extract Validation** — CSV integrity (schema, row count)
3. **Pre-Load Validation** — SF compatibility (field lengths, picklist values)
4. **Post-Migration Validation** — Final reconciliation (count, totals, checksums)

### 8.3 Expectation Suites

- `source_product_price.json` — Source data expectations
- `extract_product_price.json` — Post-extract expectations
- `postmig_product_price.json` — Post-migration expectations

---

## 9. Salesforce Data Loader Config

### 9.1 SDL Mapping Format

```
# Product2.sdl
BARCODE=TMS_Bar_Code__c
UNIT_DESC=TMS_Unit__c
PROD_SERV_CODE=ProductCode
PROD_SERV_NAME=Name
```

### 9.2 process-conf.xml Structure

Spring beans (1 per process):
- Salesforce endpoint, username, encrypted password
- SF object name, operation (insert/upsert)
- External ID field
- Mapping file path (.sdl)
- CSV input/output paths
- Bulk API settings (enabled, serial mode, batch size)

---

## 10. Airflow Connections Required

| Connection ID | Type | Purpose |
|---|---|---|
| `oracle_kpc` | Oracle | Source database (host, port, schema/SID, login, password) |
| `salesforce_prod` | Salesforce | Target org (standard SF hook) |
| `salesforce_api` | HTTP | OAuth 2.0 (login=client_id, password=client_secret, host=base_url) |
| `airflow_db` | PostgreSQL | Migration logging (uses default Airflow DB) |

---

## 11. Batch Processing Strategy

### Extraction
- Large tables chunked at 500K records/chunk
- `ROW_NUMBER() OVER (ORDER BY ...)` for pagination
- Oracle `PARALLEL(t, 8)` hints for large tables
- GZIP compression reduces file size ~70%

### Loading
- Bulk API 2.0 jobs (not 1.0)
- Max 15 concurrent jobs (Salesforce safe limit)
- GZIP upload support
- Upsert operations (idempotent via External ID)
- Poll interval: 5 seconds
- Job timeout: 7,200 seconds (2 hours)

### Resume Support
- `start_batch` parameter to skip already-processed batches
- Idempotent upsert prevents duplicate records

---

## 12. Logging Architecture

### Airflow Logs
- Standard Airflow task logs in `logs/` directory

### PostgreSQL Migration Logs
- `migration.runs` — 1 row per DAG run
- `migration.batch_logs` — 1 row per batch/job
- `migration.v_summary` — Aggregated view
- Fail-safe: logging failure doesn't stop migration

### Salesforce Status Tracking
- `TMS_Daily_Sales_File__c` object
- External ID: `TMS_External_File_Ref__c`
- Status field: `TMS_Status__c` (New, Uploading, In Progress, Uploaded, Failed)

---

## 13. Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Individual test files
pytest tests/test_oracle_service.py      # Oracle connection, health check
pytest tests/test_extraction.py          # Chunk calculation, extraction
pytest tests/test_transformation.py      # Type conversion, truncation
pytest tests/test_loading.py             # Bulk API job lifecycle
pytest tests/test_reconciliation.py      # Count, aggregate, checksum
```

### Linting

```bash
pip install "ruff>=0.14.10"
ruff check dags/ plugins/ --select E,W,F,I,C,B,UP,AIR
ruff format dags/ plugins/
```

Config (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "C", "B", "UP", "AIR"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

---

## 14. Commands

```bash
# Start Airflow
docker compose up -d

# Stop Airflow
docker compose down

# Build custom image
docker compose build

# Initialize database (first time)
docker compose up airflow-init

# View logs
docker compose logs -f

# Access Airflow CLI
docker compose exec airflow-webserver airflow <command>

# Trigger DAG
airflow dags trigger migrate_bulk_api --conf '{"sf_object": "...", "batch_size": 40000}'

# Enable Flower monitoring
docker compose --profile flower up

# Web UI: http://localhost:8080 (airflow/airflow)
```

---

## 15. .gitignore (Key Exclusions)

```
# Sensitive
.env
.venv/
venv/

# Runtime
logs/
airflow-webserver.pid

# Staging data
salesforce/data/
salesforce/logs/

# Generated reports
great_expectations/uncommitted/

# Config
config/airflow_variables.json
salesforce/dataloader_conf/config.properties
salesforce/dataloader_conf/key.txt
```

---

## 16. Architecture Patterns

1. **Configuration-Driven DAG Generation** — Single factory generates 17 DAGs from config; new tables added by updating `tables_config.py` only
2. **Modular Plugin Architecture** — Each component independently testable (extractor, transformer, loader, reconciler)
3. **Three-Layer Data Validation** — Source → Extract → Post-Migration
4. **Batch Processing with Resume** — `start_batch` parameter for picking up where you left off
5. **OAuth 2.0 Stateless Auth** — Per-run token, no password storage
6. **Fail-safe Logging** — PostgreSQL logging that won't crash the migration
7. **Idempotent Operations** — Upsert via External ID, ON CONFLICT in logging
8. **Dynamic Task Mapping** — Airflow `expand()` for parallel chunk processing
