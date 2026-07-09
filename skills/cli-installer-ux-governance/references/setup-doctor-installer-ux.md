# Setup / doctor installer UX notes

Session-derived rules for productizing a raw installer into a user-friendly CLI experience.

## Command shape

Lead with user intent:

```bash
tool setup --full
tool setup --minimal
tool setup --dry-run
tool doctor
tool doctor --fix
tool doctor --fix --full
tool doctor --json
tool doctor --strict
```

Keep implementation aliases for compatibility, but avoid making them the public happy path:

```text
--full     = recommended complete experience
--minimal  = no optional plugin mutation
--dry-run  = no side effects and no prompts
```

## Safety contracts

- Plain `doctor` is read-only.
- `doctor --json` is also read-only and should not write temp logs.
- `doctor --fix` may repair minimal dependencies.
- `doctor --fix --full` may additionally install optional plugin dependencies.
- `--dry-run` must skip both side effects and confirmation prompts.
- Missing auth is `BLOCKED`, not fixable.

## Review checks

Ask the independent reviewer to verify:

1. No hidden writes in plain `doctor`.
2. No prompts or writes in `--dry-run`.
3. `--full`, `--minimal`, and compatibility flags map to the intended environment variables.
4. Optional plugins are not installed by minimal setup.
5. JSON output is valid and useful for CI/agent automation.
6. README shows product-level commands before implementation flags.
