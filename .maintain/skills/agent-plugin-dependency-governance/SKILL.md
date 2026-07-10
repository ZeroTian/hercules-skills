---
name: agent-plugin-dependency-governance
description: "Evaluate external agent plugins using task-relevant local evidence, authority boundaries, dependency-vs-vendor decisions, and independent review without changing user setup."
version: 2.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, plugins, dependencies, governance, absorption]
    related_skills: [hercules-capability-discovery, hercules-review-workflow, hercules-skill-pack-management]
---

# Agent Plugin Dependency Governance

Use this maintainer Skill to decide whether an external plugin remains an
optional capability source, is rejected, or is explicitly forked with user
approval. Hercules does not install, configure, authenticate, register, or
require the candidate.

## Procedure

1. Record upstream identity, official documentation, version, license, and maintainer.
2. Inspect only installed, task-relevant manifests, commands, Skills, agents, MCP metadata, and documentation.
3. Confirm behavior and authority from evidence; never infer capability from a name.
4. Classify each surface as read-only, state-changing, token-spending, or context-migration.
5. Default to an external capability source plus Hercules-owned policy. Vendoring requires explicit approval.
6. Record non-secret, task-scoped runtime discovery with no setup action.
7. Run `python3 .maintain/scripts/validate-skill-pack.py --strict`, `.maintain/scripts/check-package.sh`, and relevant local tests.
8. Close stable findings only after independent recheck.

Use `templates/external-absorption-decision.md` for the decision record.

`.maintain/docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md`
is historical evidence, not a current command recipe.
