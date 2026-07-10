---
name: hercules
description: "Single public entry for adaptive Hercules task routing: understand the task, discover only relevant local capabilities, compose internal workflows, and degrade without installing dependencies."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, entry, routing, adaptive-orchestration]
    related_skills: [hercules-capability-discovery, hercules-collaborative-workflow, hercules-review-workflow, hercules-project-init]
---

# Hercules

## Purpose

This is the single public entry. Translate the user task into task capability roles, use the session capability cache when fresh, and route only to the internal Skills needed for this task.

## Routing

1. Preserve explicit user preferences and project instructions.
2. Classify task capability roles: implementation, review, browser, research, parallel execution, data access, or project initialization.
3. Load `hercules-capability-discovery` only for roles whose local capability evidence is missing or stale.
4. Route execution to `hercules-collaborative-workflow`, review to `hercules-review-workflow`, and project setup to `hercules-project-init`.
5. Prefer a confirmed local facility; fallback to another confirmed facility or Hermes itself.
6. Report a blocker only when no safe path can satisfy the task.

## Boundaries

- Never install or configure external facilities.
- Never inspect credentials or proactively test provider access.
- Missing optional facilities are silent unless the current task needs them.
- Re-scan after a relevant config change or capability-related invocation failure.

## Completion

Return the selected route, relevant confirmed capabilities, fallback used, and verification result. Do not print a full inventory unless the user asks.
