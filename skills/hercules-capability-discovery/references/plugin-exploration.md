# Plugin Exploration

Deep exploration is allowed only for an installed plugin that is relevant to a current task role and whose behavior is not yet confirmed.

## Required local evidence

Before selecting a plugin capability, inspect and cite the relevant local evidence:

- the plugin manifest and declared entry points;
- command definitions for the proposed surface;
- Skill instructions that govern the proposed workflow;
- agent definitions when the capability delegates to an agent;
- local documentation needed to interpret those files.

Confirm the behavior, authority boundary, and invocation surface from this evidence. If a manifest, command, Skill, or agent surface is absent, record that absence and do not infer behavior from the plugin name.

Fixed plugin names are examples, not requirements. Selection depends on confirmed task fit, so a compatible unfamiliar plugin may be used without changing Hercules or declaring it mandatory.

Inspect no credentials, login state, provider reachability, or unrelated plugins. Keep evidence paths and failure details sanitized in the current-session capability map.
