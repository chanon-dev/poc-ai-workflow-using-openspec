# Proposal: Add Product Price Reconciliation and Great Expectations

**Change ID:** `add-product-price-reconciliation`

## Goal

Implement robust data quality checks and reconciliation for the `migrate_product_price_dag` using strictly Great Expectations (GX), ensuring data integrity from Oracle source to Salesforce target.

## Context

The current `migrate_product_price_dag` performs a basic extraction and load but lacks rigorous validation.

- **Missing:**
  - Pre-extraction checks (Source data quality).
  - Post-extraction checks (CSV integrity).
  - Post-load reconciliation (Oracle vs Salesforce counts and values).
- **Solution:** Integrate Great Expectations as defined in `docs/GREAT_EXPECTATIONS_GUIDE.md`.

## Requirements

1. **Initialize Great Expectations:** Set up the GX project structure if not present.
2. **Source Validation:** Check `KPS_T_REQPROD_MD` and related tables for critical data quality (nulls, types).
3. **Reconciliation:** Verify that the number of records loaded into Salesforce matches the source extraction.
4. **DAG Integration:** Update `migrate_product_price_dag.py` to include `GreatExpectationsOperator` tasks.

## Review Required

- **GX Initialization:** This change will establish the initial GX directory structure.
- **Blocking behavior:** Should validation failures block the pipeline? (Proposed: Yes for Source/Extract, No (Alert only) for Post-Migration).
