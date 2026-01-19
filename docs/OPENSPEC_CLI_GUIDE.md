# OpenSpec CLI Complete Guide

> คู่มือการใช้งาน OpenSpec CLI สำหรับทุก use case ในการทำงานจริง

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Setup & Initialize](#setup--initialize)
3. [Daily Workflow Commands](#daily-workflow-commands)
4. [Creating Change Proposals](#creating-change-proposals)
5. [Validation](#validation)
6. [Viewing & Inspecting](#viewing--inspecting)
7. [Archiving Changes](#archiving-changes)
8. [Real-World Scenarios](#real-world-scenarios)
9. [Troubleshooting](#troubleshooting)

---

## Quick Reference

```bash
# Essential commands (80% ของการใช้งาน)
openspec list                  # ดู changes ที่กำลังดำเนินการ
openspec list --specs          # ดู specs ทั้งหมด
openspec show <item>           # ดูรายละเอียด change หรือ spec
openspec validate <change>     # ตรวจสอบ change
openspec archive <change> -y   # Archive หลัง deploy

# Validation (ใช้ก่อน commit)
openspec validate <change> --strict --no-interactive

# Debugging
openspec show <change> --json --deltas-only
```

---

## Setup & Initialize

### Case 1: Initialize ใน Project ใหม่

```bash
# Interactive mode (แนะนำ)
openspec init

# หรือระบุ path
openspec init /path/to/project

# Non-interactive mode (สำหรับ CI/CD)
openspec init --tools claude,cursor,github-copilot
```

**Tools ที่รองรับ:**

- `claude`, `cursor`, `github-copilot`, `windsurf`, `antigravity`
- `cline`, `continue`, `roocode`, `codex`, `gemini`
- ใช้ `all` หรือ `none` สำหรับเลือกทั้งหมด

### Case 2: Update Instruction Files

```bash
# อัพเดท AGENTS.md และไฟล์ต่างๆ เป็น version ล่าสุด
openspec update

# ระบุ path
openspec update /path/to/project
```

---

## Daily Workflow Commands

### ดูสถานะ Project

```bash
# ดู changes ที่กำลังดำเนินการ
openspec list
openspec list --changes        # เหมือนกัน (default)
openspec list --sort name      # sort ตามชื่อ
openspec list --sort recent    # sort ตามวันที่ (default)

# ดู specs ทั้งหมด
openspec list --specs

# Output เป็น JSON (สำหรับ scripting)
openspec list --json
openspec list --specs --json
```

### ดู Dashboard แบบ Interactive

```bash
# เปิด dashboard
openspec view
```

---

## Creating Change Proposals

### Case 1: Add New Feature

```bash
# 1. สร้าง directory structure
mkdir -p openspec/changes/add-email-alerts/specs/notifications

# 2. สร้าง proposal.md
cat > openspec/changes/add-email-alerts/proposal.md << 'EOF'
# Change: Add Email Alerts

## Why
ต้องการ notify team เมื่อ migration fail

## What Changes
- เพิ่ม email notification system

## Impact
- Affected specs: notifications (NEW)
- Affected code: `dags/`, `plugins/alerts.py`
EOF

# 3. สร้าง tasks.md
cat > openspec/changes/add-email-alerts/tasks.md << 'EOF'
## 1. Implementation
- [ ] 1.1 Create `plugins/email_alerts.py`
- [ ] 1.2 Add EmailOperator to DAGs
- [ ] 1.3 Write unit tests
- [ ] 1.4 Update documentation
EOF

# 4. สร้าง spec delta (ADDED)
cat > openspec/changes/add-email-alerts/specs/notifications/spec.md << 'EOF'
## ADDED Requirements

### Requirement: Email Alert on Failure
The system SHALL send email alerts when migration fails.

#### Scenario: Send alert on task failure
- **WHEN** any migration task fails
- **THEN** email is sent to configured recipients within 5 minutes
EOF

# 5. Validate
openspec validate add-email-alerts --strict --no-interactive
```

### Case 2: Modify Existing Feature

```bash
mkdir -p openspec/changes/update-chunk-size/specs/extraction

# ⚠️ สำคัญ: ต้อง copy requirement เดิมมาแก้ทั้งก้อน
cat > openspec/changes/update-chunk-size/specs/extraction/spec.md << 'EOF'
## MODIFIED Requirements

### Requirement: Chunk Size Configuration
The system SHALL extract data in chunks of **1,000,000 records**.

#### Scenario: Large table extraction
- **WHEN** extracting table with >10M records
- **THEN** each chunk contains exactly 1,000,000 records

#### Scenario: Memory constraint
- **WHEN** processing chunk
- **THEN** memory usage stays below 4GB
EOF

openspec validate update-chunk-size --strict --no-interactive
```

### Case 3: Remove Feature

```bash
mkdir -p openspec/changes/remove-legacy-export/specs/extraction

cat > openspec/changes/remove-legacy-export/specs/extraction/spec.md << 'EOF'
## REMOVED Requirements

### Requirement: Legacy CSV Export
**Reason**: ถูกแทนที่ด้วย GZIP compression
**Migration**: ใช้ `--gzip` flag แทน
EOF
```

### Case 4: Rename Feature

```bash
cat > openspec/changes/rename-auth/specs/auth/spec.md << 'EOF'
## RENAMED Requirements
- FROM: `### Requirement: Login`
- TO: `### Requirement: User Authentication`
EOF
```

### Case 5: Multiple Changes (Add + Modify)

```bash
# สร้าง structure สำหรับหลาย capabilities
mkdir -p openspec/changes/enhance-pipeline/specs/{extraction,monitoring}

# extraction - MODIFIED
cat > openspec/changes/enhance-pipeline/specs/extraction/spec.md << 'EOF'
## MODIFIED Requirements

### Requirement: Parallel Extraction
The system SHALL support 15 parallel workers (was 10).

#### Scenario: Maximum throughput
- **WHEN** running at full capacity
- **THEN** throughput exceeds 5000 records/second
EOF

# monitoring - ADDED
cat > openspec/changes/enhance-pipeline/specs/monitoring/spec.md << 'EOF'
## ADDED Requirements

### Requirement: Real-time Progress
The system SHALL display real-time progress dashboard.

#### Scenario: Dashboard update
- **WHEN** migration is running
- **THEN** progress updates every 30 seconds
EOF
```

---

## Validation

### Basic Validation

```bash
# Validate specific change
openspec validate add-email-alerts

# Validate with strict mode (แนะนำก่อน commit)
openspec validate add-email-alerts --strict

# Non-interactive (สำหรับ CI/CD)
openspec validate add-email-alerts --strict --no-interactive
```

### Bulk Validation

```bash
# Validate all changes
openspec validate --changes

# Validate all specs
openspec validate --specs

# Validate everything
openspec validate --all

# Parallel validation (เร็วขึ้น)
openspec validate --all --concurrency 8
```

### JSON Output (สำหรับ CI/CD)

```bash
# Output เป็น JSON
openspec validate add-email-alerts --json

# ใช้กับ jq
openspec validate add-email-alerts --json | jq '.errors'
```

### Validation Flags Summary

| Flag | Purpose |
|------|---------|
| `--strict` | ตรวจสอบละเอียด (แนะนำ) |
| `--no-interactive` | ไม่ถาม prompt (สำหรับ CI) |
| `--json` | Output JSON |
| `--all` | Validate ทุกอย่าง |
| `--changes` | Validate changes ทั้งหมด |
| `--specs` | Validate specs ทั้งหมด |
| `--concurrency <n>` | จำนวน parallel (default: 6) |

---

## Viewing & Inspecting

### ดู Change Details

```bash
# แบบ interactive (ถ้าไม่ระบุชื่อ)
openspec show

# ดู change เฉพาะ
openspec show add-email-alerts

# ระบุ type (กรณีชื่อซ้ำกับ spec)
openspec show my-feature --type change
```

### ดู Spec Details

```bash
# ดู spec
openspec show extraction --type spec

# หรือใช้ subcommand
openspec spec show extraction
```

### JSON Output (สำหรับ debugging)

```bash
# ดู change เป็น JSON
openspec show add-email-alerts --json

# ดูเฉพาะ deltas (spec changes)
openspec show add-email-alerts --json --deltas-only

# ดู requirements อย่างเดียว (ไม่รวม scenarios)
openspec show extraction --json --requirements --type spec

# ดู requirement เฉพาะ (by ID)
openspec show extraction --json -r 1 --type spec

# ไม่แสดง scenario content
openspec show extraction --json --no-scenarios --type spec
```

### List Specs พร้อมรายละเอียด

```bash
# List specs แบบละเอียด
openspec spec list --long

# List specs เป็น JSON
openspec spec list --json
```

---

## Archiving Changes

### หลังจาก Deploy เสร็จ

```bash
# Archive change (มี confirmation)
openspec archive add-email-alerts

# Skip confirmation (สำหรับ CI/CD)
openspec archive add-email-alerts --yes
# หรือ
openspec archive add-email-alerts -y
```

### กรณี Infrastructure/Doc Changes

```bash
# ไม่ต้อง update specs (tooling, docs, config changes)
openspec archive update-ci-pipeline --skip-specs -y
```

### Skip Validation (ไม่แนะนำ)

```bash
# ข้าม validation (ต้อง confirm)
openspec archive add-email-alerts --no-validate
```

### Archive Flags Summary

| Flag | Purpose |
|------|---------|
| `-y, --yes` | ไม่ถาม confirmation |
| `--skip-specs` | ไม่ update specs (สำหรับ tooling changes) |
| `--no-validate` | ข้าม validation (ไม่แนะนำ) |

---

## Real-World Scenarios

### Scenario 1: เริ่มทำ Feature ใหม่

```bash
# 1. ดู context ปัจจุบัน
openspec list              # ดู changes ที่กำลังทำ
openspec list --specs      # ดู specs ที่มี

# 2. ค้นหา specs ที่เกี่ยวข้อง
rg -n "Requirement:" openspec/specs

# 3. สร้าง proposal
mkdir -p openspec/changes/add-retry-logic/specs/extraction
# ... สร้างไฟล์ต่างๆ ...

# 4. Validate
openspec validate add-retry-logic --strict --no-interactive

# 5. Request review จาก team
```

### Scenario 2: แก้ไข Spec ที่มีอยู่

```bash
# 1. ดู spec ปัจจุบัน
openspec show extraction --type spec

# 2. ดู JSON เพื่อเข้าใจ structure
openspec show extraction --json --type spec | jq '.requirements'

# 3. สร้าง change proposal
mkdir -p openspec/changes/update-extraction/specs/extraction

# 4. Copy requirement เดิมมาแก้
# ... แก้ไขใน spec.md ...

# 5. Validate และ verify
openspec validate update-extraction --strict --no-interactive
openspec show update-extraction --json --deltas-only
```

### Scenario 3: หลาย Changes พร้อมกัน

```bash
# ดู changes ทั้งหมดที่กำลังทำ
openspec list

# Validate ทั้งหมดก่อน merge
openspec validate --changes --strict --no-interactive

# ตรวจสอบ conflicts
openspec list --json | jq '.[].specs'
```

### Scenario 4: CI/CD Integration

```yaml
# .github/workflows/openspec.yml
name: OpenSpec Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install OpenSpec
        run: npm install -g @anthropic/openspec
      
      - name: Validate all changes
        run: openspec validate --changes --strict --no-interactive --json
      
      - name: Validate all specs
        run: openspec validate --specs --strict --no-interactive --json
```

### Scenario 5: Debug ปัญหา Validation

```bash
# ดู error ละเอียด
openspec validate my-change --strict --json | jq '.errors'

# ดู deltas ที่ parse ได้
openspec show my-change --json --deltas-only | jq '.'

# ตรวจสอบ scenario format
rg -n "#### Scenario:" openspec/changes/my-change/

# Common fixes:
# - Scenario ต้องใช้ #### (4 hashtags)
# - ทุก requirement ต้องมี scenario
# - MODIFIED ต้อง copy ทั้ง requirement
```

### Scenario 6: Post-Deployment Cleanup

```bash
# 1. Verify implementation matches spec
openspec validate --specs --strict --no-interactive

# 2. Archive completed change
openspec archive add-email-alerts -y

# 3. Verify archive
ls openspec/changes/archive/

# 4. Verify specs updated
openspec list --specs
```

---

## Troubleshooting

### Error: "Change must have at least one delta"

```bash
# ตรวจสอบว่ามี spec files
ls openspec/changes/<change>/specs/

# ตรวจสอบ format
# ต้องมี ## ADDED|MODIFIED|REMOVED Requirements
cat openspec/changes/<change>/specs/*/spec.md
```

### Error: "Requirement must have at least one scenario"

```bash
# ❌ ผิด
### Requirement: My Feature
The system SHALL do something.

# ✅ ถูก
### Requirement: My Feature
The system SHALL do something.

#### Scenario: Success case
- **WHEN** user does action
- **THEN** expected result
```

### Error: Scenario ไม่ถูก parse

```bash
# ❌ ผิด (ใช้ 3 hashtags)
### Scenario: Test

# ❌ ผิด (ใช้ bullet)
- **Scenario: Test**

# ✅ ถูก (ใช้ 4 hashtags)
#### Scenario: Test
```

### Debug Commands

```bash
# ดู JSON output ละเอียด
openspec show my-change --json | jq '.'

# ดูเฉพาะ deltas
openspec show my-change --json --deltas-only

# ค้นหา pattern ใน specs
rg -n "Requirement:|Scenario:" openspec/specs
rg -n "^\s*####" openspec/changes/

# ตรวจสอบ file structure
find openspec/changes -name "*.md"
```

---

## Command Reference

| Command | Description |
|---------|-------------|
| `openspec init` | Initialize OpenSpec ใน project |
| `openspec update` | Update instruction files |
| `openspec list` | List changes (default) |
| `openspec list --specs` | List specifications |
| `openspec view` | Interactive dashboard |
| `openspec show <item>` | Show change or spec details |
| `openspec validate <item>` | Validate change or spec |
| `openspec archive <change>` | Archive completed change |
| `openspec spec list` | List all specs |
| `openspec spec show <spec>` | Show specific spec |

---

## Best Practices

1. **ใช้ `--strict --no-interactive` เสมอก่อน commit**
2. **ตั้งชื่อ change-id เป็น verb-led:** `add-`, `update-`, `remove-`, `refactor-`
3. **MODIFIED ต้อง copy requirement เดิมมาทั้งก้อน**
4. **ทุก requirement ต้องมี scenario อย่างน้อย 1 อัน**
5. **Archive ทันทีหลัง deploy** เพื่อ keep specs in sync
