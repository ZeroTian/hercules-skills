# CLAUDE.md — Claude Code Execution Rules

## Role

Claude Code is the implementation worker for this repository.

Use Claude for substantial edits to skills, scripts, and governance docs. Hermes remains the controller and will verify your output.

## Read first

For repository work, read the relevant files before editing:

- `README.md`
- `HERMES.md`
- `CLAUDE.md`
- `AGENTS.md`
- `docs/ai-collaboration/TASKS.md`
- the target `skills/<skill>/SKILL.md` files and linked `references/`, `templates/`, or `scripts/`

## Scope rules

Do not commit, push, reset, clean, or rewrite history.

Do not vendor Hermes builtin skills such as `claude-code`, `codex`, `hermes-agent`, or `opencode`.

Do not vendor third-party or official hub skills unless the task explicitly asks to turn one into a Hercules-owned custom workflow skill.

Preserve unrelated user changes. If `git status --short` shows unrelated changes, leave them alone and mention them in the handoff.

## SDD + TDD discipline

For behavior-changing work:

- split the task into vertical slices;
- use available `superpowers` and `oh-my-claudecode` capabilities when present;
- write or identify a failing test/check first when feasible;
- record RED, GREEN, and REFACTOR evidence;
- if automated testing is not applicable, record the manual/static check used instead.

For documentation-only work, use the same evidence pattern with static checks such as link checks, `git diff --check`, frontmatter checks, and script syntax checks.

## Skill authoring expectations

Each Hercules-owned skill should have:

- YAML frontmatter with `name`, `description`, `version`, and useful tags/related skills where appropriate;
- clear trigger conditions;
- numbered procedure or workflow steps;
- pitfalls and verification checklist;
- linked files under `references/`, `templates/`, `scripts/`, or `assets/` when the skill needs supporting artifacts.

## Handoff

Before handing back to Hermes, report:

- files changed;
- why each change was in scope;
- verification commands run and exact results;
- remaining risks or blockers;
- whether Codex review is recommended.

If working from `docs/ai-collaboration/TASKS.md`, update the relevant task fields and leave review-required tasks in `待复核` for Codex rather than marking them complete yourself.

## Exact trigger phrases

If the entire user message equals one of these phrases, execute the batch-oriented Claude workflow from `docs/ai-collaboration/TASKS.md`:

```text
启动 Claude 协作任务执行流程
继续 Claude 协作任务执行流程
```

Under Hermes, these phrases are normally handled by Hermes launching Claude Code. If Claude receives them directly, follow this file and the task ledger, then hand off to Hermes/Codex for review.
