#!/usr/bin/env python3
"""Lightweight Hercules skill-pack validator and reflection scanner.

Runs with Python stdlib only. Checks:
  - frontmatter presence and required fields (name, description, version) for skills/*/SKILL.md
  - description length <= 1024 characters
  - linked file directories are only references/templates/scripts/assets
  - skill-local linked-file references point to existing files
  - exact five-Skill runtime scope vs git tracked skills and visible skill dirs
  - maintainer SKILL_NAVIGATION role/maturity table consistency
  - TASKS archive links, no duplicate task IDs across live/archive ledgers
  - governance files exist
  - shell scripts pass `bash -n`
  - optional JSON output and strict warning-as-failure release gate
  - ledger reflection signals from TASKS.md and codex-reviews/*.md:
    repeated CR IDs, max-turns/max turns, blocked/阻塞, repair-loop/需修改,
    missing trajectory blocks for open formal tasks, and whether an evidence
    package should be considered.

Output sections: ERRORS, WARNINGS, REFLECTION SIGNALS, SUMMARY.
Exit nonzero only for structural errors (ERRORS non-empty) by default. In
`--strict` mode, warnings also fail the command; reflection signals remain
advisory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_COLLAB = REPO_ROOT / ".maintain" / "docs" / "ai-collaboration"
EXPECTED_RUNTIME_SKILLS = {
    "hercules",
    "hercules-capability-discovery",
    "hercules-collaborative-workflow",
    "hercules-review-workflow",
    "hercules-project-init",
}

REQUIRED_FRONTMATTER_FIELDS = ("name", "description", "version")
ALLOWED_LINKED_DIRS = {"references", "templates", "scripts", "assets"}
DESCRIPTION_MAX = 1024

GOVERNANCE_ROOT_FILES = (
    "README.md",
    "HERMES.md",
    "CLAUDE.md",
    "AGENTS.md",
)
GOVERNANCE_DOC_PATHS = (
    ".maintain/docs/ai-collaboration/README.md",
    ".maintain/docs/ai-collaboration/TASKS.md",
    ".maintain/docs/ai-collaboration/ARCHITECTURE.md",
    ".maintain/docs/ai-collaboration/SKILL_NAVIGATION.md",
    ".maintain/docs/ai-collaboration/PROJECT_AUDIT.md",
    ".maintain/docs/ai-collaboration/tasks",
    ".maintain/docs/ai-collaboration/codex-reviews",
    ".maintain/docs/ai-collaboration/decisions",
)

OPEN_TASK_STATUSES = ("待处理", "处理中", "阻塞", "待复核", "需修改")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.signals: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def signal(self, msg: str) -> None:
        self.signals.append(msg)

    def exit_code(self, *, strict: bool = False) -> int:
        if self.errors:
            return 1
        if strict and self.warnings:
            return 1
        return 0

    def to_dict(self, *, strict: bool = False) -> dict[str, object]:
        return {
            "errors": self.errors,
            "warnings": self.warnings,
            "signals": self.signals,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "signals": len(self.signals),
                "strict": strict,
                "exit_code": self.exit_code(strict=strict),
            },
        }


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return a flat dict of top-level frontmatter keys, or None if absent.

    Only parses simple `key: value` lines at the top YAML level. Quoted
    strings, bare scalars, and block scalars are handled for the fields we
    actually inspect (name/description/version). Nested keys under
    metadata/tags are ignored for required-field checks.
    """
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        # Strip matching surrounding quotes.
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        fields[key] = val
    return fields


def check_skill_frontmatter(report: Report) -> list[Path]:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        report.error("no skills/*/SKILL.md files found under skills/")
        return []
    for sf in skill_files:
        text = sf.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            report.error(f"{sf.relative_to(REPO_ROOT)}: missing YAML frontmatter")
            continue
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in fm or not fm[field].strip():
                report.error(f"{sf.relative_to(REPO_ROOT)}: frontmatter missing required field '{field}'")
        desc = fm.get("description", "")
        if desc and len(desc) > DESCRIPTION_MAX:
            report.error(
                f"{sf.relative_to(REPO_ROOT)}: description length {len(desc)} exceeds {DESCRIPTION_MAX}"
            )
        name = fm.get("name", "")
        if name and name != sf.parent.name:
            report.warn(
                f"{sf.relative_to(REPO_ROOT)}: frontmatter name '{name}' != directory '{sf.parent.name}'"
            )
    return skill_files


def check_linked_dirs(report: Report) -> None:
    for skill_dir in sorted(SKILLS_DIR.glob("*/")):
        for child in skill_dir.iterdir():
            if child.is_dir():
                if child.name not in ALLOWED_LINKED_DIRS:
                    report.error(
                        f"{skill_dir.relative_to(REPO_ROOT)}: unexpected subdirectory '{child.name}' "
                        f"(allowed: {sorted(ALLOWED_LINKED_DIRS)})"
                    )


LINKED_FILE_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?P<path>(?:references|templates|scripts|assets)/[A-Za-z0-9._/@%+=:,~-]+(?:/[A-Za-z0-9._/@%+=:,~-]+)*)"
)


def normalize_linked_candidate(raw: str) -> str:
    """Trim common Markdown/sentence punctuation from a linked-file candidate."""
    return raw.strip("`'\"<>()[]{}.,;:")


def should_validate_linked_candidate(line: str, rel: str) -> bool:
    """Return True for references that are intended skill-local linked files.

    SKILL.md files also contain downstream command examples such as
    `scripts/run_tests.sh`. Those should not be treated as local linked files
    for the current skill, but normal inline prose such as
    "See `references/foo.md`" should be validated.
    """
    lowered = line.strip().lower()
    downstream_hints = (
        "downstream",
        "other repos",
        "repo's documented wrapper",
        "arbitrary project",
        "target project",
        "project's documented",
    )
    if rel == "scripts/run_tests.sh":
        return False
    if rel.startswith("scripts/") and any(hint in lowered for hint in downstream_hints):
        return False
    # Repo-qualified or cross-skill paths are excluded by LINKED_FILE_RE's
    # negative lookbehind before this point. Anything left is a same-skill
    # references/templates/scripts/assets mention and should be checked.
    return True


def check_linked_file_references(report: Report, skill_files: list[Path]) -> None:
    """Warn when SKILL.md mentions a linked file that is not present.

    This is intentionally conservative: it only scans path-like mentions under
    the allowed linked directories. It catches broken `references/foo.md`,
    `templates/foo`, `scripts/foo.sh`, and `assets/foo` references without
    requiring full Markdown parsing.
    """
    for sf in skill_files:
        text = sf.read_text(encoding="utf-8")
        seen: set[str] = set()
        for line in text.splitlines():
            for match in LINKED_FILE_RE.finditer(line):
                rel = normalize_linked_candidate(match.group("path"))
                if not rel or rel in seen or not should_validate_linked_candidate(line, rel):
                    continue
                seen.add(rel)
                target = sf.parent / rel
                if not target.exists():
                    report.warn(f"{sf.relative_to(REPO_ROOT)}: linked file not found: {rel}")


def git_tracked_skills() -> set[str]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "skills/"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()
    names: set[str] = set()
    for line in out.stdout.splitlines():
        parts = line.split("/")
        if len(parts) >= 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
            names.add(parts[1])
    return names


def visible_skill_dirs() -> set[str]:
    if not SKILLS_DIR.exists():
        return set()
    return {p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}


def check_runtime_skill_scope(report: Report) -> None:
    """Require the product runtime to contain exactly the five public Skills."""
    tracked = git_tracked_skills()
    visible = visible_skill_dirs()

    for label, actual in (("git-tracked", tracked), ("visible", visible)):
        if actual != EXPECTED_RUNTIME_SKILLS:
            report.error(
                f"exact runtime skill scope drift ({label}): "
                f"missing={sorted(EXPECTED_RUNTIME_SKILLS - actual)}, "
                f"extra={sorted(actual - EXPECTED_RUNTIME_SKILLS)}"
            )



SKILL_NAV_ALLOWED_ROLES = {"entry/composite", "atom", "specialized atom"}
SKILL_NAV_ALLOWED_MATURITY = {"core", "domain"}
TASK_ARCHIVE_LINK_RE = re.compile(
    r"\.maintain/docs/ai-collaboration/tasks/[A-Za-z0-9._-]+\.md"
)


def parse_skill_navigation(path: Path) -> dict[str, list[tuple[str, str]]]:
    """Return skill -> [(role, maturity), ...] from SKILL_NAVIGATION.md."""
    rows: dict[str, list[tuple[str, str]]] = {}
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 5 or cols[0] == "Skill":
            continue
        m = re.fullmatch(r"`([a-z][a-z0-9-]*)`", cols[0])
        if not m:
            continue
        rows.setdefault(m.group(1), []).append((cols[1], cols[2]))
    return rows


def check_skill_navigation(report: Report) -> None:
    nav_path = DOCS_COLLAB / "SKILL_NAVIGATION.md"
    rows = parse_skill_navigation(nav_path)
    if not nav_path.exists():
        report.error(
            "missing governance path: "
            ".maintain/docs/ai-collaboration/SKILL_NAVIGATION.md"
        )
        return
    duplicated = {skill: len(values) for skill, values in rows.items() if len(values) > 1}
    if duplicated:
        report.warn(
            ".maintain/docs/ai-collaboration/SKILL_NAVIGATION.md duplicate skill rows: "
            f"{sorted(duplicated.items())}"
        )
    for skill, values in sorted(rows.items()):
        for role, maturity in values:
            if role not in SKILL_NAV_ALLOWED_ROLES:
                report.warn(
                    ".maintain/docs/ai-collaboration/SKILL_NAVIGATION.md: "
                    f"{skill} has unknown role '{role}'"
                )
            if maturity not in SKILL_NAV_ALLOWED_MATURITY:
                report.warn(
                    ".maintain/docs/ai-collaboration/SKILL_NAVIGATION.md: "
                    f"{skill} has unknown maturity '{maturity}'"
                )


def check_task_archives(report: Report) -> None:
    live_path = DOCS_COLLAB / "TASKS.md"
    if not live_path.exists():
        return
    live_text = live_path.read_text(encoding="utf-8")
    archive_links = sorted(set(TASK_ARCHIVE_LINK_RE.findall(live_text)))
    for rel in archive_links:
        if not (REPO_ROOT / rel).exists():
            report.error(f"TASKS.md archive link missing target: {rel}")

    live_ids = {t["id"] for t in parse_tasks(live_text)}
    archive_ids: dict[str, str] = {}
    for archive in sorted((DOCS_COLLAB / "tasks").glob("*.md")):
        archive_text = archive.read_text(encoding="utf-8")
        archive_tasks = parse_tasks(archive_text)
        rel = str(archive.relative_to(REPO_ROOT))
        if archive_text.strip() and rel not in archive_links:
            report.warn(f"TASKS.md does not link non-empty task archive: {rel}")
        for task in archive_tasks:
            tid = task["id"]
            if tid in archive_ids:
                report.warn(f"task id {tid} appears in multiple archives: {archive_ids[tid]}, {rel}")
            archive_ids[tid] = rel
    duplicated = sorted(live_ids & set(archive_ids))
    if duplicated:
        report.warn(f"task ids duplicated between TASKS.md and archive files: {duplicated}")


def check_governance_files(report: Report) -> None:
    for name in GOVERNANCE_ROOT_FILES:
        p = REPO_ROOT / name
        if not p.exists():
            report.error(f"missing root governance file: {name}")
    for rel in GOVERNANCE_DOC_PATHS:
        p = REPO_ROOT / rel
        if not p.exists():
            report.error(f"missing governance path: {rel}")


def check_shell_scripts(report: Report) -> None:
    sh_files = sorted(REPO_ROOT.glob(".maintain/scripts/**/*.sh")) + sorted(
        SKILLS_DIR.glob("*/scripts/*.sh")
    )
    for sh in sh_files:
        try:
            subprocess.run(
                ["bash", "-n", str(sh)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            report.error(
                f"{sh.relative_to(REPO_ROOT)}: bash -n failed: {exc.stderr.strip() or exc.stdout.strip()}"
            )
        except FileNotFoundError:
            report.warn(f"{sh.relative_to(REPO_ROOT)}: bash not available, skipped syntax check")


TASK_HEADER_RE = re.compile(r"^##\s*\[[ xX]\]\s*(TASK-\d+)", re.MULTILINE)
H2_RE = re.compile(r"^##\s+", re.MULTILINE)
TASK_STATUS_RE = re.compile(r"当前状态[：:]\s*(.+)$", re.MULTILINE)
CR_ID_RE = re.compile(r"\bCR-\d+\b")


def parse_tasks(text: str) -> list[dict[str, str]]:
    """Split TASKS.md into task blocks and capture id + status."""
    tasks: list[dict[str, str]] = []
    headers = list(TASK_HEADER_RE.finditer(text))
    h2_positions = [m.start() for m in H2_RE.finditer(text)]
    for i, m in enumerate(headers):
        start = m.start()
        later_h2s = [pos for pos in h2_positions if pos > start]
        end = later_h2s[0] if later_h2s else len(text)
        block = text[start:end]
        tid = m.group(1)
        sm = TASK_STATUS_RE.search(block)
        status = sm.group(1).strip() if sm else ""
        tasks.append({"id": tid, "status": status, "block": block})
    return tasks


def scan_reflection_signals(report: Report) -> None:
    tasks_path = DOCS_COLLAB / "TASKS.md"
    review_dir = DOCS_COLLAB / "codex-reviews"

    ledger_text = tasks_path.read_text(encoding="utf-8") if tasks_path.exists() else ""
    review_text_by_file: dict[str, str] = {}
    if review_dir.exists():
        for rp in sorted(review_dir.glob("*.md")):
            review_text_by_file[str(rp.relative_to(REPO_ROOT))] = rp.read_text(encoding="utf-8")

    tasks = parse_tasks(ledger_text)
    task_text = "\n".join(t["block"] for t in tasks)
    review_text = "\n".join(review_text_by_file.values())
    combined_records = task_text + "\n" + review_text

    # Repeated CR IDs across task records + review files. This intentionally
    # ignores template/policy prose outside task blocks to avoid false signals.
    cr_counts: dict[str, int] = {}
    for match in CR_ID_RE.finditer(combined_records):
        cr_counts[match.group(0)] = cr_counts.get(match.group(0), 0) + 1
    repeated = {cr: n for cr, n in cr_counts.items() if n > 1}
    if repeated:
        report.signal(
            f"repeated CR IDs detected (update originals, do not duplicate): {sorted(repeated.items())}"
        )

    max_turn_tasks: list[str] = []
    blocked_tasks: list[str] = []
    repair_tasks: list[str] = []
    open_without_trajectory: list[str] = []

    for t in tasks:
        tid = t["id"]
        status = t["status"]
        block = t["block"]

        # Look for actual recorded outcomes, not enum values in the template.
        if re.search(r"claude_result:\s*max[- ]?turns", block, re.IGNORECASE) or re.search(
            r"agent brief.*max[- ]?turns|max[- ]?turns.*brief", block, re.IGNORECASE
        ):
            max_turn_tasks.append(tid)

        bm = re.search(r"blocker_type:\s*([^\n]+)", block, re.IGNORECASE)
        blocker_value = bm.group(1).strip().lower() if bm else ""
        if "阻塞" in status or (blocker_value and blocker_value not in {"none", "无"}):
            blocked_tasks.append(tid)

        if "需修改" in status or re.search(r"repair_loop_count:\s*[1-9]\d*|修复轮次:\s*[1-9]\d*|多轮修复:\s*是", block, re.IGNORECASE):
            repair_tasks.append(tid)

        if any(s in status for s in OPEN_TASK_STATUSES) and "trajectory:" not in block:
            open_without_trajectory.append(tid)

    if max_turn_tasks:
        report.signal(
            f"tasks with recorded max-turns/brief pressure: {max_turn_tasks} — "
            f"consider narrower Claude briefs or adjusted --max-turns"
        )
    if blocked_tasks:
        report.signal(
            f"tasks currently blocked or with non-none blocker_type: {blocked_tasks} — "
            f"review next_owner and unblock action"
        )
    if repair_tasks:
        report.signal(
            f"tasks with repair-loop/需修改 signals: {repair_tasks} — multi-round repair activity detected"
        )
    if open_without_trajectory:
        report.signal(
            f"open formal tasks without a trajectory block: {open_without_trajectory} — "
            f"add a trajectory record per templates/trajectory-record.md"
        )

    # Review files may still contain free-form max-turns/blocked/repair evidence.
    review_max_turn_files = [
        path for path, text in review_text_by_file.items() if re.search(r"max[- ]?turns", text, re.IGNORECASE)
    ]
    review_blocked_files = [
        path for path, text in review_text_by_file.items() if re.search(r"blocked|阻塞", text, re.IGNORECASE)
    ]
    review_repair_files = [
        path for path, text in review_text_by_file.items() if re.search(r"repair[- ]?loop|需修改", text, re.IGNORECASE)
    ]
    if review_max_turn_files:
        report.signal(f"review files mentioning max-turns: {review_max_turn_files}")
    if review_blocked_files:
        report.signal(f"review files mentioning blocked/阻塞: {review_blocked_files}")
    if review_repair_files:
        report.signal(f"review files mentioning repair-loop/需修改: {review_repair_files}")

    # Evidence-package recommendation heuristic.
    signals_present = bool(
        repeated
        or max_turn_tasks
        or blocked_tasks
        or repair_tasks
        or review_max_turn_files
        or review_blocked_files
        or review_repair_files
    )
    if signals_present:
        report.signal(
            "consider generating an evidence package "
            "(hercules-meta-skill-evolution/templates/evidence-package.md) and, if a "
            "recurring weakness is confirmed, patch the implicated workflow skill"
        )


def run_checks() -> Report:
    report = Report()
    skill_files = check_skill_frontmatter(report)
    check_linked_dirs(report)
    check_linked_file_references(report, skill_files)
    check_runtime_skill_scope(report)
    check_skill_navigation(report)
    check_task_archives(report)
    check_governance_files(report)
    check_shell_scripts(report)
    scan_reflection_signals(report)
    return report


def print_section(title: str, lines: list[str]) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)
    if lines:
        for line in lines:
            print(f"  - {line}")
    else:
        print("  (none)")


def render_text(report: Report, *, strict: bool) -> None:
    print_section("ERRORS", report.errors)
    print()
    print_section("WARNINGS", report.warnings)
    print()
    print_section("REFLECTION SIGNALS", report.signals)
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  errors:    {len(report.errors)}")
    print(f"  warnings:  {len(report.warnings)}")
    print(f"  signals:   {len(report.signals)}")
    print(f"  strict:    {strict}")
    print(f"  exit code: {report.exit_code(strict=strict)}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the Hercules skill pack.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as release-blocking failures (signals remain advisory)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = run_checks()
    if args.json:
        print(json.dumps(report.to_dict(strict=args.strict), ensure_ascii=False, indent=2))
    else:
        render_text(report, strict=args.strict)
    return report.exit_code(strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
