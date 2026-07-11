# HERMES.md — Hermes

## Role

Hermes is the controller and runtime host for this repository.

## Non-destructive boundaries

- Inspect repository state first and preserve unrelated user changes.
- Do not install, configure, or authenticate tools, providers, MCP servers, or plugins.
- Do not commit, push, reset, clean, or rewrite history unless explicitly authorized.

## Product invariant

The runtime surface is exactly one runtime Skill: `skills/hercules/SKILL.md`. Keep `hercules` as the single public entry, keep internal workflows under `skills/hercules/references/` without Skill frontmatter, and do not add environment-management behavior.

## Maintainer guidance

Repository orchestration and collaboration guidance lives under [`.maintain/docs/ai-collaboration/`](.maintain/docs/ai-collaboration/).
