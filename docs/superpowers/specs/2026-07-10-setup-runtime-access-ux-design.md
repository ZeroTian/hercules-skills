# Setup And Runtime Access UX Design

## Goal

Make Hercules setup output understandable and keep authentication/provider configuration entirely user-managed.

## Approved Product Rules

1. `setup` and `setup --dry-run` check whether Claude Code and Codex CLI are installed, but never inspect or modify their login state.
2. `doctor` reports binary, repository, runtime-skill, validator, and optional-plugin health. It does not run `claude auth status` or `codex login status` and does not classify missing third-party authentication as `BLOCKED`.
3. Hercules never launches login flows, opens authentication pages, edits API credentials, or recommends one authentication method as mandatory.
4. When Hermes actually invokes Claude Code or Codex CLI and the invocation fails, the workflow reports the observed error, classifies the likely failure category, and gives provider-neutral checks without exposing secrets.
5. Default setup output is concise. Raw plugin, MCP, feature, and deep-capability inventories are available only through explicit verbose mode.

## Setup Output

`setup --dry-run` prints:

- a preview heading;
- selected mode and the guarantee that no changes will be made;
- concise planned repository, symlink, validation, dependency, and optional-plugin actions;
- a completion statement and the command that applies the plan.

It must not print plugin lists, MCP health tables, Codex feature tables, deep plugin inventories, or login instructions.

Normal setup uses the same concise posture. `HERCULES_VERBOSE=1` enables the existing capability inventory for troubleshooting.

## Runtime Failure Contract

On a real Claude/Codex invocation failure, Hermes should distinguish at least:

- executable missing;
- provider/authentication rejection such as HTTP 401/403 or invalid credentials;
- endpoint, DNS, TLS, proxy, or network failure;
- quota/rate-limit failure;
- model/provider configuration failure;
- permission/sandbox failure;
- unknown failure.

The report must include the component, failed operation, sanitized error summary, likely category, provider-neutral checks, and a statement that Hercules did not change authentication configuration.

## Non-goals

- Probing third-party APIs during setup or doctor.
- Validating API keys before the user runs real work.
- Adding a `doctor --probe` mode in this change.
- Installing or configuring provider credentials.

## Verification

- Automated tests prove dry-run output is concise and does not execute auth/capability inventory commands.
- Automated tests prove doctor does not execute Claude/Codex login-status commands or report auth blockers.
- Static workflow validation confirms runtime failure guidance exists for both Claude and Codex.
- Existing validator, shell syntax, fresh-clone, and package checks remain green.
