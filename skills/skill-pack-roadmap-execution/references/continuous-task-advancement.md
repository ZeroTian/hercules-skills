# Continuous Task Advancement Pattern

Session-derived pattern from the Hercules optimization roadmap where the user explicitly authorized Hermes to continue TASK-010 through TASK-013 automatically, commit each task after Codex PASS, and keep push separate.

## Proven loop

1. Confirm the authorization boundary: auto-advance + auto-commit were authorized; push was not.
2. Inspect live state before each task with Git status/log and the current TASKS section.
3. Use Claude Code for substantial skill/docs implementation where useful, but verify any self-report with real file reads and diff/status.
4. If Claude hits `max-turns` after partial edits, inspect the diff, finish narrow in-scope fixes directly, and record `max-turns` truthfully in the trajectory.
5. Run the validation bundle before Codex review.
6. Ask Codex for read-only independent review of the staged package.
7. Fix CR findings, request narrow rechecks, and only then close ledger fields.
8. Commit after PASS; do not push without separate authorization.

## Evidence from the session

- TASK-010: productized entrypoint and README landing; Codex PASS; committed.
- TASK-011: validator `--json` / `--strict` and fresh-clone smoke; Codex PASS; committed.
- TASK-012: skill navigation and TASKS archive split; Codex PASS; committed.
- TASK-013: external absorption workflow and WHY_HERCULES; Codex PASS; committed.

## Guardrails

- A clean-looking summary is not enough: run live `git status --short -uall` before reporting done.
- If a new runtime skill is created as a learning artifact, treat it like source: add linked references, update navigation lists, validate, review, and commit or delete it.
- Reflection signals such as repeated `max-turns` should become skill improvements or evidence packages, not ignored validator noise.
