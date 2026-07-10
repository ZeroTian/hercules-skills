# CLAUDE.md — Claude Code

## Role

Claude Code is the scoped implementation worker for this repository.

## Non-destructive boundaries

- Preserve unrelated user changes and stay within the requested files and behavior.
- Do not install, configure, or authenticate tools, providers, MCP servers, or plugins.
- Do not commit, push, reset, clean, or rewrite history unless explicitly authorized.

## Product invariant

The runtime surface is exactly these five Skills: `hercules`, `hercules-capability-discovery`, `hercules-collaborative-workflow`, `hercules-review-workflow`, and `hercules-project-init`. Keep `hercules` as the single public entry and do not add environment-management behavior.

## Maintainer guidance

Repository implementation and collaboration guidance lives under [`.maintain/docs/ai-collaboration/`](.maintain/docs/ai-collaboration/).
