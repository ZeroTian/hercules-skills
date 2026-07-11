# Capability Map

Create one current-session record for each task capability role that needs local evidence:

```text
role: implementation
facility: claude
surface: installed CLI plus confirmed local plugin command
authority: read-only | write-capable
evidence: command or local file inspected
freshness: current-session
```

- `role` is the capability needed by the current task.
- `facility` identifies the confirmed local facility without making it a dependency.
- `surface` records only the behavior confirmed from locally visible metadata.
- `authority` distinguishes observation from mutation capability.
- `evidence` names the local command or file that supports the record; omit secrets and provider state.
- `freshness` remains `current-session`; discard or refresh the record after a relevant configuration change or capability-related invocation failure.

Do not persist a global inventory. Do not add unrelated facilities to the map.
