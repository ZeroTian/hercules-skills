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
