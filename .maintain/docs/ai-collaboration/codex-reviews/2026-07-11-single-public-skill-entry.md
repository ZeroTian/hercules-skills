# Codex Review — TASK-016 true single public Skill entry

- Date: 2026-07-11
- Scope: staged single-Skill runtime migration, router/references, initializer UX, validator, tests, and current governance
- Reviewer: independent Codex agent, read-only
- Initial result: FAIL
- Initial highest severity: Important
- Final result: PASS
- Final highest severity: none

## Findings and fixes

### TASK016-CR-001 — Important — nested `SKILL.md` escaped exact-one validation

- Evidence: the validator inspected only top-level `skills/*/SKILL.md`; a staged `skills/hercules/references/rogue/SKILL.md` still passed strict validation.
- Fix: enforce the exact full-path set `skills/hercules/SKILL.md` for both Git-tracked and visible recursive `SKILL.md` files.
- Regression coverage: `test_validator_rejects_nested_runtime_skill_file`.
- Recheck: FIXED. A staged-clone rogue Skill now returns exit 1 with tracked and visible scope errors.

### TASK016-CR-002 — Important — current governance still declared exact-five

- Evidence: root `AGENTS.md`, `CLAUDE.md`, `HERMES.md`, and the candidate promotion policy contradicted the exact-one runtime.
- Fix: make all four current surfaces declare exactly one runtime Skill and place reusable internal workflows under `skills/hercules/references/`.
- Regression coverage: `test_governance_instructions_enforce_exactly_one_runtime_skill`.
- Recheck: FIXED. Current-governance exact-five scan has no match.

## Final verification

- Focused finding recheck: PASS, 2/2.
- Full stdlib discovery: PASS, 96/96.
- Runtime contract: PASS, 31/31.
- Initializer contract: PASS, 10/10.
- Strict validator: PASS, 0 errors / 0 warnings.
- Package gate, staged fresh-clone smoke, Bash syntax, and cached diff check: PASS.
- Real Hermes command scan: `{'/hercules': 'hercules'}`.
- Managed symlink remains `~/.hermes/skills/hercules -> <checkout>/skills`.

## Final verdict

PASS — `TASK016-CR-001` and `TASK016-CR-002` are fixed; no new findings remain.
