# Hercules Skill-First Lightweight Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Contract Hercules from a 25-Skill environment manager into a five-Skill adaptive runtime with one non-invasive initializer and a hidden maintainer boundary.

**Architecture:** `init.sh` only clones or fast-forward updates `$HOME/.hercules` and symlinks its five runtime Skills into Hermes. `/skill hercules` classifies task needs, delegates demand-led discovery to an internal Skill, then composes collaboration, review, or project initialization without installing or configuring any external facility. Repository validation, historical governance, and domain examples move under `.maintain/` and are never runtime-discoverable.

**Tech Stack:** Bash 3.2+, Markdown Hermes Skills, Python 3 standard-library `unittest`, Git.

## Global Constraints

- Default runtime contains exactly: `hercules`, `hercules-capability-discovery`, `hercules-collaborative-workflow`, `hercules-review-workflow`, and `hercules-project-init`.
- `/skill hercules` is the only user-documented runtime entry.
- `init.sh` may verify Git/Hermes, clone/fetch/fast-forward the Hercules checkout, create directories, and create the expected symlink; it may not install or configure anything.
- No initialization or runtime path may call npm, pnpm, brew, apt, Claude/Codex plugin installers, marketplaces, login commands, or provider configuration commands.
- Claude, Codex, MCP, plugins, custom agents, browser tools, and additional Skills are optional capability sources, never required dependencies.
- Capability discovery is task-demand-led; no full inventory runs at initialization or at the start of every task.
- Provider/access state is diagnosed only after a real invocation fails, with sanitized output and no automatic remediation.
- Maintainer Skills, tests, validators, review history, and domain examples live under `.maintain/` and are not linked into Hermes.
- Old `--full`, `--minimal`, `doctor`, `doctor --fix`, `bootstrap`, `status`, and package-helper product commands are removed without compatibility aliases.
- macOS, Linux, and WSL remain supported; public shell must pass the system Bash 3.2 syntax check.
- Preserve unrelated user changes. Run commit steps only when the user has explicitly authorized implementation commits; otherwise record the same checkpoints without committing.

---

## Target File Map

### Public runtime and initialization

- Create: `init.sh` — the only public executable; clone/update + symlink only.
- Rewrite: `README.md` — value statement and three-step bilingual Quickstart.
- Create: `skills/hercules/SKILL.md` — single public router.
- Create: `skills/hercules-capability-discovery/SKILL.md` — demand-led discovery and plugin exploration.
- Rewrite: `skills/hercules-collaborative-workflow/SKILL.md` — facility-neutral delegation and fallback.
- Create: `skills/hercules-review-workflow/SKILL.md` — verification and independent-review policy.
- Create: `skills/hercules-project-init/SKILL.md` — project-local instruction initialization.

### Maintainer-only boundary

- Create: `.maintain/scripts/check-package.sh` — staged privacy and package checks extracted from the old helper.
- Move: `scripts/validate-skill-pack.py` -> `.maintain/scripts/validate-skill-pack.py`.
- Move: `scripts/smoke-fresh-clone.sh` -> `.maintain/scripts/smoke-fresh-clone.sh`.
- Move: `tests/` -> `.maintain/tests/`.
- Move: `docs/ai-collaboration/` -> `.maintain/docs/ai-collaboration/`.
- Move: `docs/WHY_HERCULES.md` -> `.maintain/docs/WHY_HERCULES.md`.
- Move after implementation: `docs/superpowers/` -> `.maintain/docs/superpowers/`.
- Create: `.maintain/skills/` for repository-governance Skills.
- Create: `.maintain/examples/skills/` for domain/example Skills.

### Removed product surface

- Delete: `scripts/hercules`.
- Delete: `scripts/install-hercules.sh`.
- Delete after knowledge merge: `skills/hercules-agent-capability-preflight/` including its bootstrap installer.
- Retire: `skills/portable-skill-pack-installation/`.
- Retire: `skills/cli-installer-ux-governance/`.
- Delete merged duplicate runtime Skill directories listed in Task 4.

---

### Task 1: Add the Non-Invasive Initializer

**Files:**
- Create: `init.sh`
- Create: `.maintain/tests/test_init.py`
- Modify: `docs/ai-collaboration/TASKS.md`

**Interfaces:**
- Consumes: an already installed `git` and `hermes`; environment variables `HERCULES_HOME`, `HERMES_HOME`, `HERCULES_REPO_URL`, and `HERCULES_BRANCH`.
- Produces: an idempotent absolute symlink at `$HERMES_HOME/skills/hercules` pointing to `$HERCULES_HOME/skills`; exit `0` on success and nonzero without mutation on conflicts.

- [ ] **Step 1: Open the formal maintainer task**

Add `TASK-015` to `docs/ai-collaboration/TASKS.md` with status `处理中`, owner `Hermes`, design pointer `docs/superpowers/specs/2026-07-10-skill-first-lightweight-architecture-design.md`, and acceptance summary “exactly five runtime Skills; init-only external surface; no dependency installation.”

- [ ] **Step 2: Write failing initializer tests**

Create `.maintain/tests/test_init.py` with these concrete cases:

```python
#!/usr/bin/env python3
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INIT = REPO_ROOT / "init.sh"


class InitScriptTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source"
        self.hercules_home = self.root / "installed"
        self.hermes_home = self.root / "hermes-home"
        self.bin = self.root / "bin"
        self.bin.mkdir()
        (self.bin / "hermes").write_text("#!/bin/sh\necho hermes-test\n")
        (self.bin / "hermes").chmod(0o755)

        (self.source / "skills" / "hercules").mkdir(parents=True)
        (self.source / "skills" / "hercules" / "SKILL.md").write_text("# test\n")
        subprocess.run(["git", "init", "-b", "main", str(self.source)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.source), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.source), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.source), "commit", "-m", "fixture"], check=True, capture_output=True)

    def env(self):
        env = os.environ.copy()
        env.update({
            "PATH": f"{self.bin}:/usr/bin:/bin",
            "HERCULES_HOME": str(self.hercules_home),
            "HERMES_HOME": str(self.hermes_home),
            "HERCULES_REPO_URL": str(self.source),
            "HERCULES_BRANCH": "main",
        })
        return env

    def run_init(self, env=None):
        return subprocess.run(
            ["bash", str(INIT)], cwd=REPO_ROOT, env=env or self.env(),
            text=True, capture_output=True, check=False,
        )

    def test_clone_and_symlink_only(self):
        result = self.run_init()
        runtime = self.hermes_home / "skills" / "hercules"
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(runtime.is_symlink())
        self.assertEqual(runtime.resolve(), (self.hercules_home / "skills").resolve())
        for forbidden in ("npm ", "pnpm ", "brew ", "apt ", "claude ", "codex ", "login", "plugin install"):
            self.assertNotIn(forbidden, result.stdout + result.stderr)

    def test_rerun_is_idempotent(self):
        self.assertEqual(self.run_init().returncode, 0)
        second = self.run_init()
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

    def test_missing_hermes_stops_before_clone(self):
        env = self.env()
        env["PATH"] = "/usr/bin:/bin"
        result = self.run_init(env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Hermes is required but was not found", result.stderr)
        self.assertFalse(self.hercules_home.exists())

    def test_existing_real_runtime_directory_is_preserved(self):
        runtime = self.hermes_home / "skills" / "hercules"
        runtime.mkdir(parents=True)
        marker = runtime / "keep.txt"
        marker.write_text("keep")
        result = self.run_init()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run tests to verify RED**

Run: `python3 .maintain/tests/test_init.py -v`

Expected: FAIL because `/init.sh` does not exist.

- [ ] **Step 4: Implement the minimal initializer**

Create executable `init.sh` with this behavior:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_URL=${HERCULES_REPO_URL:-https://github.com/ZeroTian/hercules-skills.git}
BRANCH=${HERCULES_BRANCH:-main}
HERCULES_HOME=${HERCULES_HOME:-$HOME/.hercules}
HERMES_HOME=${HERMES_HOME:-$HOME/.hermes}

die() { printf 'Hercules init: %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

have git || die "Git is required but was not found. Install Git using its official instructions, then rerun init."
have hermes || die "Hermes is required but was not found. Install Hermes using its official instructions, then rerun init."

EXPECTED_SOURCE="$HERCULES_HOME/skills"
RUNTIME="$HERMES_HOME/skills/hercules"
if [ -L "$RUNTIME" ]; then
  [ "$(readlink "$RUNTIME")" = "$EXPECTED_SOURCE" ] || die "$RUNTIME is an unrelated symlink; no files were changed."
elif [ -e "$RUNTIME" ]; then
  die "$RUNTIME already exists and was preserved; move it manually before rerunning init."
fi

if [ -d "$HERCULES_HOME/.git" ]; then
  git -C "$HERCULES_HOME" fetch origin "$BRANCH"
  git -C "$HERCULES_HOME" merge --ff-only "origin/$BRANCH"
elif [ -e "$HERCULES_HOME" ]; then
  die "$HERCULES_HOME exists but is not a Hercules Git checkout; no files were changed."
else
  mkdir -p "$(dirname "$HERCULES_HOME")"
  git clone --branch "$BRANCH" "$REPO_URL" "$HERCULES_HOME"
fi

SOURCE=$(cd "$HERCULES_HOME/skills" && pwd -P)
mkdir -p "$(dirname "$RUNTIME")"

if [ -L "$RUNTIME" ]; then
  [ "$(readlink "$RUNTIME")" = "$SOURCE" ] || die "$RUNTIME no longer points to the installed Skills."
else
  ln -s "$SOURCE" "$RUNTIME"
fi

printf 'Hercules Skills are ready.\n'
printf '1. hermes --tui\n'
printf '2. /skill hercules\n'
```

- [ ] **Step 5: Verify GREEN and shell portability**

Run:

```bash
chmod +x init.sh
python3 .maintain/tests/test_init.py -v
bash -n init.sh
git diff --check
```

Expected: 4 tests pass; Bash syntax and diff checks exit `0`.

- [ ] **Step 6: Commit the initializer checkpoint if authorized**

```bash
git add init.sh .maintain/tests/test_init.py docs/ai-collaboration/TASKS.md
git commit -m "feat: add non-invasive Hercules initializer"
```

---

### Task 2: Create the Public Entry and Demand-Led Discovery Skills

**Files:**
- Create: `skills/hercules/SKILL.md`
- Create: `skills/hercules/references/runtime-routing.md`
- Create: `skills/hercules-capability-discovery/SKILL.md`
- Create: `skills/hercules-capability-discovery/references/capability-map.md`
- Create: `skills/hercules-capability-discovery/references/plugin-exploration.md`
- Create: `.maintain/tests/test_runtime_skill_contract.py`

**Interfaces:**
- Consumes: a user task plus locally visible, non-secret facility metadata.
- Produces: a task-role list, an ephemeral capability map, and routing to one of the other four core Skills; no installation request or fixed plugin requirement.

- [ ] **Step 1: Write failing runtime-contract tests**

Create `.maintain/tests/test_runtime_skill_contract.py`:

```python
#!/usr/bin/env python3
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"
CORE = {
    "hercules",
    "hercules-capability-discovery",
    "hercules-collaborative-workflow",
    "hercules-review-workflow",
    "hercules-project-init",
}


class RuntimeSkillContractTest(unittest.TestCase):
    def text(self, name):
        return (SKILLS / name / "SKILL.md").read_text()

    def test_public_entry_routes_by_task_need(self):
        text = self.text("hercules")
        for phrase in ("single public entry", "task capability roles", "session capability cache", "fallback"):
            self.assertIn(phrase, text)

    def test_discovery_is_demand_led_and_provider_neutral(self):
        text = self.text("hercules-capability-discovery")
        for phrase in ("demand-led", "shallow discovery", "deep plugin exploration", "ephemeral capability map"):
            self.assertIn(phrase, text)
        for forbidden in (
            "npm install", "pnpm add", "brew install", "apt-get install",
            "claude plugins install", "marketplace add", "claude auth", "codex login",
        ):
            self.assertNotIn(forbidden, text)

    def test_no_plugin_is_declared_required(self):
        combined = "\n".join(
            path.read_text() for path in SKILLS.glob("*/SKILL.md") if path.parent.name in CORE
        )
        self.assertIsNone(re.search(r"required plugins?\s*:", combined, re.I))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify RED**

Run: `python3 .maintain/tests/test_runtime_skill_contract.py -v`

Expected: FAIL because `skills/hercules` and `skills/hercules-capability-discovery` do not exist.

- [ ] **Step 3: Create the `hercules` entry Skill**

Use this exact frontmatter and section contract in `skills/hercules/SKILL.md`:

```markdown
---
name: hercules
description: "Single public entry for adaptive Hercules task routing: understand the task, discover only relevant local capabilities, compose internal workflows, and degrade without installing dependencies."
version: 1.0.0
author: Hercules / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hercules, entry, routing, adaptive-orchestration]
    related_skills: [hercules-capability-discovery, hercules-collaborative-workflow, hercules-review-workflow, hercules-project-init]
---

# Hercules

## Purpose

This is the single public entry. Translate the user task into task capability roles, use the session capability cache when fresh, and route only to the internal Skills needed for this task.

## Routing

1. Preserve explicit user preferences and project instructions.
2. Classify task capability roles: implementation, review, browser, research, parallel execution, data access, or project initialization.
3. Load `hercules-capability-discovery` only for roles whose local capability evidence is missing or stale.
4. Route execution to `hercules-collaborative-workflow`, review to `hercules-review-workflow`, and project setup to `hercules-project-init`.
5. Prefer a confirmed local facility; fallback to another confirmed facility or Hermes itself.
6. Report a blocker only when no safe path can satisfy the task.

## Boundaries

- Never install or configure external facilities.
- Never inspect credentials or proactively test provider access.
- Missing optional facilities are silent unless the current task needs them.
- Re-scan after a relevant config change or capability-related invocation failure.

## Completion

Return the selected route, relevant confirmed capabilities, fallback used, and verification result. Do not print a full inventory unless the user asks.
```

Put the same routing decision table, with one row per capability role and destination Skill, in `skills/hercules/references/runtime-routing.md`.

- [ ] **Step 4: Create the discovery Skill and references**

`skills/hercules-capability-discovery/SKILL.md` must contain these exact sections and rules:

```markdown
## Demand-led discovery
Start from task capability roles. Do not inventory every CLI, plugin, MCP, Skill, or agent at session startup.

## Shallow discovery
For relevant facilities only, inspect executable presence/version and locally visible installed/enabled capabilities. Do not inspect login, credentials, provider reachability, or unrelated surfaces.

## Deep plugin exploration
When an installed task-relevant plugin is unfamiliar, read its local manifest, commands, Skills, agents, and documentation. Confirm behavior from those files; never infer behavior from the plugin name.

## Ephemeral capability map
Record role, facility, confirmed surface, authority class, evidence source, and freshness for this session only.

## Selection order
explicit user preference -> project instructions -> confirmed task fit -> safety boundary -> fallback

## Fallback
Try another confirmed facility, then Hermes itself. If neither can safely satisfy the task, report the attempted facility, sanitized failure category, and the minimum user-run check.
```

`references/capability-map.md` defines this record shape:

```text
role: implementation
facility: claude
surface: installed CLI plus confirmed local plugin command
authority: read-only | write-capable
evidence: command or local file inspected
freshness: current-session
```

`references/plugin-exploration.md` requires local manifest/command/Skill/agent evidence and explicitly states that fixed plugin names are examples, not requirements.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/tests/test_init.py -v
git diff --check
```

Expected: runtime-contract tests and initializer tests pass.

- [ ] **Step 6: Commit the entry/discovery checkpoint if authorized**

```bash
git add skills/hercules skills/hercules-capability-discovery .maintain/tests/test_runtime_skill_contract.py
git commit -m "feat: add adaptive Hercules entry and discovery skills"
```

---

### Task 3: Consolidate Collaboration, Review, and Project Initialization

**Files:**
- Rewrite: `skills/hercules-collaborative-agent-workflow/SKILL.md` as `skills/hercules-collaborative-workflow/SKILL.md`
- Create: `skills/hercules-collaborative-workflow/references/invocation-failure.md`
- Create: `skills/hercules-review-workflow/SKILL.md`
- Create: `skills/hercules-review-workflow/references/review-loop.md`
- Create: `skills/hercules-project-init/SKILL.md`
- Create: `skills/hercules-project-init/references/instruction-boundaries.md`
- Modify: `.maintain/tests/test_runtime_skill_contract.py`

**Interfaces:**
- Consumes: task roles and capability map produced by Tasks 1–2.
- Produces: facility-neutral invocation briefs, verified review outcomes, and minimal project instruction files; no fixed Claude/Codex role assignment.

- [ ] **Step 1: Extend tests for all five core contracts**

Add these assertions to `.maintain/tests/test_runtime_skill_contract.py`:

```python
    def test_collaboration_consumes_confirmed_capabilities(self):
        text = self.text("hercules-collaborative-workflow")
        for phrase in ("confirmed capability map", "user and project preference", "sanitized failure category", "fallback"):
            self.assertIn(phrase, text)

    def test_review_requires_independence_only_when_task_requires_it(self):
        text = self.text("hercules-review-workflow")
        self.assertIn("independence requirement", text)
        self.assertIn("available reviewer", text)
        self.assertNotIn("Codex is always required", text)

    def test_project_init_is_project_scoped(self):
        text = self.text("hercules-project-init")
        for phrase in ("project-scoped", "do not install", "preserve existing instructions"):
            self.assertIn(phrase, text)
```

- [ ] **Step 2: Run tests to verify RED**

Run: `python3 .maintain/tests/test_runtime_skill_contract.py -v`

Expected: three new tests fail because the final Skill paths/contracts are absent.

- [ ] **Step 3: Build the collaborative workflow Skill**

Create `skills/hercules-collaborative-workflow/SKILL.md` by retaining only facility-neutral knowledge from:

- `skills/hercules-collaborative-agent-workflow/SKILL.md`;
- `skills/hermes-collaborative-workflow/SKILL.md`;
- `skills/coding-agent-orchestration/SKILL.md`.

Its procedure must be exactly:

1. consume the confirmed capability map;
2. apply user and project preference;
3. classify read-only versus write-capable authority;
4. write a capability-aware brief without naming unavailable surfaces;
5. invoke the selected facility;
6. on failure record a sanitized failure category and choose fallback;
7. run task-appropriate verification and report evidence.

Move the runtime invocation failure contract into `references/invocation-failure.md`. Delete bootstrap/install/remediation, fixed role preferences, TASKS ledger mechanics, Godot-specific cases, and plugin-specific long examples from the runtime Skill.

- [ ] **Step 4: Build the review workflow Skill**

Merge the reusable parts of `cross-agent-review-loop` and `iterative-agent-code-review` into `skills/hercules-review-workflow/SKILL.md`.

The Skill must distinguish:

```text
ordinary verification: use any confirmed suitable reviewer or Hermes verification
independent review requested/required: reviewer must be independent of the implementation actor
no independent reviewer available: report the independence gap; do not install one
review FAIL: return stable findings to the implementation route, then re-review
review PASS: close only after fresh verification evidence
```

Put the fix/re-review state machine and stable finding-ID rules in `references/review-loop.md`.

- [ ] **Step 5: Build the project-init Skill**

Merge project-scoped, cross-agent-compatible instruction initialization from `hercules-project-init-workflow` and `hermes-project-init-orchestration` into `skills/hercules-project-init/SKILL.md`.

The Skill must:

- inspect existing `AGENTS.md`, `CLAUDE.md`, and tool-specific project instructions;
- preserve existing instructions and unrelated files;
- add only project-scoped rules requested by the user;
- never install tools, plugins, Skills, or global configuration;
- verify resulting links/references and show the user the changed files.

Put user-level versus project-level instruction boundaries in `references/instruction-boundaries.md`.

- [ ] **Step 6: Verify GREEN**

Run:

```bash
python3 .maintain/tests/test_runtime_skill_contract.py -v
git diff --check
```

Expected: all five core contract tests pass while old duplicate directories may still coexist temporarily.

- [ ] **Step 7: Commit the consolidated workflow checkpoint if authorized**

```bash
git add skills/hercules-collaborative-workflow skills/hercules-review-workflow skills/hercules-project-init .maintain/tests/test_runtime_skill_contract.py
git commit -m "feat: consolidate Hercules runtime workflows"
```

---

### Task 4: Enforce Exactly Five Default Runtime Skills

**Files:**
- Move eight maintainer Skill directories to `.maintain/skills/`.
- Move seven domain/example Skill directories to `.maintain/examples/skills/`.
- Delete merged or retired runtime Skill directories.
- Modify: `.maintain/tests/test_runtime_skill_contract.py`

**Interfaces:**
- Consumes: the five final Skills from Tasks 2–3.
- Produces: `skills/` containing exactly those five directories; all other knowledge remains either hidden or in Git history.

- [ ] **Step 1: Add the exact runtime-set test**

Add:

```python
    def test_default_runtime_contains_exactly_five_skills(self):
        actual = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(actual, CORE)
```

- [ ] **Step 2: Run the exact-set test to verify RED**

Run: `python3 .maintain/tests/test_runtime_skill_contract.py -v`

Expected: FAIL showing the current 25-Skill set.

- [ ] **Step 3: Move maintainer Skills**

Use `git mv` so history remains traceable:

```bash
mkdir -p .maintain/skills
git mv skills/agent-plugin-dependency-governance .maintain/skills/
git mv skills/hercules-meta-skill-evolution .maintain/skills/
git mv skills/hercules-skill-pack-management .maintain/skills/
git mv skills/open-source-project-packaging .maintain/skills/
git mv skills/skill-pack-governance-validation .maintain/skills/
git mv skills/skill-pack-roadmap-execution .maintain/skills/
git mv skills/staged-commit-package-governance .maintain/skills/
git mv skills/workflow-skill-pack-audit .maintain/skills/
```

Before moving `agent-plugin-dependency-governance`, verify its read-only discovery rules are present in `hercules-capability-discovery`; its installation/remediation rules are intentionally not preserved at runtime.

- [ ] **Step 4: Move domain/example Skills**

```bash
mkdir -p .maintain/examples/skills
git mv skills/evaluation-closed-loop-orchestration .maintain/examples/skills/
git mv skills/godot-rl-metric-regression .maintain/examples/skills/
git mv skills/godot-wsl-artifact-validation .maintain/examples/skills/
git mv skills/kanban-codex-lane .maintain/examples/skills/
git mv skills/kanban-orchestrator .maintain/examples/skills/
git mv skills/kanban-worker .maintain/examples/skills/
git mv skills/open-ended-research-orchestration .maintain/examples/skills/
```

- [ ] **Step 5: Delete merged and retired runtime directories**

After comparing their reusable rules against the new five Skills, remove:

```bash
git rm -r skills/cli-installer-ux-governance
git rm -r skills/coding-agent-orchestration
git rm -r skills/cross-agent-review-loop
git rm -r skills/hercules-agent-capability-preflight
git rm -r skills/hercules-collaborative-agent-workflow
git rm -r skills/hercules-project-init-workflow
git rm -r skills/hermes-collaborative-workflow
git rm -r skills/hermes-project-init-orchestration
git rm -r skills/iterative-agent-code-review
git rm -r skills/portable-skill-pack-installation
```

The old capability bootstrap script is deleted with `hercules-agent-capability-preflight`; do not relocate it.

- [ ] **Step 6: Verify exact runtime set**

Run:

```bash
python3 .maintain/tests/test_runtime_skill_contract.py -v
find skills -mindepth 1 -maxdepth 1 -type d -print | sort
git diff --check
```

Expected: tests pass and `find` prints exactly the five approved directories.

- [ ] **Step 7: Commit the runtime contraction checkpoint if authorized**

```bash
git add skills .maintain/skills .maintain/examples .maintain/tests/test_runtime_skill_contract.py
git commit -m "refactor: contract default runtime to five skills"
```

---

### Task 5: Move Repository Tooling Behind `.maintain/`

**Files:**
- Move: `scripts/validate-skill-pack.py` -> `.maintain/scripts/validate-skill-pack.py`
- Move: `scripts/smoke-fresh-clone.sh` -> `.maintain/scripts/smoke-fresh-clone.sh`
- Create: `.maintain/scripts/check-package.sh`
- Move: `tests/test_validate_skill_pack_cli.py` -> `.maintain/tests/test_validate_skill_pack_cli.py`
- Replace: `tests/test_setup_doctor_ux.py` with init/runtime tests already under `.maintain/tests/`
- Move: `docs/ai-collaboration/` -> `.maintain/docs/ai-collaboration/`
- Move: `docs/WHY_HERCULES.md` -> `.maintain/docs/WHY_HERCULES.md`
- Delete: `scripts/hercules`
- Delete: `scripts/install-hercules.sh`

**Interfaces:**
- Consumes: final five-Skill runtime and `init.sh`.
- Produces: stdlib-only maintainer validation commands with no product CLI exposure.

- [ ] **Step 1: Move scripts, tests, and governance docs**

```bash
mkdir -p .maintain/scripts .maintain/tests .maintain/docs
git mv scripts/validate-skill-pack.py .maintain/scripts/validate-skill-pack.py
git mv scripts/smoke-fresh-clone.sh .maintain/scripts/smoke-fresh-clone.sh
git mv tests/test_validate_skill_pack_cli.py .maintain/tests/test_validate_skill_pack_cli.py
git rm tests/test_setup_doctor_ux.py
git mv docs/ai-collaboration .maintain/docs/ai-collaboration
git mv docs/WHY_HERCULES.md .maintain/docs/WHY_HERCULES.md
git rm scripts/hercules scripts/install-hercules.sh
```

- [ ] **Step 2: Update the validator root and scope**

In `.maintain/scripts/validate-skill-pack.py`, set:

```python
REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_COLLAB = REPO_ROOT / ".maintain" / "docs" / "ai-collaboration"
EXPECTED_RUNTIME_SKILLS = {
    "hercules",
    "hercules-capability-discovery",
    "hercules-collaborative-workflow",
    "hercules-review-workflow",
    "hercules-project-init",
}
```

Replace the 25-Skill navigation comparison with an exact comparison to `EXPECTED_RUNTIME_SKILLS`. Keep frontmatter, linked-file, JSON, strict-mode, and privacy-relevant checks. Remove requirements that maintainer history be visible from README or installed as runtime Skills.

- [ ] **Step 3: Update validator tests and smoke paths**

In `.maintain/tests/test_validate_skill_pack_cli.py` use:

```python
REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / ".maintain" / "scripts" / "validate-skill-pack.py"
```

Run the validator with `str(VALIDATOR_PATH)` rather than `scripts/validate-skill-pack.py`. Point fresh-clone assertions to `.maintain/scripts/smoke-fresh-clone.sh`.

In `.maintain/scripts/smoke-fresh-clone.sh`, replace old helper/bootstrap checks with:

```bash
python3 "$CLONE_DIR/.maintain/scripts/validate-skill-pack.py" --strict
bash -n "$CLONE_DIR/init.sh"
python3 "$CLONE_DIR/.maintain/tests/test_runtime_skill_contract.py" -v
```

- [ ] **Step 4: Create the maintainer package gate**

Create executable `.maintain/scripts/check-package.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"

python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh
git diff --check
git diff --cached --check

if git diff --cached --name-only | grep -Ei '(^|/)(\.env|.*secret.*|.*token.*|.*credential.*|id_rsa|id_ed25519|config\.toml)$'; then
  printf 'sensitive staged filename detected\n' >&2
  exit 1
fi

hits=$(git diff --cached --unified=0 | grep -Ein '(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key[[:space:]]*[:=]|secret[[:space:]]*[:=]|token[[:space:]]*[:=])' || true)
if [ -n "$hits" ]; then
  printf '%s\n' "$hits" >&2
  exit 1
fi

printf 'maintainer package checks passed\n'
```

- [ ] **Step 5: Verify maintainer tooling**

Run:

```bash
chmod +x .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh
python3 .maintain/tests/test_init.py -v
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/tests/test_validate_skill_pack_cli.py -v
python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh
git diff --check
```

Expected: all tests pass; validator has 0 errors and 0 warnings; Bash and diff checks exit `0`.

- [ ] **Step 6: Commit the maintainer-boundary checkpoint if authorized**

```bash
git add .maintain init.sh docs scripts tests
git commit -m "refactor: move repository tooling behind maintainer boundary"
```

---

### Task 6: Rewrite the Public Experience Around One Entry Skill

**Files:**
- Rewrite: `README.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `HERMES.md`
- Modify: `.maintain/tests/test_runtime_skill_contract.py`

**Interfaces:**
- Consumes: `init.sh` and the five final runtime Skills.
- Produces: a bilingual reader path with exactly three Quickstart commands and no environment-management concepts.

- [ ] **Step 1: Add public-surface tests**

Add to `.maintain/tests/test_runtime_skill_contract.py`:

```python
    def test_readme_has_one_entry_and_three_step_quickstart(self):
        text = (REPO_ROOT / "README.md").read_text()
        commands = (
            "curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash",
            "hermes --tui",
            "/skill hercules",
        )
        for command in commands:
            self.assertIn(command, text)
        for forbidden in (
            "--full", "--minimal", "doctor --fix", "bootstrap --check",
            "npm install", "claude plugins install", "codex login",
        ):
            self.assertNotIn(forbidden, text)

    def test_only_init_is_a_public_script(self):
        self.assertTrue((REPO_ROOT / "init.sh").exists())
        scripts = REPO_ROOT / "scripts"
        self.assertFalse(scripts.exists() and any(scripts.iterdir()))
```

- [ ] **Step 2: Run public-surface tests to verify RED**

Run: `python3 .maintain/tests/test_runtime_skill_contract.py -v`

Expected: README test fails on old setup/doctor/bootstrap content.

- [ ] **Step 3: Rewrite README**

Keep the English and Chinese sections short and symmetrical. The first screen must communicate:

```markdown
# Hercules

Hercules is an adaptive Hermes skill group. It discovers the capabilities already installed on your machine and composes them for the current task. It does not install, configure, authenticate, or require Claude, Codex, MCP servers, or plugins.

## Quickstart

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
/skill hercules
```

Hercules starts from the task, inspects only relevant local capabilities, uses confirmed plugins when helpful, and falls back without changing your environment.
```

The Chinese section conveys the same promises. Document the five internal Skills in one compact table. Link maintainer commands only under a final “Contributing” section pointing to `.maintain/README.md`; do not expose them as product commands.

- [ ] **Step 4: Slim repository-agent instructions**

Update `AGENTS.md`, `CLAUDE.md`, and `HERMES.md` so root files contain only actor role, non-destructive boundaries, the five-Skill product invariant, and a pointer to `.maintain/docs/ai-collaboration/`. Remove references to old `scripts/hercules`, bootstrap, installer modes, and the old 25-Skill navigation.

Create `.maintain/README.md` with exact contributor commands:

```bash
python3 .maintain/scripts/validate-skill-pack.py --strict
python3 .maintain/tests/test_init.py -v
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/tests/test_validate_skill_pack_cli.py -v
.maintain/scripts/smoke-fresh-clone.sh
.maintain/scripts/check-package.sh
```

- [ ] **Step 5: Move design/plan records into the maintainer boundary**

After all active implementation references use the new paths:

```bash
mkdir -p .maintain/docs/superpowers
git mv docs/superpowers/specs .maintain/docs/superpowers/specs
git mv docs/superpowers/plans .maintain/docs/superpowers/plans
```

Update the TASK-015 design/plan pointers to `.maintain/docs/superpowers/...`.

- [ ] **Step 6: Verify GREEN**

Run:

```bash
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/scripts/validate-skill-pack.py --strict
rg -n -- '--full|--minimal|doctor --fix|bootstrap --check|npm install|claude plugins install|codex login' README.md init.sh skills AGENTS.md CLAUDE.md HERMES.md
git diff --check
```

Expected: tests and validator pass; `rg` returns no matches; diff check exits `0`.

- [ ] **Step 7: Commit the public-experience checkpoint if authorized**

```bash
git add README.md AGENTS.md CLAUDE.md HERMES.md .maintain docs
git commit -m "docs: focus Hercules on one adaptive skill entry"
```

---

### Task 7: Full Acceptance, Independent Review, and Closure

**Files:**
- Modify: `.maintain/docs/ai-collaboration/TASKS.md`
- Create: `.maintain/docs/ai-collaboration/codex-reviews/2026-07-10-skill-first-lightweight-architecture.md`
- Modify only if findings require fixes: files from Tasks 1–6.

**Interfaces:**
- Consumes: complete implementation package.
- Produces: fresh test evidence, staged privacy proof, independent PASS, and a truthful closed maintainer task.

- [ ] **Step 1: Run the complete automated suite**

Run:

```bash
python3 .maintain/tests/test_init.py -v
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/tests/test_validate_skill_pack_cli.py -v
python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh
git diff --check
```

Expected: every test passes; validator reports 0 errors / 0 warnings; syntax and diff checks exit `0`.

- [ ] **Step 2: Run a fresh isolated initialization smoke**

Use a temporary HOME and a fake `hermes` executable; point `HERCULES_REPO_URL` at the local repository so no third-party install is possible. Verify that the only created runtime link resolves to the five-Skill checkout and that running twice succeeds.

Run `.maintain/scripts/smoke-fresh-clone.sh` after staging the intended package.

Expected: fresh clone, init, exact five-Skill check, and rerun all pass without npm/brew/apt/provider/plugin calls.

- [ ] **Step 3: Run forbidden-behavior and public-surface scans**

```bash
rg -n -- 'npm install|pnpm add|brew install|apt-get install|marketplace add|plugins install|claude auth|codex login' init.sh skills README.md
find skills -mindepth 1 -maxdepth 1 -type d -print | sort
```

Expected: `rg` returns no matches; the directory listing contains only the five approved runtime Skills.

- [ ] **Step 4: Stage the intended package and run package gate**

```bash
git add -A
.maintain/scripts/check-package.sh
git diff --cached --stat
git diff --cached --check
```

Expected: package gate prints `maintainer package checks passed`; staged paths match this plan; no unrelated changes are staged.

- [ ] **Step 5: Request independent Codex review**

The review brief must verify:

- exactly five default runtime Skills and one public entry;
- no hidden install/config/auth/plugin-management behavior;
- demand-led discovery and generic plugin exploration are preserved;
- missing facilities degrade instead of blocking unrelated work;
- maintainer/example Skills cannot be runtime-discovered;
- init conflict handling preserves user files;
- README stays at the three-step user path;
- all tests and staged privacy checks genuinely cover the staged package.

Write findings with stable IDs under `.maintain/docs/ai-collaboration/codex-reviews/2026-07-10-skill-first-lightweight-architecture.md`. Fix every P0–P3 finding and request a narrow recheck until PASS.

- [ ] **Step 6: Close TASK-015 truthfully**

Only after independent PASS, update TASK-015 to `已完成`, owner/next owner `无`, record test commands and CR IDs, and point to the final review record. Re-run strict validator and `git diff --cached --check` after the ledger update.

- [ ] **Step 7: Commit the final closure if authorized**

```bash
git add -A
git commit -m "refactor: make Hercules a lightweight adaptive skill group"
```

Do not push unless the user separately asks.
