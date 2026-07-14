# Hercules Controller-Owned Routing Design

## Problem

Hercules is a Hermes Skill, but project initialization currently places the
instruction to enter Hercules and select facilities in the shared
`AGENTS.md` contract. Codex reads that contract directly, and `CLAUDE.md`
adapters tell Claude Code to follow it. A facility selected by Hermes can
therefore attempt capability discovery and Hercules routing again.

## Decision

Routing is owned exclusively by the Hermes controller:

```text
Hermes -> Hercules -> selected facility -> result -> Hermes verification
```

Once Claude Code, Codex CLI, or another facility is selected, routing is
complete. The selected facility executes its bounded brief directly. It must
not load Hercules, perform capability discovery, select another facility, or
apply controller fallback. Invocation failure returns to Hermes for
classification and fallback.

## Runtime Contract

- `skills/hercules/SKILL.md` declares controller ownership and the no-reentry
  rule.
- `collaborative-workflow.md` and `review-workflow.md` require every facility brief to carry
  `controller`, `route_state`, `facility`, `role`, and `authority` context.
- `project-init.md` keeps execution and evidence rules shared, while moving
  Hercules entry, capability selection, fallback, and final verification into
  the `HERMES.md` adapter.
- `AGENTS.md` and `CLAUDE.md` describe Codex and Claude Code as execution or
  review facilities. They do not instruct those facilities to enter Hercules.

## Compatibility

- The public runtime remains exactly one Skill: `hercules`.
- No executable, dependency, provider configuration, or authentication
  behavior is added.
- Existing projects need an idempotent instruction migration; rerunning
  `init.sh` is neither required nor sufficient because it does not edit
  project instruction files.
- Historical design and review records remain unchanged as dated evidence.

## Acceptance

- Runtime and dogfood instructions contain no path that sends selected
  Claude/Codex facilities back into Hercules.
- A facility invocation brief explicitly states that routing is complete.
- Only the Hermes adapter owns discovery, fallback, and final verification.
- Focused contract tests demonstrate RED before the fix and GREEN afterward.
- Full repository validation passes without touching unrelated `.DS_Store`.
