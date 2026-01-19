# AI Workflow Usage Guide

The project includes an automated AI workflow script `scripts/ai-run.sh` that streamlines the **OpenSpec** methodology. It supports both **Claude Code** and **Antigravity**.

## Prerequisites

You need at least one of the following AI agents installed:

- **Claude Code**:

  ```bash
  npm install -g @anthropic-ai/claude-code
  ```

- **Antigravity**:
  Ensure the `antigravity` or `anty` command is available in your PATH.

## Quick Start

To run the full workflow (Detect changes → Create Proposal → Apply Changes):

```bash
./scripts/ai-run.sh
```

## Options

### 1. Dry Run (Analysis Only)

Analyze pending changes and specifications without modifying any files or creating proposals.

```bash
./scripts/ai-run.sh --dry-run
```

### 2. Apply Only

Skip detection and proposal creation. Just implement any existing proposals found in `openspec/changes/`.

```bash
./scripts/ai-run.sh --apply-only
```

### 3. Force Specific Agent

By default, the script attempts to use `claude` first, then `antigravity`. You can force a specific agent:

```bash
# Force Claude Code
./scripts/ai-run.sh --use-claude

# Force Antigravity
./scripts/ai-run.sh --use-antigravity
```

## How It Works

The `ai-run.sh` script orchestrates the following process:

1. **Detection**: Scans `center-docs/CHANGELOG.md` and specs to find pending changes.
2. **Proposal**:
    - If pending changes are found, it runs `scripts/create-proposal.sh`.
    - Uses the agent (e.g., `/openspec:proposal` or `/openspec-proposal` for Antigravity) to generate a detailed implementation plan in `openspec/changes/`.
3. **Review**: (User intervention usually happens here, but the script can be interactive).

    > **Note for Antigravity Users**:
    > When using Antigravity, the script will launch a chat session in your code editor and **pause**.
    > 1. Complete the task in the editor (the prompt is sent automatically).
    > 2. Return to the terminal.
    > 3. Press **Enter** to resume the script.
4. **Implementation**:
    - Runs `scripts/apply-change.sh`.
    - Uses the agent (e.g., `/openspec:apply` or `/openspec-apply` for Antigravity) to write code and update configurations.

## Helper Scripts

You can also run individual steps manually:

- **Create Proposal**:

  ```bash
  ./scripts/create-proposal.sh
  ```

- **Apply Change**:

  ```bash
  ./scripts/apply-change.sh [change-id]
  ```
