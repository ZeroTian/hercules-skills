# Usability and Commit-Package Validation Recipe

Use this reference when validating a portable Hercules workflow skill pack before reporting it ready, committing it, pushing it, or claiming migration readiness.

## Current-runtime acceptance

Run from the repository root:

```bash
readlink -f ~/.hermes/skills/hercules
find skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort
git ls-files 'skills/*/SKILL.md' | sort
find docs/ai-collaboration/candidate-skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort
test ! -e skills/hercules
find skills -type l -print
python3 scripts/validate-skill-pack.py
git diff --check
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

Expected steady state:

- runtime `~/.hermes/skills/hercules` resolves to the repository `skills/` directory;
- visible runtime skills match tracked or intentionally staged core skills;
- archived candidates live outside `skills/` and therefore do not load as live skills;
- validator reports 0 errors, 0 warnings, and 0 reflection signals;
- diff whitespace checks and script syntax checks pass;
- bootstrap audit-only completes without mutating setup.

## Skill loading check

Use representative `skill_view` calls through Hermes:

```text
skill_view(name="hercules-skill-pack-management")
skill_view(name="workflow-skill-pack-audit")
skill_view(name="skill-pack-governance-validation")
skill_view(name="hercules-agent-capability-preflight")
```

Also test at least one archived candidate and expect `Skill not found`, for example:

```text
skill_view(name="real-game-closed-loop-validation")
```

## Commit-package acceptance

Before committing or pushing:

1. Inspect `git status --short -uall` and ensure every changed path belongs to the intended package.
2. Stage only the intended package.
3. Re-run validator and diff checks against the staged state.
4. Scan staged filenames and content for secrets or private artifacts.
5. Report `staged / not committed / not pushed` until the user explicitly authorizes commit or push.

A minimal staged privacy scan should catch:

- sensitive filenames such as `.env`, `cookie`, `secret`, `password`, `credential`, or private-key material;
- GitHub tokens (`ghp_`, `github_pat_`), OpenAI/Anthropic keys, AWS access keys, and private key blocks;
- assignment-like `api_key=...`, `token=...`, `password=...`, or `secret=...` values.

Treat false positives explicitly; do not silently ignore them.

## Post-push clone acceptance

After the user authorizes commit and push, validate the remote artifact in a clean clone:

```bash
rm -rf /tmp/hercules-skills-smoke
mkdir -p /tmp/hercules-skills-smoke
git clone https://github.com/ZeroTian/hercules-skills.git /tmp/hercules-skills-smoke/hercules-skills
cd /tmp/hercules-skills-smoke/hercules-skills
git status --short -uall
python3 scripts/validate-skill-pack.py
git diff --check
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

This proves the repository can be cloned and validated independently of the active-development working tree. It does **not** prove a clean-machine migration unless Hermes, Claude, Codex, plugins, and external skill dependencies are absent and then installed or checked from scratch.

## Reporting pattern

Report four buckets:

1. **Current runtime** — symlink, live core skill count, archived-candidate non-loading, representative `skill_view` checks.
2. **Static checks** — validator summary, diff checks, shell syntax.
3. **Packaging checks** — staged package scope and privacy scan.
4. **Migration boundary** — what clone-copy or clean-machine scenarios have and have not been practiced.

Do not collapse these into a single vague "validated" statement.
