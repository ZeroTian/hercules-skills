# AI Collaboration

This directory records collaboration state for the Hercules skills repository.

It is an index for humans and agents. Long operational rules live in the actor-scoped files at the repository root:

- `HERMES.md` — Hermes orchestration rules
- `CLAUDE.md` — Claude Code execution rules
- `AGENTS.md` — Codex review rules

## Files

- `TASKS.md` — live task ledger and task template (with trajectory record policy)
- `ARCHITECTURE.md` — repository structure and boundaries
- `PROJECT_AUDIT.md` — initialization/audit snapshot with evidence
- `SKILL_GROUP_AUDIT.md` — skill-group redundancy/atomicity audit, composition map, and runnable gaps
- `USABILITY_VALIDATION.md` — practical smoke-test evidence for runtime layout, skill loading, bootstrap audit-only, and real Claude/Codex workflow use
- `codex-reviews/` — stable Codex review records
- `decisions/` — ADR-style durable decisions

## Current workflow

Hermes coordinates work, Claude Code implements substantial changes, and Codex CLI independently reviews review-required work.

README files should stay concise and reader-facing. Detailed rules belong in the files above.
