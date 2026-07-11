# Skill Navigation

This is the current navigation map for the exactly one runtime Skill under
`skills/`. The strict validator at `.maintain/scripts/validate-skill-pack.py`
checks the same exact-one set against both Git-tracked and visible Skill
directories.

Earlier skill inventories and reconciliation decisions are historical records
under `.maintain/docs/ai-collaboration/SKILL_GROUP_AUDIT.md` and
`.maintain/docs/ai-collaboration/tasks/`; they are not runtime membership lists.

## Runtime Skill (exactly one)

| Skill | Role | Maturity | Primary use | Notes |
|---|---|---|---|---|
| `hercules` | entry/composite | core | Public adaptive entry | Routes to internal references by task need; `skills/hercules/SKILL.md` |

## Internal references (not Skills)

| Reference | Purpose | Path |
|---|---|---|
| `capability-discovery.md` | Demand-led local capability discovery | `skills/hercules/references/capability-discovery.md` |
| `collaborative-workflow.md` | Capability-aware implementation workflow | `skills/hercules/references/collaborative-workflow.md` |
| `review-workflow.md` | Scoped review workflow | `skills/hercules/references/review-workflow.md` |
| `project-init.md` | Project-scoped initialization | `skills/hercules/references/project-init.md` |

## Maintainer-only material

Repository governance, archived workflows, and case studies live under
`.maintain/docs/`, `.maintain/skills/`, and `.maintain/examples/`. They are not
installed or discovered as runtime Skills.
