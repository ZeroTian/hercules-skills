# Review Loop Contract

## State Machine

```text
READY_FOR_REVIEW
  -> REVIEWING
  -> FAIL -> FIXING -> READY_FOR_REVIEW
  -> PASS_PENDING_VERIFICATION -> PASS
  -> BLOCKED
```

- `FAIL` requires one or more actionable findings supported by artifact, code, log, test, or data evidence.
- `FIXING` is routed to a confirmed write-capable implementation facility; the reviewer does not silently mutate the reviewed artifact.
- A repaired artifact returns to `READY_FOR_REVIEW`. Review the new state, not the prior summary.
- `PASS_PENDING_VERIFICATION` becomes `PASS` only after required checks run against the final reviewed state.
- `BLOCKED` records the missing capability, evidence, authority, or independence without weakening the requirement.

## Stable Finding IDs

Assign an ID when a distinct root cause is first reported. Keep that ID across fixes and re-reviews.

A finding records:

- ID and current status;
- severity and precise location;
- observed evidence and impact;
- required fix contract;
- required verification;
- re-review history and final disposition.

Reuse the ID when the same location and root cause remain, regress, or are only partially fixed. Create a new ID only for a genuinely different root cause. Never duplicate or renumber an open finding to make a review appear clean.

## Re-review Rules

1. Review every open finding against its original fix contract.
2. Inspect the complete affected scope for regressions introduced by the fix.
3. Keep unresolved findings open with updated evidence.
4. Close a finding only when its fix contract and required verification pass.
5. Emit overall `PASS` only when no blocking finding remains and final verification evidence is fresh.
