---
name: workflow-skill-pack-audit
description: "Use when auditing or maintaining a workflow skill pack: classify skills, reconcile runtime/core/archived candidates, connect task ledgers to trajectories, run validators, and close Codex-reviewed governance tasks."
version: 1.1.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, skills, audit, validation, trajectory, reconciliation]
    related_skills: [hercules-meta-skill-evolution, hercules-skill-pack-management, coding-agent-orchestration]
---

# Workflow Skill Pack Audit

## Overview

Use this class-level skill when auditing or improving a workflow skill pack. The goal is to keep the library small, composable, and runnable: classify skills, identify overlap, reconcile runtime skill directories with intended core lists, connect task ledgers to trajectory records, add deterministic validation, and use Codex review findings to close governance records accurately.

## When to Use

Use when the user asks to:

- deeply audit a skill group for redundancy, atomicity, or organic composition;
- decide whether untracked/newly found skills should become core, optional, archived, merged, or case studies;
- make `TASKS.md` capture trajectory records for future reflection;
- add or review a lightweight skill-pack validation/reflection script;
- reconcile Codex findings about stale ledger evidence or candidate-skill decisions.

## Audit Taxonomy

Classify each skill into one bucket:

1. **entry / composite** — user-facing umbrella that composes atoms and applies user preferences.
2. **atom** — reusable, single-responsibility workflow step.
3. **specialized atom** — reusable but narrower domain/technique.
4. **candidate / duplicate / archived** — overlapping or domain-specific content that should be preserved outside runtime loading until promoted or merged.

Do not force every entry skill to be atomic. Entry wrappers are valid when they prevent the user from manually loading many atoms. Reduce drift by making entry wrappers point to canonical atoms instead of duplicating long procedural prose.

## Reconciliation Procedure

1. Inventory both `git ls-files 'skills/*/SKILL.md'` and visible `find skills -mindepth 2 -maxdepth 2 -name SKILL.md`.
2. Decide candidate disposition: promote core, archive outside runtime loading, or merge/case-study under an existing skill.
3. For archived candidates, preserve `SKILL.md` under a non-runtime path such as `docs/ai-collaboration/candidate-skills/<skill>/SKILL.md` and add a README with disposition and promotion path.
4. If validator compares docs to `git ls-files`, stage newly promoted core skill files before final validation. Staging is not committing; commit/push still require explicit user request.
5. Update README, ARCHITECTURE, SKILL_GROUP_AUDIT, TASKS, and any candidate archive docs together.
6. Run validator and static checks. The desired steady state before review is 0 errors, 0 warnings, 0 reflection signals.
7. Run read-only Codex review. Ask it to check runtime `skills/` layout, doc consistency, validator behavior, archive safety, and task ledger truth.
8. After Codex PASS, save the review record and close every linked task and trajectory field.

## Validation Script Contract

A skill-pack validator should separate output into:

- **ERRORS**: structural defects that fail the run.
- **WARNINGS**: reconciliation issues such as visible untracked skills or intended core lists not matching tracked state yet.
- **REFLECTION SIGNALS**: non-failing prompts such as repeated CR IDs, max-turns, blocked tasks, repair loops, or open tasks missing trajectory blocks.

Exit nonzero only when ERRORS is non-empty. Do not weaken the validator to hide warnings; change repo state or docs so the warning becomes false.

## Ledger Closure Pitfalls

- Closing only the headline task after Codex PASS leaves stale governance state. Search for real-task `待复核`, `codex_result: not-launched`, `next_owner: Codex`, and `review_record: "暂无"` before reporting ready.
- Template examples may contain these strings; distinguish task templates from real task sections.
- Save Codex review records under `docs/ai-collaboration/codex-reviews/` and link them from TASKS trajectories.
- Set completed trajectories to `codex_result: PASS`, `score: 1.0`, and `next_owner: none` only after real PASS evidence.

## References

- `references/round2-reconciliation-pattern.md` — concrete pattern from the Hercules round-2 reconciliation: promote two core skills, archive non-core candidates, stage before validator, and close TASKS after Codex PASS.
