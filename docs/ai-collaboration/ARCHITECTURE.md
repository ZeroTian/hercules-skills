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

External skills and CLIs are dependencies checked by bootstrap scripts, not source files owned here. Optional external Claude plugins are treated the same way: the OpenAI `codex-plugin-cc` Claude plugin (`codex@openai-codex`) is checked/installed only when `HERCULES_INSTALL_OPTIONAL=1` is set and is never vendored. Its `/codex:*` command surface and `codex:codex-rescue` agent are an optional in-Claude channel; the independent final Codex CLI review remains Hermes-owned. See `skills/hercules-agent-capability-preflight/SKILL.md` for the boundary classification.

## Current core skill directories

The intended core Hercules skill pack contains these skill directories:

```text
agent-plugin-dependency-governance
coding-agent-orchestration
cross-agent-review-loop
evaluation-closed-loop-orchestration
godot-rl-metric-regression
godot-wsl-artifact-validation
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
skill-pack-governance-validation
skill-pack-roadmap-execution
staged-commit-package-governance
workflow-skill-pack-audit
```

For a role/maturity navigation map of these skills, see `docs/ai-collaboration/SKILL_NAVIGATION.md`.

`hercules-skill-pack-management` is the repository-maintenance atom (layout, symlink, backup, migration, GitHub sync, pre-push privacy checks). `workflow-skill-pack-audit` is the skill-pack audit/reconciliation atom (classification, validator/recheck workflow, ledger trajectory, Codex reconciliation). `skill-pack-governance-validation` is the runtime usability / commit-package / migration acceptance atom (runtime loading, archived candidate safety, validator/static checks, bootstrap audit-only, staged privacy scan, commit-package readiness); it is the tracked round-3 core skill promoted from the practiced usability/commit-package acceptance workflow that validated commit `97f78ca`. `skill-pack-roadmap-execution` is the continuous roadmap execution atom (authorized auto-advance, Claude max-turns recovery, Codex PASS closure, auto-commit/no-push boundary) extracted from TASK-010..013 execution. `staged-commit-package-governance` is the staged-package boundary and ledger-truth atom (index-vs-worktree boundaries, preserving unrelated unstaged work, ledger/trajectory truthfulness after staging, narrow Codex rechecks); it complements `skill-pack-governance-validation` and was promoted in TASK-009 from the round-4 staged-package boundary pattern. `agent-plugin-dependency-governance` is the external plugin dependency atom (dependency-vs-vendor boundary, optional bootstrap gating, live sub-capability scanning, safety-boundary classification). `evaluation-closed-loop-orchestration` is the canonical evaluated-system closed-loop atom (telemetry→modification request→agent handoff→BLOCKED outcome→Claude/Codex review). `godot-wsl-artifact-validation` and `godot-rl-metric-regression` are specialized domain atoms for WSL+Windows Godot artifact proof and baseline-vs-candidate Godot/RL metric regression. The core set is 22 tracked skills after adding the TASK-010..013 roadmap execution atom on top of the round-4/TASK-009 core atoms.

Eight other reviewed candidates — `real-game-closed-loop-validation`, `game-mechanics-telemetry-validation`, `game-telemetry-closed-loop-validation` (domain Godot/RL/game telemetry validation), `repository-governance-initialization` (duplicate/case-study of the project-init family), `scoped-codex-review-packets` (overlap with the review-loop family), and `artifact-driven-evaluation-loops`, `artifact-handoff-orchestration`, `autonomous-evaluation-loops` (evaluated-system loop variants that overlap `evaluation-closed-loop-orchestration` after their unique details were folded into it) — were **archived** under `docs/ai-collaboration/candidate-skills/` across these reconciliation passes. They are preserved as reference/case-study material, are **not** runtime-loaded (Hermes discovers skills only from `skills/<skill>/SKILL.md`), and are **not** part of the core list. Their full disposition and promotion path are recorded in `SKILL_GROUP_AUDIT.md` and `docs/ai-collaboration/candidate-skills/README.md`.
