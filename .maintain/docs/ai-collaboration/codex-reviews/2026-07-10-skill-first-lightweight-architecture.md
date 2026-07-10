# TASK-015 Skill-first lightweight architecture — final independent PASS

- Date: 2026-07-10
- Initial review range: `df377c0..4742721`
- Initial verdict: **FAIL**
- Repair commits: `3ee0d9a`, `823f350`, `d18a026`, `bdc5db1`, `56df17f`, `e42f4f2`, `444ff02`, `0b56986`
- Final independent recheck range: `df377c0..0b56986`; result **PASS** — 8 closed / 0 open
- Current verdict: **PASS**
- Ready: **YES**
- Closure: TASK-015 is complete

## Findings

### TASK015-CR-001 — Important — init conflict mutated Git metadata

- Status: **CLOSED**
- Fix: existing checkouts must be clean; a temporary isolated clone proves the local branch and tracking ref both fast-forward to a captured remote tip before the managed checkout fetches any object. Managed fetch uses `--no-write-fetch-head`; refs/worktree change only on the accepted update path.
- RED→GREEN: divergent, dirty tracked/untracked, and remote-rewrite regressions failed against the old fetch-first flow; `test_init.py` now covers all cases including a genuine remote fast-forward.

### TASK015-CR-002 — Important — package gate echoed secret material

- Status: **CLOSED**
- Fix: the gate emits only redacted category/path/line/count metadata. Distinctive sentinel values and matching lines never appear in stdout/stderr; deletion and unstaged-only cases remain allowed.
- RED→GREEN: redacted-output regressions failed against verbatim output and now pass in the maintainer boundary suite.

### TASK015-CR-003 — Important — compact cache bypassed authority evidence

- Status: **CLOSED**
- Recheck evidence: a compact string route for `review-only-tool` plus a write-capable demand fabricated implementation surface, write authority, and evidence, then routed without discovery.
- Fix: cache reuse now accepts only complete normalized records whose role, facility, confirmed surface, authority, evidence, and fingerprint satisfy the current demand. Compact/incomplete/read-only records become `invalid-cache-record` and use existing task-relevant discovery/fallback; missing-role, stale-fingerprint, and invocation-failure behavior is unchanged. The contract still emits no install/config/auth commands.
- RED→GREEN: the reviewer compact-cache symptom failed by routing the unproven facility; after removing string synthesis, compact and read-only records invalidate while normalized fresh reuse and all fallback paths pass in the focused 7-case set.

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

- Status: **CLOSED**
- Recheck evidence: the reference file existed but `skills/hercules/SKILL.md`, runtime tests, and the validator path did not mention it.
- Fix: `skills/hercules/SKILL.md` now links `[runtime routing reference](references/runtime-routing.md)` at the routing decision point. A regression test parses the Markdown link and resolves the target; strict linked-reference validation also covers it.
- RED→GREEN: the navigation/reference test failed against the orphaned file and now passes.

### TASK015-CR-008 — Minor — strict advisory emitted a non-resolving maintainer path

- Status: **CLOSED**
- Recheck evidence: strict output recommended `hercules-meta-skill-evolution/templates/evidence-package.md`, which does not exist at repository root.
- Fix: the advisory now emits `.maintain/skills/hercules-meta-skill-evolution/templates/evidence-package.md`. A CLI regression test reads the JSON signal, rejects the old path, and proves the emitted target exists.
- RED→GREEN: the advisory-path test failed on the stale path and now passes; the owning validator CLI suite passes 28/28.

## Final verification evidence

- Targeted CR-003 cache-integrity/fallback set: 7/7 passed.
- Runtime owning suite: 27/27 passed; complete stdlib discovery suite: 89/89 passed.
- Strict validator: 0 errors / 0 warnings; Bash, diff, public forbidden-behavior, exact-five, and root-executable scans are clean.
- Final staged package gate: passed with `maintainer package checks passed`.

## Closure gate

The final independent recheck at `0b56986` closed CR-003 after reproducing the original compact-cache symptom and verifying the normalized-cache boundary. CR-001 through CR-008 are all closed; spec compliance is PASS and Ready is YES.
