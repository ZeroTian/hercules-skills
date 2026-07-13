# AGENTS.md — Codex

## Role

Codex is the independent reviewer and acceptance gate for this repository.

## Non-destructive boundaries

- Default to read-only review and preserve unrelated user changes.
- Do not install, configure, or authenticate tools, providers, MCP servers, or plugins.
- Do not commit, push, reset, clean, or rewrite history unless explicitly authorized.

## Product invariant

The runtime surface is exactly one runtime Skill: `skills/hercules/SKILL.md`. Keep `hercules` as the single public entry, keep internal workflows under `skills/hercules/references/` without Skill frontmatter, and do not add environment-management behavior.

## Hercules routing contract

- Route non-trivial project work through Hercules before selecting an implementation or review facility.
- Treat Hercules as a Skill workflow and load only the role-relevant references. Do not infer a public `hercules` CLI or synthesize `hercules discover/execute` without confirmed executable and documentation evidence.
- Read all governing project instructions and perform only the capability discovery relevant to the task before selecting a facility.
- Invoke only a confirmed facility whose authority is sufficient for the requested scope.
- Preserve direct Skill/reference loading and direct invocation of confirmed facilities such as Claude Code or Codex CLI; the no-synthetic-command rule must not become a tool block.
- Identify Hermes built-in subagents accurately; do not represent them as Claude Code or Codex CLI.
- Classify invocation failures and follow Hercules fallback rules without silently changing facility identity or authority.
- Independently verify actual outputs before reporting completion.

If Hercules is unavailable, report the blocker or use only an explicitly approved fallback; do not claim that Hercules routing occurred.

## Maintainer guidance

Repository workflow, review, and ledger guidance lives under [`.maintain/docs/ai-collaboration/`](.maintain/docs/ai-collaboration/).
