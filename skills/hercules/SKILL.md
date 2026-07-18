---
name: hercules
description: "Single public entry for adaptive Hercules task routing: understand the task, discover only relevant local capabilities, compose internal workflows, and degrade without installing dependencies."
version: 1.1.5
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
- Load the Skill and only the references required by the current capability role. Perform shallow facility discovery directly from locally visible executable/version/authority evidence, but treat that as container evidence only; it cannot satisfy an implied or explicit specialized requirement without task-relevant surface preflight.
- Never synthesize commands such as `hercules discover` or `hercules execute`. Invoke a same-named command only when its executable is confirmed in the current session and locally inspected Hercules documentation explicitly defines that command.
- This restriction does not block Skill/reference loading or direct invocation of confirmed facilities such as Claude Code, Codex CLI, browser tools, or Hermes itself.
- Treat `capability_matrix.py` and the normalized contracts as internal deterministic references, not as proof of a public shell interface.
- Hermes controller owns Hercules routing. After it selects a facility, the route is complete: the selected facility executes the bounded brief directly and must not load Hercules, must not perform capability discovery, must not select another facility, and must not apply controller fallback. It returns results or failure to Hermes.

## Routing

Use the [runtime routing reference](references/runtime-routing.md) as the role-to-destination navigation table for this decision.

1. Preserve explicit user preferences and project instructions.
2. Classify both broad task capability roles and any concrete `required_capabilities` implied by the task, such as video transcription, browser automation, or a specific data operation.
3. When broad-role or concrete-surface evidence is missing, stale, incomplete, permission-mismatched, or invalidated, load [capability discovery](references/capability-discovery.md) and follow its normalized capability-map contract. Before selecting Claude, Codex, or another extensible facility, complete the task-relevant preflight across plausible built-ins, MCP tools, enabled plugins, nested Skills, agents, teams, and commands; executable/version evidence alone cannot prove a specialized requirement.
4. For implementation, browser, research, parallel execution, or data access, load [collaborative workflow](references/collaborative-workflow.md).
5. When invoking a confirmed facility, load [invocation lifecycle](references/invocation-lifecycle.md): choose foreground/background scheduling and PTY/non-PTY as independent decisions, and keep the work observable.
6. When scoped or independent review is required, load [review workflow](references/review-workflow.md).
7. For repository-local AI instructions, load [project initialization](references/project-init.md).
8. Prefer a confirmed local facility; fallback to another confirmed facility or Hermes itself.
9. Report a blocker only when no safe path can satisfy the task.

## Boundaries

- Never install or configure external facilities.
- Never inspect credentials or proactively test provider access.
- Missing optional facilities are silent unless the current task needs them.
- Re-scan after a relevant config change or capability-related invocation failure.
- User or project preference may rank only facilities that already cover every concrete requirement with current evidence; it never bypasses the preflight completion gate.
- Broad-role evidence, authority, and specialized-surface evidence must be explicit; never default missing evidence or treat executable/version-only evidence as proof of a specialized surface. Reuse cache records only for an exact concrete-requirement match and return only task-relevant surfaces.

## Completion

Return the selected route, relevant confirmed capabilities, fallback used, and verification result. Do not print a full inventory unless the user asks.
