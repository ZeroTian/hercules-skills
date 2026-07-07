# Godot WSL Artifact Probes (Session Notes)

Condensed notes from a real CombatGate validation session run from WSL against the Windows `Godot_console.exe`. These are the pitfalls that cost real time and the commands that produced usable evidence. Supports `skills/godot-wsl-artifact-validation/SKILL.md`.

## Artifact layout

```text
.artifacts/taskNNN_combat_gate_<timestamp>/
├── project/          # copied Godot project, candidate applied here only
├── probe_task.gd     # copied into project/, run via res://
├── probe.log
├── import.log
├── rl_infer.log      # copied from /tmp immediately after baseline run
└── infer_godot.log   # copied from /tmp immediately after candidate run
```

## WSL path pitfall

Passing a WSL absolute path to Windows Godot `--script` fails before the target logic runs:

```text
ERROR: Attempt to open script '/mnt/e/.../probe_task.gd' resulted in error 'File not found'.
```

Fix: copy the probe into the artifact project and execute via `res://`:

```bash
cp "$ART/probe_task.gd" "$ART/project/probe_task.gd"
cd "$ART/project"
/mnt/d/Godot/Godot_console.exe --headless --path . --script res://probe_task.gd > "$ART/probe.log" 2>&1
```

Keep the failed log if the first invocation failed; classify it as a probe harness issue, not product evidence.

## SceneTree probe pitfall

For one-shot probes that `extends SceneTree`, call SceneTree methods directly:

```gdscript
var monsters: Array = get_nodes_in_group("monster")
```

Not:

```gdscript
get_tree().get_nodes_in_group("monster")  # fails: get_tree() is not available from SceneTree self
```

## Inference log preservation

`harness/run_infer.sh` writes to fixed `/tmp` paths:

```text
/tmp/rl_infer.log
/tmp/infer_godot.log
```

Back-to-back baseline+candidate runs overwrite these. Copy each log into the artifact directory immediately after the run that produced it, before starting the next run.

## Probe markers that constituted real evidence

- import log: `rc=0`, no script/parse errors
- semantic probe: `INITIAL`, `AFTER_ACTION`, `AFTER_RESET`, `RESULT ok=true`
- source no-op probe (when the source scene lacks the candidate node): confirms the candidate feature is genuinely new, not silently present

## Protected-source diff guard

```bash
git diff --name-only -- testbed_platformer/rl/train_map.tscn
# expected: empty — the source scene must not change for an artifact-only candidate
```
