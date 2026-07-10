# Hercules Skill-First Lightweight Architecture

Date: 2026-07-10
Status: user-approved design

## 1. Decision

Hercules is a skill group, not an environment manager.

All user-facing intelligence belongs in Skills: task routing, capability discovery, Claude/Codex delegation, plugin use, fallback, failure diagnosis, review, and project initialization. External tools are optional facilities that Hercules discovers and launches when useful. Hercules does not install, configure, authenticate, or prescribe those facilities.

The public product surface is reduced to:

```text
README.md
init.sh
skills/
```

Repository validation, tests, release gates, review ledgers, and maintainer workflows remain available to contributors but move outside the runtime and Quickstart paths.

## 2. Problem Being Corrected

The current repository crossed the skill-group boundary:

- `scripts/install-hercules.sh` installs or checks OS packages, npm, Hermes, Claude, Codex, Hermes skills, and optional Claude plugins.
- `scripts/hercules doctor --fix` invokes that installer again.
- the bootstrap script manages registries, CLI packages, marketplaces, plugins, and fixed external skill dependencies.
- the README presents setup modes, doctor states, dependency bootstrap, release gates, and governance artifacts as part of the product entry surface.

This makes Hercules appear to require a preferred environment and distracts users from its actual value: adaptive orchestration encoded as Skills.

## 3. Goals

1. Make `/skill hercules` the only runtime entry users need to understand.
2. Keep all runtime decision-making and orchestration inside Skills.
3. Discover installed tools, plugins, MCP servers, agents, and skills on demand.
4. Adapt to user and project preferences instead of enforcing a plugin stack.
5. Install no third-party tools or plugins and modify no provider configuration.
6. Keep initialization limited to making the Hercules Skills visible to Hermes.
7. Keep contributor tooling available without placing it in the user journey.
8. Reduce the default runtime pack from 25 Skills to exactly five coherent Skills.

## 4. Non-Goals

- Installing Git, Hermes, Claude Code, Codex CLI, Node.js, package managers, MCP servers, plugins, or external Skills.
- Changing npm/pnpm registries, login state, API keys, gateways, cloud credentials, or provider configuration.
- Certifying that an external provider is usable before a real invocation.
- Recommending one plugin ecosystem as the required or preferred stack.
- Showing complete capability inventories during initialization or normal tasks.
- Installing domain-specific packs by default.

## 5. Architecture Boundaries

### 5.1 Initialization layer

`init.sh` is transport, not product intelligence. It uses `$HERCULES_HOME` (default: `$HOME/.hercules`) as the checkout and `$HERMES_HOME` (default: `$HOME/.hermes`) as the Hermes runtime home. It may only:

1. Verify that Git and Hermes already exist.
2. Clone or fast-forward update the Hercules repository at `$HERCULES_HOME`.
3. Symlink `$HERMES_HOME/skills/hercules` to `$HERCULES_HOME/skills`.
4. Print the next two commands: start Hermes and load `/skill hercules`.

If Git or Hermes is absent, initialization stops with one concise explanation and a documentation link. It does not offer or execute remediation. If the target skill path already contains a real directory or an unrelated symlink, initialization stops without moving or deleting it. Re-running against the expected checkout and symlink is idempotent.

The initializer must not call package managers, provider CLIs, plugin managers, marketplaces, authentication commands, or external installers.

### 5.2 Runtime skill layer

The default runtime contains exactly five Skills:

```text
skills/
  hercules/                         # single public entry and router
  hercules-capability-discovery/    # demand-led discovery and plugin understanding
  hercules-collaborative-workflow/  # delegation, execution, fallback
  hercules-review-workflow/         # verification and independent review
  hercules-project-init/            # project-scoped instruction initialization
```

Only `hercules` is advertised as a user entry point. The other Skills are internal building blocks selected by Hermes.

### 5.3 External facilities

Claude, Codex, MCP servers, plugins, custom agents, browser tools, and additional Skills are capability sources. They are neither dependencies nor product components.

Hercules may inspect their local, non-secret capability surfaces and invoke them when a task benefits. Their absence is normal and must not make initialization or unrelated tasks fail.

### 5.4 Maintainer layer

Contributor-only assets move under a hidden maintenance boundary:

```text
.maintain/
  scripts/       # validator, package checks, fresh-clone smoke
  tests/         # initializer and capability-matrix regression tests
  docs/          # task ledger, review records, governance history
  skills/        # repository-maintenance skills not installed at runtime
```

Maintainer assets are not copied into Hermes, are not scanned as runtime Skills, and are not shown in the user Quickstart. Historical detail can also remain recoverable through Git history instead of the main reader path.

## 6. Demand-Led Capability Discovery

Hercules must discover from task demand, not inventory everything at startup.

### 6.1 Flow

```text
user task
  -> classify required capability roles
  -> consult session capability cache
  -> shallow-scan only relevant facilities
  -> deep-inspect unfamiliar task-critical plugins
  -> build a normalized capability map
  -> select a facility or fallback
  -> invoke with a capability-aware brief
  -> verify the result
```

Example capability roles include code implementation, independent review, browser control, research, parallel agents, data access, and project initialization.

### 6.2 Shallow discovery

Shallow discovery may determine:

- whether a relevant CLI exists and its version;
- locally installed/enabled plugins, Skills, agents, and MCP servers;
- locally visible feature metadata needed for the current task.

It must not inspect login state, credentials, provider reachability, or unrelated capability surfaces.

### 6.3 Deep plugin exploration

When an installed plugin appears relevant but its capability is unknown, Hercules reads the plugin's local manifest, commands, Skills, agents, and documentation. Selection is based on confirmed behavior rather than plugin name.

Fixed plugin names may appear only as examples or known adapters. They must never be completion requirements. A newly installed compatible plugin can be selected without changing Hercules installation logic.

### 6.4 Capability map

Discovery produces an ephemeral, normalized map such as:

```text
implementation: Claude, Codex
independent-review: Codex CLI
browser-control: Playwright, Chrome DevTools
parallel-execution: installed team/agent capability
```

The map is cached only for the current session. It is invalidated when:

- a plugin, MCP, agent, Skill, or relevant config changes;
- a required capability is missing from the cache;
- a real invocation reports a capability-related failure.

## 7. Selection and Fallback Policy

Facility selection follows this order:

```text
explicit user preference
-> project instructions
-> confirmed task fit
-> safety and authority boundary
-> available fallback
```

Hercules must not encode a universal preference for Claude, Codex, a marketplace, or a plugin collection.

If the best facility is unavailable:

1. select another confirmed local capability;
2. let Hermes handle the task directly when reasonable;
3. report a blocker only when no safe path can satisfy the task.

Missing optional facilities remain silent unless they affect the current task.

## 8. Failure Handling

Initialization failures contain only:

- what prerequisite is missing;
- that Hercules did not install or change it;
- where the user can inspect the prerequisite's own documentation.

Runtime invocation failures contain:

- which facility was attempted;
- a sanitized failure category, such as missing executable, unsupported command, provider/access rejection, unavailable capability, or runtime failure;
- the fallback selected, or the minimum user-run check if no fallback exists.

Hercules never responds to a runtime failure by installing a tool, changing provider configuration, opening a login flow, or printing secrets.

## 9. Skill Disposition

The existing pack is reduced using these rules.

### 9.1 Merge into the five runtime Skills

- `hercules-agent-capability-preflight`
- `hercules-collaborative-agent-workflow`
- `hermes-collaborative-workflow`
- `coding-agent-orchestration`
- `cross-agent-review-loop`
- `iterative-agent-code-review`
- `hercules-project-init-workflow`
- `hermes-project-init-orchestration`
- the runtime discovery portions of `agent-plugin-dependency-governance`

Repeated rules become references within the owning core Skill instead of independent runtime Skills.

### 9.2 Move to `.maintain/skills`

- `hercules-meta-skill-evolution`
- `hercules-skill-pack-management`
- `open-source-project-packaging`
- `skill-pack-governance-validation`
- `skill-pack-roadmap-execution`
- `staged-commit-package-governance`
- `workflow-skill-pack-audit`
- maintainer-only portions of installer and plugin dependency governance

`portable-skill-pack-installation` and `cli-installer-ux-governance` are retired after their minimal initialization safety rules are absorbed into `init.sh` tests and maintainer documentation.

### 9.3 Move out of the default pack

- `evaluation-closed-loop-orchestration`
- `godot-rl-metric-regression`
- `godot-wsl-artifact-validation`
- `kanban-codex-lane`
- `kanban-orchestrator`
- `kanban-worker`
- `open-ended-research-orchestration`

During this contraction they move to `.maintain/examples/skills/`, which is not runtime-discoverable. A future separate extension repository is possible but outside this design. `init.sh` does not install them and exposes no profile-selection UI.

## 10. Public User Experience

The README first screen contains one explanation and three steps:

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
/skill hercules
```

There are no full/minimal modes, dependency bootstrap, doctor dashboard, fix command, plugin checklist, or release-governance concepts in the user journey.

For project-specific use, the user asks the `hercules` entry Skill to initialize the current project. It routes to `hercules-project-init`; no separate external project installer is required.

## 11. Validation Strategy

### 11.1 Initialization safety

Tests prove that `init.sh`:

- only clones/fast-forward updates the checkout and creates the expected Skills symlink;
- never invokes npm, pnpm, brew, apt, provider CLIs, plugin managers, marketplaces, or login commands;
- stops clearly when Git or Hermes is missing;
- is idempotent for an existing installation.

### 11.2 Capability matrix

Mocked runtime tests cover:

- Hermes only;
- Claude only with no plugins;
- Codex only;
- Claude and Codex together;
- arbitrary installed plugins and MCP servers;
- a task-relevant plugin that requires deep inspection;
- stale cache followed by a capability change;
- a real invocation rejected by provider/access state;
- no viable capability, producing a concise blocker.

Each scenario must demonstrate selection or fallback without any install/configuration command.

### 11.3 Package focus

Validation also enforces:

- exactly one documented runtime entry Skill;
- only the approved core Skills exist under default `skills/`;
- maintainer and extension Skills are not runtime-discoverable;
- the README Quickstart remains at three steps;
- no fixed plugin is declared required;
- public scripts contain only initialization behavior.

## 12. Migration Boundary

The implementation is a deliberate contraction, not another compatibility layer.

- Replace the current installer and CLI product surface with `init.sh`.
- Delete dependency installation, doctor repair, registry mutation, marketplace management, and bootstrap installation logic.
- Preserve useful capability discovery and orchestration knowledge by merging it into the five core Skills.
- Move maintainer and extension content out of the default runtime path.
- Rewrite the README around the single entry Skill.
- Do not keep deprecated full/minimal/fix commands as aliases; clear removal is preferred over carrying the old product model forward.

No provider, plugin, or user configuration is modified during migration.

## 13. Acceptance Criteria

The redesign is complete when:

1. users can initialize Hercules and start `/skill hercules` in three steps;
2. exactly five approved core Skills are installed by default;
3. no runtime or initialization path installs or configures third-party facilities;
4. Hermes discovers task-relevant installed capabilities and explores plugin internals when needed;
5. Claude-only, Codex-only, plugin-rich, and minimal environments all select or degrade correctly;
6. maintainer tooling remains usable but is absent from the public runtime surface;
7. tests and independent review confirm the repository has not retained hidden dependency-management behavior.
