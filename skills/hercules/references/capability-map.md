# Capability Map

Create one current-session record for each task capability role that needs local evidence. Separate the broad role from concrete task requirements and the surfaces that prove them:

```text
role: research
required_capabilities: [video-transcription]
facility: claude
confirmed_surface: [research]
confirmed_surfaces:
  - family: mcp
    name: video-watcher
    capabilities: [video-transcription]
    authority: read-only
    evidence: MCP tool metadata plus relevant local server documentation
missing_requirements: []
authority: read-only
freshness: current-session
```

- `role` is the broad capability class needed by the current task.
- `required_capabilities` contains concrete task needs inferred before route selection.
- `facility` identifies the confirmed local container or execution facility without making it a dependency.
- `confirmed_surface` records broad role evidence.
- `confirmed_surfaces` records the smallest task-relevant built-in, MCP, plugin, command, Skill, or agent surfaces that cover concrete requirements.
- Each concrete surface records `family`, `name`, `capabilities`, `authority`, and sanitized local `evidence`.
- `missing_requirements` makes rejected executable-only candidates observable.
- `authority` distinguishes observation from mutation capability.
- `freshness` remains `current-session`; discard or refresh the record after a relevant configuration change or capability-related invocation failure.

A route is eligible only when broad role, authority, and every `required_capabilities` entry are covered. User or project preference can rank eligible records but cannot repair missing evidence. A cached broad-role record is invalid for a specialized demand unless it includes the matching requirements and concrete supporting surfaces.

Do not persist a global inventory. Do not add unrelated facilities or extension surfaces to the map, and never include credentials or provider state.
