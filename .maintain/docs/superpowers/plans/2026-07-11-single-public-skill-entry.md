# Hercules Single Public Skill Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Hermes discover exactly one Hercules Skill and one slash command, `/hercules`, while preserving the four internal task-routed workflows as references.

**Architecture:** Keep `skills/hercules/SKILL.md` as the only Skill frontmatter entry. Move capability discovery, collaborative execution, review, and project initialization beneath `skills/hercules/references/`; update the router to load those references by task role. Keep the existing managed symlink target unchanged so current installations migrate through a normal repository update.

**Tech Stack:** Bash, Python 3 standard library, Markdown/YAML Skill files, `unittest`, Git, Hermes v0.18.2 integration probe.

## Global Constraints

- The runtime must contain exactly one `SKILL.md`: `skills/hercules/SKILL.md`.
- The only Hercules slash command exposed by Hermes must be `/hercules`.
- Preserve capability routing, cache authority/freshness validation, fallback behavior, project-rule preservation, and review independence semantics.
- Do not install, configure, authenticate, or probe Claude, Codex, MCP servers, plugins, or provider credentials.
- Keep `~/.hermes/skills/hercules -> <checkout>/skills`; do not introduce a symlink migration.
- Existing active sessions refresh with `/reload-skills` or restart.
- Preserve the user's untracked root `.DS_Store`; never stage or modify it.
- Use TDD for every behavior change and commit after each task.

---

## File Map

**Public runtime**

- `skills/hercules/SKILL.md` — sole discoverable Skill and task router.
- `skills/hercules/references/*.md` — internal workflow/reference modules, not slash commands.
- `skills/hercules/references/capability_matrix.py` — deterministic capability decision contract.

**Public UX**

- `init.sh` — install/update/symlink only; print real invocation and reload hint.
- `README.md` — two terminal commands plus `/hercules <task>` inside Hermes.

**Maintainer enforcement**

- `.maintain/scripts/validate-skill-pack.py` — exact-one runtime invariant.
- `.maintain/tests/test_runtime_skill_contract.py` — public/runtime/reference behavior.
- `.maintain/tests/test_maintainer_boundary.py` — validator/navigation/current-doc boundary.
- `.maintain/tests/test_init.py` — initializer output and existing safety behavior.
- `.maintain/docs/ai-collaboration/ARCHITECTURE.md` — current one-Skill architecture.
- `.maintain/docs/ai-collaboration/SKILL_NAVIGATION.md` — one public Skill plus internal reference map.
- `.maintain/docs/ai-collaboration/README.md` — current maintainer entry points.
- `.maintain/skills/hercules-skill-pack-management/SKILL.md` — package-management references for the exact-one layout.

---

### Task 1: Embed Capability Discovery in the Public Skill

**Files:**

- Modify: `.maintain/tests/test_runtime_skill_contract.py:10-110`
- Modify: `skills/hercules/SKILL.md:1-39`
- Modify: `skills/hercules/references/runtime-routing.md`
- Move: `skills/hercules-capability-discovery/SKILL.md` → `skills/hercules/references/capability-discovery.md`
- Move: `skills/hercules-capability-discovery/references/capability-map.md` → `skills/hercules/references/capability-map.md`
- Move: `skills/hercules-capability-discovery/references/plugin-exploration.md` → `skills/hercules/references/plugin-exploration.md`
- Move: `skills/hercules-capability-discovery/references/capability_matrix.py` → `skills/hercules/references/capability_matrix.py`

**Interfaces:**

- Consumes: `decide_route(*, demand, facilities, cache=None, invocation=None, evidence=None) -> dict`.
- Produces: `references/capability-discovery.md` and the unchanged `decide_route` API at `references/capability_matrix.py`.

- [ ] **Step 1: Write the failing path and embedding tests**

Change the contract path and discovery source in `.maintain/tests/test_runtime_skill_contract.py`:

```python
PUBLIC_SKILL = "hercules"
PUBLIC_REFERENCES = SKILLS / PUBLIC_SKILL / "references"
CAPABILITY_CONTRACT = PUBLIC_REFERENCES / "capability_matrix.py"

def reference_text(name):
    return (PUBLIC_REFERENCES / name).read_text(encoding="utf-8")

def test_capability_discovery_is_an_internal_reference(self):
    self.assertFalse((SKILLS / "hercules-capability-discovery").exists())
    text = reference_text("capability-discovery.md")
    for phrase in (
        "demand-led",
        "shallow discovery",
        "deep plugin exploration",
        "ephemeral capability map",
    ):
        self.assertIn(phrase, text)
    self.assertFalse(text.startswith("---"))
```

Keep every existing `CapabilityMatrixBehaviorTest`; only update `CAPABILITY_CONTRACT`.

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python3 -m unittest -v \
  test_runtime_skill_contract.RuntimeSkillContractTest.test_capability_discovery_is_an_internal_reference \
  test_runtime_skill_contract.CapabilityMatrixBehaviorTest
```

from `.maintain/tests/`.

Expected: the embedding test fails because the old directory exists and the new reference/contract paths do not; capability tests fail to load the new path.

- [ ] **Step 3: Move the discovery files and remove Skill frontmatter**

Run:

```bash
git mv skills/hercules-capability-discovery/SKILL.md skills/hercules/references/capability-discovery.md
git mv skills/hercules-capability-discovery/references/capability-map.md skills/hercules/references/capability-map.md
git mv skills/hercules-capability-discovery/references/plugin-exploration.md skills/hercules/references/plugin-exploration.md
git mv skills/hercules-capability-discovery/references/capability_matrix.py skills/hercules/references/capability_matrix.py
```

Delete the YAML frontmatter from `capability-discovery.md`; retain its `# Hercules Capability Discovery` body. Change its linked-file references to local names:

```markdown
Use [capability-map.md](capability-map.md) for the record shape, [plugin-exploration.md](plugin-exploration.md) for deep inspection, and `capability_matrix.py` for the deterministic decision contract.
```

- [ ] **Step 4: Link discovery from the public router**

Update `skills/hercules/SKILL.md`:

```yaml
version: 1.1.0
metadata:
  hermes:
    tags: [hercules, entry, routing, adaptive-orchestration]
```

Replace the discovery routing step with:

```markdown
3. When capability evidence is missing, stale, incomplete, permission-mismatched, or invalidated, load [capability discovery](references/capability-discovery.md) and follow its normalized capability-map contract.
```

Update `runtime-routing.md` to point its discovery prerequisite at `capability-discovery.md`, not a Skill name.

- [ ] **Step 5: Run focused and full runtime tests and verify GREEN**

Run:

```bash
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/scripts/validate-skill-pack.py --strict
```

Expected: runtime tests pass; strict validation has zero errors and warnings.

- [ ] **Step 6: Commit**

```bash
git add skills/hercules .maintain/tests/test_runtime_skill_contract.py
git commit -m "refactor: embed capability discovery in Hercules"
```

---

### Task 2: Embed Execution, Review, and Project Initialization Workflows

**Files:**

- Modify: `.maintain/tests/test_runtime_skill_contract.py:10-190`
- Modify: `skills/hercules/SKILL.md`
- Modify: `skills/hercules/references/runtime-routing.md`
- Move: `skills/hercules-collaborative-workflow/SKILL.md` → `skills/hercules/references/collaborative-workflow.md`
- Move: `skills/hercules-collaborative-workflow/references/invocation-failure.md` → `skills/hercules/references/invocation-failure.md`
- Move: `skills/hercules-review-workflow/SKILL.md` → `skills/hercules/references/review-workflow.md`
- Move: `skills/hercules-review-workflow/references/review-loop.md` → `skills/hercules/references/review-loop.md`
- Move: `skills/hercules-project-init/SKILL.md` → `skills/hercules/references/project-init.md`
- Move: `skills/hercules-project-init/references/instruction-boundaries.md` → `skills/hercules/references/instruction-boundaries.md`

**Interfaces:**

- Consumes: public router task roles and normalized capability records from Task 1.
- Produces: three ordinary internal workflow references linked from `SKILL.md` and `runtime-routing.md`.

- [ ] **Step 1: Write the failing exact-one and internal-reference tests**

Replace the five-Skill set with:

```python
PUBLIC_RUNTIME_SKILLS = {"hercules"}
INTERNAL_WORKFLOW_REFERENCES = {
    "capability-discovery.md",
    "collaborative-workflow.md",
    "review-workflow.md",
    "project-init.md",
}
```

Add:

```python
def test_runtime_contains_exactly_one_discoverable_skill(self):
    skill_files = sorted(SKILLS.rglob("SKILL.md"))
    self.assertEqual(skill_files, [SKILLS / "hercules" / "SKILL.md"])

def test_public_router_links_all_internal_workflows(self):
    text = self.text("hercules")
    linked = set(re.findall(r"references/([a-z-]+\.md)", text))
    self.assertTrue(INTERNAL_WORKFLOW_REFERENCES <= linked)
    for name in INTERNAL_WORKFLOW_REFERENCES:
        self.assertTrue((PUBLIC_REFERENCES / name).is_file(), name)

def test_retired_internal_skill_commands_are_not_discoverable(self):
    for name in (
        "hercules-capability-discovery",
        "hercules-collaborative-workflow",
        "hercules-review-workflow",
        "hercules-project-init",
    ):
        self.assertFalse((SKILLS / name / "SKILL.md").exists(), name)
```

Change the collaboration/review/project-init prose tests to read their new reference files and assert that they do not start with YAML frontmatter.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
python3 -m unittest -v \
  test_runtime_skill_contract.RuntimeSkillContractTest.test_runtime_contains_exactly_one_discoverable_skill \
  test_runtime_skill_contract.RuntimeSkillContractTest.test_public_router_links_all_internal_workflows \
  test_runtime_skill_contract.RuntimeSkillContractTest.test_retired_internal_skill_commands_are_not_discoverable
```

Expected: all three fail because three old workflow Skills remain and the public router does not link the new references.

- [ ] **Step 3: Move workflow files and remove frontmatter**

Run:

```bash
git mv skills/hercules-collaborative-workflow/SKILL.md skills/hercules/references/collaborative-workflow.md
git mv skills/hercules-collaborative-workflow/references/invocation-failure.md skills/hercules/references/invocation-failure.md
git mv skills/hercules-review-workflow/SKILL.md skills/hercules/references/review-workflow.md
git mv skills/hercules-review-workflow/references/review-loop.md skills/hercules/references/review-loop.md
git mv skills/hercules-project-init/SKILL.md skills/hercules/references/project-init.md
git mv skills/hercules-project-init/references/instruction-boundaries.md skills/hercules/references/instruction-boundaries.md
```

For each moved `*.md`, remove only its YAML Skill frontmatter and preserve its workflow body. Update local links to the flattened filenames:

```markdown
[invocation failure](invocation-failure.md)
[review loop](review-loop.md)
[instruction boundaries](instruction-boundaries.md)
```

- [ ] **Step 4: Make the public router load internal references**

Use this routing shape in `skills/hercules/SKILL.md`:

```markdown
4. For implementation, browser, research, parallel execution, or data access, load [collaborative workflow](references/collaborative-workflow.md).
5. When scoped or independent review is required, load [review workflow](references/review-workflow.md).
6. For repository-local AI instructions, load [project initialization](references/project-init.md).
7. Prefer a confirmed local facility; fallback to another confirmed facility or Hermes itself.
8. Report a blocker only when no safe path can satisfy the task.
```

Replace Skill names in `runtime-routing.md` with the corresponding reference links.

- [ ] **Step 5: Run runtime tests and verify GREEN**

Run:

```bash
python3 .maintain/tests/test_runtime_skill_contract.py -v
find skills -name SKILL.md -print
```

Expected: tests pass; `find` prints only `skills/hercules/SKILL.md`.

- [ ] **Step 6: Commit**

```bash
git add -A skills .maintain/tests/test_runtime_skill_contract.py
git commit -m "refactor: make Hercules the only runtime Skill"
```

---

### Task 3: Enforce Exact-One Runtime in Maintainer Gates

**Files:**

- Modify: `.maintain/tests/test_maintainer_boundary.py:11-225`
- Modify: `.maintain/scripts/validate-skill-pack.py:39-45,264-335`
- Modify: `.maintain/docs/ai-collaboration/ARCHITECTURE.md`
- Modify: `.maintain/docs/ai-collaboration/SKILL_NAVIGATION.md`
- Modify: `.maintain/docs/ai-collaboration/README.md`
- Modify: `.maintain/skills/hercules-skill-pack-management/SKILL.md`

**Interfaces:**

- Consumes: exact-one runtime layout from Task 2.
- Produces: `EXPECTED_RUNTIME_SKILLS = {"hercules"}` and a one-row navigation contract.

- [ ] **Step 1: Write failing validator and current-doc tests**

Set the test constant:

```python
EXPECTED_RUNTIME_SKILLS = {"hercules"}
```

Replace the scope tests with:

```python
def test_validator_scope_is_exactly_one_public_skill(self):
    validator = load_validator_module()
    self.assertEqual(validator.EXPECTED_RUNTIME_SKILLS, {"hercules"})

def test_validator_rejects_extra_runtime_skill(self):
    validator = load_validator_module()
    report = validator.Report()
    unexpected = {"hercules", "unexpected-runtime-skill"}
    with (
        mock.patch.object(validator, "git_tracked_skills", return_value=unexpected),
        mock.patch.object(validator, "visible_skill_dirs", return_value=unexpected),
    ):
        validator.check_runtime_skill_scope(report)
    self.assertTrue(any("exact runtime skill scope drift" in e for e in report.errors))

def test_validator_rejects_missing_or_non_entry_navigation(self):
    self.assertTrue(self.navigation_report({}).errors)
    report = self.navigation_report({"hercules": "atom"})
    self.assertTrue(any("entry/composite" in e for e in report.errors))
```

Update the current-document test to require `exactly one runtime Skill`, `skills/hercules/SKILL.md`, and all four internal reference filenames.

- [ ] **Step 2: Run maintainer tests and verify RED**

Run:

```bash
python3 .maintain/tests/test_maintainer_boundary.py -v
```

Expected: failures show the validator and current docs still declare five runtime Skills.

- [ ] **Step 3: Update the validator**

Use:

```python
EXPECTED_RUNTIME_SKILLS = {"hercules"}
```

Change `check_runtime_skill_scope()` documentation to “exactly one public Skill.” Keep its tracked/visible comparison unchanged. In `check_skill_navigation()`, retain the exact set comparison and the `hercules == [("entry/composite", "core")]` assertion; remove the loop that validates internal Skill rows because internal workflows are now references.

- [ ] **Step 4: Update current maintainer documentation**

`ARCHITECTURE.md` must state:

```markdown
Hercules is a skill-first Hermes package with one public initializer and exactly one runtime Skill. The four internal workflows live under `skills/hercules/references/` and are not discovered as slash commands.
```

`SKILL_NAVIGATION.md` must contain one runtime row:

```markdown
| `hercules` | entry/composite | core | Public adaptive entry | Routes to internal references by task need; `skills/hercules/SKILL.md` |
```

Add a separate non-Skill table listing `capability-discovery.md`, `collaborative-workflow.md`, `review-workflow.md`, and `project-init.md` as internal references. Update `.maintain/docs/ai-collaboration/README.md` and `.maintain/skills/hercules-skill-pack-management/SKILL.md` to use the same exact-one terminology and paths.

- [ ] **Step 5: Run maintainer and strict tests and verify GREEN**

Run:

```bash
python3 .maintain/tests/test_maintainer_boundary.py -v
python3 .maintain/tests/test_validate_skill_pack_cli.py -v
python3 .maintain/scripts/validate-skill-pack.py --strict
```

Expected: all tests pass; validator reports zero errors and warnings.

- [ ] **Step 6: Commit**

```bash
git add .maintain/scripts/validate-skill-pack.py .maintain/tests/test_maintainer_boundary.py .maintain/docs/ai-collaboration/ARCHITECTURE.md .maintain/docs/ai-collaboration/SKILL_NAVIGATION.md .maintain/docs/ai-collaboration/README.md .maintain/skills/hercules-skill-pack-management/SKILL.md
git commit -m "refactor: enforce one public Hercules Skill"
```

---

### Task 4: Correct the Installer and Quickstart UX

**Files:**

- Modify: `.maintain/tests/test_init.py:116-129`
- Modify: `.maintain/tests/test_runtime_skill_contract.py:17-185`
- Modify: `init.sh:65-67`
- Modify: `README.md:5-41`

**Interfaces:**

- Consumes: `/hercules` slash command produced by the single Skill.
- Produces: accurate install completion output and bilingual Quickstart.

- [ ] **Step 1: Write failing initializer-output tests**

Add to `InitScriptTest`:

```python
def test_success_output_uses_real_hermes_command(self):
    result = self.run_init()
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("hermes --tui", result.stdout)
    self.assertIn("/hercules <your task>", result.stdout)
    self.assertIn("/reload-skills", result.stdout)
    self.assertNotIn("/skill hercules", result.stdout)
```

- [ ] **Step 2: Write failing README/public-command tests**

Change the Quickstart expectations to two terminal commands:

```python
TERMINAL_QUICKSTART = (
    "curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash",
    "hermes --tui",
)
```

Require one text invocation in each language section:

```python
self.assertIn("/hercules <your task>", english_section)
self.assertIn("/hercules <你的任务>", chinese_section)
```

Replace the old `/skill ...` parser with a Hercules-family command scan:

```python
HERCULES_COMMAND_RE = re.compile(r"(?m)(?<![A-Za-z0-9_/])/(hercules(?:-[a-z0-9-]+)?)")

def test_only_public_hercules_command_is_documented(self):
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [REPO_ROOT / "README.md", REPO_ROOT / "init.sh", *SKILLS.rglob("*.md")]
    )
    commands = {f"/{name}" for name in HERCULES_COMMAND_RE.findall(text)}
    self.assertEqual(commands, {"/hercules"})
    self.assertNotIn("/skill hercules", text)
```

- [ ] **Step 3: Run focused tests and verify RED**

Run:

```bash
python3 -m unittest -v \
  test_init.InitScriptTest.test_success_output_uses_real_hermes_command \
  test_runtime_skill_contract.RuntimeSkillContractTest.test_readme_has_one_entry_and_real_hermes_invocation \
  test_runtime_skill_contract.RuntimeSkillContractTest.test_only_public_hercules_command_is_documented
```

Expected: failures show `/skill hercules`, missing reload guidance, and the old three-line Bash block.

- [ ] **Step 4: Update initializer output**

Replace the final output with:

```bash
printf 'Hercules Skill is ready.\n'
printf '1. Start Hermes: hermes --tui\n'
printf '2. Existing session after an update: /reload-skills\n'
printf '3. Run: /hercules <your task>\n'
```

Do not execute Hermes, reload a session, or modify Hermes configuration.

- [ ] **Step 5: Rewrite the bilingual Quickstart**

Use this English shape:

````markdown
```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
```

Inside Hermes:

```text
/hercules <your task>
```
````

Use the same terminal block in Chinese and `/hercules <你的任务>`. Replace the five-Skill table with a one-entry table for `hercules` and a separate “Internal references / 内部流程” table that does not present slash commands.

- [ ] **Step 6: Run init/runtime tests and verify GREEN**

Run:

```bash
python3 .maintain/tests/test_init.py -v
python3 .maintain/tests/test_runtime_skill_contract.py -v
bash -n init.sh
```

Expected: all pass; active product output contains `/hercules` and no `/skill hercules`.

- [ ] **Step 7: Commit**

```bash
git add init.sh README.md .maintain/tests/test_init.py .maintain/tests/test_runtime_skill_contract.py
git commit -m "fix: document the real Hercules command"
```

---

### Task 5: Record, Verify, and Prove the Single-Entry Release

**Files:**

- Modify: `.maintain/docs/ai-collaboration/TASKS.md`
- Create: `.maintain/docs/ai-collaboration/codex-reviews/2026-07-11-single-public-skill-entry.md`
- Verify: all product, tests, and maintainer gates from Tasks 1-4

**Interfaces:**

- Consumes: final exact-one runtime and corrected `/hercules` UX.
- Produces: TASK-016 closure evidence and an independent review record.

- [ ] **Step 1: Add TASK-016 as `待复核`**

Record:

```markdown
## [ ] TASK-016：Hercules true single public Skill entry

- 当前状态：待复核
- 当前负责人：Codex
- 下一负责人：Codex
- 验收摘要：one discoverable `SKILL.md`; one `/hercules` command; four internal reference workflows; corrected init/README UX
```

Include the exact design and plan paths, commands below, and a trajectory block with `score: provisional` and `ready: false`.

- [ ] **Step 2: Run the complete local suite**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .maintain/tests -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/check-package.sh .maintain/scripts/smoke-fresh-clone.sh
git diff --check
find skills -name SKILL.md -print
```

Expected: all tests pass; strict has zero errors/warnings; only `skills/hercules/SKILL.md` is printed.

- [ ] **Step 3: Run package and fresh-clone gates on the staged package**

Stage the intended files, preserving `.DS_Store`, then run:

```bash
git diff --cached --check
bash .maintain/scripts/check-package.sh
bash .maintain/scripts/smoke-fresh-clone.sh
```

Expected: package gate prints `maintainer package checks passed`; fresh clone passes strict validation and runtime tests.

- [ ] **Step 4: Run the real Hermes command-discovery probe**

With the existing managed symlink pointing at this checkout, run:

```bash
cd ~/.hermes/hermes-agent
venv/bin/python -c 'from agent.skill_commands import scan_skill_commands; c=scan_skill_commands(); print({k:v["name"] for k,v in c.items() if "hercules" in k})'
```

Expected exactly:

```python
{'/hercules': 'hercules'}
```

If a TUI session was already open, run `/reload-skills` there or restart it before the manual UI check.

- [ ] **Step 5: Request independent review**

The reviewer must verify:

- one `SKILL.md` and one Hermes slash command;
- four internal workflows remain linked and behaviorally covered;
- capability cache/security/privacy behavior has no regression;
- initializer symlink path and non-invasive update behavior are unchanged;
- README and `init.sh` advertise `/hercules`, not `/skill hercules`;
- full, strict, package, fresh-clone, and real Hermes probe evidence.

Write the result to `.maintain/docs/ai-collaboration/codex-reviews/2026-07-11-single-public-skill-entry.md` with stable `TASK016-CR-NNN` identifiers for any finding.

- [ ] **Step 6: Fix findings with one TDD cycle and re-review**

For each accepted finding: add a focused failing test, run it to observe RED, implement the minimal fix, run GREEN, then request a narrow recheck. Do not mark TASK-016 complete while any finding is open.

- [ ] **Step 7: Close TASK-016 and commit acceptance**

After independent PASS / Ready Yes, set:

```yaml
score: 1.0
codex_result: PASS
ready: true
next_owner: none
```

Mark TASK-016 `已完成`, set current/next owners to `无`, and commit:

```bash
git add .maintain/docs/ai-collaboration/TASKS.md .maintain/docs/ai-collaboration/codex-reviews/2026-07-11-single-public-skill-entry.md
git commit -m "docs: close true single-entry acceptance"
```

Do not push until the user explicitly requests it.
