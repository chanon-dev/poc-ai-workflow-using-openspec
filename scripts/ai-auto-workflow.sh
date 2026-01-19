#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# ai-auto-workflow.sh - AI ทำทุกขั้นตอนอัตโนมัติ
#
# AI จะ:
# 1. อ่าน center-docs หา pending changes
# 2. สร้าง proposal อัตโนมัติ
# 3. Implement ทันที (หรือรอ approve ก่อน)
# 4. Archive หลังเสร็จ
#
# OpenSpec: https://github.com/Fission-AI/OpenSpec
# ═══════════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║     █████╗ ██╗    ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██╗      ██████╗ ██╗    ██╗ ║
║    ██╔══██╗██║    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║     ██╔═══██╗██║    ██║ ║
║    ███████║██║    ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ █████╗  ██║     ██║   ██║██║ █╗ ██║ ║
║    ██╔══██║██║    ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ██╔══╝  ██║     ██║   ██║██║███╗██║ ║
║    ██║  ██║██║    ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗██║     ███████╗╚██████╔╝╚███╔███╔╝ ║
║    ╚═╝  ╚═╝╚═╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝  ║
║                                                                           ║
║                    FULLY AUTOMATED AI WORKFLOW                            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check for claude CLI
if ! command -v claude &> /dev/null; then
    echo -e "${RED}ERROR: Claude Code CLI not found${NC}"
    echo "Install: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Mode selection
echo -e "${YELLOW}Select mode:${NC}"
echo ""
echo "  1) Auto-propose  - AI อ่าน center-docs แล้วสร้าง proposal"
echo "  2) Auto-apply    - AI implement change ที่ระบุ"
echo "  3) Auto-all      - AI ทำทุกอย่าง (propose → apply)"
echo "  4) Full-auto     - AI ทำทุกอย่างรวม archive (propose → apply → archive)"
echo ""
read -p "Enter choice [1-4]: " mode

cd "$PROJECT_ROOT"

case $mode in
    1)
        echo ""
        echo -e "${GREEN}Running: AI Auto-Propose${NC}"
        echo ""

        claude "ทำตามขั้นตอนนี้อัตโนมัติ:

1. อ่าน center-docs/CHANGELOG.md หา entries ที่ [PENDING]
2. อ่าน center-docs/changes/ หา change request files
3. อ่าน center-docs/specs/ เข้าใจ current specifications
4. สร้าง OpenSpec proposal ด้วย /openspec:proposal
5. สรุปผลว่าสร้าง proposal อะไรบ้าง

ถ้าไม่มี pending changes ให้แจ้งว่าไม่มีอะไรต้องทำ"
        ;;

    2)
        echo ""
        read -p "Enter change-id to apply: " change_id

        if [ -z "$change_id" ]; then
            echo "No change-id provided"
            exit 1
        fi

        echo ""
        echo -e "${GREEN}Running: AI Auto-Apply ($change_id)${NC}"
        echo ""

        claude "Implement change '$change_id' อัตโนมัติ:

1. อ่าน openspec/changes/$change_id/proposal.md เข้าใจว่าต้องทำอะไร
2. อ่าน openspec/changes/$change_id/tasks.md ดู checklist
3. อ่าน openspec/changes/$change_id/design.md (ถ้ามี)
4. ใช้ /openspec:apply $change_id เพื่อ implement
5. Mark ทุก tasks เป็น completed
6. สรุปผลว่า implement อะไรบ้าง"
        ;;

    3)
        echo ""
        echo -e "${GREEN}Running: AI Auto-All (Propose → Apply)${NC}"
        echo ""

        claude "ทำ Data Migration workflow อัตโนมัติทั้งหมด:

## Phase 1: Detect & Propose
1. อ่าน center-docs/CHANGELOG.md หา [PENDING] entries
2. อ่าน center-docs/changes/ หา change requests
3. อ่าน center-docs/specs/ เข้าใจ specifications
4. สร้าง proposal ด้วย /openspec:proposal

## Phase 2: Implement
5. หลังสร้าง proposal เสร็จ ให้ implement ทันทีด้วย /openspec:apply
6. Generate code ตาม tasks.md
7. Update configurations
8. Mark tasks completed

## Summary
9. สรุปทุกอย่างที่ทำ:
   - Proposals ที่สร้าง
   - Code ที่ generate
   - Files ที่แก้ไข

ถ้าไม่มี pending changes ให้แจ้งว่าไม่มีอะไรต้องทำ"
        ;;

    4)
        echo ""
        echo -e "${GREEN}Running: AI Full-Auto (Propose → Apply → Archive)${NC}"
        echo -e "${YELLOW}⚠️  Warning: This will also archive changes (usually done after deploy)${NC}"
        echo ""
        read -p "Continue? (y/n): " -n 1 -r
        echo ""

        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Cancelled"
            exit 0
        fi

        claude "ทำ Data Migration workflow ครบทุกขั้นตอน:

## Phase 1: Detect & Propose
1. อ่าน center-docs/CHANGELOG.md หา [PENDING]
2. อ่าน center-docs/changes/ และ center-docs/specs/
3. สร้าง proposal ด้วย /openspec:proposal

## Phase 2: Implement
4. Implement ทันทีด้วย /openspec:apply <change-id>
5. Generate code, update configs
6. Mark tasks completed

## Phase 3: Archive
7. Archive change ด้วย /openspec:archive <change-id>
8. Update specs to final state

## Summary
9. สรุปครบทุกอย่าง:
   - Changes ที่ประมวลผล
   - Code ที่ generate
   - Files ที่แก้ไข
   - Archives ที่สร้าง

ถ้าไม่มี pending changes ให้แจ้งว่าไม่มีอะไรต้องทำ"
        ;;

    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  AI Workflow Complete${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
