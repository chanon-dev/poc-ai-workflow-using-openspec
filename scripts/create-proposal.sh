#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# create-proposal.sh - Create OpenSpec proposal using Claude Code
#
# Uses: /openspec:proposal skill
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

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  CREATE PROPOSAL - /openspec:proposal${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check for claude CLI
# Check for AI CLI
if command -v claude &> /dev/null; then
    AI_CLI="claude"
    CMD_PROPOSAL="/openspec:proposal"
    CMD_APPLY="/openspec:apply"
elif command -v antigravity &> /dev/null; then
    AI_CLI="antigravity chat"
    CMD_PROPOSAL="/openspec-proposal"
    CMD_APPLY="/openspec-apply"
elif command -v anty &> /dev/null; then
    AI_CLI="anty chat"
    CMD_PROPOSAL="/openspec-proposal"
    CMD_APPLY="/openspec-apply"
else
    echo -e "${RED}ERROR: No AI CLI found (claude, antigravity, or anty)${NC}"
    echo "Install Claude Code: npm install -g @anthropic-ai/claude-code"
    echo "Or install Antigravity"
    exit 1
fi

# Step 1: Detect changes first
echo -e "${YELLOW}Step 1: Detecting pending changes...${NC}"
echo ""
"$SCRIPT_DIR/detect-changes.sh"

# Step 2: Confirm
echo ""
read -p "Create proposal from these changes? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Step 3: Run /openspec:proposal via Claude Code
echo ""
echo -e "${YELLOW}Step 2: Running /openspec:proposal...${NC}"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"

cd "$PROJECT_ROOT"

if [[ "$AI_CLI" == *"antigravity"* ]] || [[ "$AI_CLI" == *"anty"* ]]; then
    echo -e "${YELLOW}🚀 Launching Antigravity Chat in your editor...${NC}"
    $AI_CLI "$CMD_PROPOSAL"
    echo ""
    echo -e "${YELLOW}The script is paused. Please complete the proposal generation in the editor.${NC}"
    read -p "Press [Enter] when done..."
else
    $AI_CLI "$CMD_PROPOSAL"
fi

echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${GREEN}Proposal created!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review proposal in openspec/changes/<change-id>/"
echo "  2. Get team approval"
echo "  3. Run: ./scripts/apply-change.sh <change-id>"
echo "     Or: $AI_CLI \"$CMD_APPLY <change-id>\""
