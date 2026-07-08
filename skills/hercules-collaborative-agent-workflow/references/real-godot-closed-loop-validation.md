# Real Godot Closed-Loop Validation Pattern

Use when the user challenges a Godot/RL/evaluation project as “paper only” and asks for proof with a real game run.

## Durable pattern

1. Run a real healthy path first.
   - Use the actual Godot project and scene.
   - Confirm Godot import/script check passes.
   - Confirm model observation/action spaces match the live agent (`stable_baselines3.PPO.load(...).observation_space/action_space`).
   - Run inference with an isolated `TELEMETRY_DIR` under `.artifacts/<run>/telemetry`.
   - Save stdout, Python server log, Godot log, JSONL telemetry, and `report.json` in the same artifact directory.

2. Run a real failure path.
   - Prefer a behaviorally weak but space-compatible model, or a copied project with a legal-but-bad level change.
   - Do not modify reward, telemetry, diagnosis, termination geometry, or protected measurement files just to create a failure.
   - Verify the failure appears in raw Godot logs and telemetry, not only in a summarized report.

3. Run a repair path.
   - Copy the project into an artifact directory and patch only the copy.
   - Run cheap gates before expensive inference: `.tscn` sanity, Godot `--import`, then smoke/real inference.
   - Compare failure vs repair with the same model, scene, seed, speedup, and episode budget where possible.

4. Validate the automation layer separately.
   - If the optimizer requires `git`, initialize a temporary git repo in the copied artifact project, not in the source repo.
   - Commit the bad fixture as the temporary repo baseline.
   - Add a local `.gitignore` before committing so `.artifacts/`, `.godot/`, `rec/`, and telemetry/log outputs do not trip Gate 0b as unrelated tracked changes.
   - Keep orchestrator logs/metadata under ignored `.artifacts/`; do not write untracked metadata at the temporary repo root before running gate-sensitive optimizers.
   - Expect the optimizer to early-stop if the fresh baseline has no high issue. That is a real threshold calibration result, not an optimizer failure. To exercise the LLM/patch/gate branch, make the copied defect strong enough or lower the diagnostic threshold deliberately for the experiment.

5. Report in a table-like comparison.
   - model, project copy, patch, episodes, completion rate, mean length, mean return, term distribution, issue IDs, artifact paths.
   - Include the raw Godot event lines (e.g. `DONE FALL`, `DONE GOAL`, `CROSS GAP`) that prove the run was real.

## Godot project copy rules

Use a real copy, not a hand-constructed partial project, when validating runtime behavior.

Recommended copy pattern:

```bash
rsync -a \
  --exclude='.godot/' \
  --exclude='rec/' \
  --exclude='rl/telemetry/' \
  "$SRC_TESTBED/" "$ARTIFACT_PROJECT/"
```

Why:

- Copying `.godot/` caches can be slow and can carry stale imported resources.
- Hand-selecting only a few directories can miss Godot `.import`/`.uid` files, scripts, autoload dependencies, or resource sidecars. The project may then fail at runtime with parse/resource errors even though the source project runs.
- Let Godot regenerate `.godot/` with `Godot_console.exe --headless --path . --import` inside the copied project.

## Runtime verification rules

Do not trust the wrapper return code alone. Some shell wrappers can continue after the Python server times out or fails, especially if they do not use strict `set -euo pipefail` and the last command succeeds.

For every real run, verify all of these:

- Python log contains `connection established`, model path, and `推理结束(完成 N 局)`.
- Godot log contains handshake completion plus real game event lines such as `DONE FALL`, `DONE TIMEOUT`, `CROSS GAP`, or `DONE GOAL`.
- If using this repo's `harness/run_infer.sh`, copy `/tmp/rl_infer.log` and `/tmp/infer_godot.log` into the artifact directory immediately after **each** baseline/candidate run; wrapper stdout is only a launcher summary, and the `/tmp` files are overwritten by the next run.
- The isolated `TELEMETRY_DIR` contains exactly the expected `run_*.jsonl` for that run.
- `diagnose.py` was run against that exact JSONL, not a shared `latest` fallback.
- The report summary has `n_episodes >= requested episodes` for formal evaluation.

## Optimizer-specific pitfalls

- Stage-2 optimizers may use a code summary with a specific anchor block. If the copied bad fixture changes the anchor text itself, an LLM-proposed patch using the old anchor can fail to apply. Prefer a defect that preserves the known anchor when the purpose is testing downstream gates, or update the code summary/anchor strategy to include the current observed snippet.
- A fixed policy with stochastic action sampling can pass or fail borderline bad levels depending on seed/episode budget. Use stronger synthetic defects for diagnosis tests, or multiple seeds for product conclusions.
- A one-episode budget can be useful to force a branch for automation smoke tests, but do not present it as product-level balance evidence.

## Pitfalls caught in session

- A model file with the wrong observation/action space can still connect to Godot and then fail inside policy prediction. Always inspect model spaces before running long evaluations.
- A mildly worse level may reduce completion but not cross issue thresholds. Treat that as a useful threshold calibration result, not a failed experiment; make the synthetic defect stronger if the goal is to test diagnosis.
- Copying a whole Godot project including `.godot` cache can be slow. For artifact experiments, prefer `rsync` excluding `.godot/`, `rec/`, and telemetry outputs rather than a manual whitelist copy.
- Avoid cleanup commands in the same launch command. Use unique artifact directories instead of deleting `/tmp` logs.
- When running optimizer verification in a temporary git repo, root-level untracked logs/metadata can trip change gates. Put run logs under ignored `.artifacts/`.
- An issue disappearing from `diagnose` is not automatically an improvement. Check why it disappeared: if `completion_rate` collapsed to 0, a rule such as `combat_bypassed` may stop firing only because the player can no longer reach the goal. For combat gates, inspect raw `DONE ...` events plus combat metrics (`damage_dealt`, `kill_count`, `enemy_alive_at_goal`) to distinguish valid forced combat from a permanent wall or policy failure.
- For Godot animation-driven hitboxes, prove the whole timing chain before retraining: virtual input should reach FSM Attack, AnimationPlayer must stay active until the method-track hit frame, Area2D should overlap the target at that frame, and only then should damage/kill/gate-open be expected. If `Attack` enters but returns to `Idle` before the method-track time (for example because `AnimatedSprite2D.animation_finished` fires and `exit()` stops the AnimationPlayer), training will never discover damage even when hitbox geometry overlaps. Use an artifact SceneTree probe with runtime snapshots; as a diagnostic control, calling the real `Attack.attack_check()` is acceptable to isolate hitbox→`take_hit`→gate-open, but do not call `take_hit()` directly or overclaim that control as virtual-input success.

## Example evidence shape

Healthy model:

```text
completion_rate=1.0
term_distribution={goal: 1.0}
issues=[]
Godot log: CROSS GAP ... DONE GOAL ...
```

Bad copied level:

```text
MidPlatform Vector2(600, 40) -> Vector2(1400, 260)
completion_rate=0.0
term_distribution={fall: 1.0}
issues=[difficulty_too_hard, done_reason_skew]
Godot log: DONE FALL ...
```

Repaired copied level:

```text
MidPlatform Vector2(1400, 260) -> Vector2(600, 40)
completion_rate=1.0
term_distribution={goal: 1.0}
issues=[]
Godot log: CROSS GAP ... DONE GOAL ...
```
