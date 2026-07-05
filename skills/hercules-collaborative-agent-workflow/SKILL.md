---
name: hercules-collaborative-agent-workflow
description: "Use when Hercules wants Hermes to orchestrate Claude Code and Codex CLI end-to-end: capability preflight, high/xhigh effort selection, Claude implementation, Codex review, verification, and task ledger updates."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, orchestration, claude-code, codex, code-review, workflow]
    related_skills: [hermes-collaborative-workflow, coding-agent-orchestration, cross-agent-review-loop, iterative-agent-code-review, hercules-agent-capability-preflight, hercules-meta-skill-evolution]
---

# Hercules Collaborative Agent Workflow

## Overview

Use this as the Hercules-specific entry skill for day-to-day collaborative development. It coordinates the user's portable `hercules/` development workflow pack while relying on bundled Hermes skills such as `claude-code`, `codex`, `hermes-agent`, and `opencode` from the target machine.

Default loop:

```text
Hermes gathers context
  -> capability preflight
  -> Claude Code implements with SDD/TDD
  -> Hermes verifies diff/tests/logs
  -> Codex independently reviews
  -> Hermes updates TASKS/CR records
  -> repeat until PASS or real blocker
```

## When to Use

Use when the user asks to:

- continue project work with Hermes as orchestrator;
- run a Claude implementation followed by Codex review;
- process `TASKS.md` batches;
- fix Codex CR findings through Claude and re-review;
- do architecture/code/docs changes that require independent review;
- avoid manual tool switching between Hermes, Claude Code, and Codex.

Use `hercules-project-init-workflow` instead when the primary task is repository governance initialization or reinitialization.

## Required Companion Skills

Load as needed:

1. `hermes-collaborative-workflow` — base actor selection and end-to-end loop.
2. `hercules-agent-capability-preflight` — live capability scan and effort selection.
3. `claude-code` — Claude Code launch patterns and caveats.
4. `codex` — Codex launch patterns and sandbox caveats.
5. `coding-agent-orchestration` — fix/review loop patterns.
6. `cross-agent-review-loop` or `iterative-agent-code-review` — stricter multi-round review when quality risk is high.
7. `test-driven-development` — RED/GREEN/REFACTOR discipline.
8. `subagent-driven-development` — when using Hermes `delegate_task` or Claude subagents for vertical slices.
9. `open-ended-research-orchestration` — for broad research before implementation.
10. `hercules-meta-skill-evolution` — when real runs should update the workflow pack through trajectory records, evidence packages, and evidence-backed skill patches.

Installed local custom workflow skills may already live under `hercules/`; bundled skills should stay in their official categories. `hercules/` stores the user's portable workflow pack.

## Actor Policy

- **Hermes** is the controller: gathers context, writes briefs, launches tools, monitors processes, verifies outputs, updates records, and reports state.
- **Claude Code** is the implementation worker for substantial code/docs/refactor/test changes.
- **Codex CLI** is the independent reviewer and closure authority for review-required work.
- **Hermes direct work** is allowed for small, low-risk, local edits and bookkeeping.
- **User** decides scope expansion, destructive operations, commits/pushes, and unresolved product choices.

### Owner-Driven Auto-Dispatch Policy

In Hermes-managed ledgers, `当前负责人` / `下一负责人` / `next_owner` are executable routing signals: Claude/Codex ownership means Hermes launches that CLI in the same turn, not that the user is told to run it. See `hermes-collaborative-workflow#Owner-Driven Auto-Dispatch` for the full actor matrix and the only valid stop-before-dispatch reasons (tool unavailable, auth/preflight failure, destructive/user-decision boundary, or a recorded blocker).

## Capability and Effort Policy

Before meaningful Claude/Codex launches, use `hercules-agent-capability-preflight`.

Minimum record for formal work:

```text
Capability preflight: Claude/Codex scanned or current-session cache reused.
Relevant capabilities: <plugins/MCP/agents/features actually available>.
Effort: high|xhigh because <reason>.
```

Effort defaults:

- `high` for normal repo implementation/review.
- `xhigh` for cross-subsystem, safety/gate, real external execution, failed-review, architecture, or deep debugging work.
- Avoid `xhigh` for tiny edits where latency/cost does not buy much.

## Execution Procedure

1. **Read rules and state.** For repos with governance, read `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, `TASKS.md`, relevant specs, and review records. Completion: current owner/status/next action are known.
2. **Classify and dispatch the work.** Decide Hermes direct vs Claude vs Codex vs user. If the current/next owner is Claude or Codex, launch that CLI in the same orchestration turn unless a real blocker exists. Completion: actor and effort are justified and either dispatched or explicitly blocked.
3. **Run capability preflight.** Scan or reuse current-session cache for Claude/Codex. Completion: brief mentions only real available capabilities.
4. **Delegate implementation to Claude when needed.** Scope the brief tightly: task ID, files, acceptance criteria, prohibited actions, SDD/TDD requirements, verification commands, no commit/push/reset.
5. **Verify Claude output.** Inspect exit code, logs, diff, task records, and run key tests yourself. Completion: self-report is backed by evidence.
6. **Delegate review to Codex when needed.** Use read-only review unless explicitly allowing task/review record writes. Include exact criteria and update rules.
7. **Verify Codex output.** Read modified records, check checkbox truth, and confirm PASS/FAIL evidence.
8. **Loop or stop.** If Codex rejects, route original CR back to Claude. If PASS, close task records. If blocked, record blocker and next owner.

## Brief Requirements

Claude brief must include:

- repo path and task/CR IDs;
- required files to read first;
- allowed files and forbidden actions;
- SDD/TDD expectation and RED/GREEN/REFACTOR evidence requirements;
- capability inventory and selected effort;
- exact verification commands;
- task ledger update requirements;
- “Do not commit, push, reset, read secrets, or touch unrelated files.”

Codex brief must include:

- read-only boundary, unless task/review record writes are explicitly allowed;
- task/CR IDs and acceptance criteria;
- diff/files in scope;
- verification commands to run or inspect;
- PASS/FAIL update protocol;
- “Do not commit, push, reset, or rewrite history.”

## State Reporting

Final or checkpoint reports should state:

```text
Hermes did: <direct actions>
Claude Code: launched/not launched, effort, result
Codex CLI: launched/not launched, effort, result
Verification: <real command/log output summary>
Task state: <status/current owner/next owner>
Next action: <Hermes continues | user decision | none>
```

Never say a command/test/agent succeeded unless its output was actually observed.

## Migration Pattern

Hercules development-workflow skills are portable as one group:

```text
~/.hermes/skills/hercules/
```

This group may contain both entry/policy skills and local custom atom workflow skills. Keep locally-authored development workflow skills here so migration is one directory, not a scattered set of categories.

Do **not** migrate bundled Hermes skills into this group. Use the target machine's own bundled versions of:

```text
claude-code
codex
hermes-agent
opencode
test-driven-development
plan
```

Preferred GitHub source for this user's portable workflow pack:

```text
https://github.com/ZeroTian/hercules-skills
```

When moving to another host, clone/copy `skills/` from that repo into `~/.hermes/skills/hercules/`, then start a fresh Hermes session and load the relevant skill by name. Do not ask the agent to infer missing skill contents from memory; it must read the actual `SKILL.md` files.

## Real Execution Reference

When the user asks to prove the workflow with a real run rather than more planning, use `references/real-execution-checklist.md`. Key rule: create a fresh artifact directory and redirect logs there instead of adding cleanup commands such as `rm -f /tmp/...`, which can trigger approval gates and block the actual run.

For Godot/RL/game-evaluation projects, also use `references/real-godot-closed-loop-validation.md`: validate a healthy real run, a controlled failure path, and a repaired copied-project path with telemetry/report/log evidence before claiming the loop works.

## Meta-Skill Evolution Reference

When a session reveals a reusable orchestration lesson, load `hercules-meta-skill-evolution` and use `references/skill-mas-meta-skill-evolution.md` before broadly changing Hercules workflow skills. Treat the Hercules workflow pack as an evolvable Meta-Skill: record compact trajectory evidence, use provisional scores only as sorting hints, compare successful and failed traces, produce an evidence package, then patch only the implicated workflow module with a generalized principle.

For formal collaborative work, prefer structured review/decision contracts and make Hermes verification an active merge/investigation node: recover missing diff/test/ledger evidence before closing CRs, marking tasks done, or taking any real state-changing action. Do not turn one-off failures into permanent rules without evidence; store narrow case details in `references/` instead.

## Common Pitfalls

1. **Migrating bundled skills into `hercules/`.** Do not copy/fork bundled skills such as `claude-code`, `codex`, `hermes-agent`, or `opencode`; use the target machine's built-ins. Local custom workflow skills can live in `hercules/`.
2. **Launching Claude/Codex without preflight.** The brief may request unavailable plugins/MCP.
3. **Using the wrong effort.** Default high; use xhigh for complex/high-risk work only.
4. **Trusting self-report.** Hermes must inspect actual diff, logs, records, and verification output.
5. **Skipping Codex for review-required work.** Claude implementation is not independent review.
6. **Creating duplicate CRs.** Update the original `CR-NNN` when rechecking.
7. **Leaving the user to switch tools.** If Hermes can launch the CLI, Hermes should do it.
7a. **Stopping at owner assignment.** In a Hermes-managed ledger, “next owner = Claude/Codex” is not a final state. It is the trigger for Hermes to launch Claude/Codex immediately.
8. **Blocking a real run with avoidable cleanup.** For experiments/builds/game runs, write to a unique artifact directory rather than deleting old temp logs in the launch command.
9. **Trusting wrapper success for real game runs.** For Godot/RL validation, inspect Python logs, Godot logs, fresh telemetry JSONL, and `report.json`; wrapper return code alone may hide Python timeout or missing telemetry.
10. **Hand-copying partial Godot projects.** For artifact copies, prefer `rsync` excluding generated caches (`.godot/`, `rec/`, telemetry) over manually selecting a few directories; partial copies can miss `.import`/`.uid`/autoload sidecars and create false runtime failures.

## Verification Checklist

- [ ] Relevant atom skills loaded or intentionally skipped
- [ ] Rules/state/specs read before delegation
- [ ] Capability preflight performed or fresh cache reused
- [ ] Effort selected and justified
- [ ] Ledger owner/next-owner was treated as executable routing; Claude/Codex was launched when indicated, or a real blocker was recorded
- [ ] Claude brief is scoped, testable, and prohibits unsafe actions
- [ ] Claude output verified by Hermes
- [ ] Codex review is independent and scoped
- [ ] Codex output verified by Hermes
- [ ] TASKS/CR records reflect real state
- [ ] Final report includes real verification evidence and next owner
