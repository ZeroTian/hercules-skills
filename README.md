# Hercules Skills

Portable Hermes skills for the personal Hercules development workflow.

This workflow treats Hermes as the primary orchestration agent. Hermes gathers context, chooses tools, launches Claude Code for implementation, launches Codex CLI for independent review, verifies real outputs, and reports state back to the user. The skills in this repository encode that workflow as a portable skill group.

Repository:

https://github.com/ZeroTian/hercules-skills

## What is included

Skills are stored under:

```text
skills/
```

Current Hercules-owned skills:

```text
agent-plugin-dependency-governance
coding-agent-orchestration
cross-agent-review-loop
evaluation-closed-loop-orchestration
godot-rl-metric-regression
godot-wsl-artifact-validation
hercules-agent-capability-preflight
hercules-collaborative-agent-workflow
hercules-meta-skill-evolution
hercules-project-init-workflow
hercules-skill-pack-management
hermes-collaborative-workflow
hermes-project-init-orchestration
iterative-agent-code-review
kanban-codex-lane
kanban-orchestrator
kanban-worker
open-ended-research-orchestration
skill-pack-governance-validation
workflow-skill-pack-audit
```

`hercules-skill-pack-management` is the repository-maintenance atom covering layout, runtime symlink, backups, migration, GitHub synchronization, and pre-push privacy checks. `workflow-skill-pack-audit` is the skill-pack audit/reconciliation atom covering skill classification, validator/recheck workflow, ledger trajectory, and Codex reconciliation — it codifies the exact audit pass that produced the current repository state. `skill-pack-governance-validation` is the runtime usability / commit-package / migration acceptance atom covering runtime loading, archived candidate safety, validator/static checks, bootstrap audit-only, staged privacy scan, and commit-package readiness. `agent-plugin-dependency-governance` is the external Claude/Codex/agent plugin dependency atom covering dependency-vs-vendor boundaries, optional bootstrap gating, live sub-capability scanning, and safety-boundary classification. `evaluation-closed-loop-orchestration` is the canonical evaluated-system closed-loop atom that turns telemetry/diagnosis findings into safe modification requests, agent handoffs, structured BLOCKED outcomes, and Claude/Codex review cycles. `godot-wsl-artifact-validation` and `godot-rl-metric-regression` are specialized domain atoms for WSL+Windows Godot artifact proof and baseline-vs-candidate Godot/RL metric regression respectively. The core set is 20 skills after the round-4 promotion, which codifies the practiced usability/commit-package acceptance workflow used to validate commit `97f78ca`.

Eight reviewed candidates — `real-game-closed-loop-validation` (Godot/RL domain validation), `game-mechanics-telemetry-validation` and `game-telemetry-closed-loop-validation` (game mechanic / telemetry validation), `repository-governance-initialization` (governance init pattern, overlaps the existing project-init skills), `scoped-codex-review-packets` (bounded Codex review packets, overlaps the review-loop family), and `artifact-driven-evaluation-loops`, `artifact-handoff-orchestration`, and `autonomous-evaluation-loops` (evaluated-system loop variants that overlap the canonical `evaluation-closed-loop-orchestration` atom after their unique details were folded into it) — were **archived** under `docs/ai-collaboration/candidate-skills/` across these reconciliation passes. They are preserved as reference/case-study material, are not runtime-loaded, and are not part of the core list. See `docs/ai-collaboration/SKILL_GROUP_AUDIT.md` for the full disposition and `docs/ai-collaboration/candidate-skills/README.md` for how to promote one later.

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
cp -a hercules-skills/skills/. ~/.hermes/skills/hercules/
```

For active development on the skill pack, prefer a symlink so the Hermes runtime and Git repository stay in sync:

```bash
ln -sfn /mnt/e/code/hercules-skills/skills ~/.hermes/skills/hercules
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
Claude marketplaces: claude-plugins-official, omc, openai-codex (openai/codex-plugin-cc)
Claude plugins: superpowers, oh-my-claudecode
Optional Claude plugins (HERCULES_INSTALL_OPTIONAL=1): playwright, context7, pyright-lsp, codex@openai-codex
```

The `codex@openai-codex` plugin is the OpenAI `codex-plugin-cc` Claude plugin — an optional in-Claude `/codex:*` command surface, distinct from the Codex CLI. It is not installed by default. See `skills/hercules-agent-capability-preflight/SKILL.md` for its boundary classification and `skills/cross-agent-review-loop/SKILL.md` for how it relates to the independent final Codex review.

It does not automate interactive auth. If needed, run:

```bash
claude auth login --console
codex login
```

Start a new Hermes session, then verify:

```bash
hermes skills list | grep hercules
```

## Validate the skill pack

Run the lightweight validator before skill-pack changes or before handoff to Codex review:

```bash
python3 scripts/validate-skill-pack.py
```

It checks frontmatter and required fields for `skills/*/SKILL.md`, description length, allowed linked directories, README/ARCHITECTURE skill-list consistency, governance file presence, shell-script syntax, and ledger reflection signals (repeated CR IDs, `max-turns`, `blocked/阻塞`, `repair-loop/需修改`, open formal tasks missing a trajectory block, and whether an evidence package should be considered). It exits nonzero only for structural errors. See `docs/ai-collaboration/SKILL_GROUP_AUDIT.md` for the skill-group audit and composition map.

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
2. Copy or symlink them into this repo under `skills/`.
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
