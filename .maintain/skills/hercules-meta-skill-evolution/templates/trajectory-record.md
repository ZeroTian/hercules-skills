# Hercules Trajectory Record

Use this template in TASKS/CR records or an evidence package when a collaborative workflow run should be available for later reflection.

```yaml
trajectory:
  task_id: TASK-000
  attempt: 1
  date: YYYY-MM-DD
  task_type: implementation | review | research | project-init | debugging | docs | other
  skill_versions:
    hercules-collaborative-workflow: 1.0.0
    hercules-capability-discovery: 1.0.0
  score: provisional   # 1.0 / 0.8 / 0.6 / 0.3 / 0.0, or leave blank until judged
  score_reason: "short evidence-based reason"
  actor_path: "Hermes -> Claude -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned | cached | skipped-with-reason
    relevant_capabilities: []
    effort: high | xhigh | other
    claude_result: not-launched | completed | max-turns | failed
    codex_result: not-launched | PASS | FAIL | BLOCKED
    verification:
      commands: []
      logs: []
      diff_scope: ""
    cr_ids: []
    blocker_type: none | scope | test | tool | external | unclear
    next_owner: Hermes | Claude | Codex | User | none
  source_pointers:
    task_record: "path#anchor"
    review_record: "path#anchor"
    logs: []
```

Scoring guide:

| Score | Meaning |
|---:|---|
| 1.0 | PASS with required evidence and no rework |
| 0.8 | PASS with minor P2/manual cleanup |
| 0.6 | PASS after meaningful rework |
| 0.3 | BLOCKED but with clear next owner/action |
| 0.0 | FAIL or no usable artifact |

Rules:

- Keep records compact. Link to logs instead of pasting them.
- Scores are provisional sorting hints, not objective truth.
- Do not record secrets, tokens, cookies, or private paths that should not enter a repo.
- If a field is unknown, write `unknown` or omit it; do not invent evidence.
