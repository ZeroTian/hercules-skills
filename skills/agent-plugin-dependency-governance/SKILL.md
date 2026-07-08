---
name: agent-plugin-dependency-governance
description: "Use when evaluating or adding external Claude/Codex/agent plugins to a Hercules workflow: decide dependency-vs-vendor boundaries, bootstrap optional installs, scan live sub-capabilities, classify safety boundaries, run the standard external-absorption workflow with a recorded decision, and require independent review."
version: 1.1.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, plugins, dependencies, claude-code, codex, governance, bootstrap, absorption]
    related_skills: [hercules-agent-capability-preflight, cross-agent-review-loop, hercules-skill-pack-management, open-ended-research-orchestration]
---

# Agent Plugin Dependency Governance

## Overview

Use this skill when the user asks whether an external agent plugin, marketplace package, or workflow extension should be absorbed into the Hercules skill pack.

The default target shape is **dependency + Hercules-owned governance policy**, not vendored upstream code. The Hercules skill pack should keep class-level policy, bootstrap checks, capability inventory, safety boundaries, and review gates; upstream plugin source stays upstream unless the user explicitly decides to fork or create a Hercules-owned derivative.

## When to Use

Use when evaluating or adding:

- Claude Code plugins or marketplaces.
- Codex plugins or app-server helpers.
- Agent bridge plugins that expose slash commands, subagents, MCPs, hooks, or task delegation.
- Optional development workflow plugins that need bootstrap support.

Do not use for ordinary library dependencies inside an application project; use the project's dependency management workflow instead.

## Procedure

1. **Research the upstream package.** Capture marketplace name, plugin name, install commands, license, command/agent surfaces, hooks, and runtime requirements.
2. **Decide the boundary.** Prefer:
   - upstream plugin as external dependency;
   - Hercules skill updates for policy and orchestration;
   - concise `references/` note for session-specific research.
3. **Do not vendor by default.** Do not copy upstream commands, agents, hooks, scripts, prompts, or internal skills into Hercules unless the user explicitly approves a Hercules-owned fork/derivative.
4. **Add bootstrap only behind the right gate.** Installing a plugin that can spend tokens or mutate state should be optional, for example under `HERCULES_INSTALL_OPTIONAL=1`; detection and marketplace registration may be separate from installation.
5. **Scan live sub-capabilities.** Do not treat “plugin installed” as enough. Inspect plugin cache/manifest/commands/agents/MCPs and brief only the confirmed surfaces.
6. **Classify boundaries.** Separate read-only review/acquisition commands from state-changing write/delegation commands and hooks.
7. **Preserve Hermes review authority.** Inline reviews from inside Claude Code are preliminary and same-context; they do not replace Hermes-orchestrated independent Codex review when a task requires review.
8. **Verify non-mutating audit modes.** If a bootstrap has check-only/audit-only mode, prove it does not write config or install packages.
9. **Record the decision.** Update the relevant class-level skills and task ledger; add a concise research reference when the upstream details are likely reusable.

## Standard External Absorption Workflow

Use this explicit workflow when the request is “research this external repo/plugin and decide whether/how to absorb it into Hercules”. It turns the Procedure above into a repeatable, reviewable loop. The output is a filled `templates/external-absorption-decision.md`.

1. **Frame the absorption question.** State the candidate, the Hercules need it would serve, and explicit non-goals. Separate “absorb as dependency” from “absorb as vendored derivative” up front; vendoring is not the default.
2. **Capture upstream identity.** Record repository URL, package/marketplace name(s), plugin name(s), install command(s), version/commit, license, and maintainer. Verify repository name, marketplace name, and plugin name separately because they can differ.
3. **Inspect live surfaces.** Read the upstream README/manifest and, when installed, the local plugin cache. List command, agent, hook, MCP, and script **names** only. Do not copy upstream prompts, commands, agents, hooks, scripts, or internal files into Hercules.
4. **Classify safety boundaries.** For each surface, mark read-only / state-changing / token-spending / context-migration. Default rescue/delegate/fix surfaces to state-changing unless proven read-only.
5. **Decide dependency-vs-vendor.** Default to dependency + Hercules-owned policy. Vendoring requires explicit user approval of a Hercules-owned fork/derivative; record the reason.
6. **Decide bootstrap/default-install policy.** Detection and marketplace registration may be default. Installation of token-spending or state-changing plugins must be gated, for example under `HERCULES_INSTALL_OPTIONAL=1`. Audit-only mode must be proven non-mutating.
7. **Record governance boundary.** State which Hercules skill owns the policy, that any inline in-Claude review is preliminary and same-context, and that Hermes-orchestrated independent Codex review remains the final gate for review-required work.
8. **Collect validation evidence.** Run the repo-level validator (`python3 ./scripts/validate-skill-pack.py --strict`), `git diff --check`, the bootstrap audit-only proof, and any live cache scan. Paste exact output or link logs; do not paraphrase.
9. **Route to Codex review.** Hand the filled decision template to Codex for accuracy, boundary, and overclaim checks. Record CR IDs and the verdict in the template and task ledger.
10. **Record residual risks / non-goals.** State what is explicitly untested (for example no fresh-machine install, no push) and what is out of scope.

When only a research note is needed and no runtime skill change is proposed, a lighter record under `docs/ai-collaboration/` (modeled on `CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md`) is acceptable; it must still cover the Required Decision Output Fields below.

## Required Decision Output Fields

Every absorption decision must produce a record with these fields. Use `templates/external-absorption-decision.md` so the fields stay consistent.

- **Upstream identity** - repository, package, marketplace/plugin names, version/commit, license.
- **Dependency-vs-vendor decision** - dependency / vendor / partial, with reason.
- **Surfaces and safety classification** - each command/agent/hook/MCP marked read-only / state-changing / token-spending / context-migration.
- **Bootstrap / default-install policy** - detection vs install gating, gate flag, audit-only proof.
- **Governance boundary** - owning Hercules skill, inline-review-is-preliminary, Hermes final review authority.
- **Validation evidence** - exact commands and output (validator, `git diff --check`, audit-only proof, cache scan).
- **Codex review record** - CR IDs, verdict, fixes applied.
- **Residual risks / non-goals** - what is untested or explicitly out of scope.

## Boundary Classification Template

| Surface | Boundary | Default rule |
|---|---|---|
| Read-only review command | acquisition / preliminary review | May be used for inline feedback; cannot close review-required work alone. |
| Adversarial/challenge review command | acquisition / preliminary review | Useful before final handoff; still same-context unless launched independently by Hermes. |
| Rescue/fix/delegate command | state-changing unless proven otherwise | Requires explicit Hermes/user authorization and scoped brief. Prefer read-only for diagnosis. |
| Hook/gate | state-changing control flow / token-spending loop | Disabled by default. Enable only with explicit request and monitoring. |
| Session transfer/import | context migration | Verify source restrictions and avoid leaking secrets/transcripts outside intended tool. |

## Check-only / Audit-only Pitfall

A check-only mode that writes package-manager config is not audit-only. Guard global or user-level writes behind the check-only flag and log what would happen instead.

Example mutation proof:

```bash
before=$(npm config get registry 2>/dev/null || true)
NPM_REGISTRY=https://example.invalid HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh >/tmp/hercules-checkonly.log 2>&1
after=$(npm config get registry 2>/dev/null || true)
printf 'before=%s\nafter=%s\n' "$before" "$after"
grep -E 'CHECK_ONLY: would set (npm|pnpm) registry' /tmp/hercules-checkonly.log
```

Expected: `before` and `after` match, and the log contains `would set` lines instead of performing writes.

## Case Study: OpenAI codex-plugin-cc

`openai/codex-plugin-cc` should be absorbed as an optional external Claude Code plugin dependency, not vendored source. A filled research record lives at `docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md`; record new decisions with `templates/external-absorption-decision.md`.

Key policy:

- Marketplace: `openai-codex`; plugin: `codex`; install as `codex@openai-codex`.
- Install only behind an explicit optional gate such as `HERCULES_INSTALL_OPTIONAL=1`.
- Scan `~/.claude/plugins/cache/openai-codex/codex` for `/codex:*` commands and `agents/codex-rescue.md`.
- `/codex:review` and `/codex:adversarial-review` are preliminary read-only review channels.
- `/codex:rescue` / `codex:codex-rescue` is write-capable by default and needs explicit authorization.
- stop-review-gate is disabled by default; enabling it can create long-running or costly loops.
- Hermes-owned final independent Codex review remains required for review-required tasks.

## Common Pitfalls

1. **Vendor drift.** Copying upstream plugin internals into the skill pack creates stale forks and violates the dependency boundary.
2. **Marketplace confusion.** Plugin repository name, marketplace name, and plugin name can differ; verify all three.
3. **Plugin presence overclaim.** Installed plugin does not prove every command, agent, or hook exists; inspect the cache or manifest.
4. **Inline review self-approval.** A review invoked from inside Claude Code is useful but not an independent final review.
5. **Default-write rescue.** Many “rescue” or “delegate” surfaces can edit files by default; classify them as state-changing unless proven read-only.
6. **Expensive stop hooks.** Automatic review gates can loop or spend usage; keep them opt-in and monitored.
7. **False audit-only validation.** Check-only scripts must not mutate registries, credentials, project files, or plugin state.

## Verification Checklist

- [ ] Upstream install identity verified: repository, marketplace, plugin name, version/license.
- [ ] Dependency-vs-vendor decision recorded.
- [ ] No upstream plugin source, commands, agents, hooks, or internal skills were vendored.
- [ ] Optional install is gated and default run does not install token-spending/state-changing plugins.
- [ ] Live sub-capabilities are scanned from real cache/manifest files.
- [ ] Read-only vs state-changing surfaces are classified.
- [ ] Hermes final independent review is still required where applicable.
- [ ] Check-only/audit-only mode is proven non-mutating.
- [ ] Absorption decision recorded with all Required Decision Output Fields (or a lighter research note covering them).
- [ ] Validation evidence pasted exactly (repo-level validator, `git diff --check`, audit-only proof, cache scan).
- [ ] Codex review recorded (CR IDs and verdict) for review-required absorption decisions.
- [ ] Residual risks and non-goals stated explicitly.
- [ ] Task ledger and review record reflect any findings and fixes.
