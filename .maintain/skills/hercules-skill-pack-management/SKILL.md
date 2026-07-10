---
name: hercules-skill-pack-management
description: "Maintain the exact-five Hercules runtime layout, initializer transport, maintainer boundary, validation, and repository synchronization."
version: 2.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, skills, repository-layout, validation]
    related_skills: [hercules, hercules-capability-discovery, hercules-collaborative-workflow, hercules-review-workflow, hercules-project-init]
---

# Hercules Skill Pack Management

The runtime is exactly:

```text
skills/hercules/SKILL.md
skills/hercules-capability-discovery/SKILL.md
skills/hercules-collaborative-workflow/SKILL.md
skills/hercules-review-workflow/SKILL.md
skills/hercules-project-init/SKILL.md
```

`$HERMES_HOME/skills/hercules` points to `$HERCULES_HOME/skills`. Use
`bash init.sh` for clone/fast-forward transport and symlink creation. Maintainer
Skills, tests, examples, and history stay under `.maintain/`.

Inspect before editing, preserve the exact-five set and single public entry,
run strict/unit/privacy checks, and require fresh-clone evidence for migration.
