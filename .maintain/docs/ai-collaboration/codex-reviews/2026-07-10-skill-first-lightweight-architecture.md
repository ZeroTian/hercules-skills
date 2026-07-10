# TASK-015 Skill-first lightweight architecture — final independent PASS

- Date: 2026-07-10
- Initial official review: **FAIL** — 5 findings (`Important 3`, `Minor 2`)
- Current result: **PASS** — all seven accepted findings closed on merged `main`
- Ready: **Yes**
- Closure: TASK-015 is complete

## Accepted findings

### TASK015-CR-001 — Important — capability behavior and cache authority evidence

- Status: **CLOSED**
- Fix: freshly discovered candidates now emit the same complete normalized record required by cache reuse: role, facility, kind, confirmed surface, authority, evidence, and fingerprint. A discovery-result-to-session-cache round-trip proves same-fingerprint reuse performs zero scans. Compact, incomplete, stale, permission-mismatched, and failed-invocation records still invalidate and use confirmed discovery/fallback. No install/config/auth commands are emitted.

### TASK015-CR-002 — Important — privacy gate echoed secret-like content

- Status: **CLOSED**
- Fix: staged and unstaged diff checks capture raw Git diagnostics without emitting them and report only redacted category/path/line/count metadata. Isolated sentinel regressions cover both states, and ordinary trailing whitespace still fails the gate.

### TASK015-CR-003 — Important — navigation validator did not enforce the exact-five runtime

- Status: **CLOSED**
- Fix: navigation keys must equal the five runtime Skills; `hercules` is the sole `entry/composite`, and the other four are internal rows. Missing, extra, and wrong-role fixtures fail.

### TASK015-CR-004 — Minor — missing Git/Hermes UX lacked stable links and no-mutation evidence

- Status: **CLOSED**
- Fix: prerequisite failures include official links and explicitly state that Hercules changed nothing; isolated tests compare filesystem snapshots.

### TASK015-CR-005 — Minor — public-surface assertions missed alternate Skill entries

- Status: **CLOSED**
- Fix: both Quickstarts are exactly three commands, the only root executable is `init.sh`, and documented `/skill` parsing covers common Markdown wrappers while excluding URLs/paths. Only `/skill hercules` is accepted.

### TASK015-CR-006 — Minor — public entry did not link its runtime-routing reference

- Status: **CLOSED**
- Fix: `skills/hercules/SKILL.md` links `references/runtime-routing.md`; tests resolve the target.

### TASK015-CR-007 — Minor — validator advisory emitted a non-resolving maintainer path

- Status: **CLOSED**
- Fix: the advisory targets `.maintain/skills/hercules-meta-skill-evolution/templates/evidence-package.md`; a CLI test proves it exists.

## Explicitly excluded experiments

- `bdc5db1` added a complex Git preflight that the official review explicitly treated as Candidate A, not a finding. It is reverted on `main` by `0a63485`; `init.sh` and `test_init.py` retain the lightweight clone/update/symlink contract.
- `823f350` changed active maintainer Skills and historical material outside the accepted CR package. It is reverted on `main` by `3504f0f`.
- The ignored SDD report was accidentally tracked during the interrupted run and is removed from the product package.

## Final merged-main evidence

- Complete stdlib suite: 88/88 passed.
- Runtime owning suite: 28/28 passed.
- Maintainer boundary suite: 22/22 passed.
- Independent focused recheck: 11/11 passed, including discovery-to-cache round-trip and six privacy/diff-check semantics.
- Strict validator: 0 errors / 0 warnings.
- Package gate and fresh-clone smoke passed; Bash syntax and diff checks passed.
- Default runtime remains exactly five Skills; the only public root executable is `init.sh`.

## Closure gate

The independent merged-main recheck closed CR-001 and CR-002, confirmed CR-003 through CR-007 had no regressions, and found no new Critical or Important issue. Both excluded experiments remain exact inverse cleanups. Spec compliance is PASS and Ready is Yes.
