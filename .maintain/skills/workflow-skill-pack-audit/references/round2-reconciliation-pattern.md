# Round-2 Reconciliation Pattern

Condensed case study for `workflow-skill-pack-audit`: promote useful Hercules-owned workflow atoms, archive overlapping candidates outside runtime loading, stage before validator, and close the task ledger only after independent review.

## Pattern

1. Inventory both tracked runtime skills and visible skill directories.
2. Classify each candidate as promote, merge, archive, or discard.
3. Keep archived candidates under `docs/ai-collaboration/candidate-skills/` so they remain searchable but do not runtime-load.
4. Update README, ARCHITECTURE, SKILL_GROUP_AUDIT, TASKS, and candidate archive docs together.
5. Stage newly promoted skills before running the validator if the validator compares visible directories with git-tracked files.
6. Run validator, diff checks, syntax checks, and staged privacy scan.
7. Ask Codex to review the staged package and ledger truth.
8. Close the task only after review records are saved and linked from TASKS.

## Pitfalls

- Do not treat an untracked visible skill as promoted until it is staged or otherwise dispositioned.
- Do not leave candidate archives inside `skills/`; runtime discovery will treat them as active skills.
- Do not update README counts without also updating ARCHITECTURE and the audit record.
- Do not close a task from agent self-report alone; verify the staged diff and review record.
