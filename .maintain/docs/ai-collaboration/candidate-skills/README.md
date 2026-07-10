# Candidate Skills Archive

This directory preserves skill candidates that were reviewed during the
Hercules skill-pack reconciliation rounds but were **not** promoted to the
core runtime skill pack in the relevant pass. They are kept here as reference,
case-study, or future-promotion material. They are **not** runtime-loaded:
Hermes loads skills only from `skills/<skill>/SKILL.md` at the repository
root, so a `SKILL.md` file under this directory is never discovered as a
live skill.

## Historical disposition

The table below is an immutable snapshot of the earlier reconciliation
decisions. Skill names and paths in the reasons describe the repository at the
time of those decisions; they are not current runtime or command references.

### Why these were archived

Each candidate was visible-untracked under `skills/` during the audit. The
reconciliation round (see `docs/ai-collaboration/SKILL_GROUP_AUDIT.md`)
decided per candidate:

| Candidate | Disposition | Reason |
|---|---|---|
| `real-game-closed-loop-validation` | archived (domain) | Godot/RL/evaluation real-run validation. Domain-specific, not core Hercules orchestration. The linkage to the collaborative workflow already exists via `skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md`. |
| `game-mechanics-telemetry-validation` | archived (domain) | Game/RL mechanic telemetry validation. Pairs with the real-game validation candidate rather than core orchestration. |
| `game-telemetry-closed-loop-validation` | archived (domain) | Game/RL semantic telemetry and closed-loop validation. Useful domain material, but it belongs with the game validation candidates rather than the core Hercules workflow pack. |
| `repository-governance-initialization` | archived (duplicate/case-study) | Restates the inspect→preview→approve→apply→verify→review loop already covered by `hermes-project-init-orchestration` and the `hercules-project-init-workflow` entry wrapper. Unique steps should be folded into the existing project-init skill as a case study. |
| `scoped-codex-review-packets` | archived (overlap/reference) | Useful bounded Codex review packet pattern, but overlaps the review-loop family (`coding-agent-orchestration`, `iterative-agent-code-review`, `cross-agent-review-loop`). Merge its packet contract into that family before tracking as a standalone core skill. |
| `artifact-driven-evaluation-loops` | archived (overlap/reference) | Evaluated-system loop variant. Overlaps the canonical `evaluation-closed-loop-orchestration` atom; unique details (structured `BLOCKED_SCOPE_INSUFFICIENT` outcome, field-preservation contract across handoffs) were folded into that skill before archiving. |
| `artifact-handoff-orchestration` | archived (overlap/reference) | Handoff/BLOCKED orchestration variant. Overlaps `evaluation-closed-loop-orchestration`; unique safe-anchor validator checklist (positive allowlist + concept denylist, whole-block matching) was folded into that skill before archiving. |
| `autonomous-evaluation-loops` | archived (overlap/reference) | Autonomous evaluation loop variant. Overlaps `evaluation-closed-loop-orchestration`; unique modification-request schema and instance-fixing-vs-system-capability distinction were folded into that skill before archiving. |

## How to promote a candidate later

The current runtime invariant is exactly five Skills. A candidate must not be
moved directly into `skills/` as a routine maintenance action.

1. Prefer merging reusable content into one of the five runtime Skills or
   preserving it under `.maintain/skills/`, `.maintain/examples/`, or this
   archive.
2. Treat adding a sixth runtime Skill as an explicit product-architecture
   change. Start with a failing exact-runtime contract test and obtain review.
3. If that architecture change is approved, update
   `.maintain/scripts/validate-skill-pack.py`,
   `.maintain/docs/ai-collaboration/SKILL_NAVIGATION.md`, and
   `.maintain/docs/ai-collaboration/ARCHITECTURE.md` together.
4. Run `python3 .maintain/scripts/validate-skill-pack.py --strict` and
   `.maintain/scripts/check-package.sh` before requesting Codex review.

## Layout

```text
.maintain/docs/ai-collaboration/candidate-skills/
├── README.md                                  (this file)
├── artifact-driven-evaluation-loops/SKILL.md
├── artifact-handoff-orchestration/SKILL.md
├── autonomous-evaluation-loops/SKILL.md
├── game-mechanics-telemetry-validation/SKILL.md
├── game-telemetry-closed-loop-validation/SKILL.md
├── real-game-closed-loop-validation/SKILL.md
├── repository-governance-initialization/SKILL.md
└── scoped-codex-review-packets/SKILL.md
```
