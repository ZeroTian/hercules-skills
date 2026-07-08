# Codex Review — TASK-012 skill information architecture + TASKS scaling

Date: 2026-07-08
Reviewer: Codex CLI (`codex exec`, reasoning effort `xhigh`)
Scope: staged TASK-012 package for skill navigation, TASKS archive split, validator archive/navigation checks, and ledger truth.

## Initial review verdict

Verdict: FAIL
Highest severity: P2

Findings:

- `CR-T012-001` P2 — TASK-012 evidence/trajectory were stale: ledger text described obsolete reflection signals and omitted already-run package/diff validations.
- `CR-T012-002` P2 — `parse_skill_navigation()` stored navigation rows in a dict, so duplicate skill rows could pass as long as all tracked skills were present.
- `CR-T012-003` P2 — archive validation only checked links that already existed in live `TASKS.md`; it did not require non-empty archive files under `docs/ai-collaboration/tasks/*.md` to be linked.

Clean checks noted by Codex:

- `SKILL_NAVIGATION.md` currently has 21 rows matching the 21 tracked runtime skills, with no archived candidates.
- TASK-001 through TASK-009 archive content matches the pre-split ledger after intentional `task_record` pointer rewrites.
- Live `TASKS.md` keeps TASK-010 through TASK-013 only.

## Hermes fixes

- `CR-T012-001`: Updated TASK-012 evidence and trajectory command list to match the actual verification set and current reflection signals.
- `CR-T012-002`: Changed `parse_skill_navigation()` to retain all rows per skill and report duplicate skill rows.
- `CR-T012-003`: Added archive-file checks that warn when non-empty files under `docs/ai-collaboration/tasks/*.md` are not linked from live `TASKS.md`; final fix gates this on raw non-whitespace content rather than parseable task headings.

## Recheck 1 verdict

Verdict: FAIL
Highest severity: P2

- `CR-T012-001`: fixed.
- `CR-T012-002`: fixed.
- `CR-T012-003`: partially fixed; malformed non-empty archive files without parseable task headings could still be ignored.

## Recheck 2 verdict

Verdict: PASS
Highest severity: none

Codex verified:

- malformed non-empty archive probe emits `TASKS.md does not link non-empty task archive`;
- `python3 tests/test_validate_skill_pack_cli.py -v` passes (6 tests);
- `python3 scripts/validate-skill-pack.py --strict` reports 0 errors / 0 warnings / 2 advisory signals and exits 0;
- `git diff --check` and `git diff --cached --check` pass.

## Residual risks

- Reflection signals still mention TASK-012 max-turns/brief pressure and evidence-package recommendation. These are advisory signals, not release-blocking warnings.
- Commit is authorized by the user for TASK-010 through TASK-013 after Codex PASS; push remains out of scope until separately authorized.
