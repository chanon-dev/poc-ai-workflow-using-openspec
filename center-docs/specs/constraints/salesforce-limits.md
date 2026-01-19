# Constraints: Salesforce Limits

## Overview

ข้อจำกัดของ Salesforce Bulk API 2.0 ที่ต้องคำนึงถึง

---

## API Limits

| Limit | Value | Our Setting |
|-------|-------|-------------|
| Max File Size | 150 MB | Use GZIP compression |
| Max Records per File | 150,000,000 | N/A |
| Max Concurrent Jobs | 100 | **Limit to 15** |
| Records per 24hr Rolling | 150,000,000 | Plan batches |

---

## Bulk API 2.0 Specifications

### Job Limits
- Max 100 concurrent ingest jobs
- Max 10,000 batches per job
- Max 150 MB per file (compressed)

### Record Processing
- ~3,000 records/second throughput target
- Async processing (poll for status)

---

## Rate Limiting Strategy

### Concurrent Job Management
```
Max Parallel Jobs: 15 (conservative)
Jobs per Table: Based on priority
Retry on 429: Exponential backoff
```

### Daily Volume Planning
```
150M records/day limit
Target: 100M records/day (safety margin)

Day 1: KPS_T_SALES_MD (100M)
Day 2: KPS_T_SALES_MD (100M)
Day 3: KPS_T_SALES_MD (61M) + KPS_T_SALESPAY_MD (39M)
...
```

---

## File Size Management

### GZIP Compression
```
Raw CSV: ~500 MB → Compressed: ~50 MB
Compression Ratio: ~10:1
```

### Chunk Size
```
Records per Chunk: 500,000
Estimated Chunk Size: ~40-50 MB (compressed)
```

---

## Error Handling

| Error Code | Meaning | Action |
|------------|---------|--------|
| 429 | Rate Limited | Wait & retry (exponential backoff) |
| 500 | Server Error | Retry up to 3 times |
| DUPLICATE_VALUE | Duplicate External ID | Skip or update |

---

## Change History

| Date | Change | Author |
|------|--------|--------|
| 2025-01-19 | Initial spec | System |
