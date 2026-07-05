---
name: cross-agent-review-loop
description: "Iterative Claude-fix → Codex-review loop for thorough code quality assurance"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Claude, Codex, Code-Review, Refactoring, QA, Multi-Agent]
    related_skills: [claude-code, codex]
---

# Cross-Agent Review Loop

Use Claude Code to fix issues and Codex to review the results in iterative rounds until clean. Each agent catches what the other misses, producing higher-quality fixes than either alone.

## When to Use

- Code review findings need fixing (P0/P1 issues from Codex or manual review)
- Multi-round fix → re-review → fix again cycle
- User says "让 Claude 修，修完让 Codex 审核"
- Quality-critical changes (database migrations, security fixes, data-loss risks)

## The Loop Pattern

```
Round 1: Claude fixes issues → Codex reviews → finds new issues
Round 2: Claude fixes new issues (--continue) → Codex reviews → finds more
Round 3: Claude fixes remaining (--continue) → Codex reviews → clean ✓
```

## Step-by-Step

### 0. Ledger Owner Dispatch Gate

Before starting or resuming the loop, inspect the task/CR ledger. Treat `当前负责人` / `下一负责人` / `next_owner` as executable routing: Claude/Codex ownership means Hermes launches that step directly. See `hermes-collaborative-workflow#Owner-Driven Auto-Dispatch` for the full actor matrix. Do not report “next step is Claude/Codex” and stop while the corresponding CLI is available.

### 1. Initial Claude Fix (Print Mode)

```
terminal(
    command="claude -p '<detailed fix instructions with context and line numbers>' --allowedTools 'Read,Edit,Write,Bash' --max-turns 15",
    workdir="/path/to/project",
    background=true,
    notify_on_complete=true,
    timeout=600
)
```

Key: Include exact file paths, line numbers, root cause, and expected fix approach in the prompt. Vague prompts produce vague fixes.

### 2. Codex Review

```
terminal(
    command="codex review --uncommitted",  # for unstaged changes
    # or: command="codex review --base upstream/main",  # for branch diff
    workdir="/path/to/project",
    pty=true,
    background=true,
    notify_on_complete=true,
    timeout=600
)
```

### 3. Analyze Codex Findings

Codex output includes severity levels:
- **P0**: Build-breaking, must fix immediately
- **P1**: Data loss, correctness, or stability risk
- **P2**: Edge cases, nice-to-have

For non-trivial reviews that drive task/CR routing, require a structured JSON footer (verdict, highest_severity, findings, next_owner) so Hermes does not infer state transitions from prose alone. Use the canonical footer shape in `skills/hercules-meta-skill-evolution/templates/codex-review-contract.md`.

Treat the footer as a routing contract, not proof. Hermes must still inspect the diff, tests/logs, and ledger before closing any task or CR.

Only continue if P0 or P1 remain. P2 can be deferred.

### 4. Iterate with --continue

```
terminal(
    command="claude -p '<new issues with exact context>' --continue --allowedTools 'Read,Edit,Write,Bash' --max-turns 12",
    workdir="/path/to/project",
    background=true,
    notify_on_complete=true,
    timeout=600
)
```

`--continue` preserves Claude's context from the previous round so it already knows the codebase and prior changes. This is much more efficient than starting fresh each round.

### 5. Stop Condition and Active Merge

Before calling the loop clean, Hermes performs an active merge/verification pass: diff scope matches the task, required tests/logs exist, task and CR ledgers have no stale `待复核`/unchecked review markers, CR IDs are updated rather than duplicated, and owner/next-owner fields are consistent. Stop only after this evidence is present.

Stop when Codex returns zero P0/P1 findings and Hermes' active merge pass finds no closure blocker. Three rounds is typical; if it goes past 5 rounds, the task may need human re-scoping.

## Codex Pitfalls

### `--base` Argument Ordering

`codex review --base <BRANCH> [PROMPT]` — the prompt (if any) MUST come AFTER `--base`. Running:

```
# WRONG — errors with "cannot be used with '[PROMPT]'"
codex review "some prompt" --base upstream/main

# RIGHT
codex review --base upstream/main
```

If you only need `--base`, omit the prompt entirely — Codex auto-generates review criteria.

### Review Flags

| Flag | When to use |
|------|-------------|
| `--uncommitted` | Review unstaged changes (after Claude edits) |
| `--base <branch>` | Review branch diff against base (after rebase) |
| `--commit <sha>` | Review a specific commit |

## Example: Complete cc-switch Rebase Flow

```
# 1. Git sync
git fetch upstream && git rebase upstream/main

# 2. Resolve conflicts manually (git operations are faster direct)

# 3. Codex reviews the rebase
codex review --base upstream/main → P1 issues found

# 4. Claude fixes P1 issues
claude -p "Fix P1: ..." --allowedTools "Read,Edit,Write,Bash" --max-turns 15

# 5. Re-review
codex review --uncommitted → 2 more P1 issues

# 6. Claude fixes again with --continue
claude -p "Fix new P1: ..." --continue --allowedTools "Read,Edit,Write,Bash" --max-turns 12

# 7. Final review
codex review --uncommitted → clean ✓
```

## When NOT to Use

- Simple one-shot fixes — just use Claude alone
- Git operations (fetch, rebase, merge) — faster to run directly
- Trivial changes (typos, formatting) — overhead not worth it
- Tasks where the agent needs to verify externally (deploy, API call) — add an explicit verification step after the loop

## Rules

1. **Claude for fixes, Codex for review** — each has different blind spots
2. **`--continue` for Claude iterations** — preserves context, saves tokens
3. **Stop when P0/P1 clean** — don't chase P2 indefinitely. Ask user after 5+ rounds whether to continue or defer edge cases.
4. **Include exact context in prompts** — line numbers, file paths, root cause
5. **Background + notify** — these are long-running, don't block the user
6. **Poll Claude progress proactively** — print mode is silent until done. User will get impatient; poll every 2-3 min and report status.
7. **Git operations stay with main agent** — structural conflicts (version collisions, duplicate function names) are faster to resolve directly than through Claude
8. **Do not stop at handoff** — if the ledger says the next actor is Claude or Codex, Hermes launches that actor and monitors it; only user-owned decisions or real blockers pause the loop
