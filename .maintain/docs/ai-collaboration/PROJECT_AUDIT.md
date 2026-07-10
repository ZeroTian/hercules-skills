# Project Audit

Last inspected: 2026-07-05 10:04 CST

## Evidence

Commands run during initialization preview:

```bash
pwd && git rev-parse --show-toplevel && git status --short && git branch --show-current && git remote -v
git ls-files | sort
```

Observed repository root:

```text
/mnt/e/code/hercules-skills
```

Current branch:

```text
main
```

Remote:

```text
origin https://github.com/ZeroTian/hercules-skills.git
```

Observed untracked path:

```text
skills/hercules-skill-pack-management/
```

## Current state

The repository is a Markdown/script skill pack. No `package.json`, `pyproject.toml`, CI YAML, `.gitignore`, `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, or `TASKS.md` was found during preview inspection.

`README.md` already explains the skill-pack purpose, installation flow, bootstrap script, entry skills, user-level rule location, workflow intent, and migration rule.

## Healthy patterns to preserve

- The repository has a flattened `skills/<skill>/` layout.
- README is mostly reader-facing and installation-oriented.
- Builtin Hermes skills are explicitly excluded from the pack.
- External hub skills are treated as dependencies.
- Bootstrap script is colocated with `hercules-agent-capability-preflight`.

## Gaps

- No actor-scoped repository rules for Hermes, Claude Code, or Codex CLI.
- No live task ledger for review-required collaboration work.
- No architecture/boundary document separate from README.
- No stable location for Codex CR records or ADR-style decisions.
- Current untracked `skills/hercules-skill-pack-management/` needs explicit review before being treated as part of the tracked skill pack.

## Initialization decision

This audit is created as part of governance initialization. It does not approve committing, pushing, or adding untracked skill content.
