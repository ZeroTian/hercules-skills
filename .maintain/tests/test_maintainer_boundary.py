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
EXPECTED_RUNTIME_SKILLS = {
    "hercules",
    "hercules-capability-discovery",
    "hercules-collaborative-workflow",
    "hercules-review-workflow",
    "hercules-project-init",
}


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_skill_pack_boundary", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MaintainerBoundaryContractTest(unittest.TestCase):
    def test_validator_targets_maintainer_docs(self) -> None:
        validator = load_validator_module()
        self.assertEqual(
            getattr(validator, "DOCS_COLLAB", None),
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration",
        )

    def test_validator_scope_is_exactly_five_runtime_skills(self) -> None:
        validator = load_validator_module()
        self.assertEqual(
            getattr(validator, "EXPECTED_RUNTIME_SKILLS", set()),
            EXPECTED_RUNTIME_SKILLS,
        )

    def test_validator_rejects_runtime_scope_outside_exact_five(self) -> None:
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

    def test_current_navigation_matches_exact_five_runtime_skills(self) -> None:
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

    def test_current_architecture_names_all_five_runtime_skill_paths(self) -> None:
        architecture = (
            REPO_ROOT / ".maintain" / "docs" / "ai-collaboration" / "ARCHITECTURE.md"
        ).read_text(encoding="utf-8")
        self.assertIn("exactly five runtime Skills", architecture)
        for skill in EXPECTED_RUNTIME_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(f"skills/{skill}/SKILL.md", architecture)

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
        self.assertIn("sensitive staged filename detected", result.stderr)

    def test_gate_rejects_secret_like_staged_content(self) -> None:
        self.assertTrue(self.gate_path.exists())
        repo = self.make_gate_repo()
        secret_like_fixture = "api" + "_key = placeholder\n"
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
        self.assertIn("api_key", result.stderr)

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
                self.assertIn("token", result.stderr)

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
