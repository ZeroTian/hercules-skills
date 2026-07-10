# TASK-015 Skill-first lightweight architecture — pending narrow recheck

- Date: 2026-07-10
- Initial review range: `df377c0..4742721`
- Initial verdict: **FAIL**
- Repair commits: `3ee0d9a`, `823f350`, `d18a026`, `bdc5db1`, `56df17f`, plus the final evidence commit
- Current verdict: **PENDING independent narrow recheck**
- Closure: TASK-015 remains `待复核`; this is not a PASS record

## Findings

### TASK015-CR-001 — Important — init conflict mutated Git metadata

- Status: **FIXED — AWAITING RECHECK**
- Fix: existing checkouts must be clean; a temporary isolated clone proves the local branch and tracking ref both fast-forward to a captured remote tip before the managed checkout fetches any object. Managed fetch uses `--no-write-fetch-head`; refs/worktree change only on the accepted update path.
- RED→GREEN: divergent, dirty tracked/untracked, and remote-rewrite regressions failed against the old fetch-first flow; `test_init.py` now covers all cases including a genuine remote fast-forward.

### TASK015-CR-002 — Important — package gate echoed secret material

- Status: **FIXED — AWAITING RECHECK**
- Fix: the gate emits only redacted category/path/line/count metadata. Distinctive sentinel values and matching lines never appear in stdout/stderr; deletion and unstaged-only cases remain allowed.
- RED→GREEN: redacted-output regressions failed against verbatim output and now pass in the maintainer boundary suite.

### TASK015-CR-003 — Important — nine capability environments lacked behavior tests

- Status: **FIXED — AWAITING RECHECK**
- Fix: a non-executable stdlib decision contract consumes mocked task/facility/cache/invocation evidence. The table-driven matrix covers all nine design environments and observes route, map, fallback, failure/blocker, cache invalidation, deep inspection, task-relevant scanning, and an empty setup-command list.
- RED→GREEN: nine scenarios failed while the contract was absent; the aggregate table and individual cases now pass.

### TASK015-CR-004 — Important — active maintainer workflows referenced retired paths/runtime

- Status: **FIXED — AWAITING RECHECK**
- Fix: active maintainer Skills/templates/references now use `.maintain/` commands and exact-five paths. Round-2/round-4 material moved to an explicit historical archive; older plugin research is labeled historical.
- RED→GREEN: the active-asset scan exposed retired commands/names across the maintainer tree; it now has zero matches.

### TASK015-CR-005 — Important — validator did not enforce navigation exactness

- Status: **FIXED — AWAITING RECHECK**
- Fix: `check_skill_navigation()` requires the navigation key set to equal `EXPECTED_RUNTIME_SKILLS`, one core entry row for `hercules`, and one core internal row for each other runtime Skill. The package gate invokes this validator.
- RED→GREEN: missing, extra, and wrong-entry fixtures failed before the validator change and now pass.

### TASK015-CR-006 — Minor — missing Git/Hermes UX lacked stable links

- Status: **FIXED — AWAITING RECHECK**
- Fix: failures include official Git/Hermes URLs and explicitly state Hercules changed nothing. Isolated PATH tests snapshot the filesystem and prove no checkout/runtime mutation.
- RED→GREEN: missing-prerequisite message/mutation tests failed before the URL contract and now pass.

### TASK015-CR-007 — Minor — entry did not link routing reference

- Status: **FIXED — AWAITING RECHECK**
- Fix: `skills/hercules/SKILL.md` links `references/runtime-routing.md` at the routing decision point. Runtime linked-reference validation covers the target.
- RED→GREEN: the entry-link assertion failed before the link was added and now passes.

## Final verification evidence

- Complete stdlib discovery suite: 83/83 passed.
- Explicit validator CLI suite: 27/27 passed; strict validator: 0 errors / 0 warnings.
- Bash syntax, diff, public forbidden-behavior, active stale-surface, exact-five, and root-executable scans: clean.
- Redacted default staged package gate: passed.
- Cumulative `df377c0` candidate in a disposable checkout and temporary index: package gate and fresh-clone smoke passed; the clone ran strict validation, init syntax, and 22 runtime tests.

## Closure gate

Every finding above is fixed by the implementation worker but remains open until an independent Codex recheck accepts it. Do not mark this record PASS or TASK-015 complete before that recheck.
