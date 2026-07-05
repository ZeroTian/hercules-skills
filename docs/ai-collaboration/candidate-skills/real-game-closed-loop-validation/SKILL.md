---
name: real-game-closed-loop-validation
description: "Use when validating game/RL/evaluation projects with real executable runs instead of paper plans: healthy run, controlled failure, repair, optimizer automation, telemetry/report evidence, and artifact-isolated temporary repos."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, validation, godot, reinforcement-learning, telemetry, optimization-loop]
    related_skills: [hercules-collaborative-agent-workflow, coding-agent-orchestration, systematic-debugging]
---

# Real Game Closed-Loop Validation

## Overview

Use this skill when the user asks to prove a game/RL/evaluation project with a real executable run rather than more documentation or plans. The goal is to validate the full loop with grounded evidence: runtime logs, telemetry JSONL, diagnosis reports, patches, gates, and accept/rollback outcomes.

This is a class-level workflow for real-game validation. It is not limited to one repository, but it was hardened on a Godot + stable-baselines3 PPO + telemetry/diagnose optimizer loop.

## When to Use

Use when the task asks to:

- run a real game/testbed experiment;
- prove an RL/evaluation loop works end-to-end;
- compare healthy, failed, and repaired gameplay behavior;
- validate an optimizer that patches game content or tunables;
- avoid paper-only claims about telemetry, diagnosis, gates, or LLM patching.

## Procedure

1. **Inspect the live runtime contract.** Read the runner, inference server, telemetry writer, diagnose/report code, scene files, and model-loading code. Confirm observation/action spaces before running long tests.
2. **Run a healthy real path.** Use a known-compatible model and real scene. Save stdout, Python/inference log, Godot/game log, telemetry JSONL, and report under a unique `.artifacts/<run>/` directory.
3. **Run a controlled failure path.** Use either a space-compatible weak model or a copied project with a legal-but-bad game-content change. Do not alter reward, telemetry, termination geometry, or diagnosis just to create a failure.
4. **Run a repair path.** Patch only the copied artifact project. Run cheap gates first (`.tscn` sanity/import/smoke if applicable), then real inference. Compare against the failure path with the same model/seed/budget when possible.
5. **Validate the automation layer separately.** If the optimizer uses git snapshots/commits, initialize a temporary git repo inside `.artifacts/`, commit the bad fixture, add an ignore file for generated outputs, and let the optimizer patch/commit/rollback only there.
6. **Report evidence, not vibes.** Include model, scene, patch, episode count, completion rate, mean length/return, termination distribution, issue IDs, raw event lines, artifact paths, and whether source files were touched.

## Godot/RL Copy Pattern

Prefer `rsync` over manual whitelists when copying a Godot project for artifact validation:

```bash
rsync -a \
  --exclude='.godot/' \
  --exclude='rec/' \
  --exclude='rl/telemetry/' \
  "$SRC_PROJECT/" "$ARTIFACT_PROJECT/"
```

Then run Godot import inside the copied project so `.godot/` is regenerated.

## Optimizer Automation Pitfalls

- Do not trust wrapper success alone. Verify Python connection logs, game logs, fresh telemetry JSONL, and `report.json`.
- Put logs/metadata under ignored `.artifacts/`; root-level untracked files can trip Gate 0b in gate-sensitive optimizers.
- For anchor-based `.tscn` or scene patching, feed the LLM the **current** target snippet from the copied project, not a hardcoded initial snippet.
- If an LLM repeatedly chooses `tunable_search` for fall/death/done-reason-skew issues, strengthen the prompt: when fall/death dominates or recent tunable searches had no improvement, prefer a structural patch using the provided anchor.
- Keep the current bad snippet as `patch.anchor`; provide known-good coordinates or examples only as reference for `patch.new`.
- Record the complete LLM plan in artifacts/memory when possible. Summaries alone are insufficient for debugging wrong change type, schema retry, anchor mismatch, gate failure, or no metric improvement.
- A one-episode run can force a branch for automation smoke tests; do not present it as product-level balance evidence.

## Verification Checklist

- [ ] Runner/import checks passed or blockers are explicit
- [ ] Model observation/action spaces match the live environment
- [ ] Healthy real run produced telemetry and no high issues
- [ ] Controlled failure produced raw game failure events and high issues
- [ ] Repair/optimizer run used an artifact copy or temporary repo, not source files
- [ ] Gates ran before acceptance
- [ ] Fresh telemetry/report show improvement
- [ ] Accepted patch/diff is captured, or rollback/no-accept is explained
- [ ] Source repo pollution status is checked and reported

## Reference

See `references/godot-rl-stage2-optimizer.md` for a condensed real-session trace covering a Godot PPO testbed, dynamic anchor repair, prompt hardening, and successful automatic stage2 structural acceptance.
