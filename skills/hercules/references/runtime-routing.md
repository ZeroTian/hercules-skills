# Runtime Routing

Use [capability discovery](capability-discovery.md) before the destination only when evidence for the relevant role is missing or stale.

| Capability role | Discovery condition | Internal workflow |
|---|---|---|
| implementation | Missing or stale implementation-facility evidence | [collaborative workflow](collaborative-workflow.md) |
| review | Missing or stale review-facility evidence | [review workflow](review-workflow.md) |
| browser | Missing or stale browser-facility evidence | [collaborative workflow](collaborative-workflow.md) |
| research | Missing or stale research-facility evidence | [collaborative workflow](collaborative-workflow.md) |
| parallel execution | Missing or stale parallel-execution evidence | [collaborative workflow](collaborative-workflow.md) |
| data access | Missing or stale data-access evidence | [collaborative workflow](collaborative-workflow.md) |
| project initialization | Missing or stale project-initialization evidence | [project initialization](project-init.md) |

For every row, preserve explicit user preferences and project instructions. Prefer a confirmed local facility, then another confirmed facility, then Hermes itself. Report a blocker only when no safe route remains.
