---
name: repository-governance-initialization
description: "Initialize or reinitialize repository governance files with an inspect→preview→approve→apply→verify→independent-review loop, keeping README reader-facing and actor rules scoped."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [governance, project-init, hermes, claude-code, codex, review]
    related_skills: [hercules-project-init-workflow, hermes-project-init-orchestration, coding-agent-orchestration]
---

# Repository Governance Initialization

## Overview

Use this class-level skill when initializing or reinitializing repository governance artifacts such as `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, `docs/ai-collaboration/TASKS.md`, architecture notes, audit snapshots, Codex review folders, or ADR folders.

This skill captures the safe execution pattern from a successful Hercules skill-pack initialization: inspect without mutation, generate a concrete preview outside the repo, wait for explicit approval, apply only the approved files, verify locally, then request independent Codex review because governance files become future agent instructions.

## When to Use

Use when the user asks to:

- initialize the current project for Hermes / Claude Code / Codex collaboration;
- add or repair `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, or `docs/ai-collaboration/`;
- standardize README scope versus actor-scoped operational rules;
- create a task ledger, architecture boundary doc, audit snapshot, review directory, or decisions directory;
- reinitialize governance in an existing repo without changing business code.

Do not use for a normal feature implementation. Use the collaborative coding/review skills for code changes.

## Procedure

1. **Load applicable workflow skills first.** Prefer project-init/orchestration skills already present in the library. This skill is a reusable execution pattern, not a replacement for repository-specific rules.
2. **Inspect without mutation.** Check repo root, `git status --short`, branch, remotes, existing README/governance docs, manifests, CI, scripts, and relevant tracked file lists.
3. **Separate pre-existing untracked work.** If untracked files already exist, record them as existing state. Do not silently include them in initialization unless the user explicitly approves.
4. **Create a temp preview tree outside the repo.** Generate proposed files under a path such as `/tmp/<project>-init-preview` so the repo remains unchanged during preview.
5. **Present exact scope.** List every file to create/modify, the role of each file, the validation plan, and state clearly that no repo files have changed.
6. **Wait for explicit approval.** Do not treat silence or vague acknowledgement as permission for broad governance writes.
7. **Apply only approved artifacts.** Write the previewed files into the repo. Do not commit, push, reset, clean, or refactor unrelated files.
8. **Run local validation.** Use checks appropriate to the repository type, for example `git status --short -uall`, `git diff --check`, script syntax checks, frontmatter checks, and referenced path existence checks.
9. **Run independent Codex review.** Even docs-only governance changes should get a read-only Codex pass, because these files affect future agent behavior.
10. **Report real state.** Include created/changed files, validation commands and outputs, Codex verdict, and remaining follow-up tasks or blockers.

## Documentation Boundaries

Keep responsibilities separated:

- `README.md`: human overview, install/use, migration, and navigation.
- `HERMES.md`: Hermes orchestration rules and validation commands.
- `CLAUDE.md`: Claude Code implementation rules, SDD/TDD, and handoff requirements.
- `AGENTS.md`: Codex review rules, CR handling, and acceptance criteria.
- `docs/ai-collaboration/TASKS.md`: live collaboration ledger.
- `docs/ai-collaboration/ARCHITECTURE.md`: repository structure and boundaries.
- `docs/ai-collaboration/PROJECT_AUDIT.md`: evidence-backed initialization snapshot.
- `docs/ai-collaboration/codex-reviews/`: stable Codex review records.
- `docs/ai-collaboration/decisions/`: ADR-style decisions.

## Codex Review Checklist

Ask Codex to verify:

- README remains reader-facing and does not duplicate long operational rules.
- Actor-scoped responsibilities are clear and non-conflicting.
- Builtin skills or framework-provided components are not vendored into the project by accident.
- External hub/third-party skills are listed as dependencies rather than copied unless explicitly approved.
- Task ledger fields are complete and checkbox truth is reasonable.
- Architecture and audit docs match actual repo state.
- No instruction permits commit, push, reset, clean, or history rewrite without explicit user request.
- Validation commands are appropriate for the repository type.

Require a structured footer:

```json
{
  "verdict": "PASS | FAIL | BLOCKED",
  "highest_severity": "P0 | P1 | P2 | P3 | none",
  "findings": [],
  "next_owner": "Hermes | Claude | Codex | User | none"
}
```

## Pitfalls

1. **Skipping the preview.** Governance initialization changes future agent behavior; broad writes need explicit approval.
2. **Diffing preview root against repo root.** This can include `.git`, generated files, and unrelated paths. Compare only approved target files or list the preview tree.
3. **Treating pre-existing untracked files as initialized content.** Preserve them and record follow-up tasks instead.
4. **Putting operational rules in README.** README should orient humans; actor rules belong in scoped files.
5. **Skipping Codex because changes are docs-only.** Governance docs are executable context for future agents and deserve independent review.
6. **Ending at file creation.** Completion requires validation and a real final state report.

## Verification Checklist

- [ ] Existing repository state inspected before mutation
- [ ] Temp preview created outside the repo
- [ ] Exact target files and responsibilities shown to user
- [ ] Explicit approval received before writing
- [ ] Only approved files written
- [ ] Pre-existing untracked work preserved or separately approved
- [ ] Local validation commands run and reported
- [ ] Independent read-only Codex review run for governance changes
- [ ] Final report includes Codex verdict, validation evidence, and remaining follow-up tasks

## References

- `references/hercules-skills-governance-init-2026-07-05.md` — concrete case study for initializing the `hercules-skills` repository.
