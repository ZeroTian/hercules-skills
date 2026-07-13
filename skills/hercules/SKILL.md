---
name: hercules
description: "Single public entry for adaptive Hercules task routing: understand the task, discover only relevant local capabilities, compose internal workflows, and degrade without installing dependencies."
version: 1.1.1
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, entry, routing, adaptive-orchestration]
---

# Hercules

## Purpose

This is the single public entry. Translate the user task into task capability roles, use the session capability cache when fresh, and route only to the internal workflows needed for this task.

## Interface Contract

- Hercules is exposed as this Skill and its linked references; it does not imply that a `hercules` executable, plugin command, or public `discover`/`execute` subcommand exists.
- Load the Skill and only the references required by the current capability role. Perform shallow facility discovery directly from locally visible executable/version/authority evidence.
- Never synthesize commands such as `hercules discover` or `hercules execute`. Invoke a same-named command only when its executable is confirmed in the current session and locally inspected Hercules documentation explicitly defines that command.
- This restriction does not block Skill/reference loading or direct invocation of confirmed facilities such as Claude Code, Codex CLI, browser tools, or Hermes itself.
- Treat `capability_matrix.py` and the normalized contracts as internal deterministic references, not as proof of a public shell interface.

## Routing

Use the [runtime routing reference](references/runtime-routing.md) as the role-to-destination navigation table for this decision.

1. Preserve explicit user preferences and project instructions.
2. Classify task capability roles: implementation, review, browser, research, parallel execution, data access, or project initialization.
3. When capability evidence is missing, stale, incomplete, permission-mismatched, or invalidated, load [capability discovery](references/capability-discovery.md) and follow its normalized capability-map contract.
4. For implementation, browser, research, parallel execution, or data access, load [collaborative workflow](references/collaborative-workflow.md).
5. When scoped or independent review is required, load [review workflow](references/review-workflow.md).
6. For repository-local AI instructions, load [project initialization](references/project-init.md).
7. Prefer a confirmed local facility; fallback to another confirmed facility or Hermes itself.
8. Report a blocker only when no safe path can satisfy the task.

## Boundaries

- Never install or configure external facilities.
- Never inspect credentials or proactively test provider access.
- Missing optional facilities are silent unless the current task needs them.
- Re-scan after a relevant config change or capability-related invocation failure.

## Completion

Return the selected route, relevant confirmed capabilities, fallback used, and verification result. Do not print a full inventory unless the user asks.
