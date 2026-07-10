# External Capability Decision - <candidate>

See `.maintain/skills/agent-plugin-dependency-governance/SKILL.md`. Fill every
field; use `n/a` with a reason rather than inventing evidence.

## Identity and decision

- Repository URL and official documentation:
- Package/plugin names, version, license, maintainer:
- Decision: external capability | reject | explicit fork
- Reason and explicitly approved vendored artifacts:

## Confirmed surfaces

| Surface | Local evidence | Authority | Task fit |
|---|---|---|---|
|  |  | read-only / state-changing / token-spending / context-migration |  |

## Runtime boundary

- Task-relevant discovery scope:
- Evidence that Hercules performs no setup/configuration/authentication action:
- Fallback/blocker behavior:

## Validation and review

- `python3 .maintain/scripts/validate-skill-pack.py --strict`:
- `.maintain/scripts/check-package.sh`:
- `git diff --check` and local manifest scan:
- Review record, CR IDs, verdict:
- Residual risks / non-goals:
