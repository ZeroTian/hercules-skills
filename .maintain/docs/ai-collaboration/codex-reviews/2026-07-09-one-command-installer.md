# Codex Review — one-command Hercules installer

Date: 2026-07-09
Reviewer: Codex CLI (`codex exec`, reasoning effort `xhigh`)
Scope: staged one-command installer package for fresh-machine Hercules installation.

## Staged files reviewed

- `README.md`
- `docs/ai-collaboration/ARCHITECTURE.md`
- `docs/ai-collaboration/SKILL_GROUP_AUDIT.md`
- `docs/ai-collaboration/SKILL_NAVIGATION.md`
- `scripts/install-hercules.sh`
- `skills/hercules-agent-capability-preflight/SKILL.md`
- `skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`
- `skills/open-source-project-packaging/SKILL.md`
- `skills/open-source-project-packaging/references/readme-license-boundary.md`

## User request

Make the installation flow scriptable, including dependency installation, so another machine can one-command install and align dependencies.

## Initial findings

Codex initial review returned `FAIL, highest_severity: P1` with these findings:

- `CR-INSTALL-001` P1 — `--check` failed on fresh remote audit because clone/pull is no-op in check-only mode but the installer still executed a missing repo-local bootstrap path.
- `CR-INSTALL-002` P1 — default install delegated to bootstrap behavior that installed Claude plugin marketplaces/plugins before the optional gate.
- `CR-INSTALL-003` P2 — `scripts/install-hercules.sh` executable bit was not staged.
- `CR-GOV-001` P2 — `SKILL_GROUP_AUDIT.md` still had stale 22-skill inventory/classification wording after adding `open-source-project-packaging`.

## Fixes applied

- `scripts/install-hercules.sh` now supports local-checkout and remote curl-pipe usage; `--check` is audit-only and no longer executes a missing bootstrap path when the repo does not exist.
- The installer covers OS basics where supported, npm/pnpm registry alignment, Hermes installation if missing, repository clone/pull, skill install by symlink or copy, repo validation, and delegated Hercules dependency bootstrap.
- Claude plugin marketplace/plugin installs are gated behind `--optional` / `HERCULES_INSTALL_OPTIONAL=1`. Minimal `--yes` install does not mutate Claude plugin state.
- `scripts/install-hercules.sh` is staged executable (`100755`).
- README documents full install (`--yes --optional`), minimal install (`--yes`), and audit-only mode (`--check`) in English and Chinese.
- Runtime skill inventory is updated to 23 tracked skills after promoting `open-source-project-packaging`.

## Recheck verdict

Final Codex recheck:

```text
PASS.
CR-GOV-001 is resolved.
Full package verdict: PASS, highest_severity: none.
```

## Verification evidence

Hermes and Codex observed these checks:

```text
bash -n scripts/install-hercules.sh skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
PASS

scripts/install-hercules.sh --check --repo-dir /tmp/hercules-nonexistent-final-<ts> --skip-os-packages --skip-hermes-install
exit 0; repo path not created; logs CHECK_ONLY bootstrap path

HERCULES_CHECK_ONLY=1 HERCULES_INSTALL_OPTIONAL=0 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
exit 0; no `claude plugins install`; no `claude plugins marketplace add`; skip logged

git ls-files -s scripts/install-hercules.sh
100755

python3 tests/test_validate_skill_pack_cli.py -v
6 OK

python3 scripts/validate-skill-pack.py --strict
0 errors / 0 warnings / 3 advisory signals

scripts/hercules package
PASS; staged privacy scan ok

git diff --check && git diff --cached --check
PASS
```

## Notes / boundaries

- The installer does not automate interactive auth. Users still run `hermes setup`, `claude auth login --console`, and/or `codex login` when needed.
- Full Claude plugin dependency alignment requires `--optional` by design.
- The package does not vendor Hermes built-in skills or third-party plugin source.
- The package does not push to GitHub.
