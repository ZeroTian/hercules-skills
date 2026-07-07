---
name: evaluation-closed-loop-orchestration
description: Build and govern evaluated-system loops that turn telemetry findings into safe modification requests, agent handoffs, and Claude/Codex review cycles.
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, orchestration, evaluation, telemetry, agent-handoff, safety-gates, claude-code, codex]
    related_skills: [hercules-collaborative-agent-workflow, coding-agent-orchestration, godot-rl-metric-regression, godot-wsl-artifact-validation]
---

# Evaluation Closed-Loop Orchestration

## Overview

Use this skill when the user wants a system to **discover issues, report them, and automatically push toward safe modifications** rather than having Hermes manually fix one sample by hand.

The target pattern is a class-level closed loop:

```text
real run / telemetry
  → diagnosis report
  → safe optimization attempt
  → gate accept/reject with evidence
  → modification_requests.json
  → agent_handoffs.json
  → owner-driven Claude/Codex implementation + review
```

This is especially useful for game/RL/simulation/evaluation projects, but the pattern applies to any project where real measurements, safety gates, and agent-managed task ledgers determine progress.

## Trigger Conditions

Load this skill when:

- The user asks to continue an autonomous/evaluated optimization loop.
- A run produces telemetry or diagnostics and the next step should be automatic, not manual interpretation.
- A candidate modification is rejected by a gate and the system needs to preserve the next actionable work package.
- The user corrects you away from “fix this sample directly” toward “make the system detect/report/push modifications.”
- A task creates or consumes `modification_requests.json`, `agent_handoffs.json`, escalation artifacts, CRs, or owner-driven dispatch records.

## Core Procedure

1. **Verify the real run source.** Inspect the telemetry/report/log/artifact that proves the issue exists. Do not rely on a narrative summary.
2. **Classify the issue boundary.** Separate objective/actionable issues from soft/report-only issues. Keep Goodhart boundaries explicit.
3. **Attempt only safe surfaces.** Candidate modifications must be limited to declared `allowed_surfaces`; measurement/control surfaces belong in `forbidden_surfaces`.
4. **Gate the attempt.** Accept only when real evaluation improves under the project’s gate. Rejected candidates are still useful evidence.
5. **Write `modification_requests.json`.** If issues remain unresolved or a candidate is rejected, write machine-readable requests with evidence and next-action hints.
6. **Write `agent_handoffs.json`.** Consume requests into per-agent handoffs with owner, next owner, brief, criteria, verification commands, evidence, and preserved safety surfaces.
7. **Dispatch owners.** If `owner=Claude` or `next_owner=Codex`, Hermes launches the corresponding CLI unless a real blocker exists.
8. **Review and close.** Codex independently reviews safety and behavior. Hermes updates task/CR ledgers only after verified PASS evidence.

## Artifact Contract

### Modification Request

Each request should include equivalent fields to:

- `source_issue`, `severity`, `category`, `message`
- `evidence`
- `requested_change_type`
- `allowed_surfaces`
- `forbidden_surfaces`
- `attempted_plan`
- `gate_result`
- `next_owner_hint`
- `next_actions`
- `blocked_reason`

Use this artifact when a diagnosis has enough objective evidence to drive a future modification but the current run cannot safely solve it yet.

### Agent Handoff

Each handoff should include equivalent fields to:

- `source_request_path`, `source_issue`
- `recommended_action`
- `owner`, `next_owner`
- `brief`
- `acceptance_criteria`
- `verification_commands`
- preserved `allowed_surfaces`, `forbidden_surfaces`, `evidence`, `gate_result`, `attempted_plan`, `blocked_reason`

The handoff brief must repeat forbidden measurement/control surfaces so the next agent cannot “fix” an issue by moving the ruler.

## Structured BLOCKED Outcome

If the current `allowed_surfaces` are insufficient for the recommended action, that is a valid loop outcome, not a failure. Produce a `BLOCKED_SCOPE_INSUFFICIENT` artifact instead of silently widening scope:

- `verdict=BLOCKED_SCOPE_INSUFFICIENT`
- `source_handoff_path`, `source_issue`, `recommended_action`
- why the current allowed surface is insufficient
- `required_new_safe_anchor` or required new capability
- `proposed_allowed_surfaces`, unchanged `forbidden_surfaces`
- `required_tests`, `required_verification_gates`
- `next_owner_hint`, `next_reviewer`
- copied `evidence` and `gate_result`

A structured BLOCKED result is progress: it converts an unsafe widen-scope temptation into the next safe-anchor capability task. See `references/issue-to-handoff-closed-loop.md` for a concrete artifact example.

## Owner Routing

Treat `owner`, `next_owner`, `next_owner_hint`, and `next_reviewer` as **executable routing signals**, not prose. Hermes launches the named CLI directly when the artifact names it and no real blocker exists; this is the mechanism behind Core Procedure step 7. A malformed artifact or incomplete boundary coverage is a real blocker — record a BLOCKED outcome rather than dispatching on an unsafe brief.

## Safety Rules

- Soft/persona/report-only issues do not enter objective modification requests unless the project explicitly changes the Goodhart boundary.
- `forbidden_surfaces` must cover the project’s measurement/control concepts such as goal/fall/reward/telemetry/diagnose/persona/model.
- Treat `allowed_surfaces` as a **positive allowlist**, not just a denylist.
- Reject conceptual measurement surfaces in `allowed_surfaces`, e.g. `reward`, `goal`, `fall`, `telemetry`, `diagnose`, `persona`, `model`, even when no concrete filename appears.
- Preserve safe negative-exclusion wording, e.g. “tunables whitelist excluding reward_/goal_/...” should not be misread as permission to edit those concepts.
- Prefer no dispatch over unsafe dispatch when an artifact is malformed or boundary coverage is incomplete.

## Safe-Anchor Validator Checklist

When adding a new structural safe anchor (the legal target of a future modification):

- [ ] Add TDD RED tests showing the legal new anchor is currently rejected.
- [ ] Keep previous safe anchors passing.
- [ ] Add reject tests for forbidden measurement/control anchors.
- [ ] Validate exact block shape with whole-block matching such as `fullmatch()`; avoid `match()` plus `$` when a trailing newline would weaken strictness.
- [ ] Reject trailing newline, extra fields, extra nodes, wrong parent/type, missing child nodes, wrong resources, and script/ext_resource insertion.
- [ ] Test `apply_patch`, rollback/snapshot if applicable, and scene/config sanity checks on fixtures.
- [ ] Verify real gameplay/measurement files have no diff when the task is only adding capability.

## Verification Checklist

Before claiming the loop advanced:

- [ ] Real telemetry/report/log proves the source issue.
- [ ] Rejected candidates record gate reason and scores or equivalent evidence.
- [ ] `modification_requests.json` exists and contains source issue, evidence, safety surfaces, and next actions.
- [ ] `agent_handoffs.json` exists and contains owner/next owner, brief, criteria, commands, evidence, gate result, and safety surfaces.
- [ ] Defensive tests cover malformed/soft/dangerous requests.
- [ ] Positive tests show known safe surfaces still dispatch.
- [ ] Full or relevant regression tests pass.
- [ ] Codex review PASS is recorded before task closure.

## Common Pitfalls

1. **Stopping at a report.** A diagnosis is not enough when the user wants automatic forward motion. Produce a request or handoff artifact.
2. **Hand-fixing the sample.** If the user wants the system improved, encode the next modification as an artifact/agent task rather than only tweaking today’s level or run.
3. **Denylist-only safety.** Checking only filenames misses conceptual measurement surfaces such as “reward shaping” or “GOAL_X coordinate.” Use a positive allowlist plus concept denylist.
4. **Losing non-goals.** If a task intentionally creates the next work package but does not implement the downstream design change, record that as a non-goal, not a failure.
5. **Trusting agent self-report.** Hermes must inspect diff, run tests, read artifacts, and update ledgers after Claude/Codex results.

## References

- `references/issue-to-handoff-closed-loop.md` — detailed artifact pattern and defensive checks from a real Godot/RL closed-loop session.
