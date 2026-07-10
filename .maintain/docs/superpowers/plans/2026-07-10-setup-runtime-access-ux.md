# Setup And Runtime Access UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce concise Hercules setup output and make Claude/Codex authentication completely user-managed until a real invocation fails.

**Architecture:** Keep setup/doctor responsible for local installation health only. Suppress deep capability inventory unless `HERCULES_VERBOSE=1`, remove proactive login-status checks, and encode provider-neutral runtime failure diagnosis in the Hermes collaboration skills.

**Tech Stack:** Bash 3.2-compatible shell scripts, Python 3 stdlib `unittest`, Markdown Hermes skills.

## Global Constraints

- Do not execute or modify Claude/Codex authentication.
- Do not inspect, print, or persist secret values.
- Do not add API probes or token-spending checks.
- Preserve `--full`, `--minimal`, `--dry-run`, and `--check` compatibility.
- Do not commit or push.

---

### Task 1: Setup And Doctor Regression Tests

**Files:**
- Create: `tests/test_setup_doctor_ux.py`

**Interfaces:**
- Consumes: `scripts/hercules setup --dry-run`, `scripts/hercules doctor --json`.
- Produces: black-box regression coverage using temporary fake `claude`, `codex`, and `hermes` executables.

- [ ] Write a dry-run test that expects `Hercules Setup Preview`, `No changes were made`, and no auth/plugin/MCP/feature inventory markers.
- [ ] Write a doctor test that makes native auth-status commands fail but expects no `claude auth`/`codex auth` checks and no auth-derived `blocked` result.
- [ ] Run `python3 tests/test_setup_doctor_ux.py -v`; expect both tests to fail against the current implementation for the intended reasons.

### Task 2: Concise Setup And Provider-neutral Doctor

**Files:**
- Modify: `scripts/install-hercules.sh`
- Modify: `scripts/hercules`
- Modify: `skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`

**Interfaces:**
- Consumes: existing setup modes and `HERCULES_CHECK_ONLY`.
- Produces: `HERCULES_VERBOSE=0|1`, concise preview output, provider-neutral doctor status.

- [ ] Add a dry-run preview header and plan-oriented completion output.
- [ ] In dry-run, summarize dependency bootstrap plans without executing the bootstrap script.
- [ ] Remove installer login instructions and state that provider configuration remains user-managed.
- [ ] Remove `check_auth` from doctor and `report_auth` from bootstrap.
- [ ] Gate `report_capabilities` and `report_plugin_deep_inventory` behind `HERCULES_VERBOSE=1`.
- [ ] Run `python3 tests/test_setup_doctor_ux.py -v`; expect GREEN.

### Task 3: Runtime Failure Diagnosis Contract And Documentation

**Files:**
- Modify: `skills/hermes-collaborative-workflow/SKILL.md`
- Modify: `skills/hercules-collaborative-agent-workflow/SKILL.md`
- Modify: `skills/hercules-agent-capability-preflight/SKILL.md`
- Modify: `skills/portable-skill-pack-installation/SKILL.md`
- Modify: `skills/cli-installer-ux-governance/SKILL.md`
- Modify: `skills/portable-skill-pack-installation/references/one-command-installer-pattern.md`
- Modify: `skills/cli-installer-ux-governance/references/setup-doctor-installer-ux.md`
- Modify: `README.md`
- Modify: `docs/ai-collaboration/TASKS.md`

**Interfaces:**
- Consumes: Claude/Codex process exit code and sanitized stderr observed by Hermes.
- Produces: a common provider-neutral failure-report shape and updated setup documentation.

- [ ] Document that setup/doctor never inspect or change third-party authentication.
- [ ] Add runtime categories for executable, provider/auth rejection, endpoint/network, quota, model/provider, permission, and unknown failures.
- [ ] Require component, operation, sanitized error, likely category, checks, and non-mutation statement in failure reports.
- [ ] Remove stale instructions that classify missing native login as `BLOCKED`.
- [ ] Record the behavior change and RED/GREEN evidence in `TASKS.md`.

### Task 4: Full Verification

**Files:**
- Verify all files above.

**Interfaces:**
- Consumes: completed implementation.
- Produces: executable evidence that UX, validation, and packaging remain healthy.

- [ ] Run `python3 tests/test_setup_doctor_ux.py -v`; expect all tests PASS.
- [ ] Run `python3 tests/test_validate_skill_pack_cli.py -v`; expect all tests PASS.
- [ ] Run `bash -n scripts/hercules scripts/install-hercules.sh skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`; expect exit 0.
- [ ] Run `python3 scripts/validate-skill-pack.py --strict`; expect zero errors and warnings.
- [ ] Run `scripts/hercules setup --dry-run`; expect concise preview with no capability dump or login instructions.
- [ ] Run `scripts/hercules doctor --json`; expect no Claude/Codex auth checks.
- [ ] Run `git diff --check`; expect exit 0.
