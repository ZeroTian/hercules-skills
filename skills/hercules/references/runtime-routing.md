# Runtime Routing

Use [capability discovery](capability-discovery.md) before selecting a destination whenever broad-role evidence or concrete-surface evidence for any inferred `required_capabilities` is missing, stale, incomplete, or invalidated.

| Capability role | Discovery condition | Internal workflow |
|---|---|---|
| implementation | Missing or stale implementation-facility evidence, or uncovered concrete requirements | [collaborative workflow](collaborative-workflow.md) |
| review | Missing or stale review-facility evidence, or uncovered concrete requirements | [review workflow](review-workflow.md) |
| browser | Missing or stale browser-facility evidence, or uncovered concrete requirements | [collaborative workflow](collaborative-workflow.md) |
| research | Missing or stale research-facility evidence, or uncovered concrete requirements | [collaborative workflow](collaborative-workflow.md) |
| parallel execution | Missing or stale parallel-execution evidence, or uncovered concrete requirements | [collaborative workflow](collaborative-workflow.md) |
| data access | Missing or stale data-access evidence, or uncovered concrete requirements | [collaborative workflow](collaborative-workflow.md) |
| project initialization | Missing or stale project-initialization evidence, or uncovered concrete requirements | [project initialization](project-init.md) |

For every row, require explicit current broad-role evidence and authority plus task-relevant concrete surface evidence. Preserve explicit user preferences and project instructions only after eligibility is established. Prefer a confirmed local facility, then another confirmed facility, then Hermes itself. Report a blocker only when no safe route remains.
