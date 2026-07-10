#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class SetupDoctorUxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.home = Path(self.temp_dir.name) / "home"
        self.fake_bin = Path(self.temp_dir.name) / "bin"
        self.trace = Path(self.temp_dir.name) / "tool-trace.log"
        self.home.mkdir()
        self.fake_bin.mkdir()
        (self.home / ".hermes").mkdir()
        (self.home / ".hermes" / "config.yaml").write_text("model: test\n")

        self.write_tool(
            "hermes",
            """
            case "$*" in
              "--version") echo "Hermes Agent test" ;;
              "skills list") printf '%s\n' subagent-driven-development writing-plans ;;
            esac
            """,
        )
        self.write_tool(
            "claude",
            """
            printf 'claude %s\n' "$*" >> "$HERCULES_TEST_TRACE"
            case "$*" in
              "--version") echo "Claude Code test" ;;
              "auth status --text") echo "AUTH_STATUS_CALLED"; exit 1 ;;
              "plugins list")
                printf '%s\n' \
                  "superpowers@claude-plugins-official" \
                  "oh-my-claudecode@omc" \
                  "codex@openai-codex" \
                  "playwright@claude-plugins-official" \
                  "context7@claude-plugins-official" \
                  "pyright-lsp@claude-plugins-official"
                ;;
              "mcp list") echo "NOISY_CLAUDE_MCP_LIST" ;;
            esac
            """,
        )
        self.write_tool(
            "codex",
            """
            printf 'codex %s\n' "$*" >> "$HERCULES_TEST_TRACE"
            case "$*" in
              "--version") echo "codex-cli test" ;;
              "login status") echo "LOGIN_STATUS_CALLED"; exit 1 ;;
              "mcp list") echo "NOISY_CODEX_MCP_LIST" ;;
              "features list") echo "NOISY_CODEX_FEATURE_LIST" ;;
            esac
            """,
        )

        self.env = os.environ.copy()
        self.env.update(
            {
                "HOME": str(self.home),
                "PATH": f"{self.fake_bin}:{self.env['PATH']}",
                "HERCULES_TEST_TRACE": str(self.trace),
            }
        )

    def write_tool(self, name: str, body: str) -> None:
        path = self.fake_bin / name
        path.write_text("#!/usr/bin/env bash\nset -eu\n" + textwrap.dedent(body))
        path.chmod(0o755)

    def run_command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            list(args),
            cwd=REPO_ROOT,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_installer_from_stdin(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", "-s", "--", *args],
            cwd=self.temp_dir.name,
            env=self.env,
            text=True,
            input=(REPO_ROOT / "scripts/install-hercules.sh").read_text(),
            capture_output=True,
            check=False,
        )

    def test_dry_run_is_a_concise_plan_without_auth_or_capability_inventory(self) -> None:
        result = self.run_command(
            "scripts/hercules",
            "setup",
            "--dry-run",
            "--repo-dir",
            str(REPO_ROOT),
        )
        output = result.stdout + result.stderr
        trace = self.trace.read_text() if self.trace.exists() else ""

        self.assertEqual(result.returncode, 0, output)
        self.assertIn("Hercules Setup Preview", output)
        self.assertIn("No changes were made", output)
        for forbidden in (
            "AUTH_STATUS_CALLED",
            "LOGIN_STATUS_CALLED",
            "NOISY_CLAUDE_MCP_LIST",
            "NOISY_CODEX_MCP_LIST",
            "NOISY_CODEX_FEATURE_LIST",
            "Capability summary",
            "Plugin deep capability inventory",
            "claude auth login --console",
            "codex login",
        ):
            self.assertNotIn(forbidden, output)
        for forbidden_call in (
            "claude auth status",
            "claude plugins list",
            "claude mcp list",
            "codex login status",
            "codex mcp list",
            "codex features list",
        ):
            self.assertNotIn(forbidden_call, trace)

    def test_dry_run_apply_command_preserves_selected_options(self) -> None:
        target = Path(self.temp_dir.name) / "custom checkout"
        result = self.run_command(
            "scripts/hercules",
            "setup",
            "--dry-run",
            "--copy",
            "--branch",
            "feature/ux",
            "--repo-dir",
            str(target),
            "--skip-os-packages",
            "--skip-hermes-install",
            "--skip-bootstrap",
        )
        output = result.stdout + result.stderr
        expected_doctor = str(target).replace(" ", "\\ ") + "/scripts/hercules doctor"

        self.assertEqual(result.returncode, 0, output)
        self.assertIn("scripts/hercules setup --minimal", output)
        self.assertIn("--copy", output)
        self.assertIn("--branch feature/ux", output)
        self.assertIn("--repo-dir", output)
        self.assertIn("custom\\ checkout", output)
        self.assertIn("--skip-os-packages", output)
        self.assertIn("--skip-hermes-install", output)
        self.assertIn("--skip-bootstrap", output)
        self.assertIn(expected_doctor, output)
        apply_section = output.split("Apply this plan:", 1)[1]
        self.assertNotIn("--dry-run", apply_section)

    def test_piped_dry_run_prints_a_reusable_curl_apply_command(self) -> None:
        target = Path(self.temp_dir.name) / "fresh-machine-repo"
        result = self.run_installer_from_stdin(
            "--dry-run",
            "--repo-dir",
            str(target),
            "--skip-os-packages",
            "--skip-hermes-install",
            "--skip-bootstrap",
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, output)
        self.assertIn(
            "curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh",
            output,
        )
        self.assertIn("| bash -s -- --minimal", output)
        self.assertIn("--repo-dir", output)
        self.assertNotIn("scripts/hercules setup --minimal", output)
        self.assertIn(f"{target}/scripts/hercules doctor", output)

    def test_doctor_does_not_probe_or_block_on_third_party_login_state(self) -> None:
        result = self.run_command("scripts/hercules", "doctor", "--json")
        self.assertTrue(result.stdout.strip(), result.stderr)
        payload = json.loads(result.stdout)
        check_names = {item["name"] for item in payload["checks"]}
        trace = self.trace.read_text() if self.trace.exists() else ""

        self.assertNotEqual(payload["status"], "blocked")
        self.assertNotIn("claude auth", check_names)
        self.assertNotIn("codex auth", check_names)
        self.assertNotIn("auth status", trace)
        self.assertNotIn("login status", trace)

    def test_docs_define_runtime_failure_diagnosis_without_login_instructions(self) -> None:
        workflow_text = (
            REPO_ROOT / "skills/hermes-collaborative-workflow/SKILL.md"
        ).read_text()
        hercules_workflow_text = (
            REPO_ROOT / "skills/hercules-collaborative-agent-workflow/SKILL.md"
        ).read_text()
        self.assertIn("Runtime Invocation Failure Contract", workflow_text)
        self.assertIn("provider/authentication rejection", workflow_text)
        self.assertIn("Runtime Invocation Failure Contract", hercules_workflow_text)

        for rel in (
            "README.md",
            "scripts/install-hercules.sh",
            "skills/hercules-agent-capability-preflight/SKILL.md",
            "skills/portable-skill-pack-installation/SKILL.md",
            "skills/cli-installer-ux-governance/SKILL.md",
        ):
            text = (REPO_ROOT / rel).read_text()
            self.assertNotIn("claude auth login --console", text, rel)
            self.assertNotIn("codex login", text, rel)


if __name__ == "__main__":
    unittest.main()
