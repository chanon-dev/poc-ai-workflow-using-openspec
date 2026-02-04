---
description: Reconcile Oracle vs Salesforce counts
---

# /reconcile

Run reconciliation between Oracle source and Salesforce target.

## Usage

```bash
/reconcile <entity>
```

## Steps

1. Get Oracle count for entity
2. Get Salesforce count for target object
3. Compare counts
4. Display results

## Example

```bash
/reconcile 01_Account

# Output:
# Oracle (KPS_R_SHOP): 15,234
# Salesforce (Account): 15,234
# Difference: 0
# Status: ✅ MATCH
```
