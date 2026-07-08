---
name: staged-commit-package-governance
description: "Use when preparing a staged commit/package while preserving unrelated work: verify index-vs-worktree boundaries, keep ledgers and trajectories truthful, run staged privacy checks, and use narrow Codex rechecks after review findings."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, git, staging, governance, commit-package, codex-review, ledger]
    related_skills: [skill-pack-governance-validation, workflow-skill-pack-audit, coding-agent-orchestration]
---

# Staged Commit Package Governance

## Overview

Use this class-level skill when Hermes has prepared an intended staged package but must preserve unrelated unstaged user work. The goal is to make the staged index, task ledger, trajectory record, validation evidence, and final report all describe the same package.

This complements `skill-pack-governance-validation`: that skill governs the broad acceptance pass (runtime loading, archived candidate safety, validator/static checks, bootstrap audit-only, staged privacy scan, commit-package readiness); this atom narrows in on the staged-package boundary and ledger-truth cycle — preserving unrelated unstaged work, keeping TASKS/CR ledgers and trajectory records truthful after staging, and driving narrow Codex rechecks when review finds ledger drift. Use them together rather than choosing one: the umbrella proves the pack is usable and safe to package; this atom keeps the staged index, ledger, trajectory, and review record describing the same package during the staging/review cycle.

## When to Use

Use when:

- a repo has both intended staged changes and unrelated unstaged edits;
- a skill-pack or governance package is ready for Codex review but not yet committed;
- TASKS/CR ledgers mention staged files, validation evidence, owners, or trajectories;
- Codex review finds stale ledger wording after files were staged or re-staged;
- the user has not explicitly authorized commit/push.

## Procedure

1. **Define the package boundary.** List exactly which paths belong in the intended staged package and which visible changes are intentionally excluded.
2. **Stage only the package.** Do not stage unrelated user edits just to make `git status` clean.
3. **Validate both worktree and index.** Run the repository validator, `git diff --check`, `git diff --cached --check`, relevant syntax checks, and a staged filename/content privacy scan.
4. **Verify runtime/load behavior when skills are involved.** Load promoted runtime skills and verify archived candidates no longer resolve.
5. **Re-read the ledger after staging.** Make TASKS/CR records match the staged index: modified-file lists, checkboxes, owner/next-owner, trajectory actor path, `codex_result`, review record path, residual risk, and excluded unstaged work.
6. **Search future/backlog text too.** If the package changes counts, names, or status, search not only the active task but also roadmap and future backlog sections for stale hard-coded counts or pending-state wording.
7. **Ask Codex to review the staged diff and staging boundary.** The prompt should explicitly mention any intentionally unstaged files so Codex does not mistake them for package drift.
8. **Repair ledger drift narrowly.** If Codex finds stale ledger text, patch only the affected records, re-stage them, rerun validator/diff checks, and request a narrow recheck of that CR.
9. **Report state without overclaiming.** Separate staged-package readiness from commit/push and from fresh-clone/fresh-machine migration readiness.

## Stale Text Search Patterns

When a package changes skill-pack size or status, search for hard-coded counts and stale pending words:

```text
20-skill pack|20 个核心 skill|20 个核心|pending staging|currently untracked|remains unstaged|待 Hermes 暂存|待暂存
```

Prefer count-neutral wording such as “current core skill pack” in future backlog tasks unless the exact count is the acceptance target.

## Verification Checklist

- [ ] `git diff --cached --name-only` matches the intended package list.
- [ ] unrelated unstaged edits are named and explicitly excluded.
- [ ] modified-file lists in ledgers include every staged file that matters to the task.
- [ ] trajectory fields reflect the actual review state, not an earlier pending state.
- [ ] `git diff --check` and `git diff --cached --check` pass.
- [ ] validator and relevant syntax checks pass.
- [ ] staged privacy scan finds no secret-like filenames or content.
- [ ] hard-coded count / pending-state searches are clean or intentionally explained.
- [ ] Codex review/recheck record is saved and linked before closure.
- [ ] final report says staged/not committed/not pushed unless commit/push actually happened with authorization.

## Pitfalls

1. **Stale ledger after staging.** Staging a new skill or review record can make old TASKS wording false. Re-read the ledger after staging, not only before.
2. **Clean-status temptation.** Do not stage unrelated user work just to eliminate `git status` noise. Preserve it and document that it is outside the package.
3. **Index/worktree mismatch.** `git diff --check` alone does not validate the staged package; pair it with `git diff --cached --check`.
4. **Review record not linked.** After saving a Codex review record, update the task's review path and trajectory source pointers.
5. **Migration overclaim.** Passing current-machine validator and runtime loading does not prove fresh-clone or fresh-machine readiness.

## References

- `references/round4-staged-package-boundary.md` — concrete Hercules round-4 pattern: staged TASK-007/TASK-008 package, unrelated unstaged Godot reference edit, Codex P2 ledger drift, Hermes repair, narrow Codex PASS recheck.
