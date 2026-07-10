# Issue-to-Handoff Closed-Loop (Session Notes)

Condensed artifact pattern from a real Godot/RL closed-loop session where a `combat_bypassed` diagnosis had to be converted into a safe, machine-readable handoff rather than a hand-tuned level fix. Supports `skills/evaluation-closed-loop-orchestration/SKILL.md`.

## Loop shape that worked

```text
real inference run
  -> diagnose.py report (objective issue: combat_bypassed)
  -> safe optimizer/gate attempt on allowed_surfaces only
  -> ACCEPTED or REJECTED with score evidence
  -> if unresolved: modification_requests.json
  -> agent_handoffs.json (owner, next_owner, brief, criteria, commands)
  -> Hermes dispatches owner
  -> safe execution OR BLOCKED_SCOPE_INSUFFICIENT
  -> Codex independent review
```

## Field preservation across handoffs

Every handoff must carry forward these fields from the source request, or the next agent loses the safety context:

- `allowed_surfaces` and `forbidden_surfaces`
- `evidence` (telemetry/report snippets that prove the issue)
- `gate_result` (accept/reject, reason, score before/after)
- `attempted_plan` (what was tried, so the next agent does not blindly retry)
- `blocked_reason` (why the current run could not solve it)

The handoff brief must repeat `forbidden_surfaces` explicitly so the next agent cannot "fix" the issue by moving the ruler (goal/fall/reward/telemetry/diagnose/persona/model).

## BLOCKED_SCOPE_INSUFFICIENT example

When the recommended action needs a structural anchor that is not yet in the safe allowlist, produce a BLOCKED artifact instead of widening scope:

```json
{
  "verdict": "BLOCKED_SCOPE_INSUFFICIENT",
  "source_issue": "combat_bypassed",
  "recommended_action": "add CombatGate node under Level/Obstacles",
  "why_insufficient": "no legal safe anchor for adding a combat gate node yet",
  "required_new_safe_anchor": "CombatGate block under Level/Obstacles with script binding",
  "proposed_allowed_surfaces": ["Level/Obstacles/CombatGate"],
  "forbidden_surfaces": ["reward", "goal", "fall", "telemetry", "diagnose", "persona", "model"],
  "required_tests": ["test_combat_gate_anchor_allowed", "test_measurement_anchors_rejected"],
  "required_verification_gates": ["structural parser", "godot --import", "metric regression"],
  "next_owner_hint": "Claude",
  "next_reviewer": "Codex",
  "evidence": "<copied from source request>",
  "gate_result": "REJECTED score=..."
}
```

## Defensive checks that caught real bugs

1. **Concept denylist.** A proposed surface named `reward_shaping` was rejected even though no file by that name existed. The validator strips harmless negative phrases ("excluding reward_...") and then denies the concept.
2. **Whole-block matching.** `re.match(pattern + "$", block)` accepted a trailing newline and let an extra node through. Switching to `re.fullmatch(pattern, block)` without a trailing `$` caught the extra node.
3. **Owner routing.** A handoff with `owner=Claude` but a malformed `allowed_surfaces` list was not dispatched. Hermes recorded a BLOCKED artifact instead of launching Claude on an unsafe brief.

## Non-goal pattern

A task that creates the next work package (e.g., a BLOCKED artifact plus a safe-anchor capability task) but does not implement the downstream design change is a non-goal, not a failure. Record it as such so the ledger does not reopen the same scope.
