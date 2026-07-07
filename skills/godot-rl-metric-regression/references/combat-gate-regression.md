# CombatGate Regression (Session Notes)

Session-derived notes from a CombatGate candidate that looked promising structurally but was REJECTED after real Godot RL inference because the fixed policy never attacked or killed the enemy. Supports `skills/godot-rl-metric-regression/SKILL.md`.

## Candidate

- Structural change: add a CombatGate obstacle that forces the agent to defeat an enemy before progressing.
- Applied only in `.artifacts/<run>/candidate/`; baseline copy unchanged.
- Cheap gates (`.tscn` sanity, `godot --import`) passed for both copies.

## Why it looked promising

- `diagnose.py` reported `combat_bypassed` on baseline.
- After adding the gate, the candidate's `diagnose` report no longer listed `combat_bypassed`.

## Why it was REJECTED

The issue disappeared for the wrong reason. Inspecting raw Godot events and telemetry together:

- `completion_rate` collapsed relative to baseline.
- `damage_dealt=0` and `kill_count=0` — the fixed policy never engaged the enemy.
- `DONE FALL` / `DONE HP` dominated the term distribution; `DONE GOAL` was rare or absent.
- The gate was never opened because the enemy was never killed; the player just failed earlier.

`combat_bypassed` disappeared because the player never reached the combat state, not because combat was fixed. This is a false improvement.

## Evidence inspected together

- raw Godot events: `CROSS GAP`, `DONE GOAL`, `DONE HP`, `DONE FALL`, `KILL`
- `completion_rate` and `term_distribution`
- `damage_dealt`, `kill_count`, `enemy_alive_at_goal_rate`
- candidate end position relative to the gate/obstacle

## Verdict artifact

```json
{
  "verdict": "REJECTED",
  "rationale": "combat_bypassed disappeared because completion_rate collapsed and the policy never killed the enemy; false improvement",
  "next_action": "retrain_policy_for_combat_gate",
  "candidate_score": "<worse than baseline under chosen criterion>",
  "protected_surfaces_unchanged": ["reward", "goal", "fall", "telemetry", "diagnose", "model", "train_map.tscn"]
}
```

## Lesson

Do not treat an issue disappearing from `diagnose` as proof of improvement. Some rules only fire when the player reaches a meaningful state. For combat-gate candidates, require `damage_dealt > 0` and `kill_count > 0` (or an explicit gate-opened event) before accepting a structural change.
