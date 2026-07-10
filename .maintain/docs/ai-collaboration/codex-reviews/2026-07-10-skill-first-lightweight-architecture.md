# TASK-015 Skill-first lightweight architecture — pending narrow recheck

- Date: 2026-07-10
- Initial review range: `df377c0..4742721`
- Initial verdict: **FAIL**
- Repair commits: `3ee0d9a`, `823f350`, `d18a026`, `bdc5db1`, `56df17f`, `e42f4f2`, plus the final recheck-fix commit
- Independent recheck range: `df377c0..e42f4f2`; result **FAIL** — 5 closed, 2 reopened, 1 new Minor
- Current verdict: **PENDING independent narrow recheck of CR-003, CR-007, and CR-008**
- Closure: TASK-015 remains `待复核`; this is not a PASS record

## Findings

### TASK015-CR-001 — Important — init conflict mutated Git metadata

- Status: **CLOSED**
- Fix: existing checkouts must be clean; a temporary isolated clone proves the local branch and tracking ref both fast-forward to a captured remote tip before the managed checkout fetches any object. Managed fetch uses `--no-write-fetch-head`; refs/worktree change only on the accepted update path.
- RED→GREEN: divergent, dirty tracked/untracked, and remote-rewrite regressions failed against the old fetch-first flow; `test_init.py` now covers all cases including a genuine remote fast-forward.

### TASK015-CR-002 — Important — package gate echoed secret material

- Status: **CLOSED**
- Fix: the gate emits only redacted category/path/line/count metadata. Distinctive sentinel values and matching lines never appear in stdout/stderr; deletion and unstaged-only cases remain allowed.
- RED→GREEN: redacted-output regressions failed against verbatim output and now pass in the maintainer boundary suite.

### TASK015-CR-003 — Important — fresh session cache was not consumed

- Status: **FIXED — AWAITING RECHECK**
- Recheck evidence: with a matching fingerprint and `routes={"implementation": "claude"}`, the model ignored the fresh route and returned `route=null` plus a blocker; a fresh cache lacking the requested role was not invalidated.
- Fix: fresh compact or normalized route records are consumed without discovery, normalized into role/facility/confirmed-surface/authority/evidence/fingerprint records, and returned in the capability map. Missing-role, stale-fingerprint, and invocation-failure cases invalidate the cache and retain facility fallback. The contract still returns no install/config/auth commands.
- RED→GREEN: the two independent-symptom regressions and a normalized-record regression failed before implementation; the focused cache/fallback set now passes 6/6 and the owning runtime suite passes 26/26.

### TASK015-CR-004 — Important — active maintainer workflows referenced retired paths/runtime

- Status: **CLOSED**
- Fix: active maintainer Skills/templates/references now use `.maintain/` commands and exact-five paths. Round-2/round-4 material moved to an explicit historical archive; older plugin research is labeled historical.
- RED→GREEN: the active-asset scan exposed retired commands/names across the maintainer tree; it now has zero matches.

### TASK015-CR-005 — Important — validator did not enforce navigation exactness

- Status: **CLOSED**
- Fix: `check_skill_navigation()` requires the navigation key set to equal `EXPECTED_RUNTIME_SKILLS`, one core entry row for `hercules`, and one core internal row for each other runtime Skill. The package gate invokes this validator.
- RED→GREEN: missing, extra, and wrong-entry fixtures failed before the validator change and now pass.

### TASK015-CR-006 — Minor — missing Git/Hermes UX lacked stable links

- Status: **CLOSED**
- Fix: failures include official Git/Hermes URLs and explicitly state Hercules changed nothing. Isolated PATH tests snapshot the filesystem and prove no checkout/runtime mutation.
- RED→GREEN: missing-prerequisite message/mutation tests failed before the URL contract and now pass.

### TASK015-CR-007 — Minor — entry did not link routing reference

- Status: **FIXED — AWAITING RECHECK**
- Recheck evidence: the reference file existed but `skills/hercules/SKILL.md`, runtime tests, and the validator path did not mention it.
- Fix: `skills/hercules/SKILL.md` now links `[runtime routing reference](references/runtime-routing.md)` at the routing decision point. A regression test parses the Markdown link and resolves the target; strict linked-reference validation also covers it.
- RED→GREEN: the navigation/reference test failed against the orphaned file and now passes.

### TASK015-CR-008 — Minor — strict advisory emitted a non-resolving maintainer path

- Status: **FIXED — AWAITING RECHECK**
- Recheck evidence: strict output recommended `hercules-meta-skill-evolution/templates/evidence-package.md`, which does not exist at repository root.
- Fix: the advisory now emits `.maintain/skills/hercules-meta-skill-evolution/templates/evidence-package.md`. A CLI regression test reads the JSON signal, rejects the old path, and proves the emitted target exists.
- RED→GREEN: the advisory-path test failed on the stale path and now passes; the owning validator CLI suite passes 28/28.

## Final verification evidence

- Targeted CR-003 cache/fallback set: 6/6 passed; runtime owning suite: 26/26 passed.
- Targeted CR-007 link test and strict linked-reference validation: passed.
- Targeted CR-008 advisory-path test; validator CLI owning suite: 28/28 passed.
- Complete stdlib discovery suite: 88/88 passed; strict validator: 0 errors / 0 warnings.
- Bash syntax, diff, public forbidden-behavior, active stale-surface, exact-five, and root-executable scans: clean.
- Final staged package gate: passed with `maintainer package checks passed`.

## Closure gate

CR-001, CR-002, CR-004, CR-005, and CR-006 are closed by the independent recheck. CR-003, CR-007, and CR-008 are fixed by the implementation worker but remain open until an independent Codex recheck accepts them. Do not mark this record PASS or TASK-015 complete before that recheck.
