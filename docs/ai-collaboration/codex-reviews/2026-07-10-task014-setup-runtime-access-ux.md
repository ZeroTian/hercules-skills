# Codex Review — TASK-014 setup/runtime access UX

- Date: 2026-07-10
- Scope: TASK-014 setup, doctor, preflight, runtime failure contract, tests, and documentation
- Reviewer: independent Codex agent, read-only
- Current result: PASS
- Initial result: FAIL
- Initial highest severity: P1
- Highest severity after second recheck: none

## Findings and fixes

### TASK014-CR-001 — P1 — dry-run apply command was not reusable

- Location: `scripts/install-hercules.sh`, `print_next_steps()`
- Finding: the fixed local command dropped `--repo-dir`, `--copy`, `--branch`, and skip flags; a piped installer also printed a helper that would not exist on a fresh machine.
- Fix: reconstruct a safely escaped command from the selected options and distinguish an existing checkout from `curl | bash` execution.
- Regression coverage: custom path/branch/copy/skip flags and piped fresh-machine command.
- Recheck: RESOLVED.

### TASK014-CR-002 — P2 — tests did not prove hidden provider probes were absent

- Location: `tests/test_setup_doctor_ux.py`
- Finding: terminal output assertions could pass even if provider commands ran with hidden output.
- Fix: record fake Claude/Codex calls and reject login, plugin, MCP, and feature inventory calls in the default dry-run path.
- Recheck: RESOLVED.

### TASK014-CR-003 — P3 — stale authentication-handoff wording

- Location: `docs/ai-collaboration/ARCHITECTURE.md`, `docs/ai-collaboration/SKILL_GROUP_AUDIT.md`
- Finding: old `auth handoff` wording contradicted the user-managed provider boundary.
- Fix: replace it with provider-neutral runtime failure diagnosis/guidance.
- Recheck: RESOLVED.

### TASK014-CR-004 — P2 — doctor follow-up command targeted the wrong location

- Location: `scripts/install-hercules.sh`, dry-run next steps.
- First recheck finding: the fixed `scripts/hercules doctor` command does not exist in a piped installer's current directory and checks the wrong checkout when `--repo-dir` targets another path.
- Fix: print a safely escaped absolute command at `<repo-dir>/scripts/hercules doctor`.
- Regression coverage: custom path with spaces and piped fresh-machine target.
- Second recheck: RESOLVED.

## Fix verification

- `python3 tests/test_setup_doctor_ux.py -v`: PASS, 5 tests.
- `python3 tests/test_validate_skill_pack_cli.py -v`: PASS, 6 tests.
- Shell syntax checks: PASS.
- `python3 scripts/validate-skill-pack.py --strict`: PASS, 0 errors / 0 warnings.
- `git diff --check`: PASS.
- Actual custom-option dry-run: PASS; emitted a complete, shell-escaped local apply command.
- Actual doctor JSON: `blocked=0`; no provider login check.

## Final verdict

PASS — `TASK014-CR-001` through `TASK014-CR-004` are resolved; no remaining P0-P3 findings.
