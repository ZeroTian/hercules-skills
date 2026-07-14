# Invocation Lifecycle

Decide how a confirmed facility is driven, separately from which facility is selected. Scheduling (foreground versus background) and terminal mode (PTY versus non-PTY) are orthogonal decisions; never derive one from the other.

## Scheduling

Foreground is the default only for work that is read-only, non-interactive, and duration-stable within a short bound. Default any of the following to a tracked background process with completion notification where the host supports it:

- code mutation or any state change;
- tests, builds, or other long-running commands;
- multi-step or autonomous work;
- network or browser activity;
- materially uncertain duration.

| Work shape | Scheduling default | Completion condition |
|---|---|---|
| read-only, non-interactive, duration-stable, short | bounded foreground with a safety margin | terminal exit status observed |
| mutating, test/build, autonomous, network/browser, or duration-uncertain | tracked background with completion notification | process exit status plus post-run verification observed |
| background unsupported | bounded foreground only when the task still fits its safety envelope; otherwise use another confirmed facility, execute within controller authority, or report a blocker | selected fallback completes and is verified |

### Safety margin and overrun

Expected duration is not the hard timeout. Give foreground work a bounded safety margin above the expected duration. If foreground work overruns or times out, treat completion as unknown: inspect exit status, remaining processes, the actual artifact or diff, and task-appropriate tests before deciding whether to resume. Never blindly replay a mutating brief after an overrun or timeout.

## Terminal Mode

Select PTY only when the confirmed facility requires terminal semantics or interactive input. Prefer non-PTY for non-interactive or structured output.

Confirmed examples, overridable by locally inspected facility documentation:

- Claude print mode (`-p`) normally does not need PTY; it consumes a prompt and emits structured output.
- Codex `exec` is one-shot, but use PTY when the locally inspected Codex orchestration contract requires terminal semantics for that invocation mode; do not infer PTY from the facility name alone.

If locally inspected facility documentation changes either behavior, follow it for the current invocation and report the contract drift. Do not modify this Skill or reference unless the current task explicitly authorizes that change.

## Hermes Adapter

When Hermes terminal/process tools are the confirmed host surface:

1. Start bounded background work with `terminal(command=<bounded command>, background=true, notify_on_complete=true, pty=<independent terminal-mode decision>)` and retain the returned `session_id`.
2. Use `process(action="poll", session_id=<id>)` or `process(action="log", session_id=<id>)` for progress when evidence is needed; use `process(action="wait", session_id=<id>, timeout=<bounded seconds>)` only when blocking is intentional and no independent work remains.
3. Use `process(action="submit", session_id=<id>, data=<input>)` or `process(action="write", session_id=<id>, data=<input>)` only for a confirmed interactive input need. Use `process(action="close", session_id=<id>)` or `process(action="kill", session_id=<id>)` to end abandoned or persistent sessions safely.
4. Treat only a terminal process state plus exit status as completion; then inspect artifacts and run post-run verification.

## Background Observability

A background invocation must remain observable:

- retain a process handle for the started work;
- prefer completion notification over polling where the host supports it;
- inspect poll or log output as needed, without serial blocking wait loops when independent work exists;
- verify terminal exit status before trusting any facility summary;
- clean up persistent interactive sessions after the work completes or is abandoned.

## Authority and Verification

Keep least-sufficient authority: do not widen scope or authority to make scheduling or terminal mode convenient. Independent post-run verification is intact regardless of scheduling choice: inspect actual artifacts, diffs, exit status, and tests rather than trusting a facility self-report. On overrun, timeout, or unknown completion, follow [invocation failure](invocation-failure.md) for classification and fallback.

## Common Mistakes

- Treating background as a synonym for PTY, or non-PTY as a synonym for foreground.
- Defaulting mutating or long-running work to foreground because it looks short.
- Using expected duration as the hard timeout and trusting a partial summary on overrun.
- Blindly replaying a mutating brief after a timeout.
- Selecting PTY for structured, non-interactive output.
- Overriding confirmed Claude `-p` or Codex CLI behavior from memory instead of locally inspected documentation.
- Editing this contract merely because facility behavior drifted, without task authorization.
- Assuming background support; if the host lacks it, use the explicit fallback branch instead of silently switching modes.
- Blocking on a background wait loop when independent work is available.
- Widening authority to simplify scheduling.
