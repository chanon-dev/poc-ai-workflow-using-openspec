# AI-Driven Data Migration Workflow

> **OpenSpec**: <https://github.com/Fission-AI/OpenSpec>
>
> **Powered by**: Claude Code CLI

---

## Workflow Overview

```text
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   CENTER DOCS    │     │   CLAUDE CODE    │     │  IMPLEMENTATION  │
│   (Business)     │ ──► │   (AI)           │ ──► │  (Code)          │
└──────────────────┘     └──────────────────┘     └──────────────────┘
     │                         │                        │
     │ Field Mappings          │ /openspec:proposal     │ DAGs
     │ Business Rules          │ /openspec:apply        │ Configs
     │ Constraints             │ /openspec:archive      │ Scripts
     │                         │                        │
     └─────────────────────────┴────────────────────────┘
                    Single Source of Truth
```

---

## Quick Start

```bash
# AI ทำทุกอย่างอัตโนมัติ (recommended)
./scripts/ai-run.sh

# หรือ interactive menu
./scripts/full-sync.sh
```

---

## 4-Step Workflow

### Step 1: Detect Changes

```bash
./scripts/detect-changes.sh
```

ตรวจสอบ `center-docs/CHANGELOG.md` และ `center-docs/changes/` หา pending items

---

### Step 2: Create Proposal

```bash
claude "/openspec:proposal"
```

AI จะ:

- อ่าน center-docs specs
- สร้าง `openspec/changes/<change-id>/`
  - `proposal.md` - Why & What
  - `tasks.md` - Implementation checklist
  - `design.md` - Technical decisions
  - `specs/` - Delta changes

---

### Step 3: Apply Changes

```bash
claude "/openspec:apply <change-id>"
```

หลังจาก team approve แล้ว AI จะ:

- Generate SQL scripts
- Update DAG configs
- Update field mappings
- Run tests

---

### Step 4: Archive

```bash
claude "/openspec:archive <change-id>"
```

หลัง deploy เสร็จ:

- Move to `archive/`
- Update specs
- Mark CHANGELOG as DEPLOYED

---

## Commands Reference

| Action       | Command                                  |
| ------------ | ---------------------------------------- |
| **Detect**   | `./scripts/detect-changes.sh`            |
| **Propose**  | `claude "/openspec:proposal"`            |
| **Apply**    | `claude "/openspec:apply <change-id>"`   |
| **Archive**  | `claude "/openspec:archive <change-id>"` |

### AI Automatic Scripts (Recommended)

| Script                          | Description                      |
| ------------------------------- | -------------------------------- |
| `./scripts/ai-run.sh`           | AI does everything automatically |
| `./scripts/ai-run.sh --dry-run` | AI analyzes only (no changes)    |
| `./scripts/ai-auto-workflow.sh` | Interactive AI workflow menu     |

### Manual Scripts

| Script                             | Description      |
| ---------------------------------- | ---------------- |
| `./scripts/full-sync.sh`           | Interactive menu |
| `./scripts/create-proposal.sh`     | Detect + Propose |
| `./scripts/apply-change.sh <id>`   | Apply change     |
| `./scripts/archive-change.sh <id>` | Archive change   |

### OpenSpec CLI (Optional)

```bash
openspec list                         # ดู active changes
openspec list --specs                 # ดู specs
openspec show <change-id>             # ดู details
openspec validate <id> --strict       # Validate
```

---

## Directory Structure

```text
project/
├── center-docs/                 # 📋 Business specs (SA แก้ไข)
│   ├── CHANGELOG.md             #    Version history
│   ├── specs/
│   │   ├── field-mappings/      #    Field mapping specs
│   │   ├── business-rules/      #    Business logic
│   │   └── constraints/         #    Technical limits
│   ├── changes/                 #    Pending change requests
│   └── templates/               #    Templates
│
├── openspec/                    # 🤖 AI-generated specs
│   ├── changes/                 #    Active proposals
│   │   └── <change-id>/
│   │       ├── proposal.md
│   │       ├── tasks.md
│   │       └── specs/
│   └── specs/                   #    Implemented specs
│
├── scripts/                     # 🔧 Automation scripts
│   ├── full-sync.sh
│   ├── detect-changes.sh
│   ├── create-proposal.sh
│   ├── apply-change.sh
│   └── archive-change.sh
│
└── dags/                        # ⚙️ Implementation (AI generates)
    └── config/
```

---

## Status Flow

```text
PENDING ─────► IN_PROGRESS ─────► IMPLEMENTED ─────► DEPLOYED
   │               │                   │                 │
   ▼               ▼                   ▼                 ▼
 waiting      AI working           PR ready          archived
```

---

## Team Roles

| Role            | Responsibility             | Actions                                    |
| --------------- | -------------------------- | ------------------------------------------ |
| **Business/SA** | Update center-docs         | Edit specs, create change requests         |
| **AI (Claude)** | Generate proposals & code  | `/openspec:proposal`, `/openspec:apply`    |
| **Core Team**   | Review & approve           | Review proposals, approve changes          |
| **DevOps**      | Deploy                     | Deploy to production, trigger archive      |

---

## Example: Add New Field

```bash
# 1. SA creates change request
vim center-docs/changes/2025-01-20-add-loyalty-field.md

# 2. Update CHANGELOG
vim center-docs/CHANGELOG.md
# Add: [2025-01-20] Add LoyaltyTier__c field [PENDING]

# 3. AI creates proposal
claude "/openspec:proposal"
# Output: openspec/changes/add-loyalty-field/

# 4. Team reviews
cat openspec/changes/add-loyalty-field/proposal.md

# 5. After approval - AI implements
claude "/openspec:apply add-loyalty-field"

# 6. After deploy - Archive
claude "/openspec:archive add-loyalty-field"
```
