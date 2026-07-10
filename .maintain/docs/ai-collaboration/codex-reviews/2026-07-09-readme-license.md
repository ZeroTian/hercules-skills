# Codex Review — bilingual README and project license

Date: 2026-07-09
Reviewer: Codex CLI (`codex exec`, reasoning effort `xhigh`)
Scope: staged README/license package for open-source publishing.

## Staged files reviewed

- `README.md`
- `LICENSE`

## Review brief

Review whether the staged package satisfies the user request to create a standard open-source README with English and Chinese versions and to choose an appropriate open-source license given the repository's external absorption boundary.

Important facts supplied to review:

- Hercules does not vendor upstream `openai/codex-plugin-cc` source.
- `openai/codex-plugin-cc` is treated as an optional external dependency.
- GitHub API/package metadata showed upstream `openai/codex-plugin-cc` license as Apache-2.0.
- Existing Hercules skill metadata generally uses MIT where project-level license metadata is present.
- README must remain reader-facing; long operating rules belong in governance docs.

## Codex verdict

PASS, highest_severity: none.

No staged-scope findings.

## Codex notes

- MIT is reasonable under the stated dependency-vs-vendor boundary.
- The README clearly states that third-party tools, skills, and plugins keep their own licenses.
- The README clearly states that OpenAI `codex-plugin-cc` is Apache-2.0 upstream and is not vendored into this repository.
- The bilingual README skill lists are synchronized: both English and Chinese blocks contain 22 entries and match `skills/*/SKILL.md` exactly.
- Staged files were only `README.md` and `LICENSE`; no vendored plugin/source files were staged.

## Verification observed by Codex

```text
python3 scripts/validate-skill-pack.py --strict
0 errors / 0 warnings / 3 advisory reflection signals

git diff --check && git diff --cached --check
PASS

README skill-list comparison
both English and Chinese blocks match tracked skills
```

## Residual risks / non-goals

- This is an engineering license recommendation, not legal advice.
- If future work vendors Apache-2.0 or other third-party source content, the license/notice strategy must be re-reviewed before release.
- The staged package does not push to GitHub.
