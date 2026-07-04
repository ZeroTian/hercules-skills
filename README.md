# Hercules Skills

Portable Hermes skills for Hercules-style development workflow orchestration.

This repository contains local, non-builtin Hermes skills that encode the Hercules development workflow: Hermes as orchestrator, Claude Code as implementer, Codex as independent reviewer, capability preflight before delegation, and project governance conventions for collaborative AI development.

Repository:

https://github.com/ZeroTian/hercules-skills

## What is included

Skills are stored under:

```text
skills/hercules/
```

Current Hercules-owned skills:

```text
coding-agent-orchestration
cross-agent-review-loop
hercules-agent-capability-preflight
hercules-collaborative-agent-workflow
hercules-project-init-workflow
hermes-collaborative-workflow
hermes-project-init-orchestration
iterative-agent-code-review
kanban-codex-lane
kanban-orchestrator
kanban-worker
open-ended-research-orchestration
```

## What is not included

Hermes builtin skills are intentionally not copied here. Use the target machine's own Hermes installation for them:

```text
claude-code
codex
hermes-agent
opencode
```

Third-party or official hub skills are also intentionally not vendored here unless they become Hercules-owned custom workflow skills.

Known external workflow dependencies:

```text
subagent-driven-development
writing-plans
```

These two are Superpowers/official-hub style skills, not Hercules-owned custom skills. Install them separately on a target machine if the target Hermes installation does not already provide them.

## Install on another machine

Clone the repository:

```bash
git clone https://github.com/ZeroTian/hercules-skills.git
```

Copy the skill group into Hermes:

```bash
mkdir -p ~/.hermes/skills/hercules
cp -a hercules-skills/skills/hercules/. ~/.hermes/skills/hercules/
```

Start a new Hermes session, then verify:

```bash
hermes skills list | grep hercules
```

If dependencies are missing, install them from the skills hub or another trusted source rather than copying them into this repository as Hercules-owned skills.

## Main entry skills

For project initialization or repository governance setup:

```text
/skill hercules-project-init-workflow
```

For collaborative development with Hermes + Claude Code + Codex:

```text
/skill hercules-collaborative-agent-workflow
```

For capability scanning and reasoning-effort selection before launching Claude/Codex:

```text
/skill hercules-agent-capability-preflight
```

## Workflow intent

The Hercules workflow prefers this split:

```text
Hermes: orchestrates, gathers context, launches agents, verifies output, updates task state
Claude Code: implements code/docs/refactors using SDD + TDD where appropriate
Codex CLI: performs independent review, CR, risk checks, and final acceptance
```

Before delegating substantial work, Hermes should scan the live Claude/Codex capabilities, including available plugins, MCP servers, agents, and features, then choose reasoning effort:

```text
default: high
complex or high-risk: xhigh
```

## Migration rule

When adding new Hercules-specific development workflow skills:

1. Put them under `~/.hermes/skills/hercules/` locally.
2. Copy them into this repo under `skills/hercules/`.
3. Do not copy Hermes builtin skills into this repo.
4. Do not vendor third-party or official hub skills into this repo; list them as dependencies instead.
5. Do not vendor broad general-purpose skills unless they are part of the Hercules workflow contract and have been customized for that contract.

## Current possible future candidates

A local scan found these non-builtin skills that may be related to development workflow but are not currently included:

```text
software-development/chrome-cdp-automation
software-development/debugging-hermes-tui-commands
software-development/hermes-s6-container-supervision
software-development/tauri-build
```

They were not added automatically because they are tool-specific or project/domain-specific rather than core Hercules orchestration skills.

Other scanned skills such as Telegram formatting, webhook subscriptions, MCP utilities, ML/MLOps, and image generation are useful but are not core development workflow skills for this repository.
