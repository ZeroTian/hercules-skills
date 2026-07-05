---
name: coding-agent-orchestration
description: "Orchestrate Claude Code + Codex CLI in fix→review loops. Covers tool selection, pitfall avoidance, and proactive progress reporting."
version: 1.0.0
tags: [coding-agent, multi-agent, code-review, claude-code, codex, orchestration]
related_skills: [claude-code, codex]
---

# Coding Agent Orchestration

Drive Claude Code and Codex CLI together in coordinated workflows. Each agent has different strengths and CLI quirks — this skill covers when to use which and how to avoid common pitfalls.

## Agent Selection

| Task | Agent | Why |
|------|-------|-----|
| Fix bugs, refactor, add features | Claude Code (`claude -p`) | Stronger reasoning, better at reading code + editing |
| Code review, diff analysis | Codex CLI (`codex review`) | Purpose-built review subcommand, structured output |
| Batch issue fixing | Codex CLI (`codex exec`) | Parallel worktrees, `--yolo`/`--full-auto` modes |
| Multi-turn exploratory work | Claude Code (interactive via tmux) | Conversation continuity, slash commands |

## Core Workflow: Fix → Review Loop

User says "Claude fix this, then Codex review". Follow this pattern.

For repositories with Markdown governance records (`TASKS.md`, CR files, review logs), also use `references/governance-task-closure.md`: after Codex passes, close every linked task/CR metadata field and checkbox, append a follow-up review record instead of deleting old failures, and search for stale `待复核` / unchecked Codex-review markers before reporting completion.

**Role boundary for Hermes:** Hermes is the orchestrator, not a substitute for Claude or Codex. When the user asks for delegated development/review, do not directly implement the fix yourself and then call it a Claude/Codex workflow. Launch Claude Code for implementation work, launch Codex CLI for review/verification, then have Hermes collect outputs, run any necessary verification, update task records, and report. If Hermes must directly edit because the user explicitly authorizes a narrow exception, record that exception and still delegate the review pass to Codex.

**Ledger ownership:** Subagent summaries are not authoritative state changes. After Claude says a task is ready for review or Codex says PASS/FAIL, Hermes must inspect the task ledger and apply the resulting transition itself: close tasks/CRs on PASS, create/update CRs on FAIL, set owners and next steps, run consistency checks, then report. Do not ask the user to trigger another agent if Hermes can run that delegate and finish the ledger update now.

**Owner-driven dispatch:** In a Hermes-managed project, `当前负责人` / `下一负责人` / `next_owner` fields are dispatch triggers — Hermes launches Claude/Codex directly rather than telling the user to run them. See `hermes-collaborative-workflow#Owner-Driven Auto-Dispatch` for the full rule and valid stop-before-dispatch reasons.

### Step 1: Claude fixes (print mode)

```
terminal(command="claude -p '<detailed fix description>' --allowedTools 'Read,Edit,Write,Bash' --max-turns 15",
         workdir="/path/to/project", background=true, notify_on_complete=true, timeout=600)
```

Key flags:
- `-p`: print mode, no interactive dialogs, exits when done
- `--allowedTools`: restrict to what's needed (Read,Edit,Write,Bash for code fixes)
- `--max-turns 15`: generous limit for complex fixes, prevents runaway loops
- `background=true` + `notify_on_complete=true`: non-blocking, auto-notify on finish

### Step 2: POLL PROGRESS — don't wait silently

Print mode output is fully buffered — you see nothing until completion. For tasks taking >3 minutes, the user WILL ask "还没好吗". Avoid this:

```
# After ~3 minutes, poll for basic status
process(action="poll", session_id="<claude_session_id>")

# Report to user: "Claude 还在跑，已运行 X 分钟，读代码中"
```

Do NOT just fire-and-forget. Proactively update the user every 3-5 minutes on long tasks.

### Step 3: Codex reviews Claude's changes

After Claude exits successfully (check `git diff --stat`):

```
terminal(command="codex review --uncommitted", workdir="/path/to/project",
         background=true, pty=true, notify_on_complete=true, timeout=600)
```

For longer `codex exec` review briefs, avoid embedding Markdown directly in a double-quoted shell string when it contains backticks, `$()`, or other shell metacharacters — the shell may execute snippets such as `` `docs/file.md` `` as commands before Codex sees the prompt. Write the prompt to a temp file and pass it safely, for example:

```
write_file('/tmp/codex_review_prompt.md', prompt_text)
terminal(command='codex exec --sandbox danger-full-access "$(cat /tmp/codex_review_prompt.md)"',
         workdir="/path/to/project", background=true, pty=true,
         notify_on_complete=true, timeout=600)
```

**CRITICAL:** Use `--uncommitted` for unstaged changes. Do NOT use:
- `codex review --base upstream/main "some prompt"` — `--base` and `[PROMPT]` are mutually exclusive, Codex will error
- `codex review --base upstream/main` — only for branch-level diff, not unstaged work

### Step 4: Report results

Summarize Codex's findings in the user's language. If P0 issues found (build broken, duplicate functions), fix them immediately — don't wait for user to ask.

### Structured Review Contract

For non-trivial `codex exec` review briefs, ask Codex to include a structured JSON footer (verdict, highest_severity, findings, next_owner) so Hermes does not infer routing from free text. Use the canonical footer shape in `skills/hercules-meta-skill-evolution/templates/codex-review-contract.md` when the review result will drive task/CR state transitions.

Treat the footer as a routing aid, not as proof. Hermes still verifies the diff, tests, and ledger before closing anything.

### Active Merge / Verification Node

Before closing CRs, marking tasks done, or taking any real state-changing action, Hermes must actively recover missing evidence rather than passively summarize agent reports. Check diff scope, required commands/logs, task and CR consistency, stale `待复核` markers, duplicate CR IDs, and owner/next-owner fields. If evidence is missing or low-confidence, route to targeted Claude repair, Codex re-review, or user decision instead of closing optimistically.

## Proactive Progress Reporting Rules

1. **Start with an estimate**: "Claude 开工了，预计 5-10 分钟"
2. **Poll at 3 min intervals**: `process(action="poll", ...)` and update user
3. **Never go silent >5 min**: if no update, user will ping "还没好吗"
4. **On completion, immediately**: show what changed (`git diff --stat`), summarize findings
5. **Chain automatically**: after Claude finishes, start Codex review without waiting for user approval
6. **Dispatch ledger owners**: after setting `下一负责人` to Claude or Codex, immediately launch the matching CLI or record a blocker; owner assignment alone is not a completed turn

## Codex Review — Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `codex review --base main "review this"` | `codex review --base main` | `--base` rejects `[PROMPT]` |
| `codex review` (no args) | `codex review --uncommitted` | Without args Codex may not know what to review |
| Not using `pty=true` | Always `pty=true` | Codex hangs without PTY |
| Forgetting `notify_on_complete` | Always set it for background | Otherwise you never know it finished |

## Claude Code Print Mode — Pitfalls

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Output fully buffered | No progress visible for 5-10 min | Poll `process(action="poll")` every 3 min, report status |
| `--max-turns` too low | Claude may exit `Error: Reached max turns` even after already writing useful/complete changes | Do not treat max-turns exit as automatic rollback/failure. Immediately inspect the allowed-file diff, read task records, and run the required verification. If changes satisfy scope and tests pass, complete the orchestration/hand-off yourself and report that Claude hit the turn cap after making edits. Use 15-20 for complex fixes, 5-10 for simple ones |
| Missing `--allowedTools` | Claude uses WebSearch/WebFetch unnecessarily | Always restrict: `'Read,Edit,Write,Bash'` for code fixes |
| First run in directory slow | Trust dialog, CLAUDE.md loading | Accept overhead, warn user if >30s startup |

### Handling Partial/Turn-Capped Claude Runs

When `claude -p` exits non-zero due to `max turns` or budget after a long run:
1. Capture the process output and note the termination reason.
2. Inspect the actual diff for the files Claude was allowed to touch; do not assume no work happened.
3. Run the same verification commands the task required (tests, syntax checks, `git diff --check`, targeted searches).
4. If verification passes and the task records are consistent, finish the hand-off in Hermes' orchestrator role rather than re-running Claude blindly.
5. If verification exposes gaps, either run a narrow follow-up Claude prompt focused on the missing items or patch the task status as blocked/needs modification with evidence.

### Codex FAIL → Claude Fix → Codex Re-review Loop

When Codex rejects a task after tests pass, preserve the review record and run a narrow repair loop instead of starting a new broad implementation task:

1. Read Codex's review file and task ledger, then identify exact CR IDs/findings (for example `CR-006`, `CR-007`).
2. Update the main task to `需修改`, owner `Claude`, next owner `Codex`, and record the CR IDs plus failing acceptance criteria.
3. Launch Claude with a **CR-only** brief: fix only the listed findings, add failing regression tests first, update the original review file with a handling note, and do not mark the main task `[x]`.
4. If Claude hits `max turns` after changing files, inspect the actual diff and run the CR-specific tests yourself. If the fix is complete, Hermes may update the ledger back to `待复核` and owner `Codex` with real verification evidence.
5. Re-run Codex on the same review file. On PASS, close the CR checkboxes/metadata and then close the main task; on FAIL, append to the same CR/review record instead of creating duplicates.

This preserves the audit trail while still letting Hermes finish bookkeeping when an implementation agent times out after producing valid code.

## Quick Reference: Flag Cheat Sheet

### Claude Code (`claude -p`)
```
claude -p "<task>" \
  --allowedTools 'Read,Edit,Write,Bash' \
  --max-turns 15 \
  --output-format text   # default, good for Hermes
```

### Codex CLI (`codex`)
```
codex exec "<task>" --full-auto     # feature work
codex review --uncommitted          # review unstaged
codex review --base upstream/main   # review branch diff
```
