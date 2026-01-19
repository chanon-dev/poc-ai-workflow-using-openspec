<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this project.

## Project Overview

This is a **KPC TMS Data Migration** project using Apache Airflow for orchestrating data migration workflows.

## Tech Stack

- **Orchestration:** Apache Airflow 3.x (Docker Compose, CeleryExecutor)
- **Source System:** Oracle Database (On-Premise)
- **Target System:** Salesforce (Cloud)
- **ETL Tool:** Salesforce Data Loader CLI (Bulk API)
- **Database:** PostgreSQL (Airflow metadata)
- **Message Broker:** Redis (Celery broker)
- **Container Runtime:** Docker & Docker Compose

## Migration Overview

> **Note:** Migration includes 2-3 years historical data (ข้อมูลย้อนหลัง 2-3 ปี)

| Source Table | Target Object | Per Year | 2-3 Years Total |
| --- | --- | --- | --- |
| KPS_T_SALES_MD | KPS_Sales__c | ~87M | **174M - 261M** |
| KPS_T_SALESPAY_MD | KPS_SalesPay__c | ~36M | **73M - 109M** |
| KPS_T_SALES_M | KPS_SalesM__c | ~36M | **72M - 108M** |
| Others (13 tables) | Various | < 500K | < 1.5M |

**Total Migration Volume:** ~522M - 783M records

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design.

## Project Structure

```text
kpc-tms-data-migration/
├── dags/                     # Airflow DAG files
│   ├── dag_factory.py        # Auto-generates all migration DAGs
│   ├── config/
│   │   └── tables_config.py  # Table configurations (add tables here)
│   └── reconciliation_dag.py # Data reconciliation DAG
├── plugins/                  # Custom Airflow plugins
├── config/                   # Configuration files
│   ├── process-conf.xml      # Salesforce Data Loader config
│   ├── config.properties     # SF connection properties
│   └── mappings/             # Field mapping files (.sdl)
├── great_expectations/       # GX data validation
│   ├── expectations/         # Expectation suites
│   ├── checkpoints/          # Checkpoint configs
│   └── plugins/              # Custom expectations
├── docs/                     # Documentation
│   ├── AIRFLOW_SETUP.md      # Setup documentation
│   ├── AIRFLOW_BEST_PRACTICES.md # Best practices guide
│   ├── ARCHITECTURE.md       # Migration architecture design
│   ├── PIPELINE_DESIGN.md    # Complete pipeline implementation
│   ├── MIGRATION_CHECKLIST.md # Expert checklist & audit log
│   └── GREAT_EXPECTATIONS_GUIDE.md # GX integration guide
├── logs/                     # Airflow logs (gitignored)
├── docker-compose.yaml       # Airflow services definition
├── .env                      # Environment variables
└── CLAUDE.md                 # Project guidance for Claude Code
```

## Common Commands

```bash
# Start Airflow
docker compose up -d

# Stop Airflow
docker compose down

# View logs
docker compose logs -f

# Initialize database (first time only)
docker compose up airflow-init

# Access Airflow CLI
docker compose exec airflow-webserver airflow <command>
```

## DAG Development Guidelines

1. **Place DAGs in `./dags/` directory** - Auto-detected by Airflow
2. **Use TaskFlow API** - Preferred way to write tasks in Airflow 3.x
3. **Follow idempotency** - Tasks should be safe to retry
4. **Use Jinja templates** - For variables: `{{ var.value.my_var }}`
5. **Test DAGs locally** - Run `python dags/my_dag.py` to check syntax

## Environment Variables

Key variables in `.env`:

- `AIRFLOW_UID` - User ID for containers
- `AIRFLOW_IMAGE_NAME` - Docker image (default: apache/airflow:3.x)

## Web UI Access

- **URL:** <http://localhost:8080>
- **Credentials:** airflow / airflow (development only)

## Airflow Best Practices

> Based on [Official Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

### Quick Reference

| Do | Don't |
| --- | --- |
| Use `{{ var.value.x }}` | Call `Variable.get()` at top level |
| Store secrets in Connections | Hardcode credentials |
| Make tasks idempotent | Use `INSERT` without conflict handling |
| Use `data_interval_start` | Use `datetime.now()` |
| Store large data in S3/GCS | Pass large data via XCom |
| Test DAG loading | Deploy untested DAGs |
| Move imports inside tasks | Import heavy libs at module level |

### Avoid Expensive Top-Level Code

The scheduler continuously parses DAG files. Minimize expensive operations at module level.

```python
# ❌ Bad - Runs on every parse
my_response = expensive_api_call()

with DAG(...):
    @task()
    def print_result():
        print(my_response)

# ✅ Good - Runs only during execution
with DAG(...):
    @task()
    def print_result():
        result = expensive_api_call()
        print(result)
```

### Avoid Variable.get() at Top Level

```python
# ❌ Bad - Database call on every parse
foo = Variable.get("foo")

# ✅ Good - Use Jinja templates (lazy evaluation)
task = BashOperator(
    bash_command="echo {{ var.value.foo }}",
)

# ✅ Good - Access inside task
@task()
def my_task():
    foo = Variable.get("foo")
```

### Task Design Principles

**1. Idempotency** - Tasks should produce same result on retry:

```sql
-- Use UPSERT instead of INSERT
INSERT INTO table VALUES (...)
ON CONFLICT (id) DO UPDATE SET ...
```

**2. Use Data Intervals** - Not `now()`:

```python
@task()
def process(data_interval_start):
    data = get_data(timestamp=data_interval_start)
```

**3. Don't Rely on Local Filesystem** - Use remote storage:

```python
# Use S3/GCS instead of local files
hook = S3Hook()
data = hook.read_key("bucket/data.csv")
```

### Testing DAGs

```bash
# Syntax check
python dags/my_dag.py

# Measure parse time
time python dags/my_dag.py
```

```python
# Unit test
import pytest
from airflow.models import DagBag

def test_dag_loaded():
    dagbag = DagBag()
    dag = dagbag.get_dag(dag_id="my_dag")
    assert dagbag.import_errors == {}
    assert dag is not None
```

### Mock Variables and Connections

```python
from unittest import mock
from airflow.models import Variable, Connection

# Mock variable
with mock.patch.dict("os.environ", AIRFLOW_VAR_MY_VAR="test-value"):
    assert Variable.get("my_var") == "test-value"

# Mock connection
conn = Connection(conn_type="postgres", host="localhost")
with mock.patch.dict("os.environ", AIRFLOW_CONN_MY_DB=conn.get_uri()):
    assert Connection.get_connection_from_secrets("my_db").host == "localhost"
```

### Handling Task Dependencies

**Option 1: PythonVirtualenvOperator** - Dynamic isolated environment:

```python
@task.virtualenv(requirements=["pandas==2.0.0"])
def process_data():
    import pandas as pd
```

**Option 2: DockerOperator** - Full container isolation:

```python
task = DockerOperator(
    task_id="run_in_docker",
    image="my-image:latest",
    command="python /scripts/process.py",
)
```

**Option 3: KubernetesPodOperator** - K8s pod isolation:

```python
task = KubernetesPodOperator(
    task_id="k8s_task",
    image="my-image:latest",
    cmds=["python", "process.py"],
)
```

### Environment-Specific Config

```python
import os

ENV = os.environ.get("AIRFLOW_ENV", "dev")

if ENV == "prod":
    S3_BUCKET = "prod-bucket"
    SCHEDULE = "@hourly"
else:
    S3_BUCKET = "dev-bucket"
    SCHEDULE = None  # Manual trigger only
```

### Code Quality with ruff

```bash
pip install "ruff>=0.14.10"
ruff check dags/ --select AIR3  # Check Airflow 3.0 deprecations
```

### Database Maintenance

```bash
# Clean old metadata
airflow db clean --clean-before-timestamp "2024-01-01"
```

## Official Resources

- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
