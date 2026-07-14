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

## Canonical Shared Execution Contract

Keep the canonical shared execution contract in the repository's applicable general instruction file, normally `AGENTS.md`. Merge rules requiring selected execution or review facilities to:

- preserve the declared facility identity, role, and authority from the invocation brief;
- execute the bounded brief directly within the approved scope;
- enforce that selected facilities must not load Hercules, must not perform capability discovery, must not select another facility, and must not apply controller fallback;
- run only permitted self-checks and return concrete result or failure evidence to the controller;
- return the failure to Hermes without silently changing facility identity, authority, or scope.

Do not copy the complete Hercules Skill or internal workflow references into a project instruction file.

## Tool-specific Adapters

### `CLAUDE.md` facility adapter

Retain Claude-specific implementation boundaries and identify Claude Code as an implementation or review facility. Add only a short instruction to follow the canonical shared execution contract in `AGENTS.md` and execute its bounded brief directly. State that a selected Claude Code facility must not load Hercules or select another facility. Do not duplicate the canonical shared execution contract.

### `HERMES.md` controller adapter

State that Hermes is the controller: it must load the canonical shared execution contract and Hercules, route non-trivial project work through Hercules, perform relevant capability discovery before selection, and invoke only a confirmed facility with sufficient authority. Hermes built-in subagents must not be represented as Claude Code or Codex CLI, and Hermes must not use `delegate_task` or another built-in subagent as a substitute for a requested or selected external facility. After a real invocation failure, Hermes must follow Hercules fallback rules without silently changing identity, authority, or scope. After execution, Hermes must independently verify actual outputs before reporting completion.

Clarify that Hercules is loaded as a Skill workflow rather than assumed to be a CLI, that synthetic `hercules discover/execute` commands are forbidden without confirmed executable/documentation evidence, and that this does not block Skill/reference loading or direct invocation of confirmed facilities. If Hercules is unavailable, Hermes reports a blocker or uses only an explicitly approved fallback; it must not claim that Hercules routing occurred. Do not duplicate the canonical shared execution contract.

Update only instruction filenames supported by the applicable tool. If a supported file is absent, create it only when its exact content appeared in the approved preview. If an existing rule conflicts with this contract, stop and show the conflict instead of silently overriding either rule.

## File Selection

- Extend an existing applicable instruction file before creating a duplicate.
- Keep shared execution facts in the repository's general agent instructions.
- Keep a tool-specific rule in that tool's existing project file when only that tool consumes it.
- State an unresolved conflict instead of silently choosing or duplicating both rules.
- Do not add fixed implementation or reviewer identities when capability roles express the requirement.
- Keep project initialization scoped to instructions: do not install tools, plugins, Skills, dependencies, or write global configuration.

## Change Contract

The final report must list changed files, summarize the project-scoped rules added, identify preserved conflicts or blockers, name unsupported or uncovered instruction surfaces, and provide link/reference plus final-diff verification evidence. Confirm that shared execution rules have one canonical owner, controller routing exists only in the Hermes adapter, and facility adapters do not re-enter Hercules. If no file change is necessary, say so and show the equivalent rules used as evidence.

## Common Mistakes

- Treating the Hercules Skill or `capability_matrix.py` reference as proof that a public `hercules` executable/subcommand exists.
- Writing a no-synthetic-command rule so broadly that it suppresses Hercules Skill loading or confirmed Claude Code/Codex CLI invocation.
- Replacing an existing instruction file with a generic template.
- Copying personal preferences or machine setup into a repository.
- Creating parallel rule files with overlapping scope.
- Putting controller routing into shared facility instructions and causing recursive Hercules entry.
- Changing unrelated code or documentation during initialization.
- Reporting completion without checking links, references, and the actual diff.
