#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# archive-change.sh - Archive completed change using Claude Code
#
# Uses: /openspec:archive skill
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
echo -e "${BLUE}  ARCHIVE CHANGE - /openspec:archive${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check for claude CLI
if ! command -v claude &> /dev/null; then
    echo -e "${RED}ERROR: Claude Code CLI not found${NC}"
    echo "Install: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Check arguments
if [ -z "$CHANGE_ID" ]; then
    echo -e "${YELLOW}Usage: $0 <change-id>${NC}"
    echo ""
    echo "Changes available to archive:"
    echo ""

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
    read -p "Enter change-id to archive: " CHANGE_ID

    if [ -z "$CHANGE_ID" ]; then
        echo "No change-id provided. Exiting."
        exit 1
    fi
fi

# Confirm deployment
echo -e "${YELLOW}⚠️  IMPORTANT: Only archive AFTER successful deployment!${NC}"
echo ""
read -p "Has '$CHANGE_ID' been deployed to production? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Archive cancelled. Deploy first, then archive."
    exit 0
fi

# Run /openspec:archive via Claude Code
echo ""
echo -e "${YELLOW}Running /openspec:archive ${CHANGE_ID}...${NC}"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"

cd "$PROJECT_ROOT"
claude "/openspec:archive $CHANGE_ID"

echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${GREEN}Archive complete!${NC}"
echo ""
echo "Results:"
echo "  - Change moved to: openspec/changes/archive/"
echo "  - Specs updated in: openspec/specs/"
echo ""
echo "Don't forget to:"
echo "  1. Update center-docs/CHANGELOG.md status to [DEPLOYED]"
echo "  2. Commit and push changes"
