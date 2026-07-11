# Hercules Project Init

## Purpose

Create the smallest project-scoped instruction change that satisfies the user's request. Reuse existing instruction files, preserve existing instructions, and keep personal or machine-wide policy outside the project.

## Procedure

1. Confirm the repository root, requested rules, approved files, and existing user changes.
2. Inspect existing `AGENTS.md`, `CLAUDE.md`, and tool-specific project instructions before proposing changes.
3. Map each requested rule to the narrowest project-scoped file using [instruction boundaries](instruction-boundaries.md).
4. Identify content to preserve, conflicts requiring a user decision, and the exact files that would change.
5. Merge only the requested project rules; preserve existing instructions and unrelated files.
6. do not install tools, plugins, Skills, dependencies, or write global configuration.
7. Verify resulting links/references, inspect the final diff, and show the user the changed files.

## File Selection

- Extend an existing applicable instruction file before creating a duplicate.
- Keep shared repository facts in the repository's general agent instructions.
- Keep a tool-specific rule in that tool's existing project file when only that tool consumes it.
- State an unresolved conflict instead of silently choosing or duplicating both rules.
- Do not add fixed implementation or reviewer identities when capability roles express the requirement.

## Change Contract

The final report must list changed files, summarize the project-scoped rules added, identify preserved conflicts or blockers, and provide link/reference verification evidence. If no file change is necessary, say so and show the evidence used.

## Common Mistakes

- Replacing an existing instruction file with a generic template.
- Copying personal preferences or machine setup into a repository.
- Creating parallel rule files with overlapping scope.
- Changing unrelated code or documentation during initialization.
- Reporting completion without checking links, references, and the actual diff.
