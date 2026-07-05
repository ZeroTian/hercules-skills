# Tasks

This file is the live collaboration ledger for the Hercules skills repository.

Status values:

```text
待处理 / 处理中 / 阻塞 / 待复核 / 需修改 / 已完成 / 已取消
```

Owners:

```text
Hermes / Claude / Codex / 用户 / 无
```

## [x] TASK-001：Review visible untracked skill candidates

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；round-2 候选处置已完成并经 Codex PASS 复核
- 是否需要 Codex 复核：是
- 创建日期：2026-07-05
- 最后更新：2026-07-05 12:50
- 来源：项目初始化预览 + 技能组审计（SKILL_GROUP_AUDIT.md）
- 关联任务：TASK-003
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md`
- 验证证据：`git status --short -uall` 起初显示六个 visible-untracked 候选；本轮将 `hercules-skill-pack-management` 与 `workflow-skill-pack-audit` 保留在 `skills/` 并 staged 为 core skill，将 `real-game-closed-loop-validation`、`game-mechanics-telemetry-validation`、`repository-governance-initialization`、`scoped-codex-review-packets` 移至 `docs/ai-collaboration/candidate-skills/<skill>/SKILL.md`；`python3 scripts/validate-skill-pack.py` 输出 0 errors、0 warnings、0 signals；Codex final review PASS（highest severity: none）
- 阻塞原因：无

### 目标

确认六个未跟踪 skill 是否属于 Hercules skill pack 的正式内容，并对每个候选给出纳入/不纳入/合并/归档的理由。

### 执行项

- [x] 读取每个候选 skill 的内容和 frontmatter
- [x] 判断是否符合 Hercules-owned workflow skill 范围
- [x] 对 `hercules-skill-pack-management`：提升为 intended core atom（仓库布局/symlink/迁移/同步/隐私检查），保留在 `skills/`
- [x] 对 `workflow-skill-pack-audit`：提升为 intended core atom（技能组审计/validator/重检工作流），保留在 `skills/`
- [x] 对 `real-game-closed-loop-validation`：归档到 `docs/ai-collaboration/candidate-skills/`，不纳入核心；若后续推广为核心或领域 pack，需先补齐或移除断开的 `references/godot-rl-stage2-optimizer.md` 链接
- [x] 对 `game-mechanics-telemetry-validation`：归档到 `docs/ai-collaboration/candidate-skills/`，作为 game/RL 领域候选与 `real-game-closed-loop-validation` 一并保留
- [x] 对 `repository-governance-initialization`：归档为重复/案例研究候选；若后续推广，需先补齐或移除断开的 `references/hercules-skills-governance-init-2026-07-05.md` 链接，或先将独有步骤合并进 `hermes-project-init-orchestration/references/`
- [x] 对 `scoped-codex-review-packets`：归档到 `docs/ai-collaboration/candidate-skills/`，作为 review-loop 家族重叠候选；后续推广前先确认是否合并进 `coding-agent-orchestration` / `iterative-agent-code-review`
- [x] 更新 README 当前核心技能列表（加入 `workflow-skill-pack-audit`）与归档候选说明
- [x] 更新 ARCHITECTURE 当前核心技能目录与归档候选说明
- [x] 更新 SKILL_GROUP_AUDIT.md 反映 15 核心 skill + 4 归档候选 + 组合图 + 下一步
- [x] 新增 `docs/ai-collaboration/candidate-skills/README.md` 说明归档原因与推广路径
- [x] 运行 `python3 scripts/validate-skill-pack.py`（0 errors, 0 warnings, 0 signals）
- [x] 提交 Codex 复核

### 验收标准

- [x] 已明确每个候选纳入、归档或合并的理由
- [x] README 与实际 tracked/staged skill 列表一致
- [x] Codex 已完成复核

### Trajectory

```yaml
trajectory:
  task_id: TASK-001
  attempt: 2
  date: 2026-07-05
  task_type: review
  skill_versions:
    hercules-collaborative-agent-workflow: 1.0.0
    workflow-skill-pack-audit: 1.0.0
    hercules-skill-pack-management: 1.0.0
  score: 1.0
  actor_path: "Hermes -> Claude reconcile -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned
    relevant_capabilities: ["superpowers", "oh-my-claudecode", "skill-creator"]
    effort: xhigh
    claude_result: completed
    codex_result: PASS
    verification:
      commands: ["git status --short -uall", "git ls-files 'skills/*/SKILL.md' | sort", "find skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort", "python3 scripts/validate-skill-pack.py", "git diff --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"]
      logs: ["docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"]
      diff_scope: "skills/ (4 candidates moved), docs/ai-collaboration/candidate-skills/, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/TASKS.md, README.md"
    cr_ids: []
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-001"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"
    logs: []
```

## [x] TASK-002：Add lightweight repository validation script or documented check command

- 当前状态：已完成
- 优先级：P2
- 当前负责人：无
- 下一负责人：无
- 下一步：无；validator 已通过并经 Codex PASS 复核
- 是否需要 Codex 复核：是
- 创建日期：2026-07-05
- 最后更新：2026-07-05 11:50
- 来源：项目初始化预览 + 技能组审计
- 关联任务：TASK-003
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md`
- 验证证据：`scripts/validate-skill-pack.py` 已创建并运行通过（round 2 after staging core skills: 0 errors, 0 warnings, 0 reflection signals）；Codex final review PASS（highest severity: none）
- 阻塞原因：无

### 目标

为 skill pack 提供可重复的轻量验证入口，避免每次人工拼接检查命令。

### 执行项

- [x] 盘点现有技能结构和 linked files
- [x] 确定最小验证范围
- [x] 创建 `scripts/validate-skill-pack.py`（stdlib only），记录等价静态检查证据
- [x] 更新 HERMES.md 与 README.md 验证入口
- [x] 提交 Codex 复核

### 验收标准

- [x] 验证入口清晰可运行
- [x] 不引入不必要依赖
- [x] Codex 已完成复核

### Trajectory

```yaml
trajectory:
  task_id: TASK-002
  attempt: 1
  date: 2026-07-05
  task_type: implementation
  skill_versions:
    hercules-collaborative-agent-workflow: 1.0.0
    hercules-meta-skill-evolution: 1.0.0
  score: 1.0
  actor_path: "Hermes -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned
    relevant_capabilities: []
    effort: xhigh
    claude_result: completed
    codex_result: PASS
    verification:
      commands: ["python3 scripts/validate-skill-pack.py", "git diff --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"]
      logs: ["docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"]
      diff_scope: "scripts/validate-skill-pack.py, HERMES.md, README.md, docs/ai-collaboration/*"
    cr_ids: []
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-002"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"
    logs: []
```

## [x] TASK-003：Skill-group audit and validation infrastructure

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；技能组审计、trajectory 接入、validator 与 round-2 reconciliation 已经 Codex PASS 复核
- 是否需要 Codex 复核：是
- 创建日期：2026-07-05
- 最后更新：2026-07-05 11:50
- 来源：用户需求（深度审计技能组 + 连接 TASKS 与轨迹记录 + 轻量验证/反思脚本）
- 关联任务：TASK-001, TASK-002
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md`
- 验证证据：`docs/ai-collaboration/SKILL_GROUP_AUDIT.md` 已创建并更新到 round 2；`scripts/validate-skill-pack.py` 运行通过（0 errors, 0 warnings, 0 reflection signals）；`git diff --check` 通过；Codex final review PASS（highest severity: none）
- 阻塞原因：无

### 目标

深度审计 Hercules 技能组的冗余/原子性，定义有机组合图，连接 TASKS 与轨迹记录，并提供可运行的验证/反思脚本。

### 执行项

- [x] Round 1：盘点 13 个 tracked skill + 5 个 visible untracked 候选
- [x] Round 2：形成 15 个 core skill（13 原有 + `hercules-skill-pack-management` + `workflow-skill-pack-audit`）并将 4 个非核心候选归档
- [x] 分类 entry / atom / specialized atom / candidate-duplicate
- [x] 识别冗余与重叠（collaborative-workflow 对、project-init 三元组、review-loop 家族）
- [x] 定义有机组合图：init → preflight → execution → review → trajectory → evidence → patch → validation
- [x] 创建 `docs/ai-collaboration/SKILL_GROUP_AUDIT.md`
- [x] 创建 `scripts/validate-skill-pack.py`（stdlib only）
- [x] 在 TASKS.md 添加 Trajectory record policy 与 trajectory block
- [x] 更新 HERMES.md 验证命令、README.md 验证入口与核心技能列表
- [x] 提交 Codex 复核

### 验收标准

- [x] 审计文档覆盖 inventory、分类、冗余分析、组合图、可运行缺口、下一步行动
- [x] 验证脚本可运行且仅对结构错误非零退出
- [x] TASKS 模板包含 trajectory block 字段
- [x] README/ARCHITECTURE 与 tracked/staged skill 列表一致
- [x] Codex 已完成复核

### Trajectory

```yaml
trajectory:
  task_id: TASK-003
  attempt: 1
  date: 2026-07-05
  task_type: docs
  skill_versions:
    hercules-collaborative-agent-workflow: 1.0.0
    hercules-meta-skill-evolution: 1.0.0
    hercules-agent-capability-preflight: 1.0.0
  score: 1.0
  actor_path: "Hermes -> Claude audit+implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned
    relevant_capabilities: ["superpowers", "oh-my-claudecode", "skill-creator"]
    effort: xhigh
    claude_result: completed
    codex_result: PASS
    verification:
      commands: ["python3 scripts/validate-skill-pack.py", "git diff --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"]
      logs: ["docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"]
      diff_scope: "docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/TASKS.md, scripts/validate-skill-pack.py, HERMES.md, README.md"
    cr_ids: []
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-003"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"
    logs: []
```

## [x] TASK-004：Practice skill-pack usability smoke test

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；当前 runtime 可用性已完成 smoke test，fresh clone / fresh machine 测试等待 commit/push 后执行
- 是否需要 Codex 复核：否（本任务只记录 smoke-test 证据；round-2 reconciliation 已经 Codex PASS）
- 创建日期：2026-07-05
- 最后更新：2026-07-05 13:10
- 来源：用户追问“是否有实践过技能组的可用性”
- 关联任务：TASK-001, TASK-002, TASK-003
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md`
- 验证证据：`docs/ai-collaboration/USABILITY_VALIDATION.md` 记录 runtime symlink、15 core skills、archived candidate not loaded、validator/static checks、bootstrap audit-only，以及实际 Hermes→Claude→Hermes verify→Codex→TASKS closure 链路
- 阻塞原因：无

### 目标

确认当前 Hercules skill pack 不是只完成文档整理，而是在 live runtime 中具备基本可用性证据。

### 执行项

- [x] 检查 `~/.hermes/skills/hercules` symlink 解析到 `/mnt/e/code/hercules-skills/skills`
- [x] 对比 runtime visible skills 与 tracked/staged core skill 列表
- [x] 确认 archived candidate 位于非 runtime 路径
- [x] 用 `skill_view` 成功加载代表性 core skills
- [x] 用 `skill_view` 确认 `real-game-closed-loop-validation` 归档后不再作为 live skill 加载
- [x] 运行 validator/static checks
- [x] 运行 `HERCULES_CHECK_ONLY=1` bootstrap/dependency doctor
- [x] 写入 `docs/ai-collaboration/USABILITY_VALIDATION.md`

### 验收标准

- [x] runtime 目录与 15 core skill 预期一致
- [x] validator 输出 0 errors / 0 warnings / 0 signals
- [x] bootstrap audit-only 成功完成
- [x] 已明确未覆盖的 fresh clone / fresh machine 测试

### Trajectory

```yaml
trajectory:
  task_id: TASK-004
  attempt: 1
  date: 2026-07-05
  task_type: validation
  skill_versions:
    workflow-skill-pack-audit: 1.1.0
    hercules-skill-pack-management: 1.0.0
    hercules-agent-capability-preflight: 1.0.0
  score: 0.8
  actor_path: "Hermes smoke test -> validator/static checks -> bootstrap audit-only -> report"
  phi:
    capability_preflight: scanned
    relevant_capabilities: ["skill_view", "bootstrap audit-only", "validator"]
    effort: high
    claude_result: not-launched
    codex_result: skipped-with-reason-current-smoke-test-only
    verification:
      commands: ["readlink -f ~/.hermes/skills/hercules", "find skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort", "git ls-files 'skills/*/SKILL.md' | sort", "python3 scripts/validate-skill-pack.py", "git diff --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"]
      logs: ["docs/ai-collaboration/USABILITY_VALIDATION.md"]
      diff_scope: "docs/ai-collaboration/USABILITY_VALIDATION.md, docs/ai-collaboration/README.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/TASKS.md"
    cr_ids: []
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-004"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md"
    logs: ["docs/ai-collaboration/USABILITY_VALIDATION.md"]
```

## [x] TASK-005：Promote skill-pack-governance-validation to core skill

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；round-3 staged package 已经 Codex PASS，等待用户确认 commit/push
- 是否需要 Codex 复核：是
- 创建日期：2026-07-05
- 最后更新：2026-07-05
- 来源：用户选择 option 1，将已存在的 untracked skill `skills/skill-pack-governance-validation/SKILL.md` 正式提升为 Hercules core skill（round-3 promotion，源自已实践的 usability/commit-package 接受工作流）
- 关联任务：TASK-001, TASK-003, TASK-004
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-05-round3-governance-validation.md`
- 验证证据：clone-copy 验证已对 commit `97f78ca` 实践（clone HEAD = `97f78cacbc107f02b918576fdddc053388eab95d`，validator 0 errors / 0 warnings / 0 signals，bootstrap audit-only `[hercules-bootstrap] done`）；Hermes 已补齐 `skill-pack-governance-validation` 引用文件并将无关 game telemetry candidate 归档到非 runtime 路径；最终验证 `python3 scripts/validate-skill-pack.py` = 0 errors / 0 warnings / 0 signals，`git diff --cached --check` / `git diff --check` / `bash -n` 均通过，staged privacy scan 无命中；Codex final review PASS（highest severity: none）
- 阻塞原因：无

### 目标

将 `skill-pack-governance-validation` 从 untracked 候选正式纳入 Hercules core skill pack，更新 README / ARCHITECTURE / SKILL_GROUP_AUDIT / USABILITY_VALIDATION / TASKS 一致性，并将 clone-copy 验证实践固化为该 skill 的接受证据。

### 执行项

- [x] 在 README.md 核心技能列表加入 `skill-pack-governance-validation` 并更新 prose（16 skills, round-3 promotion）
- [x] 在 docs/ai-collaboration/ARCHITECTURE.md 核心技能目录加入该 skill 并更新 prose
- [x] 在 docs/ai-collaboration/SKILL_GROUP_AUDIT.md 更新核心数量（15→16）、分类表、组合图 validation+audit 分支、practical usability 段、verification 段、prioritized actions
- [x] 在 docs/ai-collaboration/USABILITY_VALIDATION.md 记录 commit `97f78ca` 的 clone-copy 验证证据，并标注新 skill 固化该实践
- [x] 新增 TASK-005 条目（待复核，owner Codex）
- [x] 补齐 `skills/skill-pack-governance-validation/references/usability-and-commit-package-validation.md`
- [x] 将无关 `game-telemetry-closed-loop-validation` domain candidate 归档到 `docs/ai-collaboration/candidate-skills/`
- [x] Hermes 暂存 `skills/skill-pack-governance-validation/SKILL.md` 及引用文件并运行最终验证
- [x] Codex 独立复核

### 验收标准

- [x] README / ARCHITECTURE 核心列表与 runtime visible skills 一致（16 skills）
- [x] validator 0 errors / 0 warnings / 0 signals
- [x] `skill-pack-governance-validation` referenced files exist
- [x] unrelated game telemetry domain candidate preserved outside runtime loading
- [x] clone-copy 验证证据真实可复现
- [x] fresh-machine clean install 与 new-project use 仍未覆盖（如实记录）
- [x] Codex 已完成复核

### Claude 执行记录

- 修改内容：将 `skill-pack-governance-validation` 正式提升为 core skill；更新核心列表 15→16；更新组合图 validation+audit 分支；记录 commit `97f78ca` clone-copy 验证证据；新增 TASK-005；Hermes 补齐该 skill 的引用文件并将无关 game telemetry domain candidate 归档到非 runtime 路径
- 修改文件：README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/USABILITY_VALIDATION.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/candidate-skills/README.md, docs/ai-collaboration/candidate-skills/game-telemetry-closed-loop-validation/SKILL.md, skills/skill-pack-governance-validation/SKILL.md, skills/skill-pack-governance-validation/references/usability-and-commit-package-validation.md
- 验证命令：`python3 scripts/validate-skill-pack.py`, `git diff --check`, `bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, clone-copy validation 对 commit `97f78ca`
- 验证结果：Claude 交付时本地 validator 0 errors / 3 warnings（新 core skill 未暂存 + 无关 game telemetry candidate 在 runtime 路径）；Hermes 随后补齐引用文件并归档无关 domain candidate，最终验证 0 errors / 0 warnings / 0 signals；`git diff --cached --check`、`git diff --check`、`bash -n` 通过；staged privacy scan 无命中
- 遗留问题：无已知引用缺口；fresh-machine clean install 与 new-project use 仍未覆盖，需后续单独验证

### Codex 复核记录

- 复核日期：2026-07-05
- 复核范围：round-3 promotion 一致性、clone-copy 证据真实性、references 缺口处置
- 复核结果：PASS；初审 P3 `CR-R3-001` / `CR-R3-002` 已修复，recheck 无 findings
- 遗留风险：本轮不覆盖 fresh-machine clean install 与 new-project use；提交/推送需用户确认

### Trajectory

```yaml
trajectory:
  task_id: TASK-005
  attempt: 1
  date: 2026-07-05
  task_type: docs
  skill_versions:
    skill-pack-governance-validation: 1.0.0
    workflow-skill-pack-audit: 1.0.0
    hercules-skill-pack-management: 1.0.0
    hercules-agent-capability-preflight: 1.0.0
  score: 1.0
  actor_path: "Hermes -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: ["superpowers", "oh-my-claudecode"]
    effort: high
    claude_result: completed
    codex_result: PASS
    verification:
      commands: ["python3 scripts/validate-skill-pack.py", "git diff --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "rm -rf /tmp/hercules-skills-smoke && mkdir -p /tmp/hercules-skills-smoke && git clone https://github.com/ZeroTian/hercules-skills.git /tmp/hercules-skills-smoke/hercules-skills && cd /tmp/hercules-skills-smoke/hercules-skills && git rev-parse HEAD && python3 scripts/validate-skill-pack.py && HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"]
      logs: ["docs/ai-collaboration/USABILITY_VALIDATION.md"]
      diff_scope: "README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/USABILITY_VALIDATION.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/candidate-skills/README.md, docs/ai-collaboration/candidate-skills/game-telemetry-closed-loop-validation/SKILL.md, skills/skill-pack-governance-validation/"
    cr_ids: []
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-005"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-05-round3-governance-validation.md"
    logs: ["docs/ai-collaboration/USABILITY_VALIDATION.md"]
```

## Trajectory record policy

Every formal Claude/Codex collaboration task in this ledger should be able to leave reflection data. Use the trajectory shape from `skills/hercules-meta-skill-evolution/templates/trajectory-record.md`.

Minimal fields to capture per attempt:

```yaml
trajectory:
  task_id: TASK-NNN
  attempt: <int>
  date: YYYY-MM-DD
  task_type: implementation | review | research | project-init | debugging | docs | other
  skill_versions: {}
  score: provisional   # 1.0 / 0.8 / 0.6 / 0.3 / 0.0, or blank until judged
  actor_path: "Hermes -> Claude -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned | cached | skipped-with-reason
    relevant_capabilities: []
    effort: high | xhigh | other
    claude_result: not-launched | completed | max-turns | failed
    codex_result: not-launched | PASS | FAIL | BLOCKED
    verification:
      commands: []
      logs: []
      diff_scope: ""
    cr_ids: []
    blocker_type: none | scope | test | tool | external | unclear
    next_owner: Hermes | Claude | Codex | User | none
  source_pointers:
    task_record: "path#anchor"
    review_record: "path#anchor"
    logs: []
```

Rules:

- Add the block as a `### Trajectory` subsection at the end of each task record.
- Keep records compact. Link to logs instead of pasting them. Do not record secrets, tokens, cookies, or private paths.
- Scores are provisional sorting hints, not objective truth. If a field is unknown, write `unknown` or omit it; do not invent evidence.
- The validation script (`scripts/validate-skill-pack.py`) flags open formal tasks that lack a trajectory block as a reflection signal (non-failing).
- When repeated CR IDs, `max-turns`, `blocked/阻塞`, or `repair-loop/需修改` signals accumulate, consider generating an evidence package via `skills/hercules-meta-skill-evolution/templates/evidence-package.md` and patching only the implicated workflow module.

## Task template

```markdown
## [ ] TASK-XXX：任务标题

- 当前状态：待处理
- 优先级：P1
- 当前负责人：Claude
- 下一负责人：Codex
- 下一步：完成实现和自检后提交复核
- 是否需要 Codex 复核：是
- 创建日期：YYYY-MM-DD
- 最后更新：YYYY-MM-DD HH:mm
- 来源：用户需求 / 项目初始化 / Codex 审阅
- 关联任务：无
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：无

### 目标

说明可验证的预期结果。

### 执行项

- [ ] 完成必要调研
- [ ] 确认影响范围
- [ ] 拆分 SDD 垂直切片并记录子代理/插件使用计划或不可用原因
- [ ] 按 TDD 写失败测试并记录 RED 结果，或记录不可测试原因与替代验证
- [ ] 完成获批的实现或修改
- [ ] 记录 GREEN 结果并完成必要 REFACTOR
- [ ] 补充或更新测试
- [ ] 更新相关文档
- [ ] 执行验证并记录结果
- [ ] 完成 Claude 自检
- [ ] 完成交接信息
- [ ] 完成 Codex 复核

### 验收标准

- [ ] 需求已经满足
- [ ] SDD/TDD 证据完整且真实
- [ ] 相关验证已经通过
- [ ] 文档与实现一致
- [ ] 没有未说明的遗留风险
- [ ] Codex 已完成复核

### Claude 执行记录

- 修改内容：
- 修改文件：
- 验证命令：
- 验证结果：
- 遗留问题：

### Codex 复核记录

- 复核日期：
- 复核范围：
- 复核结果：
- 遗留风险：

### Trajectory

```yaml
trajectory:
  task_id: TASK-XXX
  attempt: 1
  date: YYYY-MM-DD
  task_type: implementation
  skill_versions: {}
  score: provisional
  actor_path: "Hermes -> Claude -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned | cached | skipped-with-reason
    relevant_capabilities: []
    effort: high
    claude_result: not-launched | completed | max-turns | failed
    codex_result: not-launched | PASS | FAIL | BLOCKED
    verification:
      commands: []
      logs: []
      diff_scope: ""
    cr_ids: []
    blocker_type: none
    next_owner: Codex
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-xxx"
    review_record: "暂无"
    logs: []
```
