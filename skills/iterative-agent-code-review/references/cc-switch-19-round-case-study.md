# cc-switch 19-Round Claude+Codex Review Case Study

**Date:** 2026-07-01
**Project:** ZeroTian/cc-switch (fork of farion1231/cc-switch)
**Task:** Rebase onto upstream/main (v3.16.4) + fix all review issues
**Result:** 19 rounds, 30+ issues fixed, Codex clean

## Context

- 51 local commits rebased onto upstream/main (v3.16.4)
- Schema version collision: both upstream and fork added v10→v11 migration
- Upstream: usage_daily_rollups rebuild (request_model/pricing_model columns)
- Fork: skill_groups + skill_group_members tables
- Resolution: upstream kept v10→v11, fork's skill_groups moved v11→v12→v16→v17

## Round-by-Round Breakdown

### Rounds 1-2: Structural (P0)
- Duplicate `migrate_v11_to_v12` function (build-breaking)
- Missing `migrate_v10_to_v11` after conflict resolution
- Merged two v11→v12 functions into one with ALTER TABLE for app columns

### Rounds 3-5: Logic Gaps (P1)
- Manifest ownership: symlink fallback deleting without checking manifest
- SQLite PRAGMA foreign_keys inside savepoint = ignored
- Workspace deduplication: INSERT OR IGNORE losing group associations
- clear_skills_dir deleting user-managed files

### Rounds 6-8: Edge Cases (P1)
- Windows rename() failing when target exists (not atomic-replace like Unix)
- Manifest empty (`[]`) causing re-bootstrap every sync
- Legacy copy-fallback deployments without .cc-switch-managed marker
- Orphan symlink recovery after manifest write failure
- Path traversal via manifest entries (`../` escaping skills_dir)

### Rounds 9-12: Content Verification Escalation
Round 9:  name-based matching (active_dir_names)
Round 10: filename subset checking (is_subset_of_ssot)  
Round 11: filename majority + no_foreign check
Round 12: recursive byte-comparison (dir_content_equals)

User suggestion at round 10: "Claude self-review before Codex" — cut 2 rounds.

### Rounds 13-15: Error Handling (P2)
- copy_dir partial failure leaving orphan directories
- Marker write failure silently succeeding → permanent zombie
- Manifest write failure silently succeeding → tracking loss
- Deletion failure leaving entries permanently unmanaged

### Rounds 16-18: Deep Verification
- v16→v17 migration for databases already past v10 (missing rollup columns)
- Partial schema repair preserving existing column data
- Content comparison: subset→equality (user's SKILL.md-only directory bypass)
- Recursive byte-comparison for exact content match

### Round 19: CLEAN
Codex: "No discrete, actionable regressions were identified."

## Key Learnings

1. Self-review cut rounds by 40%: User suggested Claude self-review before Codex cross-review
2. Content ownership is an arms race: Filename→subset→byte-comparison→equality. Jump to strongest first.
3. 19 rounds is not a failure: Each round exposed deeper issues. Layer-by-layer discovery is inherent.
4. Max-turns needs extra headroom: Content byte-comparison required 18 turns (vs default 10-12).
5. Both agents needed: Claude fixed; Codex found what Claude missed. Neither alone would catch everything.

## Final Stats

| Metric | Value |
|--------|-------|
| Total rounds | 19 |
| Issues found/fixed | 30+ |
| P0 (build-breaking) | 2 |
| P1 (functional/security) | 18 |
| P2 (edge/error-handling) | 12 |
| Claude max-turns used | Up to 18 |
| Codex review time | 3-8 min each |
| Files changed | schema.rs (+198), workspace_skill.rs (+510), mod.rs (±2) |
| Net code change | +665 / -45 lines |
