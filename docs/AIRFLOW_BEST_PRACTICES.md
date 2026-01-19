# Apache Airflow Best Practices

> Based on [Official Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

---

## Table of Contents

1. [Writing DAGs](#writing-dags)
2. [Task Design Principles](#task-design-principles)
3. [Variables & Connections](#variables--connections)
4. [Testing DAGs](#testing-dags)
5. [Reducing DAG Complexity](#reducing-dag-complexity)
6. [Handling Dependencies](#handling-dependencies)
7. [Production Deployment](#production-deployment)

---

## Writing DAGs

### Avoid Expensive Top-Level Code

The scheduler continuously parses DAG files. Minimize expensive operations at module level.

❌ **Bad - Runs on every parse:**

```python
from airflow.sdk import DAG, task

def expensive_api_call():
    sleep(1000)
    return "Hello"

my_response = expensive_api_call()  # Executed on EVERY parse!

with DAG(dag_id="my_dag", ...):
    @task()
    def print_result():
        print(my_response)
```

✅ **Good - Runs only during execution:**

```python
from airflow.sdk import DAG, task

with DAG(dag_id="my_dag", ...):
    @task()
    def print_result():
        result = expensive_api_call()  # Only during task execution
        print(result)
```

### Move Expensive Imports Into Functions

```python
# ❌ Bad - imported on every parse
import pandas as pd
from heavy_library import process_data

# ✅ Good - imported only when task runs
@task()
def process():
    import pandas as pd
    from heavy_library import process_data
    # use them here
```

### Use Default Arguments

Define repetitive parameters in `default_args` to prevent typos:

```python
default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
}

with DAG(
    dag_id="my_dag",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
):
    ...
```

---

## Task Design Principles

### 1. Idempotency

Tasks should produce the same result when run multiple times.

```python
# ❌ Bad - creates duplicates on retry
INSERT INTO table VALUES (...)

# ✅ Good - safe to retry
INSERT INTO table VALUES (...)
ON CONFLICT (id) DO UPDATE SET ...
```

### 2. Use Data Intervals (Not `now()`)

```python
# ❌ Bad - non-deterministic
@task()
def process():
    data = get_data(timestamp=datetime.now())

# ✅ Good - deterministic, replayable
@task()
def process(data_interval_start):
    data = get_data(timestamp=data_interval_start)
```

### 3. Don't Rely on Local Filesystem

Tasks may run on different workers. Use remote storage:

```python
# ❌ Bad - file may not exist on another worker
with open("/tmp/data.csv") as f:
    process(f)

# ✅ Good - use remote storage
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@task()
def process():
    hook = S3Hook()
    data = hook.read_key("bucket/data.csv")
```

### 4. Use XCom for Small Data

```python
@task()
def extract():
    return {"key": "value"}  # Automatically pushed to XCom

@task()
def transform(data):  # Automatically pulled from XCom
    return process(data)

extract() >> transform()
```

For large data, store in S3/GCS and pass the path via XCom.

---

## Variables & Connections

### Avoid Variable.get() at Top Level

❌ **Bad - Database call on every parse:**

```python
from airflow.sdk import Variable

foo = Variable.get("foo")  # Network call!

with DAG(...):
    task = BashOperator(
        bash_command=f"echo {Variable.get('bar')}"  # Another call!
    )
```

✅ **Good - Use Jinja templates (lazy evaluation):**

```python
with DAG(...):
    task = BashOperator(
        bash_command="echo {{ var.value.foo }}",  # Evaluated at runtime
    )
```

✅ **Good - Access inside task:**

```python
@task()
def my_task():
    foo = Variable.get("foo")  # Only during execution
    print(foo)
```

### Store Credentials in Connections

```python
# ❌ Bad - hardcoded credentials
password = "secret123"

# ✅ Good - use Airflow Connections
from airflow.hooks.base import BaseHook

conn = BaseHook.get_connection("my_database")
password = conn.password
```

---

## Testing DAGs

### 1. Syntax Check

```bash
python dags/my_dag.py
```

### 2. Measure Parse Time

```bash
time python dags/my_dag.py
```

### 3. Unit Test DAG Loading

```python
import pytest
from airflow.models import DagBag

@pytest.fixture()
def dagbag():
    return DagBag()

def test_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id="my_dag")
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 3
```

### 4. Test DAG Structure

```python
def test_dag_structure():
    from dags.my_dag import dag

    expected = {
        "extract": ["transform"],
        "transform": ["load"],
        "load": [],
    }

    for task_id, downstream in expected.items():
        task = dag.get_task(task_id)
        assert task.downstream_task_ids == set(downstream)
```

### 5. Mock Variables and Connections

```python
from unittest import mock
from airflow.models import Variable, Connection

# Mock variable
with mock.patch.dict("os.environ", AIRFLOW_VAR_MY_VAR="test-value"):
    assert Variable.get("my_var") == "test-value"

# Mock connection
conn = Connection(conn_type="postgres", host="localhost", login="user")
with mock.patch.dict("os.environ", AIRFLOW_CONN_MY_DB=conn.get_uri()):
    assert Connection.get_connection_from_secrets("my_db").host == "localhost"
```

### 6. Add Self-Check Tasks

```python
upload = UploadToS3(task_id="upload", ...)

verify = S3KeySensor(
    task_id="verify_upload",
    bucket_key="s3://bucket/output.parquet",
    poke_interval=0,
    timeout=0,
)

upload >> verify
```

---

## Reducing DAG Complexity

### 1. Optimize Parsing Speed

| Action | Impact |
|--------|--------|
| Move imports inside tasks | Faster parse |
| Use Jinja for variables | No DB calls |
| Split large DAG files | Parallel processing |

### 2. Simplify Task Dependencies

```python
# ✅ Prefer linear chains
task_a >> task_b >> task_c

# ⚠️ Avoid deep nested trees
#     a
#    /|\
#   b c d
#  /|\ ...
```

### 3. Use DAG Factories

```python
# dag_factory.py
def create_dag(dag_id, schedule, tasks):
    with DAG(dag_id=dag_id, schedule=schedule, ...) as dag:
        for task in tasks:
            ...
    return dag

# dags/dag_a.py
from dag_factory import create_dag
dag = create_dag("dag_a", "@daily", [...])

# dags/dag_b.py
from dag_factory import create_dag
dag = create_dag("dag_b", "@hourly", [...])
```

---

## Handling Dependencies

### Option 1: PythonVirtualenvOperator

Creates isolated environment per task:

```python
@task.virtualenv(requirements=["pandas==2.0.0", "requests"])
def process_data():
    import pandas as pd
    # task code
```

**Pros:** No setup, dynamic environments
**Cons:** Overhead, needs PyPI access

### Option 2: ExternalPythonOperator

Uses pre-built Python environment:

```python
@task.external_python(python="/opt/venvs/ml/bin/python")
def ml_task():
    import sklearn
    # task code
```

**Pros:** No runtime overhead, pre-vetted deps
**Cons:** Requires environment setup

### Option 3: DockerOperator

Full container isolation:

```python
from airflow.providers.docker.operators.docker import DockerOperator

task = DockerOperator(
    task_id="run_in_docker",
    image="my-image:latest",
    command="python /scripts/process.py",
)
```

**Pros:** Complete isolation, any language
**Cons:** Requires Docker knowledge, image pipeline

### Option 4: KubernetesPodOperator

```python
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

task = KubernetesPodOperator(
    task_id="k8s_task",
    image="my-image:latest",
    cmds=["python", "process.py"],
    namespace="airflow",
)
```

---

## Production Deployment

### 1. Database Maintenance

```bash
# Clean old metadata
airflow db clean --clean-before-timestamp "2024-01-01"
```

### 2. Upgrade Checklist

1. ✅ Backup metadata database
2. ✅ Pause all DAGs: `airflow dags pause <dag_id>`
3. ✅ Run integration tests
4. ✅ Prune old data (can be slow)
5. ✅ Upgrade Airflow
6. ✅ Enable DAGs gradually

### 3. Environment-Specific Config

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

### 4. Watcher Pattern for Failure Handling

```python
from airflow.exceptions import AirflowException
from airflow.utils.trigger_rule import TriggerRule

@task(trigger_rule=TriggerRule.ONE_FAILED, retries=0)
def watcher():
    raise AirflowException("A task has failed!")

with DAG(...) as dag:
    t1 = task_1()
    t2 = task_2()
    cleanup = cleanup_task()

    t1 >> t2 >> cleanup
    [t1, t2] >> watcher()
```

### 5. Use ruff for Code Quality

```bash
# Install
pip install "ruff>=0.14.10"

# Check for Airflow 3.0 deprecations
ruff check dags/ --select AIR3
```

---

## Quick Reference Card

| Do ✅ | Don't ❌ |
|------|---------|
| Use `{{ var.value.x }}` | Call `Variable.get()` at top level |
| Store secrets in Connections | Hardcode credentials |
| Make tasks idempotent | Use `INSERT` without conflict handling |
| Use `data_interval_start` | Use `datetime.now()` |
| Store large data in S3/GCS | Pass large data via XCom |
| Test DAG loading | Deploy untested DAGs |
| Use linear dependencies | Create complex nested graphs |
| Move imports inside tasks | Import heavy libs at module level |

---
---

## Python Code Quality

### 1. Type Hinting (Strongly Recommended)

Airflow DAGs are complex. Type hints prevent 50% of bugs.

```python
# ❌ Bad
def process_data(data, limit):
    ...

# ✅ Good
from typing import List, Dict, Any

def process_data(data: List[Dict[str, Any]], limit: int = 100) -> None:
    ...
```

### 2. Explicit Imports

Avoid `from module import *`. It pollutes the namespace and causes conflicts with Airflow context variables.

```python
# ❌ Bad
from airflow.operators.python import *

# ✅ Good
from airflow.operators.python import PythonOperator
```

### 3. Use Pydantic for Configuration

Pass configuration as objects, not dictionaries. This validates data types early.

```python
from pydantic import BaseModel

class TableConfig(BaseModel):
    table_name: str
    chunk_size: int = 50000

# Usage in Task
@task()
def process(config: dict):
    # Auto-validates types
    cfg = TableConfig(**config)
    print(cfg.chunk_size)
```

### 4. Exception Handling

Handle specific errors, let Airflow retry transient ones.

```python
# ✅ Good
try:
    api.get_data()
except ValueError as e:
    # Permanent error: Fail task immediately (no retry)
    raise AirflowFailException(e)
except ConnectionError:
    # Transient error: Raise normally so Airflow retries
    raise
```

---

## Official Resources

- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Testing DAGs](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-dags)
