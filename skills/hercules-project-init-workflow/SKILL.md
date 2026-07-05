---
name: hercules-project-init-workflow
description: "Use when initializing or reinitializing a repository under Hercules preferences: Hermes-governed project rules, README scope separation, Claude SDD/TDD execution, Codex review, and portable governance docs."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, project-init, governance, claude-code, codex, sdd, tdd]
    related_skills: [hermes-project-init-orchestration, hermes-collaborative-workflow, hercules-agent-capability-preflight, test-driven-development, writing-plans]
---

# Hercules Project Init Workflow

## Overview

Use this as the Hercules-specific entry skill for project initialization or governance reinitialization. It does not replace the lower-level skills. It composes them and adds Hercules preferences so the portable policy lives under `~/.hermes/skills/hercules/` instead of modifying bundled or hub skills.

Core idea:

```text
Hercules entry skill
  -> load project-init/governance atom skills
  -> apply Hercules preferences
  -> Hermes orchestrates Claude and Codex
  -> task ledger records real evidence
```

## When to Use

Use when the user asks to:

- initialize a project for Hermes / Claude Code / Codex collaboration;
- reinitialize or standardize governance files in an existing repository;
- create or repair `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, `TASKS.md`, or `docs/ai-collaboration/`;
- separate README reader-facing docs from long-lived agent operation rules;
- build a portable project governance baseline that can be reused on other repos.

Do not use for a normal one-off implementation task. Use `hercules-collaborative-agent-workflow` for day-to-day task execution.

## Required Companion Skills

Load these when relevant:

1. `hermes-project-init-orchestration` — primary governance init workflow and state machine.
2. `hermes-collaborative-workflow` — Hermes as controller rather than manual Claude/Codex switching.
3. `hercules-agent-capability-preflight` — scan Claude/Codex capabilities and choose `high`/`xhigh` effort.
4. `claude-code` — implementation worker reference.
5. `codex` — review worker reference.
6. `test-driven-development` — RED/GREEN/REFACTOR discipline.
7. `writing-plans` or `plan` — actionable implementation plans when a plan artifact is needed.

These are dependencies, not content to copy into project repositories. Local custom workflow skills may live in the portable `hercules/` skill group; bundled Hermes skills should remain in their official categories on each host.

## Hercules Governance Preferences

Apply these preferences on top of the companion skills:

1. **Hermes is the controller.** Hermes reads state, launches Claude/Codex, monitors processes, verifies output, and updates records.
2. **README stays reader-facing.** README files are overview, install/use, and navigation docs. They should link to agent rules, not duplicate SDD/TDD or trigger protocols.
3. **Rules are actor-scoped.** Use `HERMES.md` for repository-specific Hermes orchestration, `CLAUDE.md` for Claude execution rules, `AGENTS.md` for Codex review rules, and `TASKS.md` for live repo state.
4. **User-level Hercules policy belongs in user config, not project docs.** Personal workflow preferences such as “Hercules skills live in `~/.hermes/skills/hercules/` and sync to `ZeroTian/hercules-skills`” belong in the user's global Hermes/SOUL configuration and in the portable skill pack, not in every repository `HERMES.md`.
5. **Formal development uses SDD + TDD.** Claude plans vertical slices, records RED/GREEN/REFACTOR evidence, and uses OMC/superpowers when available.
6. **Codex closes review-required work.** Main tasks requiring review become `[x]` only after Codex PASS and Hermes verification.
7. **Capability preflight is mandatory before delegation.** Use `hercules-agent-capability-preflight` before meaningful Claude/Codex launches.
8. **Effort defaults to high.** Use `xhigh` for cross-subsystem, high-risk, safety/gate, real external execution, or failed-review work.
9. **No commit/push/reset unless requested.** Governance init may patch files and run verification, but does not change Git history without explicit user request.

## Recommended Artifact Layout

```text
.
├── HERMES.md
├── CLAUDE.md
├── AGENTS.md
└── docs/
    └── ai-collaboration/
        ├── README.md
        ├── TASKS.md
        ├── ARCHITECTURE.md
        ├── PROJECT_AUDIT.md
        ├── codex-reviews/
        └── decisions/
```

Reuse existing equivalent files when present. Do not create duplicate rulebooks.

## Execution Procedure

1. **Inspect without mutation.** Read current governance files, manifests, CI, test commands, and `git status`. Completion: current governance state and proposed mapping are known.
2. **Prepare preview.** Show exact files to create/modify and the reason for each. Completion: user can approve or reject without hidden changes.
3. **Wait for explicit approval.** Do not apply broad governance changes on vague agreement.
4. **Apply narrowly.** Patch only approved files. Completion: every changed file is in scope.
5. **Verify.** Run link/diff/status checks and any lightweight syntax checks. Completion: verification output exists or blocker is recorded.
6. **If implementation is needed, switch to collaborative workflow.** Use `hercules-collaborative-agent-workflow` rather than embedding an implementation loop here.

## Migration Pattern

To move Hercules project-init and development workflow policy to another machine, use the portable Hercules skill group:

```text
https://github.com/ZeroTian/hercules-skills
```

Copy or clone that repository's `skills/` directory into:

```text
~/.hermes/skills/hercules/
```

Then start a fresh Hermes session and load skills by name. Do not ask the agent to reconstruct missing workflow rules from memory; the target host must have the actual `SKILL.md` files.

Use the target machine's own bundled Hermes skills directly instead of copying them into `hercules/`:

```text
claude-code
codex
hermes-agent
opencode
test-driven-development
plan
```

If a local custom development-workflow skill is authored later, place it under `~/.hermes/skills/hercules/` before syncing the GitHub skill group.

## Common Pitfalls

1. **Moving bundled skills into `hercules/`.** Do not move or fork bundled skills such as `claude-code`, `codex`, or `hermes-agent`; use the target host's bundled versions. Local custom workflow skills can live in the portable `hercules/` pack.
2. **Duplicating rule content in README.** Keep long operational rules in actor-scoped files.
3. **Skipping preview.** Governance rewrites need an explicit approved scope.
4. **Treating generated plans as completion.** Completion requires files patched and verification run.
5. **Forgetting capability preflight.** Scan live Claude/Codex capabilities before asking them to use plugins/MCP.

## Verification Checklist

- [ ] Companion skills loaded as needed
- [ ] Current repo governance inspected before mutation
- [ ] Proposed artifact mapping is explicit
- [ ] User approved broad governance changes before applying
- [ ] README remains reader-facing
- [ ] HERMES/CLAUDE/AGENTS/TASKS responsibilities are separated
- [ ] SDD/TDD and Codex closure rules are present where needed
- [ ] Capability preflight and effort choice are recorded for formal delegation
- [ ] Verification output is real and reported
