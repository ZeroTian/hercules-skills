---
name: game-telemetry-closed-loop-validation
description: "Validate game/RL optimization loops with real engine probes, semantic telemetry, diagnose rules, and agent-reviewed task closure so gameplay issues are discovered by the project itself, not only by human observation."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, game-dev, godot, rl, telemetry, diagnosis, closed-loop-validation, tdd]
    related_skills: [hercules-collaborative-agent-workflow, coding-agent-orchestration, systematic-debugging, test-driven-development]
---

# Game Telemetry Closed-Loop Validation

## Overview

Use this skill when a game, simulation, RL environment, or automated optimizer appears to "work" by objective scores but may miss gameplay semantics. The goal is to prove not only that a loop runs, but that the project can observe, diagnose, and optimize the gameplay property the human cares about.

Core principle:

```text
Human-visible bug
  -> deterministic engine probe reproduces it
  -> telemetry exposes the semantic signal
  -> diagnose emits an explicit issue
  -> optimizer / LLM prompt can see the issue evidence
  -> real engine run proves the fix
  -> independent review closes the task
```

Do not stop at "the model reached goal" or "score improved" if the concern is gameplay meaning such as enemies, damage, combat, traps, resources, stealth, fairness, or puzzle constraints.

## When to Use

Use when:

- A Godot/Unity/game/RL testbed is evaluated by automated agents or optimizer loops.
- The user asks whether a game mechanic "really works".
- A policy can win while ignoring the intended mechanic.
- Reward code contains branches that may never be triggered in real play.
- Telemetry JSONL/report lacks semantic fields needed for diagnosis.
- You need a RED/GREEN real-engine proof for gameplay semantics.

## Workflow

1. **Separate loop success from gameplay success.** State clearly whether the current evidence proves structure/pathing, combat, economy, UX, or only wrapper execution.
2. **Read the mechanic path.** Trace scene nodes, collision layers/masks, signals, animation-method tracks, state machines, reward code, telemetry, and diagnose aggregation before changing anything.
3. **Build a deterministic engine probe.** Use a script/artifact that positions actors in a controlled scenario and prints the semantic state every N frames. For Godot, save under `.artifacts/<task>_*` and run with `Godot_console.exe --headless --path <project> --script <probe.gd>`.
4. **RED first.** Capture a failing probe/log that demonstrates the human concern (for example HP stays 100 while overlapping an enemy attack area).
5. **Fix the minimal mechanic.** Prefer fixing the intended mechanic path (attack timing/range/orientation/state) over masking the symptom with reward or goal changes. Add cooldown/one-shot guards when adding damage to avoid per-frame spam.
6. **Add semantic telemetry.** Record episode metrics for the property, not just return/length/term. Examples: `hp_lost`, `hurt_count`, `damage_dealt`, `kill_count`, `enemy_alive_at_goal`, `resource_spent`, `trap_triggered`, `objective_item_collected`.
7. **Add diagnose rules.** Create explicit issues such as `enemy_no_threat`, `combat_bypassed`, `trap_never_triggers`, or `objective_bypassed`. Ensure missing old metrics are safe defaults and do not create false positives when the mechanic is absent.
8. **Feed optimizer evidence.** Ensure reports/prompts include the semantic summary and issue evidence so LLM/optimizer layers can act on it. Avoid only optimizing geometry/reward scalars when the issue is semantic.
9. **Run real validation.** Verify with targeted tests, import/script checks, real engine probe, and at least one real policy/scripted episode that writes telemetry and diagnose report.
10. **Review and close.** For formal work, record RED/GREEN/REFACTOR evidence in `TASKS.md`, run Codex read-only review, then close only on PASS.

## Probe Pattern for Godot

A good headless probe:

- Loads the real scene with `load("res://...").instantiate()`.
- Positions the player and mechanic actor explicitly.
- Resets velocity/health/state needed for determinism.
- Runs a bounded number of `physics_frame` ticks.
- Prints the semantic state (`hp`, `min_hp`, state name, overlap count, actor positions).
- Exits non-zero when the semantic criterion fails.
- Uses explicit GDScript type annotations for variables that Godot cannot infer in headless scripts.
- Quits early once the GREEN condition is observed to avoid freed-node lifecycle noise.

## Telemetry / Diagnose Design Rules

- Metrics must be set before the episode record is finalized.
- Reset per-episode counters at environment/agent reset.
- Keep old telemetry compatible: absent metrics should aggregate to zero/false without crashing.
- Distinguish "mechanic absent" from "mechanic present but ineffective" with a field like `enemies_present` or `mechanic_expected`.
- Separate severity: no damage when enemies are present may be high; bypassing combat while still taking damage may be medium or design-dependent.
- Store residual risks explicitly, e.g. attack attempt/hit counters not yet emitted, single-seed validation only, or directional hitbox polish pending.

## Orchestration Pitfall

Creating a formal task for a game-semantic issue is not the end of the job. Unless the user asked only for planning, Hermes should continue the loop: capability preflight, Claude implementation if useful, inspect actual diff/artifacts, run real probes/tests, Codex review, then update the ledger. If Claude hits a turn cap after partial work, inspect the diff and either launch a narrow follow-up or finish a tightly scoped repair directly with real validation.

## Verification Checklist

- [ ] Real engine RED artifact proves the gameplay-semantic failure
- [ ] Minimal mechanic fix preserves intended design and avoids damage/reward spam
- [ ] Semantic episode metrics are emitted and reset correctly
- [ ] Diagnose emits explicit issue(s) with evidence and handles missing old metrics
- [ ] Optimizer/LLM report can see the semantic issue evidence
- [ ] Targeted unit tests pass
- [ ] Engine import/script check has no parse/script errors
- [ ] Real engine GREEN probe proves the mechanic now works
- [ ] Real episode telemetry demonstrates self-discovery or improved behavior
- [ ] Independent review passes before closing formal tasks

## References

- `references/task010-enemy-threat-self-diagnosis.md` — concrete Godot RL case: FireKnight looked like an enemy but did not damage the player; fix used attack-state one-shot hit fallback, combat telemetry, diagnose rules, real probe, inference, and Codex PASS.
