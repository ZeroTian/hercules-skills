---
name: hermes-collaborative-workflow
description: "Use when Hermes should centrally orchestrate collaborative work: handle simple/non-code tasks directly, delegate coding/docs/refactors to Claude Code, send CR/review/verification to Codex CLI, and manage the full loop without making the user switch tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [orchestration, collaboration, claude-code, codex, code-review, workflow]
    related_skills: [claude-code, codex, coding-agent-orchestration, hermes-project-init-orchestration]
---

# Hermes Collaborative Workflow

## Overview

Use this skill when Hermes should be the single controller for a task instead of asking the user to move between Hermes, Claude Code, and Codex.

Hermes chooses the right actor for each part:

1. **Hermes handles directly**: simple, non-code, low-risk, informational, planning, routing, bookkeeping, formatting, status updates, and small file edits where delegation would add overhead.
2. **Claude Code executes**: coding, docs implementation, refactors, bug fixes, test writing, project setup, multi-file edits, or tasks that benefit from Claude Code skills/plugins and codebase navigation.
3. **Codex CLI reviews**: CR, code review, risk analysis, diff inspection, acceptance verification, checkbox truth checks, and final closure of review-required work.
4. **Hermes verifies and records**: Hermes inspects outputs, runs key checks, updates task/review state, and reports a concrete result.

The user should not have to manually switch to Claude or Codex when Hermes can launch those tools.

## When to Use

Use this skill when the user asks for:

- “协同作业”, “由 Hermes 统一管控”, “不要让我切 Claude/Codex”.
- A project task that may include coding plus review.
- A Claude implementation followed by Codex CR/review.
- A batch of tasks from `TASKS.md` or an equivalent tracker.
- Project governance initialization or standardization; for that, also load `hermes-project-init-orchestration`.
- Any workflow where actor selection matters: Hermes vs Claude Code vs Codex CLI.

Do **not** delegate automatically when the work is trivial and Hermes can finish it safely with built-in tools.

## Actor Selection Matrix

| Work type | Default actor | Why |
|---|---|---|
| Answering status, summarizing files, finding current task state | Hermes | Fast, grounded by tools, no extra agent overhead |
| Simple non-code edits, formatting, small docs tweaks | Hermes | Direct patch is lower overhead; still verify |
| Planning, task decomposition, checkbox bookkeeping | Hermes | Hermes owns orchestration and state |
| Open-ended online research across papers/blogs/videos/repos | Hermes source collection → Claude synthesis → Codex review | Hermes preserves verifiable sources, Claude is better for broad synthesis, Codex is better for adversarial checking |
| Code implementation, bug fixes, refactors | Claude Code | Strong coding agent with codebase skills/plugins |
| Tests, docs implementation tied to code, project setup | Claude Code | Benefits from repo navigation and iterative edits |
| Code review, CR, risk analysis, diff inspection | Codex CLI | Independent reviewer, separate from implementer |
| Final acceptance for review-required tasks | Codex CLI + Hermes verification | Codex decides review result; Hermes checks records |
| User decisions, scope expansion, destructive ops | User | Requires authority, not agent discretion |

Rule of thumb:

- **If it is simple and low-risk, Hermes does it.**
- **If it changes real code or substantial docs, Claude does it.**
- **If it judges code or closes a review-required task, Codex checks it.**
- **Hermes never blindly trusts either agent’s self-report.**

## Hermes Direct-Work Rules

Hermes may directly complete work when all are true:

- The task is small, local, and low-risk.
- The required context can be gathered with Hermes tools.
- The edit or action does not require broad codebase reasoning.
- Verification is straightforward.
- The user did not explicitly require Claude/Codex execution.

Examples:

- Read `TASKS.md` and summarize current progress.
- Patch a typo in a Markdown task record.
- Create or update a Hermes skill from an explicitly approved request.
- Run tests, `git diff`, `git status`, or other verification commands.
- Update bookkeeping after verified Claude/Codex output.

When Hermes works directly, it still follows repository rules: read first, patch with tools, verify, and do not commit/push/reset unless asked.

## Claude Code Delegation Rules

Delegate to Claude Code when work involves coding or substantial implementation:

- Multi-file code changes.
- Bug fixes or refactors.
- Test writing/updating.
- Docs that must stay synchronized with implementation.
- Project setup or generated governance artifacts with many cross-links.
- Any task where Claude Code’s skills/plugins materially improve execution.

For development work, the Claude brief must require **SDD + TDD** by default: split the task into subagent-driven vertical slices, use available `superpowers` and `oh-my-claudecode` (OMC) plugins when present, write and run failing tests first, implement minimal GREEN, refactor only after GREEN, and record RED/GREEN/REFACTOR evidence in the task ledger.

Use `claude -p` for bounded tasks:

```bash
claude -p '<self-contained task brief>' \
  --allowedTools 'Read,Edit,Write,Bash' \
  --max-turns 15
```

Hermes terminal pattern:

```text
terminal(command="claude -p '<brief>' --allowedTools 'Read,Edit,Write,Bash' --max-turns 15", workdir="/path/to/repo", background=true, notify_on_complete=true, timeout=600)
```

A good Claude brief includes:

- Task ID / CR ID / user goal.
- Files and directories in scope.
- Files to read first.
- Allowed and forbidden changes.
- Required tests or checks, including the exact RED/GREEN/REFACTOR evidence expected when behavior changes.
- Required task-record updates for SDD slices, plugin/subagent usage or unavailable-plugin fallback, verification evidence, and handoff state.
- “Do not commit, push, reset, or touch unrelated user changes.”

Hermes must monitor the background process and inspect its output. If Claude hits `max turns`, permission errors, or incomplete work, Hermes either resumes with a narrower brief or records the blocker.

## Codex Review Rules

Use Codex CLI for independent review and CR work:

- Review uncommitted diffs.
- Check architecture, tests, dependency, security, and maintainability risk.
- Verify acceptance criteria and checkbox truth.
- Create or update `CR-NNN` findings.
- Decide whether a review-required task can close.

Preferred command in Hermes service contexts:

```bash
codex exec --sandbox danger-full-access '<read-only review brief>'
```

Hermes terminal pattern:

```text
terminal(command="codex exec --sandbox danger-full-access '<review brief>'", workdir="/path/to/repo", background=true, pty=true, notify_on_complete=true, timeout=600)
```

A good Codex brief includes:

- “Read-only review unless explicitly told otherwise.”
- The task/CR IDs and acceptance criteria.
- The files/diffs in scope.
- Verification commands to run.
- What should happen on pass/fail.
- Rule to update the original `CR-NNN`, not duplicate issues.
- Rule not to commit, push, reset, or rewrite history.

Hermes then verifies Codex output: exit code, review completeness, task/review file changes, checkbox truth, and key command evidence.

## Open-Ended Research Delegation

For broad online research across papers, blogs, videos, repositories, or competing technical approaches:

1. **Hermes builds the source packet**: gather real URLs, titles, dates when available, source type, relevance, key takeaway, and confidence. Use the appropriate research skills/tools and verify that cited sources exist.
2. **Claude synthesizes**: ask Claude to compare approaches, map findings to the current project, define non-goals, identify risks, and draft an implementation proposal or plan.
3. **Codex reviews adversarially**: ask Codex to check whether sources support the claims, whether the proposal overreaches, and whether it conflicts with repo specs, code, tests, or governance.
4. **Hermes records**: write validated results to `docs/research/`, `TASKS.md`, or the relevant project docs only after scope and uncertainties are explicit.

Do not use Codex as the first broad researcher when the desired output is product/architecture direction; use Codex after there is a proposal or source packet to challenge.

## End-to-End Loop

For collaborative tasks, run this loop:

1. **Gather context**
   - Read `HERMES.md` when present, actor-specific rule files (`CLAUDE.md` for Claude work, `AGENTS.md` for Codex review), and the task state.
   - Treat README files as human-facing maps unless the repository explicitly makes one the rulebook; do not infer hidden operational rules from README prose when actor-scoped files exist.
   - Identify owner, status, scope, acceptance criteria, and blockers.
   - Decide actor using the matrix.

2. **Execute or delegate**
   - Hermes handles simple/non-code work directly.
   - Claude Code handles code/substantial implementation.
   - Hermes monitors and verifies before proceeding.

3. **Review when needed**
   - If code, architecture, dependency, config, build, tests, or review-required docs changed, launch Codex.
   - If Codex rejects, route back to Claude with the original `CR-NNN`.
   - If Codex passes, Hermes records closure.

4. **Verify and record**
   - Run relevant tests/build/lint/static checks yourself where feasible.
   - Update `TASKS.md`, CR records, or equivalent trackers.
   - Keep main tasks unchecked until Codex passes when review is required.

5. **Report real state**
   - Say what Hermes did directly.
   - Say whether Claude Code was launched and what it returned.
   - Say whether Codex CLI was launched and what it concluded.
   - State blockers or next user decisions only when real.

## Batch Handling

When using a task tracker such as `docs/ai-collaboration/TASKS.md`:

- Collect all eligible tasks for the relevant actor.
- Sort P0 → P1 → P2 → P3, then dependency order, then task number.
- Do not stop the whole batch because one independent task fails.
- Skip tasks blocked on the user and continue independent work.
- Keep all task state changes synchronized: status, owner, next owner, next step, timestamp, evidence, blocker.

Review-required main tasks are `[x]` only after Codex passes them.

## Required Final Report Shape

End with a concise state report:

```markdown
## 下一步操作

- 当前结果：逐项列出完成、待复核、需修改、阻塞或跳过的任务
- Hermes 已执行：直接处理了什么；是否启动 Claude Code；是否启动 Codex CLI；运行了哪些验证
- 下一负责人：Hermes / Claude / Codex / 用户 / 无
- 关联任务：`TASK-NNN` / `TASK-NNN`, `TASK-MMM` / 无
- 下一动作：Hermes 将自动继续 / 等待用户决定 / 无
- 说明：如果没有启动某个代理，说明原因；不要让用户切端，除非 Hermes 无法启动对应工具。
```

If nothing remains:

```text
协作流程已结束，无需启动下一代理。
```

## Common Pitfalls

1. **Over-delegating simple work.** Do not start Claude for a small status summary or one-line bookkeeping patch.
2. **Under-delegating code work.** Do not personally implement substantial code when Claude Code is available and the user expects agent orchestration.
3. **Skipping Codex.** Code changes and CR closure need independent review unless the user explicitly waives it.
4. **Trusting self-reports.** Hermes must inspect diffs, records, and key verification output.
5. **Making the user switch tools.** If Hermes can launch Claude/Codex, do it and report the result.
6. **Duplicating rules into README.** Keep user-facing README files concise; put Hermes/Claude/Codex obligations in `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, and task templates.
7. **Duplicate CRs.** Update the original review item for the same issue.
8. **Premature `[x]`.** Main review-required tasks close only after Codex passes.
9. **Silent background jobs.** Poll long-running processes and promptly report final output.

## Verification Checklist

- [ ] Actor selection is justified by task type and risk
- [ ] Hermes handled simple/non-code work directly where appropriate
- [ ] Claude Code was used for substantial implementation/code work when available
- [ ] Codex CLI independently reviewed review-required work
- [ ] Hermes inspected agent output instead of trusting it blindly
- [ ] Relevant tests/build/lint/static checks ran or blockers are recorded
- [ ] Task/CR state is synchronized and checkbox truth is preserved
- [ ] User is not asked to switch tools unless Hermes cannot launch them
