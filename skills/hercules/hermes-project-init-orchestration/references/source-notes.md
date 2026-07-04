# Source Notes: Codex project-init → Hermes orchestration

Original files read:

- `/mnt/c/Users/Administrator/Documents/Codex/2026-06-29/codex-claude-claude-codex-codex-claude/work/project-init/SKILL.md`
- `/mnt/c/Users/Administrator/Documents/Codex/2026-06-29/codex-claude-claude-codex-codex-claude/work/project-init/references/governance-contract.md`

Key source behaviors preserved:

- Inspect without mutation.
- Preview exact governance diffs and wait for explicit approval before writing.
- Use `CLAUDE.md`, `AGENTS.md`, `docs/ai-collaboration/TASKS.md`, `codex-reviews/`, and `decisions/` as the default governance map.
- Enforce checkbox truth: `[x]` means executed, inspected, evidenced, and reviewed when required.
- Preserve owner/status/next owner/next action/timestamp/evidence/blocker fields.
- Batch all eligible Claude/Codex tasks; never stop after one task when independent work remains.
- Update original `CR-NNN`; do not create duplicate issues for the same finding.

Hermes-specific changes:

- Manual “open Claude/Codex and type this trigger” becomes Hermes-run orchestration.
- Hermes launches Claude Code for implementation and Codex CLI for independent review.
- Hermes monitors background processes, polls proactively, verifies outputs, and writes state back.
- `下一步操作` reports what Hermes actually launched; it must not imply a tool ran if it did not.
- User is asked only for approvals, scope decisions, or real blockers.
