# Codex Review — Hercules setup/doctor UX v2

- Date: 2026-07-09
- Scope: staged installer/setup/doctor UX v2 package
- Reviewer: Codex CLI, read-only
- Result: PASS
- Highest severity after recheck: none

## Staged package

- `scripts/hercules`
  - Adds productized `setup` entry that delegates to `scripts/install-hercules.sh`.
  - Adds dashboard-style `doctor`, `doctor --fix`, `doctor --fix --full`, `doctor --json`, and `doctor --strict`.
  - Uses `OK` / `WARN` / `FIXABLE` / `BLOCKED` status classes.
- `scripts/install-hercules.sh`
  - Adds `--full`, `--minimal`, and `--dry-run` aliases.
  - Preserves `--yes`, `--optional`, and `--check` compatibility.
  - Adds no-argument interactive setup picker when a TTY is available.
- `skills/portable-skill-pack-installation/`
  - Promotes one-command installer / setup / doctor workflow into a reusable runtime skill.
- `skills/cli-installer-ux-governance/`
  - Promotes focused setup/doctor installer UX safety guidance into a reusable runtime skill.
- `README.md`, `ARCHITECTURE.md`, `SKILL_NAVIGATION.md`, `SKILL_GROUP_AUDIT.md`
  - Update public commands and runtime skill inventory to 25 tracked skills.

## Review commands

Initial review:

```bash
codex exec -c model_reasoning_effort="xhigh" --sandbox read-only "$(cat /tmp/hercules_ux_v2_codex_review.md)"
```

Recheck after CR-HIUX-001/002 fixes:

```bash
codex exec -c model_reasoning_effort="xhigh" --sandbox read-only "$(cat /tmp/hercules_ux_v2_codex_recheck.md)"
```

Narrow recheck after CR-HIUX-003 fix:

```bash
codex exec -c model_reasoning_effort="xhigh" --sandbox read-only "$(cat /tmp/hercules_ux_v2_codex_recheck2.md)"
```

## Findings

### CR-HIUX-001 — P1 — `doctor` wrote a fixed temp validation log

- Location: `scripts/hercules`, `check_validator()`
- Initial result: FAIL
- Root cause: plain `scripts/hercules doctor` / `doctor --json` redirected validator output to `/tmp/hercules-doctor-validator.log`, violating the read-only doctor contract.
- Fix: keep validator output in shell memory and report `run: python3 scripts/validate-skill-pack.py --strict` on failure instead of writing a fixed temp log.
- Recheck: PASS

### CR-HIUX-002 — P2 — `--dry-run` could still prompt on fresh machines

- Location: `scripts/install-hercules.sh`, `install_os_basics()` and `install_hermes_if_missing()`
- Initial result: FAIL
- Root cause: `CHECK_ONLY=1` prevented command execution but did not skip pre-command confirmation prompts.
- Fix: return early in check-only mode with `CHECK_ONLY: would ...` logs before confirmation prompts.
- Recheck: PASS

### CR-HIUX-003 — P2 — stale runtime skill count after promoting a second UX skill

- Location: `scripts/hercules`, `EXPECTED_SKILL_COUNT`
- Initial recheck result: FAIL
- Root cause: staged docs and skill tree moved to 25 runtime skills, but `EXPECTED_SKILL_COUNT` remained 24, causing `doctor` / `doctor --json` to warn on `skill count` and `doctor --strict` to fail.
- Fix: update `EXPECTED_SKILL_COUNT=25`.
- Recheck: PASS

## Independent verification evidence

Codex confirmed:

- `bash -n scripts/hercules` passed.
- `bash -n scripts/install-hercules.sh` passed.
- `bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` passed.
- `python3 scripts/validate-skill-pack.py --strict` passed with 0 errors / 0 warnings.
- `git diff --check` passed.
- `git diff --cached --check` passed.
- `scripts/hercules setup --dry-run --repo-dir /tmp/...` exited 0 and did not create the repo path.
- `scripts/hercules package` passed, including staged privacy scan.
- `/tmp/hercules-doctor-validator` pattern is not present in staged installer/helper scripts.
- No staged vendoring, sensitive filename, or token/private-key pattern issues were found.

Codex also observed `scripts/hercules doctor --strict --json` exits nonzero on current local warnings (`worktree` local changes and optional `codex` Claude plugin missing), which is expected strict-mode behavior rather than a package blocker.

## Final verdict

PASS — highest_severity: none.
