# Why Hercules

This is a reader-facing positioning note. It explains how Hercules relates to the OpenAI `codex-plugin-cc` Claude Code plugin accurately and without overclaiming. It is not an install guide; for install and validation steps see `README.md`.

## TL;DR

- `codex-plugin-cc` lets Claude call Codex from inside Claude Code.
- Hercules makes Claude + Codex collaboration governable, auditable, and safe under Hermes orchestration.
- They are complementary, not substitutes. Hercules does not replace `codex-plugin-cc`, and `codex-plugin-cc` does not provide the Hercules governance layer.

## What `codex-plugin-cc` is

`openai/codex-plugin-cc` is an OpenAI Claude Code plugin (marketplace `openai-codex`, plugin `codex`, installed as `codex@openai-codex`). It exposes a `/codex:*` command surface inside Claude Code so Claude can invoke Codex for review, adversarial review, rescue/fix, status, and related operations without leaving the Claude Code session.

Strengths:

- Low friction: install one plugin and Claude gains an in-session Codex channel.
- Good for quick inline second opinions and challenge reviews while Claude is already working.
- Lets a single Claude session delegate focused review or rescue tasks to Codex.

Limitations:

- The in-Claude Codex review runs in the same session/context as the work being reviewed; it is a preliminary channel, not an independent final gate.
- Some surfaces (for example rescue/delegate/fix) are write-capable by default and need explicit authorization before they should be used on real work.
- Automatic review gates can create long-running or costly loops; they are off by default.
- The plugin itself does not maintain a task ledger, trajectory records, safety-boundary classification, or a dependency-vs-vendor policy.

The detailed surface inventory and safety classification live in `skills/agent-plugin-dependency-governance/SKILL.md`, not here.

## What Hercules is

Hercules is a portable Hermes skill pack. It encodes a workflow, not a plugin:

```text
Hermes orchestrates -> Claude Code implements -> Codex independently reviews -> real commands verify
```

Strengths:

- Explicit role split with one owner per phase, so review is not same-context self-approval.
- Auditable trail: task records, validation commands, review records, trajectory blocks, and explicit residual risks in `docs/ai-collaboration/TASKS.md` and `docs/ai-collaboration/codex-reviews/`.
- Dependency boundary: external plugins (including `codex-plugin-cc`) are dependencies checked by bootstrap, never vendored source. Optional, token-spending, or state-changing installs are gated.
- Safety classification of plugin surfaces, audit-only bootstrap proof, and a validator release gate (`scripts/validate-skill-pack.py --strict`).
- Independent final Codex review is launched by Hermes as a separate Codex CLI pass, distinct from any in-Claude `/codex:*` review.

Limitations:

- Heavier setup: it requires Hermes, the skill pack, Claude Code, and Codex CLI, plus the discipline to actually run the Hermes -> Claude -> Codex -> verify loop.
- It is a governance/workflow skill pack, not a plugin. It does not give Claude new in-context commands; if you want Claude to call Codex inline, you still want `codex-plugin-cc` or an equivalent.
- Its value depends on following the loop. A team that skips independent review or skips recording evidence gets little of the audit benefit.
- It does not certify upstream plugin behavior; it classifies surfaces and gates installs, then hands review to Codex and verification to real commands.

## How they compose

Hercules treats `codex-plugin-cc` as an optional external dependency, not a competitor:

- The bootstrap can register the `openai-codex` marketplace and install `codex@openai-codex` only under an explicit optional gate such as `HERCULES_INSTALL_OPTIONAL=1`.
- The governance skill classifies `/codex:review` and `/codex:adversarial-review` as preliminary read-only review channels and rescue/delegate surfaces as state-changing by default.
- Inline `/codex:*` review is useful before handoff, but the Hermes-orchestrated independent Codex CLI review remains the final acceptance gate for review-required work.

In short: `codex-plugin-cc` adds an in-Claude channel to reach Codex; Hercules adds the governance, boundary, audit trail, and independent final review around Claude + Codex collaboration. Use both when you want inline Codex help inside Claude Code and an auditable, independently reviewed workflow.

## When to use which

- Want Claude to call Codex inline during a Claude Code session? Install `codex-plugin-cc`.
- Want Claude + Codex collaboration to leave an auditable, independently reviewed trail under Hermes? Use Hercules.
- Want both? Use Hercules and treat `codex-plugin-cc` as an optional, gated, classified dependency.

This note makes no claim that Hercules replaces `codex-plugin-cc`, and no claim of capabilities beyond what the repository's validator, bootstrap audit, and recorded Codex reviews already evidence.
