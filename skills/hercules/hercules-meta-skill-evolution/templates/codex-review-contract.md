# Codex Review Contract Footer

Ask Codex to include this JSON footer when its review result drives task/CR routing or closure.

```json
{
  "verdict": "PASS | FAIL | BLOCKED",
  "highest_severity": "P0 | P1 | P2 | P3 | none",
  "summary": "one sentence",
  "findings": [
    {
      "id": "CR-001",
      "severity": "P1",
      "location": "path:line or path#anchor",
      "root_cause_category": "correctness | test | architecture | security | docs | process | evidence | other",
      "required_fix_contract": "specific condition that must be true before PASS",
      "verification_required": "command, log, diff, or record evidence required",
      "original_or_duplicate": "original | duplicate-of-CR-000 | follow-up"
    }
  ],
  "ledger_updates_allowed": false,
  "next_owner": "Hermes | Claude | Codex | User | none",
  "confidence": "high | medium | low"
}
```

Hermes rules:

- Treat the footer as a routing aid, not proof.
- Verify diff, tests/logs, and ledger truth before closure.
- Update original CRs instead of creating duplicates.
- If confidence is low or evidence is missing, route to targeted repair or additional review.
