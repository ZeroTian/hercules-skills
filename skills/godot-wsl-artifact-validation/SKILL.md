---
name: godot-wsl-artifact-validation
description: "Use when validating Godot gameplay/evaluation candidates from WSL with Windows Godot: artifact projects, headless probes, import/smoke evidence, and baseline-vs-candidate log preservation."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, godot, wsl, artifact-validation, evaluation, probes]
    related_skills: [coding-agent-orchestration, hercules-collaborative-agent-workflow, evaluation-closed-loop-orchestration, godot-rl-metric-regression]
---

# Godot WSL Artifact Validation

## When to use

Use this skill when a task needs real Godot evidence while Hermes is running in WSL and the executable is the Windows `Godot_console.exe`, especially for:

- isolated artifact projects under `.artifacts/`
- candidate scene validation without modifying source scenes
- headless GDScript probes
- Godot import/smoke checks
- baseline vs candidate inference or metric regression evidence

## Core workflow

1. Create an artifact directory and copy the Godot project into it.
2. Apply candidate-only scene/code changes inside the artifact when the source tree must remain protected.
3. Run `Godot_console.exe --headless --path <artifact-project> --import` and save the log.
4. Run a small semantic probe that prints explicit pass/fail markers.
5. If the feature is optional/no-op in source, run a separate source no-op probe/import.
6. Run Python tests and `git diff --check`.
7. Confirm protected source scenes are unchanged, e.g. `git diff --name-only -- testbed_platformer/rl/train_map.tscn` is empty.
8. Record artifact paths, commands, exit codes, and marker lines in the task ledger before handing to Codex.

## WSL + Windows Godot script paths

Do not pass WSL absolute script paths such as `/mnt/e/.../probe_task.gd` directly to Windows Godot `--script`. Windows Godot may fail before exercising the target logic:

```text
ERROR: Attempt to open script '/mnt/e/.../probe_task.gd' resulted in error 'File not found'.
```

Instead, copy the probe into the artifact project and execute via `res://`:

```bash
cp "$ART/probe_task.gd" "$ART/project/probe_task.gd"
cd "$ART/project"
/mnt/d/Godot/Godot_console.exe --headless --path . --script res://probe_task.gd > "$ART/probe.log" 2>&1
```

Keep the failed log if the first invocation failed; classify it as a probe harness issue, not as product evidence.

## SceneTree probe pitfall

For one-shot scripts that `extends SceneTree`, call SceneTree methods directly:

```gdscript
var monsters: Array = get_nodes_in_group("monster")
```

Do not call:

```gdscript
get_tree().get_nodes_in_group("monster")
```

From `SceneTree` self, `get_tree()` is not available and the probe can fail before it reaches the target logic.

## Inference log preservation

`harness/run_infer.sh` writes detailed Python/Godot logs to fixed `/tmp` paths such as:

```text
/tmp/rl_infer.log
/tmp/infer_godot.log
```

If running baseline and candidate back-to-back, copy these logs into the artifact immediately after each run. Otherwise the next run overwrites the evidence.

## Evidence quality bar

A good Godot artifact proof includes:

- import log with rc=0 and no script/parse errors
- semantic probe markers such as `INITIAL`, `AFTER_ACTION`, `AFTER_RESET`, `RESULT ok=true`
- source no-op probe when the source scene lacks the candidate node/feature
- exact artifact path
- exact commands or enough replay detail
- protected-source diff guards
- Python test results and `git diff --check`

## References

- `references/godot-wsl-artifact-probes.md` — condensed notes from a real CombatGate validation session, including WSL path and `SceneTree` probe pitfalls.
