# Case Study: Personas × LLM Judge S3 Research

Use this as an example of how open-ended research should reconcile synthesis with adversarial review before becoming a task.

## Context

Research question: how to design a `Personas × LLM Judge (S3)` report-only MVP for a game AI project.

Hermes collected a source packet, Claude synthesized a design, and Codex adversarially reviewed it.

## What Worked

- Hermes preserved a source packet with external rows (`E1`-style IDs) and local repo rows (`L1`-style IDs).
- Claude produced a useful architecture direction: S3 as a composition/report layer, not a new optimizer.
- Codex caught schema and implementation-boundary issues that the synthesis missed.
- Final durable research doc used the Codex-corrected conclusion, not the raw Claude output.

## Review Findings That Should Generalize

When turning research into implementation tasks, require the synthesis/review loop to check:

1. **Terminology/schema alignment.** If an existing module has strict enum values, do not reuse a field name with mapped human-facing labels. Keep raw and mapped forms separate.
2. **Presence vs equality validation.** Existing validators often compare fields only when both sides include them. New composition layers may need stricter “field must be present and equal” checks.
3. **Coverage accounting.** If an upstream batch/panel can skip failed items, downstream reports need `failed_*`, `missing_*`, and coverage counts instead of silently treating missing items as neutral.
4. **Aggregation semantics.** Multi-run or multi-seed research must explicitly define whether it uses a representative sample, per-item aggregation, majority vote, or summary-only evidence.
5. **Overclaim control.** Phrases like “best practice” or “sufficient” should be downgraded to “engineering recommendation” unless sources directly establish them.
6. **Report-only boundaries.** If research recommends an artifact-only integration, tests must prove it does not feed scoring, gates, acceptance, or early-stop logic.

## Durable Pattern

After Codex returns `not PASS as-is` but no P0/P1:

1. Do not discard the synthesis.
2. Extract P2/P3 findings into a “revised recommendation”.
3. Write the durable research note from the revised recommendation, not from the raw synthesis.
4. If creating a task, make the findings explicit acceptance criteria and test cases.

## Example Output Shape

```markdown
## Codex adversarial review result

Codex conclusion: synthesis not PASS as-is; no P0/P1; fix P2 before task creation.

Findings:
- P2: schema enum conflict; split raw vs mapped field names.
- P2: missing strict provenance requirements.
- P2: missing failed/missing coverage fields.
- P2: multi-seed semantics undefined.
- P3: overclaims need softer language.

## Revised recommendation

Proceed, but only with the corrected boundaries and tests listed above.
```
