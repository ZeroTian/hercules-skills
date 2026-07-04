# Skill-MAS Lessons for Hercules Collaborative Workflow

Session source: analysis of `Skill-MAS: Evolving Meta-Skill for Automatic Multi-Agent Systems` (arXiv:2606.18837v2) and adversarial Codex review of the resulting recommendations.

## Core transfer

Treat the Hercules workflow pack as a hand-authored Meta-Skill:

- **Task Decomposition**: task splitting, Kanban lanes, acceptance criteria, dependency mapping.
- **Agent Engineering**: Hermes/Claude/Codex role selection, capability preflight, prompt contracts, boundary conditions.
- **Workflow Orchestration**: fix→review loops, fan-out/fan-in, evidence handoffs, CR closure, retry/replan rules.

The useful lesson is not to rebuild a full automatic MAS benchmark immediately. The useful lesson is to add an experience-retention loop around the existing workflow: record trajectories, score outcomes provisionally, reflect on high/low-performing traces, and patch skills only from evidence.

## Lightweight trajectory record

For formal collaborative work, record or summarize enough data to reconstruct the orchestration trajectory:

```yaml
trajectory:
  task_id: TASK-123
  attempt: 1
  skill_versions:
    hercules-collaborative-agent-workflow: 1.0.0
    coding-agent-orchestration: 1.0.0
  score: provisional
  phi:
    capability_preflight: Claude/Codex scanned or cache reused
    actor_path: Hermes -> Claude -> Hermes verify -> Codex
    claude_result: completed | max-turns | failed | not-launched
    codex_result: PASS | P0/P1/P2/P3 | BLOCKED | not-launched
    verification: tests/logs/diff/ledger evidence summary
    blocker_type: none | tool | test | unclear-scope | external | user
```

`phi` is a compact evidence snapshot, not a full transcript. Prefer links/paths to logs and CR records.

## Provisional score field

Use a numeric score only as an early sorting signal, not as a hard truth. A starting rubric can be:

- `1.0`: PASS with no material rework.
- `0.8`: PASS with minor cleanup or deferred P2/P3.
- `0.6`: PASS after repair loop.
- `0.3`: BLOCKED with a clear next owner/action.
- `0.0`: FAIL, unusable result, or unresolved P0/P1.

This rubric is not from the paper; calibrate it against Hercules data over time. If unsure, record `score: provisional` plus the raw outcome.

## Evidence package before skill edits

Before making broad workflow-skill changes, produce a compact evidence package:

```markdown
# Hercules Workflow Evidence Package

## Scope
- task set:
- skill versions:
- time window:
- reviewer:

## Trajectory Summary
| task | attempt | score | actor path | result | blocker |
|---|---:|---:|---|---|---|

## Within-task Contrast
- high-score success factors:
- low-score failure modes:
- divergence points:
- root causes:

## Cross-task Synthesis
- recurring weakness:
- recurring strength to preserve:
- implicated module: Task Decomposition | Agent Engineering | Workflow Orchestration

## Candidate Skill Patches
| priority | module | evidence | generalized principle | risk |
|---|---|---|---|---|
```

Only promote a lesson into a main SKILL.md rule when it is evidence-backed or clearly a reusable safety/quality invariant. One-off lessons should live in `references/` as case studies.

## Skill optimizer protocol

When evolving Hercules workflow skills:

1. Preserve the class-level skill shape; do not create narrow one-session skills.
2. Preserve the three conceptual modules: decomposition, agent engineering, orchestration.
3. Review existing guidance first; prune or rewrite evidence-contradicted/redundant rules before adding new ones.
4. Add at most one substantive conceptual upgrade per implicated module per evolution pass.
5. Every new rule should cite the evidence package or a concrete recurring pitfall.
6. Abstract changes into general orchestration principles, not task-specific patches.
7. Run a structural sanity check: trigger conditions, procedure, pitfalls, and verification remain clear.

## Selective reflection adaptation

The paper prioritizes tasks by uncertainty and difficulty. For Hercules, do this lightly:

- Sort reflection candidates by failed/blocked tasks, repeated repair loops, high-severity Codex findings, max-turns partial completions, and inconsistent outcomes.
- Use numeric mean/stddev only when there are multiple comparable attempts.
- Use elbow selection only when enough samples exist; otherwise just review the top few high-signal cases.
- K=3 can be a low-cost experiment for selected tasks, but it is not proven sufficient for Hercules. Calibrate before relying on it.

## Structured decision contracts

When Codex or another reviewer drives routing, prefer a structured footer in addition to prose:

```json
{
  "verdict": "PASS | FAIL | BLOCKED",
  "highest_severity": "P0 | P1 | P2 | P3 | none",
  "findings": [
    {
      "id": "CR-001",
      "severity": "P1",
      "location": "path:line",
      "root_cause_category": "correctness | test | architecture | security | docs | process",
      "required_fix_contract": "specific condition before PASS",
      "verification_required": "command or evidence"
    }
  ],
  "next_owner": "Hermes | Claude | Codex | User | none"
}
```

Phrase this as formalizing review output, not assuming all current reviews are unstructured.

## Active merge investigator rule

Hermes verification should act as an active merge/investigation node, not a passive summary step. Before ledger closure or any real state-changing action, Hermes should recover missing evidence where feasible:

- inspect diff scope;
- verify task/CR ledger consistency;
- run or inspect required tests/logs;
- ensure CR IDs are updated rather than duplicated;
- check for stale `待复核`, unchecked review markers, or contradictory owner/next-owner fields.

If evidence is missing or low-confidence, route to targeted repair, re-review, or user decision instead of closing optimistically.
