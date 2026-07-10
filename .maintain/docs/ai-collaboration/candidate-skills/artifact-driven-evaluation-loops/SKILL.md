---
name: artifact-driven-evaluation-loops
description: "Orchestrate artifact-driven evaluation/modification loops: modification requests, agent handoffs, safe execution or structured BLOCKED results, and Codex-reviewed next tasks."
version: 1.0.0
tags: [hercules, autonomous-evaluation, artifact-handoff, modification-request, agent-handoff, code-review]
related_skills: [autonomous-evaluation-loops, evaluation-closed-loop-orchestration, hercules-collaborative-agent-workflow, coding-agent-orchestration]
---

# Artifact-Driven Evaluation Loops

## When to Use

Use when a project produces or should produce machine-readable artifacts that drive the next modification step, such as:

- `modification_requests.json`
- `agent_handoffs.json`
- `blocked_handoff_result.json`
- review/closure artifacts that declare `owner`, `next_owner`, `next_owner_hint`, or `next_reviewer`

Use especially when the user clarifies that the goal is **not** to manually perfect the current sample/demo/game, but to make the system discover, report, and automatically push modifications.

## Core Principle

Do not stop at a diagnosis or prose summary. A healthy evaluated-system loop turns each unresolved issue into the next machine-readable artifact and then dispatches the indicated owner.

```text
real run / telemetry
  -> diagnosis report
  -> safe optimizer/gate attempt
  -> modification_requests.json
  -> agent_handoffs.json
  -> Hermes dispatches owner
  -> safe execution OR BLOCKED_SCOPE_INSUFFICIENT
  -> Codex review
  -> next task/artifact
```

## Hermes Responsibilities

1. Read the actual artifact before writing the next brief. Do not infer fields from memory.
2. Preserve and pass through `allowed_surfaces`, `forbidden_surfaces`, `evidence`, `gate_result`, `attempted_plan`, and `blocked_reason`.
3. Treat `owner`, `next_owner`, `next_owner_hint`, and `next_reviewer` as executable routing signals.
4. Launch Claude/Codex directly when the artifact names them and no real blocker exists.
5. Verify artifact schema, diff scope, tests, and ledger state before closing the task.
6. Delegate independent Codex review for review-required work.

## Safety Rules

- Never make an issue disappear by changing the measurement/control surface: goal/fall thresholds, reward shaping, telemetry, diagnosis thresholds, persona panels, or model files.
- Use explicit `allowed_surfaces` and `forbidden_surfaces` in every handoff.
- For proposed future surfaces, use a positive allowlist plus concept denylist.
- File-extension-only validation is insufficient when safe and forbidden nodes share the same scene/file.

## Structured BLOCKED Outcome

If the current allowed surface is insufficient for the recommended action, this is not a failure. It is a valid loop outcome if it is structured and reviewable.

Produce a `BLOCKED_SCOPE_INSUFFICIENT` artifact containing:

- `source_handoff_path`
- `source_issue`
- `recommended_action`
- why the current allowed surface is insufficient
- `required_new_safe_anchor` or required new capability
- `proposed_allowed_surfaces`
- unchanged `forbidden_surfaces`
- `required_tests`
- `required_verification_gates`
- `next_owner_hint`
- `next_reviewer`
- copied `evidence` and `gate_result`

Do not silently widen scope to implement the desired action.

## TDD / Verification Expectations

Minimum tests for this class of loop:

1. Artifact can be consumed into the next artifact.
2. Dangerous allowed/proposed surfaces are rejected.
3. Forbidden surfaces are preserved and cover measurement/control concepts.
4. Real prior artifact can be consumed end-to-end.
5. BLOCKED artifact includes the next safe anchor, tests, and gates.

Hermes should run focused tests, relevant regression tests, full or justified tiered regression, syntax checks, and `git diff --check` before review.

## References

- `references/artifact-driven-handoff-loop.md` — session-derived pattern for `modification_requests.json -> agent_handoffs.json -> blocked_handoff_result.json` loops.
