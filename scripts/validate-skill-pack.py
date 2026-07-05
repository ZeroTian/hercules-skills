#!/usr/bin/env python3
"""Lightweight Hercules skill-pack validator and reflection scanner.

Runs with Python stdlib only. Checks:
  - frontmatter presence and required fields (name, description, version) for skills/*/SKILL.md
  - description length <= 1024 characters
  - linked file directories are only references/templates/scripts/assets
  - README and ARCHITECTURE tracked skill lists vs git tracked skills and visible skill dirs
  - governance files exist
  - shell scripts pass `bash -n`
  - ledger reflection signals from TASKS.md and codex-reviews/*.md:
    repeated CR IDs, max-turns/max turns, blocked/阻塞, repair-loop/需修改,
    missing trajectory blocks for open formal tasks, and whether an evidence
    package should be considered.

Output sections: ERRORS, WARNINGS, REFLECTION SIGNALS, SUMMARY.
Exit nonzero only for structural errors (ERRORS non-empty). Warnings and
reflection signals do not fail the command by default.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_COLLAB = REPO_ROOT / "docs" / "ai-collaboration"

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
    "docs/ai-collaboration/README.md",
    "docs/ai-collaboration/TASKS.md",
    "docs/ai-collaboration/ARCHITECTURE.md",
    "docs/ai-collaboration/PROJECT_AUDIT.md",
    "docs/ai-collaboration/codex-reviews",
    "docs/ai-collaboration/decisions",
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


def extract_skill_list_from_doc(path: Path) -> set[str]:
    """Pull skill names out of fenced code blocks that list one skill per line."""
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    names: set[str] = set()
    in_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            continue
        token = stripped.split("#", 1)[0].strip()
        if re.match(r"^[a-z][a-z0-9-]*$", token):
            names.add(token)
    return names


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


def check_skill_lists(report: Report) -> None:
    readme_skills = extract_skill_list_from_doc(REPO_ROOT / "README.md")
    arch_skills = extract_skill_list_from_doc(DOCS_COLLAB / "ARCHITECTURE.md")
    tracked = git_tracked_skills()
    visible = visible_skill_dirs()

    # Filter doc-extracted sets to plausible skill names that actually exist as dirs.
    readme_skills = readme_skills & visible if visible else readme_skills
    arch_skills = arch_skills & visible if visible else arch_skills

    if tracked and tracked != visible:
        untracked_visible = visible - tracked
        tracked_missing_dir = tracked - visible
        if untracked_visible:
            report.warn(
                f"visible skill directories not tracked by git: {sorted(untracked_visible)}"
            )
        if tracked_missing_dir:
            report.error(
                f"git-tracked skills without a visible SKILL.md directory: {sorted(tracked_missing_dir)}"
            )

    if readme_skills and tracked and not readme_skills.issuperset(tracked):
        missing_from_readme = tracked - readme_skills
        report.warn(f"README skill list missing tracked skills: {sorted(missing_from_readme)}")
    if readme_skills and tracked:
        extra_in_readme = readme_skills - tracked
        if extra_in_readme:
            report.warn(f"README lists skills not tracked by git: {sorted(extra_in_readme)}")

    if arch_skills and tracked and not arch_skills.issuperset(tracked):
        missing_from_arch = tracked - arch_skills
        report.warn(f"ARCHITECTURE skill list missing tracked skills: {sorted(missing_from_arch)}")
    if arch_skills and tracked:
        extra_in_arch = arch_skills - tracked
        if extra_in_arch:
            report.warn(f"ARCHITECTURE lists skills not tracked by git: {sorted(extra_in_arch)}")


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
    sh_files = sorted(REPO_ROOT.glob("scripts/**/*.sh")) + sorted(SKILLS_DIR.glob("*/scripts/*.sh"))
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


def main() -> int:
    report = Report()
    check_skill_frontmatter(report)
    check_linked_dirs(report)
    check_skill_lists(report)
    check_governance_files(report)
    check_shell_scripts(report)
    scan_reflection_signals(report)

    print("=" * 60)
    print("ERRORS")
    print("=" * 60)
    if report.errors:
        for line in report.errors:
            print(f"  - {line}")
    else:
        print("  (none)")

    print()
    print("=" * 60)
    print("WARNINGS")
    print("=" * 60)
    if report.warnings:
        for line in report.warnings:
            print(f"  - {line}")
    else:
        print("  (none)")

    print()
    print("=" * 60)
    print("REFLECTION SIGNALS")
    print("=" * 60)
    if report.signals:
        for line in report.signals:
            print(f"  - {line}")
    else:
        print("  (none)")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  errors:    {len(report.errors)}")
    print(f"  warnings:  {len(report.warnings)}")
    print(f"  signals:   {len(report.signals)}")
    print(f"  exit code: {1 if report.errors else 0}")

    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
