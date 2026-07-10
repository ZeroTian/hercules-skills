# Instruction Boundaries

Use the narrowest scope that matches who needs the rule and where it is true.

| Scope | Appropriate content | Exclude |
|---|---|---|
| Project-level shared instructions | repository layout, local commands, test and verification rules, project safety boundaries, generated-file rules, domain conventions | personal preferences that should follow the user everywhere |
| Tool-specific project instructions | project rules needed only by that tool or runtime, using its existing supported filename | duplicate copies of shared rules; fixed roles unrelated to capability |
| User-level instructions | cross-project communication preferences and general working methods | repository paths, project secrets, local service identifiers, or team-specific workflow facts |
| Global tool configuration | only an explicit separate user request outside project initialization | any implicit install, plugin enablement, credential, provider, or authentication change |

## Placement Rules

1. Read every existing instruction file that governs the target path, including nested files.
2. Put a shared project rule in the repository's existing general instruction file, commonly `AGENTS.md`.
3. Put a tool-only project rule in its existing tool-specific file, such as `CLAUDE.md`, only when the rule is not shared.
4. Keep user-wide preferences out of the repository unless the user explicitly converts them into project rules.
5. When existing files disagree, show the conflict and requested resolution; do not erase either side silently.

## Preservation and Verification

Patch the smallest relevant section and retain unrelated wording, ordering, and files. After editing:

- inspect the diff for accidental deletion or scope expansion;
- resolve every newly added relative link from its containing file;
- search renamed or referenced instruction filenames for stale paths;
- list all changed files and distinguish additions from preserved content.
