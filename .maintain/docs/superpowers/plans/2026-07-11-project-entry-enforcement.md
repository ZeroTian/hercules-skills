# Hercules Project Entry Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Hercules project initialization install a minimal, explicit entry contract across supported project instruction files so agents cannot bypass capability discovery or misidentify Hermes built-in subagents as Claude Code or Codex CLI.

**Architecture:** Keep `init.sh` as transport-only installation. Extend the internal `project-init.md` workflow with one canonical shared contract for `AGENTS.md` and minimal adapters for `CLAUDE.md` and `HERMES.md`; enforce the behavior through runtime-contract tests rather than adding another executable or runtime Skill.

**Tech Stack:** Markdown runtime Skill references, Python 3 `unittest`, Bash initializer.

## Global Constraints

- The runtime surface remains exactly one discoverable Skill: `skills/hercules/SKILL.md`.
- `init.sh` must not edit target-project instruction files.
- Preserve existing project instructions and unrelated user changes.
- Preview exact changes and obtain explicit user approval before writing project files.
- Shared rules live canonically in `AGENTS.md`; `CLAUDE.md` and `HERMES.md` receive only tool-specific adapters.
- Never install, configure, authenticate, or proactively probe external facilities.
- Never represent a Hermes built-in subagent as Claude Code or Codex CLI.

---

## File Map

- Modify `skills/hercules/references/project-init.md`: define the canonical entry contract, adapters, preview/apply behavior, conflict handling, idempotency, and verification report.
- Modify `.maintain/tests/test_runtime_skill_contract.py`: lock the content and separation guarantees of the project-init contract.
- Modify `.maintain/tests/test_init.py`: prove the public initializer remains transport-only and cannot write project instruction files.

### Task 1: Lock the project-entry contract with failing tests

**Files:**
- Modify: `.maintain/tests/test_runtime_skill_contract.py`

**Interfaces:**
- Consumes: `RuntimeSkillContractTest.reference_text(name: str) -> str`.
- Produces: regression tests defining canonical `AGENTS.md` ownership, minimal `CLAUDE.md`/`HERMES.md` adapters, identity accuracy, preview approval, conflict handling, and idempotency.

- [ ] **Step 1: Add failing contract tests after `test_project_init_is_project_scoped`**

```python
    def test_project_init_defines_canonical_entry_contract(self):
        text = self.reference_text("project-init.md")
        for phrase in (
            "canonical shared contract",
            "AGENTS.md",
            "route non-trivial project work through Hercules",
            "capability discovery",
            "independently verify actual outputs",
        ):
            self.assertIn(phrase, text)

    def test_project_init_uses_minimal_tool_adapters(self):
        text = self.reference_text("project-init.md")
        for phrase in (
            "CLAUDE.md adapter",
            "HERMES.md adapter",
            "Do not duplicate the canonical shared contract",
            "delegate_task",
            "must not be represented as Claude Code or Codex CLI",
        ):
            self.assertIn(phrase, text)

    def test_project_init_requires_approved_idempotent_merge(self):
        text = self.reference_text("project-init.md")
        for phrase in (
            "Preview the exact additions and changed files",
            "Obtain explicit user approval",
            "Repeated initialization must be idempotent",
            "stop and show the conflict",
        ):
            self.assertIn(phrase, text)
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  .maintain.tests.test_runtime_skill_contract.RuntimeSkillContractTest.test_project_init_defines_canonical_entry_contract \
  .maintain.tests.test_runtime_skill_contract.RuntimeSkillContractTest.test_project_init_uses_minimal_tool_adapters \
  .maintain.tests.test_runtime_skill_contract.RuntimeSkillContractTest.test_project_init_requires_approved_idempotent_merge -v
```

Expected: three failures reporting missing required phrases in `project-init.md`.

- [ ] **Step 3: Commit the failing contract tests if explicitly authorized**

```bash
git add .maintain/tests/test_runtime_skill_contract.py
git commit -m "test: define Hercules project entry contract"
```

If commit authorization is absent, leave the tested diff unstaged and report that no commit was created.

### Task 2: Implement canonical shared rules and tool adapters

**Files:**
- Modify: `skills/hercules/references/project-init.md`

**Interfaces:**
- Consumes: repository root, governing project instruction files, user-requested project rules, and user approval.
- Produces: an approved minimal merge into supported instruction files plus a verification report; no script or callable API is added.

- [ ] **Step 1: Replace the Procedure section with the explicit entry-enforcement flow**

Use this complete procedure text:

```markdown
## Procedure

1. Confirm the repository root, requested rules, approved files, and existing user changes.
2. Inspect every instruction file governing the target path, including existing `AGENTS.md`, `CLAUDE.md`, `HERMES.md`, and nested instructions.
3. Detect existing Hercules entry rules, equivalent wording, and conflicts.
4. Map each rule to the narrowest project-scoped file using [instruction boundaries](instruction-boundaries.md).
5. Preview the exact additions and changed files. Identify preserved content, conflicts, and unsupported instruction surfaces.
6. Obtain explicit user approval before changing any instruction file.
7. Apply the smallest approved merge. Repeated initialization must be idempotent: retain equivalent rules instead of appending duplicates.
8. Verify references, canonical ownership, adapter scope, preservation of existing content, and the final diff.
9. Report changed files, preserved conflicts, uncovered tools, and verification evidence.
```

- [ ] **Step 2: Add the canonical shared contract after Procedure**

```markdown
## Canonical Shared Contract

Keep the canonical shared contract in the repository's applicable general instruction file, normally `AGENTS.md`. Merge rules requiring agents to:

- route non-trivial project work through Hercules before selecting an implementation or review facility;
- read governing project instructions and perform relevant capability discovery before facility selection;
- invoke only a confirmed facility with sufficient authority;
- identify Hermes built-in subagents accurately: they must not be represented as Claude Code or Codex CLI;
- classify invocation failures and follow Hercules fallback rules without silently changing identity or authority;
- independently verify actual outputs before reporting completion.

Do not copy the complete Hercules Skill or internal workflow references into a project instruction file.
```

- [ ] **Step 3: Add minimal adapters and conflict behavior**

```markdown
## Tool-specific Adapters

### `CLAUDE.md` adapter

Retain Claude-specific implementation boundaries and add only a short instruction to follow the canonical shared contract in `AGENTS.md`. Do not duplicate the canonical shared contract.

### `HERMES.md` adapter

State that Hermes is the controller, must load the canonical shared contract and Hercules before routing project work, and must not use `delegate_task` or another built-in subagent as a substitute for a requested or selected Claude Code or Codex CLI facility. Do not duplicate the canonical shared contract.

Update only instruction filenames supported by the applicable tool. If a supported file is absent, create it only when its exact content appeared in the approved preview. If an existing rule conflicts with this contract, stop and show the conflict instead of silently overriding either rule.
```

- [ ] **Step 4: Replace Change Contract with enforcement evidence requirements**

```markdown
## Change Contract

The final report must list changed files, summarize the project-scoped rules added, identify preserved conflicts or blockers, name unsupported or uncovered instruction surfaces, and provide link/reference plus final-diff verification evidence. Confirm that shared rules have one canonical owner and tool-specific files contain only adapters. If no file change is necessary, say so and show the equivalent rules used as evidence.
```

- [ ] **Step 5: Run focused runtime-contract tests**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest .maintain.tests.test_runtime_skill_contract.RuntimeSkillContractTest -v
```

Expected: all `RuntimeSkillContractTest` tests pass, including the three new project-init tests.

- [ ] **Step 6: Commit implementation if explicitly authorized**

```bash
git add skills/hercules/references/project-init.md
git commit -m "feat: enforce Hercules project entry routing"
```

If commit authorization is absent, do not stage or commit.

### Task 3: Prove `init.sh` remains non-invasive and run full verification

**Files:**
- Modify: `.maintain/tests/test_init.py`

**Interfaces:**
- Consumes: `InitScriptTest.run_init()` and its isolated temporary fixture.
- Produces: a regression test proving the installer does not create or modify project instruction files.

- [ ] **Step 1: Add the initializer boundary test after `test_clone_and_symlink_only`**

```python
    def test_init_does_not_write_project_instruction_files(self):
        project = self.root / "project"
        project.mkdir()
        instructions = {
            "AGENTS.md": "agents-keep\n",
            "CLAUDE.md": "claude-keep\n",
            "HERMES.md": "hermes-keep\n",
        }
        for name, content in instructions.items():
            (project / name).write_text(content, encoding="utf-8")

        result = subprocess.run(
            ["/bin/bash", str(INIT)],
            cwd=project,
            env=self.env(),
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name, content in instructions.items():
            self.assertEqual((project / name).read_text(encoding="utf-8"), content)
```

- [ ] **Step 2: Run the focused initializer boundary test**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  .maintain.tests.test_init.InitScriptTest.test_init_does_not_write_project_instruction_files -v
```

Expected: PASS.

- [ ] **Step 3: Run the complete test suite**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .maintain/tests -p 'test_*.py' -v
```

Expected: all tests pass.

- [ ] **Step 4: Run repository validation**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .maintain/scripts/validate-skill-pack.py --strict
```

Expected: exit code `0`, with `0 errors` and `0 warnings`.

- [ ] **Step 5: Inspect final scope and whitespace**

```bash
git diff --check
git status --short
git diff -- .maintain/tests/test_runtime_skill_contract.py .maintain/tests/test_init.py skills/hercules/references/project-init.md
```

Expected: `git diff --check` has no output; only the approved plan files are changed, plus any pre-existing unrelated files such as `.DS_Store` remain untouched.

- [ ] **Step 6: Commit final regression test if explicitly authorized**

```bash
git add .maintain/tests/test_init.py
git commit -m "test: preserve initializer instruction boundary"
```

If commit authorization is absent, leave all changes uncommitted and report the verified working tree state.
