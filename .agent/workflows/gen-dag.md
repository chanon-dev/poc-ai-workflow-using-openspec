---
description: Generate migration DAG for a single entity (e.g., /gen-dag 01_Account)
---

Generate an Airflow DAG for a specific entity from the mapping document.

## Usage

```
/gen-dag <entity_name>
```

Examples:

- `/gen-dag 01_Account`
- `/gen-dag 17_Units`
- `/gen-dag 12_Product & Price`

## Steps

1. **Parse entity name from user input**
   - If no entity provided, ask user to specify one
   - Suggest running `/gen-dag-list` to see available entities

2. **Read Skill instructions**
   - Read `.agent/skills/generate-migration-dag/SKILL.md`

3. **Execute the Skill**
   - Follow the Skill instructions to generate the DAG
   - Read mapping document for entity details
   - Read template DAG for structure
   - Create new DAG file

4. **Report results**
   - Show file path created
   - Show source tables used
   - Show SQL query preview
