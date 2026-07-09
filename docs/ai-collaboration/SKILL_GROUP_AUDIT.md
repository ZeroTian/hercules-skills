# Skill Group Audit

Last inspected: 2026-07-08
Reconciliation round: 2026-07-08 (round 4)
Inspector: Claude Code (xhigh), under Hermes governance scope
Scope: classify Hercules skills, identify redundancy/overlap, define an organic composition map, and list runnable gaps. Round 1 produced audit + runnable validation infrastructure. Round 2 reconciled visible-untracked candidates: promoted two core atoms and archived four non-core candidates. Round 3 promotes `skill-pack-governance-validation` from a practiced usability/commit-package acceptance workflow that validated commit `97f78ca`. Round 4 reconciles seven further visible-untracked candidates: promotes four core/specialized atoms (`agent-plugin-dependency-governance`, `evaluation-closed-loop-orchestration`, `godot-wsl-artifact-validation`, `godot-rl-metric-regression`) and archives three evaluated-system loop variants after folding their unique details into `evaluation-closed-loop-orchestration`. Round 4 folds reusable detail into one promoted skill and reconciles the runtime skill directory, docs, and task ledger. TASK-009 (follow-up to round 4) promotes one additional atom, `staged-commit-package-governance`, captured from the round-4 staged-package boundary and ledger-truth pattern, and keeps a durable Godot validation reference improvement in the same package. Post TASK-013 cleanup promotes `skill-pack-roadmap-execution` from the successful TASK-010..013 auto-advance/auto-commit pattern. The README/license packaging pass promotes `open-source-project-packaging` from the bilingual open-source README and license-boundary workflow.

## Inventory

### Core skills after round 4 + TASK-009 + post TASK-013 cleanup + README/license packaging (23)

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
open-source-project-packaging
skill-pack-governance-validation
skill-pack-roadmap-execution
staged-commit-package-governance
workflow-skill-pack-audit
```

Round 2 promoted `hercules-skill-pack-management` and `workflow-skill-pack-audit` from visible-untracked candidates to core skills (now tracked). Round 3 promotes `skill-pack-governance-validation` from a practiced usability/commit-package acceptance workflow that validated commit `97f78ca` (clone-copy acceptance after push). Round 4 promotes `agent-plugin-dependency-governance`, `evaluation-closed-loop-orchestration`, `godot-wsl-artifact-validation`, and `godot-rl-metric-regression` from visible-untracked candidates to core/specialized atoms. Hermes stages the promoted skill files for tracking before final validation so the runtime `skills/` directory and documentation list align. TASK-009 promotes `staged-commit-package-governance` from the round-4 staged-package boundary and ledger-truth pattern; it complements `skill-pack-governance-validation`. Post TASK-013 cleanup promotes `skill-pack-roadmap-execution` from the authorized auto-advance/auto-commit pattern; it complements the audit/validation/staging atoms by governing continuous roadmap execution. The README/license packaging pass promotes `open-source-project-packaging`; it complements `agent-plugin-dependency-governance` by turning dependency-vs-vendor/license decisions into reader-facing README, LICENSE, attribution, validation, and Codex review outputs.

### Archived candidates (8, under `docs/ai-collaboration/candidate-skills/`)

```text
artifact-driven-evaluation-loops
artifact-handoff-orchestration
autonomous-evaluation-loops
game-mechanics-telemetry-validation
game-telemetry-closed-loop-validation
real-game-closed-loop-validation
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

For a compact role/maturity navigation table of all runtime skills, see `docs/ai-collaboration/SKILL_NAVIGATION.md` (validated against `git ls-files 'skills/*/SKILL.md'`). The table below is the detailed audit classification including archived candidates.

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
| open-source-project-packaging | atom (core) | Reader-facing open-source README, license choice, third-party attribution, dependency-vs-vendor boundaries, validation, and Codex review. |
| hercules-skill-pack-management | atom (core) | Repo layout, symlink, backup, migration, GitHub sync, privacy pre-push checks. |
| workflow-skill-pack-audit | atom (core) | Skill-pack audit/reconciliation: classification, validator/recheck workflow, ledger trajectory, Codex reconciliation. |
| skill-pack-governance-validation | atom (core) | Runtime usability / commit-package / migration acceptance: runtime loading, archived candidate safety, validator/static checks, bootstrap audit-only, staged privacy scan, commit-package readiness. |
| skill-pack-roadmap-execution | atom (core) | Continuous roadmap execution after user authorization: TASKS auto-advance, Claude max-turns recovery, validation/review/commit loop, auto-commit/no-push boundary. |
| staged-commit-package-governance | atom (core) | Staged-package boundary and ledger-truth: index-vs-worktree boundaries, preserving unrelated unstaged work, ledger/trajectory truthfulness after staging, narrow Codex rechecks. Complements `skill-pack-governance-validation`. |
| agent-plugin-dependency-governance | atom (core) | External Claude/Codex/agent plugin dependency governance: dependency-vs-vendor boundary, optional bootstrap gating, live sub-capability scanning, safety-boundary classification, independent review authority. |
| evaluation-closed-loop-orchestration | atom (core) | Canonical evaluated-system closed loop: telemetry→diagnosis→safe attempt→gate→modification request→agent handoff→BLOCKED outcome→Claude/Codex review. Absorbs the unique detail of three archived loop variants. |
| godot-wsl-artifact-validation | specialized atom (domain) | WSL + Windows Godot artifact proof: artifact projects, headless probes, import/smoke evidence, baseline-vs-candidate log preservation, SceneTree/`res://` pitfalls. |
| godot-rl-metric-regression | specialized atom (domain) | Baseline-vs-candidate Godot/RL metric regression: real inference, telemetry provenance, `objective.score()`, artifact-backed ACCEPTED/REJECTED, false-improvement guards. |
| real-game-closed-loop-validation | archived (domain) | Godot/RL/evaluation real-run validation; domain-specific, not core orchestration. |
| game-mechanics-telemetry-validation | archived (domain) | Game/RL mechanic telemetry validation; pairs with real-game validation rather than core orchestration. |
| game-telemetry-closed-loop-validation | archived (domain) | Game/RL semantic telemetry and closed-loop validation; useful domain material, but not core workflow orchestration. |
| repository-governance-initialization | archived (duplicate/case-study) | Governance init pattern; overlaps the two existing project-init skills. |
| scoped-codex-review-packets | archived (overlap/reference) | Tight Codex packet pattern; overlaps the review-loop family. |
| artifact-driven-evaluation-loops | archived (overlap/reference) | Evaluated-system loop variant; overlaps `evaluation-closed-loop-orchestration`. Unique BLOCKED outcome + field-preservation contract folded into the canonical atom before archiving. |
| artifact-handoff-orchestration | archived (overlap/reference) | Handoff/BLOCKED orchestration variant; overlaps `evaluation-closed-loop-orchestration`. Unique safe-anchor validator checklist folded into the canonical atom before archiving. |
| autonomous-evaluation-loops | archived (overlap/reference) | Autonomous evaluation loop variant; overlaps `evaluation-closed-loop-orchestration`. Unique modification-request schema + instance-vs-system distinction folded into the canonical atom before archiving. |

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

### skill-pack-roadmap-execution

- **Relationship**: post-roadmap execution atom extracted from TASK-010..013. It complements `workflow-skill-pack-audit`, `skill-pack-governance-validation`, and `staged-commit-package-governance`: those govern audit, acceptance, and staged-package truth; this skill governs the continuous auto-advance loop once the user authorizes Hermes to proceed through multiple ledger tasks and commit after Codex PASS while keeping push separate.
- **Decision (post TASK-013)**: **promoted to core atom**. The session produced repeated max-turns/reflection signals plus a successful auto-advance/auto-commit pattern, so the reusable behavior is tracked as a first-class Hercules skill with a linked reference note. Added to README, ARCHITECTURE, and SKILL_NAVIGATION core lists.

### open-source-project-packaging

- **Relationship**: post README/license packaging atom extracted from the bilingual open-source README and MIT license package. It complements `agent-plugin-dependency-governance` by turning dependency-vs-vendor/license decisions into reader-facing README, LICENSE, attribution, validation, and Codex review outputs.
- **Decision (post README/license package)**: **promoted to core atom**. The workflow is reusable for future Hercules or agent-workflow repositories that need public README/license packaging without overclaiming third-party relationships. Added to README, ARCHITECTURE, and SKILL_NAVIGATION core lists.

### staged-commit-package-governance

- **Relationship**: TASK-009 visible-untracked candidate, captured from the round-4 staged-package boundary and ledger-truth pattern. It overlaps `skill-pack-governance-validation` in the commit-package space but narrows in on a distinct concern: keeping the staged index, TASKS/CR ledger, trajectory record, and review record aligned during the staging/review cycle, especially when unrelated unstaged work must be preserved and Codex finds ledger drift after staging.
- **Decision (TASK-009)**: **promoted to core atom**. Distinct from `skill-pack-governance-validation`: that skill governs the broad acceptance pass (runtime loading, validator, bootstrap, privacy scan, commit-package readiness); this atom governs the staged-package boundary and ledger-truth cycle during the actual staging/review cycle, including narrow Codex rechecks of ledger drift. Added to README and ARCHITECTURE core lists.

### agent-plugin-dependency-governance

- **Relationship**: round-4 visible-untracked candidate. It codifies the dependency-vs-vendor boundary for external Claude/Codex/agent plugins: research upstream identity, decide dependency vs vendor, gate optional installs, scan live sub-capabilities, classify read-only vs state-changing surfaces, preserve Hermes independent review authority. TASK-007 practiced this with `openai/codex-plugin-cc`; this skill generalizes the policy.
- **Decision (round 4)**: **promoted to core atom**. Distinct from `hercules-agent-capability-preflight` (which scans live Claude/Codex capabilities and chooses reasoning effort): preflight answers "what can the agents do now"; this skill answers "should a new plugin be vendored, depended on, or rejected, and how is it bootstrapped and bounded". Added to README and ARCHITECTURE core lists.

### evaluation-closed-loop-orchestration (and archived loop variants)

- **Relationship**: round-4 visible-untracked candidate, plus three overlapping siblings (`artifact-driven-evaluation-loops`, `artifact-handoff-orchestration`, `autonomous-evaluation-loops`). All four describe the same evaluated-system loop: real run → diagnosis → safe attempt → gate → modification request → agent handoff → review. The three siblings each add some unique detail (BLOCKED outcome, field-preservation contract, safe-anchor validator checklist, modification-request schema, instance-vs-system distinction) but restate the same core loop.
- **Decision (round 4)**: **promote `evaluation-closed-loop-orchestration` as the canonical broad atom** and **archive the three siblings** under `docs/ai-collaboration/candidate-skills/`. Before archiving, the genuinely unique details were folded into the canonical atom: structured `BLOCKED_SCOPE_INSUFFICIENT` outcome, preservation of `allowed_surfaces` / `forbidden_surfaces` / `evidence` / `gate_result` / `attempted_plan` / `blocked_reason` across handoffs, safe-anchor validator checklist (positive allowlist + concept denylist, whole-block matching), and owner/next_owner as executable routing signals. The canonical atom now carries a `references/issue-to-handoff-closed-loop.md` session note; the archived siblings keep their original prose as case-study material.

### godot-wsl-artifact-validation + godot-rl-metric-regression

- **Relationship**: round-4 visible-untracked domain candidates. `godot-wsl-artifact-validation` covers WSL+Windows Godot artifact proof (artifact projects, headless probes, import/smoke evidence, log preservation, `res://`/SceneTree pitfalls). `godot-rl-metric-regression` covers baseline-vs-candidate Godot/RL metric regression (real inference, telemetry provenance, `objective.score()`, ACCEPTED/REJECTED, false-improvement guards). They are narrower than `evaluation-closed-loop-orchestration` but fill a genuine domain gap: the broad atom governs the loop shape; these two govern concrete Godot/RL evidence quality. `hercules-collaborative-agent-workflow` already references its Godot checklist via `references/real-godot-closed-loop-validation.md`, and these two skills formalize that domain know-how as trackable atoms.
- **Decision (round 4)**: **promoted to specialized domain atoms**. Each carries a concise `references/` session note. Distinct from the archived `real-game-closed-loop-validation` (which is a broader real-run validation case study, not a trackable atom).

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
  agent-plugin-dependency-governance (plugin dependency-vs-vendor boundary, optional install gating)
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
  staged-commit-package-governance (staged-package boundary, ledger truth, narrow Codex recheck)
  skill-pack-roadmap-execution (authorized auto-advance, Codex PASS closure, auto-commit/no-push boundary)
```

Side branches:
- `open-ended-research-orchestration` feeds research/source packets into the execution branch when broad exploration is needed before implementation.
- `kanban-orchestrator` + `kanban-worker` are the Kanban-profile parallel path; they compose with `kanban-codex-lane` when a Kanban worker needs an isolated Codex implementation lane.
- `evaluation-closed-loop-orchestration` is the evaluated-system loop side branch: telemetry/diagnosis → safe modification request → agent handoff → BLOCKED outcome → Claude/Codex review. `godot-wsl-artifact-validation` and `godot-rl-metric-regression` are its Godot/RL domain evidence atoms.
- Archived candidates (`artifact-driven-evaluation-loops`, `artifact-handoff-orchestration`, `autonomous-evaluation-loops`, `real-game-closed-loop-validation`, `game-mechanics-telemetry-validation`, `game-telemetry-closed-loop-validation`, `repository-governance-initialization`, `scoped-codex-review-packets`) are **not** runtime side-branches. They live under `docs/ai-collaboration/candidate-skills/` and attach only if a future promotion brings them back into `skills/`.

## Runnable gaps

1. **No validation script existed.** Fixed in round 1: `scripts/validate-skill-pack.py` (Python stdlib only).
2. **Visible untracked skills were unresolved.** Resolved in round 2: `hercules-skill-pack-management` and `workflow-skill-pack-audit` promoted to intended core (pending Hermes commit); `real-game-closed-loop-validation`, `game-mechanics-telemetry-validation`, `repository-governance-initialization`, and `scoped-codex-review-packets` archived under `docs/ai-collaboration/candidate-skills/`.
3. **TASKS.md has no trajectory blocks.** Fixed in round 1: trajectory record policy + minimal trajectory blocks added to TASKS.md.
4. **No reflection signal scanning.** Fixed in round 1: the validation script scans TASKS.md and codex-reviews/*.md for repeated CR IDs, max-turns, blocked, repair-loop, missing trajectory blocks, and evidence-package recommendations.
5. **Review-loop family overlap.** Not fixed in this pass (no skill rewrites); layering map recorded above for a future evidence-backed patch round.
6. **`repository-governance-initialization` duplicate.** Resolved in round 2 by archiving; unique content still pending merge into `hermes-project-init-orchestration/references/` as a case study.
7. **Seven further visible-untracked candidates unresolved after round 3.** Resolved in round 4: `agent-plugin-dependency-governance`, `evaluation-closed-loop-orchestration`, `godot-wsl-artifact-validation`, `godot-rl-metric-regression` promoted to core/specialized atoms; `artifact-driven-evaluation-loops`, `artifact-handoff-orchestration`, `autonomous-evaluation-loops` archived after their unique details were folded into `evaluation-closed-loop-orchestration`.
8. **Two residual worktree items after the round-4 commit.** Resolved in TASK-009 package: `staged-commit-package-governance` promoted to core atom and staged by Hermes; `real-godot-closed-loop-validation.md` durable reference improvement kept as a standalone tracked improvement. The runtime `skills/` directory matched the intended 21-skill core after this package was committed; post TASK-013 cleanup adds `skill-pack-roadmap-execution`, and the README/license packaging pass adds `open-source-project-packaging`, bringing the intended core to 23 tracked skills.

## Prioritized next actions

| Priority | Action | Owner | Notes |
|---:|---|---|---|
| P1 | Commit the round-2 reconciliation when the user requests it: two promoted core skills + four archived candidates + doc updates. | Hermes | Commit/push remains out of scope until explicitly requested. Round-2 work is already committed at `97f78ca`. |
| P1 | Commit the round-3 promotion when the user requests it: `skill-pack-governance-validation` promoted to core + doc updates. | Hermes | Commit/push remains out of scope until explicitly requested. |
| P1 | Commit the round-4 promotion when the user requests it: four promoted core/specialized atoms + three archived loop variants + folded detail + reference files + doc updates. | Hermes | Commit/push remains out of scope until explicitly requested. Do not overclaim post-push migration readiness; fresh-clone validation still pending. |
| P1 | Commit the TASK-009 residual cleanup when the user requests it: one promoted core atom (`staged-commit-package-governance`) + reference file + Godot validation reference improvement + doc updates. | Hermes | Commit/push remains out of scope until explicitly requested. Codex review pending; fresh-clone validation still pending. |
| P1 | Run `python3 scripts/validate-skill-pack.py` before every skill-pack change. | Hermes / Claude | Added to HERMES.md validation commands. |
| P2 | Merge `repository-governance-initialization` unique steps into `hermes-project-init-orchestration/references/` as a case study; then delete the archived copy. | Claude (after Codex review) | Open as a follow-up task. |
| P2 | If promoting a domain validation candidate later, fix broken `references/godot-rl-stage2-optimizer.md` link first. | Claude | Follow `docs/ai-collaboration/candidate-skills/README.md`. |
| P3 | Execute the review-loop family consolidation map with evidence (trajectory records + evidence package) before rewriting. | Claude (under hercules-meta-skill-evolution) | Do not rewrite without evidence. |
| P3 | Reduce drift between `hercules-collaborative-agent-workflow` and `hermes-collaborative-workflow` by replacing duplicated prose with links to the base skill. | Claude | Future skill-patch round. |

## Practical usability validation

Round 2 was practiced in the live repository rather than only documented. Round 3 extends the evidence with a clone-copy validation performed after pushing commit `97f78ca`, now codified by the `skill-pack-governance-validation` core skill. Round 4 reconciles seven further visible-untracked candidates (four promoted, three archived) against the same validator and ledger discipline; fresh-clone validation of the round-4 package is still pending and should be run after the promoted skills are committed. See `docs/ai-collaboration/USABILITY_VALIDATION.md` for evidence covering runtime symlink, the round-3 16-core-skill inventory, archived candidate non-loading, validator/static checks, bootstrap audit-only mode, clone-copy acceptance for `97f78ca`, and the actual Hermes → Claude → Hermes verify → Codex → TASKS closure loop. TASK-009 adds one promoted atom (`staged-commit-package-governance`) and keeps a Godot validation reference improvement. Post TASK-013 cleanup added `skill-pack-roadmap-execution`; the README/license packaging pass adds `open-source-project-packaging`, bringing the current runtime core to 23 tracked skills. Fresh-clone validation of the broader package remains a separate migration proof.

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

The validation script reports 0 errors. After Hermes stages the round-3 promoted core skill file (`skill-pack-governance-validation`) for tracking and archives the unrelated game telemetry candidate outside `skills/`, the runtime `skills/` directory matches the intended round-3 16-skill core. Round 4 adds four promoted atoms and archives three loop variants; after staging/commit, the runtime `skills/` directory matches the intended 20-skill core and archived candidates live outside `skills/`. TASK-009 promotes one additional atom (`staged-commit-package-governance`) and keeps a Godot validation reference improvement; post TASK-013 cleanup promotes `skill-pack-roadmap-execution`; the README/license packaging pass promotes `open-source-project-packaging`; Hermes staged the current package and the validator reports 0 errors / 0 warnings with the intended 23-skill core. Reflection signals are non-failing and should point to concrete task IDs or review files rather than template prose.
