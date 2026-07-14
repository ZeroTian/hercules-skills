#!/usr/bin/env python3
import importlib.util
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / "skills"
PUBLIC_SKILL = "hercules"
PUBLIC_RUNTIME_SKILLS = {PUBLIC_SKILL}
PUBLIC_REFERENCES = SKILLS / PUBLIC_SKILL / "references"
INTERNAL_WORKFLOW_REFERENCES = {
    "capability-discovery.md",
    "collaborative-workflow.md",
    "review-workflow.md",
    "project-init.md",
}
TERMINAL_QUICKSTART = (
    "curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash",
    "hermes --tui",
)
CAPABILITY_CONTRACT = PUBLIC_REFERENCES / "capability_matrix.py"
HERCULES_COMMAND_RE = re.compile(
    r"(?m)(?<![A-Za-z0-9_/])/(hercules(?:-[a-z0-9-]+)?)"
)
DOCUMENTED_SKILL_INVOCATION_RE = re.compile(r"/skill[ \t]+[a-z][a-z0-9-]*")
MARKDOWN_SKILL_PREFIXES = frozenset({"`", "*", "(", "[", "{", "<", ">", "'", '"', "~"})


def documented_skill_invocations(text):
    invocations = []
    for match in DOCUMENTED_SKILL_INVOCATION_RE.finditer(text):
        start = match.start()
        if start == 0:
            invocations.append(match.group())
            continue
        prefix = text[:start]
        previous = prefix[-1]
        if previous.isspace() or previous in MARKDOWN_SKILL_PREFIXES:
            invocations.append(match.group())
            continue
        if previous != "_":
            continue
        opener_start = len(prefix)
        while opener_start and prefix[opener_start - 1] == "_":
            opener_start -= 1
        if opener_start == 0:
            invocations.append(match.group())
            continue
        before_opener = prefix[opener_start - 1]
        if before_opener.isspace() or before_opener in MARKDOWN_SKILL_PREFIXES:
            invocations.append(match.group())
    return invocations


class RuntimeSkillContractTest(unittest.TestCase):
    def text(self, name):
        return (SKILLS / name / "SKILL.md").read_text()

    def reference_text(self, name):
        return (PUBLIC_REFERENCES / name).read_text(encoding="utf-8")

    def markdown_section(self, text, heading, level):
        marker = "#" * level
        match = re.search(
            rf"(?m)^{re.escape(marker)} {re.escape(heading)}\s*$",
            text,
        )
        self.assertIsNotNone(match, heading)
        following = text[match.end():]
        next_heading = re.search(rf"(?m)^#{{1,{level}}} ", following)
        return following[:next_heading.start()] if next_heading else following

    def test_runtime_contains_exactly_one_discoverable_skill(self):
        skill_files = sorted(SKILLS.rglob("SKILL.md"))
        self.assertEqual(skill_files, [SKILLS / PUBLIC_SKILL / "SKILL.md"])

    def test_default_runtime_contains_only_public_skill(self):
        actual = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(actual, PUBLIC_RUNTIME_SKILLS)

    def test_public_entry_routes_by_task_need(self):
        text = self.text("hercules")
        for phrase in ("single public entry", "task capability roles", "session capability cache", "fallback"):
            self.assertIn(phrase, text)

    def test_public_entry_is_hermes_controller_owned(self):
        text = self.text("hercules")
        for phrase in (
            "Hermes controller owns Hercules routing",
            "the route is complete",
            "must not load Hercules",
            "must not perform capability discovery",
            "must not select another facility",
        ):
            self.assertIn(phrase, text)

    def test_public_entry_does_not_infer_a_cli_surface(self):
        text = self.text("hercules")
        interface = " ".join(
            self.markdown_section(text, "Interface Contract", 2).split()
        )
        self.assertRegex(
            interface,
            r"Hercules is exposed as this Skill.*does not imply that a `hercules` executable",
        )
        self.assertRegex(
            interface,
            r"Never synthesize commands.*`hercules discover`.*`hercules execute`",
        )
        self.assertRegex(
            interface,
            r"Invoke a same-named command only when.*executable is confirmed.*documentation explicitly defines that command",
        )
        self.assertRegex(
            interface,
            r"restriction does not block Skill/reference loading.*direct invocation of confirmed facilities",
        )

    def test_runtime_docs_do_not_advertise_bare_hercules_cli_commands(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [REPO_ROOT / "README.md", *SKILLS.rglob("*.md")]
        )
        executable_lines = re.findall(
            r"(?mi)^\s*(?:[$>]\s*)?hercules\s+(?:discover|execute)\b.*$",
            text,
        )
        self.assertEqual(executable_lines, [])

    def test_public_entry_links_runtime_routing_reference(self):
        text = self.text("hercules")
        link = re.search(
            r"\[[^\]]+\]\((references/runtime-routing\.md)\)",
            text,
        )
        self.assertIsNotNone(link)
        self.assertTrue((SKILLS / "hercules" / link.group(1)).is_file())

    def test_public_router_links_all_internal_workflows(self):
        text = self.text(PUBLIC_SKILL)
        linked = set(re.findall(r"references/([a-z-]+\.md)", text))
        self.assertTrue(INTERNAL_WORKFLOW_REFERENCES <= linked)
        for name in INTERNAL_WORKFLOW_REFERENCES:
            self.assertTrue((PUBLIC_REFERENCES / name).is_file(), name)

    def test_retired_internal_skill_commands_are_not_discoverable(self):
        for name in (
            "hercules-capability-discovery",
            "hercules-collaborative-workflow",
            "hercules-review-workflow",
            "hercules-project-init",
        ):
            self.assertFalse((SKILLS / name / "SKILL.md").exists(), name)

    def test_capability_discovery_is_an_internal_reference(self):
        self.assertFalse((SKILLS / "hercules-capability-discovery").exists())
        text = self.reference_text("capability-discovery.md")
        for phrase in ("demand-led", "shallow discovery", "deep plugin exploration", "ephemeral capability map"):
            self.assertIn(phrase, text)
        self.assertFalse(text.startswith("---"))
        for forbidden in (
            "npm install", "pnpm add", "brew install", "apt-get install",
            "claude plugins install", "marketplace add", "claude auth", "codex login",
        ):
            self.assertNotIn(forbidden, text)

    def test_collaboration_consumes_confirmed_capabilities(self):
        text = self.reference_text("collaborative-workflow.md")
        self.assertFalse(text.startswith("---"))
        for phrase in ("confirmed capability map", "user and project preference", "sanitized failure category", "fallback"):
            self.assertIn(phrase, text)

    def test_collaboration_brief_marks_the_facility_as_already_routed(self):
        text = self.reference_text("collaborative-workflow.md")
        brief = self.markdown_section(text, "Invocation Brief", 2)
        for phrase in (
            "controller: Hermes",
            "route_state: selected",
            "facility: <confirmed facility>",
            "role: <capability role>",
            "authority: read-only | write-capable",
            "must not load Hercules",
            "must not perform capability discovery",
            "must not select another facility",
            "return the failure to Hermes",
        ):
            self.assertIn(phrase, brief)

    def test_review_requires_independence_only_when_task_requires_it(self):
        text = self.reference_text("review-workflow.md")
        self.assertFalse(text.startswith("---"))
        self.assertIn("independence requirement", text)
        self.assertIn("available reviewer", text)
        self.assertNotIn("Codex is always required", text)

    def test_review_brief_marks_the_reviewer_as_already_routed(self):
        text = self.reference_text("review-workflow.md")
        brief = self.markdown_section(text, "Invocation Brief", 2)
        for phrase in (
            "controller: Hermes",
            "route_state: selected",
            "facility: <confirmed facility>",
            "role: review",
            "authority: read-only",
            "must not load Hercules",
            "must not perform capability discovery",
            "must not select another facility",
            "return the failure to Hermes",
        ):
            self.assertIn(phrase, brief)

    def test_project_init_is_project_scoped(self):
        text = self.reference_text("project-init.md")
        self.assertFalse(text.startswith("---"))
        for phrase in ("project-scoped", "do not install", "preserve existing instructions"):
            self.assertIn(phrase, text)

    def test_project_init_separates_shared_execution_from_controller_routing(self):
        text = self.reference_text("project-init.md")
        shared = self.markdown_section(
            text, "Canonical Shared Execution Contract", 2
        )
        hermes = self.markdown_section(text, "`HERMES.md` controller adapter", 3)

        for phrase in (
            "AGENTS.md",
            "execute the bounded brief directly",
            "must not load Hercules",
            "must not perform capability discovery",
            "must not select another facility",
            "return the failure to Hermes",
        ):
            self.assertIn(phrase, shared)
        for phrase in (
            "route non-trivial project work through Hercules",
            "perform relevant capability discovery",
            "follow Hercules fallback rules",
            "independently verify actual outputs",
        ):
            self.assertNotIn(phrase, shared)
            self.assertIn(phrase, hermes)

    def test_project_init_keeps_cli_boundary_in_controller_adapter(self):
        text = self.reference_text("project-init.md")
        hermes = " ".join(
            self.markdown_section(
                text, "`HERMES.md` controller adapter", 3
            ).split()
        )
        self.assertRegex(
            hermes,
            r"Hercules is loaded as a Skill workflow.*synthetic `hercules discover/execute` commands are forbidden.*confirmed executable/documentation evidence",
        )
        self.assertRegex(
            hermes,
            r"does not block Skill/reference loading.*direct invocation of confirmed facilities",
        )

    def test_repository_instructions_dogfood_controller_facility_boundary(self):
        agents = " ".join((REPO_ROOT / "AGENTS.md").read_text().split())
        claude = " ".join((REPO_ROOT / "CLAUDE.md").read_text().split())
        hermes = " ".join((REPO_ROOT / "HERMES.md").read_text().split())
        self.assertIn("Codex is the independent reviewer and acceptance gate", agents)
        self.assertIn("selected review facility, not the Hermes controller", agents)
        self.assertIn("execute the bounded brief directly", agents)
        self.assertIn("must not load Hercules", agents)
        self.assertNotIn("Route non-trivial project work through Hercules", agents)
        self.assertIn("Claude Code is the scoped implementation facility", claude)
        self.assertIn("not the Hermes controller", claude)
        self.assertIn("must not load Hercules", claude)
        self.assertRegex(
            hermes,
            r"Hercules is a Skill workflow, not an assumed CLI.*do not synthesize `hercules discover/execute`.*confirmed executable and documentation evidence",
        )
        self.assertRegex(
            hermes,
            r"does not block Skill/reference loading.*direct invocation of confirmed facilities",
        )

    def test_project_init_uses_minimal_tool_adapters(self):
        text = self.reference_text("project-init.md")
        shared = self.markdown_section(
            text, "Canonical Shared Execution Contract", 2
        )
        claude = self.markdown_section(
            text, "`CLAUDE.md` facility adapter", 3
        )
        hermes = self.markdown_section(text, "`HERMES.md` controller adapter", 3)
        controller_rule_phrases = (
            "route non-trivial project work through Hercules",
            "perform relevant capability discovery",
            "must not be represented as Claude Code or Codex CLI",
            "follow Hercules fallback rules",
            "independently verify actual outputs",
        )

        self.assertIn("Claude-specific implementation boundaries", claude)
        self.assertIn("canonical shared execution contract in `AGENTS.md`", claude)
        self.assertIn("must not load Hercules", claude)
        self.assertIn("Hermes is the controller", hermes)
        self.assertIn("load the canonical shared execution contract and Hercules", hermes)
        self.assertIn("`delegate_task`", hermes)
        self.assertNotIn("`delegate_task`", shared)
        self.assertNotIn("`delegate_task`", claude)
        self.assertEqual(text.count("`delegate_task`"), hermes.count("`delegate_task`"))
        for phrase in controller_rule_phrases:
            self.assertNotIn(phrase, shared)
            self.assertNotIn(phrase, claude)
            self.assertIn(phrase, hermes)
            self.assertEqual(text.count(phrase), hermes.count(phrase))

    def test_project_init_requires_approved_idempotent_merge(self):
        text = self.reference_text("project-init.md")
        for phrase in (
            "Preview the exact additions and changed files",
            "Obtain explicit user approval",
            "Repeated initialization must be idempotent",
            "stop and show the conflict",
        ):
            self.assertIn(phrase, text)

    def test_no_plugin_is_declared_required(self):
        combined = "\n".join(
            path.read_text() for path in SKILLS.rglob("*.md")
        )
        self.assertIsNone(re.search(r"required plugins?\s*:", combined, re.I))

    def test_readme_has_one_entry_and_real_hermes_invocation(self):
        text = (REPO_ROOT / "README.md").read_text()
        self.assertIn("single adaptive Hermes Skill", text)
        self.assertIn("一个自适应的 Hermes Skill", text)
        sections = {
            "Quickstart": "/hercules <your task>",
            "快速开始": "/hercules <你的任务>",
        }
        for heading, invocation in sections.items():
            with self.subTest(heading=heading):
                block = re.search(
                    rf"^### {heading}\s*$\n+```bash\n(?P<commands>.*?)\n```",
                    text,
                    re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(block, heading)
                self.assertEqual(
                    tuple(block.group("commands").splitlines()),
                    TERMINAL_QUICKSTART,
                )
                section = text[block.end():]
                next_heading = re.search(r"^## ", section, re.MULTILINE)
                if next_heading:
                    section = section[:next_heading.start()]
                self.assertIn(invocation, section)
        for forbidden in (
            "--full", "--minimal", "doctor --fix", "bootstrap --check",
            "npm install", "claude plugins install", "codex login",
        ):
            self.assertNotIn(forbidden, text)

    def test_only_public_hercules_command_is_documented(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                REPO_ROOT / "README.md",
                REPO_ROOT / "init.sh",
                *SKILLS.rglob("*.md"),
            ]
        )
        commands = {f"/{name}" for name in HERCULES_COMMAND_RE.findall(text)}
        self.assertEqual(commands, {"/hercules"})
        self.assertNotIn("/skill hercules", text)

    def test_documented_skill_entry_parser_handles_markdown_wrappers(self):
        wrapped_invocations = (
            "/skill other",
            "`/skill other`",
            "``/skill other``",
            "**/skill other**",
            "_/skill rogue_",
            "__/skill rogue__",
            "___/skill rogue___",
            "~~/skill other~~",
            "<code>/skill other</code>",
            "(/skill other)",
            "[/skill other]",
            "> /skill other",
            "- `/skill other`",
        )
        for markdown in wrapped_invocations:
            with self.subTest(markdown=markdown):
                self.assertEqual(
                    documented_skill_invocations(markdown),
                    ["/skill rogue"] if "rogue" in markdown else ["/skill other"],
                )

    def test_documented_skill_entry_parser_ignores_urls_and_paths(self):
        non_invocations = (
            "https://example.invalid/skill rogue",
            "/docs/skill rogue",
            "path_/skill rogue",
            "path__/skill rogue",
            "./skill rogue",
            "../skill rogue",
            "C:/skill rogue",
        )
        for text in non_invocations:
            with self.subTest(text=text):
                self.assertEqual(documented_skill_invocations(text), [])

    def test_only_init_is_a_public_script(self):
        public_root_executables = {
            path.name
            for path in REPO_ROOT.iterdir()
            if path.is_file() and path.stat().st_mode & 0o111
        }
        self.assertEqual(public_root_executables, {"init.sh"})


class InvocationLifecycleContractTest(unittest.TestCase):
    """Regression tests for the facility invocation lifecycle contract.

    The lifecycle decides *how* a confirmed facility is driven
    (foreground/background scheduling, PTY/non-PTY terminal mode) as a
    concern orthogonal to *which* facility is selected.
    """

    REFERENCE = "invocation-lifecycle.md"

    def setUp(self):
        self.reference = (PUBLIC_REFERENCES / self.REFERENCE).read_text(encoding="utf-8")
        self.skill = (SKILLS / PUBLIC_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.collaborative = (
            PUBLIC_REFERENCES / "collaborative-workflow.md"
        ).read_text(encoding="utf-8")

    def test_lifecycle_reference_exists_without_skill_frontmatter(self):
        self.assertTrue((PUBLIC_REFERENCES / self.REFERENCE).is_file())
        self.assertFalse(self.reference.startswith("---"))

    def test_public_skill_links_lifecycle_reference(self):
        self.assertRegex(
            self.skill,
            r"\[[^\]]+\]\(references/invocation-lifecycle\.md\)",
        )

    def test_collaborative_workflow_links_lifecycle_reference(self):
        self.assertRegex(
            self.collaborative,
            r"\[[^\]]+\]\(invocation-lifecycle\.md\)",
        )

    def test_scheduling_and_terminal_mode_are_orthogonal_decisions(self):
        for phrase in ("foreground", "background", "PTY", "non-PTY"):
            self.assertIn(phrase, self.reference)
        # Orthogonality must be stated, not merely implied by co-occurrence.
        self.assertRegex(self.reference, r"(?i)orthogonal")

    def test_foreground_default_is_narrow_and_background_defaults_for_risky_work(self):
        for phrase in ("read-only", "non-interactive", "duration-stable"):
            self.assertIn(phrase, self.reference)
        for phrase in (
            "code mutation", "tests", "builds", "multi-step",
            "network", "browser", "uncertain duration",
        ):
            self.assertIn(phrase, self.reference)
        self.assertRegex(self.reference, r"(?i)tracked background process")

    def test_foreground_safety_margin_and_unknown_completion_on_overrun(self):
        for phrase in (
            "safety margin", "unknown", "exit status", "remaining processes",
            "artifact", "diff", "tests",
        ):
            self.assertIn(phrase, self.reference)
        self.assertIn("Never blindly replay a mutating brief", self.reference)

    def test_pty_rules_encode_confirmed_facility_examples(self):
        for phrase in ("terminal semantics", "interactive input", "structured output"):
            self.assertIn(phrase, self.reference)
        # Confirmed examples, overridable by locally inspected documentation.
        self.assertRegex(self.reference, r"Claude print mode.*`-p`")
        self.assertIn("Codex CLI", self.reference)
        self.assertRegex(self.reference, r"(?i)locally inspected facility documentation")

    def test_background_execution_remains_observable(self):
        for phrase in (
            "process handle", "completion notification", "poll",
            "serial blocking", "exit status", "clean up",
        ):
            self.assertIn(phrase, self.reference)

    def test_hermes_adapter_maps_terminal_and_process_lifecycle(self):
        for phrase in (
            "terminal(command=<bounded command>, background=true, notify_on_complete=true, pty=<independent terminal-mode decision>)",
            'process(action="poll", session_id=<id>)',
            'process(action="log", session_id=<id>)',
            'process(action="wait", session_id=<id>, timeout=<bounded seconds>)',
            'process(action="submit", session_id=<id>, data=<input>)',
            'process(action="write", session_id=<id>, data=<input>)',
            'process(action="close", session_id=<id>)',
            'process(action="kill", session_id=<id>)',
        ):
            self.assertIn(phrase, self.reference)

    def test_background_unsupported_has_an_explicit_safe_fallback(self):
        self.assertIn("background unsupported", self.reference)
        for phrase in (
            "bounded foreground",
            "another confirmed facility",
            "controller authority",
            "report a blocker",
        ):
            self.assertIn(phrase, self.reference)

    def test_facility_drift_does_not_authorize_skill_self_modification(self):
        self.assertIn("report the contract drift", self.reference)
        self.assertIn(
            "Do not modify this Skill or reference unless the current task explicitly authorizes",
            self.reference,
        )

    def test_least_sufficient_authority_and_independent_verification_preserved(self):
        self.assertIn("least-sufficient authority", self.reference)
        self.assertIn("post-run verification", self.reference)
        self.assertRegex(self.reference, r"\[[^\]]+\]\(invocation-failure\.md\)")

    def test_lifecycle_reference_respects_non_destructive_boundary(self):
        for forbidden in (
            "npm install", "pnpm add", "brew install", "apt-get install",
            "claude plugins install", "marketplace add", "claude auth", "codex login",
            "configure provider",
        ):
            self.assertNotIn(forbidden, self.reference)
        self.assertNotIn("hercules discover", self.reference)
        self.assertNotIn("hercules execute", self.reference)
        self.assertNotIn("/Users/", self.reference)
        self.assertNotIn("~/.claude", self.reference)

    def test_readme_internal_reference_table_lists_lifecycle(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("invocation-lifecycle.md", readme)

    def test_controller_owned_routing_release_declares_version_1_1_3(self):
        match = re.search(r"(?m)^version:\s*(\d+)\.(\d+)\.(\d+)", self.skill)
        self.assertIsNotNone(match, "SKILL.md frontmatter must declare a semver version")
        version = tuple(int(match.group(i)) for i in (1, 2, 3))
        self.assertEqual(version, (1, 1, 3))


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
        self.assertEqual(
            set(decision["capability_map"]), set(decision["discovery"]["roles"])
        )
        for observable in ("route", "capability_map", "fallback", "failure", "blocker"):
            self.assertIn(observable, decision)
        self.assert_safe_decision(decision)

    def test_design_environment_matrix_is_table_driven(self):
        scenarios = (
            ("Hermes only", self.test_hermes_only_routes_to_hermes),
            ("Claude only with no plugins", self.test_claude_only_without_plugins_routes_to_claude),
            ("Codex only", self.test_codex_only_routes_to_codex),
            ("Claude and Codex together", self.test_claude_and_codex_honor_explicit_preference),
            ("arbitrary plugins and MCP", self.test_arbitrary_plugins_and_mcp_route_by_confirmed_task_fit),
            ("task-relevant deep inspection", self.test_task_relevant_unknown_plugin_is_deep_inspected_before_selection),
            ("stale cache", self.test_stale_cache_is_invalidated_after_capability_change),
            ("provider rejection", self.test_provider_access_rejection_invalidates_and_falls_back),
            ("no viable capability", self.test_no_viable_capability_returns_concise_blocker),
        )
        for environment, scenario in scenarios:
            with self.subTest(environment=environment):
                scenario()

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

    def test_compact_cache_without_authority_evidence_is_invalidated(self):
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[],
            cache={
                "fingerprint": "v1",
                "routes": {"implementation": "review-only-tool"},
            },
        )
        self.assert_route(
            decision,
            route=None,
            blocker="No confirmed safe capability for implementation.",
            invalidated=True,
        )
        self.assertEqual(decision["invalidation_reason"], "invalid-cache-record")
        self.assertEqual(decision["discovery"]["scanned"], [])
        self.assertEqual(decision["capability_map"]["implementation"], [])

    def test_read_only_cache_record_cannot_satisfy_write_demand(self):
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[{
                "name": "hermes",
                "kind": "agent",
                "capabilities": ["implementation"],
                "authority": "write-capable",
                "evidence": "local-runtime",
            }],
            cache={
                "fingerprint": "v1",
                "routes": {
                    "implementation": {
                        "role": "implementation",
                        "facility": "review-only-tool",
                        "kind": "cli",
                        "confirmed_surface": ["implementation"],
                        "authority": "read-only",
                        "evidence": "executable-version",
                        "fingerprint": "v1",
                    }
                },
            },
        )
        self.assert_route(decision, route="hermes", invalidated=True)
        self.assertEqual(decision["invalidation_reason"], "invalid-cache-record")
        self.assertEqual(decision["discovery"]["scanned"], ["hermes"])

    def test_fresh_normalized_cache_record_preserves_confirmed_evidence(self):
        cached_record = {
            "role": "implementation",
            "facility": "claude",
            "kind": "cli",
            "confirmed_surface": ["implementation"],
            "authority": "write-capable",
            "evidence": "executable-version",
            "fingerprint": "v1",
        }
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[],
            cache={
                "fingerprint": "v1",
                "routes": {"implementation": cached_record},
            },
        )
        self.assert_route(decision, route="claude")
        self.assertEqual(decision["discovery"]["scanned"], [])
        self.assertEqual(
            decision["capability_map"]["implementation"],
            [cached_record],
        )

    def test_discovered_record_round_trips_through_session_cache_without_scanning(self):
        first = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[{
                "name": "hermes",
                "kind": "agent",
                "capabilities": ["implementation"],
                "authority": "write-capable",
                "evidence": "local-runtime",
            }],
            fingerprint="session-v1",
        )
        discovered_record = first["capability_map"]["implementation"][0]
        self.assertEqual(
            discovered_record,
            {
                "role": "implementation",
                "facility": "hermes",
                "kind": "agent",
                "confirmed_surface": ["implementation"],
                "authority": "write-capable",
                "evidence": "local-runtime",
                "fingerprint": "session-v1",
            },
        )

        reused = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[],
            cache={
                "fingerprint": "session-v1",
                "routes": {"implementation": discovered_record},
            },
            fingerprint="session-v1",
        )

        self.assert_route(reused, route="hermes")
        self.assertEqual(reused["discovery"]["scanned"], [])
        self.assertEqual(
            reused["capability_map"]["implementation"],
            [discovered_record],
        )

    def test_fresh_cache_missing_required_role_is_invalidated_then_falls_back(self):
        decision = self.decide(
            demand={"role": "implementation", "authority": "write-capable"},
            facilities=[{
                "name": "hermes",
                "kind": "agent",
                "capabilities": ["implementation"],
                "authority": "write-capable",
                "evidence": "local-runtime",
            }],
            cache={
                "fingerprint": "v1",
                "routes": {"review": "codex"},
            },
        )
        self.assert_route(decision, route="hermes", invalidated=True)
        self.assertEqual(decision["invalidation_reason"], "cache-missing-role")
        self.assertEqual(decision["discovery"]["scanned"], ["hermes"])

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
