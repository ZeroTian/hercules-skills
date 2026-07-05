# Skill Group Deep Research — Redundancy, Atomicity, and Skill-MAS Fit

Date: 2026-07-05
Repository: `/mnt/e/code/hercules-skills`
Reviewed commit: `749a377`

## Evidence sources

- Repository inspection: `git status --short -uall`, `git ls-files 'skills/*/SKILL.md'`, `find skills -mindepth 2 -maxdepth 2 -name SKILL.md`, `python3 scripts/validate-skill-pack.py`, skill file reads.
- Runtime check: `readlink -f ~/.hermes/skills/hercules` resolves to this repository's `skills/` directory.
- Paper source: arXiv API and PDF extraction for `Skill-MAS: Evolving Meta-Skill for Automatic Multi-Agent Systems`, arXiv `2606.18837v2`.
- Agent synthesis/review: Claude synthesis pass followed by Codex adversarial review. Codex result: PASS with non-blocking corrections incorporated here.

## Current state

Committed baseline at the start of this research was healthy:

```text
HEAD: 749a377
tracked core skills: 16
runtime symlink: ~/.hermes/skills/hercules -> /mnt/e/code/hercules-skills/skills
```

Before the P0/P1 convergence pass, the repository-visible runtime had one drift item:

```text
visible runtime skills from repository directory: 17
validator: 0 errors / 1 warning / 0 signals
warning source: skills/post-task-memory-skill-evolution/SKILL.md
```

After TASK-006, that standalone untracked skill was removed and its unique lessons were merged into existing skills; current validation is 0 errors / 0 warnings / 0 signals with 16 visible/tracked runtime skills.

Before convergence there were also four unstaged tracked skill edits, all expressing the same owner-driven dispatch principle:

```text
skills/coding-agent-orchestration/SKILL.md
skills/cross-agent-review-loop/SKILL.md
skills/hercules-collaborative-agent-workflow/SKILL.md
skills/hermes-collaborative-workflow/SKILL.md
```

## Redundancy clusters

### 1. Collaborative workflow entry/base pair

- `hercules-collaborative-agent-workflow` is a Hercules-specific entry wrapper.
- `hermes-collaborative-workflow` is the portable base actor-selection/orchestration contract.

Decision: keep both. The wrapper is valid because it applies user preferences and composes companion skills. Optimization is drift reduction: keep the long actor matrix, owner-dispatch rule, and brief rules in `hermes-collaborative-workflow`; make the Hercules wrapper point to it instead of restating it.

### 2. Review-loop family

- `coding-agent-orchestration`: CLI flags, Claude/Codex command patterns, max-turn handling, governance closure.
- `iterative-agent-code-review`: canonical multi-round Claude-fix -> Codex-review loop.
- `cross-agent-review-loop`: lighter restatement of the same loop.

Decision: keep `coding-agent-orchestration` and `iterative-agent-code-review`; treat `cross-agent-review-loop` as a candidate for merge/reference. It should either become a short quick-start section inside `iterative-agent-code-review` or move to references. Do not keep three long variants of the same loop.

### 3. Project-init pair and archived duplicate

- `hercules-project-init-workflow`: Hercules entry wrapper.
- `hermes-project-init-orchestration`: detailed governance-init state machine.
- archived `repository-governance-initialization`: duplicate/case-study candidate.

Decision: keep wrapper + atom. `hermes-project-init-orchestration` is currently the most overstuffed skill. It mixes project-init state machine, execution batches, and task/review templates. Future work should move templates to `templates/`, move case-study details to `references/`, and point implementation/review phases to collaborative workflow atoms instead of duplicating them.

### 4. Governance trio

- `hercules-skill-pack-management`: layout, symlink, backup, migration, GitHub sync, privacy checks.
- `workflow-skill-pack-audit`: classification, reconciliation, validator/recheck workflow, ledger closure.
- `skill-pack-governance-validation`: runtime usability, archived-candidate safety, staged package validation, bootstrap audit-only, commit-package readiness.

Decision: keep all three. They are distinct evidence buckets: layout/sync, audit/reconciliation, and acceptance/readiness. Add a short responsibility matrix to avoid trigger ambiguity.

### 5. `post-task-memory-skill-evolution`

This untracked skill should not enter core as-is. It overlaps `hercules-meta-skill-evolution`, `workflow-skill-pack-audit`, and `skill-pack-governance-validation`.

Preserve its unique value:

- durable user memory vs reusable skill boundary;
- patch loaded skills first;
- frustration/correction as a signal for memory + skill update;
- avoid narrow one-off skills;
- session-specific evidence belongs in references.

Recommended disposition: merge the memory-vs-skill boundary and post-task reflection checklist into `hercules-meta-skill-evolution`; move governance pitfalls into `workflow-skill-pack-audit` or `skill-pack-governance-validation`; then delete or archive the standalone untracked skill. This restores validator 0 warnings.

### 6. Kanban family

- `kanban-orchestrator`, `kanban-worker`, and `kanban-codex-lane` are sufficiently distinct.
- `kanban-codex-lane` may still contain project-specific prompt/safety material that should live under `templates/` if it is not general.

Decision: keep family intact; extract project-specific long blocks to templates or references if found during a targeted pass.

## Atomicity verdict

The pack does not need every entry skill to be atomic. Entry wrappers are useful when they prevent the user from manually loading a stack of atoms.

Current atomicity status:

| Area | Verdict | Action |
|---|---|---|
| Entry wrappers | acceptable | reduce duplicated prose, keep wrapper role |
| Governance trio | atomic enough | keep distinct, add responsibility matrix |
| Review-loop family | partially redundant | consolidate `cross-agent-review-loop` later |
| Project-init atom | overstuffed | split templates/references, reduce overlap |
| Post-task skill | redundant as standalone | merge/archive |

## Skill-MAS usefulness

Skill-MAS is useful for Hercules, but not as a full benchmark machine.

What is already correctly adopted:

- three-module scaffold: Task Decomposition / Agent Engineering / Workflow Orchestration;
- trajectory records with score, actor path, evidence, blockers, next owner;
- evidence package workflow: within-task contrast + cross-task synthesis;
- skill optimizer discipline: prune first, preserve scaffold, patch only evidence-backed generalized principles;
- structured review contracts;
- active merge/investigation before closure.

What should not be overclaimed:

- K=5 rollout, elbow selection, transfer experiments, and ablations are paper mechanisms, not yet Hercules practice.
- Hercules has no large labeled validation set; Codex PASS/FAIL can be a weak label only as a local pilot hypothesis.
- K=2-3 repeated attempts may be useful for selected high-value tasks, but this is a local experiment, not a paper-backed default.

Most valuable new exploration:

1. Add post-hoc trajectory fields:
   - `decomposition_quality: over-split | under-split | right-sized | unknown`
   - `agent_assignment_review: correct | overkill | underpowered | wrong-specialist | unknown`
2. Pilot K=2-3 trajectories only for expensive recurring workflow failures, not every task.
3. Use Codex severity/PASS as weak labels for prioritizing reflection, with explicit uncertainty.

## Optimized composition model

```text
entry wrappers
  hercules-project-init-workflow
  hercules-collaborative-agent-workflow
      |
      v
portable base atoms
  hermes-project-init-orchestration
  hermes-collaborative-workflow  <-- canonical owner-driven dispatch + actor matrix
  hercules-agent-capability-preflight
      |
      v
execution/review atoms
  coding-agent-orchestration      <-- CLI/flags/governance closure
  iterative-agent-code-review     <-- canonical multi-round review loop
  cross-agent-review-loop         <-- candidate to merge/reference
      |
      v
specialized lanes
  kanban-orchestrator
  kanban-worker
  kanban-codex-lane
  open-ended-research-orchestration
      |
      v
meta-skill evolution
  hercules-meta-skill-evolution
  templates/trajectory-record.md
  templates/evidence-package.md
  templates/codex-review-contract.md
      |
      v
governance validation
  hercules-skill-pack-management
  workflow-skill-pack-audit
  skill-pack-governance-validation
  scripts/validate-skill-pack.py
```

## Priority plan

> Implementation status (2026-07-05): P0 and P1 were implemented in TASK-006 (see `docs/ai-collaboration/TASKS.md#task-006`). The validator returned to 0 errors / 0 warnings / 0 signals and the core skill count returned to 16 after removing the standalone `post-task-memory-skill-evolution` skill; its unique lessons were merged into `hercules-meta-skill-evolution` and `skill-pack-governance-validation`. P2 and P3 below remain future work.

### P0 / release gate

Resolve `post-task-memory-skill-evolution`:

- merge unique memory-vs-skill content into `hercules-meta-skill-evolution`;
- merge governance pitfalls into governance trio if still needed;
- remove or archive standalone skill;
- run validator until 0 errors / 0 warnings / 0 signals.

### P1

Consolidate current owner-driven dispatch edits:

- canonical long guidance only in `hermes-collaborative-workflow`;
- short pointers in `hercules-collaborative-agent-workflow`, `coding-agent-orchestration`, and `cross-agent-review-loop`;
- keep the checklist item, remove repeated long prose.

Deduplicate structured review contract JSON:

- template remains `hercules-meta-skill-evolution/templates/codex-review-contract.md`;
- SKILL.md files point to the template instead of embedding copies.

### P2

Run an evidence-backed consolidation pass:

- merge/reference `cross-agent-review-loop` into `iterative-agent-code-review`;
- slim `hermes-project-init-orchestration` by moving templates/references out of SKILL.md;
- fold useful archived `repository-governance-initialization` content into project-init references.

### P3

Skill-MAS pilots:

- add optional post-hoc trajectory fields;
- test K=2-3 only on 2-3 recurring complex workflow types;
- record evidence package before changing permanent rules.

## Validation gate for any future change

```bash
python3 scripts/validate-skill-pack.py        # target: 0 errors / 0 warnings / 0 signals
git diff --check
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

Runtime checks:

- `skill_view` loads representative core skills.
- archived candidate such as `real-game-closed-loop-validation` does not load.
- visible `skills/*/SKILL.md` matches tracked/staged core skills.

Commit-package checks:

- staged package only;
- staged privacy scan no sensitive filenames or secret-like contents;
- Codex read-only review for P1/P2 structural changes;
- commit/push only after explicit user authorization.
