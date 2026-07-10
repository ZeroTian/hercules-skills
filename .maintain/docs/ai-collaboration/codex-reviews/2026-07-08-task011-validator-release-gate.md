# Codex Review — TASK-011 validator release gate + fresh-clone smoke

Date: 2026-07-08
Reviewer: Codex CLI (`codex exec`, model `gpt-5.5`, reasoning effort `xhigh`)
Scope: staged TASK-011 package for validator release-gate tooling and fresh-clone smoke.

## Initial review verdict

Verdict: FAIL
Highest severity: P2

Findings:

- `CR-T011-001` P2 — Deep linked-file validation missed normal inline same-skill links such as `See references/foo.md`.
- `CR-T011-002` P2 — `scripts/smoke-fresh-clone.sh` applied unstaged tracked diffs by default, so the smoke could pass because of files outside the staged package.
- `CR-T011-003` P3 — README described validator exit behavior imprecisely after adding `--strict`.

## Hermes fixes

- `scripts/validate-skill-pack.py`: linked-file classifier now validates ordinary same-skill `references/`, `templates/`, `scripts/`, and `assets/` mentions while skipping downstream `scripts/run_tests.sh` examples and repo-qualified paths.
- `tests/test_validate_skill_pack_cli.py`: added regression tests for inline linked references, downstream test-wrapper examples, and staged-only smoke behavior.
- `scripts/smoke-fresh-clone.sh`: defaults to staged-only smoke; including unstaged tracked diffs requires explicit `HERCULES_SMOKE_INCLUDE_UNSTAGED=1`.
- `README.md`: distinguishes default exit behavior from `--strict` warning-as-release-blocking behavior.

Verification after fixes:

- `python3 tests/test_validate_skill_pack_cli.py -v` — PASS, 6 tests.
- `python3 scripts/validate-skill-pack.py` — 0 errors / 0 warnings / 3 reflection signals.
- `python3 scripts/validate-skill-pack.py --json` — machine-parseable JSON.
- `python3 scripts/validate-skill-pack.py --strict` — exit 0.
- `scripts/smoke-fresh-clone.sh` — PASS in temporary clone.
- `scripts/hercules validate` — PASS.
- `scripts/hercules package` — PASS, staged privacy scan ok.
- `git diff --check` and `git diff --cached --check` — PASS.

## Recheck 1 verdict

Verdict: FAIL
Highest severity: P2

Recheck result: `CR-T011-001`, `CR-T011-002`, and `CR-T011-003` were fixed.

New finding:

- `CR-T011-004` P2 — `docs/ai-collaboration/TASKS.md` linked to this review record before the file existed, while the trajectory still said `review_record: "暂无"`.

Hermes fix: create and stage this review record, then synchronize the TASK-011 trajectory `source_pointers.review_record` to this path before a narrow Codex recheck.

## Recheck 2 verdict

Verdict: FAIL
Highest severity: P2

Recheck result: `CR-T011-004` review-record existence and pointer were fixed.

New finding:

- `CR-T011-005` P2 — TASK-011 CR IDs were accidentally attached to TASK-001's trajectory, while TASK-011 still had `cr_ids: []`.

Hermes fix: restore TASK-001 `cr_ids` to `[]` and put `CR-T011-001` through `CR-T011-005` on TASK-011's trajectory.

## Recheck 3 verdict

Verdict: PASS
Highest severity: none

Recheck result: `CR-T011-005` fixed. Codex verified the staged index: TASK-001 trajectory has `cr_ids: []`, TASK-011 trajectory has `CR-T011-001` through `CR-T011-005`, TASK-011 `review_record` points to this file, and this review record includes the CR-T011-005 history and Hermes fix note.

Final verdict: PASS.
