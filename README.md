# Hercules Skills

Portable Hermes skills for the personal Hercules development workflow.

This workflow treats Hermes as the primary orchestration agent. Hermes gathers context, chooses tools, launches Claude Code for implementation, launches Codex CLI for independent review, verifies real outputs, and reports state back to the user. The skills in this repository encode that workflow as a portable skill group.

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

These two are Superpowers/official-hub style skills, not Hercules-owned custom skills. The bootstrap script can check/install them on a target machine.

## Install on another machine

Install Hermes first using the official Hermes installation flow.

Then clone this repository:

```bash
git clone https://github.com/ZeroTian/hercules-skills.git
```

Copy the skill group into Hermes:

```bash
mkdir -p ~/.hermes/skills/hercules
cp -a hercules-skills/skills/hercules/. ~/.hermes/skills/hercules/
```

Run the bootstrap/dependency doctor:

```bash
bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

For unattended setup after you have authorized installation:

```bash
HERCULES_YES=1 bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

For audit-only mode:

```bash
HERCULES_CHECK_ONLY=1 bash ~/.hermes/skills/hercules/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

The bootstrap script checks and installs where possible:

```text
Claude Code CLI: npm install -g @anthropic-ai/claude-code
Codex CLI: npm install -g @openai/codex
Hermes skills: subagent-driven-development, writing-plans
Claude marketplaces: claude-plugins-official, omc
Claude plugins: superpowers, oh-my-claudecode
```

It does not automate interactive auth. If needed, run:

```bash
claude auth login --console
codex login
```

Start a new Hermes session, then verify:

```bash
hermes skills list | grep hercules
```

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

## User-level rule location

The personal workflow rule belongs in the user's Hermes-level configuration/persona, not in each project repository and not as a fake `HERMES.md` inside this skill group.

For the default Hermes profile, that file is:

```text
~/.hermes/SOUL.md
```

The rule should say, in effect:

```text
Hermes is the main orchestration agent.
Claude Code is the default implementation agent.
Codex CLI is the default independent review/acceptance agent.
Hercules-owned development workflow skills live under ~/.hermes/skills/hercules/ and sync to ZeroTian/hercules-skills.
Builtin Hermes skills stay in the normal Hermes installation.
Third-party/hub skills are dependencies and should be checked/installed, not vendored.
Before launching Claude/Codex, run capability preflight and choose high/xhigh reasoning effort by task complexity.
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
4. Do not vendor third-party or official hub skills into this repo; list them as dependencies and extend bootstrap if needed.
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
