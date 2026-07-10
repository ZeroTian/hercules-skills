---
name: portable-skill-pack-installation
description: "Use when making a Hermes/Hercules skill pack installable on another machine: one-command installer modes, setup/doctor UX, dependency alignment, dry-run safety, runtime symlink/copy install, provider-neutral runtime handoff, and validation/review gates."
version: 1.1.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, installation, migration, bootstrap, setup, doctor, skills, dependencies, validation]
    related_skills: [hercules-skill-pack-management, hercules-agent-capability-preflight, skill-pack-governance-validation, staged-commit-package-governance]
---

# Portable Skill Pack Installation

## Overview

Use this skill when the user asks how to install a Hercules/Hermes skill pack on another computer, asks whether installation and dependency setup can be scripted into a one-command flow, or asks to improve installer UX into a `setup` / `doctor` model.

The goal is a safe productized installer with explicit modes: recommended full setup, minimal setup, and audit-only dry run. Do not turn “one-click” into uncontrolled mutation: separate required runtime setup from optional Claude/plugin ecosystem setup, and separate read-only diagnosis from repair.

## When to Use

Use when:

- creating or reviewing `./scripts/install-*.sh` for a skill pack;
- adding `./scripts/hercules setup`, `doctor`, `doctor --fix`, or install aliases;
- documenting fresh-machine setup with `curl ... | bash -s -- ...`;
- aligning Hermes, Claude Code, Codex CLI, npm/pnpm registry, external skills, and optional plugins;
- validating migration/install claims before telling the user another machine can install it;
- ensuring `--dry-run` / `--check` mode is truly audit-only.

## Procedure

1. **Define user-facing modes first.** Prefer product terms in README/help, while preserving lower-level compatibility flags:

   ```bash
   ./scripts/install-hercules.sh --full      # recommended setup, including optional Claude plugins
   ./scripts/install-hercules.sh --minimal   # minimal install, no Claude plugin mutation
   ./scripts/install-hercules.sh --dry-run   # audit-only; no installs/clones/pulls/config/symlink writes
   ```

   Compatibility aliases may remain:

   ```bash
   ./scripts/install-hercules.sh --yes --optional  # same intent as --full
   ./scripts/install-hercules.sh --yes             # same intent as --minimal
   ./scripts/install-hercules.sh --check           # same intent as --dry-run
   ```

2. **Separate setup and doctor.** `setup` may install or mutate when the user selects a mode. `doctor` must be read-only by default and should produce a dashboard summary. `doctor --fix` may call the installer for safe minimal repairs; `doctor --fix --full` may additionally align optional plugins.
3. **Keep dry-run pure.** In `--dry-run` / `--check` mode, never clone, pull, install, write npm/pnpm registry, alter symlinks, create backups, or execute repo-local scripts that would be absent because clone is a no-op. Log the would-run action and return success.
4. **Separate required and optional dependencies.** Required path may align Hermes, repo checkout, runtime skills, Node/npm, Claude Code CLI, Codex CLI, and required external Hermes skills. Claude marketplace/plugin installation must be gated behind `--full`, `--optional`, or `HERCULES_INSTALL_OPTIONAL=1` unless the user explicitly asked for plugin mutation.
5. **Handle runtime installation explicitly.** Prefer symlink for active development (`~/.hermes/skills/hercules -> <repo>/skills`) and copy mode for consumption-only machines. Back up pre-existing non-symlink runtime directories outside `~/.hermes/skills/` to avoid duplicate skill discovery.
6. **Leave provider access user-managed.** Setup and doctor check that Claude/Codex executables exist but do not inspect login state, API keys, gateways, or cloud-provider credentials. Diagnose provider access only after a real invocation fails, then report the sanitized cause and checks without modifying credentials.
7. **End with a dashboard summary.** Installation logs are allowed, but the final output should clearly distinguish `OK`, `WARN`, `FIXABLE`, and `BLOCKED` items and give the next command.
8. **Expose machine-readable checks.** Provide `doctor --json` for CI/agent automation and `doctor --strict` for release gates.
9. **Update reader docs and governance counts together.** If the installer package promotes a new runtime skill, update README, architecture/navigation/audit docs, and search for stale hard-coded skill counts.
10. **Use independent review.** Ask Codex to review installer safety, check-only semantics, optional plugin gating, executable bit, README accuracy, no secrets, and no third-party vendoring.

## Verification Checklist

- [ ] Installer shell syntax passes.
- [ ] Helper shell syntax passes.
- [ ] Bootstrap shell syntax passes.
- [ ] `./scripts/install-hercules.sh --dry-run --repo-dir /tmp/<unique>` exits 0 and does not create the repo path.
- [ ] `./scripts/hercules setup --dry-run --repo-dir /tmp/<unique>` delegates correctly and does not mutate the machine.
- [ ] `./scripts/hercules doctor --json` emits valid JSON with top-level `status`, `counts`, and `checks`.
- [ ] `./scripts/hercules doctor` is read-only unless `--fix` is supplied.
- [ ] Default bootstrap with `HERCULES_CHECK_ONLY=1 HERCULES_INSTALL_OPTIONAL=0` emits no `claude plugins install` and no `claude plugins marketplace add`.
- [ ] Default dry-run emits a concise plan and no plugin/MCP/feature inventory or provider-login checks.
- [ ] `doctor` does not call Claude/Codex login-status commands or classify unprobed provider state as `BLOCKED`.
- [ ] Full dependency alignment is documented as `--full`; minimal install is documented as `--minimal`; audit-only is documented as `--dry-run`.
- [ ] Installer executable bit is staged (`git ls-files -s ./scripts/install-hercules.sh` shows `100755`).
- [ ] Validator, package readiness, whitespace checks, and staged privacy scan pass.
- [ ] Codex review or recheck returns PASS before committing.

## Pitfalls

1. **Dry-run that executes missing files.** If clone is skipped in `--dry-run`, repo-local bootstrap files will not exist. Do not execute them.
2. **Optional plugin drift.** A delegated bootstrap may still install Claude plugins before the outer installer’s optional gate. Recheck the inner script, not just the wrapper.
3. **Executable bit mismatch.** A local script may run during development but be staged as `100644`; fresh clone direct execution then fails.
4. **Stale skill counts.** Adding a packaging/installer skill requires updating not just the primary inventory but later evidence paragraphs and audit summaries.
5. **Treating one login method as mandatory.** Native login, API keys, external gateways, and cloud providers are user choices. Do not probe them during setup/doctor; diagnose only an observed runtime failure.
6. **Ambiguous flag names.** `--optional` is precise for dependency governance but weak for user onboarding. Prefer `--full` in public docs and keep `--optional` as a compatibility/advanced flag.
7. **Doctor with side effects.** A `doctor` command that installs packages without `--fix` breaks user trust. Keep default diagnosis read-only.

## References

- `references/one-command-installer-pattern.md` — concise pattern and verification recipe extracted from the Hercules one-command installer session.
