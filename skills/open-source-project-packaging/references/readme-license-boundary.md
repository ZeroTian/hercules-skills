# README and License Boundary Case Study

Date: 2026-07-09
Repository: `ZeroTian/hercules-skills`

## Context

The user asked to turn the Hercules skill pack into a standard open-source project with English and Chinese README content and an appropriate license, while accounting for absorbed open-source workflow ideas.

## Boundary decision

- OpenAI `codex-plugin-cc` was checked via authoritative upstream metadata and is Apache-2.0.
- Hercules does **not** vendor `codex-plugin-cc` source, prompts, commands, hooks, scripts, or plugin internals.
- Hercules treats it as an optional external dependency (`codex@openai-codex`) and records governance policy, safety classification, and bootstrap checks around it.
- Because the relationship is ideas/policy/optional-dependency rather than vendored source, Hercules can keep its own project license.
- MIT was selected for continuity with existing Hercules skill metadata and low-friction reuse.

## Verification pattern

1. Check upstream license via GitHub/package metadata or upstream `LICENSE`.
2. Confirm the repository does not contain copied upstream source.
3. Write README third-party boundary statements in both languages.
4. Add/update top-level `LICENSE`.
5. Run validator/package/diff checks.
6. Ask Codex to review license reasonableness, non-vendoring claims, stale bilingual lists, overclaiming, and privacy.

## Pitfall

If future work copies Apache-2.0 or other third-party source into this repository, this decision no longer applies as-is. Re-run a focused license/notice review before release.
