# HERMES.md — Hermes Orchestration Rules

## Project identity

This repository is the portable Hercules skill pack for Hermes Agent.

Repository path in the main development workstation:

```text
/mnt/e/code/hercules-skills
```

Public repository:

```text
https://github.com/ZeroTian/hercules-skills
```

## Responsibilities

Hermes is the controller for this repository.

Hermes must:

- inspect repository state before changing files;
- preserve user changes and untracked work;
- keep README reader-facing and avoid duplicating long operational rules there;
- route substantial documentation or workflow implementation work to Claude Code when useful;
- route independent review, acceptance checks, and CR closure to Codex CLI;
- verify agent self-reports with real `git diff`, file reads, and lightweight checks;
- update `docs/ai-collaboration/TASKS.md` when formal collaboration tasks are opened or closed.

Hermes must not:

- commit, push, reset, clean, or rewrite history unless the user explicitly asks;
- vendor Hermes builtin skills into this repository;
- vendor third-party / official hub skills unless they become Hercules-owned custom workflow skills by explicit decision;
- treat generated plans or agent self-reports as completed work without verification.

## Agent orchestration

Before launching Claude Code or Codex CLI for meaningful work, run capability preflight or use a fresh cached inventory for this session.

Default reasoning effort:

```text
normal repository work: high
complex, cross-skill, risky, failed-review, or governance-changing work: xhigh
```

Use Claude Code for:

- adding or updating Hercules-owned skills;
- substantial documentation changes;
- scripts such as bootstrap/check tooling;
- refactors across multiple skill files;
- SDD/TDD tasks where tests or executable checks are relevant.

Use Codex CLI for:

- independent review of uncommitted changes;
- checking governance consistency and checkbox truth;
- validating that README stays reader-facing;
- final acceptance of review-required tasks.

Hermes owns bookkeeping after either agent finishes.

## Validation commands

This repository is Markdown and shell-script heavy. Prefer the bundled validator first, then targeted checks when relevant:

```bash
python3 scripts/validate-skill-pack.py
git status --short
git diff --check
git ls-files | sort
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

`scripts/validate-skill-pack.py` (Python stdlib only) checks frontmatter and required fields for `skills/*/SKILL.md`, description length, allowed linked directories, README/ARCHITECTURE skill-list consistency against git-tracked and visible skill directories, governance file presence, shell-script syntax, and ledger reflection signals (repeated CR IDs, `max-turns`, `blocked/阻塞`, `repair-loop/需修改`, open formal tasks missing a trajectory block, and whether an evidence package should be considered). It exits nonzero only for structural errors; warnings and reflection signals do not fail the run by default.

If a check is not applicable, record why in `docs/ai-collaboration/TASKS.md` or the final report.

## Documentation boundaries

- `README.md`: human overview, install instructions, migration guidance, and navigation.
- `HERMES.md`: Hermes-specific orchestration rules.
- `CLAUDE.md`: Claude Code implementation rules.
- `AGENTS.md`: Codex review rules.
- `docs/ai-collaboration/TASKS.md`: live collaboration ledger.
- `docs/ai-collaboration/ARCHITECTURE.md`: repository structure and ownership boundaries.
- `docs/ai-collaboration/PROJECT_AUDIT.md`: evidence-backed initialization/audit snapshot.
- `docs/ai-collaboration/decisions/`: ADR-style durable decisions.
- `docs/ai-collaboration/codex-reviews/`: stable Codex review records.
