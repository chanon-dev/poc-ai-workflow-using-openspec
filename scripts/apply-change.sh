#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# apply-change.sh - Apply approved OpenSpec change using Claude Code
#
# Uses: /openspec:apply skill
# OpenSpec: https://github.com/Fission-AI/OpenSpec
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CHANGE_ID="$1"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  APPLY CHANGE - /openspec:apply${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check for claude CLI
# Check for AI CLI
if command -v claude &> /dev/null; then
    AI_CLI="claude"
    CMD_APPLY="/openspec:apply"
elif command -v antigravity &> /dev/null; then
    AI_CLI="antigravity chat"
    CMD_APPLY="/openspec-apply"
elif command -v anty &> /dev/null; then
    AI_CLI="anty chat"
    CMD_APPLY="/openspec-apply"
else
    echo -e "${RED}ERROR: No AI CLI found (claude, antigravity, or anty)${NC}"
    echo "Install Claude Code: npm install -g @anthropic-ai/claude-code"
    echo "Or install Antigravity"
    exit 1
fi

# Check arguments
if [ -z "$CHANGE_ID" ]; then
    echo -e "${YELLOW}Usage: $0 <change-id>${NC}"
    echo ""
    echo "Available changes:"
    echo ""

    # List changes directory
    CHANGES_DIR="$PROJECT_ROOT/openspec/changes"
    if [ -d "$CHANGES_DIR" ]; then
        for dir in "$CHANGES_DIR"/*/; do
            if [ -d "$dir" ] && [ "$(basename "$dir")" != "archive" ]; then
                echo "  - $(basename "$dir")"
            fi
        done
    else
        echo "  (no changes found)"
    fi

    echo ""
    read -p "Enter change-id: " CHANGE_ID

    if [ -z "$CHANGE_ID" ]; then
        echo "No change-id provided. Exiting."
        exit 1
    fi
fi

# Confirm
echo -e "${YELLOW}⚠️  This will implement change: ${CHANGE_ID}${NC}"
echo ""
read -p "Continue? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Run /openspec:apply via Claude Code
echo ""
echo -e "${YELLOW}Running /openspec:apply ${CHANGE_ID}...${NC}"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"

cd "$PROJECT_ROOT"
$AI_CLI "$CMD_APPLY $CHANGE_ID"

echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${GREEN}Implementation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review generated code"
echo "  2. Run tests"
echo "  3. Create PR for review"
echo "  4. After deploy: ./scripts/archive-change.sh $CHANGE_ID"
