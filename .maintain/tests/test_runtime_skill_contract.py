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

    def test_no_plugin_is_declared_required(self):
        combined = "\n".join(
            path.read_text() for path in SKILLS.glob("*/SKILL.md") if path.parent.name in CORE
        )
        self.assertIsNone(re.search(r"required plugins?\s*:", combined, re.I))


if __name__ == "__main__":
    unittest.main()
