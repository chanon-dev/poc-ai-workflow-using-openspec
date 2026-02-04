---
description: Generate validation and coding rules documentation
---

# /gen-validation-rules

Generate validation rules and coding standards documentation.

## Usage

```bash
/gen-validation-rules
```

## Steps

1. Analyze existing code in `plugins/` and `dags/`
2. Extract patterns and conventions
3. Document:
   - Coding standards
   - Naming conventions
   - Validation rules
   - Error handling patterns
4. Output to `docs/VALIDATION_RULES.md`

## Example

```bash
/gen-validation-rules
```
