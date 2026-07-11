# Hercules Project Init

## Purpose

Create the smallest project-scoped instruction change that satisfies the user's request. Reuse existing instruction files, preserve existing instructions, and keep personal or machine-wide policy outside the project.

## Procedure

1. Confirm the repository root, requested rules, candidate files, and existing user changes.
2. Inspect every instruction file governing the target path, including existing `AGENTS.md`, `CLAUDE.md`, `HERMES.md`, and nested instructions.
3. Detect existing Hercules entry rules, equivalent wording, and conflicts.
4. Map each rule to the narrowest project-scoped file using [instruction boundaries](instruction-boundaries.md).
5. Preview the exact additions and changed files. Identify preserved content, conflicts, and unsupported or uncovered instruction surfaces.
6. Obtain explicit user approval before changing any instruction file.
7. Apply the smallest approved merge. Repeated initialization must be idempotent: retain equivalent rules instead of appending duplicates.
8. Verify references, canonical ownership, adapter scope, preservation of existing content, and the final diff.
9. Report changed files, preserved conflicts, uncovered tools, and verification evidence.

## Canonical Shared Contract

Keep the canonical shared contract in the repository's applicable general instruction file, normally `AGENTS.md`. Merge rules requiring agents to:

- route non-trivial project work through Hercules before selecting an implementation or review facility;
- read governing project instructions and perform relevant capability discovery before facility selection;
- invoke only a confirmed facility with sufficient authority;
- identify Hermes built-in subagents accurately: they must not be represented as Claude Code or Codex CLI;
- classify invocation failures and follow Hercules fallback rules without silently changing identity or authority;
- independently verify actual outputs before reporting completion.

If Hercules is unavailable, report a blocker or use only an explicitly approved fallback; do not claim that Hercules routing occurred.

Do not copy the complete Hercules Skill or internal workflow references into a project instruction file.

## Tool-specific Adapters

### `CLAUDE.md` adapter

Retain Claude-specific implementation boundaries and add only a short instruction to follow the canonical shared contract in `AGENTS.md`. Do not duplicate the canonical shared contract.

### `HERMES.md` adapter

State that Hermes is the controller, must load the canonical shared contract and Hercules before routing project work, and must not use `delegate_task` or another built-in subagent as a substitute for a requested or selected Claude Code or Codex CLI facility. Do not duplicate the canonical shared contract.

Update only instruction filenames supported by the applicable tool. If a supported file is absent, create it only when its exact content appeared in the approved preview. If an existing rule conflicts with this contract, stop and show the conflict instead of silently overriding either rule.

## File Selection

- Extend an existing applicable instruction file before creating a duplicate.
- Keep shared repository facts in the repository's general agent instructions.
- Keep a tool-specific rule in that tool's existing project file when only that tool consumes it.
- State an unresolved conflict instead of silently choosing or duplicating both rules.
- Do not add fixed implementation or reviewer identities when capability roles express the requirement.
- Keep project initialization scoped to instructions: do not install tools, plugins, Skills, dependencies, or write global configuration.

## Change Contract

The final report must list changed files, summarize the project-scoped rules added, identify preserved conflicts or blockers, name unsupported or uncovered instruction surfaces, and provide link/reference plus final-diff verification evidence. Confirm that shared rules have one canonical owner and tool-specific files contain only adapters. If no file change is necessary, say so and show the equivalent rules used as evidence.

## Common Mistakes

- Replacing an existing instruction file with a generic template.
- Copying personal preferences or machine setup into a repository.
- Creating parallel rule files with overlapping scope.
- Changing unrelated code or documentation during initialization.
- Reporting completion without checking links, references, and the actual diff.
