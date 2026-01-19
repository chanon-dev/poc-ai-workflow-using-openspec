#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# detect-changes.sh - Detect pending changes in center-docs
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CENTER_DOCS="$PROJECT_ROOT/center-docs"
CHANGELOG="$CENTER_DOCS/CHANGELOG.md"
CHANGES_DIR="$CENTER_DOCS/changes"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  DETECT CHANGES - KPC TMS Data Migration${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if center-docs exists
if [ ! -d "$CENTER_DOCS" ]; then
    echo -e "${RED}ERROR: center-docs directory not found${NC}"
    echo "Expected: $CENTER_DOCS"
    exit 1
fi

# 1. Check CHANGELOG for PENDING items
echo -e "${YELLOW}📋 Checking CHANGELOG.md for PENDING items...${NC}"
echo ""

if [ -f "$CHANGELOG" ]; then
    PENDING_COUNT=$(grep -c "\[PENDING\]" "$CHANGELOG" 2>/dev/null || echo "0")

    if [ "$PENDING_COUNT" -gt 0 ]; then
        echo -e "${GREEN}Found $PENDING_COUNT PENDING item(s):${NC}"
        echo "────────────────────────────────────────"
        grep -n "\[PENDING\]" "$CHANGELOG" | head -20
        echo "────────────────────────────────────────"
    else
        echo -e "${GREEN}No PENDING items in CHANGELOG.md${NC}"
    fi
else
    echo -e "${YELLOW}WARNING: CHANGELOG.md not found${NC}"
fi

echo ""

# 2. Check for change request files
echo -e "${YELLOW}📁 Checking changes/ directory...${NC}"
echo ""

if [ -d "$CHANGES_DIR" ]; then
    CHANGE_FILES=$(find "$CHANGES_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

    if [ "$CHANGE_FILES" -gt 0 ]; then
        echo -e "${GREEN}Found $CHANGE_FILES change request file(s):${NC}"
        echo "────────────────────────────────────────"
        ls -la "$CHANGES_DIR"/*.md 2>/dev/null | awk '{print $NF}' | xargs -I {} basename {}
        echo "────────────────────────────────────────"
    else
        echo -e "${GREEN}No pending change requests${NC}"
    fi
else
    echo -e "${YELLOW}WARNING: changes/ directory not found${NC}"
    mkdir -p "$CHANGES_DIR"
    echo "Created: $CHANGES_DIR"
fi

echo ""

# 3. Summary
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  SUMMARY${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

TOTAL_PENDING=$((PENDING_COUNT + CHANGE_FILES))

if [ "$TOTAL_PENDING" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Total pending items: $TOTAL_PENDING${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review the pending changes"
    echo "  2. Run: claude \"/openspec:proposal\""
    echo "  3. Or run: ./scripts/create-proposal.sh"
else
    echo -e "${GREEN}✅ No pending changes detected${NC}"
fi

echo ""
