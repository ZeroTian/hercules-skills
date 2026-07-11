# Architecture

## Repository purpose

Hercules is a skill-first Hermes package with one public initializer and
exactly one runtime Skill. The four internal workflows live under
`skills/hercules/references/` and are not discovered as slash commands.
Repository tooling and governance history stay behind the maintainer boundary.

## Current layout

```text
.
├── init.sh
├── skills/
│   └── hercules/                  # exactly one runtime Skill
│       ├── SKILL.md               # public /hercules router
│       └── references/            # internal, non-Skill workflows
└── .maintain/
    ├── scripts/                    # validator, smoke, package gate
    ├── tests/                      # init/runtime/tooling contracts
    ├── docs/                       # current governance + dated history
    ├── skills/                     # maintainer-only archived workflows
    └── examples/                   # maintainer-only case studies
```

Nothing under `.maintain/` is part of the installed runtime Skill surface.

## Runtime boundary

The only runtime Skill file is:

- `skills/hercules/SKILL.md`

Its internal workflow references are:

- `skills/hercules/references/capability-discovery.md`
- `skills/hercules/references/collaborative-workflow.md`
- `skills/hercules/references/review-workflow.md`
- `skills/hercules/references/project-init.md`

`.maintain/scripts/validate-skill-pack.py` enforces this exact set against both
Git-tracked files and visible directories. Historical navigation and audit
records do not define runtime membership.

## Maintainer boundary

- `.maintain/docs/ai-collaboration/TASKS.md` contains the live ledger, active
  policy, and task template. Dated task/review evidence remains historical.
- `.maintain/docs/ai-collaboration/SKILL_NAVIGATION.md` is the current exact-one
  runtime navigation.
- `.maintain/docs/ai-collaboration/candidate-skills/` preserves candidates
  outside runtime loading.
- `.maintain/scripts/smoke-fresh-clone.sh` validates a staged package in a
  temporary clone.
- `.maintain/scripts/check-package.sh` validates the staged package and scans
  staged additions for sensitive filenames/content without fixed temp logs.

Current maintainer gates:

```bash
python3 .maintain/scripts/validate-skill-pack.py --strict
python3 .maintain/tests/test_init.py -v
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/tests/test_validate_skill_pack_cli.py -v
.maintain/scripts/smoke-fresh-clone.sh
.maintain/scripts/check-package.sh
```

## Dependency boundary

Runtime discovery is demand-led and provider-neutral. Hercules may use a
confirmed local capability when helpful, but the repository does not vendor,
install, configure, authenticate, or require external agents, plugins, MCP
servers, or provider credentials.

## Historical records

Audit snapshots, dated tasks, trajectory evidence, and Codex review records
remain under `.maintain/docs/ai-collaboration/`. Old paths inside dated evidence
describe commands that actually ran at that time and must not be treated as
current instructions.
