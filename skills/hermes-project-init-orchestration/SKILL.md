---
name: hermes-project-init-orchestration
description: "Use when initializing or standardizing repository governance under Hermes control: project init, CLAUDE.md/AGENTS.md, TASKS.md, Claude execution batches, Codex review batches, and automated Hermes-run Claude→Codex loops without making the user switch between tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [project-init, governance, claude-code, codex, orchestration, code-review]
    related_skills: [claude-code, codex, coding-agent-orchestration]
---

# Hermes Project Init Orchestration

## Overview

This skill adapts the Codex-side `project-init` governance contract into a Hermes-first workflow.

For general协同作业, load `hermes-collaborative-workflow` first. This `project-init` skill is the narrower governance-initialization layer for `CLAUDE.md`, `AGENTS.md`, `TASKS.md`, review templates, architecture boundaries, and ADR structure.

The original contract assumes a human switches between Claude and Codex by typing exact trigger phrases. Under Hermes, do **not** make the user bounce between tools. Hermes is the controller:

1. Hermes inspects the repository and prepares the governance preview.
2. Hermes applies only user-approved governance changes.
3. Hermes launches Claude Code for execution work.
4. Hermes launches Codex CLI for independent review.
5. Hermes records task/review state, verifies outputs, and reports the next real state to the user.

The durable files may still contain Claude/Codex rules for portability, but Hermes should execute the loop itself whenever the CLIs are available.

## When to Use

Use this skill when the user asks to:

- Initialize a new or existing repository for Claude × Codex collaboration.
- Add or standardize `CLAUDE.md`, `AGENTS.md`, `docs/ai-collaboration/TASKS.md`, review records, ADRs, or governance docs.
- Convert a manual Claude/Codex handoff process into a Hermes-orchestrated loop.
- Continue a project task batch where Claude should implement and Codex should review.
- Avoid switching between Claude and Codex UIs and have Hermes centrally manage the lifecycle.

Do **not** use this skill for ordinary one-off code edits that do not need durable governance. For simple Claude→Codex fix/review loops, load `coding-agent-orchestration` and run the smaller loop.

## Source Contract Adaptation

This skill is based on the Codex-side `project-init` skill and its `governance-contract.md`:

- Original purpose: inspect → preview → wait for approval → apply durable Claude/Codex governance.
- Original limitation: Markdown handoff tells the user which agent to open next.
- Hermes adaptation: Markdown remains a record, but Hermes actually invokes Claude Code and Codex CLI when possible.

Important conversion rule:

> Replace “提示用户前往 Claude/Codex 并输入触发词” with “Hermes launches the appropriate CLI, monitors it, verifies its output, writes back state, and only asks the user when a real decision or approval is required.”

## Artifact Map and Scope Partition

When a repository needs a governance refactor or a user questions where rules belong, use `references/governance-scope-partition.md` for the detailed placement matrix.

Default governance tree:

```text
.
├── HERMES.md                         # Hermes orchestration rules (controller, CLI routing, ledger updates)
├── CLAUDE.md                         # Claude Code durable execution rules (implementation, SDD/TDD, handoff)
├── AGENTS.md                         # Codex durable review rules (review, CRs, closure)
└── docs/
    └── ai-collaboration/
        ├── README.md                 # Human-readable overview/index only; not a duplicated rulebook
        ├── PROJECT_AUDIT.md          # Evidence-backed snapshot and follow-up risks
        ├── ARCHITECTURE.md           # Directory responsibilities and boundaries
        ├── TASKS.md                  # Live task status source of truth and task templates
        ├── codex-reviews/            # CR-NNN findings and recheck history
        └── decisions/                # ADR-NNN durable decisions
```

Reuse equivalent existing files instead of creating duplicates. Show the mapping in the preview before writing.

Scope rule: keep operational constraints in actor-scoped rule files. `README.md` files should help humans understand and navigate the project; they may summarize workflow and link to rule files, but should not duplicate long Claude/Codex/Hermes obligations, SDD/TDD checklists, trigger protocols, or closure rules.

## Role Model Under Hermes

### Hermes

Hermes owns orchestration:

- Discovers repository context and existing governance.
- Writes or patches files only after scope is approved.
- Calls Claude Code for implementation, refactoring, documentation, and task execution.
- Calls Codex CLI for review, verification, risk analysis, and closure decisions.
- Runs independent local verification where needed.
- Updates `TASKS.md` and review records after tool output is verified.
- Reports a concrete state summary to the user.

### Claude Code

Claude Code is the implementation worker:

- Reads project rules and task context.
- Uses SDD + TDD by default for development work: split into vertical subagent-driven slices, write/verify failing tests first, implement minimal GREEN, then refactor with tests green.
- Uses available Claude Code development plugins such as `superpowers` and `oh-my-claudecode` (OMC) when present; if unavailable, records that fact and follows the same process manually.
- Creates or completes checkbox execution plans.
- Modifies code/docs within the scope Hermes gives it.
- Runs appropriate tests or records why it cannot.
- Writes implementation evidence and hands off for review.

### Codex CLI

Codex is the independent reviewer:

- Reviews code, architecture, dependencies, tests, docs, and risk.
- Checks checkbox truth against repository state and evidence.
- Creates or updates stable `CR-NNN` findings with acceptance criteria.
- Independently verifies resubmissions.
- Closes review-required tasks only after acceptance criteria pass.

## Phase 1 — Inspect Without Mutation

Before changing anything:

1. Locate repository root, nested repos, worktrees, and instruction files.
2. Read likely governance files: `CLAUDE.md`, `AGENTS.md`, `README.md`, contribution docs, architecture docs, task trackers, CI, tests, manifests, `.gitignore`, and `git status`.
3. Infer technology, commands, entry points, directory responsibilities, dependency boundaries, and generated artifacts from evidence.
4. Identify existing equivalents to the default artifact map.
5. Preserve user changes. Do not clean, reset, move, delete, install, commit, or refactor.

Completion criterion: Hermes can name the current governance state, existing files to preserve, missing pieces, conflicts, and proposed artifact mapping without having changed files.

## Phase 2 — Preview and Wait for Approval

For initialization or governance rewrites, present a non-mutating preview and stop for explicit approval.

Preview must include:

1. Project and governance summary.
2. Healthy patterns to preserve.
3. Missing, uncertain, stale, or conflicting rules.
4. Mapping from the default artifact map to existing files.
5. Exact `HERMES.md`, `CLAUDE.md`, and `AGENTS.md` rule additions or diffs.
6. Exact `docs/ai-collaboration/README.md` overview/index changes, kept concise and non-duplicative.
7. Initial checkbox tasks for structural issues; do not fix them during init.
8. Validation plan.
9. SDD + TDD plan: which actor-scoped rule files carry the obligations, how Claude tasks will be split into subagent-driven vertical slices, how RED/GREEN/REFACTOR evidence will be recorded, and whether `superpowers` / `oh-my-claudecode` (OMC) plugins are available.
10. Hermes orchestration plan: when Hermes will call Claude Code and Codex CLI instead of asking the user to switch tools.

State that no files changed. Silence, questions, or vague agreement are not approval.

Exception: if the user has explicitly asked to create a Hermes skill or user-level rule, that request itself is approval for that scoped artifact only.

## Phase 3 — Apply Approved Governance

When approval is explicit:

1. Merge narrowly; never overwrite useful existing instructions.
2. Resolve conflicts only as approved.
3. Create only governance artifacts with defined responsibilities; place rules in `HERMES.md`, `CLAUDE.md`, or `AGENTS.md`, and keep `README.md` files as concise human-facing maps unless the repository has an explicit different convention.
4. Mark uncertain facts as `待验证` rather than pretending certainty.
5. Do not touch business code, reorganize directories, opportunistically clean, commit, or push unless separately requested.
6. Keep all executable plan steps, tasks, subtasks, fixes, acceptance criteria, and review checks as Markdown checkboxes.

Completion criterion: every changed file is in the approved scope, every task/review field is complete, and validation has run or is explicitly marked blocked.

## Phase 4 — Hermes-Driven Execution Batch

When a user asks Hermes to run the collaboration workflow, Hermes should collect and execute eligible Claude-owned tasks itself.

### Batch Collection

Read `docs/ai-collaboration/TASKS.md` and collect tasks where:

- Current owner is `Claude`.
- Status is `待处理`, `处理中`, `需修改`, or an unblocked `阻塞` state.

Sort by:

1. P0 → P1 → P2 → P3.
2. Explicit dependency order.
3. Task number.

Skip tasks owned by the user or blocked on user approval. Continue independent tasks when one task is blocked.

### Launch Claude Code

Use print mode for bounded implementation tasks:

```bash
claude -p '<self-contained task brief>' \
  --allowedTools 'Read,Edit,Write,Bash' \
  --max-turns 15
```

Hermes terminal pattern:

```text
terminal(command="claude -p '<brief>' --allowedTools 'Read,Edit,Write,Bash' --max-turns 15", workdir="/path/to/repo", background=true, notify_on_complete=true, timeout=600)
```

The Claude brief must include:

- Repository path and files/tasks in scope.
- Required files to read first.
- Exact task IDs and CR IDs to handle.
- Allowed and forbidden files/directories.
- Required tests or checks, including TDD RED/GREEN/REFACTOR evidence when behavior changes.
- Required task-record updates for SDD slices, plugin/subagent usage, verification evidence, and handoff state.
- Explicit instruction not to commit, push, reset, or touch unrelated user changes.

Hermes must monitor the process. Do not tell the user to “wait for notification”; poll long jobs and report final output promptly.

### Verify Claude Output

After Claude exits:

1. Check exit code and output for `max turns`, permission errors, or incomplete work.
2. Inspect `git diff --stat` and relevant diffs.
3. Run critical verification commands yourself if Claude’s evidence matters.
4. If Claude changed broad or unexpected files, stop and report before launching Codex.
5. If Claude partially completed work, either resume Claude with a narrower brief or record the blocker.

Completion criterion: Hermes has verified that Claude either submitted the task to `待复核` with evidence or left a clear blocker.

## Phase 5 — Hermes-Driven Codex Review Batch

When tasks are in `待复核`, Hermes launches Codex CLI instead of asking the user to open Codex.

### Batch Collection

Collect tasks where:

- Current owner is `Codex`.
- Status is `待复核`.

Sort by priority, dependency, and task number. Review independent tasks even if one fails.

### Launch Codex CLI

For governance/task review, prefer `codex exec` with a read-only review prompt and a narrow file list. In Hermes gateway/service contexts, use `--sandbox danger-full-access` if Codex sandboxing fails.

Example:

```bash
codex exec --sandbox danger-full-access '<read-only review brief>'
```

Hermes terminal pattern:

```text
terminal(command="codex exec --sandbox danger-full-access '<review brief>'", workdir="/path/to/repo", background=true, pty=true, notify_on_complete=true, timeout=600)
```

Codex review brief must include:

- “Read-only review unless explicitly told otherwise.”
- Task IDs and acceptance criteria.
- Files and diffs in scope.
- Required verification commands.
- How to update `TASKS.md` and `codex-reviews/` if the review passes or fails.
- Rule: update original `CR-NNN`; do not create duplicate issues for the same problem.
- Rule: do not commit, push, reset, or rewrite history.

### Verify Codex Output

After Codex exits:

1. Check exit code and whether the review actually completed.
2. Read modified task/review files if Codex wrote them.
3. Run or inspect key verification evidence where feasible.
4. Confirm checkbox truth: main task `[x]` only when status is `已完成` and review requirements passed.
5. If Codex reports findings but does not write them, Hermes writes or asks Claude/Codex to write the stable `CR-NNN` record.

Completion criterion: every reviewed task is either `已完成`, `需修改`, `阻塞`, or still `待复核` with a clear reason.

## State Machine

Every task and review finding must carry:

```markdown
- 当前负责人：Claude / Codex / 用户 / 无
- 当前状态：待处理 / 处理中 / 阻塞 / 待复核 / 需修改 / 已完成 / 已取消
- 下一负责人：Claude / Codex / 用户 / 无
- 下一步：接收方要执行的具体动作
- 是否需要 Codex 复核：是 / 否
- 最后更新：YYYY-MM-DD HH:mm
- 关联任务：`TASK-NNN` / 无
- 关联审阅：`codex-reviews/YYYY-MM-DD-review-NNN.md` / 暂无
- 验证证据：命令、结果或文件 / 待补充
- 阻塞原因：无 / 具体原因
```

Required transitions:

| Event | Status | Current owner | Next owner | Required action |
|---|---|---|---|---|
| Task starts | `处理中` | Claude | Codex | Execute checklist and collect evidence. |
| Claude submits | `待复核` | Codex | Codex | Review implementation and evidence. |
| Codex rejects | `需修改` | Claude | Codex | Address specific `CR-NNN` acceptance criteria. |
| Claude resubmits | `待复核` | Codex | Codex | Recheck the original finding. |
| Codex accepts | `已完成` | 无 | 无 | Check the main task and record the verdict. |
| Work blocks | `阻塞` | actor who can unblock or 用户 | named actor | Record blocker and exact unblock action. |

On every transition, update status, owner, next owner, next action, timestamp, and evidence together.

## Required Templates

### Task Template

```markdown
## [ ] TASK-001：任务标题

- 当前状态：待处理
- 优先级：P1
- 当前负责人：Claude
- 下一负责人：Codex
- 下一步：完成实现和自检后提交复核
- 是否需要 Codex 复核：是
- 创建日期：YYYY-MM-DD
- 最后更新：YYYY-MM-DD HH:mm
- 来源：用户需求 / 项目初始化 / Codex 审阅
- 关联任务：无
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：无

### 目标

说明可验证的预期结果。

### 执行项

- [ ] 完成必要调研
- [ ] 确认影响范围
- [ ] 拆分 SDD 垂直切片并记录子代理/插件使用计划或不可用原因
- [ ] 按 TDD 写失败测试并记录 RED 结果，或记录不可测试原因与替代验证
- [ ] 完成获批的实现或修改
- [ ] 记录 GREEN 结果并完成必要 REFACTOR
- [ ] 补充或更新测试
- [ ] 更新相关文档
- [ ] 执行验证并记录结果
- [ ] 完成 Claude 自检
- [ ] 完成交接信息
- [ ] 完成 Codex 复核

### 验收标准

- [ ] 需求已经满足
- [ ] SDD/TDD 证据完整且真实
- [ ] 相关验证已经通过
- [ ] 文档与实现一致
- [ ] 没有未说明的遗留风险
- [ ] Codex 已完成复核

### Claude 执行记录

- 修改内容：
- 修改文件：
- 验证命令：
- 验证结果：
- 遗留问题：

### Codex 复核记录

- 复核日期：
- 复核范围：
- 复核结果：
- 遗留风险：
```

### Review Finding Template

```markdown
## [ ] CR-001：问题标题

- 当前状态：需修改
- 优先级：P1
- 当前负责人：Claude
- 下一负责人：Codex
- 下一步：按验收标准修改并重新提交
- 最后更新：YYYY-MM-DD HH:mm
- 关联任务：`TASK-001`
- 位置：`path/to/file`
- 验证证据：待补充
- 阻塞原因：无

### 问题说明

描述可定位的问题。

### 判断依据

列出代码、配置、测试或引用证据。

### 风险与影响

说明实际影响。

### 建议方案

给出可执行建议，不替代 Claude 的方案判断。

### 验收标准

- [ ] 问题已经修复
- [ ] 相关引用已经检查
- [ ] 相关验证已经通过
- [ ] 文档已经同步
- [ ] Claude 已填写处理记录
- [ ] Codex 已完成独立复核

### Claude 处理记录

- 修改内容：
- 修改文件：
- 验证命令：
- 验证结果：
- 未采纳部分及原因：
- 遗留问题：

### Codex 复核记录

- 复核日期：
- 复核范围：
- 复核结果：
- 遗留问题：
- 最终结论：
```

## Exact Shortcut Protocols in Durable Files

Keep exact shortcut protocol sections in `CLAUDE.md` and `AGENTS.md` for portability, but adapt the final handoff wording for Hermes.

### Trigger Rules

Trigger comparison is strict:

- Trim leading and trailing whitespace.
- The entire user message must equal one trigger phrase.
- A phrase inside a quote, code block, example, question, or longer sentence must not trigger execution.

### Claude Durable Trigger Phrases

- `启动 Claude 协作任务执行流程`
- `继续 Claude 协作任务执行流程`

### Codex Durable Trigger Phrases

- `启动 Codex 协作任务复核流程`
- `继续 Codex 协作任务复核流程`

### Hermes Override

When Hermes is present and CLI tools are available, these phrases are user-facing commands to Hermes. Hermes should not simply print “open Claude/Codex”. It should:

1. Load this skill plus `claude-code`, `codex`, and `coding-agent-orchestration` as needed.
2. Read `HERMES.md` when present, plus the task ledger and the actor-specific rule files relevant to the step.
3. Collect the relevant batch.
4. Launch the appropriate CLI.
5. Monitor, verify, update records, and either launch the next phase or report a real blocker.

## Mandatory Next-Step Output Under Hermes

End workflow reports with this shape:

```markdown
## 下一步操作

- 当前结果：本轮批次工作的准确结果，逐项列出完成、待复核、需修改、阻塞或跳过的任务
- Hermes 已执行：已启动/未启动 Claude Code；已启动/未启动 Codex CLI；已运行的验证
- 下一负责人：Hermes / Claude / Codex / 用户 / 无
- 关联任务：`TASK-NNN` / `TASK-NNN`, `TASK-MMM`
- 下一动作：Hermes 将自动继续 / 等待用户决定 / 无
- 说明：如果 Hermes 已实际启动下一代理，不再要求用户切换端；如果没有启动，说明具体原因。
```

If no incomplete collaboration task remains, include:

```text
协作流程已结束，无需启动下一代理。
```

## Architecture Health Rules

Adapt these rules to the actual repository:

- Give every top-level directory one stable responsibility.
- Reuse a suitable existing directory before creating another.
- Separate source, tests, docs, scripts, config, generated output, caches, logs, and artifacts.
- Keep temporary files and generated output out of source directories and version control.
- Search for existing capability before adding a file, module, or abstraction.
- Require a caller, dependency boundary, and verification approach for new modules.
- Create shared modules only for demonstrated reuse.
- Record durable boundary changes as ADRs.
- During initialization, record cleanup opportunities as unchecked tasks; do not perform them opportunistically.

## Validation Checklist

Before reporting initialization or orchestration as complete:

- [ ] Existing instructions were preserved or changed exactly as approved
- [ ] `HERMES.md` exists or an approved equivalent carries Hermes orchestration rules
- [ ] `CLAUDE.md` contains Claude-specific checkbox planning, SDD/TDD, self-check, evidence, and handoff rules
- [ ] `AGENTS.md` contains Codex-specific checkbox truth, independent review, return, and close rules
- [ ] `docs/ai-collaboration/README.md` is a concise human-facing overview/index and does not duplicate long actor rule blocks
- [ ] `TASKS.md` is the live status source of truth or an approved equivalent exists
- [ ] Task and review templates contain owner, status, next owner, next action, timestamp, evidence, and blocker fields
- [ ] Status transitions identify owner, next owner, next action, timestamp, and evidence together
- [ ] Shortcut phrases are exact-match only and batch-oriented
- [ ] Durable handoff text does not falsely claim a CLI was launched
- [ ] Hermes runtime did not ask the user to switch tools when it could launch the CLI itself
- [ ] Claude Code output was inspected before Codex review
- [ ] Codex review was independent of Claude implementation
- [ ] Every modified file is within the approved scope
- [ ] Relevant tests, builds, lint, type checks, or documented manual checks ran
- [ ] Cross-links resolve or are marked `待验证`
- [ ] No business code, directory layout, Git history, or unrelated file was changed during governance init
- [ ] Unresolved conflicts and blocked items remain unchecked and visible

## Common Pitfalls

1. **Leaving the old manual handoff in place.** If Hermes can launch Claude/Codex, do not end by telling the user to open another terminal and type a trigger.
2. **Letting Claude review itself.** Claude may self-check, but Codex must independently review review-required work.
3. **Trusting agent self-reports.** Hermes verifies changed files, status fields, and key commands before reporting success.
4. **Creating duplicate CRs.** Update the original `CR-NNN` for resubmissions of the same issue.
5. **Checking main tasks too early.** A review-required main task is `[x]` only after Codex passes it.
6. **Using single-task shortcuts.** Batch all eligible tasks and continue independent work after blockers.
7. **Overwriting project rules.** Merge narrowly and preserve existing useful instructions.
8. **Conflating Markdown with orchestration.** Updating `TASKS.md` is not the same as launching the next agent. Hermes must either actually launch the tool or state why it did not.
9. **Diffing the whole repository for a governance preview.** When generating a reinitialization preview, diff only the approved governance files (for example, run `git diff --no-index` per target file against a preview directory). Do not diff repo root vs preview root: large binary/generated/unrelated files can enter the patch, cause decode failures, and obscure the actual governance scope.
10. **Putting work rules in README.** README files are for human orientation and navigation. Put durable agent obligations in `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, and task templates; let README link to them rather than duplicating them.
