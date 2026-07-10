# Round-4 Staged Package Boundary (Case Study)

Condensed pattern from the Hercules round-4 reconciliation (TASK-007 + TASK-008 package) where an intended staged package had to coexist with unrelated unstaged work and a Codex review found ledger drift after staging. Supports `skills/staged-commit-package-governance/SKILL.md`.

## Situation

After round 4, the worktree held:

- an intended staged package: TASK-007 `codex-plugin-cc` absorption + TASK-008 round-4 skill-pack reconciliation (four promoted atoms, three archived loop variants, folded detail, reference files, doc updates);
- an unrelated unstaged user edit: `skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md`;
- a not-yet-dispositioned untracked candidate: `skills/staged-commit-package-governance/`.

The user had not authorized commit/push. Hermes needed to stage only the intended package, preserve the unrelated edit, and keep the TASKS/CR ledger truthful about what was staged.

## Boundary that worked

1. **List the package paths explicitly.** Every path that belonged in the TASK-007/TASK-008 package was named; the Godot reference edit was named as intentionally excluded.
2. **Stage only the package.** `git add` targeted only the intended paths. The unrelated Godot edit stayed unstaged so `git status` still showed it, documented as outside the package.
3. **Validate both worktree and index.** `git diff --check` validated the worktree; `git diff --cached --check` validated the staged index. The validator, `bash -n`, and bootstrap audit-only were re-run against the staged state.
4. **Re-read the ledger after staging.** The TASK-008 record was re-checked against the staged index: modified-file list, owner/next-owner, trajectory actor path, `codex_result`, and residual-risk wording.

## Ledger drift caught by Codex (CR-T008-001)

Codex initial review found the TASK-008 ledger was stale relative to the staged index:

- the modified-file list omitted `agent-plugin-dependency-governance`;
- the record still described four promoted skills as unstaged after Hermes had staged them;
- the trajectory `actor_path` / `verification` / `codex_result` fields still reflected an earlier pending state.

This is the core ledger-truth risk: staging a new skill or review record can make earlier TASKS wording false. Re-reading the ledger before staging is not enough; re-read it after staging.

## Narrow repair + recheck

Hermes did not re-open the whole task. The repair was narrow:

1. Patch only the affected TASK-008 fields (modified-file list, residual risk, trajectory `actor_path` / `verification` / `codex_result`).
2. Re-stage the edited TASKS.md.
3. Re-run validator and `git diff --cached --check` against the updated staged state.
4. Request a **narrow Codex recheck** of only CR-T008-001, not a fresh full review.

Codex recheck returned PASS with no remaining findings.

## Reporting pattern

The final report separated four states explicitly:

- **committed**: nothing yet (no push authorization);
- **staged**: the intended TASK-007/TASK-008 package;
- **unstaged**: the unrelated Godot reference edit, intentionally excluded;
- **unpushed**: the staged package was not yet committed or pushed.

Passing current-machine validator, diff checks, and bootstrap audit-only did not imply fresh-clone or fresh-machine readiness; that remained a separate evidence bucket.

## Non-goal

A staged package that preserves unrelated work is not a commit. Recording the staged/not-committed/not-pushed state truthfully is the deliverable; commit and push remain gated on explicit user authorization.
