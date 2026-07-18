# Capability Map

Create one current-session record for each task capability role that needs local evidence. Separate the broad role from concrete task requirements and the surfaces that prove them:

```text
role: research
facility: claude
confirmed_surface: [research]
authority: read-only
evidence: current local facility metadata confirming the research role and authority
required_capabilities: [video-transcription]
confirmed_surfaces:
  - family: mcp
    name: video-watcher
    capabilities: [video-transcription]
    authority: read-only
    evidence: MCP tool metadata plus relevant local server documentation
missing_requirements: []
freshness: current-session
```

- `role` is the broad capability class needed by the current task.
- `facility` identifies the confirmed local container or execution facility without making it a dependency.
- `confirmed_surface`, top-level `authority`, and top-level `evidence` jointly prove the broad role. Authority and evidence are required explicit fields; do not infer or default them when deciding eligibility.
- `required_capabilities` contains concrete task needs inferred before route selection.
- `confirmed_surfaces` records the smallest task-relevant built-in, MCP, plugin, command, Skill, or agent surfaces that cover concrete requirements.
- Each concrete surface records `family`, `name`, `capabilities`, explicit `authority`, and concrete current `evidence`. Evidence must identify an inspected metadata, schema, manifest, definition, instructions, documentation/docs, or help surface.
- Executable presence, CLI identity, or version-only evidence can confirm that a facility container exists, but cannot prove a specialized surface.
- `missing_requirements` makes rejected executable-only candidates observable.
- `freshness` remains `current-session`; discard or refresh the record after a relevant configuration change or capability-related invocation failure.

A route is eligible only when broad role, authority, and every `required_capabilities` entry are covered. User or project preference can rank eligible records but cannot repair missing evidence. A cached route is reusable only when its requirement set exactly matches the current demand and its concrete supporting surfaces still cover that set. Return only surfaces and capability names relevant to the current demand; filter unrelated cached surfaces.

Do not persist a global inventory. Do not add unrelated facilities or extension surfaces to the map, and never include credentials or provider state.
