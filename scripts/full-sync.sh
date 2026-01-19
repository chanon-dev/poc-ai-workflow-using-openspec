#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# full-sync.sh - AI-Driven Migration Workflow using OpenSpec + Claude Code
#
# OpenSpec: https://github.com/Fission-AI/OpenSpec
# Uses Claude Code CLI with /openspec skills
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║     ██╗  ██╗██████╗  ██████╗    ████████╗███╗   ███╗███████╗             ║"
echo "║     ██║ ██╔╝██╔══██╗██╔════╝    ╚══██╔══╝████╗ ████║██╔════╝             ║"
echo "║     █████╔╝ ██████╔╝██║            ██║   ██╔████╔██║███████╗             ║"
echo "║     ██╔═██╗ ██╔═══╝ ██║            ██║   ██║╚██╔╝██║╚════██║             ║"
echo "║     ██║  ██╗██║     ╚██████╗       ██║   ██║ ╚═╝ ██║███████║             ║"
echo "║     ╚═╝  ╚═╝╚═╝      ╚═════╝       ╚═╝   ╚═╝     ╚═╝╚══════╝             ║"
echo "║                                                                           ║"
echo "║              AI-DRIVEN DATA MIGRATION WORKFLOW                            ║"
echo "║              Powered by OpenSpec + Claude Code                            ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for claude CLI
if ! command -v claude &> /dev/null; then
    echo -e "${RED}ERROR: Claude Code CLI not found${NC}"
    echo ""
    echo "Install Claude Code CLI:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
    echo "Or see: https://docs.anthropic.com/en/docs/claude-code"
    exit 1
fi

echo ""
echo -e "${BLUE}Workflow Steps:${NC}"
echo "  1. Detect changes in center-docs"
echo "  2. Create OpenSpec proposal (/openspec:proposal)"
echo "  3. Review & validate"
echo "  4. Apply changes (/openspec:apply)"
echo "  5. Archive after deploy (/openspec:archive)"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# Menu
# ═══════════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}Select action:${NC}"
echo ""
echo "  1) Detect changes        - ตรวจจับ pending changes"
echo "  2) Create proposal       - /openspec:proposal"
echo "  3) Apply change          - /openspec:apply"
echo "  4) Archive change        - /openspec:archive"
echo "  5) Full workflow         - ทำทั้งหมด (1→2→3)"
echo "  0) Exit"
echo ""
read -p "Enter choice [0-5]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}  DETECT CHANGES${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        "$SCRIPT_DIR/detect-changes.sh"
        ;;

    2)
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}  CREATE PROPOSAL - /openspec:proposal${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "Running Claude Code with /openspec:proposal..."
        echo ""
        cd "$PROJECT_ROOT"
        claude "/openspec:proposal"
        ;;

    3)
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}  APPLY CHANGE - /openspec:apply${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo ""
        read -p "Enter change-id to apply: " change_id
        if [ -n "$change_id" ]; then
            cd "$PROJECT_ROOT"
            claude "/openspec:apply $change_id"
        else
            echo "No change-id provided."
        fi
        ;;

    4)
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}  ARCHIVE CHANGE - /openspec:archive${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo ""
        read -p "Enter change-id to archive: " change_id
        if [ -n "$change_id" ]; then
            cd "$PROJECT_ROOT"
            claude "/openspec:archive $change_id"
        else
            echo "No change-id provided."
        fi
        ;;

    5)
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}  FULL WORKFLOW${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        echo ""

        # Step 1: Detect
        echo -e "${YELLOW}Step 1/3: Detecting changes...${NC}"
        "$SCRIPT_DIR/detect-changes.sh"

        echo ""
        read -p "Continue to create proposal? (y/n): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Step 2: Proposal
            echo ""
            echo -e "${YELLOW}Step 2/3: Creating proposal...${NC}"
            cd "$PROJECT_ROOT"
            claude "/openspec:proposal"

            echo ""
            read -p "Apply the proposal? Enter change-id (or skip): " change_id

            if [ -n "$change_id" ]; then
                # Step 3: Apply
                echo ""
                echo -e "${YELLOW}Step 3/3: Applying changes...${NC}"
                claude "/openspec:apply $change_id"
            fi
        fi
        ;;

    0)
        echo "Bye!"
        exit 0
        ;;

    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
