# Candidate Skills Archive

This directory preserves skill candidates that were reviewed during the
Hercules skill-pack reconciliation rounds but were **not** promoted to the
core runtime skill pack in the relevant pass. They are kept here as reference,
case-study, or future-promotion material. They are **not** runtime-loaded:
Hermes loads skills only from `skills/<skill>/SKILL.md` at the repository
root, so a `SKILL.md` file under this directory is never discovered as a
live skill.

## Why these are archived

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

## How to promote a candidate later

1. Decide whether the candidate is truly a new core atom or whether its
   unique content should be merged into an existing skill's `references/`
   or `templates/`.
2. If it should be a standalone core skill, move the directory back:
   ```bash
   mkdir -p skills/<candidate>
   mv docs/ai-collaboration/candidate-skills/<candidate>/SKILL.md skills/<candidate>/SKILL.md
   ```
3. Add the skill name to the core skill lists in `README.md` and
   `docs/ai-collaboration/ARCHITECTURE.md`.
4. Fix any broken intra-file references (e.g. missing `references/*.md`
   links) noted in `docs/ai-collaboration/TASKS.md`.
5. Run `python3 scripts/validate-skill-pack.py` and confirm zero errors.
6. Leave the task in `待复核` for Codex review before considering the
   promotion complete.

## Layout

```text
docs/ai-collaboration/candidate-skills/
├── README.md                                  (this file)
├── real-game-closed-loop-validation/SKILL.md
├── game-mechanics-telemetry-validation/SKILL.md
├── game-telemetry-closed-loop-validation/SKILL.md
├── repository-governance-initialization/SKILL.md
└── scoped-codex-review-packets/SKILL.md
```
