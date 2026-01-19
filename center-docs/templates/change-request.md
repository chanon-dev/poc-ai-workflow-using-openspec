# Change Request: [Brief Title]

## Metadata

| Field | Value |
|-------|-------|
| Requested By | [Name/Team] |
| Date | YYYY-MM-DD |
| Priority | Critical / High / Medium / Low |
| Status | PENDING |

---

## Description

[อธิบายสั้นๆ ว่าต้องการเปลี่ยนแปลงอะไร]

---

## Affected Tables

| Source Table | Target Object | Change Type |
|--------------|---------------|-------------|
| `KPS_T_XXX` | `KPS_XXX__c` | Add Field / Modify Mapping / Remove Field |

---

## Field Changes

### New Fields (ถ้ามี)

| Oracle Column | SF Field | Data Type | Transformation | Required |
|---------------|----------|-----------|----------------|----------|
| `NEW_FIELD` | `New_Field__c` | Text(50) | Direct | No |

### Modified Fields (ถ้ามี)

| Oracle Column | SF Field | Current | New |
|---------------|----------|---------|-----|
| `FIELD_NAME` | `Field__c` | Direct | CASE WHEN... |

### Removed Fields (ถ้ามี)

| Oracle Column | SF Field | Reason |
|---------------|----------|--------|
| `OLD_FIELD` | `Old_Field__c` | Deprecated |

---

## Business Rules

[อธิบาย business rules ที่เกี่ยวข้อง]

- Rule 1: ...
- Rule 2: ...

---

## Validation Rules

[อธิบาย validation ที่ต้องเพิ่ม/แก้ไข]

- [ ] Field X must not be NULL
- [ ] Value must be in range [A, B, C]

---

## Dependencies

- [ ] ต้องรอ change XXX เสร็จก่อน
- [ ] ต้อง deploy Salesforce field ก่อน

---

## Notes

[หมายเหตุเพิ่มเติม]
