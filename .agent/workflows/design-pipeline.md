---
description: Design full pipeline for an entity (mapping, extract, transform, load, validate, reconcile)
---

# /design-pipeline

Design complete pipeline for an entity with all ETL stages.

## Usage

```bash
/design-pipeline <entity>
```

## Steps

1. Read entity info from `center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md`
2. Extract mapping info (KP Table/Field → SFDC Table/Field)
3. Design pipeline stages:
   - **Source**: Oracle tables, columns
   - **Extract**: SQL query design
   - **Transform**: Type conversions needed
   - **Load**: Bulk API config
   - **Validate**: GX expectations (source + extract)
   - **Reconcile**: Count comparison strategy
4. Output to `docs/pipelines/<entity>_pipeline.md`

## Example

```bash
/design-pipeline 01_Account
```

Creates `docs/pipelines/01_account_pipeline.md` with full pipeline design.
