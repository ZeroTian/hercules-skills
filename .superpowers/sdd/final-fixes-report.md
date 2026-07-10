# TASK-015 Final Fixes Report

Date: 2026-07-10
State: **FIXED — AWAITING INDEPENDENT RECHECK**

TASK-015 remains `待复核`. No PASS, completion, merge, or push is claimed.

## Repair package

- `3ee0d9a` — privacy/navigation/capability/prerequisite/routing fixes.
- `823f350` — active maintainer path/runtime migration and historical archive.
- `d18a026`, `56df17f` — public Skill-entry parser regression coverage.
- `bdc5db1` — isolated update preflight, divergence/rewrite refusal, and real fast-forward coverage.
- `e42f4f2` — seven-finding ledger, table-driven aggregate coverage, and this report.
- Final recheck-fix commit — fresh-cache reuse, routing-reference navigation, advisory-path correction, and updated evidence.

## History integrity note

The original checkpoint was reported as `edee39d`; the shared-worktree reflog later recorded it as amended to `3ee0d9a`. This worker did not intentionally amend that checkpoint. The lost CR-001 portion was restored non-destructively in new commit `bdc5db1`, and no later history rewrite was performed.

## TDD ledger

| Finding | RED evidence | GREEN evidence |
|---|---|---|
| TASK015-CR-001 | divergent/dirty/rewrite init cases exposed fetch-first mutation | isolated preflight cases including real fast-forward |
| TASK015-CR-002 | redacted-output expectations failed against verbatim secret lines | distinctive secret absent; maintainer gate tests pass |
| TASK015-CR-003 | fresh compact/normalized cache returned no route; missing role stayed valid | cache records are consumed without discovery; missing/stale/failure cases invalidate and fall back; focused 6/6 |
| TASK015-CR-004 | active maintainer scan found deleted commands/Skills/paths | active scan 0; history explicitly archived |
| TASK015-CR-005 | missing/extra/wrong-entry navigation fixtures passed incorrectly | validator errors on all three drift classes |
| TASK015-CR-006 | missing prerequisite link/no-mutation assertions failed | Git/Hermes isolated snapshots pass |
| TASK015-CR-007 | independent recheck confirmed the routing reference was orphaned | Markdown navigation link resolves and passes runtime/strict coverage |
| TASK015-CR-008 | strict JSON signal emitted a non-resolving root-relative path | signal emits the real `.maintain/skills/...` target and the CLI test resolves it |

## Verification

- CR-003 focused cache/fallback set: 6/6 tests passed.
- Runtime owning suite: 26/26 tests passed.
- Validator CLI owning suite: 28/28 tests passed; CR-007 strict linked-reference check passed.
- Complete stdlib discovery suite: 88/88 tests passed; strict validator: 0 errors / 0 warnings.
- Bash, diff, forbidden behavior, active stale-surface, exact-five, and root executable scans: clean.
- Final staged package gate: passed with redacted output.

## Concerns retained for recheck

- The decision model is a non-executable deterministic reference; it adds no third-party dependency or discovery side effect.
- Redacted gate output includes only category/path/line/count metadata, never matched content.
- Independent narrow recheck is still required for CR-003, CR-007, and CR-008; the other five findings are closed.
