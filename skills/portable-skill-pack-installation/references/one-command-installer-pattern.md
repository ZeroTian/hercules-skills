# One-command installer pattern

Use this reference when productizing a Hercules/Hermes skill pack installer.

## Recommended command model

Public docs should lead with user intent rather than implementation flags:

```bash
scripts/install-hercules.sh --full      # recommended complete setup
scripts/install-hercules.sh --minimal   # minimal setup, no Claude plugin mutation
scripts/install-hercules.sh --dry-run   # preview only, no writes
```

Preserve compatibility aliases when they already exist:

```bash
--full     ~= --yes --optional
--minimal  ~= --yes
--dry-run  ~= --check
```

## setup / doctor split

- `setup`: may install or mutate after the selected mode is explicit.
- `doctor`: read-only by default; outputs a dashboard.
- `doctor --fix`: performs safe minimal repairs by calling setup/installer.
- `doctor --fix --full`: additionally aligns optional Claude/plugin dependencies.
- `doctor --json`: machine-readable for CI/agent automation.
- `doctor --strict`: release gate; warnings/fixable/blockers produce nonzero exit.
- Provider/login state is not probed. A real Claude/Codex invocation owns provider-access diagnosis.

## Safety rules

`--dry-run` / `--check` must not:

- clone or pull a repository;
- install OS packages, npm packages, Hermes, Claude, Codex, or plugins;
- write npm/pnpm registry config;
- create backups or alter symlinks;
- execute repo-local scripts that would be missing because clone was skipped.
- dump plugin, MCP, feature, or deep-capability inventories by default.

The preview should end with a short “no changes were made” statement and the exact command that applies the selected plan. Keep deep inventories behind an explicit verbose mode.

## Provider boundary

Setup and doctor may verify that Claude Code and Codex CLI executables exist. They must not inspect or change native login, API keys, external gateways, cloud-provider credentials, or private tokens. If a real workflow invocation fails, report the sanitized observed error and provider-neutral checks; never infer a blocker from an unprobed login state.

Optional Claude plugins must remain gated behind explicit full/optional mode.

## Verification recipe

```bash
bash -n scripts/install-hercules.sh
bash -n scripts/hercules
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh

tmp=/tmp/hercules-dry-run-$(date +%s)
scripts/install-hercules.sh --dry-run --repo-dir "$tmp" --skip-os-packages --skip-hermes-install --skip-bootstrap
test ! -e "$tmp"

tmp=/tmp/hercules-setup-dry-run-$(date +%s)
scripts/hercules setup --dry-run --repo-dir "$tmp" --skip-os-packages --skip-hermes-install --skip-bootstrap
test ! -e "$tmp"

scripts/hercules doctor --json | python3 -m json.tool >/dev/null
python3 tests/test_setup_doctor_ux.py -v
python3 scripts/validate-skill-pack.py --strict
scripts/hercules package
git diff --check
git diff --cached --check
```

For review-required packages, ask Codex to inspect the staged diff for installer safety, no hidden side effects, optional plugin gating, docs accuracy, and no credential leakage.
