# Real Execution Checklist

Use this when the user asks for a real run, game experiment, browser run, build, or other evidence-producing execution instead of more planning.

## Lessons

- Prefer unique artifact/log directories over cleanup commands. Avoid `rm -f` / `rm -rf` for routine log cleanup because approval gates can block the real run. Write logs to a fresh `.artifacts/<run_id>/` directory instead.
- Before launching a long external run, verify compatibility cheaply: model observation/action spaces, script/import checks, required ports, and output directories.
- For Godot RL-style experiments, inspect the model's `observation_space` and `action_space` before connecting to the game. A wrong model can connect successfully and then fail only at `model.predict()`.
- Bind outputs to the current run: telemetry path, infer log, game log, diagnose report, and stdout should all be in the same run directory.
- After the run, read the actual telemetry/report and summarize observed results. Do not report success from process launch alone.

## Minimal shape

```text
1. Create fresh run dir.
2. Run cheap import/static/model compatibility checks.
3. Launch real execution with logs redirected into the run dir.
4. Generate report from the exact telemetry file produced by this run.
5. Summarize real observed metrics and blockers.
```
