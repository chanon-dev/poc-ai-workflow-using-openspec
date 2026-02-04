---
description: Add or modify a shared service in plugins/
---

# /add-service

Create new service or modify existing service in `plugins/`.

## Usage

```bash
/add-service <service-name> [method-name]
```

## Behavior

- **If service doesn't exist**: Create new service class with method
- **If service exists**: Add/modify method in existing class

## Steps

1. Check if `plugins/<service_name>.py` exists
2. If new:
   - Create service class following existing patterns
   - Add docstrings and type hints
3. If exists:
   - Read existing file
   - Add/modify requested method
4. Ensure imports and logging are correct

## Examples

```bash
# Create new service
/add-service entity-config load_yaml

# Add method to existing service
/add-service oracle-service batch_extract
```

## Output

- `plugins/<service_name>.py`
