# Relationship to project-init

`hermes-collaborative-workflow` is the general operating skill.

Use it for any collaborative work where Hermes decides whether to:

- handle the task directly,
- delegate implementation to Claude Code,
- delegate review/CR/verification to Codex CLI.

`hermes-project-init-orchestration` is narrower. Use it when the work specifically initializes or rewrites durable repository governance such as `CLAUDE.md`, `AGENTS.md`, `TASKS.md`, review templates, architecture docs, or ADR structure.

Common pattern:

1. Load `hermes-collaborative-workflow` first for actor selection.
2. If the task is repository governance initialization, also load `hermes-project-init-orchestration`.
3. If code implementation is needed, load/use `claude-code`.
4. If review is needed, load/use `codex`.
