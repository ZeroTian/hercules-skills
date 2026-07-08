#!/usr/bin/env python3
import json
import importlib.util
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-skill-pack.py"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_skill_pack", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSkillPackCliTest(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/validate-skill-pack.py", *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_json_output_is_machine_readable(self) -> None:
        result = self.run_validator("--json")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("errors", payload)
        self.assertIn("warnings", payload)
        self.assertIn("signals", payload)
        self.assertEqual(payload["summary"]["errors"], 0)
        self.assertEqual(payload["summary"]["warnings"], 0)

    def test_strict_mode_succeeds_when_no_warnings_or_errors(self) -> None:
        result = self.run_validator("--strict", "--json")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["exit_code"], 0)
        self.assertTrue(payload["summary"]["strict"])


class FreshCloneSmokeScriptTest(unittest.TestCase):
    def test_smoke_script_exists_and_is_executable(self) -> None:
        script = REPO_ROOT / "scripts" / "smoke-fresh-clone.sh"
        self.assertTrue(script.exists())
        self.assertTrue(script.stat().st_mode & 0o111)

    def test_smoke_script_is_staged_only_by_default(self) -> None:
        script = (REPO_ROOT / "scripts" / "smoke-fresh-clone.sh").read_text()
        self.assertIn("HERCULES_SMOKE_INCLUDE_UNSTAGED", script)
        self.assertIn('if [ "${HERCULES_SMOKE_INCLUDE_UNSTAGED:-0}" = "1" ]; then', script)


class LinkedFileReferenceClassifierTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = load_validator_module()

    def test_inline_skill_local_reference_is_validated(self) -> None:
        self.assertTrue(
            self.validator.should_validate_linked_candidate(
                "See `references/example.md` for the detailed workflow.",
                "references/example.md",
            )
        )

    def test_downstream_test_wrapper_example_is_not_validated(self) -> None:
        self.assertFalse(
            self.validator.should_validate_linked_candidate(
                "Hermes ran the canonical tests itself, using `scripts/run_tests.sh` for Hermes Agent or the repo's documented wrapper for other repos.",
                "scripts/run_tests.sh",
            )
        )


if __name__ == "__main__":
    unittest.main()
