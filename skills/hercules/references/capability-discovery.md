# Hercules Capability Discovery

This demand-led workflow combines shallow discovery, deep plugin exploration, and an ephemeral capability map.

Use [capability-map.md](capability-map.md) for the record shape, [plugin-exploration.md](plugin-exploration.md) for deep inspection, and `capability_matrix.py` for the deterministic decision contract. Feed that contract the current task demand plus facility, cache, and real invocation evidence; consume its route, fallback, blocker, cache invalidation, missing-requirement, and deep-inspection decisions. The contract is a non-executable deterministic reference, not a public command.

## Demand-led discovery

Decompose the task into:

- one broad capability `role`, such as research, implementation, or data access; and
- zero or more concrete `required_capabilities`, such as `video-transcription`, browser automation, repository review, or a specific data operation.

Infer concrete requirements from the task, not only from tool names explicitly mentioned by the user. A request to learn from videos implies a video-understanding or `video-transcription` requirement even when the user does not say “MCP”. Do not inventory every CLI, plugin, MCP, Skill, or agent at session startup.

## Task-relevant surface preflight

For each plausible facility, inspect only the extension families that could satisfy the concrete requirement:

- core and built-in tools or feature metadata;
- configured MCP tool metadata and relevant local server documentation;
- enabled plugins and their declared entry points;
- commands exposed by the facility or plugin;
- nested Skills that govern the proposed workflow; and
- agents or team roles that provide the needed capability.

Checking executable presence is only shallow discovery. Do not stop at `claude --version` or `codex --version` when an extension surface could satisfy a `required_capabilities` entry. A facility must not be selected merely because its CLI broadly supports the task role.

This is an unskippable completion gate: Hermes must not select a route until every concrete requirement has task-relevant local evidence, or every plausible relevant surface family has a confirmed absence and the candidate is rejected. Record absence without inspecting credentials, secret values, login state, or provider reachability. User and project preferences rank only candidates that already pass this gate.

## Shallow discovery

For relevant facilities only, inspect executable presence/version and locally visible installed/enabled capabilities. Facility-native list/status commands, local manifests, tool schemas, and Skill or agent definitions are valid non-secret evidence. Do not inspect unrelated surfaces.

## Deep plugin exploration

When a task-relevant extension is unfamiliar or shallow evidence does not establish the concrete behavior, follow [plugin-exploration.md](plugin-exploration.md). Read the smallest relevant manifest, MCP tool schema, command, Skill, agent, or documentation surface. Confirm behavior from those files; never infer behavior from a product or plugin name.

## Ephemeral capability map

Record broad role, `required_capabilities`, facility, concrete confirmed surfaces, authority class, evidence source, missing requirements, and freshness for this session only. A broad-role cache entry cannot satisfy a later specialized demand unless it records the same concrete requirements and supporting surfaces.

## Selection order

confirmed task fit -> explicit user preference -> project instructions -> safety boundary -> fallback

Preferences never bypass required-capability coverage or authority checks.

## Fallback

Try another confirmed facility, then Hermes itself. Re-run the relevant surface preflight after a capability-related invocation failure or relevant configuration change. If no route can satisfy all concrete requirements, report the inspected relevant surfaces, confirmed absence or sanitized failure category, and the remaining blocker.
