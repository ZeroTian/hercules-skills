---
name: skill-pack-roadmap-execution
description: "Use when executing a multi-task skill-pack roadmap under Hermes: advance TASKS.md automatically after user authorization, delegate implementation/review, verify staged packages, close ledgers truthfully, and auto-commit after Codex PASS while keeping push separate."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, roadmap, tasks, audit, codex, claude, commit, governance]
    related_skills: [workflow-skill-pack-audit, staged-commit-package-governance, skill-pack-governance-validation, coding-agent-orchestration]
---

# Skill-Pack Roadmap Execution

## Overview

Use this class-level skill when the user wants Hermes to keep advancing a skill-pack roadmap rather than stop after each task. It covers the operating loop for `docs/ai-collaboration/TASKS.md`: inventory, implementation, validation, independent Codex review, ledger closure, and optional auto-commit.

This skill complements `workflow-skill-pack-audit` and `staged-commit-package-governance`: those cover audit/reconciliation and staged-package truth; this skill covers the continuous roadmap execution mode.

## When to Use

Use when:

- The user says “下一步”, “继续下一个任务”, or similar after a roadmap/task ledger exists.
- The user has explicitly authorized automatic multi-task execution.
- TASKS/CR records identify Claude/Codex owners and Hermes should orchestrate without making the user switch tools.
- Each task should be committed after Codex PASS, while push remains separately authorized.

Do not use when the user asks only for planning, only for review, or for a one-off code edit with no ledger/roadmap.

## Procedure

1. **Confirm the authorization boundary from memory/session.** Auto-advance and auto-commit require user authorization. Push still requires explicit separate authorization.
2. **Inspect live state before every task.** Run/read real `git status --short -uall`, recent `git log --oneline`, the active TASKS section, and relevant docs/skills. Do not rely on an agent summary alone.
3. **Set one active todo.** Use inventory -> implement -> verify -> review -> commit. Keep only one item `in_progress` at a time.
4. **Delegate implementation when useful.** Claude Code is preferred for substantial docs/skill/script changes. Brief it with exact scope, files, constraints, validation commands, and forbidden actions.
5. **Handle partial agent exits.** If Claude hits `max-turns` or exits nonzero after partial edits, inspect `git diff`, read changed files, and finish/fix small in-scope validation or ledger issues directly. Record the max-turns outcome in the trajectory/reflection fields instead of hiding it.
6. **Verify before review.** Run the relevant local gates and stage only the intended package.
7. **Use independent Codex review.** Codex review must be read-only unless explicitly asked to write a review record. Give Codex the staged scope, task goal, and exact verification evidence.
8. **Close only after PASS.** Write/link the Codex review record, update TASKS/roadmap truthfully, set `codex_result: PASS`, `score: 1.0`, and `next_owner: none` only after real PASS evidence.
9. **Auto-commit if authorized.** Commit after final validation and Codex PASS. Do not push unless explicitly authorized.
10. **Advance or stop.** If more active tasks remain and the user authorized continuation, move to the next task; otherwise report current clean state and next decision.

## Standard Validation Bundle

For Hercules skill-pack documentation/governance tasks, prefer:

```bash
python3 ./tests/test_validate_skill_pack_cli.py -v
python3 ./scripts/validate-skill-pack.py --strict
./scripts/hercules package
git diff --check
git diff --cached --check
git status --short -uall
git diff --cached --stat
```

Treat validator `ERRORS` and `WARNINGS` as blockers. Treat `REFLECTION SIGNALS` as advisory unless the task specifically requires resolving them. Repeated signals such as `max-turns` should feed an evidence package or skill improvement, not a weakened validator.

## Common Pitfalls

1. **Stopping after a successful commit despite active authorization.** If the user authorized automatic continuation and says “下一步”, advance to the next eligible task.
2. **Pushing under auto-commit authorization.** Commit and push are separate boundaries; do not push without explicit permission.
3. **Trusting agent self-report.** Always verify with real diff/status/file reads and commands.
4. **Premature ledger closure.** Do not mark checkboxes, trajectory score, or Codex result complete before review records and PASS evidence exist.
5. **Losing partial Claude work.** `max-turns` can still leave useful edits. Inspect and reconcile instead of discarding or blindly rerunning.
6. **Mixing staged and unstaged scope.** Stage only intended files, run staged package checks, and preserve unrelated work.

## References

- `references/continuous-task-advancement.md` — session-derived pattern for auto-advancing TASKS.md, handling Claude `max-turns`, and committing after Codex PASS without push.
