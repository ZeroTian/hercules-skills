# Codex Review Request — TASK-015 Skill-first lightweight architecture

- Date: 2026-07-10
- Scope: cumulative branch diff from `df377c0` through the acceptance-preparation commit
- Requested reviewer: independent Codex agent that did not implement Tasks 1–7
- Current result: PENDING independent review
- Highest severity: not assessed
- Closure state: TASK-015 remains `待复核`; this file is not a PASS record

## Review contract

Review the complete cumulative package, not only the final documentation commit. Assign stable IDs in the form `TASK015-CR-NNN` for every P0–P3 finding, preserve findings in this record, and append narrow recheck results after fixes.

The independent review must verify:

1. Default runtime contains exactly `hercules`, `hercules-capability-discovery`, `hercules-collaborative-workflow`, `hercules-review-workflow`, and `hercules-project-init`; `hercules` is the single public entry.
2. No initialization or runtime path hides dependency installation, configuration, authentication, provider probing, marketplace calls, or plugin management.
3. Discovery remains demand-led and preserves generic plugin exploration without declaring any plugin or provider required.
4. Missing optional facilities degrade to another confirmed facility or Hermes itself without blocking unrelated work.
5. Maintainer Skills, tests, validators, historical governance, and domain examples cannot be runtime-discovered.
6. Initializer conflict handling preserves real directories, unrelated symlinks/checkouts, wrong branches, and blocked parent paths without mutation.
7. README stays on the bilingual three-step user path and does not expose retired environment-manager commands.
8. Automated tests, cumulative staged privacy checks, and fresh-clone smoke genuinely exercise the package intended for release.

## Fresh acceptance evidence prepared for the reviewer

- Automated tests: `test_init.py` 8/8; `test_runtime_skill_contract.py` 9/9; `test_maintainer_boundary.py` 14/14; `test_validate_skill_pack_cli.py` 20/20.
- Strict validator: 0 errors, 0 warnings, exit 0.
- Syntax/diff: `bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh` and `git diff --check` exit 0.
- Real init smoke: isolated HOME, fake `hermes`, local `HERCULES_REPO_URL`, and failure stubs for forbidden tools; first clone and second fetch/fast-forward both exit 0. The only Hermes runtime entry resolves to the checkout's five-Skill directory, and the checkout remains clean.
- Forbidden behavior scan: no matches for package-manager, marketplace/plugin-install, or Claude/Codex login commands in `init.sh`, `skills`, or `README.md`.
- Public surface scan: exactly five top-level directories under `skills/`; `init.sh` is the only executable root file.
- Cumulative package gate: a disposable source clone was detached at `df377c0`, mirrored from the current worktree, and staged with `GIT_INDEX_FILE=<temp>/cumulative.index` after `git read-tree df377c0`; 125 paths (`1536 insertions`, `5112 deletions`) were checked. `.maintain/scripts/check-package.sh` printed `maintainer package checks passed`, and `git diff --cached --check` exited 0.
- Fresh-clone staged smoke: the verified temporary index was installed only into the disposable source clone's own index, `GIT_INDEX_FILE` was unset, and `.maintain/scripts/smoke-fresh-clone.sh` applied the staged diff to a clone of `df377c0`; strict validation, Bash syntax, and 9 runtime contract tests passed. The real worktree index SHA-256 was identical before and after.

## Findings

PENDING. No independent finding assessment has been performed. The reviewer must add stable `TASK015-CR-NNN` entries here; absence of an entry at request time does not mean PASS.

## Closure gate

Do not mark this review PASS or TASK-015 complete until the independent reviewer has inspected the cumulative diff, every P0–P3 finding is fixed and narrowly rechecked, and strict/package checks have been rerun after the final ledger update.
