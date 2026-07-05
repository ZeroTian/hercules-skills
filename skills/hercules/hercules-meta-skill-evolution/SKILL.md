---
name: hercules-meta-skill-evolution
description: "Use when improving Hercules workflow skills from real collaborative-agent outcomes: record trajectories, build evidence packages, compare success/failure traces, and patch only evidence-supported orchestration principles."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, meta-skill, skill-evolution, multi-agent, orchestration, evidence]
    related_skills: [hercules-collaborative-agent-workflow, hermes-collaborative-workflow, coding-agent-orchestration, cross-agent-review-loop, kanban-orchestrator]
---

# Hercules Meta-Skill Evolution

## Overview

Use this skill to evolve the user's Hercules collaborative workflow pack from real execution evidence. Treat the `hercules/` skill group as a portable, evolvable Meta-Skill: the goal is not to memorize one-off failures, but to improve reusable orchestration principles for how Hermes decomposes tasks, assigns Claude/Codex/Kanban actors, verifies evidence, and updates ledgers.

The workflow is inspired by Skill-MAS: collect compact trajectories, score outcomes provisionally, compare successful and failed traces, synthesize an evidence package, then patch only the implicated skill module with a generalized principle. Do not train models or build a benchmark platform unless the user explicitly asks; this skill is for lightweight workflow governance.

## When to Use

Use when:

- A Hercules collaborative run revealed a reusable orchestration lesson.
- Multiple Claude/Codex/Kanban attempts produced different outcomes on similar work.
- The user asks to optimize the协同作业技能组 or apply a paper such as Skill-MAS to the workflow.
- A recurring failure appears across tasks, CRs, or review loops.
- You are about to patch a Hercules workflow skill for process reasons rather than a typo.

Do not use for:

- One-off project facts, temporary TODOs, or task progress; those stay in ledgers/session history.
- Narrow case details with no reusable process lesson; put them in `references/` as a case study instead.
- Replacing Claude/Codex execution; this skill improves orchestration, not implementation.

## Three-Module Scaffold

Classify every proposed workflow change into one module:

1. **Task Decomposition — the what.** How Hermes scopes, splits, orders, prioritizes, and defines success criteria for work.
2. **Agent Engineering — the who.** Which actor owns each subtask, what capabilities/boundaries/context they need, and what output contract they must return.
3. **Workflow Orchestration — the how.** How outputs flow, how review loops/backtracking/parallelism work, how Hermes verifies and closes state.

Completion criterion: every candidate skill patch names exactly one primary module and, if needed, secondary modules affected.

## Trajectory Record

For formal collaborative work, add or preserve a compact trajectory record in the task ledger, review file, or evidence package. Use `templates/trajectory-record.md` as the source shape.

Minimum fields:

```yaml
trajectory:
  task_id: TASK-000
  attempt: 1
  skill_versions: {}
  score: provisional
  actor_path: Hermes -> Claude -> Hermes verify -> Codex
  phi:
    capability_preflight: scanned | cached | skipped-with-reason
    claude_result: not-launched | completed | max-turns | failed
    codex_result: not-launched | PASS | FAIL | BLOCKED
    verification: commands/logs/diff evidence
    blocker_type: none | scope | test | tool | external | unclear
```

Scoring is provisional and exists for sorting, not truth. Start with a simple rubric only when needed:

| Score | Meaning |
|---:|---|
| 1.0 | PASS with required evidence and no rework |
| 0.8 | PASS with minor P2/manual cleanup |
| 0.6 | PASS after meaningful rework |
| 0.3 | BLOCKED but with clear next owner/action |
| 0.0 | FAIL or no usable artifact |

Completion criterion: enough fields exist to compare why one attempt succeeded or failed; do not overfill ledgers with raw logs.

## Evidence Package Workflow

Use `templates/evidence-package.md` when there are at least two comparable trajectories, a repeated failure, or a proposed skill change that would affect future runs.

1. **Select evidence.** Prefer recent, verified trajectories with real command/log/CR evidence. Completion: every included trajectory has source pointers.
2. **Contrast within task.** Compare high-scoring and low-scoring traces: divergence point, success factors, failure modes, root causes. Completion: at least one concrete difference is identified or the package says why none exists.
3. **Synthesize across tasks.** Extract recurring weaknesses and strengths. Completion: each systemic claim points to multiple traces or is marked as single-case.
4. **Rank candidate patches.** Sort by expected impact and feasibility. Completion: every candidate names module, evidence, generalized principle, and risk.
5. **Decide patch/defer/store.** Patch only when evidence supports a general principle; otherwise store a case study under `references/`.

## Skill Patch Protocol

Before patching a Hercules workflow skill:

1. **Prune first.** Identify existing wording that evidence shows is ineffective, misleading, redundant, or contradicted. Completion: removed/replaced text is named, or state “no prune”.
2. **One conceptual upgrade per module per round.** Avoid piling unrelated rules into one edit. Completion: patch list has at most one substantive new idea per module.
3. **Evidence citation.** Every new rule points to an evidence package item, a verified case study, or an explicitly user-approved design decision. Completion: no unsupported permanent rule remains.
4. **Generalize.** Rewrite task-specific fixes as durable orchestration principles. Completion: rule does not mention one project, one file, one API, or one accidental failure unless stored as a reference example.
5. **Preserve scaffold.** Keep the target skill's role and structure intact. Completion: edited skill still has clear triggers, procedure, pitfalls, and verification checklist.
6. **Verify.** Validate frontmatter, linked files, and diff. Completion: skill loads or file validation passes, and the diff is reviewed.

## Structured Decision Contracts

When an agent result drives routing or ledger closure, require a machine-readable footer in addition to prose. Use `templates/codex-review-contract.md` for reviews.

Hermes must treat contracts as routing aids, not proof. Before closing state, Hermes performs an active merge/verification pass: check diff scope, commands/logs, stale markers, duplicate CRs, owner/next-owner, and task checkbox truth.

## Priority Reflection

When enough trajectory data exists, prioritize reflection using uncertainty and difficulty:

```text
uncertainty = stddev(scores for same task/type)
difficulty = 1 - mean(score)   # equivalent practical form for provisional scores
priority = 0.5 * norm(uncertainty) + 0.5 * norm(difficulty)
```

Sort by priority first. Use elbow detection only when there are enough tasks for it to be meaningful; otherwise manually inspect the top few. For expensive Hercules tasks, K=2-3 repeated attempts may be a low-cost starting point, but this must be calibrated against real data and must not be presented as proven.

## Reference Cases

- `references/skill-mas-paper-application-case.md` — how the Skill-MAS paper was translated into the Hercules workflow pack, including reviewer caveats about provisional scores, K values, structured review contracts, and evidence-backed patching.

## Common Pitfalls

1. **Turning one failure into a permanent rule.** Store narrow lessons as case studies unless they recur or the user explicitly approves the rule.
2. **Overfitting to a project.** Hercules skills should transfer across repositories; project-specific facts belong in project docs.
3. **Pretending provisional scores are objective.** Use scores to prioritize review, not to certify truth.
4. **Patching without pruning.** Adding forever creates sediment. Remove or sharpen stale guidance first.
5. **Parsing prose as control flow.** Ask reviewer/decision agents for structured contracts when their output changes state.
6. **Passive merge nodes.** Hermes verification must actively recover missing evidence before closure.
7. **Premature automation.** Build templates and records before benchmark runners or A/B systems.

## Verification Checklist

- [ ] Proposed change is classified under Task Decomposition, Agent Engineering, or Workflow Orchestration
- [ ] Trajectory records or verified case evidence exist
- [ ] Evidence package distinguishes repeated pattern vs single-case lesson
- [ ] Candidate patch is generalized and evidence-supported
- [ ] No more than one substantive upgrade per module in this round
- [ ] Existing stale/redundant wording was pruned or explicitly kept
- [ ] Structured contracts are used where agent output drives routing/closure
- [ ] Hermes active verification gates ledger closure and state-changing actions
- [ ] Skill frontmatter and linked templates validate
