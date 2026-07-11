# Hercules Review Workflow

## Purpose

This internal workflow selects an available reviewer from confirmed capabilities and makes independence conditional on the task. Review is an evidence gate, not a permanent assignment to a named facility.

## Review Mode

```text
ordinary verification: use any confirmed suitable reviewer or Hermes verification
independent review requested/required: reviewer must be independent of the implementation actor
no independent reviewer available: report the independence gap; do not install one
review FAIL: return stable findings to the implementation route, then re-review
review PASS: close only after fresh verification evidence
```

Determine the independence requirement from the user request, project instructions, risk contract, or acceptance criteria. Do not invent independence for ordinary checks, and do not weaken an explicit independence requirement.

## Procedure

1. Read the task criteria, implementation route, confirmed capability map, and independence requirement.
2. Select an available reviewer with sufficient read-only capability; exclude the implementation actor only when independence is required.
3. Provide the exact artifact or diff, acceptance criteria, known risks, and existing verification evidence.
4. Require inspection of actual artifacts and task-appropriate checks rather than accepting implementation self-report.
5. Normalize actionable findings using the [review loop](review-loop.md).
6. On FAIL, return the stable findings to a confirmed write-capable implementation route and re-review the resulting change.
7. On PASS, obtain fresh verification evidence and report the reviewer, independence status, scope, checks, and outcome.

## Review Output

A review outcome contains:

- verdict: `PASS`, `FAIL`, or `BLOCKED`;
- reviewer and whether the independence requirement was satisfied;
- reviewed artifact or diff scope;
- stable finding IDs with evidence and required verification;
- fresh checks observed after the final change.

## Common Mistakes

- Assuming one named facility is always required.
- Calling implementation self-review independent.
- Installing a reviewer to fill an independence gap.
- Creating a new finding ID for the same unresolved root cause.
- Closing after a fix without re-review and fresh evidence.
