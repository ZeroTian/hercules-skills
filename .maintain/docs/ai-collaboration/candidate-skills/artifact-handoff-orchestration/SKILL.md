---
name: artifact-handoff-orchestration
description: "Orchestrate machine-readable evaluation artifacts through modification requests, agent handoffs, structured BLOCKED outcomes, safe-anchor expansion, and Codex-reviewed closure."
version: 1.0.0
tags: [hercules, artifact-handoff, autonomous-evaluation, modification-request, safe-anchor, code-review]
related_skills: [artifact-driven-evaluation-loops, autonomous-evaluation-loops, evaluation-closed-loop-orchestration, hercules-collaborative-agent-workflow, coding-agent-orchestration]
---

# Artifact Handoff Orchestration

## When to Use

Use when an evaluated system should keep moving through machine-readable artifacts rather than stop at prose diagnostics, especially when the user says the goal is not to manually perfect the current sample/demo/game but to make the system discover, report, and automatically push modifications.

Typical artifacts:

- `modification_requests.json`
- `agent_handoffs.json`
- `blocked_handoff_result.json`
- review artifacts with `owner`, `next_owner`, `next_owner_hint`, or `next_reviewer`

## Core Loop

```text
real run / telemetry
  -> objective diagnosis
  -> safe optimizer/gate attempt
  -> modification_requests.json
  -> agent_handoffs.json
  -> Hermes dispatches owner
  -> safe execution OR BLOCKED_SCOPE_INSUFFICIENT
  -> Codex review
  -> next safe-anchor task or closure
```

Do not stop at a diagnosis like `combat_bypassed`. The next durable artifact should say what action, owner, safety boundary, evidence, and verification gates come next.

## Hermes Procedure

1. Read the actual upstream artifact before writing the next brief.
2. Preserve `allowed_surfaces`, `forbidden_surfaces`, `evidence`, `gate_result`, `attempted_plan`, and `blocked_reason` across handoffs.
3. Treat `owner`, `next_owner`, `next_owner_hint`, and `next_reviewer` as executable routing signals; launch Claude/Codex unless a real blocker exists.
4. If the requested action exceeds the current allowed surface, produce or preserve a structured `BLOCKED_SCOPE_INSUFFICIENT` artifact instead of widening scope.
5. Convert a structured BLOCKED result into the next safe-anchor capability task.
6. Hermes verifies actual diffs, artifacts, test counts, and ledger state before Codex review. Correct self-reported counts with real command output.
7. Codex independently reviews both tests and the safety boundary before closure.

## Safety Rules

- Never make an issue disappear by changing the measuring stick: goal/fall thresholds, reward, telemetry, diagnosis logic, persona panels, model files, or game-agent measurement files.
- Use explicit `allowed_surfaces` and `forbidden_surfaces` in every handoff.
- Use positive allowlists for safe surfaces and deny dangerous concepts after stripping harmless negative phrases.
- File-extension-only validation is insufficient when safe and forbidden nodes share a scene/config file.
- Capability-only safe-anchor tasks should not modify real gameplay files; applying a candidate plus import/smoke/metric regression is a follow-up task.

## Structured BLOCKED Outcome

A structured BLOCKED result is progress when the current allowed surface is insufficient. Include:

- `verdict=BLOCKED_SCOPE_INSUFFICIENT`
- `source_issue`, `recommended_action`
- explanation of why the current surface is insufficient
- `required_new_safe_anchor` or required new capability
- `proposed_allowed_surfaces`
- unchanged `forbidden_surfaces`
- `required_tests`, `required_verification_gates`
- `next_owner_hint`, `next_reviewer`
- copied `evidence` and `gate_result`

## Safe-Anchor Validator Checklist

When adding a new structural safe anchor:

- [ ] Add TDD RED tests showing the legal new anchor is currently rejected.
- [ ] Keep previous safe anchors passing.
- [ ] Add reject tests for forbidden measurement/control anchors.
- [ ] Validate exact block shape with whole-block matching such as `fullmatch()`; avoid `match()` plus `$` when a trailing newline would weaken strictness.
- [ ] Reject trailing newline, extra fields, extra nodes, wrong parent/type, missing child nodes, wrong resources, and script/ext_resource insertion.
- [ ] Test `apply_patch`, rollback/snapshot if applicable, and scene/config sanity checks on fixtures.
- [ ] Verify real gameplay/measurement files have no diff when the task is only adding capability.

## Codex Review Brief Must Ask For

- strict validator shape and whole-block matching;
- whether allowlists contain only safe anchors;
- forbidden-surface preservation;
- artifact schema and owner routing;
- real file diff scope;
- whether task ledger evidence matches real command output.

## References

- `references/artifact-driven-handoff-loop.md` — session-derived details for modification request → handoff → BLOCKED → safe-anchor escalation loops.
