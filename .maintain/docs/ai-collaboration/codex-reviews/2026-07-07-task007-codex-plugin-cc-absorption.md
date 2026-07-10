# Codex Review — TASK-007 codex-plugin-cc absorption

Date: 2026-07-07
Reviewer: Codex CLI (`codex exec`, model `gpt-5.5`, reasoning effort `xhigh`)
Scope: OpenAI `openai/codex-plugin-cc` absorption into Hercules skill pack as optional external Claude Code plugin dependency plus Hercules-owned governance policy.

## Initial review

Verdict: FAIL, P2 finding.

### CR-T007-001 — `HERCULES_CHECK_ONLY=1` was not fully audit-only

- Severity: P2
- Location: `skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`
- Finding: `ensure_node_toolchain` advertised check-only as non-mutating, but still ran `npm config set registry` / `pnpm config set registry` during `HERCULES_CHECK_ONLY=1`.
- Notes: This behavior pre-existed the codex-plugin-cc absorption, but TASK-007 relied on audit-only validation, so it needed fixing.

## Fix

Hermes patched `ensure_node_toolchain` so `CHECK_ONLY=1` logs:

```text
CHECK_ONLY: would set npm registry to <registry>
CHECK_ONLY: would set pnpm registry to <registry>
```

and returns before `npm config set` / `pnpm config set`.

## Recheck

Verdict: PASS.

Codex verified:

- `bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` passed.
- `git diff --check` passed.
- `python3 scripts/validate-skill-pack.py` passed: 0 errors, 1 pre-existing untracked-skills warning, 2 TASK-007 reflection signals.
- Runtime mutation proof passed: `NPM_REGISTRY=https://example.invalid HERCULES_CHECK_ONLY=1 ...` logged both “would set” lines, and npm registry stayed unchanged before/after.
- No accidental vendoring of `codex-plugin-cc` found.
- Optional `codex@openai-codex` install remains gated behind `HERCULES_INSTALL_OPTIONAL=1`.
- Boundary docs cover `/codex:review` and `/codex:adversarial-review` as read-only, `/codex:rescue` as write-capable, and stop-review-gate as off by default.

## Residual risks

- `codex@openai-codex` is not installed on this machine; deep inventory reports cache not found as a non-fatal optional warning.
- The working tree still contains unrelated pre-existing modified/untracked files outside TASK-007 scope.
- Commit/push requires explicit user authorization.
