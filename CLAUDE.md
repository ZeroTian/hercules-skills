# CLAUDE.md — Claude Code

## Role

Claude Code is the scoped implementation worker for this repository.

## Non-destructive boundaries

- Preserve unrelated user changes and stay within the requested files and behavior.
- Do not install, configure, or authenticate tools, providers, MCP servers, or plugins.
- Do not commit, push, reset, clean, or rewrite history unless explicitly authorized.

## Product invariant

The runtime surface is exactly one runtime Skill: `skills/hercules/SKILL.md`. Keep `hercules` as the single public entry, keep internal workflows under `skills/hercules/references/` without Skill frontmatter, and do not add environment-management behavior.

## Hercules adapter

Follow the canonical Hercules routing contract in [AGENTS.md](AGENTS.md) while retaining the Claude Code-specific implementation boundaries in this file.

## Maintainer guidance

Repository implementation and collaboration guidance lives under [`.maintain/docs/ai-collaboration/`](.maintain/docs/ai-collaboration/).
