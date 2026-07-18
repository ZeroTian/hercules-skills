# Plugin and Extension Exploration

Deep exploration is allowed only for an installed or configured extension surface that is relevant to a current concrete requirement and whose behavior is not yet confirmed. Extension surfaces include MCP tools, plugins, nested Skills, agents, teams, and commands exposed by a facility.

## Required local evidence

Before selecting an extension capability, inspect and cite the smallest relevant local evidence:

- MCP server/tool metadata and the proposed tool schema;
- the plugin manifest and declared entry points;
- command definitions for the proposed surface;
- Skill instructions that govern the proposed workflow;
- agent or team definitions when the capability delegates work; and
- local documentation needed to interpret those files.

Confirm concrete behavior, authority boundary, invocation surface, and task fit. Record the surface family, concrete name, covered requirements, and evidence in the current-session capability map. If a relevant manifest, MCP tool, command, Skill, agent, or team surface is absent, record that confirmed absence and do not infer behavior from a name.

For a facility such as Claude Code or Codex CLI, the executable/version proves only that the container exists. It does not prove that a configured MCP, enabled plugin, nested Skill, agent, team, command, or built-in feature is present or absent. Inspect only the families plausibly related to the current `required_capabilities`; do not enumerate unrelated extensions.

Fixed extension names are examples, not requirements. Selection depends on confirmed task fit, so a compatible unfamiliar extension may be used without changing Hercules or declaring it mandatory.

Inspect no credentials, secret values, login state, or provider reachability. Keep evidence paths and failure details sanitized in the current-session capability map.
