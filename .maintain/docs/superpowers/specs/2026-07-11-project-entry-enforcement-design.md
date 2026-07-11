# Hercules Project Entry Enforcement Design

## Problem

Hercules rules become effective only after an agent explicitly invokes the Hercules Skill. A newly entered project can therefore bypass capability discovery and collaborative routing, or treat a Hermes built-in subagent as Claude Code or Codex CLI.

Project initialization must establish a small, durable entry contract in the project instruction files so that agents load Hercules before selecting or invoking an implementation or review facility.

## Goals

- Make Hercules the default routing entry for project tasks.
- Require capability discovery before selecting Claude Code, Codex CLI, Hermes execution, or another facility.
- Prevent Hermes built-in subagents from being represented as Claude Code or Codex CLI.
- Keep shared rules in one canonical location and avoid three drifting copies.
- Preserve existing project instructions and require preview plus approval before changes.

## Non-goals

- `init.sh` does not edit business repositories or user-level configuration.
- Project initialization does not install, configure, authenticate, or probe external facilities.
- Instruction files do not duplicate the complete Hercules Skill or its internal references.
- Personal writing preferences are not silently converted into project rules.

## Instruction Layout

### `AGENTS.md`: canonical shared contract

Project initialization adds or minimally merges a Hercules entry section that requires agents to:

1. route non-trivial project work through the installed Hercules Skill;
2. inspect project instructions and discover relevant local capabilities before choosing a facility;
3. select only a confirmed facility with sufficient authority;
4. distinguish Hermes built-in subagents from actual Claude Code and Codex CLI invocations;
5. follow Hercules fallback behavior after an invocation failure instead of silently changing identity or authority;
6. independently verify actual outputs before reporting completion.

### `CLAUDE.md`: Claude-specific adapter

The file retains Claude-specific implementation boundaries and adds a short reference to the canonical Hercules entry contract in `AGENTS.md`. It must not copy the complete shared contract.

### `HERMES.md`: controller-specific adapter

The file states that Hermes is the controller, must load the canonical contract and Hercules before routing project work, and must not use `delegate_task` or another built-in subagent as a substitute for a requested or selected Claude Code or Codex CLI facility.

If a repository does not support one of these instruction filenames, initialization updates only supported, applicable files and reports the uncovered surface.

## Initialization Flow

1. Confirm the repository root and read all governing instruction files, including nested rules relevant to the target path.
2. Detect existing Hercules entry rules, conflicts, and unrelated user changes.
3. Build a preview containing exact additions and changed files.
4. Obtain explicit user approval.
5. Apply the smallest merge: shared rules in `AGENTS.md`, short tool-specific adapters elsewhere.
6. Verify references, absence of duplicated shared blocks, preservation of existing content, and final diff.
7. Report changed files, preserved conflicts, uncovered tools, and verification evidence.

Repeated initialization must be idempotent. Existing equivalent rules are retained rather than appended again.

## Failure Handling

- Missing instruction file: create it only when the tool supports that filename and the approved preview includes creation.
- Conflicting existing rule: stop and show the conflict; do not silently override it.
- Hercules unavailable: report a blocker or use an explicitly approved fallback; do not claim Hercules routing occurred.
- Requested facility unavailable or invocation denied: classify the failure and follow Hercules fallback rules; do not replace it with a differently identified subagent.

## Verification

Automated tests should cover:

- `init.sh` never writes `AGENTS.md`, `CLAUDE.md`, or `HERMES.md` in a target project;
- project initialization previews before writing;
- canonical shared contract plus two minimal adapters;
- idempotent repeated initialization;
- preservation of unrelated instructions;
- conflict detection;
- no full shared-rule duplication across files;
- explicit prohibition on representing built-in subagents as Claude Code or Codex CLI.

Manual acceptance uses a fresh sample repository. After initialization, ask Hermes to perform a task requiring implementation and review. It must load Hercules, discover capabilities, identify the selected facility accurately, respect authority boundaries, and verify the result.
