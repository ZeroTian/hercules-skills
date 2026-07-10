# Skill Navigation

This is the current navigation map for the exactly five runtime Skills under
`skills/`. The strict validator at `.maintain/scripts/validate-skill-pack.py`
checks the same exact-five set against both Git-tracked and visible Skill
directories.

Earlier skill inventories and reconciliation decisions are historical records
under `.maintain/docs/ai-collaboration/SKILL_GROUP_AUDIT.md` and
`.maintain/docs/ai-collaboration/tasks/`; they are not runtime membership lists.

## Runtime Skills (exactly five)

| Skill | Role | Maturity | Primary use | Notes |
|---|---|---|---|---|
| `hercules` | entry/composite | core | Public adaptive entry | Routes by task need; `skills/hercules/SKILL.md` |
| `hercules-capability-discovery` | atom | core | Demand-led local capability discovery | Confirms capabilities without environment mutation; `skills/hercules-capability-discovery/SKILL.md` |
| `hercules-collaborative-workflow` | atom | core | Capability-aware implementation workflow | Uses only confirmed capabilities; `skills/hercules-collaborative-workflow/SKILL.md` |
| `hercules-review-workflow` | atom | core | Scoped review workflow | Requires independence only when the task requires it; `skills/hercules-review-workflow/SKILL.md` |
| `hercules-project-init` | atom | core | Project-scoped initialization | Preserves existing project state; `skills/hercules-project-init/SKILL.md` |

## Maintainer-only material

Repository governance, archived workflows, and case studies live under
`.maintain/docs/`, `.maintain/skills/`, and `.maintain/examples/`. They are not
installed or discovered as runtime Skills.
