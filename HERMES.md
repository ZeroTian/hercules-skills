# HERMES.md — Hermes

## Role

Hermes is the controller and runtime host for this repository.

## Non-destructive boundaries

- Inspect repository state first and preserve unrelated user changes.
- Do not install, configure, or authenticate tools, providers, MCP servers, or plugins.
- Do not commit, push, reset, clean, or rewrite history unless explicitly authorized.

## Product invariant

The runtime surface is exactly one runtime Skill: `skills/hercules/SKILL.md`. Keep `hercules` as the single public entry, keep internal workflows under `skills/hercules/references/` without Skill frontmatter, and do not add environment-management behavior.

## Hercules adapter

Hermes is the controller: load the canonical routing contract in [AGENTS.md](AGENTS.md) and Hercules before routing non-trivial project work. Hercules is a Skill workflow, not an assumed CLI: do not synthesize `hercules discover/execute` without confirmed executable and documentation evidence. This restriction does not block Skill/reference loading or direct invocation of confirmed facilities. Do not use `delegate_task` or another Hermes built-in subagent as a substitute for a requested or selected Claude Code or Codex CLI facility.

## Maintainer guidance

Repository orchestration and collaboration guidance lives under [`.maintain/docs/ai-collaboration/`](.maintain/docs/ai-collaboration/).
