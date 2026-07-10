---
name: hercules-skill-pack-management
description: "Use when managing the portable Hercules skill pack repository layout, runtime symlink, backups, validation, and GitHub synchronization."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, skills, repository-layout, symlink, migration, synchronization]
    related_skills: [hercules-collaborative-agent-workflow, hercules-project-init-workflow, hercules-agent-capability-preflight, hercules-meta-skill-evolution]
---

# Hercules Skill Pack Management

## Overview

Use this skill when changing how the user's portable Hercules workflow skill pack is stored, linked, backed up, or synchronized to GitHub. The goal is to keep the Git repository understandable while preserving Hermes runtime compatibility.

Current preferred layout:

```text
Repository: /mnt/e/code/hercules-skills/
Skills:     /mnt/e/code/hercules-skills/skills/<skill>/SKILL.md
Runtime:    ~/.hermes/skills/hercules/<skill>/SKILL.md
Symlink:    ~/.hermes/skills/hercules -> /mnt/e/code/hercules-skills/skills
Remote:     https://github.com/ZeroTian/hercules-skills
```

Do not use the older double-nested layout:

```text
/mnt/e/code/hercules-skills/skills/hercules/<skill>/SKILL.md
```

For this repository, `hercules` is already the project/repository identity; adding another `skills/hercules/` layer inside the repo is confusing unless the repo later becomes a multi-category skill monorepo.

## When to Use

Use when the user asks to:

- change or explain `hercules-skills` repository layout;
- create or repair the symlink between Hermes runtime skills and the Git repository;
- migrate Hercules skills between machines;
- sync local runtime skill changes into `ZeroTian/hercules-skills`;
- avoid duplicate skill-name ambiguity from backups or old copies.

## Procedure

1. **Inspect first.** Check the symlink, resolved target, repo status, and visible `SKILL.md` files before editing.
2. **Keep repo layout flat under `skills/`.** Store skills as `skills/<skill>/SKILL.md`; keep README, `.git/`, release docs, and scripts outside the runtime skill directory.
3. **Point runtime symlink at the skills directory, not repo root.** Preferred active-development link:

   ```bash
   ln -sfn /mnt/e/code/hercules-skills/skills ~/.hermes/skills/hercules
   ```

4. **Do not leave backups under `~/.hermes/skills/`.** Hermes may scan them and report ambiguous duplicate skill names. Put backups under a non-scanned location such as:

   ```text
   ~/.hermes/backups/skills/
   ```

5. **Validate before reporting.** Confirm representative skills load, validate frontmatter, and check `git status`/diff.
6. **Before GitHub push, run privacy checks.** At minimum confirm no tracked or changed filenames match `cookie|token|secret|key|.env|password`, and scan changed files for real secret-looking values.

## Pitfalls

1. **Linking to repo root.** `~/.hermes/skills/hercules -> /mnt/e/code/hercules-skills` exposes README and Git metadata to the runtime skill directory and can confuse skill loading.
2. **Double nesting by habit.** `skills/hercules/<skill>` only makes sense for a multi-category repository; for `hercules-skills`, use `skills/<skill>`.
3. **Backup ambiguity.** Keeping `hercules.backup.*` inside `~/.hermes/skills/` can make `skill_view` fail with duplicate skill-name ambiguity.
4. **Memory-only migration.** Do not rely on model memory to reconstruct the workflow pack; copy or symlink the actual `SKILL.md` files.

## Verification Checklist

- [ ] `~/.hermes/skills/hercules` resolves to `/mnt/e/code/hercules-skills/skills`
- [ ] `skills/<skill>/SKILL.md` exists for all expected Hercules skills
- [ ] No `skills/hercules/<skill>` double nesting remains unless deliberately reintroduced for a multi-category repo
- [ ] Backups are outside `~/.hermes/skills/`
- [ ] Representative Hercules skills load without ambiguity
- [ ] Frontmatter validation passes
- [ ] Git status/diff is understood
- [ ] Sensitive filename/content scan passes before commit or push
