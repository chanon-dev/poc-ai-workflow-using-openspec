# Data Migration Pipeline Design

## Pros & Cons Analysis

### Overall Architecture Decision

| Approach | Pros | Cons |
| --- | --- | --- |
| **Airflow + Bulk API 2.0** (Chosen) | Full control, parallel processing, audit trail, retry logic | Complex setup, requires maintenance |
| MuleSoft/Informatica | Enterprise support, GUI-based | Expensive license, less flexible |
| Salesforce Data Loader GUI | Simple, free | Manual, no automation, slow |
| Heroku Connect | Real-time sync, managed | Monthly cost, limited customization |

---

### Component-Level Pros & Cons

#### 1. Extract: Oracle Parallel Query

| Pros | Cons |
| --- | --- |
| ✅ 5-10x faster with parallel hints | ❌ Increases Oracle CPU/memory load |
| ✅ Chunking prevents memory overflow | ❌ Complex ROWNUM pagination logic |
| ✅ Can resume from failed chunk | ❌ Requires tuning parallel degree |
| ✅ Date partitioning reduces scan | ❌ Need to handle Oracle session limits |

**Risk Mitigation:**

- Monitor Oracle AWR reports during extraction
- Set `parallel_degree` based on available CPU cores
- Schedule extraction during off-peak hours

---

#### 2. Transform: Python/Pandas

| Pros | Cons |
| --- | --- |
| ✅ Flexible field mapping | ❌ Memory intensive for large chunks |
| ✅ Easy to add custom logic | ❌ Slower than compiled languages |
| ✅ Rich ecosystem (pandas, numpy) | ❌ GIL limits true parallelism |
| ✅ Easy debugging and testing | ❌ Type coercion can be tricky |

**Alternatives Considered:**

| Alternative | Why Not Chosen |
| --- | --- |
| Apache Spark | Overkill for transformation, complex setup |
| dbt | Better for warehouse, not ETL to Salesforce |
| Pure SQL | Less flexible for complex mappings |

---

#### 3. Staging: Local CSV Files

| Pros | Cons |
| --- | --- |
| ✅ Simple, no additional infra | ❌ Disk I/O bottleneck possible |
| ✅ Easy to inspect/debug | ❌ Single point of failure |
| ✅ Bulk API accepts CSV directly | ❌ Need sufficient disk space (~500GB) |
| ✅ GZIP compression reduces size | ❌ Not distributed (single machine) |

**Alternatives Considered:**

| Alternative | Pros | Cons |
| --- | --- | --- |
| S3/GCS | Distributed, durable | Added latency, cost |
| Database staging | ACID, queryable | Extra DB load, slower |
| In-memory | Fastest | Memory limits, no persistence |

**Recommendation:** Use local NVMe SSD for speed. For production, consider S3 for durability.

---

#### 4. Load: Salesforce Bulk API 2.0

| Pros | Cons |
| --- | --- |
| ✅ Fastest SF loading method | ❌ 150MB file size limit |
| ✅ 150M records per 24hr rolling | ❌ Limited error details |
| ✅ Automatic batching | ❌ No real-time progress |
| ✅ Async - doesn't block | ❌ Job queuing during peak |
| ✅ GZIP supported | ❌ Complex retry logic needed |

**Bulk API 2.0 vs 1.0:**

| Feature | Bulk API 1.0 | Bulk API 2.0 (Chosen) |
| --- | --- | --- |
| Simplicity | Complex batch management | Simple job-based |
| Performance | Good | Better (auto-optimized) |
| Monitoring | Manual batch tracking | Unified job status |
| File handling | Multiple batches | Single upload |

**Salesforce Limits to Consider:**

| Limit | Value | Impact |
| --- | --- | --- |
| Daily Bulk API requests | 15,000 | ~1,000 jobs max |
| Records per 24hr | 150,000,000 | Split across days if > 150M |
| Concurrent jobs | 100 | Use 15 to be safe |
| File size | 150MB | GZIP helps stay under |

---

#### 5. Parallel Processing: Celery Workers

| Pros | Cons |
| --- | --- |
| ✅ True parallelism | ❌ Redis/RabbitMQ dependency |
| ✅ Scalable (add workers) | ❌ Network overhead |
| ✅ Task retry built-in | ❌ Debugging distributed tasks |
| ✅ Resource isolation | ❌ More infrastructure to manage |

**Alternatives:**

| Alternative | Why Not Chosen |
| --- | --- |
| LocalExecutor | Single machine limit, no horizontal scale |
| KubernetesExecutor | Complex K8s setup, overkill for this |
| Sequential | Too slow for 783M records |

---

#### 6. Reconciliation Approach

| Pros | Cons |
| --- | --- |
| ✅ Catches data loss early | ❌ Adds 1-2 hours to pipeline |
| ✅ Multiple check types | ❌ SOQL query limits |
| ✅ Automated alerting | ❌ Sample checksum not 100% |
| ✅ Audit trail | ❌ Cannot fix, only detect |

**Reconciliation Trade-offs:**

| Check Type | Accuracy | Speed | Cost |
| --- | --- | --- | --- |
| Count only | Low | Fast | Free |
| Count + Aggregates | Medium | Medium | Low |
| Full checksum | High | Slow | High API calls |
| Sample checksum (Chosen) | Medium-High | Medium | Medium |

---

### Performance vs Complexity Trade-offs

```
                    HIGH PERFORMANCE
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
    │   Spark Cluster     │   Custom C++ ETL    │
    │   (Overkill)        │   (Maintenance hell)│
    │                     │                     │
    ├─────────────────────┼─────────────────────┤
    │                     │                     │
    │ ★ CHOSEN APPROACH   │   Real-time CDC     │
    │   Airflow+BulkAPI   │   (Different use)   │
    │                     │                     │
    ├─────────────────────┼─────────────────────┤
    │                     │                     │
    │   Single Thread     │   Data Loader GUI   │
    │   (Too slow)        │   (Manual)          │
    │                     │                     │
    └─────────────────────┴─────────────────────┘
  LOW COMPLEXITY ◄────────────────────► HIGH COMPLEXITY
```

---

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
| --- | --- | --- | --- |
| SF API rate limit hit | Medium | High | Throttling, parallel limit |
| Oracle connection timeout | Low | Medium | Connection pooling, retry |
| Disk space exhausted | Medium | High | Monitor, cleanup after load |
| Data corruption | Low | Critical | Checksum validation |
| Network failure | Medium | Medium | Idempotent upsert, retry |
| SF triggers slow load | High | High | Disable during migration |

---

### Cost Analysis (On-Premise)

| Component | One-time Cost | Monthly Cost |
| --- | --- | --- |
| Airflow Server (8 CPU, 32GB) | $0 (existing) | $0 |
| Redis (Celery broker) | $0 | $0 |
| Staging Storage (1TB NVMe) | ~$150 | $0 |
| Network bandwidth | $0 | $0 |
| **Total** | **~$150** | **$0** |

**vs Cloud Alternative:**

| Component | Monthly Cost |
| --- | --- |
| AWS MWAA (Managed Airflow) | ~$500 |
| S3 storage | ~$50 |
| Data transfer | ~$100 |
| **Total** | **~$650/month** |

---

### When NOT to Use This Approach

| Scenario | Better Alternative |
| --- | --- |
| Real-time sync needed | Heroku Connect, Platform Events |
| < 1M records total | Salesforce Data Loader GUI |
| No technical team | MuleSoft, Informatica |
| Need CDC (change capture) | Debezium + Kafka |
| Budget unlimited | Informatica Cloud |

---

### Summary: Why This Approach?

| Requirement | Solution | Score |
| --- | --- | --- |
| Handle 783M records | Parallel chunking + Bulk API 2.0 | ✅ |
| Minimize load time | 15 concurrent jobs, GZIP | ✅ |
| Data integrity | Reconciliation checks | ✅ |
| Cost effective | On-premise, open source | ✅ |
| Maintainable | Python, well-documented | ✅ |
| Retryable | Idempotent upsert, checkpoints | ✅ |

### Overall Rating: 8/10

- Lost 1 point: Complexity of setup
- Lost 1 point: Requires technical expertise

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           DATA MIGRATION PIPELINE                                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ EXTRACT  │───▶│TRANSFORM │───▶│  STAGE   │───▶│   LOAD   │───▶│ RECONCILE│      │
│  │ (Oracle) │    │ (Python) │    │  (CSV)   │    │(Salesforce)   │ (Verify) │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │               │               │               │               │             │
│       ▼               ▼               ▼               ▼               ▼             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Parallel │    │  Field   │    │Compress &│    │ Bulk API │    │  Count   │      │
│  │ Chunks   │    │ Mapping  │    │  Split   │    │   2.0    │    │ Compare  │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Performance Optimization Strategy

### Target Performance

| Table | Records | Target Time | Throughput |
| --- | --- | --- | --- |
| KPS_T_SALES_MD | 261M (3 years) | < 24 hours | ~3,000 records/sec |
| KPS_T_SALESPAY_MD | 109M (3 years) | < 10 hours | ~3,000 records/sec |
| KPS_T_SALES_M | 108M (3 years) | < 10 hours | ~3,000 records/sec |
| Others | < 2M | < 1 hour | ~500 records/sec |

### Key Performance Factors

| Factor | Optimization |
| --- | --- |
| **Salesforce Bulk API** | Use Bulk API 2.0 (faster than 1.0) |
| **Parallel Jobs** | Run 10-15 concurrent bulk jobs |
| **Batch Size** | 10,000 records per batch (SF limit) |
| **Compression** | GZIP CSV files before upload |
| **Network** | Direct connection, minimize latency |
| **SF Triggers** | Disable during migration |
| **Indexes** | Defer index creation |

---

## Phase 1: Extract (Oracle → Staging)

### Parallel Extraction Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORACLE DATABASE                               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              KPS_T_SALES_MD (261M records)               │    │
│  └─────────────────────────────────────────────────────────┘    │
│           │         │         │         │         │              │
│           ▼         ▼         ▼         ▼         ▼              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Worker1 │ │ Worker2 │ │ Worker3 │ │ Worker4 │ │ Worker5 │   │
│  │ Chunk 1 │ │ Chunk 2 │ │ Chunk 3 │ │ Chunk 4 │ │ Chunk 5 │   │
│  │ 0-500K  │ │500K-1M  │ │ 1M-1.5M │ │1.5M-2M  │ │ 2M-2.5M │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
│           │         │         │         │         │              │
└───────────┼─────────┼─────────┼─────────┼─────────┼──────────────┘
            ▼         ▼         ▼         ▼         ▼
     ┌─────────────────────────────────────────────────────┐
     │              STAGING AREA (NFS/SSD)                  │
     │  chunk_001.csv  chunk_002.csv  chunk_003.csv  ...   │
     └─────────────────────────────────────────────────────┘
```

### Extract Configuration

```python
# config/extract_config.py

EXTRACT_CONFIG = {
    "KPS_T_SALES_MD": {
        "chunk_size": 500_000,          # Records per chunk
        "parallel_workers": 10,          # Concurrent extractions
        "partition_column": "CREATED_DATE",  # For date-based partitioning
        "order_by": "SALES_ID",          # Primary key for consistent ordering
        "fetch_size": 50_000,            # Oracle fetch size
        "use_parallel_hint": True,       # Oracle parallel query hint
        "parallel_degree": 8,            # Oracle parallel degree
    },
    "KPS_T_SALESPAY_MD": {
        "chunk_size": 500_000,
        "parallel_workers": 8,
        "partition_column": "CREATED_DATE",
        "order_by": "SALESPAY_ID",
        "fetch_size": 50_000,
        "use_parallel_hint": True,
        "parallel_degree": 8,
    },
    "KPS_T_SALES_M": {
        "chunk_size": 500_000,
        "parallel_workers": 8,
        "partition_column": "CREATED_DATE",
        "order_by": "SALES_M_ID",
        "fetch_size": 50_000,
        "use_parallel_hint": True,
        "parallel_degree": 8,
    },
    # Smaller tables - single batch
    "DEFAULT": {
        "chunk_size": 1_000_000,
        "parallel_workers": 1,
        "fetch_size": 10_000,
        "use_parallel_hint": False,
    }
}
```

### Optimized Oracle Query

```python
def generate_extract_query(table_name: str, start_date: str, end_date: str,
                          chunk_start: int, chunk_end: int) -> str:
    """Generate optimized Oracle extraction query"""

    config = EXTRACT_CONFIG.get(table_name, EXTRACT_CONFIG["DEFAULT"])

    parallel_hint = "/*+ PARALLEL(t, 8) */" if config["use_parallel_hint"] else ""

    return f"""
        SELECT {parallel_hint} *
        FROM (
            SELECT t.*, ROW_NUMBER() OVER (ORDER BY {config['order_by']}) as rn
            FROM {table_name} t
            WHERE {config['partition_column']} BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD')
                                                   AND TO_DATE(:end_date, 'YYYY-MM-DD')
        )
        WHERE rn BETWEEN :chunk_start AND :chunk_end
    """
```

---

## Phase 2: Transform (Data Mapping)

### Field Mapping Configuration

```python
# config/field_mappings.py

FIELD_MAPPINGS = {
    "KPS_T_SALES_MD": {
        "sf_object": "KPS_Sales__c",
        "external_id": "External_ID__c",
        "mappings": {
            # Oracle Column → Salesforce Field
            "SALES_ID": "External_ID__c",
            "TENANT_CODE": "Tenant_Code__c",
            "STORE_CODE": "Store_Code__c",
            "SALES_DATE": "Sales_Date__c",
            "SALES_AMOUNT": "Sales_Amount__c",
            "TAX_AMOUNT": "Tax_Amount__c",
            "DISCOUNT_AMOUNT": "Discount_Amount__c",
            "NET_AMOUNT": "Net_Amount__c",
            "PAYMENT_TYPE": "Payment_Type__c",
            "CREATED_DATE": "Oracle_Created_Date__c",
            "UPDATED_DATE": "Oracle_Updated_Date__c",
        },
        "transformations": {
            "SALES_DATE": "to_sf_datetime",
            "CREATED_DATE": "to_sf_datetime",
            "UPDATED_DATE": "to_sf_datetime",
            "SALES_AMOUNT": "to_decimal_2",
            "TAX_AMOUNT": "to_decimal_2",
        },
        "lookups": {
            # Field → (SF Object, External ID Field, Lookup Field)
            "TENANT_CODE": ("Account", "Tenant_Code__c", "Account__c"),
            "STORE_CODE": ("Store__c", "Store_Code__c", "Store__c"),
        }
    },
    # ... other table mappings
}
```

### Transform Functions

```python
# plugins/transformers.py

import pandas as pd
from datetime import datetime
from decimal import Decimal

class DataTransformer:
    """Transform Oracle data for Salesforce compatibility"""

    @staticmethod
    def to_sf_datetime(value):
        """Convert Oracle datetime to Salesforce format"""
        if pd.isna(value):
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        return value

    @staticmethod
    def to_decimal_2(value):
        """Convert to 2 decimal places"""
        if pd.isna(value):
            return None
        return round(float(value), 2)

    @staticmethod
    def to_sf_boolean(value):
        """Convert to Salesforce boolean"""
        if pd.isna(value):
            return None
        return str(value).upper() in ('1', 'Y', 'YES', 'TRUE')

    @staticmethod
    def truncate_text(value, max_length=255):
        """Truncate text to max length"""
        if pd.isna(value):
            return None
        return str(value)[:max_length]

    def transform_dataframe(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Apply all transformations to dataframe"""
        config = FIELD_MAPPINGS[table_name]

        # Rename columns
        df = df.rename(columns=config["mappings"])

        # Apply transformations
        for oracle_col, transform_func in config.get("transformations", {}).items():
            sf_col = config["mappings"].get(oracle_col, oracle_col)
            if sf_col in df.columns:
                df[sf_col] = df[sf_col].apply(getattr(self, transform_func))

        # Select only mapped columns
        sf_columns = list(config["mappings"].values())
        df = df[[col for col in sf_columns if col in df.columns]]

        return df
```

---

## Phase 3: Load (Salesforce Bulk API 2.0)

### Salesforce Bulk API 2.0 Optimization

```
┌─────────────────────────────────────────────────────────────────┐
│                 SALESFORCE BULK API 2.0 FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │ Create  │───▶│ Upload  │───▶│ Close   │───▶│ Monitor │      │
│  │   Job   │    │  Data   │    │   Job   │    │ Status  │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│                                                                  │
│  Parallel Jobs: 10-15 concurrent                                │
│  Batch Size: 10,000 records (150MB max per job)                 │
│  Compression: GZIP enabled                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Bulk API 2.0 Loader

```python
# plugins/salesforce_bulk_loader.py

import requests
import gzip
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

class SalesforceBulkLoader:
    """High-performance Salesforce Bulk API 2.0 loader"""

    def __init__(self, instance_url: str, access_token: str):
        self.instance_url = instance_url
        self.access_token = access_token
        self.api_version = "v59.0"
        self.base_url = f"{instance_url}/services/data/{self.api_version}"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Performance settings
        self.max_concurrent_jobs = 15
        self.poll_interval = 5  # seconds
        self.max_records_per_job = 150_000_000  # 150M records per job
        self.max_file_size = 150 * 1024 * 1024  # 150MB per upload

    def create_job(self, object_name: str, operation: str = "upsert",
                   external_id: str = None) -> str:
        """Create a new Bulk API 2.0 ingest job"""

        job_data = {
            "object": object_name,
            "operation": operation,
            "contentType": "CSV",
            "lineEnding": "LF",
        }

        if operation == "upsert" and external_id:
            job_data["externalIdFieldName"] = external_id

        response = requests.post(
            f"{self.base_url}/jobs/ingest",
            headers=self.headers,
            json=job_data
        )
        response.raise_for_status()

        return response.json()["id"]

    def upload_data(self, job_id: str, csv_file_path: str, use_gzip: bool = True):
        """Upload CSV data to the job"""

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "text/csv",
            "Accept": "application/json"
        }

        if use_gzip:
            headers["Content-Encoding"] = "gzip"
            with open(csv_file_path, 'rb') as f:
                data = gzip.compress(f.read())
        else:
            with open(csv_file_path, 'rb') as f:
                data = f.read()

        response = requests.put(
            f"{self.base_url}/jobs/ingest/{job_id}/batches",
            headers=headers,
            data=data
        )
        response.raise_for_status()

    def close_job(self, job_id: str):
        """Close the job to start processing"""

        response = requests.patch(
            f"{self.base_url}/jobs/ingest/{job_id}",
            headers=self.headers,
            json={"state": "UploadComplete"}
        )
        response.raise_for_status()

    def get_job_status(self, job_id: str) -> Dict:
        """Get job processing status"""

        response = requests.get(
            f"{self.base_url}/jobs/ingest/{job_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def wait_for_job(self, job_id: str, timeout: int = 3600) -> Dict:
        """Wait for job to complete"""

        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            state = status["state"]

            if state in ("JobComplete", "Failed", "Aborted"):
                return status

            time.sleep(self.poll_interval)

        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")

    def get_job_results(self, job_id: str) -> Dict:
        """Get successful and failed records info"""

        status = self.get_job_status(job_id)

        return {
            "job_id": job_id,
            "state": status["state"],
            "records_processed": status.get("numberRecordsProcessed", 0),
            "records_failed": status.get("numberRecordsFailed", 0),
            "api_active_processing_time": status.get("apiActiveProcessingTime", 0),
            "total_processing_time": status.get("totalProcessingTime", 0),
        }

    def load_files_parallel(self, object_name: str, csv_files: List[str],
                           external_id: str, max_workers: int = None) -> List[Dict]:
        """Load multiple CSV files in parallel"""

        max_workers = max_workers or self.max_concurrent_jobs
        results = []

        def load_single_file(csv_file: str) -> Dict:
            job_id = self.create_job(object_name, "upsert", external_id)
            self.upload_data(job_id, csv_file, use_gzip=True)
            self.close_job(job_id)
            return self.wait_for_job(job_id)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(load_single_file, f): f for f in csv_files}

            for future in as_completed(futures):
                csv_file = futures[future]
                try:
                    result = future.result()
                    result["file"] = csv_file
                    results.append(result)
                except Exception as e:
                    results.append({
                        "file": csv_file,
                        "state": "Error",
                        "error": str(e)
                    })

        return results
```

### Load Configuration

```python
# config/load_config.py

LOAD_CONFIG = {
    "salesforce": {
        "api_version": "v59.0",
        "max_concurrent_jobs": 15,      # Parallel Bulk API jobs
        "poll_interval_seconds": 5,
        "job_timeout_seconds": 7200,    # 2 hours per job
        "use_gzip_compression": True,
        "retry_attempts": 3,
        "retry_delay_seconds": 60,
    },
    "batching": {
        "records_per_file": 100_000,    # Split CSVs for parallel upload
        "max_file_size_mb": 100,        # Max file size before split
    },
    "performance": {
        # Disable these in SF during migration for speed
        "disable_triggers": True,
        "disable_workflows": True,
        "disable_validation_rules": True,
        "disable_duplicate_rules": True,
    }
}

# Load order (dependencies)
LOAD_ORDER = [
    # Phase 1: Reference Data (no dependencies)
    {
        "phase": 1,
        "parallel": True,
        "tables": [
            "KPS_R_EMAIL_SUPPLIER",
            "KPS_R_EMAIL_TENANT",
            "KPS_R_POS_SUPPLIER",
        ]
    },
    # Phase 2: Pre-Invoice tables
    {
        "phase": 2,
        "parallel": True,
        "tables": [
            "KPS_T_PREINV",
            "KPS_T_PREINV_MIN",
            "KPS_T_PREINV_REVGUA",
        ]
    },
    # Phase 3: Pre-Invoice Details (depends on Phase 2)
    {
        "phase": 3,
        "parallel": True,
        "tables": [
            "KPS_T_PREINV_DETAIL",
            "KPS_T_PREINV_REVSALES_D",
            "KPS_T_PREINV_REVSALES_M",
        ]
    },
    # Phase 4: Main Sales tables (largest - run separately)
    {
        "phase": 4,
        "parallel": False,  # Sequential to avoid API limits
        "tables": [
            "KPS_T_SALES_M",
        ]
    },
    # Phase 5: Sales Details
    {
        "phase": 5,
        "parallel": False,
        "tables": [
            "KPS_T_SALES_MD",
        ]
    },
    # Phase 6: Sales Payment
    {
        "phase": 6,
        "parallel": False,
        "tables": [
            "KPS_T_SALESPAY_MD",
        ]
    },
    # Phase 7: Supporting tables
    {
        "phase": 7,
        "parallel": True,
        "tables": [
            "KPS_T_SALES_APPRV",
            "KPS_T_SALES_APPRV_DETAIL",
            "KPS_T_SALESBANK_MD",
            "KPS_WEB_SALES",
        ]
    },
]
```

---

## Phase 4: Reconciliation

### Reconciliation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECONCILIATION PROCESS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐         ┌─────────────┐         ┌───────────┐ │
│  │   Oracle    │         │  Salesforce │         │   MATCH   │ │
│  │   COUNT     │────────▶│    COUNT    │────────▶│  COMPARE  │ │
│  │  261M rows  │         │   261M rows │         │    ✓/✗    │ │
│  └─────────────┘         └─────────────┘         └───────────┘ │
│         │                       │                       │       │
│         ▼                       ▼                       ▼       │
│  ┌─────────────┐         ┌─────────────┐         ┌───────────┐ │
│  │   CHECKSUM  │         │   CHECKSUM  │         │  CHECKSUM │ │
│  │  (Sample)   │────────▶│  (Sample)   │────────▶│   MATCH   │ │
│  └─────────────┘         └─────────────┘         └───────────┘ │
│                                                         │       │
│                                                         ▼       │
│                                                  ┌───────────┐  │
│                                                  │  REPORT   │  │
│                                                  │ & ALERTS  │  │
│                                                  └───────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Reconciliation Checks

```python
# plugins/reconciliation.py

from typing import Dict, List
import hashlib

class DataReconciliation:
    """Data reconciliation between Oracle and Salesforce"""

    def __init__(self, oracle_hook, sf_hook):
        self.oracle = oracle_hook
        self.sf = sf_hook

    def count_check(self, oracle_table: str, sf_object: str,
                    date_filter: Dict = None) -> Dict:
        """Compare record counts"""

        # Oracle count
        oracle_sql = f"SELECT COUNT(*) FROM {oracle_table}"
        if date_filter:
            oracle_sql += f" WHERE {date_filter['column']} BETWEEN :start AND :end"
        oracle_count = self.oracle.get_first(oracle_sql, date_filter)[0]

        # Salesforce count
        sf_query = f"SELECT COUNT(Id) FROM {sf_object}"
        if date_filter:
            sf_query += f" WHERE Oracle_Created_Date__c >= {date_filter['start']}"
        sf_result = self.sf.query(sf_query)
        sf_count = sf_result["totalSize"]

        return {
            "oracle_count": oracle_count,
            "sf_count": sf_count,
            "difference": oracle_count - sf_count,
            "match_percentage": (sf_count / oracle_count * 100) if oracle_count > 0 else 0,
            "status": "PASS" if oracle_count == sf_count else "FAIL"
        }

    def checksum_sample(self, oracle_table: str, sf_object: str,
                        key_column: str, sample_size: int = 1000) -> Dict:
        """Compare checksums on sample records"""

        # Get random sample of keys from Oracle
        oracle_sql = f"""
            SELECT {key_column} FROM (
                SELECT {key_column} FROM {oracle_table}
                ORDER BY DBMS_RANDOM.VALUE
            ) WHERE ROWNUM <= :sample_size
        """
        sample_keys = [r[0] for r in self.oracle.get_records(oracle_sql, {"sample_size": sample_size})]

        matches = 0
        mismatches = []

        for key in sample_keys:
            oracle_checksum = self._get_oracle_checksum(oracle_table, key_column, key)
            sf_checksum = self._get_sf_checksum(sf_object, key)

            if oracle_checksum == sf_checksum:
                matches += 1
            else:
                mismatches.append(key)

        return {
            "sample_size": sample_size,
            "matches": matches,
            "mismatches": len(mismatches),
            "match_percentage": (matches / sample_size * 100),
            "mismatch_keys": mismatches[:10],  # First 10 for debugging
            "status": "PASS" if len(mismatches) == 0 else "FAIL"
        }

    def aggregate_check(self, oracle_table: str, sf_object: str,
                        numeric_column: str, sf_field: str) -> Dict:
        """Compare sum/avg of numeric columns"""

        # Oracle aggregates
        oracle_sql = f"""
            SELECT SUM({numeric_column}), AVG({numeric_column}),
                   MIN({numeric_column}), MAX({numeric_column})
            FROM {oracle_table}
        """
        oracle_agg = self.oracle.get_first(oracle_sql)

        # Salesforce aggregates
        sf_query = f"""
            SELECT SUM({sf_field}), AVG({sf_field}),
                   MIN({sf_field}), MAX({sf_field})
            FROM {sf_object}
        """
        sf_result = self.sf.query(sf_query)
        sf_agg = sf_result["records"][0]

        return {
            "oracle": {
                "sum": oracle_agg[0],
                "avg": oracle_agg[1],
                "min": oracle_agg[2],
                "max": oracle_agg[3]
            },
            "salesforce": {
                "sum": sf_agg.get("expr0"),
                "avg": sf_agg.get("expr1"),
                "min": sf_agg.get("expr2"),
                "max": sf_agg.get("expr3")
            },
            "status": "PASS" if abs(oracle_agg[0] - sf_agg.get("expr0", 0)) < 0.01 else "FAIL"
        }

    def generate_report(self, table_name: str) -> Dict:
        """Generate full reconciliation report"""

        config = FIELD_MAPPINGS[table_name]
        sf_object = config["sf_object"]

        report = {
            "table": table_name,
            "sf_object": sf_object,
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }

        # Count check
        report["checks"]["count"] = self.count_check(table_name, sf_object)

        # Checksum sample
        report["checks"]["checksum"] = self.checksum_sample(
            table_name, sf_object,
            config["mappings"].keys()[0]  # First column as key
        )

        # Aggregate check for numeric fields
        for oracle_col, transform in config.get("transformations", {}).items():
            if "decimal" in transform:
                sf_field = config["mappings"][oracle_col]
                report["checks"][f"aggregate_{sf_field}"] = self.aggregate_check(
                    table_name, sf_object, oracle_col, sf_field
                )

        # Overall status
        all_passed = all(
            check["status"] == "PASS"
            for check in report["checks"].values()
        )
        report["overall_status"] = "PASS" if all_passed else "FAIL"

        return report
```

---

## Complete DAG Implementation

### Master Migration DAG

```python
# dags/migration_master_dag.py

"""
KPC TMS Data Migration - Master DAG
Orchestrates the complete migration pipeline
"""

from datetime import datetime, timedelta
from airflow.sdk import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "email_on_failure": True,
    "email": ["data-team@company.com"],
}

with DAG(
    dag_id="kpc_migration_master",
    default_args=default_args,
    description="Master orchestration for KPC TMS data migration",
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["migration", "kpc", "master"],
    max_active_runs=1,
) as dag:

    # Phase 1: Reference Data (parallel)
    phase1_tables = ["KPS_R_EMAIL_SUPPLIER", "KPS_R_EMAIL_TENANT", "KPS_R_POS_SUPPLIER"]
    phase1_triggers = []
    for table in phase1_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"migrate_{table.lower()}",
            trigger_dag_id=f"migrate_{table.lower()}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase1_triggers.append(trigger)

    # Phase 2: Pre-Invoice (parallel)
    phase2_tables = ["KPS_T_PREINV", "KPS_T_PREINV_MIN", "KPS_T_PREINV_REVGUA"]
    phase2_triggers = []
    for table in phase2_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"migrate_{table.lower()}",
            trigger_dag_id=f"migrate_{table.lower()}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase2_triggers.append(trigger)

    # Phase 3: Pre-Invoice Details
    phase3_tables = ["KPS_T_PREINV_DETAIL", "KPS_T_PREINV_REVSALES_D", "KPS_T_PREINV_REVSALES_M"]
    phase3_triggers = []
    for table in phase3_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"migrate_{table.lower()}",
            trigger_dag_id=f"migrate_{table.lower()}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase3_triggers.append(trigger)

    # Phase 4-6: Large tables (sequential)
    migrate_sales_m = TriggerDagRunOperator(
        task_id="migrate_kps_t_sales_m",
        trigger_dag_id="migrate_kps_t_sales_m_chunked",
        wait_for_completion=True,
        poke_interval=60,
    )

    migrate_sales_md = TriggerDagRunOperator(
        task_id="migrate_kps_t_sales_md",
        trigger_dag_id="migrate_kps_t_sales_md_chunked",
        wait_for_completion=True,
        poke_interval=60,
    )

    migrate_salespay = TriggerDagRunOperator(
        task_id="migrate_kps_t_salespay_md",
        trigger_dag_id="migrate_kps_t_salespay_md_chunked",
        wait_for_completion=True,
        poke_interval=60,
    )

    # Phase 7: Supporting tables
    phase7_tables = ["KPS_T_SALES_APPRV", "KPS_T_SALES_APPRV_DETAIL",
                     "KPS_T_SALESBANK_MD", "KPS_WEB_SALES"]
    phase7_triggers = []
    for table in phase7_tables:
        trigger = TriggerDagRunOperator(
            task_id=f"migrate_{table.lower()}",
            trigger_dag_id=f"migrate_{table.lower()}",
            wait_for_completion=True,
            poke_interval=30,
        )
        phase7_triggers.append(trigger)

    # Reconciliation
    reconciliation = TriggerDagRunOperator(
        task_id="run_reconciliation",
        trigger_dag_id="data_reconciliation",
        wait_for_completion=True,
        poke_interval=60,
    )

    # Send completion notification
    def send_completion_notification(**context):
        # Implement Slack/Email notification
        pass

    notify_complete = PythonOperator(
        task_id="notify_completion",
        python_callable=send_completion_notification,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    # DAG Flow
    phase1_triggers >> phase2_triggers >> phase3_triggers
    phase3_triggers >> migrate_sales_m >> migrate_sales_md >> migrate_salespay
    migrate_salespay >> phase7_triggers >> reconciliation >> notify_complete
```

### Chunked Migration DAG (for large tables)

```python
# dags/migrate_kps_t_sales_md_chunked.py

"""
KPC TMS - KPS_T_SALES_MD Migration with Parallel Chunking
Handles 261M records with optimal performance
"""

from datetime import datetime, timedelta
from airflow.sdk import DAG, task
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.operators.python import PythonOperator
import pandas as pd
import os

# Configuration
TABLE_NAME = "KPS_T_SALES_MD"
SF_OBJECT = "KPS_Sales__c"
EXTERNAL_ID = "External_ID__c"
CHUNK_SIZE = 500_000
MAX_PARALLEL_EXTRACTS = 10
MAX_PARALLEL_LOADS = 15
STAGING_PATH = "/data/staging/kps_t_sales_md"

default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="migrate_kps_t_sales_md_chunked",
    default_args=default_args,
    description=f"Migrate {TABLE_NAME} with parallel chunking",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_tasks=MAX_PARALLEL_EXTRACTS,
    tags=["migration", "kpc", "chunked", TABLE_NAME.lower()],
) as dag:

    @task()
    def prepare_staging():
        """Create staging directory"""
        os.makedirs(STAGING_PATH, exist_ok=True)
        # Clean old files
        for f in os.listdir(STAGING_PATH):
            os.remove(os.path.join(STAGING_PATH, f))
        return STAGING_PATH

    @task()
    def calculate_chunks(**context) -> list:
        """Calculate chunk ranges based on total records"""
        hook = OracleHook(oracle_conn_id="oracle_kpc")

        # Get date range from DAG params or use default (3 years)
        params = context.get("params", {})
        start_date = params.get("start_date", "2022-01-01")
        end_date = params.get("end_date", "2024-12-31")

        # Get total count
        sql = f"""
            SELECT COUNT(*) FROM {TABLE_NAME}
            WHERE CREATED_DATE BETWEEN TO_DATE(:start, 'YYYY-MM-DD')
                                   AND TO_DATE(:end, 'YYYY-MM-DD')
        """
        total = hook.get_first(sql, {"start": start_date, "end": end_date})[0]

        # Generate chunks
        chunks = []
        num_chunks = (total // CHUNK_SIZE) + 1

        for i in range(num_chunks):
            chunks.append({
                "chunk_id": i,
                "start_row": i * CHUNK_SIZE + 1,
                "end_row": (i + 1) * CHUNK_SIZE,
                "start_date": start_date,
                "end_date": end_date,
            })

        return chunks

    @task(max_active_tis_per_dag=MAX_PARALLEL_EXTRACTS)
    def extract_chunk(chunk: dict, staging_path: str) -> dict:
        """Extract single chunk from Oracle"""
        from plugins.transformers import DataTransformer

        hook = OracleHook(oracle_conn_id="oracle_kpc")
        transformer = DataTransformer()

        sql = f"""
            SELECT /*+ PARALLEL(t, 8) */ *
            FROM (
                SELECT t.*, ROW_NUMBER() OVER (ORDER BY SALES_ID) as rn
                FROM {TABLE_NAME} t
                WHERE CREATED_DATE BETWEEN TO_DATE(:start, 'YYYY-MM-DD')
                                       AND TO_DATE(:end, 'YYYY-MM-DD')
            )
            WHERE rn BETWEEN :start_row AND :end_row
        """

        df = hook.get_pandas_df(sql, parameters={
            "start": chunk["start_date"],
            "end": chunk["end_date"],
            "start_row": chunk["start_row"],
            "end_row": chunk["end_row"],
        })

        # Transform
        df = transformer.transform_dataframe(df, TABLE_NAME)

        # Save to CSV
        output_file = f"{staging_path}/chunk_{chunk['chunk_id']:05d}.csv"
        df.to_csv(output_file, index=False)

        return {
            "chunk_id": chunk["chunk_id"],
            "file_path": output_file,
            "record_count": len(df),
        }

    @task()
    def load_to_salesforce(extract_results: list) -> list:
        """Load all chunks to Salesforce in parallel"""
        from plugins.salesforce_bulk_loader import SalesforceBulkLoader
        from airflow.providers.salesforce.hooks.salesforce import SalesforceHook

        sf_hook = SalesforceHook(salesforce_conn_id="salesforce_prod")
        sf_conn = sf_hook.get_conn()

        loader = SalesforceBulkLoader(
            instance_url=sf_conn.sf_instance,
            access_token=sf_conn.session_id
        )

        csv_files = [r["file_path"] for r in extract_results]

        results = loader.load_files_parallel(
            object_name=SF_OBJECT,
            csv_files=csv_files,
            external_id=EXTERNAL_ID,
            max_workers=MAX_PARALLEL_LOADS
        )

        return results

    @task()
    def summarize_results(load_results: list) -> dict:
        """Summarize migration results"""
        total_processed = sum(r.get("records_processed", 0) for r in load_results)
        total_failed = sum(r.get("records_failed", 0) for r in load_results)

        failed_jobs = [r for r in load_results if r.get("state") != "JobComplete"]

        summary = {
            "table": TABLE_NAME,
            "total_processed": total_processed,
            "total_failed": total_failed,
            "success_rate": (total_processed - total_failed) / total_processed * 100 if total_processed > 0 else 0,
            "failed_jobs": len(failed_jobs),
            "timestamp": datetime.now().isoformat(),
        }

        # Alert if failures
        if total_failed > 0 or failed_jobs:
            # Send alert
            pass

        return summary

    @task()
    def cleanup_staging(staging_path: str, summary: dict):
        """Clean up staging files after successful migration"""
        if summary["failed_jobs"] == 0:
            import shutil
            shutil.rmtree(staging_path, ignore_errors=True)

    # DAG Flow
    staging = prepare_staging()
    chunks = calculate_chunks()
    extract_results = extract_chunk.expand(chunk=chunks, staging_path=[staging] * 1000)
    load_results = load_to_salesforce(extract_results)
    summary = summarize_results(load_results)
    cleanup_staging(staging, summary)
```

---

## Performance Monitoring Dashboard

### Key Metrics to Track

```python
# plugins/metrics.py

MIGRATION_METRICS = {
    "extraction": {
        "records_per_second": "Gauge",
        "chunk_duration_seconds": "Histogram",
        "oracle_query_time": "Histogram",
    },
    "transformation": {
        "transform_duration_seconds": "Histogram",
        "records_transformed": "Counter",
    },
    "loading": {
        "sf_api_calls": "Counter",
        "records_loaded_per_second": "Gauge",
        "bulk_job_duration_seconds": "Histogram",
        "failed_records": "Counter",
    },
    "reconciliation": {
        "count_mismatch": "Gauge",
        "checksum_failures": "Counter",
    }
}
```

---

## Summary: Pipeline Steps

| Step | Action | Performance Target |
| --- | --- | --- |
| 1 | **Pre-check** | Verify connections, disk space |
| 2 | **Disable SF Triggers** | Reduce load time by 50% |
| 3 | **Extract (Parallel)** | 10 workers × 500K chunks |
| 4 | **Transform** | Field mapping + data types |
| 5 | **Stage (CSV)** | GZIP compression |
| 6 | **Load (Bulk API 2.0)** | 15 parallel jobs |
| 7 | **Reconcile** | Count + Checksum + Aggregates |
| 8 | **Enable SF Triggers** | Restore normal operation |
| 9 | **Report** | Send summary notification |

### Estimated Timeline (3 Years Data)

| Phase | Tables | Records | Est. Time |
| --- | --- | --- | --- |
| 1-3 | Reference + PreInv | ~2M | 1 hour |
| 4 | KPS_T_SALES_M | 108M | 8-10 hours |
| 5 | KPS_T_SALES_MD | 261M | 20-24 hours |
| 6 | KPS_T_SALESPAY_MD | 109M | 8-10 hours |
| 7 | Supporting tables | ~1M | 1 hour |
| 8 | Reconciliation | - | 2 hours |
| **Total** | **16 tables** | **~481M** | **~42-48 hours** |
