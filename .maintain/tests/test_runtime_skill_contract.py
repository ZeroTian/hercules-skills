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


if __name__ == "__main__":
    unittest.main()
