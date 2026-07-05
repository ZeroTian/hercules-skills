---
name: skill-pack-governance-validation
description: "Validate a portable workflow skill pack before commit, push, migration, or handoff: runtime loading, archived candidate safety, validator/static checks, bootstrap audit-only, staged privacy scan, and commit-package readiness."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, skills, validation, governance, commit-package, migration]
    related_skills: [workflow-skill-pack-audit, hercules-skill-pack-management, hercules-agent-capability-preflight, coding-agent-orchestration]
---

# Skill Pack Governance Validation

## Overview

Use this class-level skill after auditing or changing a portable workflow skill pack, especially before commit/push or migration claims. It turns "the files look right" into evidence that the pack is usable in the current runtime and safe to package.

This skill complements `workflow-skill-pack-audit` and `hercules-skill-pack-management`: those govern classification/reconciliation and repository layout; this governs the acceptance pass after changes are made.

## When to Use

Use when the user asks:

- whether the skill group has actually been practiced or only documented;
- to continue from a completed skill-pack audit toward commit/push;
- to prepare a commit package for a skill-pack repository;
- to validate runtime skill loading, archived candidate safety, bootstrap readiness, or migration readiness;
- to decide whether it is safe to report "ready" after Claude/Codex/validator work.

## Procedure

1. **Runtime layout smoke test.** Check symlink target, runtime `skills/*/SKILL.md`, tracked/staged skill list, archived candidates, double nesting, and accidental symlinks inside `skills/`.
2. **Skill loading test.** Load representative core skills with `skill_view`. Try one archived candidate and expect it not to load from the runtime skill library.
3. **Static validation.** Run the skill-pack validator, `git diff --check`, and shell syntax checks for bundled scripts.
4. **Bootstrap audit-only.** Run the dependency doctor in check-only mode so the workflow proves it can inspect Claude/Codex/plugins/MCP/external skills without mutating setup.
5. **Actual workflow evidence.** Record whether the pack was exercised end-to-end, for example Hermes preflight → Claude implementation → Hermes verification → Codex review → TASKS closure.
6. **Commit package acceptance.** If moving toward commit/push, stage the intended package only, re-run validation against staged state, run a staged-file privacy scan, then report staged/not-committed/not-pushed until the user explicitly authorizes commit/push.
7. **Document gaps.** Separate current-runtime readiness from fresh clone/fresh machine readiness. Do not claim migration readiness until a post-push clone-style test has run.

## Verification Checklist

- [ ] `~/.hermes/skills/hercules` resolves to the intended repository `skills/` directory
- [ ] visible runtime skills match tracked/staged core skills
- [ ] archived candidates live outside runtime loading and do not resolve via `skill_view`
- [ ] representative core skills load successfully
- [ ] validator returns 0 errors / 0 warnings / 0 signals
- [ ] `git diff --check` and relevant script syntax checks pass
- [ ] bootstrap/dependency doctor passes in audit-only mode
- [ ] staged package has no unstaged drift before commit
- [ ] staged privacy scan finds no sensitive filenames or secret-like content
- [ ] final report states what was practiced and what remains untested

## References

- `references/usability-and-commit-package-validation.md` — command recipe and reporting pattern from the Hercules round-2 usability/commit-package acceptance pass.

## Pitfalls

- Do not treat static validator success as runtime usability proof; include `skill_view` loading and archived-candidate non-loading checks.
- Do not treat current-machine runtime success as fresh-machine migration proof.
- Do not commit or push just because files are staged; wait for explicit user authorization.
- If a staged file is edited again, re-stage it and re-run staged validation.
- Codex P3 ledger/evidence fixes often require re-staging the edited file and a narrow recheck of only the affected task/CR before closure.
- Promoted skills may reference `references/`, `templates/`, or `scripts/` files that the generic validator does not check; confirm every linked path exists before claiming acceptance.
- Treat runtime usability, staged package readiness, and post-push clone acceptance as three distinct evidence buckets — passing one does not imply passing the others.
- When searching governance ledgers for stale review markers, distinguish real tasks from template examples.
