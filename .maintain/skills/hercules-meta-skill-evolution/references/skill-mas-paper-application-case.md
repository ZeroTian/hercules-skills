# Case Study: Applying Skill-MAS to the Hercules Workflow Pack

## Session trigger

The user shared `Skill-MAS: Evolving Meta-Skill for Automatic Multi-Agent Systems` (arXiv:2606.18837) and asked what it could teach the Hercules collaborative-agent skill group.

## What transferred

The useful transfer was not to build a full automatic-MAS benchmark immediately. The durable lesson was to treat `~/.hermes/skills/hercules/` as an evolvable Meta-Skill pack:

1. Record compact trajectories from real collaborative work.
2. Use provisional scores only as prioritization hints.
3. Compare successful and failed traces.
4. Produce an evidence package.
5. Patch only the implicated workflow module with a generalized orchestration principle.

## Three-module mapping

| Skill-MAS module | Hercules equivalent |
|---|---|
| Task Decomposition | Kanban/task splitting, acceptance criteria, dependency mapping |
| Agent Engineering | Hermes/Claude/Codex role selection, capability preflight, prompt contracts |
| Workflow Orchestration | Claude fix → Hermes verify → Codex review loops, fan-out/fan-in, ledger closure |

## Changes made from the lesson

- Added `hercules-meta-skill-evolution` as the class-level umbrella skill.
- Added templates for trajectory records, evidence packages, and Codex review contracts.
- Patched collaborative workflow skills to prefer structured decision contracts and active Hermes merge/verification before closure.
- Patched capability preflight to distinguish read/acquisition capabilities from state-changing execution capabilities.
- Patched Kanban orchestration to preserve uncertainty with bounded fan-out, active merge/review cards, and fallback replanning for empty or low-confidence results.

## Reviewer caveats to preserve

Codex adversarial review caught overclaims that should remain part of the method:

- Do not claim `K=3` is proven enough for Hercules; it is only a possible low-cost starting point that needs calibration.
- Do not assert all current Codex reviews are unstructured; phrase the change as formalizing review output when review drives routing or closure.
- Treat provisional 0–1 scoring as a sorting aid, not objective truth.
- Use elbow selection only when there are enough comparable trajectories; otherwise manually inspect the top high-signal cases.

## Reusable rule

When a paper or external method inspires workflow changes, run the same loop used here:

```text
source packet → synthesis → adversarial review → reconciled recommendation → evidence-backed skill patch
```

Do not let raw synthesis directly rewrite the skill library without review and caveat reconciliation.
