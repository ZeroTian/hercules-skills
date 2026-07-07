---
name: autonomous-evaluation-loops
description: "Build and govern autonomous evaluation/optimization loops that discover issues, report evidence, attempt safe modifications, and escalate unresolved problems as machine-readable requests."
version: 1.0.0
tags: [hercules, autonomous-evaluation, optimization-loop, telemetry, modification-request, godot, rl]
related_skills: [hercules-collaborative-agent-workflow, coding-agent-orchestration, test-driven-development]
---

# Autonomous Evaluation Loops

## When to Use

Use this skill when a project is trying to make a system evaluate artifacts, discover problems, report them, and automatically push toward modifications. Common examples:

- RL/game/playtest loops using telemetry and diagnosis reports.
- LLM/evaluator pipelines that propose candidate changes and gate them with metrics.
- Systems where the user says the goal is not to hand-fix the current sample, but to make the pipeline detect, report, and drive future fixes.

## Core Principle

Distinguish **instance fixing** from **system capability**.

- Instance fixing: manually tune the current demo until it looks better.
- System capability: create a repeatable loop that can detect issues, produce evidence, try safe candidates, reject bad candidates, and leave a structured next action.

When the user corrects the goal toward system capability, do not keep optimizing the sample by hand. Convert the discovered issue into a machine-readable modification request or escalation artifact that a next agent can consume.

## Required Loop Shape

A healthy loop should have artifacts for every transition:

```text
real run / telemetry
  -> diagnosis report with objective issues
  -> actionable issue enters proposer/optimizer
  -> safe candidate attempted through gates
  -> accepted OR rejected with metric evidence
  -> if unresolved/rejected: modification request artifact
  -> Hermes/Claude/Codex can pick up the request next
```

Console prose is not enough. If the candidate fails, the failure should still produce a next-step artifact.

## Modification Request Schema

Use a compact machine-readable artifact such as `modification_requests.json`. Field names can vary, but the semantics should include:

- `source_issue`: issue id from the report, e.g. `combat_bypassed`.
- `severity` / `category`.
- `evidence`: telemetry/report evidence copied from the issue.
- `requested_change_type`: e.g. `structural`, `tunable_search`, `logic`.
- `allowed_surfaces`: safe anchors or tunable surfaces currently allowed.
- `forbidden_surfaces`: measurement/control surfaces that must not be touched.
- `attempted_plan`: plan summary, if any candidate was tried.
- `gate_result`: accepted/rejected, reason, score before/after.
- `next_owner_hint`: usually `Claude` for implementation follow-up.
- `next_actions`: concrete follow-up directions.
- `blocked_reason`: why the current run did not solve the issue.

## Safety Rules

- Do not make the issue disappear by modifying the ruler: goal/fall thresholds, reward shaping, telemetry, diagnosis thresholds, persona panels, or model files are measurement surfaces.
- Keep subjective/persona soft issues report-only unless a separate task explicitly designs a safe objective interface.
- For structural edits, require safe-anchor validation. File-extension-only checks are insufficient when measurement/control nodes live in the same scene file.
- A rejected safe candidate is still useful if it records enough evidence and next actions for the next agent.

## TDD Expectations

Add tests before production changes. Minimum coverage:

1. Actionable objective issue -> structured modification request.
2. Soft/persona issue -> no objective request.
3. Rejected candidate -> gate result plus blocked reason.
4. Summary/report output -> artifact path/count so the next agent can find it.
5. Safety boundaries remain intact.

Run focused tests, relevant regressions, full or justified tiered regression, and `git diff --check`.

## Orchestration Pattern

1. Verify the issue from telemetry/report, not only visual intuition.
2. Ask whether the user wants a one-off sample fix or system-loop capability.
3. If system-loop capability, create or continue a task for issue-to-modification escalation.
4. Delegate implementation to Claude with SDD/TDD requirements.
5. Hermes verifies diff, tests, and real artifact output.
6. Delegate independent review to Codex.
7. Close the task only after the review passes and the artifact is machine-readable.

## References

- `references/issue-to-modification-escalation.md` — session-derived pattern and example from a Godot/RL `combat_bypassed` loop.