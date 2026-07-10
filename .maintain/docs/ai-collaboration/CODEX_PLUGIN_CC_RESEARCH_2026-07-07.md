# codex-plugin-cc Absorption Research

Date: 2026-07-07
Repository: `/mnt/e/code/hercules-skills`
Scope: absorb OpenAI `openai/codex-plugin-cc` into the Hercules skill pack as an OPTIONAL external Claude Code plugin dependency + Hercules-owned governance policy. Upstream plugin source is NOT vendored.

## Recommendation

Partial absorb: dependency + policy, not vendored source.

- Treat `codex-plugin-cc` as an optional external Claude plugin dependency, checked/installed by the bootstrap script under `HERCULES_INSTALL_OPTIONAL=1` (same optional bucket as `playwright`, `context7`, `pyright-lsp`).
- Encode the governance policy (boundary classification, Hermes-owned final review, authorization rules) in Hercules-owned skills (`hercules-agent-capability-preflight`, `cross-agent-review-loop`) rather than copying plugin source.

## Sources

- Upstream plugin: `openai/codex-plugin-cc` GitHub repository (OpenAI). Provides `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:transfer`, `/codex:status`, `/codex:result`, `/codex:cancel`, `/codex:setup`, and the `codex:codex-rescue` agent.
- Repository boundary convention: external plugins/skills are dependencies checked by bootstrap, not vendored (see `docs/ai-collaboration/ARCHITECTURE.md` and `README.md`).
- Capability inventory for this run: Claude Code 2.1.201, Codex CLI 0.142.5 logged in, Claude plugins `superpowers` + `oh-my-claudecode` + `context7` + `playwright` + `pyright-lsp` available; `codex` Claude plugin not currently installed.

## Risks

1. **`/codex:rescue` defaults to write-capable.** Unless a read-only rescue is explicitly requested, it can mutate files/state. Must require explicit Hermes/user authorization.
2. **Stop-review-gate can create long-running/costly loops.** It is off by default; enabling it must be explicit and user-monitored.
3. **Claude-side plugin review must not replace Hermes-owned independent final Codex review.** `/codex:review` and `/codex:adversarial-review` run inside Claude Code (same context, preliminary). The independent Codex CLI review/acceptance pass remains required for review-required work.
4. **Plugin not installed by default.** Briefs must not assume `/codex:*` commands exist; preflight must confirm via plugin cache inspection.

## Implementation decision

- Bootstrap: add `openai-codex` marketplace (`openai/codex-plugin-cc`) always; install `codex@openai-codex` only with `HERCULES_INSTALL_OPTIONAL=1`. Add deep inventory for `~/.claude/plugins/cache/openai-codex/codex` (list `/codex:*` commands, report `agents/codex-rescue.md` presence as a non-fatal warning).
- Preflight skill: update dependency table, optional install docs, Claude capability scan, and boundary classification (`/codex:review` + `/codex:adversarial-review` read-only; `/codex:rescue` write-capable; stop gate off by default). Add pitfalls for the three risks above.
- Cross-agent review loop: add a concise section making the plugin an optional inline/preliminary channel; require explicit authorization for `/codex:rescue`; reaffirm Hermes-owned final independent Codex review.
- README / ARCHITECTURE: mention `codex-plugin-cc` as optional external Claude plugin dependency; do not duplicate long policy.
- TASKS: add TASK-007 for this absorption work.

No upstream plugin source is copied into this repository.
