# Governance task closure after delegated review

Use this reference when a repository has Markdown task/CR governance and Hermes is orchestrating Claude/Codex rather than implementing directly.

## Pattern

1. Read the task source of truth and any linked review docs before launching a reviewer.
2. Delegate the independent review to Codex in read-only terms. If the service context makes Codex sandboxing fragile, use `codex exec --sandbox danger-full-access` but constrain safety with:
   - explicit `workdir`
   - a prompt that says "do not modify files"
   - narrow file/task scope
   - required verification commands
3. Capture Codex's result and only close tasks/CRs when the report includes concrete PASS evidence.
4. Update every matching governance location, not just the headline task:
   - task checkbox and `当前状态`
   - `当前负责人` / `下一负责人` / `下一步`
   - `最后更新`
   - `验证证据`
   - execution/acceptance checkboxes
   - linked CR top metadata and final review section
5. Re-run lightweight consistency checks after editing:
   - `git diff --check`
   - search for stale markers such as `待复核`, `等待 Codex 独立复核`, unchecked task/CR headings, or unchecked `Codex 已完成复核` in the affected files.
6. Treat old failed review records as history. Do not delete them; append a "再复核"/follow-up record with date, scope, commands, result, and residual risk.
7. If the PASS leaves no active tasks, verify the task table/sections show every real task as `[x]` + `已完成` + owners `无`, then report the finished state directly. Do not ask the user to type another trigger when Hermes has already run the needed delegate and updated the ledger.

## Consistency-check recipe

Use searches that distinguish real task sections from templates. A useful pattern is:

- `rg -n "^## \\[[ x]\\] TASK-|^- 当前状态：|^- 当前负责人：|^- 下一负责人：|^- 下一步：" TASKS.md`
- Inspect the results and ignore the task template section explicitly; do not treat template placeholders as active work.
- For linked CR files, search both headings and top metadata (`CR-`, `当前状态`, `Codex 已完成独立复核`, `最终结论`).

## Pitfalls

- Closing only the main task while leaving linked CRs as `待复核` creates contradictory facts.
- Generic patches can hit duplicate checkbox text; use exact surrounding context or targeted replace operations.
- If a patch fails because the file was read with offset/limit pagination, re-read the whole file before retrying so replacement context is current.
- If the governance file is newly untracked, `git status --short -- <path>` shows `??`; this does not invalidate the closure, but mention it only as repository state, not as a review failure.
- Subagent summaries are not state changes. After Claude says "已交 Codex" or Codex says "建议关闭", Hermes still must patch the authoritative ledger and verify it before finalizing.
