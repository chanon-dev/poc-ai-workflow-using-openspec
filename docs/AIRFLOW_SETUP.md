# Apache Airflow Docker Setup Guide

## Download Official Docker Compose File

### Method 1: Using curl (Recommended)

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

**Flags explained:**
- `-L` : Follow redirects
- `-f` : Fail silently on server errors
- `-O` : Save file with original name

### Method 2: Using wget

```bash
wget https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml
```

### Method 3: Direct Download

Download directly from browser:
- URL: https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml

---

## Quick Start

### 1. Create Required Directories

```bash
mkdir -p ./dags ./logs ./plugins ./config
```

| Directory | Purpose |
|-----------|---------|
| `dags/` | Store your DAG files |
| `logs/` | Airflow logs |
| `plugins/` | Custom plugins |
| `config/` | Configuration files |

### 2. Set Environment Variables

**Linux/macOS:**
```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

**Windows (PowerShell):**
```powershell
echo "AIRFLOW_UID=50000" > .env
```

### 3. Initialize Database

```bash
docker compose up airflow-init
```

Wait until you see the message:
```
airflow-init_1 | Upgrades done
airflow-init_1 | Admin user created
```

### 4. Start Airflow

```bash
docker compose up -d
```

### 5. Access Web UI

- **URL:** http://localhost:8080
- **Username:** `airflow`
- **Password:** `airflow`

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `docker compose up -d` | Start all services |
| `docker compose down` | Stop all services |
| `docker compose down -v` | Stop and remove volumes |
| `docker compose ps` | Check running services |
| `docker compose logs -f` | View logs |

---

## Requirements

- Docker Engine: 20.10.0+
- Docker Compose: v2.14.0+
- Memory: 4GB minimum (8GB recommended)

---

## Official Documentation

- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Apache Airflow GitHub](https://github.com/apache/airflow)
