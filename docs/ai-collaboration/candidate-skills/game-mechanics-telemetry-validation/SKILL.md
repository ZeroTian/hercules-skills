---
name: game-mechanics-telemetry-validation
description: Use when validating game/RL/testbed projects where success depends on gameplay semantics such as combat, hazards, pickups, resources, stealth, or enemy threat — ensures mechanics are executable, observable in telemetry, diagnosable, and not merely inferred from completion rate.
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, validation, game-dev, godot, reinforcement-learning, telemetry, diagnostics]
    related_skills: [real-game-closed-loop-validation, systematic-debugging, test-driven-development]
---

# Game Mechanics Telemetry Validation

## Overview

Use this skill when a game/RL loop appears to work but the user questions whether the actual gameplay mechanic is real. Completion rate, score, episode length, and terminal reason are not enough to validate mechanics like enemy threat, damage, combat, hazards, pickups, resources, stealth detection, or required interactions.

The goal is to make each important mechanic:

1. **Executable** — the real game code changes state when the mechanic occurs.
2. **Probeable** — a headless or scripted RED test can reproduce failure and GREEN after the fix.
3. **Observable** — telemetry records the semantic event/metric.
4. **Diagnosable** — report rules flag missing or bypassed mechanics.
5. **Optimizable** — LLM/optimizer prompts receive the semantic evidence rather than optimizing only geometry or reward numbers.

## Trigger Conditions

Load this skill when:

- The user says a visible mechanic does not actually matter, e.g. “the enemy doesn’t hurt me,” “hazards are decorative,” or “the agent just ignores combat.”
- A real-game validation succeeded on path/score metrics but may have missed a semantic requirement.
- Telemetry episodes have empty `events` / `metrics` despite important mechanics being present in the scene.
- Reward code includes terms such as hurt/damage/kill/resource cost, but there is no proof those signals can be triggered in real gameplay.
- You need to design diagnose rules like `enemy_no_threat`, `combat_bypassed`, `hazard_no_effect`, or `resource_irrelevant`.

## Procedure

### 1. State the validation scope precisely

Do not collapse all success into “the game loop works.” Say which layer is validated:

- structural/path validation;
- combat/threat validation;
- resource economy validation;
- hazard validation;
- subjective/experience reporting.

A structural optimizer success (bad platform → fall issue → patch → goal) does **not** imply combat or enemy threat works.

### 2. Build a RED-capable mechanic probe

Create or run the smallest real-game probe that asserts the semantic state directly:

- enemy threat: place player in attack/contact range, run fixed physics frames, assert `player.health < initial_health`;
- hazard: place player in hazard, assert damage/death/status event;
- pickup: place player on pickup, assert inventory/resource delta;
- stealth/detection: place actor in detection cone, assert alert state;
- resource cost: perform action, assert resource decreases.

Probe real scene code when possible. Avoid only checking that the scene loads or that the policy reaches the goal.

### 3. Isolate where the mechanic fails

When a mechanic does not trigger, distinguish these classes before fixing:

- state API failure: direct `take_hit()` / `apply_damage()` / resource mutation does not work;
- collision/layer/mask failure: overlap never becomes true;
- hit-frame/timing failure: overlap becomes true only before/after the damage frame;
- facing/range/AI transition failure: agent enters wrong state or attacks away from target;
- reset/telemetry failure: mechanic works but is not recorded or is reset before episode output.

A useful probe pattern is: first run automatic behavior, then manually invoke the semantic function while overlap/contact is known true. If manual invocation changes state, the API works and the bug is in timing/range/AI/collision.

### 4. Add semantic telemetry

For each mechanic that matters, add episode metrics/events that diagnose can aggregate. For combat/threat, prefer at least:

- `hp_lost`
- `hurt_count`
- `damage_dealt`
- `kill_count`
- `enemy_alive_at_goal`

When possible, also record:

- `enemy_contact_frames`
- `enemy_attack_attempts`
- `enemy_attack_hits`
- `hazard_contact_frames`
- `mechanic_required` / design intent flags when bypassing is or is not allowed.

### 5. Add diagnose rules for missing semantics

Examples:

- `enemy_no_threat`: enemies exist and the agent completes or survives while `hp_lost == 0` and `hurt_count == 0` across sufficient exposure.
- `combat_bypassed`: design requires combat, but episodes finish with `enemy_alive_at_goal > 0` and no combat events.
- `damage_signal_unreachable`: reward has hurt/damage/kill terms, but corresponding telemetry metrics remain zero.
- `hazard_no_effect`: hazard contact is observed but damage/status/death never occurs.
- `resource_irrelevant`: a resource-gated action succeeds without resource cost or scarcity.

### 6. Feed semantic evidence into optimizer prompts

Optimizer/LLM propose layers should see issue IDs and evidence fields, not just scalar reward. Include the semantic metrics and the target mechanic in stage prompts so the LLM does not “fix” the wrong layer (e.g. moving platforms or tuning rewards while enemy damage remains unreachable).

### 7. Verify no Goodhart regression

If a subjective/report-only layer exists, keep soft issues out of objective gates unless explicitly designed otherwise. Semantic objective issues like `enemy_no_threat` can be objective diagnostics when backed by telemetry; subjective preference judgements should remain report-only unless the project has a defined acceptance policy.

## Verification Checklist

- [ ] A RED mechanic probe reproduces the exact failure.
- [ ] Manual semantic function invocation was used when needed to isolate API vs collision/timing/AI failure.
- [ ] The fix makes the real probe GREEN.
- [ ] Episode telemetry contains the semantic event/metric.
- [ ] Diagnose has fixture tests for the missing/bypassed mechanic.
- [ ] Real telemetry or fixtures prove the diagnose rule fires on the bad case.
- [ ] Optimizer/LLM prompt/report receives semantic evidence.
- [ ] Existing structural/path optimization tests still pass.
- [ ] The final report distinguishes which mechanic class was validated.

## Support Files

- `references/combat-semantics-blind-spot.md` — FireKnight-style session pattern: structural optimizer succeeded, but enemy threat was decorative until probed with semantic telemetry.
