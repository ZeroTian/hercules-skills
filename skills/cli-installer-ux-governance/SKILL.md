---
name: cli-installer-ux-governance
description: "Use when designing or reviewing productized CLI installer UX: setup/doctor/status commands, full/minimal/dry-run modes, read-only diagnosis, repair boundaries, provider-neutral runtime handoff, and independent review checks."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cli, installer, setup, doctor, dry-run, ux, governance, hercules]
    related_skills: [portable-skill-pack-installation, hercules-skill-pack-management, hercules-agent-capability-preflight]
---

# CLI Installer UX Governance

## Overview

Use this skill when turning raw install flags into a productized CLI experience for Hercules/Hermes skill packs or similar developer tools.

The goal is to make installation intuitive without hiding mutations: `setup` guides or runs installation, `doctor` diagnoses, `doctor --fix` repairs, and `status` summarizes. Public docs should lead with user intent (`--full`, `--minimal`, `--dry-run`) while preserving lower-level compatibility flags (`--yes`, `--optional`, `--check`).

## When to Use

Use when:

- adding or reviewing `setup`, `doctor`, `doctor --fix`, `status`, or installer aliases;
- documenting one-command installation for another machine;
- deciding whether a CLI flow is intuitive enough for open-source users;
- checking that dry-run and doctor modes are safe and non-mutating;
- aligning required dependencies, optional plugins, and user-managed provider boundaries.

## Procedure

1. **Start from the user mental model.** Prefer:

   ```bash
   tool setup --full
   tool setup --minimal
   tool setup --dry-run
   tool doctor
   tool doctor --fix
   tool status
   ```

   over raw implementation flags such as `--yes --optional` in public docs.

2. **Keep compatibility aliases.** Preserve existing flags where useful:

   ```text
   --full     ~= --yes --optional
   --minimal  ~= --yes
   --dry-run  ~= --check
   ```

3. **Make doctor read-only by default.** `doctor` and `doctor --json` must not install, pull, clone, write config, write registry settings, create backups, alter symlinks, or write fixed log files. If detailed validation fails, point to a command the user can run rather than writing `/tmp/...` by default.
4. **Put repair behind explicit intent.** `doctor --fix` may perform minimal safe repairs. `doctor --fix --full` may additionally align optional plugin dependencies. Do not install optional plugins from plain `doctor` or minimal repair.
5. **Make dry-run non-interactive.** `--dry-run` / `--check` must skip both side effects and confirmation prompts. On fresh machines, print “would install OS packages/Hermes” and continue; do not prompt `[y/N]`.
6. **Classify final state.** End setup/doctor with a concise dashboard:

   ```text
   OK       satisfied
   WARN     usable but incomplete
   FIXABLE  doctor --fix can repair
   BLOCKED  an observed core setup or runtime operation failed
   ```

7. **Keep provider access outside setup.** Do not inspect, validate, or modify Claude/Codex login state, API keys, gateways, or cloud credentials during setup or doctor. When a real invocation fails, report a sanitized cause and provider-neutral checks.
8. **Expose automation outputs.** Add `doctor --json` for CI/agent automation and `doctor --strict` for release gates.
9. **Review and verify.** Run shell syntax, dry-run smoke against a nonexistent path, JSON validation, package validator, whitespace checks, and independent Codex review.

## Verification Checklist

- [ ] `bash -n` passes for helper, installer, and delegated bootstrap scripts.
- [ ] `setup --dry-run --repo-dir /tmp/<unique>` exits without creating the repo path.
- [ ] `doctor --json` emits valid JSON with top-level `status`, `counts`, and `checks`.
- [ ] Plain `doctor` does not write logs or other artifacts.
- [ ] Dry-run mode does not ask confirmation questions.
- [ ] Optional plugins are gated behind `--full`, `--optional`, or an explicit env flag.
- [ ] Unprobed provider/login state does not appear as `BLOCKED`; only a real failed invocation can create that blocker.
- [ ] README and governance docs use product-level commands and aligned skill/dependency counts.
- [ ] Codex review checks safety, UX mappings, idempotency, docs consistency, executable bits, and no secrets.

## Pitfalls

1. **Doctor that writes temp logs.** Even a fixed `/tmp` validation log violates the “read-only doctor” promise. Keep output in memory or tell users what command to run.
2. **Dry-run that prompts.** Preview mode should be non-interactive; users choose it specifically to avoid changes and decisions.
3. **`--optional` as the public happy path.** It is precise for dependency governance but reads as “not recommended.” Use `--full` in README and keep `--optional` as an advanced alias.
4. **Conflating installation with provider access.** Setup completion covers local components. Provider access remains user-managed and is diagnosed only after a real invocation fails.
5. **Summary hidden in logs.** Always end with a short actionable state and next command.

## References

- `references/setup-doctor-installer-ux.md` — session-derived safety notes for setup/doctor installer UX review.
