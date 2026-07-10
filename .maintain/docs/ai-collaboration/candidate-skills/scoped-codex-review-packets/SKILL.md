---
name: scoped-codex-review-packets
description: "Use when Codex review must be tightly constrained to a specific diff/evidence packet, especially after a broad review wanders, omits a verdict, or over-reads large task/artifact trees."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, codex, code-review, orchestration, review-packet]
    related_skills: [coding-agent-orchestration, hercules-collaborative-agent-workflow, real-game-closed-loop-validation]
---

# Scoped Codex Review Packets

## Overview

Use this skill when Hermes needs an independent Codex review but the normal broad review risks reading too much, wandering into task ledgers/artifacts, or exiting without a usable PASS/FAIL verdict.

The pattern is class-level: create a small review packet, instruct Codex to read only that packet, demand a machine-checkable final verdict, and iterate on findings with regression tests.

## When to Use

Use when:

- a previous Codex run exited without a final verdict;
- Codex read large unrelated docs, task ledgers, or artifacts instead of the intended diff;
- review scope must be limited to a few files and specific evidence;
- the user asks for a shorter, stronger Codex review;
- Hermes needs a clear PASS/FAIL signal before closing work.

## Packet Contents

Write a temporary packet containing only:

1. Scope: exact files/diff under review.
2. Problem: the bug or behavior that motivated the change.
3. Implemented changes: short bullet list.
4. Validation evidence: exact tests and real run summaries.
5. Targeted diff: `git diff -- <scoped files>`.
6. Known prior findings fixed, if rerunning review.

Keep it short enough that Codex can review it without browsing the repo.

## Codex Prompt Contract

Use a prompt like:

```text
READ-ONLY REVIEW. Do not modify files. Do not inspect docs/TASKS.md.
Do not inspect the repository broadly. Do not inspect .artifacts except the
summarized evidence already in the packet. Read ONLY this packet: <path>.
Evaluate for P0/P1/P2 correctness/safety/regression/test-adequacy issues.
Output must be concise and must end with exactly one final verdict line:
VERDICT: PASS or VERDICT: FAIL. If fail, list findings with severity.
Do not provide process narrative.
```

Use `codex exec` with PTY and `notify_on_complete=true`. If the process exits but the final verdict line is missing, treat the review as unusable and rerun with a stricter packet/prompt.

## Iteration Rules

- Treat P0/P1/P2 findings as real review feedback, even if tests passed.
- Patch the root cause, not just the wording.
- Add a regression test for each accepted finding.
- Rerun the relevant tests before asking Codex again.
- Regenerate the packet after fixes so Codex sees the current diff and validation evidence.
- Continue until Codex returns `VERDICT: PASS` or a genuine blocker remains.

## Pitfalls

- A normal `codex exec` review can spend its budget reading large ledgers or artifacts and exit with command output but no final judgment. Do not count that as PASS.
- If the packet summarizes artifact evidence, do not ask Codex to inspect the full artifact tree unless necessary; huge temporary repos can distract from the source diff.
- Avoid shell metacharacter surprises in long prompts. Prefer writing the packet to a file and passing the file path.
- A PASS is scoped to the packet. Do not generalize it to unrelated dirty worktree changes.

## Example Findings This Pattern Catches

- A dynamic anchor fix that still hardcodes the target scene elsewhere in the prompt.
- Prompt metric conversion that crashes on malformed report values.
- A structural-priority prompt that still embeds a specific map name while the optimizer supports custom scenes.

## Verification Checklist

- [ ] Packet contains only scoped files and evidence.
- [ ] Codex was told not to inspect broad repo/docs/artifacts.
- [ ] Codex final output ends with `VERDICT: PASS` or `VERDICT: FAIL`.
- [ ] Any P0/P1/P2 findings have fixes plus regression tests.
- [ ] Relevant tests were rerun after fixes.
- [ ] Final report states the review scope and verdict.
