# Hercules Controller-Owned Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and superpowers:verification-before-completion. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent Claude Code and Codex CLI selected by Hermes from recursively entering Hercules routing.

**Architecture:** Make Hermes the sole Hercules controller, mark facility invocations as already routed, and keep selected facilities within their bounded execution or review role. Enforce the boundary through runtime-contract tests and repository dogfood instructions.

**Tech Stack:** Markdown runtime contracts, Python 3 `unittest`, repository validation scripts.

## Global Constraints

- Preserve exactly one public runtime Skill: `skills/hercules/SKILL.md`.
- Do not install, configure, authenticate, commit, push, or touch `.DS_Store`.
- Write tests before runtime contract changes and observe the expected RED.
- Keep dated historical records unchanged.

---

### Task 1: Lock controller ownership with failing tests

**Files:**
- Modify: `.maintain/tests/test_runtime_skill_contract.py`

**Interfaces:**
- Consumes: current `SKILL.md`, `collaborative-workflow.md`, `project-init.md`, and root instruction files.
- Produces: regression assertions for controller ownership, route-complete briefs, adapter separation, and version `1.1.3`.

- [x] Add tests asserting that the public Skill names Hermes as controller and forbids selected-facility reentry.
- [x] Add tests asserting that implementation and review briefs contain `controller`, `route_state`, `facility`, `role`, and `authority` and return failure to Hermes.
- [x] Replace old shared-routing assertions with controller/facility separation assertions.
- [x] Run the focused test class and confirm failures point to the missing controller-owned contract.

The tests must assert these exact contract phrases:

```python
def test_public_entry_is_hermes_controller_owned(self):
    text = self.text("hercules")
    for phrase in (
        "Hermes controller owns Hercules routing",
        "the route is complete",
        "must not load Hercules",
        "must not perform capability discovery",
        "must not select another facility",
    ):
        self.assertIn(phrase, text)

def test_collaboration_brief_marks_the_facility_as_already_routed(self):
    text = self.reference_text("collaborative-workflow.md")
    brief = self.markdown_section(text, "Invocation Brief", 2)
    for phrase in (
        "controller: Hermes",
        "route_state: selected",
        "facility: <confirmed facility>",
        "role: <capability role>",
        "authority: read-only | write-capable",
        "return the failure to Hermes",
    ):
        self.assertIn(phrase, brief)
```

The project-init and repository-dogfood tests must additionally prove that
the shared/Codex/Claude sections contain direct bounded execution and no
Hercules entry, while the Hermes adapter alone contains Hercules loading,
capability discovery, fallback, and final verification.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  .maintain/tests/test_runtime_skill_contract.py \
  RuntimeSkillContractTest InvocationLifecycleContractTest -v
```

Expected: FAIL because the existing shared contract still requires every agent to route through Hercules and the version is still `1.1.2`.

### Task 2: Implement the minimal controller-owned contract

**Files:**
- Modify: `skills/hercules/SKILL.md`
- Modify: `skills/hercules/references/collaborative-workflow.md`
- Modify: `skills/hercules/references/review-workflow.md`
- Modify: `skills/hercules/references/project-init.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `HERMES.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the failing tests from Task 1.
- Produces: Hermes-only routing and direct selected-facility execution.

- [x] Add the controller ownership/no-reentry invariant and bump the Skill patch version to `1.1.3`.
- [x] Add the structured already-routed context to every implementation and review invocation brief.
- [x] Move discovery, fallback, and final verification out of the shared contract and into the Hermes adapter.
- [x] Update repository dogfood instructions to match the generated contract without broadening existing Claude/Codex roles.
- [x] Add one concise README sentence explaining that selected facilities execute directly.
- [x] Re-run the focused tests and confirm GREEN.

Use this runtime wording as the canonical invariant:

```markdown
Hermes controller owns Hercules routing. After it selects a facility, the
route is complete: the selected facility executes the bounded brief directly
and must not load Hercules, perform capability discovery, select another
facility, or apply controller fallback.
```

Every invocation brief must include this exact route context:

```text
controller: Hermes
route_state: selected
facility: <confirmed facility>
role: <capability role>
authority: read-only | write-capable
```

### Task 3: Verify scope and repository gates

**Files:**
- Verify all changed files; do not add unrelated changes.

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: fresh acceptance evidence and a Codex review verdict.

- [x] Run the full unittest suite.
- [x] Run strict validation, package check, fresh-clone smoke, Bash syntax, and whitespace checks.
- [x] Inspect `git diff`, verify `.DS_Store` remains untouched, and search for stale active shared-routing language.
- [x] Record the route, facility, fallback, verification, and any residual migration risk.

## Execution Record

- Route: Hercules implementation -> Claude Code 2.1.206 selected -> external network invocation rejected -> current Codex local write-capable fallback.
- TDD: initial RED 7 expected contract failures; review-gap RED 2 failures; final focused GREEN.
- Verification: full suite 122 tests passed; strict validator 0 errors / 0 warnings; package check passed; unstaged-inclusive fresh-clone smoke passed; Bash and diff checks passed.
- Independence: implementation and final review share the current Codex context because external Claude access was rejected. This is reported as a review-independence gap, not hidden as an independent PASS.
- Migration: existing initialized projects still require an approved idempotent instruction update; `init.sh` does not edit them.
