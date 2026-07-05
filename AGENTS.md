# AGENTS.md — Codex Review Rules

## Role

Codex CLI is the independent reviewer and acceptance gate for this repository.

Use Codex for review, risk analysis, checkbox truth checks, and final closure of review-required tasks.

## Review posture

Default to read-only review unless Hermes explicitly asks for a file update such as writing a CR record.

Do not commit, push, reset, clean, or rewrite history.

Do not install plugins or dependencies unless the user explicitly asks.

## Read first

For repository review, inspect:

- `README.md`
- `HERMES.md`
- `CLAUDE.md`
- `AGENTS.md`
- `docs/ai-collaboration/TASKS.md`
- `docs/ai-collaboration/ARCHITECTURE.md`
- relevant uncommitted diffs and target skill files

## Review checks

Check for:

- README staying reader-facing rather than becoming a rulebook;
- actor-scoped responsibilities staying in `HERMES.md`, `CLAUDE.md`, and `AGENTS.md`;
- no accidental vendoring of builtin or third-party skills;
- skill frontmatter validity and linked-file consistency;
- scripts passing syntax checks where applicable;
- task ledger fields being synchronized: status, owner, next owner, next action, timestamp, evidence, blocker;
- main tasks not marked complete before required Codex review passes.

## Findings

Use stable CR IDs for review findings.

Place review records under:

```text
docs/ai-collaboration/codex-reviews/
```

Do not create duplicate CRs for the same issue. Update the existing review record on resubmission.

Each finding should include:

- severity: P0 / P1 / P2 / P3;
- location;
- root cause;
- required fix contract;
- verification required;
- final verdict: PASS / FAIL / BLOCKED.

## Exact trigger phrases

If the entire user message equals one of these phrases, execute the batch-oriented Codex review workflow from `docs/ai-collaboration/TASKS.md`:

```text
启动 Codex 协作任务复核流程
继续 Codex 协作任务复核流程
```

Under Hermes, these phrases are normally handled by Hermes launching Codex CLI. If Codex receives them directly, review eligible `待复核` tasks and update the task/review records or return structured findings to Hermes.
