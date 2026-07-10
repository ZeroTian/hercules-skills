#!/usr/bin/env python3
import os
import shlex
import shutil
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
        self.real_git = shutil.which("git")
        self.assertIsNotNone(self.real_git)
        self.git_log = self.root / "git-commands.log"
        (self.bin / "git").write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$*\" >> \"$INIT_GIT_LOG\"\n"
            f"exec {shlex.quote(self.real_git)} \"$@\"\n"
        )
        (self.bin / "git").chmod(0o755)
        (self.bin / "hermes").write_text("#!/bin/sh\necho hermes-test\n")
        (self.bin / "hermes").chmod(0o755)

        (self.source / "skills" / "hercules").mkdir(parents=True)
        (self.source / "skills" / "hercules" / "SKILL.md").write_text("# test\n")
        self.git("init", "-b", "main", self.source)
        self.git("-C", self.source, "config", "user.email", "test@example.com")
        self.git("-C", self.source, "config", "user.name", "Test")
        self.commit_all(self.source, "fixture")

    def git(self, *args):
        return subprocess.run(
            [self.real_git, *(str(arg) for arg in args)],
            text=True, capture_output=True, check=True,
        )

    def commit_all(self, repo, message):
        self.git("-C", repo, "add", ".")
        self.git("-C", repo, "commit", "-m", message)

    def clone_source(self):
        self.git("clone", "--branch", "main", self.source, self.hercules_home)

    def advance_source(self):
        skill = self.source / "skills" / "hercules" / "SKILL.md"
        skill.write_text("# updated\n")
        self.commit_all(self.source, "update fixture")

    def repo_state(self, repo):
        return {
            "head": self.git("-C", repo, "rev-parse", "HEAD").stdout,
            "refs": self.git(
                "-C", repo, "for-each-ref",
                "--format=%(refname):%(objectname)",
            ).stdout,
            "status": self.git(
                "-C", repo, "status", "--porcelain=v1", "--untracked-files=all",
            ).stdout,
            "fetch_head": (
                (repo / ".git" / "FETCH_HEAD").read_bytes()
                if (repo / ".git" / "FETCH_HEAD").exists()
                else None
            ),
        }

    def filesystem_snapshot(self):
        snapshot = []
        for path in sorted(self.root.rglob("*")):
            relative = str(path.relative_to(self.root))
            if path.is_symlink():
                snapshot.append((relative, "symlink", os.readlink(path)))
            elif path.is_file():
                snapshot.append((relative, "file", path.read_bytes()))
            else:
                snapshot.append((relative, "directory", None))
        return snapshot

    def assert_no_git_actions(self, *actions):
        commands = self.git_log.read_text().splitlines() if self.git_log.exists() else []
        for action in actions:
            self.assertFalse(
                any(action in command.split() for command in commands),
                f"unexpected git {action}: {commands}",
            )

    def env(self):
        env = os.environ.copy()
        env.update({
            "PATH": f"{self.bin}:/usr/bin:/bin",
            "HERCULES_HOME": str(self.hercules_home),
            "HERMES_HOME": str(self.hermes_home),
            "HERCULES_REPO_URL": str(self.source),
            "HERCULES_BRANCH": "main",
            "INIT_GIT_LOG": str(self.git_log),
        })
        return env

    def run_init(self, env=None):
        return subprocess.run(
            ["/bin/bash", str(INIT)], cwd=REPO_ROOT, env=env or self.env(),
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
        before = self.filesystem_snapshot()
        result = self.run_init(env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Hermes is required but was not found", result.stderr)
        self.assertIn(
            "https://hermes-agent.nousresearch.com/docs/getting-started/quickstart",
            result.stderr,
        )
        self.assertIn("Hercules 未安装或修改任何内容", result.stderr)
        self.assertFalse(self.hercules_home.exists())
        self.assertFalse(self.hermes_home.exists())
        self.assertEqual(self.filesystem_snapshot(), before)

    def test_missing_git_stops_without_mutation(self):
        hermes_only_bin = self.root / "hermes-only-bin"
        hermes_only_bin.mkdir()
        (hermes_only_bin / "hermes").write_text(
            "#!/bin/sh\necho hermes-test\n", encoding="utf-8"
        )
        (hermes_only_bin / "hermes").chmod(0o755)
        env = self.env()
        env["PATH"] = str(hermes_only_bin)
        before = self.filesystem_snapshot()

        result = self.run_init(env)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Git is required but was not found", result.stderr)
        self.assertIn("https://git-scm.com/downloads", result.stderr)
        self.assertIn("Hercules 未安装或修改任何内容", result.stderr)
        self.assertFalse(self.hercules_home.exists())
        self.assertFalse(self.hermes_home.exists())
        self.assertEqual(self.filesystem_snapshot(), before)

    def test_existing_real_runtime_directory_is_preserved(self):
        runtime = self.hermes_home / "skills" / "hercules"
        runtime.mkdir(parents=True)
        marker = runtime / "keep.txt"
        marker.write_text("keep")
        result = self.run_init()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(marker.read_text(), "keep")

    def test_unrelated_git_checkout_is_preserved_without_fetch_or_merge(self):
        unrelated = self.root / "unrelated"
        (unrelated / "skills").mkdir(parents=True)
        (unrelated / "skills" / "foreign.txt").write_text("foreign-v1")
        self.git("init", "-b", "main", unrelated)
        self.git("-C", unrelated, "config", "user.email", "test@example.com")
        self.git("-C", unrelated, "config", "user.name", "Test")
        self.commit_all(unrelated, "unrelated fixture")
        self.git("clone", "--branch", "main", unrelated, self.hercules_home)

        (unrelated / "skills" / "foreign.txt").write_text("foreign-v2")
        self.commit_all(unrelated, "unrelated update")

        runtime = self.hermes_home / "skills" / "hercules"
        runtime.parent.mkdir(parents=True)
        runtime.symlink_to((self.hercules_home / "skills").resolve(), target_is_directory=True)
        before_state = self.repo_state(self.hercules_home)
        before_file = (self.hercules_home / "skills" / "foreign.txt").read_text()
        before_link = os.readlink(runtime)

        result = self.run_init()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.repo_state(self.hercules_home), before_state)
        self.assertEqual(
            (self.hercules_home / "skills" / "foreign.txt").read_text(),
            before_file,
        )
        self.assertEqual(os.readlink(runtime), before_link)
        self.assert_no_git_actions("fetch", "merge")

    def test_hercules_checkout_on_wrong_branch_is_preserved_without_update(self):
        self.clone_source()
        self.git("-C", self.hercules_home, "checkout", "-b", "other")
        self.advance_source()
        runtime = self.hermes_home / "skills" / "hercules"
        runtime.parent.mkdir(parents=True)
        runtime.symlink_to(
            (self.hercules_home / "skills").resolve(), target_is_directory=True,
        )
        before_state = self.repo_state(self.hercules_home)
        before_file = (self.hercules_home / "skills" / "hercules" / "SKILL.md").read_text()
        before_link = os.readlink(runtime)

        result = self.run_init()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.repo_state(self.hercules_home), before_state)
        self.assertEqual(
            (self.hercules_home / "skills" / "hercules" / "SKILL.md").read_text(),
            before_file,
        )
        self.assertEqual(os.readlink(runtime), before_link)
        self.assert_no_git_actions("fetch", "merge")

    def test_runtime_parent_file_stops_before_fresh_clone(self):
        self.hermes_home.mkdir()
        conflict = self.hermes_home / "skills"
        conflict.write_text("keep")

        result = self.run_init()

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.hercules_home.exists())
        self.assertEqual(conflict.read_text(), "keep")
        self.assertFalse((conflict / "hercules").is_symlink())
        self.assert_no_git_actions("clone", "fetch", "merge")

    def test_runtime_parent_file_stops_before_existing_checkout_update(self):
        self.clone_source()
        self.advance_source()
        self.hermes_home.mkdir()
        conflict = self.hermes_home / "skills"
        conflict.write_text("keep")
        before_state = self.repo_state(self.hercules_home)
        before_file = (self.hercules_home / "skills" / "hercules" / "SKILL.md").read_text()

        result = self.run_init()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.repo_state(self.hercules_home), before_state)
        self.assertEqual(
            (self.hercules_home / "skills" / "hercules" / "SKILL.md").read_text(),
            before_file,
        )
        self.assertEqual(conflict.read_text(), "keep")
        self.assertFalse((conflict / "hercules").is_symlink())
        self.assert_no_git_actions("fetch", "merge")


if __name__ == "__main__":
    unittest.main()
