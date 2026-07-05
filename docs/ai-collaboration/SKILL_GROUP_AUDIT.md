# Skill Group Audit

Last inspected: 2026-07-05
Reconciliation round: 2026-07-05 (round 3)
Inspector: Claude Code (xhigh), under Hermes governance scope
Scope: classify Hercules skills, identify redundancy/overlap, define an organic composition map, and list runnable gaps. Round 1 produced audit + runnable validation infrastructure. Round 2 reconciled visible-untracked candidates: promoted two core atoms and archived four non-core candidates. Round 3 promotes `skill-pack-governance-validation` from a practiced usability/commit-package acceptance workflow that validated commit `97f78ca`. This pass does **not** rewrite skill `SKILL.md` files; it reconciles the runtime skill directory, docs, and task ledger.

## Inventory

### Core skills after round 3 (16)

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
skill-pack-governance-validation
workflow-skill-pack-audit
```

Round 2 promoted `hercules-skill-pack-management` and `workflow-skill-pack-audit` from visible-untracked candidates to core skills (now tracked). Round 3 promotes `skill-pack-governance-validation` from a practiced usability/commit-package acceptance workflow that validated commit `97f78ca` (clone-copy acceptance after push). Hermes stages the round-3 skill file for tracking before final validation so the runtime `skills/` directory and documentation list align.

### Archived candidates (5, under `docs/ai-collaboration/candidate-skills/`)

```text
real-game-closed-loop-validation
game-mechanics-telemetry-validation
game-telemetry-closed-loop-validation
repository-governance-initialization
scoped-codex-review-packets
```

These candidates were visible-untracked under `skills/` during reconciliation. They were moved out of the runtime skill directory to `docs/ai-collaboration/candidate-skills/<skill>/SKILL.md`. They are preserved as reference/case-study material, are **not** runtime-loaded (Hermes discovers skills only from `skills/<skill>/SKILL.md`), and are **not** part of the core list. See `docs/ai-collaboration/candidate-skills/README.md` for the promotion path.

### Runtime symlink note

The repository uses a flat `skills/<skill>/SKILL.md` layout. On an active-development machine the Hermes runtime points at this directory via a symlink:

```text
~/.hermes/skills/hercules -> /mnt/e/code/hercules-skills/skills
```

No symlinks live inside the repository itself (`find skills -type l` is empty), so Git does not track any symlink. The `hercules-skill-pack-management` skill documents the symlink contract and the backup/ambiguity rules. Validation of the symlink target is a runtime/machine concern, not a repo-tracked artifact.

## Classification

Legend:
- **entry** — Hercules-specific entry wrapper that composes atoms and applies Hercules preferences.
- **atom** — single-responsibility generic workflow skill, reusable across repositories.
- **specialized atom** — atom scoped to a domain or a narrower technique.
- **archived** — reviewed candidate moved out of the runtime skill directory; preserved as reference/case-study, not runtime-loaded.

| Skill | Type | Role |
|---|---|---|
| hercules-project-init-workflow | entry | Hercules entry for project/governance init; composes atoms + Hercules preferences. |
| hercules-collaborative-agent-workflow | entry | Hercules entry for day-to-day collaborative dev; composes atoms + Hercules preferences. |
| hermes-project-init-orchestration | atom | Detailed governance-init state machine (inspect→preview→approve→apply→verify→review). |
| hermes-collaborative-workflow | atom | Generic actor-selection base + end-to-end loop; the canonical "who does what" matrix. |
| hercules-agent-capability-preflight | atom | Capability scan + reasoning-effort selection before Claude/Codex delegation. |
| coding-agent-orchestration | atom | Claude+Codex CLI patterns, fix→review loop, max-turns handling, governance-task-closure reference. |
| iterative-agent-code-review | specialized atom | Iterative fix-review loop with self-review step; v2.0.0, deepest of the review-loop family. |
| cross-agent-review-loop | specialized atom | Iterative Claude-fix→Codex-review loop; v1.0.0, lighter variant of the same loop. |
| hercules-meta-skill-evolution | specialized atom | Trajectory records, evidence packages, evidence-backed skill patches (Skill-MAS inspired). |
| kanban-orchestrator | atom | Kanban decomposition playbook + anti-temptation rules for the orchestrator profile. |
| kanban-worker | atom | Kanban worker lifecycle, handoff shapes, retry diagnostics. |
| kanban-codex-lane | specialized atom | Codex-as-isolated-lane for Kanban workers; worktree/branch + reconciliation contract. |
| open-ended-research-orchestration | specialized atom | Source packet → Claude synthesis → Codex adversarial review → durable output. |
| hercules-skill-pack-management | atom (core) | Repo layout, symlink, backup, migration, GitHub sync, privacy pre-push checks. |
| workflow-skill-pack-audit | atom (core) | Skill-pack audit/reconciliation: classification, validator/recheck workflow, ledger trajectory, Codex reconciliation. |
| skill-pack-governance-validation | atom (core) | Runtime usability / commit-package / migration acceptance: runtime loading, archived candidate safety, validator/static checks, bootstrap audit-only, staged privacy scan, commit-package readiness. |
| real-game-closed-loop-validation | archived (domain) | Godot/RL/evaluation real-run validation; domain-specific, not core orchestration. |
| game-mechanics-telemetry-validation | archived (domain) | Game/RL mechanic telemetry validation; pairs with real-game validation rather than core orchestration. |
| game-telemetry-closed-loop-validation | archived (domain) | Game/RL semantic telemetry and closed-loop validation; useful domain material, but not core workflow orchestration. |
| repository-governance-initialization | archived (duplicate/case-study) | Governance init pattern; overlaps the two existing project-init skills. |
| scoped-codex-review-packets | archived (overlap/reference) | Tight Codex packet pattern; overlaps the review-loop family. |

## Redundancy and overlap

### hercules-collaborative-agent-workflow vs hermes-collaborative-workflow

- **Relationship**: entry wrapper + generic base. The Hercules entry skill duplicates actor policy, brief requirements, end-to-end loop, pitfalls, and verification checklist that already live in the base skill.
- **Decision (this pass)**: keep both. The entry skill is the Hercules-flavored front door (preferences, migration, companion-skill list); the base skill is the portable actor-selection contract.
- **Future drift reduction**: make the entry skill **point to** `hermes-collaborative-workflow` for the actor-selection matrix and brief requirements instead of re-stating them. Replace duplicated prose with `See hermes-collaborative-workflow#Actor Selection Matrix` style links. Do not rewrite in this audit pass.

### hercules-project-init-workflow vs hermes-project-init-orchestration vs repository-governance-initialization

- **Relationship**: entry wrapper + detailed orchestration atom + duplicate candidate. `repository-governance-initialization` restates the same inspect→preview→approve→apply→verify→review loop already covered by `hermes-project-init-orchestration` (state machine, artifact map, scope partition) and the Hercules entry wrapper.
- **Decision (round 2)**: keep the wrapper + atom pair. `repository-governance-initialization` is **archived** under `docs/ai-collaboration/candidate-skills/`. Its reusable content (preview-outside-repo, pre-existing-untracked-work preservation) should be folded into `hermes-project-init-orchestration/references/` as a case study before any future promotion.
- **Future action**: open a follow-up task to merge the unique steps into `hermes-project-init-orchestration/references/` and delete the archived copy only after the case study lands.

### coding-agent-orchestration, cross-agent-review-loop, iterative-agent-code-review

- **Relationship**: overlapping review-loop family. `iterative-agent-code-review` (v2.0.0, self-review step, 19-round case study) is the deepest; `cross-agent-review-loop` (v1.0.0) is a lighter restatement of the same loop; `coding-agent-orchestration` is broader (CLI patterns, max-turns handling, governance closure) and references the loop as one of its workflows.
- **Recommended layering** (future consolidation map, not this pass):
  - `coding-agent-orchestration` = broad CLI/flag patterns + max-turns recovery + governance-task-closure reference.
  - `iterative-agent-code-review` = canonical multi-round fix-review loop pattern (self-review, stop conditions, round budget).
  - `cross-agent-review-loop` = either consolidate into `iterative-agent-code-review` as a section, or keep as a lighter quick-start variant that points to the deeper skill for >3-round cases.
- **Decision (this pass)**: no rewrite. Record the layering intent here so a future skill-patch round can execute it with evidence.

### hercules-skill-pack-management

- **Relationship**: round 1 untracked candidate. Covers repository layout, symlink, backup ambiguity, migration, GitHub sync, and pre-push privacy checks. No existing tracked skill covers this; `README.md` documents install/symlink but not the management workflow.
- **Decision (round 2)**: **promoted to core atom**. Added to README and ARCHITECTURE core lists and staged by Hermes for tracking before final validation.

### workflow-skill-pack-audit

- **Relationship**: appeared after round 1. It codifies this exact audit/reconciliation workflow: skill classification, validator contract (ERRORS/WARNINGS/REFLECTION SIGNALS), reflection-scanner pitfalls, and the Codex recheck pattern for stale ledger evidence. No existing tracked skill covers the audit/reconciliation pass; `hercules-meta-skill-evolution` governs evidence-backed skill evolution, while this skill governs the concrete audit/validation pass for the repository.
- **Decision (round 2)**: **promoted to core atom**. Added to README and ARCHITECTURE core lists and staged by Hermes for tracking before final validation.

### skill-pack-governance-validation

- **Relationship**: visible-untracked after round 2. It codifies the acceptance pass that follows an audit or skill-pack change: runtime layout smoke test, `skill_view` loading, archived-candidate non-loading, validator/static checks, bootstrap audit-only, staged privacy scan, and commit-package readiness. It complements `workflow-skill-pack-audit` (which governs classification/reconciliation) and `hercules-skill-pack-management` (which governs layout/sync): those govern what the pack looks like; this governs evidence that the pack is usable and safe to package. The practice was exercised end-to-end against commit `97f78ca` (clone-copy validation after push).
- **Decision (round 3)**: **promoted to core atom**. Added to README and ARCHITECTURE core lists. Hermes stages the skill file for tracking before final validation. Distinct from `workflow-skill-pack-audit`: audit/reconciliation stays with the audit atom; runtime usability / commit-package / migration acceptance stays with this skill.

### real-game / game-telemetry validation candidates

- **Relationship**: domain-specific (Godot/RL/evaluation) real-run, semantic telemetry, and mechanic validation. Not core orchestration; they are class-level domain validation skills.
- **Decision (round 2/3)**: **archived** under `docs/ai-collaboration/candidate-skills/`. They are preserved as reference material and are not runtime-loaded. `hercules-collaborative-agent-workflow` already references its Godot validation checklist via `references/real-godot-closed-loop-validation.md`, so the linkage exists without tracking these skills as core. If the user later wants Hercules to include domain-specific validation skills, follow the promotion path in `docs/ai-collaboration/candidate-skills/README.md` and fix any broken `references/*.md` links first.

### scoped-codex-review-packets

- **Relationship**: round 1 untracked candidate. It is a specialized review-loop pattern that builds small Codex review packets and requires a final verdict when broad Codex reviews over-read or omit PASS/FAIL.
- **Decision (round 2)**: **archived** under `docs/ai-collaboration/candidate-skills/`. It is useful but overlaps `coding-agent-orchestration` and `iterative-agent-code-review`. Before any future promotion, merge its packet contract into one of those skills or confirm it fills a genuine gap the review-loop family does not cover.

## Organic composition map

The skills should compose end-to-end as follows (arrow = "hands off to"):

```text
project init
  hercules-project-init-workflow (entry)
    -> hermes-project-init-orchestration (atom: state machine, artifact map)
    -> hercules-skill-pack-management (atom: repo layout, symlink, sync)
        |
        v
capability preflight
  hercules-agent-capability-preflight (scan + effort selection)
        |
        v
collaborative execution
  hercules-collaborative-agent-workflow (entry)
    -> hermes-collaborative-workflow (actor-selection base)
    -> coding-agent-orchestration (CLI patterns, max-turns recovery)
        |
        v
review loop
  iterative-agent-code-review (canonical multi-round loop)
  cross-agent-review-loop (lighter variant)
  kanban-codex-lane (when Codex runs as an isolated Kanban lane)
        |
        v
ledger trajectory
  TASKS.md trajectory blocks (templates/trajectory-record.md)
        |
        v
meta-skill evidence package
  hercules-meta-skill-evolution (templates/evidence-package.md)
        |
        v
skill patch
  hercules-meta-skill-evolution Skill Patch Protocol
        |
        v
validation + audit
  scripts/validate-skill-pack.py (frontmatter, links, lists, governance, shell, reflection signals)
  workflow-skill-pack-audit (audit/reconciliation pass, Codex recheck)
  skill-pack-governance-validation (runtime usability / commit-package / migration acceptance)
```

Side branches:
- `open-ended-research-orchestration` feeds research/source packets into the execution branch when broad exploration is needed before implementation.
- `kanban-orchestrator` + `kanban-worker` are the Kanban-profile parallel path; they compose with `kanban-codex-lane` when a Kanban worker needs an isolated Codex implementation lane.
- Archived candidates (`real-game-closed-loop-validation`, `game-mechanics-telemetry-validation`, `game-telemetry-closed-loop-validation`, `repository-governance-initialization`, `scoped-codex-review-packets`) are **not** runtime side-branches in this pass. They live under `docs/ai-collaboration/candidate-skills/` and attach only if a future promotion brings them back into `skills/`.

## Runnable gaps

1. **No validation script existed.** Fixed in round 1: `scripts/validate-skill-pack.py` (Python stdlib only).
2. **Visible untracked skills were unresolved.** Resolved in round 2: `hercules-skill-pack-management` and `workflow-skill-pack-audit` promoted to intended core (pending Hermes commit); `real-game-closed-loop-validation`, `game-mechanics-telemetry-validation`, `repository-governance-initialization`, and `scoped-codex-review-packets` archived under `docs/ai-collaboration/candidate-skills/`.
3. **TASKS.md has no trajectory blocks.** Fixed in round 1: trajectory record policy + minimal trajectory blocks added to TASKS.md.
4. **No reflection signal scanning.** Fixed in round 1: the validation script scans TASKS.md and codex-reviews/*.md for repeated CR IDs, max-turns, blocked, repair-loop, missing trajectory blocks, and evidence-package recommendations.
5. **Review-loop family overlap.** Not fixed in this pass (no skill rewrites); layering map recorded above for a future evidence-backed patch round.
6. **`repository-governance-initialization` duplicate.** Resolved in round 2 by archiving; unique content still pending merge into `hermes-project-init-orchestration/references/` as a case study.

## Prioritized next actions

| Priority | Action | Owner | Notes |
|---:|---|---|---|
| P1 | Commit the round-2 reconciliation when the user requests it: two promoted core skills + four archived candidates + doc updates. | Hermes | Commit/push remains out of scope until explicitly requested. Round-2 work is already committed at `97f78ca`. |
| P1 | Commit the round-3 promotion when the user requests it: `skill-pack-governance-validation` promoted to core + doc updates. | Hermes | Commit/push remains out of scope until explicitly requested. |
| P1 | Run `python3 scripts/validate-skill-pack.py` before every skill-pack change. | Hermes / Claude | Added to HERMES.md validation commands. |
| P2 | Merge `repository-governance-initialization` unique steps into `hermes-project-init-orchestration/references/` as a case study; then delete the archived copy. | Claude (after Codex review) | Open as a follow-up task. |
| P2 | If promoting a domain validation candidate later, fix broken `references/godot-rl-stage2-optimizer.md` link first. | Claude | Follow `docs/ai-collaboration/candidate-skills/README.md`. |
| P3 | Execute the review-loop family consolidation map with evidence (trajectory records + evidence package) before rewriting. | Claude (under hercules-meta-skill-evolution) | Do not rewrite without evidence. |
| P3 | Reduce drift between `hercules-collaborative-agent-workflow` and `hermes-collaborative-workflow` by replacing duplicated prose with links to the base skill. | Claude | Future skill-patch round. |

## Practical usability validation

Round 2 was practiced in the live repository rather than only documented. Round 3 extends the evidence with a clone-copy validation performed after pushing commit `97f78ca`, now codified by the `skill-pack-governance-validation` core skill. See `docs/ai-collaboration/USABILITY_VALIDATION.md` for evidence covering runtime symlink, 16-core-skill inventory, archived candidate non-loading, validator/static checks, bootstrap audit-only mode, clone-copy acceptance for `97f78ca`, and the actual Hermes → Claude → Hermes verify → Codex → TASKS closure loop.

## Verification

Commands run for this audit round:

```bash
git ls-files skills/
git status --short -uall
find skills -name SKILL.md -maxdepth 2 | sort
find skills -type l
python3 scripts/validate-skill-pack.py
git diff --check
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

The validation script reports 0 errors. After Hermes stages the round-3 promoted core skill file (`skill-pack-governance-validation`) for tracking and archives the unrelated game telemetry candidate outside `skills/`, the runtime `skills/` directory matches the intended 16-skill core and archived candidates live outside `skills/`. Reflection signals are non-failing and should point to concrete task IDs or review files rather than template prose.
