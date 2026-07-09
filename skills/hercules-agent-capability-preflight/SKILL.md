---
name: hercules-agent-capability-preflight
description: "Use before delegating work to Claude Code or Codex CLI when Hermes should scan live skills/plugins/MCP/features and choose reasoning effort by task complexity."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, claude-code, codex, orchestration, mcp, plugins, effort, delegation]
    related_skills: [claude-code, codex, hermes-collaborative-workflow]
---

# Hercules Agent Capability Preflight

## Overview

Use this skill before Hermes delegates meaningful work to Claude Code or Codex CLI. It keeps Hermes from treating those agents as generic black boxes: first ensure the portable Hercules workflow dependencies exist, then scan what each agent can actually use right now, then write briefs that exploit available skills, plugins, MCP servers, custom agents, and reasoning controls.

This is a user-portable Hercules skill. It intentionally lives outside bundled Hermes skill categories so it can be copied to other projects or machines without carrying official skills such as `claude-code`, `codex`, `hermes-agent`, or `opencode`.

## When to Use

Use when:

- Launching Claude Code for substantial implementation, refactor, debugging, docs synchronization, or SDD/TDD work.
- Launching Codex for code review, architecture review, CR closure, adversarial research review, or safety/gate validation.
- The task may benefit from MCP, plugins, browser/Godot/design tools, custom agents, or specialized skill packs.
- The agent environment may have changed since the last run.
- The task is complex enough that reasoning effort should be selected deliberately.

Skip or use a cached result when:

- The task is a tiny one-line edit or status query.
- Capability inventory was already run in this session and no agent config changed.
- The agent will not be launched.

## Step 0 — Bootstrap / Dependency Doctor

On a fresh machine, or whenever Claude/Codex/plugins/skills may be missing, run the bundled bootstrap script before normal preflight:

```bash
bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

For unattended install on a machine where the user has authorized setup:

```bash
HERCULES_YES=1 bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

For audit-only mode:

```bash
HERCULES_CHECK_ONLY=1 bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

The script checks and installs where possible. Claude plugin marketplace/plugin installation is gated behind `HERCULES_INSTALL_OPTIONAL=1` so audit/minimal setup does not mutate Claude plugin state:

| Component | Check | Install / remediation |
|---|---|---|
| Claude Code CLI | `claude --version` | `npm install -g @anthropic-ai/claude-code` |
| Codex CLI | `codex --version` | `npm install -g @openai/codex` |
| Hercules external skills | `hermes skills list` | `hermes skills install official/software-development/subagent-driven-development` and `hermes skills install skills-sh/obra/superpowers/writing-plans` |
| Claude official plugin marketplace | `claude plugins marketplace list` | `claude plugins marketplace add anthropics/claude-plugins-official` — only with `HERCULES_INSTALL_OPTIONAL=1` |
| OMC marketplace | `claude plugins marketplace list` | `claude plugins marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode.git` — only with `HERCULES_INSTALL_OPTIONAL=1` |
| OpenAI codex-plugin-cc marketplace | `claude plugins marketplace list` | `claude plugins marketplace add openai/codex-plugin-cc` (registers as `openai-codex`) — only with `HERCULES_INSTALL_OPTIONAL=1` |
| Claude `superpowers` plugin | `claude plugins list` | `claude plugins install --scope user superpowers@claude-plugins-official` — only with `HERCULES_INSTALL_OPTIONAL=1` |
| Claude OMC plugin | `claude plugins list` | `claude plugins install --scope user oh-my-claudecode@omc` — only with `HERCULES_INSTALL_OPTIONAL=1` |
| Claude `codex` plugin (optional) | `claude plugins list` | `claude plugins install --scope user codex@openai-codex` — only with `HERCULES_INSTALL_OPTIONAL=1` |

It does **not** automate interactive auth. If auth is missing, it reports the required commands:

```bash
claude auth login --console
codex login
```

Claude plugin installation, including `superpowers`, `oh-my-claudecode`, `playwright`, `context7`, `pyright-lsp`, and the OpenAI `codex` Claude plugin (`codex@openai-codex`, from the `openai/codex-plugin-cc` marketplace) can be installed by running with:

```bash
HERCULES_YES=1 HERCULES_INSTALL_OPTIONAL=1 bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

The `codex` Claude plugin is **not** the Codex CLI. It is an optional in-Claude plugin that exposes `/codex:*` slash commands and a `codex:codex-rescue` agent. It is never installed by default. When present, the bootstrap deep inventory lists its `/codex:*` commands and reports whether `agents/codex-rescue.md` is available.

Completion criterion: `claude`, `codex`, required Hermes skills, and any explicitly requested Claude plugins are present or the script has reported a real blocker such as missing Node/npm or missing auth.

## Step 1 — Classify Task Complexity

Pick the lowest level that fits:

| Level | Signs | Claude effort | Codex effort |
|---|---|---|---|
| Simple | One file, mechanical edit, no architecture risk | `--effort medium` | `-c model_reasoning_effort="medium"` |
| Normal default | Regular implementation/review, tests needed, limited subsystem span | `--effort high` | `-c model_reasoning_effort="high"` |
| Complex / high-risk | Multi-subsystem change, SDD/TDD task orchestration, root-cause debugging, safety gates, real external execution, failed prior review | `--effort xhigh` | `-c model_reasoning_effort="xhigh"` |
| Exceptional | Ambiguous root cause, safety-critical design, unusually high uncertainty | `--effort max` if supported, or add `ultrathink` | highest supported configured effort |

Default for formal repo work: `high`.

Escalate to `xhigh` when any of these are true:

- The task spans multiple subsystems.
- It changes safety boundaries, rollback logic, CI/build, auth, data integrity, or evaluation gates.
- It involves real external execution such as browser/Godot/game/server runs.
- A prior Claude/Hermes/Codex attempt failed or produced CR findings.
- The brief asks for adversarial review or architecture-level judgment.

Record the selected effort in `TASKS.md`, a CR record, or the final report for formal tasks.

## Step 2 — Scan Claude Code Capabilities

Run when Claude Code will be used and the current session lacks a fresh inventory:

```bash
claude --version
claude auth status --text || true
claude mcp list || true
claude plugins list || claude plugin list || true
claude agents || true
```

Capture:

- Version and auth state.
- Enabled plugins, especially `superpowers`, `oh-my-claudecode`, `playwright`, `context7`, `pyright-lsp`, `frontend-design`, `skill-creator`, and the optional OpenAI `codex` Claude plugin (`codex@openai-codex`, distinct from the Codex CLI).
- Connected MCP servers, especially project-specific ones like `godot`, browser/playwright, design, video, database, GitHub, or custom MCPs.
- Custom agents if listed or configured.
- Plugin-internal capability surfaces when relevant, not just the plugin name. For OMC this includes bundled commands/skills such as `omc-teams`, team bridge/MCP files, and agent prompts; for Superpowers this includes bundled skills such as `using-superpowers`, `test-driven-development`, `subagent-driven-development`, `dispatching-parallel-agents`, `verification-before-completion`, `requesting-code-review`, and `using-git-worktrees`; for the OpenAI `codex` Claude plugin this includes the `/codex:*` slash commands (e.g. `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:transfer`, `/codex:status`, `/codex:result`, `/codex:cancel`, `/codex:setup`) and the `codex:codex-rescue` agent. Inspect the plugin cache at `~/.claude/plugins/cache/openai-codex/codex` and name the exact command/agent in the brief. Report the stop-review-gate status only when the user has explicitly enabled or is monitoring it; it is off by default.
- Warnings that change capability, e.g. Claude connectors disabled because API key auth takes precedence over Claude.ai login.

Do not ask Claude to use a capability that was not found.

Do not treat “plugin installed” as proof that every sub-capability is available. For task-critical features, inspect the plugin cache or command/skill files and name the exact capability in the brief. Example: if OMC is installed and `skills/omc-teams/SKILL.md` or the `omc-teams` compatibility command is present, the brief may ask Claude to use OMC team orchestration; otherwise say OMC is installed but team capability was not confirmed.

Do not use `--bare` for tasks that should use plugins, MCP, hooks, CLAUDE.md, or project settings. `--bare` intentionally disables much of the capability surface.

## Step 3 — Scan Codex Capabilities

Run when Codex will be used and the current session lacks a fresh inventory:

```bash
codex --version
codex login status || true
codex mcp list || true
codex plugin list || true
codex features list || true
```

When reasoning effort, model, sandbox, or MCP availability matters, also inspect non-secret config snippets:

```bash
sed -n '1,220p' ~/.codex/config.toml
```

Capture:

- Version and login state.
- Current model and `model_reasoning_effort` from config.
- Enabled MCP servers such as `godot`, `google-search`, `sequentialthinking`, `node_repl`, `video-watcher`, `aseprite`.
- Feature flags that matter to the task, such as browser/computer-use capabilities.
- Installed plugins only. Marketplace entries marked `not installed` are options, not capabilities.

Do not install new Codex plugins unless the user explicitly asks.

## Step 4 — Capability Boundary Classification

Before writing the agent brief, separate capabilities into two classes:

| Capability class | Examples | How to use in briefs |
|---|---|---|
| Read/acquisition | Read files, search docs, browser/Playwright inspection, MCP list/read calls, static analysis | Safe for discovery, evidence gathering, and verification. Missing read capability usually means gather context another way before delegating. |
| State-changing execution | Edit/write files, package install, server control, browser form submission, deploy, booking/purchase/API mutation, git push/commit | Only allow when the task requires it and the user/repo rules permit it. Require preconditions, rollback/verification, and explicit scope. |

Do not give one agent both acquisition and state-changing authority when the task naturally crosses a safety boundary. Prefer a split: one actor gathers/selects options with structured output, then a separate scoped actor performs the state-changing step after Hermes verifies current context.

OpenAI `codex` Claude plugin boundary classification (when installed):

| Plugin surface | Class | Rule |
|---|---|---|
| `/codex:review`, `/codex:adversarial-review` | Read-only | Safe as an inline/preliminary review channel inside Claude Code. Does not replace Hermes-owned independent final Codex review. |
| `/codex:rescue` | State-changing / write-capable by default | Requires explicit Hermes/user authorization before use. Treat as write-capable unless the brief explicitly requests a read-only rescue. |
| Stop-review-gate | Off by default | Do not enable by default. Only use when explicitly requested and user-monitored; an enabled stop gate can create long-running or costly review loops. |

Completion criterion: the brief states which capabilities are read-only, which are allowed to mutate state, and which are forbidden.

## Step 5 — Write Capability-Aware Briefs

Include a compact capability section in the agent prompt.

Claude example:

```text
Capability inventory: Claude Code has superpowers + oh-my-claudecode + playwright + godot MCP available. OMC team capability was confirmed via `omc-teams`/team skill files; Superpowers skills confirmed include test-driven-development, subagent-driven-development, dispatching-parallel-agents, and verification-before-completion. Use OMC team orchestration for multi-lane implementation when it reduces coordination risk; use Superpowers SDD/TDD/verification skills for development discipline; use godot MCP only for Godot inspection tasks. Record if any capability is unavailable at runtime.
Reasoning effort: xhigh because this task spans Godot runtime, Python harness, tests, and safety gates.
```

Codex example:

```text
Capability inventory: Codex has MCP servers godot, google-search, sequentialthinking, node_repl, video-watcher, and aseprite enabled. Use only relevant MCPs; do not install plugins. Marketplace plugins marked not installed are not available.
Reasoning effort: xhigh because this is final safety/gate review after a failed implementation attempt.
```

## Step 6 — Launch with Selected Effort

Claude print-mode pattern:

```bash
claude -p "$(cat /tmp/brief.md)" \
  --effort high \
  --allowedTools 'Read,Edit,Write,Bash' \
  --max-turns 20
```

Claude complex task pattern:

```bash
claude -p "$(cat /tmp/brief.md)" \
  --effort xhigh \
  --allowedTools 'Read,Edit,Write,Bash' \
  --max-turns 30
```

Codex review pattern:

```bash
codex exec \
  -c model_reasoning_effort="high" \
  --sandbox danger-full-access \
  "$(cat /tmp/review.md)"
```

Codex complex review pattern:

```bash
codex exec \
  -c model_reasoning_effort="xhigh" \
  --sandbox danger-full-access \
  "$(cat /tmp/review.md)"
```

Keep the usual safety rules:

- Set `workdir` explicitly.
- Use background + notify for long-running bounded tasks.
- Do not allow commit/push/reset unless user explicitly requested it.
- Hermes verifies output and diff; do not trust self-report.

## Step 7 — Cache and Report

For the current Hermes session, treat capability inventory as cached unless:

- `claude` / `codex` was updated.
- MCP/plugin config changed.
- A launch failed due to missing capability.
- The user asks to rescan.

For formal tasks, record:

```text
Agent capability preflight: Claude vX / Codex vY scanned; relevant plugins/MCP: ...
Reasoning effort: high|xhigh because ...
```

## Migration Pattern

This skill is part of the user's portable Hercules workflow pack:

```text
https://github.com/ZeroTian/hercules-skills
```

To reuse this workflow on another machine:

1. Install Hermes normally.
2. Clone or copy this repository's `skills/` directory into `~/.hermes/skills/hercules/`.
3. Run the bootstrap script above to install/check Claude Code, Codex, required Claude plugins, and external skill dependencies.
4. Start a fresh Hermes session and load it by name: `hercules-agent-capability-preflight`.

Migration guarantee boundary: the bootstrap/dependency doctor is a best-effort declared-dependency and live-capability scanner, not an omniscient proof that every transitive plugin feature, per-project MCP server, credential, external binary, OS package, or interactive auth state exists. A target machine is only “ready” after both dependency checks and task-specific executable smoke tests pass. Missing auth, broken MCP servers, optional plugins, project-local tools, private credentials, and plugin-internal feature changes must be reported as blockers rather than papered over.

Keep bundled Hermes skills unmodified and outside this pack:

```text
claude-code
codex
hermes-agent
opencode
```

Do not rely on model memory to reconstruct this workflow on a new host. The target agent must read the actual `SKILL.md` files from `~/.hermes/skills/hercules/`.

## Common Pitfalls

1. **Editing bundled skills directly.** Upstream updates may overwrite changes or create drift. Put personal orchestration policy here instead.
2. **Placing personal skills under official categories.** It works, but makes migration noisy. Prefer the `hercules/` namespace for user-specific skills.
3. **Mistaking marketplace plugins for installed capability.** Codex `plugin list` shows many `not installed` entries. Only enabled/installed tools count.
4. **Confusing plugin presence with sub-capability readiness.** `oh-my-claudecode` being enabled does not by itself prove team orchestration is usable; `superpowers` being enabled does not by itself prove the task-relevant skill was considered. Inspect and name the sub-capability when it matters.
5. **Using `--bare` accidentally.** Claude `--bare` skips plugin/MCP/project context discovery. Avoid it when capability use matters.
6. **Always using xhigh.** High is the default. Escalate only when risk/complexity justifies the cost and latency.
7. **Stale capability assumptions.** Re-scan after upgrades, config changes, plugin updates, migration, or capability-related failures.
8. **Brief bloat.** Include only capabilities relevant to the task; do not paste full inventories into every prompt.
9. **Overclaiming migration readiness.** A fresh host cannot be certified by static scans alone. Run the bootstrap doctor, then run the actual workflow smoke test for the intended task class.
10. **Mistaking the Claude-side `codex` plugin review for Hermes final review.** `/codex:review` and `/codex:adversarial-review` run inside Claude Code as an inline/preliminary channel. They do not replace the Hermes-owned independent final Codex CLI review/acceptance pass. Always run the independent Codex review before closing review-required work.
11. **Enabling the stop-review-gate by default.** The `codex` plugin stop gate is off by default. Enabling it can create long-running or costly review loops. Only enable it when explicitly requested and user-monitored.
12. **Treating `/codex:rescue` as read-only.** `/codex:rescue` defaults to write-capable. Require explicit Hermes/user authorization and a scoped brief before invoking it; prefer a read-only rescue when only diagnosis is needed.

## Verification Checklist

- [ ] Task complexity classified as simple/default/complex/exceptional
- [ ] Claude/Codex capability inventory scanned or explicitly reused from current-session cache
- [ ] Prompt mentions only capabilities that actually exist
- [ ] Task-critical plugin sub-capabilities were confirmed by command/skill/MCP evidence, not inferred from plugin presence alone
- [ ] Effort selected and justified
- [ ] Launch command includes the selected effort flag/config
- [ ] Agent output verified by Hermes with real diff/test/log evidence
- [ ] Formal task/CR records include capability and effort notes when relevant
