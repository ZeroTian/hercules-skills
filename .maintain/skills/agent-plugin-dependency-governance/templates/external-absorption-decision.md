# External Absorption Decision - <candidate>

Use this template to record a standard absorption decision for an external repo, plugin, or marketplace package. Fill every section; write `n/a` with a reason rather than leaving a field blank. See `skills/agent-plugin-dependency-governance/SKILL.md` for the workflow and `docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md` for a filled example.

Do not paste upstream source, prompts, commands, agents, hooks, or internal files into this record. Capture names and classifications only.

## Upstream identity

- Repository URL:
- Package / marketplace name(s):
- Plugin name(s):
- Install command(s):
- Version / commit inspected:
- License:
- Maintainer:

Notes on identity verification (repository name vs marketplace name vs plugin name can differ):

## Dependency-vs-vendor decision

- Decision: dependency | vendor | partial
- Reason:
- Vendored artifacts (if any): none | <list, only when explicitly approved>
- Hercules-owned skills updated for policy:

## Surfaces and safety classification

List each confirmed surface from the live cache/manifest. Do not assume a surface exists because the plugin is installed.

| Surface | Type | Classification | Default rule |
|---|---|---|---|
|  | command / agent / hook / MCP / script | read-only / state-changing / token-spending / context-migration |  |

Classification legend:

- read-only: review, status, or inspection only; no file or state mutation.
- state-changing: can edit files, run commands, or mutate project/tool state by default.
- token-spending: can launch long-running or billed agent loops.
- context-migration: imports/exports session context or transcripts; verify source restrictions and secret handling.

## Bootstrap / default-install policy

- Detection (default / gated):
- Marketplace registration (default / gated):
- Installation (default / gated, gate flag):
- Audit-only proof (commands + before/after evidence):

## Governance boundary

- Owning Hercules skill:
- Inline-review-is-preliminary note:
- Hermes final review authority:

## Validation evidence

Record exact commands and output (or log links). Do not paraphrase results.

- validator (`python3 scripts/validate-skill-pack.py [--strict]`):
- `git diff --check`:
- bootstrap audit-only proof:
- live cache / manifest scan:
- other:

## Codex review record

- Review record path:
- CR IDs:
- Verdict: PASS | FAIL | BLOCKED
- Fixes applied:

## Residual risks / non-goals

- Untested:
- Out of scope:
- Open questions:
