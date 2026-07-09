# Skill Navigation

This is the single-source navigation map for the Hercules skill pack. It lists every current runtime core skill exactly once with its role, maturity, primary use, and composition notes. `scripts/validate-skill-pack.py` checks that this table stays in sync with `git ls-files 'skills/*/SKILL.md'`.

For the full redundancy/overlap audit and the organic composition graph, see `docs/ai-collaboration/SKILL_GROUP_AUDIT.md`. For archived candidates and the promotion path, see `docs/ai-collaboration/candidate-skills/README.md`.

## Legend

- **Role**:
  - `entry/composite` - Hercules-specific entry wrapper that composes atoms and applies Hercules preferences.
  - `atom` - single-responsibility generic workflow skill, reusable across repositories.
  - `specialized atom` - atom scoped to a domain or a narrower technique.
- **Maturity**:
  - `core` - tracked runtime skill in the core Hercules pack.
  - `domain` - specialized domain atom (narrower scope, still runtime-tracked).

## Runtime core skills (23)

| Skill | Role | Maturity | Primary use | Composes with / Notes |
|---|---|---|---|---|
| `hercules-project-init-workflow` | entry/composite | core | Hercules entry for project/governance init | Composes `hermes-project-init-orchestration` + `hercules-skill-pack-management`; v1.0.0 |
| `hercules-collaborative-agent-workflow` | entry/composite | core | Hercules entry for day-to-day collaborative dev | Composes `hermes-collaborative-workflow` + `coding-agent-orchestration` + preflight; v1.0.0 |
| `hermes-project-init-orchestration` | atom | core | Governance-init state machine (inspect->preview->approve->apply->verify->review) | Paired with the init entry; v1.0.0 |
| `hermes-collaborative-workflow` | atom | core | Generic actor-selection base + end-to-end loop | Canonical "who does what" matrix; v1.0.0 |
| `hercules-agent-capability-preflight` | atom | core | Capability scan + reasoning-effort selection | Run before Claude/Codex delegation; v1.0.0 |
| `coding-agent-orchestration` | atom | core | Claude+Codex CLI patterns, fix->review loop, max-turns handling | v1.0.0 |
| `iterative-agent-code-review` | specialized atom | core | Iterative fix-review loop with self-review step | Deepest of the review-loop family; v2.0.0 |
| `cross-agent-review-loop` | specialized atom | core | Lighter Claude-fix->Codex-review loop | v1.0.0 |
| `hercules-meta-skill-evolution` | specialized atom | core | Trajectory records, evidence packages, evidence-backed skill patches | v1.0.0 |
| `kanban-orchestrator` | atom | core | Kanban decomposition playbook + anti-temptation rules | v3.0.0 |
| `kanban-worker` | atom | core | Kanban worker lifecycle, handoff shapes, retry diagnostics | v2.0.0 |
| `kanban-codex-lane` | specialized atom | core | Codex-as-isolated-lane for Kanban workers | v1.0.0 |
| `open-ended-research-orchestration` | specialized atom | core | Source packet -> Claude synthesis -> Codex adversarial review | v1.0.0 |
| `open-source-project-packaging` | atom | core | Reader-facing open-source README, license, attribution, and release packaging | Extracted after README/license package; v1.0.0 |
| `hercules-skill-pack-management` | atom | core | Repo layout, symlink, backup, migration, GitHub sync, privacy checks | Promoted round 2; v1.0.0 |
| `workflow-skill-pack-audit` | atom | core | Skill-pack audit/reconciliation, validator/recheck, ledger trajectory | Promoted round 2; v1.1.0 |
| `skill-pack-governance-validation` | atom | core | Runtime usability / commit-package / migration acceptance | Promoted round 3; v1.0.0 |
| `skill-pack-roadmap-execution` | atom | core | Authorized TASKS auto-advance, validation/review/commit loop, no-push boundary | Extracted after TASK-010..013; v1.0.0 |
| `staged-commit-package-governance` | atom | core | Staged-package boundary, ledger-truth, narrow Codex rechecks | Promoted TASK-009; v1.0.0 |
| `agent-plugin-dependency-governance` | atom | core | External plugin dependency-vs-vendor boundary, optional install gating, standard absorption workflow | Promoted round 4; v1.1.0 |
| `evaluation-closed-loop-orchestration` | atom | core | Canonical evaluated-system closed loop: telemetry->modification request->handoff->review | Promoted round 4; absorbs 3 archived variants; v1.0.0 |
| `godot-wsl-artifact-validation` | specialized atom | domain | WSL+Windows Godot artifact proof, headless probes, log preservation | Promoted round 4; v1.0.0 |
| `godot-rl-metric-regression` | specialized atom | domain | Baseline-vs-candidate Godot/RL metric regression, ACCEPTED/REJECTED | Promoted round 4; v1.0.0 |

## Archived candidates (not runtime-loaded)

Eight reviewed candidates are archived under `docs/ai-collaboration/candidate-skills/` and are not runtime-loaded. They are preserved as reference/case-study material and are not part of the core list above. See `docs/ai-collaboration/candidate-skills/README.md` for the full disposition table and the promotion path.
