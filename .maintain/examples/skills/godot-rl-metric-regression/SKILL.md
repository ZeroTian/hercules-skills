---
name: godot-rl-metric-regression
description: "Use when evaluating Godot RL baseline-vs-candidate gameplay changes with real inference, telemetry provenance, diagnose reports, objective.score, and artifact-backed ACCEPTED/REJECTED decisions."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, godot, rl, metric-regression, telemetry, artifacts, evaluation]
    related_skills: [godot-wsl-artifact-validation, hercules-collaborative-agent-workflow, evaluation-closed-loop-orchestration]
---

# Godot RL Metric Regression

## When to use

Use this skill when deciding whether a Godot RL gameplay/layout candidate is actually better than baseline, especially when the candidate is applied only in `.artifacts/` and must be judged by real Godot inference, telemetry, `diagnose.py`, and `objective.score()`.

Typical cases:

- baseline vs candidate scene comparison
- CombatGate / obstacle / level-layout candidates
- verifying that an issue reduction is a real gameplay improvement rather than a side effect of failure
- producing a machine-readable `summary.json` with `ACCEPTED` or `REJECTED`

For WSL/Windows Godot path and probe details, also load `godot-wsl-artifact-validation`.

## Core workflow

1. Create a unique artifact directory, e.g. `.artifacts/taskNNN_<topic>_<timestamp>/`.
2. Copy the full Godot project into baseline and candidate copies with `.godot/`, `rec/`, and old telemetry excluded.
3. Apply the candidate only to the candidate copy unless the task explicitly authorizes source edits.
4. Run cheap gates before inference: structural parser/safe-anchor checks, `.tscn` sanity, and Godot `--import` for both copies.
5. Run baseline and candidate inference with the same model, scene, speedup, seed, episode budget, and isolated `TELEMETRY_DIR`.
6. Immediately archive `/tmp/rl_infer.log` and `/tmp/infer_godot.log` after each run; these fixed paths are overwritten by the next run.
7. Validate every telemetry JSONL with `evaluation.validate_telemetry(scene=..., model=..., speedup=..., min_episodes=...)`.
8. Recompute `objective.score(report)` from the validated report; do not trust a copied summary alone.
9. Compare score, completion rate, term distribution, issues, combat/behavior counters, and raw Godot event lines.
10. Write `summary.json` and a Hermes verification artifact that include the verdict, rationale, paths, commands, and next action if rejected.
11. Run targeted tests, `git diff --check`, and source-scene diff guards before handing to Codex.

## Acceptance rules

`objective.score()` is lower-is-better. A candidate can be `ACCEPTED` only when the evidence supports a real gameplay improvement, not just an issue disappearing from the report.

Require at least:

- candidate score does not regress under the chosen acceptance criterion
- completion rate does not collapse relative to baseline
- candidate does not introduce high-severity structural/tuning failures such as `difficulty_too_hard` or `done_reason_skew`
- the target issue improves for a gameplay-valid reason visible in logs/telemetry
- protected source files, reward, telemetry, model, and measurement surfaces remain unchanged unless explicitly in scope

If these conditions are not met, produce `REJECTED` with a precise `next_action` such as `retrain_policy_for_combat_gate`, `combat_gate_position_sweep`, or `combat_reward_or_curriculum_followup`.

## Pitfall: disappearing issues can be false improvement

Do not treat an issue disappearing from `diagnose` as proof of improvement. Some rules only fire when the player reaches a meaningful state. For example, `combat_bypassed` may disappear simply because a wall reduces `completion_rate` to zero and the player never reaches the goal.

For combat-gate candidates, inspect these together:

- raw Godot events: `CROSS GAP`, `DONE GOAL`, `DONE HP`, `DONE FALL`, `KILL` if available
- `completion_rate` and `term_distribution`
- `damage_dealt`, `kill_count`, `enemy_alive_at_goal_rate`
- candidate end position relative to the gate/obstacle

If `damage_dealt=0` and `kill_count=0`, a gate-open-on-kill mechanic has not been exercised by the policy; the correct result is usually `REJECTED` plus a training-side next action, not a structural acceptance.

## Evidence checklist

- [ ] baseline and candidate telemetry are from this run and pass provenance validation
- [ ] Python logs contain connection and completion markers
- [ ] Godot logs contain handshake plus real gameplay terminal events
- [ ] reports and scores are recomputed from the exact JSONL files
- [ ] candidate artifact differs from baseline only in the intended scoped files
- [ ] protected source scene diff is empty when required
- [ ] verdict is `ACCEPTED` or `REJECTED` with clear rationale
- [ ] next action is scoped and does not overclaim beyond the evidence

## References

- `references/combat-gate-regression.md` — session-derived notes from a CombatGate candidate that looked promising structurally but was rejected because the fixed policy never attacked or killed the enemy.
