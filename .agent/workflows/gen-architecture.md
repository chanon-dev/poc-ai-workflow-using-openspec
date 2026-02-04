---
description: Generate architecture documentation for Bulk API system
---

# /gen-architecture

Generate architecture documentation with diagrams.

## Usage

```bash
/gen-architecture [component]
```

## Steps

1. Read existing architecture from `docs/ARCHITECTURE.md`
2. Add/update Bulk API section with:
   - Component diagram (Mermaid)
   - Data flow diagram
   - Service dependencies
3. Output to `docs/BULK_API_ARCHITECTURE.md`

## Example

```bash
/gen-architecture bulk-api
```
