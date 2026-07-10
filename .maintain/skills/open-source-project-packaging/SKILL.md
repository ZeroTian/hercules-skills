---
name: open-source-project-packaging
description: "Use when turning a Hercules or agent-workflow repository into a reader-facing open-source project: bilingual README, license selection, third-party attribution, dependency-vs-vendor boundaries, validation, and independent review."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, open-source, readme, license, attribution, release, governance]
    related_skills: [agent-plugin-dependency-governance, staged-commit-package-governance, skill-pack-governance-validation, github-repo-management]
---

# Open-Source Project Packaging

## Overview

Use this skill when the user asks to package a Hercules/agent-workflow repository for public open source release: standard README, bilingual presentation, license choice, attribution, and release-readiness checks.

The goal is a reader-facing project entry point backed by real validation and independent review. Keep long operating rules in governance docs; README should explain what the project is, why it exists, how to install/use/validate it, and how third-party boundaries work.

## When to Use

Use when the user asks for:

- a standard open-source `README.md`;
- English + Chinese README content;
- license selection for a repo that was inspired by, depends on, or partially absorbed external open-source work;
- `LICENSE`, `NOTICE`, or third-party attribution boundaries;
- public-release packaging of a Hercules skill pack or agent-workflow repo.

Pair with `agent-plugin-dependency-governance` when the work involves external Claude/Codex/agent plugins. Pair with `staged-commit-package-governance` before commit.

## Procedure

1. **Inventory current repo state.** Check Git status, tracked files, existing README/license/notice files, and relevant positioning docs. Do not overwrite unrelated user work.
2. **Verify upstream license facts.** For any external project mentioned, use authoritative sources: upstream `LICENSE`, GitHub license API, package metadata, or release metadata. Record SPDX IDs and source paths.
3. **Classify the third-party relationship.** Distinguish:
   - ideas/patterns/process inspiration;
   - optional dependency;
   - copied snippets;
   - vendored source or derivative fork.
4. **Choose license by actual boundary.** If no upstream source is vendored and the project only absorbs ideas/policy/workflow around optional dependencies, the repo can usually keep its own permissive license. Prefer continuity with existing project metadata. If source is copied or vendored, re-review compatibility and notice obligations before release.
5. **Write reader-facing README.** Include title, one-line pitch, why it exists, features, quickstart, install, usage, validation, repository layout, external dependencies, contribution rules, and license. Keep detailed agent operating rules in `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, or `docs/`.
6. **Handle bilingual output deliberately.** Either use one `README.md` with English and Chinese sections linked at top, or separate `README.md` + `README.zh-CN.md`; keep skill lists and counts synchronized across languages.
7. **State third-party boundaries plainly.** README should name important upstream projects, their license, whether they are optional dependencies, and whether their source is vendored. Avoid implying affiliation or endorsement.
8. **Add license/notice files.** Add top-level `LICENSE`. Add `NOTICE` or `THIRD_PARTY_NOTICES.md` when vendored content or license terms require it, or when attribution would otherwise be easy to miss.
9. **Validate and review.** Run repository validators, package checks, diff whitespace checks, and staged privacy scans. Send the staged README/license package to independent Codex review for license boundary, attribution, overclaiming, stale counts, and accidental vendoring.
10. **Commit only after PASS.** If the user has authorized auto-commit, commit after validation + Codex PASS. Do not push unless separately authorized.

## License Decision Rules of Thumb

- **Ideas only + optional dependency + no copied source:** project may choose its own license; MIT is appropriate for simple personal workflow packs, Apache-2.0 is appropriate when patent grants/enterprise signaling matter.
- **Existing skill/project metadata already says MIT:** prefer MIT unless new copied code creates a compatibility reason to change.
- **Apache-2.0 upstream dependency not vendored:** MIT project license can still be reasonable; acknowledge upstream Apache-2.0 and keep upstream source upstream.
- **Copied Apache-2.0 source:** preserve required notices and license text; consider Apache-2.0 or dual strategy after review.
- **GPL/AGPL/LGPL/MPL source or unclear provenance:** stop and do a focused license review before publishing.

This is engineering guidance, not legal advice.

## README Checklist

- [ ] Project title and one-line pitch.
- [ ] Clear statement of what the project is and is not.
- [ ] Why/positioning section with no overclaiming.
- [ ] Features grounded in actual repository artifacts.
- [ ] Quickstart commands that exist.
- [ ] Install/migration instructions.
- [ ] Validation/release-gate commands.
- [ ] Repository layout.
- [ ] External dependency and third-party license boundaries.
- [ ] Contributing expectations.
- [ ] License section pointing to `LICENSE`.
- [ ] Bilingual sections synchronized if present.

## Codex Review Prompt Focus

Ask Codex to check:

- whether the selected license is reasonable under the dependency-vs-vendor boundary;
- whether README states third-party licenses and non-vendoring accurately;
- whether bilingual skill lists/counts match tracked files;
- whether README overclaims capabilities or confuses the project with upstream tools;
- whether secrets or credential-like content leaked;
- whether only intended files are staged.

## Pitfalls

1. **License-by-vibes.** Do not choose a license before checking upstream license metadata and whether source was copied.
2. **Hidden vendoring.** README saying “not vendored” is false if commands, prompts, hooks, scripts, or internal plugin files were copied.
3. **README as rulebook.** Keep README public-facing; put operational constraints in governance docs.
4. **Bilingual drift.** English and Chinese skill lists/counts easily diverge; compare both against tracked files before review.
5. **Attribution overclaim.** “Inspired by” and “optional interoperability” are safer than language implying official affiliation, fork status, or endorsement.

## References

- `references/readme-license-boundary.md` — Hercules 2026-07 case: bilingual README + MIT license while treating Apache-2.0 `codex-plugin-cc` as non-vendored optional dependency.
