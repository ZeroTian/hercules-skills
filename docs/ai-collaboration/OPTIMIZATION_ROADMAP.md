# Hercules Skill Pack Optimization Roadmap

Last updated: 2026-07-08

## Purpose

This roadmap turns the `codex-plugin-cc` comparison and Hercules optimization proposal into traceable, reviewable work. The goal is to keep the repository in a state where each phase can be answered with evidence:

- What task ID owns it?
- What files are in scope?
- What is the acceptance gate?
- Which command or review proves it?
- What remains explicitly untested?

## Status summary

| Phase | Task | Status | Evidence |
|---|---|---|---|
| P0 clean package | TASK-008 | Completed / committed as `14343ca` | Codex review `docs/ai-collaboration/codex-reviews/2026-07-08-task008-round4-skill-pack-reconciliation.md`; validator 0 errors / 0 warnings |
| P0 residual cleanup before push | TASK-009 | Completed / committed as `304b0d1` | Codex review `docs/ai-collaboration/codex-reviews/2026-07-08-task009-residual-cleanup.md`; `staged-commit-package-governance` promoted to core atom; Godot reference improvement kept; validator 0 errors / 0 warnings |
| P1 productized entry + landing | TASK-010 | Completed / staged for auto-commit | Codex review `docs/ai-collaboration/codex-reviews/2026-07-08-task010-productized-entry.md`; wrapper smoke tests pass |
| P1/P2 release gate + migration proof | TASK-011 | Backlog | validator `--json` / `--strict`, linked-file deep checks, fresh-clone smoke script |
| P2 information architecture | TASK-012 | Backlog | skill role metadata/composition map + TASKS active/archive split |
| P2/P3 absorption + outreach package | TASK-013 | Backlog | external-tool absorption workflow + `docs/WHY_HERCULES.md` + demo/tiny example decision |

## TASK-008 — P0 clean package

Completed in commit `14343ca`.

Delivered:

- promoted four runtime skills;
- archived three overlapping loop variants;
- recorded `codex-plugin-cc` as optional external Claude plugin dependency and governance policy;
- saved Codex review records;
- validated with validator, diff checks, bash syntax, bootstrap audit-only, privacy scan, and Codex recheck.

Residual outside TASK-008, now addressed by TASK-009 package:

- `skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md` is kept as a durable reference improvement;
- `skills/staged-commit-package-governance/` is promoted to a core atom with a round-4 case-study reference file.

TASK-009 passed Codex recheck and was committed as `304b0d1`; not pushed.

## TASK-009 — P0 residual cleanup before push

Goal: decide and package the two currently visible residual worktree items.

Scope:

- `skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md`
- `skills/staged-commit-package-governance/SKILL.md`

Dispositions (decided):

- `staged-commit-package-governance`: PROMOTE/TRACK as core atom. Captures the round-4 staged-package boundary / ledger-truth / narrow Codex recheck pattern. Complements `skill-pack-governance-validation` (not redundant). Reference file `references/round4-staged-package-boundary.md` added. Staged by Hermes; Codex recheck PASS.
- `real-godot-closed-loop-validation.md`: KEEP/TRACK as a standalone durable reference improvement. Three durable Godot validation additions kept (timely `/tmp` log copy, combat-gate false-improvement detection, animation-driven hitbox timing chain). Not deleted or rewritten.

Acceptance gates:

- disposition recorded for each residual item: commit as standalone improvement, merge into an existing skill/reference, archive as candidate, or discard if explicitly approved;
- validator returns 0 errors / 0 warnings;
- `git diff --check` and, if staged, `git diff --cached --check` pass;
- Codex reviews any staged package that changes runtime skills or governance ledgers;
- final report separates committed, staged, unstaged, and unpushed state.

## TASK-010 — P1 productized entry + landing

Goal: reduce adoption friction by giving users a small command surface and a clearer README first screen.

Candidate deliverables:

- `scripts/hercules` wrapper with at least:
  - `hercules validate`
  - `hercules bootstrap --check`
  - `hercules status`
  - `hercules package`
  - `hercules doctor`
- README landing rewrite that states:
  - Hermes orchestrates;
  - Claude Code implements;
  - Codex independently reviews;
  - real commands verify the result.
- Quickstart that can be copied on a new machine.

Acceptance gates:

- wrapper subcommands have deterministic exit codes;
- `scripts/hercules validate` runs validator, diff check, and bash syntax check;
- README remains reader-facing and does not duplicate long agent rules;
- shell syntax and validator pass;
- Codex review confirms the CLI/README lowers entry friction without weakening governance.

## TASK-011 — P1/P2 release gate + migration proof

Goal: turn the validator and smoke checks into release-gate tooling.

Candidate deliverables:

- `python3 scripts/validate-skill-pack.py --json`
- `python3 scripts/validate-skill-pack.py --strict`
- untracked candidate disposition checks;
- deeper linked-file checks for `references/`, `templates/`, and `scripts/` mentioned by `SKILL.md` files;
- `scripts/smoke-fresh-clone.sh` or equivalent repo-level fresh-clone smoke test.

Acceptance gates:

- JSON output is machine-readable by Hermes/Codex/CI;
- strict mode fails on warnings intended to block release;
- current repo passes normal validation and documents any strict-mode exceptions;
- smoke script uses a temporary clone/workdir and does not mutate the source repo;
- Codex review checks validator behavior, not just docs.

## TASK-012 — P2 skill information architecture and ledger scaling

Goal: make the current core skill pack easier to navigate and keep TASKS manageable.

Candidate deliverables:

- role/maturity metadata convention, e.g. `entry`, `atom`, `specialized`, `archived`;
- composition map maintained in `SKILL_GROUP_AUDIT.md` or a dedicated architecture doc;
- TASKS active/archive split, e.g. `docs/ai-collaboration/tasks/archive-2026-07.md`;
- validator checks for role/list consistency where practical.

Acceptance gates:

- new users can identify entry skills versus atoms without reading every skill;
- current active TASKS remains compact;
- archived task records stay linked and searchable;
- validator still passes and Codex review confirms no ledger truth was lost.

## TASK-013 — P2/P3 absorption workflow + outreach package

Goal: make the `codex-plugin-cc` research/absorption pattern reusable and communicate why Hercules is different.

Candidate deliverables:

- external-tool/repo absorption workflow, likely in `agent-plugin-dependency-governance` or `open-ended-research-orchestration`;
- `docs/WHY_HERCULES.md` comparing:
  - `codex-plugin-cc` lets Claude call Codex;
  - Hercules makes Claude + Codex collaboration governable, auditable, and safe;
- optional demo/tiny example repository or transcript plan.

Acceptance gates:

- future request “研究这个 repo 能不能吸收到我们的技能组” has a standard workflow;
- decision output includes dependency-vs-vendor, risks, bootstrap changes, governance boundary, validation evidence, and Codex review;
- outreach docs do not overclaim beyond actual runtime evidence;
- Codex review confirms the comparison is accurate and fair.

## Traceability rules

Every formal task from this roadmap should preserve:

- a `TASKS.md` task ID;
- acceptance checklist;
- validation command output summary;
- Codex review record when the task changes runtime skills, validator behavior, governance ledgers, or release/package state;
- explicit residual risks such as no fresh-machine test or no push authorization.
