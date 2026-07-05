# Architecture

## Repository purpose

`hercules-skills` stores Hercules-owned Hermes workflow skills as a portable skill pack.

## Top-level layout

```text
.
├── README.md
├── HERMES.md
├── CLAUDE.md
├── AGENTS.md
├── docs/ai-collaboration/
└── skills/
```

## Directory responsibilities

- `skills/<skill>/SKILL.md`: primary skill instructions and metadata.
- `skills/<skill>/references/`: supporting long-form references and case studies.
- `skills/<skill>/templates/`: reusable prompts, records, or document templates.
- `skills/<skill>/scripts/`: executable helper scripts used by that skill.
- `docs/ai-collaboration/`: repository collaboration ledger, audit snapshot, review records, and decisions.

## Dependency boundaries

This repository should contain only Hercules-owned custom workflow skills.

It should not copy these builtin skills:

```text
claude-code
codex
hermes-agent
opencode
```

It should not vendor external hub skills such as:

```text
subagent-driven-development
writing-plans
```

External skills and CLIs are dependencies checked by bootstrap scripts, not source files owned here.

## Current core skill directories

The intended core Hercules skill pack contains these skill directories:

```text
coding-agent-orchestration
cross-agent-review-loop
hercules-agent-capability-preflight
hercules-collaborative-agent-workflow
hercules-meta-skill-evolution
hercules-project-init-workflow
hercules-skill-pack-management
hermes-collaborative-workflow
hermes-project-init-orchestration
iterative-agent-code-review
kanban-codex-lane
kanban-orchestrator
kanban-worker
open-ended-research-orchestration
workflow-skill-pack-audit
```

`hercules-skill-pack-management` is the repository-maintenance atom (layout, symlink, backup, migration, GitHub sync, pre-push privacy checks). `workflow-skill-pack-audit` is the skill-pack audit/reconciliation atom (classification, validator/recheck workflow, ledger trajectory, Codex reconciliation). Both are core skills after the round-2 reconciliation and are staged for tracking before final validation.

Four other reviewed candidates — `real-game-closed-loop-validation`, `game-mechanics-telemetry-validation` (domain Godot/RL validation), `repository-governance-initialization` (duplicate/case-study of the project-init family), and `scoped-codex-review-packets` (overlap with the review-loop family) — were **archived** under `docs/ai-collaboration/candidate-skills/` in this pass. They are preserved as reference/case-study material, are **not** runtime-loaded (Hermes discovers skills only from `skills/<skill>/SKILL.md`), and are **not** part of the core list. Their full disposition and promotion path are recorded in `SKILL_GROUP_AUDIT.md` and `docs/ai-collaboration/candidate-skills/README.md`.
