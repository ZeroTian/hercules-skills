# TASK-015 Skill-first lightweight architecture — merged-main cleanup recheck

- Date: 2026-07-10
- Initial official review: **FAIL** — 5 findings (`Important 3`, `Minor 2`)
- Current result: **PENDING** — approved lightweight package is implemented; merged `main` cleanup awaits one independent recheck
- Ready: **No — cleanup recheck pending**
- Closure: TASK-015 temporarily returns to `待复核`

## Accepted findings

### TASK015-CR-001 — Important — capability behavior and cache authority evidence

- Status: **FIXED — AWAITING RECHECK**
- Fix: the nine task/facility/cache environments have executable behavior coverage. Cache reuse accepts only complete normalized records whose role, facility, surface, authority, evidence, and fingerprint satisfy the current demand. Compact, incomplete, stale, permission-mismatched, and failed-invocation records invalidate and use confirmed discovery/fallback. No install/config/auth commands are emitted.

### TASK015-CR-002 — Important — privacy gate echoed secret-like content

- Status: **FIXED — AWAITING RECHECK**
- Fix: staged privacy output is limited to redacted category/path/line/count metadata; sentinel content is never printed.

### TASK015-CR-003 — Important — navigation validator did not enforce the exact-five runtime

- Status: **FIXED — AWAITING RECHECK**
- Fix: navigation keys must equal the five runtime Skills; `hercules` is the sole `entry/composite`, and the other four are internal rows. Missing, extra, and wrong-role fixtures fail.

### TASK015-CR-004 — Minor — missing Git/Hermes UX lacked stable links and no-mutation evidence

- Status: **FIXED — AWAITING RECHECK**
- Fix: prerequisite failures include official links and explicitly state that Hercules changed nothing; isolated tests compare filesystem snapshots.

### TASK015-CR-005 — Minor — public-surface assertions missed alternate Skill entries

- Status: **FIXED — AWAITING RECHECK**
- Fix: both Quickstarts are exactly three commands, the only root executable is `init.sh`, and documented `/skill` parsing covers common Markdown wrappers while excluding URLs/paths. Only `/skill hercules` is accepted.

### TASK015-CR-006 — Minor — public entry did not link its runtime-routing reference

- Status: **FIXED — AWAITING RECHECK**
- Fix: `skills/hercules/SKILL.md` links `references/runtime-routing.md`; tests resolve the target.

### TASK015-CR-007 — Minor — validator advisory emitted a non-resolving maintainer path

- Status: **FIXED — AWAITING RECHECK**
- Fix: the advisory targets `.maintain/skills/hercules-meta-skill-evolution/templates/evidence-package.md`; a CLI test proves it exists.

## Explicitly excluded experiments

- `bdc5db1` added a complex Git preflight that the official review explicitly treated as Candidate A, not a finding. It is reverted on `main` by `0a63485`; `init.sh` and `test_init.py` retain the lightweight clone/update/symlink contract.
- `823f350` changed active maintainer Skills and historical material outside the accepted CR package. It is reverted on `main` by `3504f0f`.
- The ignored SDD report was accidentally tracked during the interrupted run and is removed from the product package.

## Fresh merged-main evidence before recheck

- Complete stdlib suite: 81/81 passed.
- Runtime owning suite: 27/27 passed.
- Strict validator: 0 errors / 0 warnings.
- Bash syntax and diff checks passed.
- Default runtime remains exactly five Skills; the only public root executable is `init.sh`.

## Closure gate

An independent reviewer must confirm the seven accepted fixes, both cleanup reverts, the untracked-report removal, package gate, and fresh-clone smoke on merged `main`. Only then may this record return to PASS / Ready Yes and TASK-015 to `已完成`.
