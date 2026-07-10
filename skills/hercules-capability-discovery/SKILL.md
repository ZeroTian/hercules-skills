---
name: hercules-capability-discovery
description: "Internal demand-led discovery of task-relevant local capabilities, evidence, authority, freshness, and provider-neutral fallbacks."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, capability-discovery, routing, provider-neutral]
    related_skills: [hercules, hercules-collaborative-workflow, hercules-review-workflow, hercules-project-init]
---

# Hercules Capability Discovery

This demand-led workflow combines shallow discovery, deep plugin exploration, and an ephemeral capability map.

Use the record in `references/capability-map.md` and the evidence rules in `references/plugin-exploration.md`.

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
