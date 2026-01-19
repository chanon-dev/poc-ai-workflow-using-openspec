# Constraints: Oracle Extraction Settings

## Overview

การตั้งค่า Oracle สำหรับ extraction ที่มีประสิทธิภาพ

---

## Parallel Query Settings

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `parallel_extract` | 8-10 | Number of parallel streams |
| `ROWNUM` chunking | 500,000 | Records per chunk |
| Fetch size | 10,000 | Rows per fetch |

---

## Connection Pool

```
Min Connections: 5
Max Connections: 20
Connection Timeout: 30s
Query Timeout: 300s (5 min)
```

---

## Extraction Strategy

### ROWNUM-Based Chunking
```sql
SELECT /*+ PARALLEL(t, 8) */
    *
FROM KPS_T_SALES_MD t
WHERE ROWNUM BETWEEN :start_row AND :end_row
ORDER BY SALES_ID;
```

### Date-Based Partitioning (Alternative)
```sql
SELECT *
FROM KPS_T_SALES_MD
WHERE SALES_DATE BETWEEN :start_date AND :end_date
ORDER BY SALES_ID;
```

---

## Resource Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| Temp Tablespace | Monitor usage | Large sorts |
| Undo Tablespace | Sufficient for long queries | |
| Network Bandwidth | 1 Gbps+ recommended | |

---

## Performance Tuning

### Index Hints
```sql
SELECT /*+ INDEX(t IDX_SALES_DATE) */
    *
FROM KPS_T_SALES_MD t
WHERE SALES_DATE >= :start_date;
```

### Avoid Full Table Scans
- Use indexed columns in WHERE clause
- Prefer range scans over full scans

---

## Monitoring Queries

```sql
-- Check long-running queries
SELECT sid, serial#, sql_id, elapsed_time
FROM v$session
WHERE status = 'ACTIVE'
  AND username = 'MIGRATION_USER';

-- Check temp usage
SELECT tablespace_name, bytes_used/1024/1024 MB_USED
FROM v$temp_space_header;
```

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-01-19 | Initial spec | System |
