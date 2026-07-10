# Codex Review Request — TASK-015 Skill-first lightweight architecture

- Date: 2026-07-10
- Scope: initial full-branch review of `df377c0..4742721`, followed by the five-finding repair package
- Requested reviewer: independent Codex agent that did not implement Tasks 1–7
- Initial result: **FAIL** — 5 findings (`Important 3`, `Minor 2`)
- Current result: fixes implemented with focused tests; independent narrow recheck PENDING
- Highest severity: Important
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

## Pre-review acceptance evidence

- Automated tests: `test_init.py` 8/8; `test_runtime_skill_contract.py` 9/9; `test_maintainer_boundary.py` 14/14; `test_validate_skill_pack_cli.py` 20/20.
- Strict validator: 0 errors, 0 warnings, exit 0.
- Syntax/diff: `bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh` and `git diff --check` exit 0.
- Real init smoke: isolated HOME, fake `hermes`, local `HERCULES_REPO_URL`, and failure stubs for forbidden tools; first clone and second fetch/fast-forward both exit 0. The only Hermes runtime entry resolves to the checkout's five-Skill directory, and the checkout remains clean.
- Forbidden behavior scan: no matches for package-manager, marketplace/plugin-install, or Claude/Codex login commands in `init.sh`, `skills`, or `README.md`.
- Public surface scan: exactly five top-level directories under `skills/`; `init.sh` is the only executable root file.
- Cumulative package gate: a disposable source clone was detached at `df377c0`, mirrored from the current worktree, and staged with `GIT_INDEX_FILE=<temp>/cumulative.index` after `git read-tree df377c0`; 125 paths (`1536 insertions`, `5112 deletions`) were checked. `.maintain/scripts/check-package.sh` printed `maintainer package checks passed`, and `git diff --cached --check` exited 0.
- Fresh-clone staged smoke: the verified temporary index was installed only into the disposable source clone's own index, `GIT_INDEX_FILE` was unset, and `.maintain/scripts/smoke-fresh-clone.sh` applied the staged diff to a clone of `df377c0`; strict validation, Bash syntax, and 9 runtime contract tests passed. The real worktree index SHA-256 was identical before and after.

## Initial findings and repair status

The independent full-branch review returned FAIL. The statuses below describe the implementation worker's repair and focused evidence; none is closed until an independent Codex narrow recheck accepts it.

### TASK015-CR-001 — Important — capability-matrix behavior was not tested

- Initial evidence: `.maintain/tests/test_runtime_skill_contract.py` asserted only Skill text and forbidden strings; the nine design scenarios had no task/facility/cache/invocation behavior assertions.
- Repair status: **IMPLEMENTED — PENDING RECHECK**.
- Repair: added nine behavior tests that load the non-executable stdlib contract at `skills/hercules-capability-discovery/references/capability_matrix.py`; each supplies task demand and local facility/cache/invocation evidence and asserts route, fallback, blocker, cache invalidation, deep inspection, and an empty command list. The owning Skill explicitly consumes the same contract.

### TASK015-CR-002 — Important — privacy gate echoed secret-like content

- Initial evidence: `.maintain/scripts/check-package.sh` captured and printed matching added lines verbatim.
- Repair status: **IMPLEMENTED — PENDING RECHECK**.
- Repair: staged added-line scanning now emits only `redacted category`, `path`, `line`, and `count`; sentinel, plus-prefixed, unstaged-only, deletion, and self-scan regressions are covered.

### TASK015-CR-003 — Important — navigation validator did not enforce exact-five rows

- Initial evidence: `check_skill_navigation()` validated row syntax but never compared its row keys with `EXPECTED_RUNTIME_SKILLS` or enforced the single entry role.
- Repair status: **IMPLEMENTED — PENDING RECHECK**.
- Repair: navigation keys must equal `EXPECTED_RUNTIME_SKILLS`; `hercules` must have exactly one `entry/composite` core row and the other four exactly one internal core row. Missing, extra, and wrong-entry fixtures now fail validation.

### TASK015-CR-004 — Minor — prerequisite failures omitted links and non-remediation statement

- Initial evidence: missing Git/Hermes messages referred generically to official instructions and only missing Hermes was tested.
- Repair status: **IMPLEMENTED — PENDING RECHECK**.
- Repair: both messages include a concrete official URL and `Hercules 未安装或修改任何内容`; isolated missing-Git and missing-Hermes tests compare filesystem snapshots and confirm no checkout/runtime mutation.

### TASK015-CR-005 — Minor — public-surface tests used presence-only assertions

- Initial evidence: extra Quickstart commands, another documented `/skill` entry, or another root executable could pass.
- Repair status: **IMPLEMENTED — PENDING RECHECK**.
- Repair: tests parse English and Chinese Quickstart blocks to the same exact three-command tuple, require every public documented `/skill` invocation to be `/skill hercules`, and require the root public executable set to equal `{init.sh}`.

## Focused repair evidence

- TDD RED: capability contract missing produced 9 failures; redacted metadata expectations produced 4 failures; missing/extra/wrong-entry navigation produced 3 failures; Git/Hermes prerequisite UX produced 2 failures. Temporary public-surface mutations produced failures for a fourth command, alternate Skill entry, and extra root executable.
- Focused GREEN: `test_runtime_skill_contract.py` 19/19, `test_maintainer_boundary.py` 19/19, and `test_init.py` 9/9.
- Candidate A remained a non-finding and its experimental zero-Git-metadata implementation/tests were removed from the repair package.

## Full repair-package validation

- `python3 .maintain/tests/test_init.py -v` — 9/9 passed.
- `python3 .maintain/tests/test_runtime_skill_contract.py -v` — 19/19 passed, including the nine capability environments.
- `python3 .maintain/tests/test_maintainer_boundary.py -v` — 19/19 passed.
- `python3 .maintain/tests/test_validate_skill_pack_cli.py -v` — 25/25 passed.
- `python3 .maintain/scripts/validate-skill-pack.py --strict` — 0 errors, 0 warnings, exit 0.
- Bash syntax, forbidden behavior scan, `git diff --check`, `git diff --check df377c0`, exact-five directory scan, and root executable scan passed.
- `.maintain/scripts/check-package.sh` — `maintainer package checks passed`; secret-like fixtures remained absent from its output.
- `.maintain/scripts/smoke-fresh-clone.sh` — strict validation, init syntax, and all 19 runtime contract tests passed in the staged clone.

## Closure gate

Do not mark this review PASS or TASK-015 complete until an independent reviewer has narrowly rechecked `TASK015-CR-001` through `TASK015-CR-005` and the strict/package/fresh-clone checks have been rerun after the final repair ledger update.
