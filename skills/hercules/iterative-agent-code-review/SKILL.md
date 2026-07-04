---
name: iterative-agent-code-review
description: "Iterative fix-review loop: delegate fixes to Claude, review with Codex, repeat until clean."
version: 2.0.0
category: software-development
tags: [claude-code, codex, code-review, iterative, quality]
triggers:
  - "让 claude 修完 codex 审核"
  - "claude fix codex review loop"
  - iterative code review with dual agents
  - fix-review cycle
---

# Iterative Agent Code Review

Run an iterative fix-review loop where Claude Code fixes issues and OpenAI Codex reviews the changes, repeating until the codebase is clean. Each agent catches issues the other misses.

## When to Use

- Fixing multiple code review issues found by Codex or another tool
- Refactoring with quality gates
- Bug fixing where edge cases matter
- Any scenario where you want dual-agent quality assurance

## The Loop

```
┌─────────────────────────────────────────────┐
│  1. Claude fixes issues (print mode)        │
│     claude -p "fix N issues" --continue     │
├─────────────────────────────────────────────┤
│  2. Claude SELF-REVIEWS (includes in prompt)│
│     "修复后自审，再输出总结"                   │
├─────────────────────────────────────────────┤
│  3. Codex reviews uncommitted changes       │
│     codex review --uncommitted              │
├─────────────────────────────────────────────┤
│  4. New issues found? → back to step 1      │
│     Clean?               → DONE             │
└─────────────────────────────────────────────┘
```

The self-review step (2) is critical — it catches obvious errors before Codex sees them, reducing total rounds by 40-50%.

## Commands

### Step 1: Claude Fixes

```bash
cd /path/to/repo && claude -p "修复以下 N 个问题：
问题1 (file:line): root cause + fix approach
问题2 (file:line): root cause + fix approach
确保编译通过。" --allowedTools "Read,Edit,Write,Bash" --max-turns 12 --continue 2>&1
```

- Run in background with `notify_on_complete=true`
- Use `--continue` to preserve context from previous rounds
- Each round's prompt should include specific file paths and line numbers

### Step 2: Codex Reviews

```bash
cd /path/to/repo && codex review --uncommitted 2>&1
```

- Also runs in background with `notify_on_complete=true`
- `--uncommitted` for unstaged changes; `--base upstream/main` for branch-level

### Step 3: Evaluate and Repeat

- Parse Codex output for P0/P1/P2 issues
- P0 = build-breaking, must fix immediately
- P1 = functional/security issues, should fix
- P2 = minor/edge case, optional
- If only P2 or pre-existing issues remain → done
- Otherwise → back to step 1 with new prompt

## Why It Works

**Two complementary mechanisms:**

### 1. Dual-Agent Blind Spots

Claude (Sonnet) and Codex (gpt-5.5) have different blind spots:

| Issue type | Claude tends to miss | Codex catches |
|-----------|---------------------|---------------|
| Path traversal in manifest | ✅ | ✅ |
| SQLite PRAGMA in savepoint semantics | ✅ | ✅ |
| Foreign key cascade during migration | ✅ | ✅ |
| Duplicate function definitions | ✅ | ✅ |
| Windows cross-platform (rename semantics) | ✅ | ✅ |
| Bootstrap heuristics accuracy | ✅ | ✅ |
| Content-level ownership verification | ✅ | ✅ |

### 2. Layer-by-Layer Discovery

Codex can't find ALL issues in one pass because:

- **Attention limits**: gpt-5.5's effective attention covers ~1000 lines of diff per review. Issues in later sections get lower priority.
- **Predecessor blocking**: fix A must happen before issue B becomes visible. Example: duplicate function names block the path traversal review from even reaching that code section.
- **Fix introduces new issues**: Claude's own fixes create new edge cases that didn't exist in the original.

Real 19-round cc-switch experience (2026-07-01, upstream sync + workspace skill refactoring):

```
Rounds 1-2: structural (duplicate fns, missing migrations, version collisions)
Rounds 3-5: logic gaps (manifest ownership, foreign keys, PRAGMA semantics)  
Rounds 6-8: edge cases (Windows rename, orphan recovery, atomic writes)
Rounds 9-12: content verification (copy fallback, broken symlinks, path safety)
Rounds 13-15: error handling (partial writes, orphan adoption, content hashing)
Rounds 16-18: deep verification (recursive byte-comparison, partial-schema repair, subset→equality)
Round 19:     CLEAN — Codex found no actionable regressions
```

Deepest round (16-18) pushed content comparison from filename matching → name subset → byte-for-byte recursive equality. Each escalation was driven by Codex finding a bypass for the previous heuristic.

## Pitfalls

1. **Don't let Claude and Codex run simultaneously** on the same uncommitted changes — Codex may review a partial fix
2. **Print mode output is silent until complete** — `process(action='poll')` shows very little; wait for completion notification
3. **Codex review can take 3-8 minutes** — be patient, it's reading and analyzing the full diff
4. **Stop threshold**: after 3+ rounds with only P2 findings, consider stopping; diminishing returns. But the user may say "继续直到没问题" — honor that.
5. **`--continue` requires same working directory** — Claude finds the most recent session by cwd
6. **Each new round's prompt must be self-contained** — Claude's `--continue` preserves session context but new findings still need to be described explicitly
7. **Codex finds problems layer by layer** — don't expect one pass to catch everything. The first round finds structural issues (duplicate fns, missing migrations); later rounds uncover edge cases (Windows rename, orphan recovery). This is inherent to LLM attention limits, not a failure.
8. **`--base <BRANCH>` conflicts with inline prompt** — `codex review --base main "prompt"` errors. Use `--base main` alone or `--uncommitted` for staged changes.
9. **When user says "用Claude修" — USE CLAUDE**: don't manually git-fetch/rebase/patch. You're the orchestrator, Claude is the worker.
10. **Respect repo-level Claude→Codex governance**: before implementing in a repo with `AGENTS.md` / `CLAUDE.md` / collaboration docs, check whether the project assigns implementation to Claude and review/closure to Codex. If yes, Codex should primarily review/verify and create CRs; do not directly implement business changes unless the user explicitly authorizes an exception. For small governance/doc fixes after explicit approval, record the exception, keep the task in `待复核`, and do not self-close.
11. **Distinguish user-level OMC rules from project-level protocol**: user-level `~/AGENTS.md` may say to delegate code to an executor and keep author/reviewer separate, while project-level files may explicitly name Claude as implementer and Codex as reviewer. Follow the stricter project protocol for that repo, then use user-level rules as the general fallback.
12. **Claude may hit max-turns on heavy implementations** — bump by 3-5 and retry with `--continue`. Content comparison and recursive operations need more turns (we hit `max-turns 10` on content byte-comparison, resolved with `--max-turns 18`).
13. **Cron `deliver: "origin"` breaks across platform switches** — a cron created on WeChat stays on WeChat even after moving to Telegram. Set explicit `deliver: "telegram:<chat_id>"`.
14. **User-driven workflow improvements**: When user says "是不是可以claude自己先做一次cr" — adopt it immediately. They see efficiencies you don't. Self-review before cross-review cut our rounds from 12→8 for equivalent depth.
15. **Content ownership verification is an arms race**: filename matching → name subset → byte-comparison → exact recursive equality. Each heuristic has a bypass until you reach the final form. Jump to the strongest verification first if the task involves file content.

## Real-World Case Study

See `references/cc-switch-19-round-case-study.md` for a complete 19-round Claude+Codex loop on cc-switch workspace skill refactoring and upstream sync, covering: migration version collisions, manifest ownership tracking, path traversal defense, SQLite foreign-key semantics, copy-fallback deployment, broken symlink cleanup, atomic manifest writes, cross-platform rename, orphan recovery, content-level ownership verification (filename→byte-comparison escalation), and partial-schema migration repair.
