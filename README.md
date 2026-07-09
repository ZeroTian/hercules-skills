# Hercules Skills

[English](#english) | [中文](#中文)

A portable Hermes Agent skill pack for governed multi-agent software development.

Hercules turns the pattern below into reusable skills, scripts, ledgers, and review gates:

```text
Hermes orchestrates → Claude Code implements → Codex independently reviews → real commands verify
```

> Status: local working package with 25 tracked runtime skills, validator release gate, task ledger, Codex review records, and optional external-plugin governance.

---

## English

### What is Hercules Skills?

Hercules Skills is a portable workflow skill pack for [Hermes Agent](https://hermes-agent.nousresearch.com/). It is designed for developers who want Claude Code and Codex CLI to collaborate under a clear controller instead of operating as ad-hoc assistants.

The repository provides:

- reusable Hercules-owned Hermes skills under `skills/`;
- a lightweight command entry point at `scripts/hercules`;
- validation and packaging checks for the skill pack;
- a live task ledger and archived task history;
- independent Codex review records;
- governance rules for optional external agent plugins such as OpenAI `codex-plugin-cc`.

Hercules is a workflow layer, not a replacement for Claude Code, Codex CLI, Hermes Agent, or `codex-plugin-cc`.

### Why this project exists

Modern AI coding workflows can become hard to audit: one agent edits, another reviews, a shell command verifies, and the user has to remember who did what. Hercules makes that loop explicit:

| Actor | Responsibility |
|---|---|
| Hermes | Orchestrates, gathers context, delegates work, verifies outputs, updates ledgers. |
| Claude Code | Implements code/docs/refactors with scoped instructions. |
| Codex CLI | Performs independent review, risk checks, CR closure, and final acceptance. |
| Real commands | Provide executable evidence: validators, tests, shell syntax checks, package checks. |

For the positioning note comparing Hercules with OpenAI `codex-plugin-cc`, see [`docs/WHY_HERCULES.md`](docs/WHY_HERCULES.md).

### Key features

- **25 runtime skills** organized as entry skills, atoms, specialized atoms, and domain atoms.
- **Productized CLI helper**: `scripts/hercules setup`, `doctor`, `doctor --fix`, `validate`, `package`, `status`, and `bootstrap --check`.
- **Release gate**: `scripts/validate-skill-pack.py --strict` checks skill metadata, linked files, navigation drift, task archive integrity, and reflection signals.
- **Fresh-clone smoke test**: `scripts/smoke-fresh-clone.sh` validates staged-package portability.
- **Task governance**: `docs/ai-collaboration/TASKS.md` keeps active/recent work compact while `docs/ai-collaboration/tasks/archive-2026-07.md` preserves history.
- **Independent review trail**: Codex review records live under `docs/ai-collaboration/codex-reviews/`.
- **External-plugin boundary**: third-party agent plugins are treated as dependencies, not vendored source.

### Quickstart

### One-command install

For a fresh Linux/macOS/WSL machine, the installer can clone/update this repository, install Hermes if missing, install/link the Hercules skills, and run the dependency bootstrap.

Recommended full setup, including optional Claude plugins used by the full Hercules workflow:

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- --full
```

Minimal install without Claude plugin mutation:

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- --minimal
```

Preview first, with no installs, clones, pulls, registry writes, or symlink changes:

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- --dry-run
```

Local checkout equivalent:

```bash
scripts/hercules setup --full
scripts/hercules setup --minimal
scripts/hercules setup --dry-run
scripts/hercules doctor
scripts/hercules doctor --fix --full
```

The installer does not automate interactive auth. After it finishes, run `hermes setup`, `claude auth login --console`, or `codex login` if any of those are still missing. Use `scripts/hercules doctor` for a read-only dashboard of what is ready, fixable, or blocked.

From a checkout of this repository:

```bash
git clone https://github.com/ZeroTian/hercules-skills.git
cd hercules-skills

scripts/hercules status
scripts/hercules validate
scripts/hercules bootstrap --check
```

Use the helper as the lightweight product entry point:

```bash
scripts/hercules setup --full      # recommended full setup, including optional Claude plugins
scripts/hercules setup --dry-run   # preview-only install plan; no writes
scripts/hercules doctor            # read-only dashboard: OK/WARN/FIXABLE/BLOCKED
scripts/hercules doctor --fix      # repair minimal dependencies
scripts/hercules validate          # validator + whitespace diff check + bootstrap script syntax
scripts/hercules package           # staged package readiness; no commit or push
```

### Install into Hermes

Install Hermes first using the official Hermes installation flow.

Then copy this skill group into your Hermes skills directory:

```bash
mkdir -p ~/.hermes/skills/hercules
cp -a skills/. ~/.hermes/skills/hercules/
```

For active development, prefer a symlink so the Hermes runtime and this Git repository stay in sync:

```bash
ln -sfn /path/to/hercules-skills/skills ~/.hermes/skills/hercules
```

Start a new Hermes session and verify that the skills are visible:

```bash
hermes skills list | grep hercules
```

### Current Hercules-owned skills

The current runtime skill pack contains these tracked skills:

```text
agent-plugin-dependency-governance
coding-agent-orchestration
cross-agent-review-loop
evaluation-closed-loop-orchestration
godot-rl-metric-regression
godot-wsl-artifact-validation
hercules-agent-capability-preflight
hercules-collaborative-agent-workflow
hercules-meta-skill-evolution
hercules-project-init-workflow
hercules-skill-pack-management
hermes-collaborative-workflow
hermes-project-init-orchestration
iterative-agent-code-review
kanban-codex-lane
kanban-orchestrator
kanban-worker
open-ended-research-orchestration
open-source-project-packaging
portable-skill-pack-installation
cli-installer-ux-governance
skill-pack-governance-validation
skill-pack-roadmap-execution
staged-commit-package-governance
workflow-skill-pack-audit
```

For role/maturity navigation, see [`docs/ai-collaboration/SKILL_NAVIGATION.md`](docs/ai-collaboration/SKILL_NAVIGATION.md). For the full audit and composition map, see [`docs/ai-collaboration/SKILL_GROUP_AUDIT.md`](docs/ai-collaboration/SKILL_GROUP_AUDIT.md).

### Repository layout

```text
skills/                                  # Runtime Hercules skills
scripts/hercules                         # Productized helper entry point
scripts/validate-skill-pack.py           # Skill-pack validator and release gate
scripts/smoke-fresh-clone.sh             # Fresh-clone smoke validation
tests/                                   # Validator tests
docs/WHY_HERCULES.md                     # Positioning vs codex-plugin-cc
docs/ai-collaboration/TASKS.md           # Live collaboration ledger
docs/ai-collaboration/tasks/             # Archived task ledgers
docs/ai-collaboration/codex-reviews/     # Independent Codex review records
docs/ai-collaboration/SKILL_NAVIGATION.md# Skill role/maturity map
HERMES.md                                # Hermes orchestration rules
CLAUDE.md                                # Claude Code implementation rules
AGENTS.md                                # Codex review rules
```

### Validation

Run the standard validation bundle before submitting changes:

```bash
python3 tests/test_validate_skill_pack_cli.py -v
python3 scripts/validate-skill-pack.py --strict
scripts/hercules package
git diff --check
git diff --cached --check
```

`--strict` fails on structural warnings. Reflection signals remain advisory and are used to improve future workflow skills.

### External dependencies and third-party content

Hercules intentionally does **not** vendor Hermes built-in skills or third-party agent plugins.

Known external workflow dependencies include:

```text
subagent-driven-development
writing-plans
```

Claude plugins checked/installed by the bootstrap workflow only when `--optional` / `HERCULES_INSTALL_OPTIONAL=1` is set can include:

```text
superpowers
oh-my-claudecode
codex@openai-codex
```

OpenAI [`codex-plugin-cc`](https://github.com/openai/codex-plugin-cc) is treated as an optional external dependency (`codex@openai-codex`), not copied source. It is licensed upstream under Apache-2.0. Hercules records policy, safety classification, and bootstrap checks around it; upstream plugin code remains upstream.

### Contributing

Contributions should preserve the actor boundaries and validation discipline:

1. Keep README reader-facing; put long operating rules in `HERMES.md`, `CLAUDE.md`, `AGENTS.md`, or `docs/ai-collaboration/`.
2. Keep Hercules-owned skills under `skills/<skill>/SKILL.md`.
3. Do not vendor Hermes built-in skills or third-party plugins unless an explicit governance decision says otherwise.
4. Run the validation bundle before review.
5. Use independent Codex review for review-required governance changes.

### License

This repository is licensed under the MIT License. See [`LICENSE`](LICENSE).

Third-party tools, skills, and plugins remain under their own licenses. In particular, OpenAI `codex-plugin-cc` is Apache-2.0 upstream and is not vendored into this repository.

---

## 中文

### Hercules Skills 是什么？

Hercules Skills 是一套面向 [Hermes Agent](https://hermes-agent.nousresearch.com/) 的可迁移 workflow skill pack。它面向希望把 Claude Code 与 Codex CLI 纳入清晰编排、独立复核和真实验证闭环的开发者。

这个仓库提供：

- `skills/` 下的 Hercules 自有 Hermes skills；
- `scripts/hercules` 轻量命令入口；
- skill pack validator、package gate 和 fresh-clone smoke；
- live task ledger 与历史任务归档；
- 独立 Codex review 记录；
- 对 OpenAI `codex-plugin-cc` 等可选外部 agent plugin 的依赖治理边界。

Hercules 是 workflow layer，不替代 Claude Code、Codex CLI、Hermes Agent 或 `codex-plugin-cc`。

### 为什么需要它？

AI coding workflow 很容易变得不可审计：一个 agent 写代码，另一个 agent review，shell 命令做验证，最后用户要靠记忆判断哪些事情完成了。Hercules 把这个过程显式化：

| 角色 | 职责 |
|---|---|
| Hermes | 编排、收集上下文、分派 agent、验证输出、更新账本。 |
| Claude Code | 在明确范围内实现代码、文档、重构。 |
| Codex CLI | 独立 review、风险检查、CR closure、最终验收。 |
| 真实命令 | 提供可执行证据：validator、tests、shell syntax、package checks。 |

关于 Hercules 与 OpenAI `codex-plugin-cc` 的区别，见 [`docs/WHY_HERCULES.md`](docs/WHY_HERCULES.md)。

### 核心能力

- **25 个 runtime skills**：按 entry、atom、specialized atom、domain atom 组织。
- **产品化命令入口**：`scripts/hercules setup/doctor/doctor --fix/validate/package/status/bootstrap --check`。
- **发布门禁**：`scripts/validate-skill-pack.py --strict` 检查 skill metadata、linked files、导航漂移、任务归档完整性和 reflection signals。
- **fresh-clone smoke**：`scripts/smoke-fresh-clone.sh` 验证 staged package 可迁移性。
- **任务治理**：`TASKS.md` 保留活跃/近期任务，`tasks/archive-2026-07.md` 保留历史审计链路。
- **独立 review 轨迹**：Codex review records 位于 `docs/ai-collaboration/codex-reviews/`。
- **外部插件边界**：第三方 agent plugin 作为 dependency，不 vendor 源码。

### 快速开始

### 一键安装

在新的 Linux / macOS / WSL 机器上，可以用安装脚本自动 clone/update 仓库、安装缺失的 Hermes、安装/链接 Hercules skills，并运行依赖 bootstrap。

推荐完整安装，包括 Hercules workflow 使用的 optional Claude plugins：

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- --full
```

不改 Claude plugin 状态的最小安装：

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- --minimal
```

先预览，不安装、不 clone/pull、不写 registry、不改 symlink：

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- --dry-run
```

本地 checkout 中等价命令：

```bash
scripts/hercules setup --full
scripts/hercules setup --minimal
scripts/hercules setup --dry-run
scripts/hercules doctor
scripts/hercules doctor --fix --full
```

安装脚本不会自动完成交互式登录。如果结束后仍缺认证，请运行 `hermes setup`、`claude auth login --console` 或 `codex login`。使用 `scripts/hercules doctor` 可以查看只读仪表盘，区分已就绪、警告、可自动修复和必须手动处理的项。

```bash
git clone https://github.com/ZeroTian/hercules-skills.git
cd hercules-skills

scripts/hercules status
scripts/hercules validate
scripts/hercules bootstrap --check
```

常用命令：

```bash
scripts/hercules setup --full      # 推荐完整安装，包括 optional Claude plugins
scripts/hercules setup --dry-run   # 只预览安装计划，不写入
scripts/hercules doctor            # 只读仪表盘：OK/WARN/FIXABLE/BLOCKED
scripts/hercules doctor --fix      # 修复最小依赖
scripts/hercules validate          # validator + whitespace diff check + bootstrap script syntax
scripts/hercules package           # staged package readiness；不 commit / 不 push
```

### 安装到 Hermes

先按 Hermes 官方流程安装 Hermes。

然后复制 skill group：

```bash
mkdir -p ~/.hermes/skills/hercules
cp -a skills/. ~/.hermes/skills/hercules/
```

如果是开发本仓库，建议使用 symlink：

```bash
ln -sfn /path/to/hercules-skills/skills ~/.hermes/skills/hercules
```

启动新的 Hermes session 后验证：

```bash
hermes skills list | grep hercules
```

### 当前 Hercules 自有 skills

当前 runtime skill pack 包含这些 tracked skills：

```text
agent-plugin-dependency-governance
coding-agent-orchestration
cross-agent-review-loop
evaluation-closed-loop-orchestration
godot-rl-metric-regression
godot-wsl-artifact-validation
hercules-agent-capability-preflight
hercules-collaborative-agent-workflow
hercules-meta-skill-evolution
hercules-project-init-workflow
hercules-skill-pack-management
hermes-collaborative-workflow
hermes-project-init-orchestration
iterative-agent-code-review
kanban-codex-lane
kanban-orchestrator
kanban-worker
open-ended-research-orchestration
open-source-project-packaging
portable-skill-pack-installation
cli-installer-ux-governance
skill-pack-governance-validation
skill-pack-roadmap-execution
staged-commit-package-governance
workflow-skill-pack-audit
```

角色与成熟度导航见 [`docs/ai-collaboration/SKILL_NAVIGATION.md`](docs/ai-collaboration/SKILL_NAVIGATION.md)。完整审计与组合图见 [`docs/ai-collaboration/SKILL_GROUP_AUDIT.md`](docs/ai-collaboration/SKILL_GROUP_AUDIT.md)。

### 仓库结构

```text
skills/                                  # Runtime Hercules skills
scripts/hercules                         # 产品化 helper 入口
scripts/validate-skill-pack.py           # skill-pack validator / release gate
scripts/smoke-fresh-clone.sh             # fresh-clone smoke validation
tests/                                   # validator tests
docs/WHY_HERCULES.md                     # 与 codex-plugin-cc 的定位对比
docs/ai-collaboration/TASKS.md           # live collaboration ledger
docs/ai-collaboration/tasks/             # 历史任务归档
docs/ai-collaboration/codex-reviews/     # 独立 Codex review records
docs/ai-collaboration/SKILL_NAVIGATION.md# skill role/maturity map
HERMES.md                                # Hermes 编排规则
CLAUDE.md                                # Claude Code 实现规则
AGENTS.md                                # Codex review 规则
```

### 验证

提交变更前建议运行：

```bash
python3 tests/test_validate_skill_pack_cli.py -v
python3 scripts/validate-skill-pack.py --strict
scripts/hercules package
git diff --check
git diff --cached --check
```

`--strict` 会把结构性 warning 作为 release blocker；reflection signals 仍是 advisory，用于推动后续 workflow skill 改进。

### 外部依赖与第三方内容

Hercules 不 vendor Hermes builtin skills，也不默认 vendor 第三方 agent plugins。

已知外部 workflow dependencies：

```text
subagent-driven-development
writing-plans
```

bootstrap 可检查的 optional Claude plugins 包括：

```text
superpowers
oh-my-claudecode
codex@openai-codex
```

OpenAI [`codex-plugin-cc`](https://github.com/openai/codex-plugin-cc) 在 Hercules 中被视为 optional external dependency（`codex@openai-codex`），不是 vendored source。它上游采用 Apache-2.0 license。Hercules 只沉淀围绕它的治理策略、安全边界和 bootstrap 检查；上游插件源码仍保留在上游。

### 贡献指南

贡献时请保持 actor boundary 和验证纪律：

1. README 保持 reader-facing；长规则放到 `HERMES.md`、`CLAUDE.md`、`AGENTS.md` 或 `docs/ai-collaboration/`。
2. Hercules 自有 skills 放在 `skills/<skill>/SKILL.md`。
3. 不 vendor Hermes builtin skills 或第三方 plugins，除非有明确治理决策。
4. review 前运行验证命令。
5. 需要验收的治理变更使用独立 Codex review。

### 开源协议

本仓库采用 MIT License，见 [`LICENSE`](LICENSE)。

第三方工具、skills、plugins 保留其各自 license。尤其是 OpenAI `codex-plugin-cc` 上游是 Apache-2.0，本仓库没有 vendor 它的源码。
