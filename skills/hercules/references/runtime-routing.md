# Runtime Routing

Use `hercules-capability-discovery` before the destination only when evidence for the relevant role is missing or stale.

| Capability role | Discovery condition | Destination Skill |
|---|---|---|
| implementation | Missing or stale implementation-facility evidence | `hercules-collaborative-workflow` |
| review | Missing or stale review-facility evidence | `hercules-review-workflow` |
| browser | Missing or stale browser-facility evidence | `hercules-collaborative-workflow` |
| research | Missing or stale research-facility evidence | `hercules-collaborative-workflow` |
| parallel execution | Missing or stale parallel-execution evidence | `hercules-collaborative-workflow` |
| data access | Missing or stale data-access evidence | `hercules-collaborative-workflow` |
| project initialization | Missing or stale project-initialization evidence | `hercules-project-init` |

For every row, preserve explicit user preferences and project instructions. Prefer a confirmed local facility, then another confirmed facility, then Hermes itself. Report a blocker only when no safe route remains.
