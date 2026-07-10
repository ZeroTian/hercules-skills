#!/usr/bin/env python3
import importlib.util
import json
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
QUICKSTART_COMMANDS = (
    "curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash",
    "hermes --tui",
    "/skill hercules",
)
CAPABILITY_CONTRACT = (
    SKILLS
    / "hercules-capability-discovery"
    / "references"
    / "capability_matrix.py"
)


class RuntimeSkillContractTest(unittest.TestCase):
    def text(self, name):
        return (SKILLS / name / "SKILL.md").read_text()

    def test_default_runtime_contains_exactly_five_skills(self):
        actual = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(actual, CORE)

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

    def test_no_plugin_is_declared_required(self):
        combined = "\n".join(
            path.read_text() for path in SKILLS.glob("*/SKILL.md") if path.parent.name in CORE
        )
        self.assertIsNone(re.search(r"required plugins?\s*:", combined, re.I))

    def test_readme_has_one_entry_and_three_step_quickstart(self):
        text = (REPO_ROOT / "README.md").read_text()
        for heading in ("Quickstart", "快速开始"):
            with self.subTest(heading=heading):
                block = re.search(
                    rf"^### {heading}\s*$\n+```bash\n(?P<commands>.*?)\n```",
                    text,
                    re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(block, heading)
                self.assertEqual(
                    tuple(block.group("commands").splitlines()),
                    QUICKSTART_COMMANDS,
                )
        for forbidden in (
            "--full", "--minimal", "doctor --fix", "bootstrap --check",
            "npm install", "claude plugins install", "codex login",
        ):
            self.assertNotIn(forbidden, text)

    def test_every_documented_skill_entry_is_hercules(self):
        public_docs = [REPO_ROOT / "README.md", *SKILLS.rglob("*.md")]
        invocations = []
        for path in public_docs:
            invocations.extend(
                re.findall(r"(?m)(?<!\S)/skill\s+[a-z][a-z0-9-]*", path.read_text())
            )
        self.assertTrue(invocations)
        self.assertEqual(set(invocations), {"/skill hercules"})

    def test_only_init_is_a_public_script(self):
        public_root_executables = {
            path.name
            for path in REPO_ROOT.iterdir()
            if path.is_file() and path.stat().st_mode & 0o111
        }
        self.assertEqual(public_root_executables, {"init.sh"})


class CapabilityMatrixBehaviorTest(unittest.TestCase):
    def load_contract(self):
        self.assertTrue(CAPABILITY_CONTRACT.is_file(), CAPABILITY_CONTRACT)
        self.assertFalse(CAPABILITY_CONTRACT.stat().st_mode & 0o111)
        spec = importlib.util.spec_from_file_location(
            "hercules_capability_matrix", CAPABILITY_CONTRACT
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def decide(self, *, demand, facilities, cache=None, invocation=None, fingerprint="v1"):
        contract = self.load_contract()
        return contract.decide_route(
            demand=demand,
            facilities=facilities,
            cache=cache,
            invocation=invocation,
            evidence={"fingerprint": fingerprint},
        )

    def assert_safe_decision(self, decision):
        self.assertEqual(decision["commands"], [])
        rendered = json.dumps(decision, sort_keys=True).lower()
        for forbidden in (
            "npm install",
            "pnpm add",
            "brew install",
            "apt-get install",
            "marketplace add",
            "plugins install",
            "claude auth",
            "codex login",
            "configure provider",
        ):
            self.assertNotIn(forbidden, rendered)

    def assert_route(
        self,
        decision,
        *,
        route,
        fallback=None,
        blocker=None,
        invalidated=False,
        deep_inspection=(),
    ):
        self.assertEqual(decision["route"], route)
        self.assertEqual(decision["fallback"], fallback)
        self.assertEqual(decision["blocker"], blocker)
        self.assertEqual(decision["cache_invalidated"], invalidated)
        self.assertEqual(decision["deep_inspection"], list(deep_inspection))
        self.assert_safe_decision(decision)

    def test_hermes_only_routes_to_hermes(self):
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[{
                "name": "hermes",
                "kind": "agent",
                "capabilities": ["implementation"],
                "authority": "write-capable",
                "evidence": "local-runtime",
            }],
        )
        self.assert_route(decision, route="hermes")

    def test_claude_only_without_plugins_routes_to_claude(self):
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[{
                "name": "claude",
                "kind": "cli",
                "capabilities": ["implementation"],
                "authority": "write-capable",
                "evidence": "executable-version",
            }],
        )
        self.assert_route(decision, route="claude")

    def test_codex_only_routes_to_codex(self):
        decision = self.decide(
            demand={"role": "independent-review", "authority": "read-only"},
            facilities=[{
                "name": "codex",
                "kind": "cli",
                "capabilities": ["independent-review"],
                "authority": "read-only",
                "evidence": "executable-version",
            }],
        )
        self.assert_route(decision, route="codex")

    def test_claude_and_codex_honor_explicit_preference(self):
        decision = self.decide(
            demand={
                "role": "implementation",
                "authority": "write-capable",
                "user_preference": "codex",
            },
            facilities=[
                {
                    "name": "claude",
                    "kind": "cli",
                    "capabilities": ["implementation"],
                    "authority": "write-capable",
                    "evidence": "executable-version",
                },
                {
                    "name": "codex",
                    "kind": "cli",
                    "capabilities": ["implementation"],
                    "authority": "write-capable",
                    "evidence": "executable-version",
                },
            ],
        )
        self.assert_route(decision, route="codex")

    def test_arbitrary_plugins_and_mcp_route_by_confirmed_task_fit(self):
        decision = self.decide(
            demand={"role": "browser-control", "authority": "write-capable"},
            facilities=[
                {
                    "name": "aurora-browser",
                    "kind": "plugin",
                    "capabilities": ["browser-control"],
                    "authority": "write-capable",
                    "evidence": "local-manifest",
                },
                {
                    "name": "atlas-docs",
                    "kind": "mcp",
                    "capabilities": ["research"],
                    "authority": "read-only",
                    "evidence": "local-tool-metadata",
                },
            ],
        )
        self.assert_route(decision, route="aurora-browser")

    def test_task_relevant_unknown_plugin_is_deep_inspected_before_selection(self):
        decision = self.decide(
            demand={"role": "browser-control", "authority": "write-capable"},
            facilities=[{
                "name": "comet-tools",
                "kind": "plugin",
                "capabilities": [],
                "deep_capabilities": ["browser-control"],
                "relevant": True,
                "authority": "write-capable",
                "evidence": "local-manifest-and-skill",
            }],
        )
        self.assert_route(
            decision,
            route="comet-tools",
            deep_inspection=("comet-tools",),
        )

    def test_stale_cache_is_invalidated_after_capability_change(self):
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[{
                "name": "codex",
                "kind": "cli",
                "capabilities": ["implementation"],
                "authority": "write-capable",
                "evidence": "executable-version",
            }],
            cache={
                "fingerprint": "old",
                "routes": {"implementation": "claude"},
            },
            fingerprint="new",
        )
        self.assert_route(decision, route="codex", invalidated=True)
        self.assertEqual(decision["invalidation_reason"], "stale-cache")

    def test_provider_access_rejection_invalidates_and_falls_back(self):
        decision = self.decide(
            demand={
                "role": "implementation",
                "authority": "write-capable",
                "user_preference": "claude",
            },
            facilities=[
                {
                    "name": "claude",
                    "kind": "cli",
                    "capabilities": ["implementation"],
                    "authority": "write-capable",
                    "evidence": "executable-version",
                },
                {
                    "name": "codex",
                    "kind": "cli",
                    "capabilities": ["implementation"],
                    "authority": "write-capable",
                    "evidence": "executable-version",
                },
            ],
            cache={
                "fingerprint": "v1",
                "routes": {"implementation": "claude"},
            },
            invocation={
                "facility": "claude",
                "ok": False,
                "category": "provider/access rejection",
            },
        )
        self.assert_route(
            decision,
            route="codex",
            fallback={
                "from": "claude",
                "to": "codex",
                "reason": "provider/access rejection",
            },
            invalidated=True,
        )
        self.assertEqual(decision["invalidation_reason"], "invocation-failure")

    def test_no_viable_capability_returns_concise_blocker(self):
        decision = self.decide(
            demand={"role": "browser-control", "authority": "write-capable"},
            facilities=[{
                "name": "atlas-docs",
                "kind": "mcp",
                "capabilities": ["research"],
                "authority": "read-only",
                "evidence": "local-tool-metadata",
            }],
        )
        self.assert_route(
            decision,
            route=None,
            blocker="No confirmed safe capability for browser-control.",
        )


if __name__ == "__main__":
    unittest.main()
