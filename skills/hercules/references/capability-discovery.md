# Hercules Capability Discovery

This demand-led workflow combines shallow discovery, deep plugin exploration, and an ephemeral capability map.

Use [capability-map.md](capability-map.md) for the record shape, [plugin-exploration.md](plugin-exploration.md) for deep inspection, and `capability_matrix.py` for the deterministic decision contract. Feed that contract the current task demand plus facility, cache, and real invocation evidence; consume its route, fallback, blocker, cache invalidation, and deep-inspection decisions. The contract is a non-executable deterministic reference, not a public command.

## Demand-led discovery
Start from task capability roles. Do not inventory every CLI, plugin, MCP, Skill, or agent at session startup.

## Shallow discovery
For relevant facilities only, inspect executable presence/version and locally visible installed/enabled capabilities. Do not inspect login, credentials, provider reachability, or unrelated surfaces.

## Deep plugin exploration
When an installed task-relevant plugin is unfamiliar, read its local manifest, commands, Skills, agents, and documentation. Confirm behavior from those files; never infer behavior from the plugin name.

## Ephemeral capability map
Record role, facility, confirmed surface, authority class, evidence source, and freshness for this session only.

## Selection order
explicit user preference -> project instructions -> confirmed task fit -> safety boundary -> fallback

## Fallback
Try another confirmed facility, then Hermes itself. If neither can safely satisfy the task, report the attempted facility, sanitized failure category, and the minimum user-run check.
