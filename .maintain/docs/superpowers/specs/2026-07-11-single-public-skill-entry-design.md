# Hercules Single Public Skill Entry Design

Date: 2026-07-11
Status: approved in conversation; awaiting written-spec review

## Problem

Hercules currently installs five top-level `SKILL.md` files: one intended public entry and four intended internal workflows. Hermes v0.18.2 exposes every discovered `SKILL.md` as a slash command, so the UI shows all five and the claimed single public entry is only a convention.

The published Quickstart and `init.sh` also print `/skill hercules`. Hermes actually maps an installed skill named `hercules` to `/hercules`; `/skills` opens the management hub instead of invoking the skill.

## Goals

- Hermes discovers exactly one Hercules skill and one slash command: `/hercules`.
- Capability discovery, collaborative execution, review, and project initialization remain available as internal task-routed workflows.
- Existing installations update without changing the managed symlink or user configuration.
- README and initializer output show the real Hermes v0.18.2 invocation.
- Active Hermes sessions receive a clear `/reload-skills` or restart hint.

## Non-goals

- Do not modify Hermes itself.
- Do not hide skills through user-level Hermes configuration.
- Do not preserve direct invocation of the four internal workflow commands.
- Do not install, configure, authenticate, or probe external facilities.

## Architecture

The runtime package becomes one skill with internal references:

```text
skills/
└── hercules/
    ├── SKILL.md
    └── references/
        ├── runtime-routing.md
        ├── capability-discovery.md
        ├── capability-map.md
        ├── plugin-exploration.md
        ├── capability_matrix.py
        ├── collaborative-workflow.md
        ├── invocation-failure.md
        ├── review-workflow.md
        ├── review-loop.md
        ├── project-init.md
        └── instruction-boundaries.md
```

Only `skills/hercules/SKILL.md` has Skill frontmatter. Internal workflow files are ordinary references and therefore do not become Hermes slash commands.

The existing symlink remains unchanged:

```text
~/.hermes/skills/hercules -> <checkout>/skills
```

Because `<checkout>/skills` contains only one `SKILL.md`, Hermes exposes only `/hercules` after a reload or restart.

## Routing Contract

`skills/hercules/SKILL.md` remains the router and links each internal workflow explicitly:

1. Classify the task into capability roles.
2. Load `capability-discovery.md` only when relevant evidence is missing, stale, or invalidated.
3. Load `collaborative-workflow.md` for implementation, browser, research, parallel execution, and data-access work.
4. Load `review-workflow.md` when review independence or scoped verification is required.
5. Load `project-init.md` for repository-local instruction initialization or updates.
6. Use only confirmed local facilities; fallback safely without installing or authenticating anything.

The deterministic capability decision contract moves with the discovery references. Its cache authority, freshness, fallback, and no-install behavior stay unchanged.

## User Experience

The public Quickstart becomes:

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
```

Then, inside Hermes:

```text
/hercules <your task>
```

`init.sh` prints the same command. It also explains that an already-running Hermes session should execute `/reload-skills` or restart before invoking `/hercules`.

The `/skills` hub remains a management interface. It may show a `hercules` category, but that category contains only the single `hercules` skill.

## Migration and Compatibility

- A normal fast-forward update removes the four retired top-level workflow directories and adds their content under `skills/hercules/references/`.
- The managed symlink target does not change, so existing installations need no relink or global configuration migration.
- An active TUI may retain its startup slash-command catalog. `/reload-skills` or a restart refreshes it.
- The four old slash commands intentionally disappear. Their functionality remains reachable through `/hercules` routing.
- The Hercules skill version advances from `1.0.0` to `1.1.0`.

## Maintainer Surfaces

Current architecture, navigation, validator, and tests change from an exact-five runtime contract to an exact-one public runtime contract. Historical review/spec records remain historical and are not rewritten as current architecture.

The validator must reject:

- any additional top-level runtime `SKILL.md`;
- a missing `skills/hercules/SKILL.md`;
- internal workflow references with broken links;
- documentation that advertises `/skill hercules` or any retired direct workflow command.

## Testing Strategy

TDD begins with failing tests for the observed user-visible defects:

1. Runtime structure contains exactly one `SKILL.md`, named `hercules`.
2. README and initializer advertise `/hercules`, never `/skill hercules`.
3. The public router links all four internal workflow references, and every target resolves.
4. The four retired workflow directories and direct commands are absent.
5. Capability matrix behavior tests load the moved contract and preserve all existing routing/cache/privacy guarantees.
6. Initializer clone, rerun, conflict preservation, and symlink behavior remain green.
7. Strict validator, package gate, and fresh-clone smoke pass.

On the current machine, a final Hermes integration probe rescans installed skills and must return exactly:

```text
{/hercules: hercules}
```

The portable repository gate relies on the structural one-`SKILL.md` invariant rather than requiring Hermes to be installed in CI.

## Acceptance Criteria

- `find skills -name SKILL.md` returns only `skills/hercules/SKILL.md`.
- Hermes slash discovery returns only `/hercules` for this package.
- `/hercules <task>` routes capability discovery, execution, review, and project initialization correctly.
- `/skill hercules` and the four retired workflow commands are absent from active product documentation and initializer output.
- Existing symlink installs update without relinking.
- All focused and full tests, strict validation, package privacy checks, and fresh-clone smoke pass.
