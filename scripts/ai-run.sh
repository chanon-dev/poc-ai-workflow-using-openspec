#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# ai-run.sh - AI Workflow (supports Claude Code & Antigravity)
#
# Usage:
#   ./scripts/ai-run.sh                    # AI ทำทุกอย่าง
#   ./scripts/ai-run.sh --dry-run          # AI วิเคราะห์เท่านั้น
#   ./scripts/ai-run.sh --apply-only       # Apply existing proposals
#   ./scripts/ai-run.sh --use-claude       # Force use Claude Code
#   ./scripts/ai-run.sh --use-antigravity  # Force use Antigravity
#
# Supports:
#   - Claude Code CLI (claude)
#   - Antigravity (antigravity / anty)
#
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════════════════
# Detect available AI CLI
# ═══════════════════════════════════════════════════════════════════════════════

detect_ai_cli() {
    # Defaults
    CMD_PROPOSAL="/openspec:proposal"
    CMD_APPLY="/openspec:apply"

    # Check for forced option
    for arg in "$@"; do
        case $arg in
            --use-claude)
                if command -v claude &> /dev/null; then
                    AI_CLI="claude"
                    AI_NAME="Claude Code"
                    return 0
                else
                    echo -e "${RED}ERROR: Claude Code CLI not found${NC}"
                    exit 1
                fi
                ;;
            --use-antigravity)
                if command -v antigravity &> /dev/null; then
                    AI_CLI="antigravity"
                    AI_NAME="Antigravity"
                    CMD_PROPOSAL="/openspec-proposal"
                    CMD_APPLY="/openspec-apply"
                    return 0
                elif command -v anty &> /dev/null; then
                    AI_CLI="anty"
                    AI_NAME="Antigravity (anty)"
                    CMD_PROPOSAL="/openspec-proposal"
                    CMD_APPLY="/openspec-apply"
                    return 0
                else
                    echo -e "${RED}ERROR: Antigravity CLI not found${NC}"
                    exit 1
                fi
                ;;
        esac
    done

    # Auto-detect
    if command -v claude &> /dev/null; then
        AI_CLI="claude"
        AI_NAME="Claude Code"
    elif command -v antigravity &> /dev/null; then
        AI_CLI="antigravity"
        AI_NAME="Antigravity"
        CMD_PROPOSAL="/openspec-proposal"
        CMD_APPLY="/openspec-apply"
    elif command -v anty &> /dev/null; then
        AI_CLI="anty"
        AI_NAME="Antigravity (anty)"
        CMD_PROPOSAL="/openspec-proposal"
        CMD_APPLY="/openspec-apply"
    else
        echo -e "${RED}ERROR: No AI CLI found${NC}"
        echo ""
        echo "Please install one of:"
        echo "  - Claude Code: npm install -g @anthropic-ai/claude-code"
        echo "  - Antigravity: See https://antigravity.dev"
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# Run AI with prompt
# ═══════════════════════════════════════════════════════════════════════════════

run_ai() {
    local prompt="$1"
    echo -e "${CYAN}Using: $AI_NAME ($AI_CLI)${NC}"
    echo ""
    $AI_CLI "$prompt"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

detect_ai_cli "$@"
cd "$PROJECT_ROOT"

# Parse mode (excluding --use-* flags)
MODE=""
for arg in "$@"; do
    case $arg in
        --dry-run) MODE="dry-run" ;;
        --apply-only) MODE="apply-only" ;;
        --help|-h) MODE="help" ;;
        --use-*) ;; # Skip
        *) ;;
    esac
done

case "$MODE" in
    dry-run)
        echo -e "${GREEN}🔍 AI Dry Run - Analyzing only...${NC}"
        echo ""
        run_ai "วิเคราะห์ center-docs/ และสรุปว่ามี pending changes อะไรบ้าง:

1. อ่าน center-docs/CHANGELOG.md หา [PENDING]
2. อ่าน center-docs/changes/*.md
3. อ่าน center-docs/specs/

สรุป:
- มี pending changes กี่รายการ
- แต่ละรายการต้องทำอะไร
- ถ้าจะ implement จะต้องแก้ไขไฟล์อะไรบ้าง

**ไม่ต้อง implement** แค่วิเคราะห์และสรุปเท่านั้น"
        ;;

    apply-only)
        echo -e "${GREEN}⚡ AI Apply Only - Implementing existing proposals...${NC}"
        echo ""
        run_ai "ดู openspec/changes/ และ implement proposals ที่มีอยู่:

1. List all active changes in openspec/changes/
2. For each change, run $CMD_APPLY
3. สรุปผลการ implement

ถ้าไม่มี proposals ให้แจ้งว่าไม่มี"
        ;;

    help)
        echo "AI-Run: One command, AI does everything"
        echo ""
        echo "Supports: Claude Code CLI & Antigravity"
        echo ""
        echo "Usage:"
        echo "  ./scripts/ai-run.sh                    AI ทำทุกอย่าง"
        echo "  ./scripts/ai-run.sh --dry-run          AI วิเคราะห์เท่านั้น"
        echo "  ./scripts/ai-run.sh --apply-only       Apply existing proposals"
        echo ""
        echo "Options:"
        echo "  --use-claude       Force use Claude Code"
        echo "  --use-antigravity  Force use Antigravity"
        echo "  --help             Show this help"
        echo ""
        echo "Detected: $AI_NAME"
        ;;

    *)
        echo -e "${GREEN}🚀 AI Full Workflow${NC}"
        echo -e "${CYAN}Using: $AI_NAME${NC}"
        echo ""
        run_ai "ทำ Data Migration workflow อัตโนมัติ:

## Step 1: Detect
- อ่าน center-docs/CHANGELOG.md หา [PENDING]
- อ่าน center-docs/changes/ หา change requests
- อ่าน center-docs/specs/ เข้าใจ current specs

## Step 2: Propose
- ถ้ามี pending changes → สร้าง proposal ด้วย $CMD_PROPOSAL
- ถ้าไม่มี → ข้ามไป Step 3

## Step 3: Apply
- ถ้ามี proposals ใน openspec/changes/ → implement ด้วย $CMD_APPLY
- Generate code ตาม tasks
- Update configs

## Step 4: Summary
- สรุปทุกอย่างที่ทำ
- List files ที่สร้าง/แก้ไข
- แจ้ง next steps (ถ้ามี)

ถ้าไม่มี pending changes และไม่มี proposals ให้แจ้งว่า 'ไม่มีงานที่ต้องทำ ระบบ up-to-date'"
        ;;
esac
