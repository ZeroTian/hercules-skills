#!/usr/bin/env python3
import importlib.util
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / ".maintain" / "scripts" / "validate-skill-pack.py"
EXPECTED_RUNTIME_SKILLS = {"hercules"}


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_skill_pack_boundary", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MaintainerBoundaryContractTest(unittest.TestCase):
    def navigation_rows(self, roles: dict[str, str]) -> str:
        lines = [
            "# Skill Navigation",
            "",
            "| Skill | Role | Maturity | Primary use | Notes |",
            "|---|---|---|---|---|",
        ]
        lines.extend(
            f"| `{skill}` | {role} | core | fixture | fixture |"
            for skill, role in sorted(roles.items())
        )
        return "\n".join(lines) + "\n"

    def navigation_report(self, roles: dict[str, str]):
        validator = load_validator_module()
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs / "SKILL_NAVIGATION.md").write_text(
                self.navigation_rows(roles), encoding="utf-8"
            )
            report = validator.Report()
            with mock.patch.object(validator, "DOCS_COLLAB", docs):
                validator.check_skill_navigation(report)
        return report

    def test_validator_targets_maintainer_docs(self) -> None:
        validator = load_validator_module()
        self.assertEqual(
            getattr(validator, "DOCS_COLLAB", None),
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration",
        )

    def test_validator_scope_is_exactly_one_public_skill(self) -> None:
        validator = load_validator_module()
        self.assertEqual(
            getattr(validator, "EXPECTED_RUNTIME_SKILLS", set()),
            EXPECTED_RUNTIME_SKILLS,
        )

    def test_validator_rejects_extra_runtime_skill(self) -> None:
        validator = load_validator_module()
        check = getattr(validator, "check_runtime_skill_scope", None)
        self.assertIsNotNone(check)
        report = validator.Report()
        unexpected = EXPECTED_RUNTIME_SKILLS | {"unexpected-runtime-skill"}
        with (
            mock.patch.object(validator, "git_tracked_skills", return_value=unexpected),
            mock.patch.object(validator, "visible_skill_dirs", return_value=unexpected),
        ):
            check(report)
        self.assertTrue(
            any("exact runtime skill scope drift" in error for error in report.errors),
            report.errors,
        )

    def test_validator_rejects_nested_runtime_skill_file(self) -> None:
        validator = load_validator_module()
        expected = {"skills/hercules/SKILL.md"}
        unexpected = expected | {
            "skills/hercules/references/rogue/SKILL.md"
        }
        report = validator.Report()
        with (
            mock.patch.object(
                validator, "git_tracked_skill_files", return_value=unexpected
            ),
            mock.patch.object(
                validator, "visible_skill_files", return_value=unexpected
            ),
        ):
            validator.check_runtime_skill_scope(report)
        self.assertTrue(
            any("exact runtime skill file scope drift" in error for error in report.errors),
            report.errors,
        )

    def test_validator_rejects_missing_or_non_entry_navigation(self) -> None:
        self.assertTrue(self.navigation_report({}).errors)
        report = self.navigation_report({"hercules": "atom"})
        self.assertTrue(
            any("entry/composite" in error for error in report.errors),
            report.errors,
        )

    def test_validator_rejects_extra_navigation_row(self) -> None:
        report = self.navigation_report({
            "hercules": "entry/composite",
            "unexpected-runtime-skill": "atom",
        })
        self.assertTrue(
            any("navigation runtime skill scope drift" in error for error in report.errors),
            report.errors,
        )

    def test_validator_rejects_broken_internal_workflow_link(self) -> None:
        validator = load_validator_module()
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "skills" / "hercules"
            references = skill / "references"
            references.mkdir(parents=True)
            skill_file = skill / "SKILL.md"
            skill_file.write_text(
                "[workflow](references/workflow.md)\n", encoding="utf-8"
            )
            (references / "workflow.md").write_text(
                "[missing](missing.md)\n", encoding="utf-8"
            )
            report = validator.Report()
            validator.check_skill_markdown_links(report, [skill_file])
        self.assertTrue(
            any("linked file not found" in warning for warning in report.warnings),
            report.warnings,
        )

    def test_repository_tooling_is_behind_maintainer_boundary(self) -> None:
        maintained_paths = (
            ".maintain/scripts/validate-skill-pack.py",
            ".maintain/scripts/smoke-fresh-clone.sh",
            ".maintain/tests/test_validate_skill_pack_cli.py",
            ".maintain/docs/ai-collaboration",
            ".maintain/docs/WHY_HERCULES.md",
        )
        removed_paths = (
            "scripts/validate-skill-pack.py",
            "scripts/smoke-fresh-clone.sh",
            "scripts/hercules",
            "scripts/install-hercules.sh",
            "tests/test_validate_skill_pack_cli.py",
            "tests/test_setup_doctor_ux.py",
            "docs/ai-collaboration",
            "docs/WHY_HERCULES.md",
        )
        for rel in maintained_paths:
            with self.subTest(path=rel):
                self.assertTrue((REPO_ROOT / rel).exists())
        for rel in removed_paths:
            with self.subTest(path=rel):
                self.assertFalse((REPO_ROOT / rel).exists())


class MaintainerDocumentContractTest(unittest.TestCase):
    def current_document_text(self) -> str:
        active_docs = (
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration" / "README.md",
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration" / "ARCHITECTURE.md",
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration" / "SKILL_NAVIGATION.md",
        )
        texts = [path.read_text(encoding="utf-8") for path in active_docs]

        candidate = (
            REPO_ROOT
            / ".maintain"
            / "docs"
            / "ai-collaboration"
            / "candidate-skills"
            / "README.md"
        ).read_text(encoding="utf-8")
        if "## Historical disposition" in candidate and "## How to promote" in candidate:
            current_prefix = candidate.split("## Historical disposition", 1)[0]
            current_suffix = candidate.split("## How to promote", 1)[1]
            candidate = current_prefix + "\n## How to promote" + current_suffix
        texts.append(candidate)

        tasks = (
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration" / "TASKS.md"
        ).read_text(encoding="utf-8")
        texts.append(tasks.split("## Trajectory record policy", 1)[-1])

        positioning = (
            REPO_ROOT / ".maintain" / "docs" / "WHY_HERCULES.md"
        ).read_text(encoding="utf-8")
        texts.append(positioning.split("## Historical snapshot", 1)[0])
        return "\n".join(texts)

    def test_active_maintainer_documents_do_not_advertise_retired_paths(self) -> None:
        text = self.current_document_text()
        stale_patterns = (
            r"(?<!\.maintain/)docs/ai-collaboration",
            r"(?<!\.maintain/)docs/WHY_HERCULES\.md",
            r"(?<!\.maintain/)scripts/(?:validate-skill-pack\.py|smoke-fresh-clone\.sh|hercules|install-hercules\.sh)",
            r"(?<!\.maintain/)tests/(?:test_validate_skill_pack_cli|test_setup_doctor_ux)\.py",
            r"Runtime core skills \(25\)",
            r"25 tracked skills",
        )
        for pattern in stale_patterns:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, text), pattern)

    def test_current_navigation_matches_exactly_one_runtime_skill(self) -> None:
        validator = load_validator_module()
        navigation = (
            REPO_ROOT
            / ".maintain"
            / "docs"
            / "ai-collaboration"
            / "SKILL_NAVIGATION.md"
        )
        self.assertEqual(
            set(validator.parse_skill_navigation(navigation)),
            EXPECTED_RUNTIME_SKILLS,
        )

    def test_current_architecture_names_public_skill_and_internal_references(self) -> None:
        architecture = (
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration" / "ARCHITECTURE.md"
        ).read_text(encoding="utf-8")
        self.assertIn("exactly one runtime Skill", architecture)
        self.assertIn("skills/hercules/SKILL.md", architecture)
        for reference in (
            "capability-discovery.md",
            "collaborative-workflow.md",
            "review-workflow.md",
            "project-init.md",
        ):
            with self.subTest(reference=reference):
                self.assertIn(reference, architecture)

    def test_governance_instructions_enforce_exactly_one_runtime_skill(self) -> None:
        paths = (
            REPO_ROOT / "AGENTS.md",
            REPO_ROOT / "CLAUDE.md",
            REPO_ROOT / "HERMES.md",
            REPO_ROOT
            / ".maintain"
            / "docs"
            / "ai-collaboration"
            / "candidate-skills"
            / "README.md",
        )
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("exactly one runtime Skill", text)
                self.assertNotIn("exactly five", text)

    def test_advertised_current_paths_and_commands_resolve(self) -> None:
        text = self.current_document_text()
        advertised_paths = {
            match.rstrip(".,;:")
            for match in re.findall(r"`((?:\.maintain|skills)/[^`\n]+)`", text)
            if not re.search(r"[<>{}*]", match)
        }
        self.assertTrue(advertised_paths)
        for rel in sorted(advertised_paths):
            with self.subTest(path=rel):
                self.assertTrue((REPO_ROOT / rel).exists(), rel)

        commands = (
            "python3 .maintain/scripts/validate-skill-pack.py --strict",
            ".maintain/scripts/check-package.sh",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertIn(command, text)
            executable = command.split()[1 if command.startswith("python3 ") else 0]
            self.assertTrue((REPO_ROOT / executable).exists(), executable)


class MaintainerPackageGateTest(unittest.TestCase):
    @property
    def gate_path(self) -> Path:
        return REPO_ROOT / ".maintain" / "scripts" / "check-package.sh"

    def make_gate_repo(self) -> Path:
        repo = Path(tempfile.mkdtemp(prefix="hercules-package-gate-test-"))
        scripts = repo / ".maintain" / "scripts"
        scripts.mkdir(parents=True)
        shutil.copy2(self.gate_path, scripts / "check-package.sh")
        (scripts / "validate-skill-pack.py").write_text(
            "#!/usr/bin/env python3\n",
            encoding="utf-8",
        )
        (scripts / "smoke-fresh-clone.sh").write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\n",
            encoding="utf-8",
        )
        (repo / "init.sh").write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        self.addCleanup(shutil.rmtree, repo)
        return repo

    def test_gate_is_executable_and_avoids_fixed_sensitive_temp_logs(self) -> None:
        self.assertTrue(self.gate_path.exists())
        self.assertTrue(self.gate_path.stat().st_mode & 0o111)
        script = self.gate_path.read_text(encoding="utf-8")
        self.assertNotIn("/tmp/", script)
        self.assertNotIn("hercules_staged_secret_hits", script)

    def test_gate_does_not_flag_its_own_secret_scan_patterns(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_gate_rejects_sensitive_staged_filename(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        (repo / ".env").write_text("placeholder\n", encoding="utf-8")
        subprocess.run(["git", "add", ".env"], cwd=repo, check=True)
        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            result.stderr,
            "redacted category=sensitive-filename path=.env line=- count=1\n",
        )

    def test_gate_rejects_secret_like_staged_content(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        sentinel_value = "DISTINCTIVE-DO-NOT-ECHO-7f3d92"
        secret_like_fixture = "api" + f"_key = {sentinel_value}\n"
        (repo / "notes.md").write_text(secret_like_fixture, encoding="utf-8")
        subprocess.run(["git", "add", "notes.md"], cwd=repo, check=True)
        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertEqual(
            result.stderr,
            "redacted category=api-key path=notes.md line=1 count=1\n",
        )
        self.assertNotIn(sentinel_value, output)
        self.assertNotIn(secret_like_fixture.strip(), output)

    def test_gate_redacts_staged_secret_like_trailing_whitespace(self) -> None:
        repo = self.make_gate_repo()
        sentinel = "STAGED-WHITESPACE-SENTINEL-a91f4c"
        fixture = "api" + "_key = " + sentinel + " \n"
        (repo / "staged-notes.md").write_text(fixture, encoding="utf-8")
        subprocess.run(["git", "add", "staged-notes.md"], cwd=repo, check=True)

        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            result.stderr,
            "redacted category=trailing-whitespace path=staged-notes.md line=1 count=1\n",
        )
        self.assertNotIn(sentinel, result.stdout + result.stderr)
        self.assertNotIn(fixture.strip(), result.stdout + result.stderr)

    def test_gate_redacts_unstaged_secret_like_trailing_whitespace(self) -> None:
        repo = self.make_gate_repo()
        notes = repo / "unstaged-notes.md"
        notes.write_text("safe baseline\n", encoding="utf-8")
        subprocess.run(["git", "add", "unstaged-notes.md"], cwd=repo, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Hercules Test",
                "-c",
                "user.email=hercules-test@example.invalid",
                "commit",
                "-qm",
                "baseline",
            ],
            cwd=repo,
            check=True,
        )
        sentinel = "UNSTAGED-WHITESPACE-SENTINEL-6ce208"
        fixture = "to" + "ken = " + sentinel + " \n"
        notes.write_text(fixture, encoding="utf-8")

        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            result.stderr,
            "redacted category=trailing-whitespace path=unstaged-notes.md line=1 count=1\n",
        )
        self.assertNotIn(sentinel, result.stdout + result.stderr)
        self.assertNotIn(fixture.strip(), result.stdout + result.stderr)

    def test_gate_rejects_non_secret_trailing_whitespace_with_redacted_output(self) -> None:
        repo = self.make_gate_repo()
        (repo / "formatting.md").write_text("ordinary text \n", encoding="utf-8")
        subprocess.run(["git", "add", "formatting.md"], cwd=repo, check=True)

        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            result.stderr,
            "redacted category=trailing-whitespace path=formatting.md line=1 count=1\n",
        )
        self.assertNotIn("ordinary text", result.stdout + result.stderr)

    def test_gate_rejects_plus_prefixed_secret_like_staged_content(self) -> None:
        self.assertTrue(self.gate_path.exists())
        for prefix in ("+", "++"):
            with self.subTest(prefix=prefix):
                repo = self.make_gate_repo()
                secret_like_fixture = prefix + "to" + "ken = placeholder\n"
                (repo / "plus-prefixed.txt").write_text(
                    secret_like_fixture,
                    encoding="utf-8",
                )
                subprocess.run(
                    ["git", "add", "plus-prefixed.txt"],
                    cwd=repo,
                    check=True,
                )
                result = subprocess.run(
                    ["bash", ".maintain/scripts/check-package.sh"],
                    cwd=repo,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(
                    result.stderr,
                    "redacted category=token path=plus-prefixed.txt line=1 count=1\n",
                )

    def test_gate_reports_redacted_match_count_and_lines(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        sentinel = "COUNT-SENTINEL-58cc1a"
        (repo / "notes.md").write_text(
            "to" + "ken = " + sentinel + "\n" + "to" + "ken = second-value\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "notes.md"], cwd=repo, check=True)
        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            result.stderr,
            "redacted category=token path=notes.md line=1,2 count=2\n",
        )
        self.assertNotIn(sentinel, result.stdout + result.stderr)

    def test_gate_ignores_secret_like_unstaged_content(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        notes = repo / "notes.md"
        notes.write_text("safe staged content\n", encoding="utf-8")
        subprocess.run(["git", "add", "notes.md"], cwd=repo, check=True)
        notes.write_text("to" + "ken = unstaged-only\n", encoding="utf-8")
        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_gate_allows_removing_secret_like_content(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        legacy = repo / "legacy.txt"
        legacy.write_text("to" + "ken = placeholder\n", encoding="utf-8")
        subprocess.run(["git", "add", "legacy.txt"], cwd=repo, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Hercules Test",
                "-c",
                "user.email=hercules-test@example.invalid",
                "commit",
                "-qm",
                "baseline",
            ],
            cwd=repo,
            check=True,
        )
        legacy.unlink()
        subprocess.run(["git", "add", "-u"], cwd=repo, check=True)
        result = subprocess.run(
            ["bash", ".maintain/scripts/check-package.sh"],
            cwd=repo,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
