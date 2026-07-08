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
    claude_result: timeout-after-edits-verified-by-Hermes
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

## [x] TASK-006：P0+P1 skill-pack convergence (post-task skill merge + owner-dispatch dedup)

- 当前状态：已完成
- 优先级：P0
- 当前负责人：无
- 下一负责人：无
- 下一步：无；P0/P1 收敛包已经 Codex recheck PASS
- 是否需要 Codex 复核：是
- 创建日期：2026-07-05
- 最后更新：2026-07-05
- 来源：用户需求（基于 SKILL_GROUP_DEEP_RESEARCH_2026-07-05.md 的 P0/P1 优先级，执行收敛而非 P2 重构）
- 关联任务：TASK-005
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-05-task006-p0-p1-convergence.md`
- 验证证据：`python3 scripts/validate-skill-pack.py` 输出 0 errors / 0 warnings / 0 signals；`git diff --check` 通过；`bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` 通过；`git status --short -uall` 显示 6 个已修改 tracked skill、ARCHITECTURE/TASKS 文档更新、1 个 untracked 研究记录，`post-task-memory-skill-evolution` 目录已移除；Codex 初审 P3 `CR-T006-001` / `CR-T006-002` 已修复，recheck PASS
- 阻塞原因：无

### 目标

在不触发 P2 重构的前提下，消除 untracked `post-task-memory-skill-evolution` 引发的 validator 警告，并将四个技能中重复的 owner-driven auto-dispatch 长文与嵌入的 review contract JSON 去重，使核心技能数回到 16、validator 回到 0 errors / 0 warnings / 0 signals。

### 执行项

- [x] 将 post-task memory-vs-skill 决策内容合并进 `skills/hercules-meta-skill-evolution/SKILL.md`（新增 Post-Task Memory vs Skill Decision 段 + checklist 项）
- [x] 将治理类 pitfalls 合并进 `skills/skill-pack-governance-validation/SKILL.md`（P3 restaging + narrow recheck、缺失引用文件、三类证据桶）
- [x] 删除 `skills/post-task-memory-skill-evolution/` 独立目录
- [x] 以 `hermes-collaborative-workflow#Owner-Driven Auto-Dispatch` 为权威，将 `hercules-collaborative-agent-workflow`、`coding-agent-orchestration`、`cross-agent-review-loop` 中的重复长文替换为短指针，保留必要 checklist 行
- [x] 将 `coding-agent-orchestration` 与 `cross-agent-review-loop` 中嵌入的 review contract JSON 替换为指向 `skills/hercules-meta-skill-evolution/templates/codex-review-contract.md` 的指针
- [x] 保留 owner-driven dispatch 原则：ledger 中 `当前负责人` / `下一负责人` / `next_owner` 是可执行路由信号，Hermes 直接启动 Claude/Codex 而非让用户手动运行
- [x] 运行 `python3 scripts/validate-skill-pack.py`、`git diff --check`、`bash -n` 静态检查
- [x] 完成 Codex 复核

### 验收标准

- [x] `skills/post-task-memory-skill-evolution/` 已移除，核心技能数为 16
- [x] validator 输出 0 errors / 0 warnings / 0 signals
- [x] owner-driven auto-dispatch 长文仅存在于 `hermes-collaborative-workflow`，其余三个技能为短指针
- [x] review contract JSON 仅存在于 `templates/codex-review-contract.md`，SKILL.md 文件中不再嵌入
- [x] post-task 技能的独有概念（memory vs skill 边界、patch loaded skills first、frustration 双信号、避免 one-off 窄技能、session 细节入 references）已保留在 meta-skill-evolution
- [x] 治理 pitfalls 已保留在 governance-validation
- [x] 未触及 P2 范围（未合并 cross-agent-review-loop、未拆分 project-init、未做大重构）
- [x] Codex 已完成复核

### Claude 执行记录

- 修改内容：P0 合并 post-task memory-vs-skill 决策进 meta-skill-evolution、治理 pitfalls 进 governance-validation、删除独立 post-task 目录；P1 将三个技能的 owner-dispatch 长文替换为指向 hermes-collaborative-workflow 的短指针、将两处嵌入 JSON 替换为指向 codex-review-contract 模板的指针；新增 TASK-006 并在研究记录中标注 P0/P1 已实现
- 修改文件：skills/hercules-meta-skill-evolution/SKILL.md, skills/skill-pack-governance-validation/SKILL.md, skills/hermes-collaborative-workflow/SKILL.md, skills/hercules-collaborative-agent-workflow/SKILL.md, skills/coding-agent-orchestration/SKILL.md, skills/cross-agent-review-loop/SKILL.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/SKILL_GROUP_DEEP_RESEARCH_2026-07-05.md
- 删除文件：skills/post-task-memory-skill-evolution/SKILL.md（untracked，独有内容已合并）
- 验证命令：`python3 scripts/validate-skill-pack.py`, `git diff --check`, `bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, `git status --short -uall`
- 验证结果：validator 0 errors / 0 warnings / 0 signals；`git diff --check` 通过；`bash -n` 通过；`git status` 显示 6 个已修改 tracked skill、ARCHITECTURE/TASKS 文档更新和 1 个 untracked 研究记录，post-task 目录已移除
- 遗留问题：无 P2 重构；commit/push 需用户明确授权

### Codex 复核记录

- 复核日期：2026-07-05
- 复核范围：P0/P1 收敛包（post-task skill 合并/移除、owner-dispatch 去重、review-contract JSON 去重、TASK-006 账本一致性、ARCHITECTURE stale wording）
- 复核结果：PASS；初审 P3 `CR-T006-001` / `CR-T006-002` 已修复，Codex recheck 无新 findings
- 遗留风险：P2 重构未执行；fresh-machine clean install 与 new-project use 仍未覆盖；commit/push 需用户明确授权

### Trajectory

```yaml
trajectory:
  task_id: TASK-006
  attempt: 1
  date: 2026-07-05
  task_type: docs
  skill_versions:
    hercules-meta-skill-evolution: 1.0.0
    skill-pack-governance-validation: 1.0.0
    hermes-collaborative-workflow: 1.0.0
  score: 1.0
  actor_path: "Hermes -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned
    relevant_capabilities: ["superpowers", "oh-my-claudecode"]
    effort: high
    claude_result: completed
    codex_result: PASS
    verification:
      commands: ["python3 scripts/validate-skill-pack.py", "git diff --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "git status --short -uall"]
      logs: ["docs/ai-collaboration/codex-reviews/2026-07-05-task006-p0-p1-convergence.md"]
      diff_scope: "skills/hercules-meta-skill-evolution/SKILL.md, skills/skill-pack-governance-validation/SKILL.md, skills/hermes-collaborative-workflow/SKILL.md, skills/hercules-collaborative-agent-workflow/SKILL.md, skills/coding-agent-orchestration/SKILL.md, skills/cross-agent-review-loop/SKILL.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/SKILL_GROUP_DEEP_RESEARCH_2026-07-05.md"
    cr_ids: ["CR-T006-001", "CR-T006-002"]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-006"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-05-task006-p0-p1-convergence.md"
    logs: ["docs/ai-collaboration/codex-reviews/2026-07-05-task006-p0-p1-convergence.md"]
```

## [x] TASK-007：Absorb OpenAI codex-plugin-cc as optional external Claude plugin dependency + governance policy

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；Codex recheck PASS，等待用户明确授权 commit/push（如需要）
- 是否需要 Codex 复核：是
- 创建日期：2026-07-07
- 最后更新：2026-07-07
- 来源：用户需求（吸收 OpenAI `openai/codex-plugin-cc` 为可选外部 Claude 插件依赖 + Hercules-owned 治理策略，不 vendor 上游源码）
- 关联任务：无
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-07-task007-codex-plugin-cc-absorption.md`
- 验证证据：Hermes 复跑验证：`bash -n` 通过；`python3 scripts/validate-skill-pack.py` 0 errors / 1 warning（预存在的 6 个 untracked 候选目录，非本任务引入）/ 2 reflection signals（记录本任务 Claude max-turns 事实）；`git diff --check` 通过；`HERCULES_CHECK_ONLY=1` bootstrap audit-only 完成；`NPM_REGISTRY=https://example.invalid HERCULES_CHECK_ONLY=1` mutation proof 显示 npm registry before/after unchanged；Codex 初审 P2 `CR-T007-001` 已修复，recheck PASS
- 阻塞原因：无

### 目标

将 `openai/codex-plugin-cc` 作为可选外部 Claude Code 插件依赖纳入 Hercules skill pack，并以 Hercules-owned 治理策略约束其 `/codex:*` 命令边界，不 vendor 上游插件源码。

### 执行项

- [x] 调研结论：partial absorb（依赖 + 策略，不 vendor 源码）
- [x] bootstrap：新增 `openai-codex` marketplace（`openai/codex-plugin-cc`），`HERCULES_INSTALL_OPTIONAL=1` 时安装 `codex@openai-codex`，新增 codex 插件 cache 深度盘点
- [x] preflight skill：更新依赖表、可选安装文档、Claude 能力扫描、边界分类、pitfalls
- [x] cross-agent-review-loop：新增可选 inline/preliminary 渠道段落，要求 `/codex:rescue` 显式授权
- [x] README / ARCHITECTURE：提及 `codex-plugin-cc` 为可选外部 Claude 插件依赖
- [x] 研究记录：`docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md`
- [x] 静态检查：`bash -n`、`python3 scripts/validate-skill-pack.py`、`git diff --check`、`HERCULES_CHECK_ONLY=1` bootstrap audit-only
- [x] 完成 Codex 复核

### 验收标准

- [x] 未 vendor 上游插件源码
- [x] 默认不安装 `codex@openai-codex`，仅 `HERCULES_INSTALL_OPTIONAL=1` 安装
- [x] 边界分类明确：`/codex:review` + `/codex:adversarial-review` 只读；`/codex:rescue` 默认 write-capable；stop-gate 默认关闭
- [x] Hermes-owned 独立最终 Codex 复核未被插件渠道替代
- [x] validator 0 errors；`bash -n` / `git diff --check` 通过
- [x] Codex 已完成复核

### Claude 执行记录

- 修改内容：吸收 `codex-plugin-cc` 为可选外部依赖 + 治理策略；bootstrap 新增 marketplace/可选安装/深度盘点；preflight 更新依赖表/能力扫描/边界分类/pitfalls；cross-agent-review-loop 新增 inline 渠道段落；README/ARCHITECTURE 提及；新增研究记录与 TASK-007
- 修改文件：`skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, `skills/hercules-agent-capability-preflight/SKILL.md`, `skills/cross-agent-review-loop/SKILL.md`, `README.md`, `docs/ai-collaboration/ARCHITECTURE.md`, `docs/ai-collaboration/TASKS.md`, `docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md`
- 验证命令：`bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, `python3 scripts/validate-skill-pack.py`, `git diff --check`, `HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`
- 验证结果：Hermes 复跑确认 `bash -n` OK；validator 0 errors / 1 warning（预存在 untracked 候选目录）/ 2 reflection signals（由本任务如实记录 Claude max-turns 触发）；`git diff --check` OK；`HERCULES_CHECK_ONLY=1` bootstrap audit-only 完成，codex 插件 cache 未找到以 warn 报告（可选插件未安装），未执行任何安装
- 遗留问题：codex 插件未在本机安装（可选），深度盘点将以 warn 形式报告 cache not found；commit/push 需用户明确授权

### Codex 复核记录

- 复核日期：2026-07-07
- 复核范围：codex-plugin-cc optional dependency boundary, bootstrap check-only/install gating, preflight/cross-agent policy, README/ARCHITECTURE/TASKS consistency
- 复核结果：PASS；初审 P2 `CR-T007-001`（`HERCULES_CHECK_ONLY=1` 仍会写 npm/pnpm registry）已修复，recheck 无剩余 findings
- 遗留风险：`codex@openai-codex` 未在本机安装（可选）；当前工作树仍有 TASK-007 范围外的既有修改/未跟踪候选；commit/push 需用户明确授权

### Trajectory

```yaml
trajectory:
  task_id: TASK-007
  attempt: 1
  date: 2026-07-07
  task_type: docs
  skill_versions:
    hercules-agent-capability-preflight: 1.0.0
    cross-agent-review-loop: 1.0.0
  score: 1.0
  actor_path: "Hermes -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: scanned
    relevant_capabilities: ["superpowers", "oh-my-claudecode"]
    effort: xhigh
    claude_result: max-turns-after-edits
    codex_result: PASS
    verification:
      commands: ["bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "python3 scripts/validate-skill-pack.py", "git diff --check", "HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"]
      logs: ["docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md"]
      diff_scope: "skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh, skills/hercules-agent-capability-preflight/SKILL.md, skills/cross-agent-review-loop/SKILL.md, README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md"
    cr_ids: ["CR-T007-001"]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-007"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-07-task007-codex-plugin-cc-absorption.md"
    logs: ["docs/ai-collaboration/CODEX_PLUGIN_CC_RESEARCH_2026-07-07.md"]
```

## [x] TASK-008：P0 round-4 skill-pack reconciliation (promote 4 atoms, archive 3 loop variants, fold unique detail)

- 当前状态：已完成
- 优先级：P0
- 当前负责人：无
- 下一负责人：无
- 下一步：无；Codex recheck PASS，等待用户明确授权 commit/push（如需要）
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：用户需求（优化 Hercules skill pack；P0 清理：协调 7 个 visible-untracked 候选 + 固化 TASK-007 codex-plugin-cc 吸收状态）
- 关联任务：TASK-007
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-08-task008-round4-skill-pack-reconciliation.md`
- 验证证据：Hermes 已暂存 intended TASK-007/TASK-008 package（排除既有未暂存 `real-godot-closed-loop-validation.md` 用户改动）；`python3 scripts/validate-skill-pack.py` 0 errors / 0 warnings / 2 reflection signals（TASK-007 max-turns 既有信号）；`git diff --check` 与 `git diff --cached --check` 通过；`bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` 通过；`HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` 通过；staged filename/content privacy scan 通过；4 个提升技能 `skill_view` 可加载，`artifact-driven-evaluation-loops` 不再 runtime-load
- 阻塞原因：无

### 目标

将 7 个 visible-untracked 候选协调为干净、有文档的状态：4 个提升为 Hercules-owned runtime 技能，3 个重叠候选在折叠独有细节后归档；保持 README/ARCHITECTURE/AUDIT/candidate-skills 一致；不触及 TASK-007 既有成果与无关用户改动。

### 处置表

| # | Candidate | Disposition | Rationale |
|---|---|---|---|
| A | `agent-plugin-dependency-governance` | PROMOTE/TRACK (core atom) | 外部 Claude/Codex/agent 插件依赖治理核心原子；TASK-007 已实践其策略，本技能一般化该策略。 |
| B | `evaluation-closed-loop-orchestration` | PROMOTE/TRACK (core atom) | 评估系统闭环的规范宽原子；吸收 3 个重叠候选的独有细节后作为唯一闭环原子。 |
| C | `godot-wsl-artifact-validation` | PROMOTE/TRACK (specialized domain atom) | WSL+Windows Godot 工件证据领域原子；填补 broad 闭环未覆盖的具体证据质量缺口。 |
| D | `godot-rl-metric-regression` | PROMOTE/TRACK (specialized domain atom) | baseline-vs-candidate Godot/RL 指标回归领域原子；填补 Godot/RL 回归证据缺口。 |
| E | `artifact-driven-evaluation-loops` | ARCHIVE (overlap/reference) | 与 `evaluation-closed-loop-orchestration` 重叠；BLOCKED 结果 + 字段保留契约已折叠进规范原子。 |
| F | `artifact-handoff-orchestration` | ARCHIVE (overlap/reference) | 与 `evaluation-closed-loop-orchestration` 重叠；safe-anchor 校验清单已折叠进规范原子。 |
| G | `autonomous-evaluation-loops` | ARCHIVE (overlap/reference) | 与 `evaluation-closed-loop-orchestration` 重叠；modification-request schema + instance-vs-system 区分已折叠进规范原子。 |

### 执行项

- [x] 读取 7 个候选 SKILL.md、README、ARCHITECTURE、AUDIT、candidate-skills/README、validator
- [x] 折叠 3 个待归档候选的独有细节进 `evaluation-closed-loop-orchestration/SKILL.md`（BLOCKED 结果、字段保留、safe-anchor 校验清单、owner 路由信号）
- [x] 更新 4 个提升技能的 `related_skills`（移除指向归档候选的引用）
- [x] 创建 3 个 reference 文件（issue-to-handoff-closed-loop.md、godot-wsl-artifact-probes.md、combat-gate-regression.md）
- [x] 移动 3 个重叠候选到 `docs/ai-collaboration/candidate-skills/<skill>/SKILL.md` 并移除 runtime 目录
- [x] 更新 README、ARCHITECTURE 核心技能列表与计数（16→20）及归档候选说明（5→8）
- [x] 更新 SKILL_GROUP_AUDIT.md（round 4、清单、分类表、冗余分析、组合图、runnable gaps、prioritized actions、验证段）
- [x] 更新 candidate-skills/README.md（表格 + layout）
- [x] 新增 TASK-008 条目（待复核，owner Codex）
- [x] Hermes 暂存 4 个提升技能 + reference 文件并复跑最终 validator
- [x] Codex 独立复核

### 验收标准

- [x] README / ARCHITECTURE 核心列表与 runtime visible skills 一致（20 skills）
- [x] 3 个重叠候选已移出 `skills/`，归档于 `docs/ai-collaboration/candidate-skills/`
- [x] `evaluation-closed-loop-orchestration` 含 BLOCKED 结果、字段保留、safe-anchor 校验清单、owner 路由信号
- [x] 3 个 reference 文件存在且被对应 SKILL.md 引用
- [x] validator 0 errors / 0 warnings after staging intended package
- [x] `git diff --check` / `git diff --cached --check` / `bash -n` / bootstrap audit-only / privacy scan 通过
- [x] 未暂存既有无关 `real-godot-closed-loop-validation.md` 改动；TASK-007 既有成果保留
- [x] Codex 已完成复核

### Claude 执行记录

- 修改内容：round-4 协调——4 候选提升（agent-plugin-dependency-governance、evaluation-closed-loop-orchestration、godot-wsl-artifact-validation、godot-rl-metric-regression），3 重叠候选归档（artifact-driven-evaluation-loops、artifact-handoff-orchestration、autonomous-evaluation-loops）；折叠独有细节进 evaluation-closed-loop-orchestration；创建 3 个 reference 文件；更新 README/ARCHITECTURE/AUDIT/candidate-skills 一致性与计数（16→20，归档 5→8）；更新 4 提升技能 related_skills；新增 TASK-008
- 修改文件：README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/candidate-skills/README.md, docs/ai-collaboration/TASKS.md, skills/agent-plugin-dependency-governance/SKILL.md, skills/evaluation-closed-loop-orchestration/SKILL.md, skills/evaluation-closed-loop-orchestration/references/issue-to-handoff-closed-loop.md, skills/godot-wsl-artifact-validation/SKILL.md, skills/godot-wsl-artifact-validation/references/godot-wsl-artifact-probes.md, skills/godot-rl-metric-regression/SKILL.md, skills/godot-rl-metric-regression/references/combat-gate-regression.md
- 移动文件：skills/artifact-driven-evaluation-loops/SKILL.md → docs/ai-collaboration/candidate-skills/artifact-driven-evaluation-loops/SKILL.md；skills/artifact-handoff-orchestration/SKILL.md → docs/ai-collaboration/candidate-skills/artifact-handoff-orchestration/SKILL.md；skills/autonomous-evaluation-loops/SKILL.md → docs/ai-collaboration/candidate-skills/autonomous-evaluation-loops/SKILL.md
- 验证命令：`python3 scripts/validate-skill-pack.py`, `git diff --check`, `git diff --cached --check`, `bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, `HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, staged privacy scan
- 验证结果：Hermes 暂存 intended package 后复跑，validator 0 errors / 0 warnings / 2 reflection signals；diff checks、bash -n、bootstrap audit-only、staged privacy scan 均通过；4 个提升技能均已暂存且 runtime-load 成功；`artifact-driven-evaluation-loops` 不再 runtime-load
- 遗留问题：fresh-clone 验证未覆盖；commit/push 需用户明确授权；既有未暂存 `real-godot-closed-loop-validation.md` 改动明确排除在本 package 外

### Codex 复核记录

- 复核日期：2026-07-08
- 复核范围：staged TASK-007/TASK-008 package；skill count/list/disposition；TASK-007 optional codex-plugin policy；TASK-008 ledger truth；staging boundary and privacy
- 初审结果：FAIL/P2 — `CR-T008-001`，TASK-008 ledger 有陈旧暂存/验证文字（遗漏 `agent-plugin-dependency-governance`、仍称 4 个提升技能未暂存、trajectory 写 Hermes verify pending）
- 处理：Hermes 修正 TASK-008 修改文件、遗留问题、trajectory actor_path/verification/codex_result 字段并复跑验证；Codex recheck PASS
- 最终结果：PASS，无剩余 findings
- 遗留风险：fresh-clone 验证未覆盖；commit/push 需用户明确授权

### Trajectory

```yaml
trajectory:
  task_id: TASK-008
  attempt: 1
  date: 2026-07-08
  task_type: docs
  skill_versions:
    workflow-skill-pack-audit: 1.0.0
    evaluation-closed-loop-orchestration: 1.0.0
    agent-plugin-dependency-governance: 1.0.0
  score: 0.8
  actor_path: "Hermes -> Claude reconcile -> Hermes verify -> Codex initial review -> Hermes repair -> Codex recheck"
  phi:
    capability_preflight: scanned
    relevant_capabilities: ["superpowers", "oh-my-claudecode"]
    effort: xhigh
    claude_result: timeout-after-edits-verified-by-Hermes
    codex_result: PASS-after-CR-T008-001
    verification:
      commands: ["python3 scripts/validate-skill-pack.py", "git diff --check", "git diff --cached --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "staged privacy scan"]
      logs: ["/tmp/hercules_task008_bootstrap_checkonly.log", "/tmp/hercules_task008_staged_files.txt"]
      diff_scope: "README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/candidate-skills/README.md, docs/ai-collaboration/TASKS.md, skills/evaluation-closed-loop-orchestration/, skills/godot-wsl-artifact-validation/, skills/godot-rl-metric-regression/, skills/agent-plugin-dependency-governance/, docs/ai-collaboration/candidate-skills/{artifact-driven-evaluation-loops,artifact-handoff-orchestration,autonomous-evaluation-loops}/"
    cr_ids: ["CR-T008-001"]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-008"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-08-task008-round4-skill-pack-reconciliation.md"
    logs: []
```

## [x] TASK-009：P0 residual cleanup before push (Godot reference edit + staged-package governance candidate)

- 当前状态：已完成
- 优先级：P0
- 当前负责人：无
- 下一负责人：无
- 下一步：无；Codex recheck PASS，等待用户明确授权 commit/push（如需要）
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（P0 clean/push-ready 收敛后的残留项）
- 关联任务：TASK-008
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-08-task009-residual-cleanup.md`
- 验证证据：Hermes 已暂存 intended TASK-009 package；`python3 scripts/validate-skill-pack.py` 0 errors / 0 warnings / 3 reflection signals（TASK-007 max-turns 既有信号 + TASK-010..013 open blocked）；`git diff --check` 与 `git diff --cached --check` 通过；`bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` 通过；`HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh` 通过；staged filename/content privacy scan 通过；`staged-commit-package-governance` reference 可通过 `skill_view` 加载；Codex 初审 P2 `CR-T009-001` 已修复，recheck PASS；commit 前发现 accidental duplicate `staged-package-ledger-governance` 未跟踪目录，已吸收其 stale-text search pattern into `staged-commit-package-governance` 并移除 duplicate，validator 回到 0 warnings
- 阻塞原因：无

### 目标

让仓库重新达到可明确描述的 clean/push-ready 状态：当前已提交 TASK-008，但仍有一个未暂存 Godot reference 改动和一个未跟踪 `staged-commit-package-governance` skill candidate，需要单独处置。

### 处置表

| # | Residual | Disposition | Rationale |
|---|---|---|---|
| A | `skills/staged-commit-package-governance/SKILL.md` | PROMOTE/TRACK (core atom) | 捕获 round-4 staged-package boundary / ledger-truth / narrow Codex recheck 模式；与 `skill-pack-governance-validation` 互补而非冗余；补齐 `references/round4-staged-package-boundary.md`。 |
| B | `skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md` | KEEP/TRACK (reference improvement) | 3 条 durable Godot validation 新增（`/tmp` 日志及时复制、combat gate 伪改善判别、animation-driven hitbox 时序链）；作为独立 reference 改进纳入 TASK-009 package，不删除不重写。 |

### 执行项

- [x] 读取两个残留项并判断是否属于同一 package（同一 TASK-009 package，disposition 不同）
- [x] 决定 `staged-commit-package-governance`：PROMOTE/TRACK core atom；补齐 `references/round4-staged-package-boundary.md`；调整 Overview 措辞以互补 `skill-pack-governance-validation`
- [x] 决定 `real-godot-closed-loop-validation.md`：KEEP/TRACK 作为独立 reference 改进
- [x] 更新 README / ARCHITECTURE / SKILL_GROUP_AUDIT 核心技能列表与计数（20→21）
- [x] 更新 TASKS / OPTIMIZATION_ROADMAP 反映实际 disposition
- [x] 运行 validator、`git diff --check`
- [x] Hermes 暂存 intended TASK-009 package 并复跑 `git diff --cached --check`、staged privacy scan、bootstrap audit-only
- [x] Codex 复核 staged TASK-009 package

### 验收标准

- [x] 两个残留项均有明确 disposition
- [x] `staged-commit-package-governance` 作为正常 runtime skill 出现且 linked files 有效
- [x] README/ARCHITECTURE/AUDIT skill counts/lists 与 21 runtime skills 一致
- [x] validator 0 errors / 0 warnings after staging intended package
- [x] `git diff --check` / `git diff --cached --check` / `bash -n` / bootstrap audit-only / privacy scan 通过
- [x] 任务记录说明 committed / staged / unstaged / unpushed 状态
- [x] Codex 已复核需要复核的 package

### Claude 执行记录

- 修改内容：promote `staged-commit-package-governance` 为 core atom（补齐 `references/round4-staged-package-boundary.md`、调整 Overview 措辞以互补 `skill-pack-governance-validation`）；KEEP `real-godot-closed-loop-validation.md` 3 条 Godot validation 新增作为独立 reference 改进；更新 README/ARCHITECTURE/AUDIT 核心技能列表与计数（20→21）；更新 TASKS/OPTIMIZATION_ROADMAP TASK-009 disposition
- 补充处置：commit 前发现 accidental duplicate `skills/staged-package-ledger-governance/SKILL.md`；吸收其 stale future/backlog text search pattern into `staged-commit-package-governance`，删除 duplicate runtime directory，避免再次产生 visible-untracked warning
- 修改文件：skills/staged-commit-package-governance/SKILL.md, skills/staged-commit-package-governance/references/round4-staged-package-boundary.md, README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/OPTIMIZATION_ROADMAP.md
- KEEP/TRACK reference improvement：skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md（3 条 durable Godot validation 新增纳入本 package）
- 验证命令：`python3 scripts/validate-skill-pack.py`, `git diff --check`, `git diff --cached --check`, `bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, `HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh`, staged privacy scan, `skill_view(staged-commit-package-governance, references/round4-staged-package-boundary.md)`
- 验证结果：Hermes 暂存 intended package 后复跑，validator 0 errors / 0 warnings / 3 reflection signals；diff checks、bash -n、bootstrap audit-only、staged privacy scan 均通过；`staged-commit-package-governance` reference 可通过 `skill_view` 加载；`git status` 仅显示 staged TASK-009 package
- 遗留问题：fresh-clone 验证未覆盖；commit/push 需用户明确授权

### Codex 复核记录

- 复核日期：2026-07-08
- 复核范围：staged TASK-009 package；21-skill count/list consistency；`staged-commit-package-governance` promotion; Godot reference guidance; TASKS/roadmap truth; staging boundary and privacy
- 初审结果：PASS overall / P2 `CR-T009-001` — TASK-012 backlog text still referred to the pre-TASK-009 20-skill pack
- 处理：Hermes 将 TASK-012 roadmap/ledger wording改为 count-neutral “current core skill pack”，修正 TASK-009 trajectory truth，并恢复 TASK-002 误改字段；Codex recheck PASS
- 最终结果：PASS，无剩余 findings
- 遗留风险：fresh-clone 验证未覆盖；commit/push 需用户明确授权

### Trajectory

```yaml
trajectory:
  task_id: TASK-009
  attempt: 1
  date: 2026-07-08
  task_type: docs
  skill_versions:
    staged-commit-package-governance: 1.0.0
    skill-pack-governance-validation: 1.0.0
  score: 0.8
  actor_path: "Hermes -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: xhigh
    claude_result: timeout-after-edits-verified-by-Hermes
    codex_result: PASS-after-CR-T009-001
    verification:
      commands: ["python3 scripts/validate-skill-pack.py", "git diff --check", "git diff --cached --check", "bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh", "staged privacy scan", "skill_view reference load"]
      logs: ["/tmp/hercules_task009_bootstrap_checkonly.log"]
      diff_scope: "skills/staged-commit-package-governance/SKILL.md, skills/staged-commit-package-governance/references/round4-staged-package-boundary.md, skills/hercules-collaborative-agent-workflow/references/real-godot-closed-loop-validation.md, README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/OPTIMIZATION_ROADMAP.md"
    cr_ids: ["CR-T009-001"]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-009"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-08-task009-residual-cleanup.md"
    logs: []
```

## [ ] TASK-010：P1 productized entry + README landing

- 当前状态：待处理
- 优先级：P1
- 当前负责人：User
- 下一负责人：Hermes
- 下一步：用户选择启动后，Hermes/Claude 设计 `scripts/hercules` wrapper 与 README landing 改写
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（codex-plugin-cc 对比：入口简单、可执行命令面）
- 关联任务：TASK-008
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：等待 TASK-009 或用户明确跳过残留项后启动

### 目标

降低外部用户的上手成本：提供 `scripts/hercules` 命令入口和 reader-facing README landing，让用户不用先理解全部治理文档也能跑通 validate/bootstrap/status/package/doctor。

### 执行项

- [ ] 设计 `scripts/hercules` 子命令：`validate`, `bootstrap --check`, `status`, `package`, `doctor`
- [ ] 实现 shell wrapper 并保持无外部依赖
- [ ] README 第一屏改为价值主张 + 三步 quickstart + 典型 Hermes→Claude→Codex→verification 流程
- [ ] 运行 shell syntax、validator、wrapper 子命令 smoke tests
- [ ] Codex 复核 CLI/README 是否降低入口门槛且不削弱治理边界

### 验收标准

- [ ] `scripts/hercules validate` 运行 validator、diff check、bootstrap script syntax check，并返回正确 exit code
- [ ] `scripts/hercules bootstrap --check` 运行 audit-only bootstrap，不安装 optional plugin
- [ ] README 保持 reader-facing，不复制长规则
- [ ] validator / diff checks / shell syntax 通过
- [ ] Codex review PASS

### Trajectory

```yaml
trajectory:
  task_id: TASK-010
  attempt: 1
  date: 2026-07-08
  task_type: implementation
  skill_versions:
    writing-plans: 1.1.0
  score: provisional
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: not-launched
    codex_result: not-launched
    verification:
      commands: []
      logs: []
      diff_scope: "scripts/hercules, README.md"
    cr_ids: []
    blocker_type: scope
    next_owner: User
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-010"
    review_record: "暂无"
    logs: []
```

## [ ] TASK-011：P1/P2 validator release gate + fresh-clone smoke

- 当前状态：待处理
- 优先级：P1
- 当前负责人：User
- 下一负责人：Hermes
- 下一步：用户选择启动后，Hermes/Claude 增强 validator 与 migration smoke tooling
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（发布门禁与可迁移证明）
- 关联任务：TASK-010
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：等待用户选择启动

### 目标

把 `scripts/validate-skill-pack.py` 从结构检查升级为可供 Hermes/Codex/CI 消费的 release gate，并增加 fresh-clone smoke proof。

### 执行项

- [ ] 增加 `--json` 输出
- [ ] 增加 `--strict` 模式
- [ ] 增加 untracked candidate disposition 检查
- [ ] 增加 `references/` / `templates/` / `scripts/` 深度链接检查
- [ ] 新增 `scripts/smoke-fresh-clone.sh` 或等价 repo-level smoke script
- [ ] 为 validator/smoke 增加可运行验证和 Codex review

### 验收标准

- [ ] JSON 输出可机器解析
- [ ] strict mode 对 release-blocking warning 失败
- [ ] fresh-clone smoke 使用临时目录，不修改源 repo
- [ ] 当前 repo normal validation 通过；strict 例外如有必须记录
- [ ] Codex review PASS

### Trajectory

```yaml
trajectory:
  task_id: TASK-011
  attempt: 1
  date: 2026-07-08
  task_type: implementation
  skill_versions:
    skill-pack-governance-validation: 1.0.0
  score: provisional
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: not-launched
    codex_result: not-launched
    verification:
      commands: []
      logs: []
      diff_scope: "scripts/validate-skill-pack.py, scripts/smoke-fresh-clone.sh"
    cr_ids: []
    blocker_type: scope
    next_owner: User
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-011"
    review_record: "暂无"
    logs: []
```

## [ ] TASK-012：P2 skill information architecture + TASKS scaling

- 当前状态：待处理
- 优先级：P2
- 当前负责人：User
- 下一负责人：Hermes
- 下一步：用户选择启动后，Hermes/Claude 设计 skill role metadata、组合图与 TASKS archive split
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（core skill pack 导航与 ledger 可维护性）
- 关联任务：TASK-011
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：等待用户选择启动

### 目标

让当前核心 skill pack 更易导航，并降低 `TASKS.md` 长期膨胀带来的上下文成本。

### 执行项

- [ ] 定义 role/maturity metadata：entry / atom / specialized / archived 等
- [ ] 更新组合图和 skill 分类说明
- [ ] 设计并实施 TASKS active/archive split，如 `docs/ai-collaboration/tasks/archive-2026-07.md`
- [ ] 更新 validator 可检查的分类一致性
- [ ] Codex 复核 ledger truth 未丢失

### 验收标准

- [ ] 新用户能区分 entry skills 与 atoms
- [ ] 主 TASKS 只保留 active/recently closed，历史任务可回溯
- [ ] archive 链接和 review records 不断链
- [ ] validator 通过
- [ ] Codex review PASS

### Trajectory

```yaml
trajectory:
  task_id: TASK-012
  attempt: 1
  date: 2026-07-08
  task_type: docs
  skill_versions:
    workflow-skill-pack-audit: 1.1.0
  score: provisional
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: not-launched
    codex_result: not-launched
    verification:
      commands: []
      logs: []
      diff_scope: "docs/ai-collaboration/TASKS.md, docs/ai-collaboration/tasks/, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, scripts/validate-skill-pack.py"
    cr_ids: []
    blocker_type: scope
    next_owner: User
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-012"
    review_record: "暂无"
    logs: []
```

## [ ] TASK-013：P2/P3 external absorption workflow + WHY_HERCULES outreach package

- 当前状态：待处理
- 优先级：P2
- 当前负责人：User
- 下一负责人：Hermes
- 下一步：用户选择启动后，Hermes/Claude 将 `codex-plugin-cc` 研究吸收流程产品化，并产出对外说明
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（让“研究某 repo 能否吸收到技能组”可复用；对外传播）
- 关联任务：TASK-007, TASK-008
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：等待用户选择启动

### 目标

把 `codex-plugin-cc` 研究/吸收流程沉淀为标准工作流，并用 `docs/WHY_HERCULES.md` 讲清 Hercules 与 `codex-plugin-cc` 的定位差异。

### 执行项

- [ ] 将 external repo/plugin absorption workflow 写入 `agent-plugin-dependency-governance` 或 `open-ended-research-orchestration`
- [ ] 输出标准决策字段：dependency-vs-vendor、risks、bootstrap changes、governance boundary、validation evidence、Codex review
- [ ] 新增 `docs/WHY_HERCULES.md`
- [ ] 决定是否创建 demo/tiny example 或 transcript plan
- [ ] Codex 复核比较是否准确、不过度营销

### 验收标准

- [ ] 未来“研究这个 repo 能不能吸收到我们的技能组”有标准流程
- [ ] WHY_HERCULES 准确表达：`codex-plugin-cc` lets Claude call Codex；Hercules makes Claude+Codex collaboration governable, auditable, and safe
- [ ] 不 vendor 外部源码，不夸大未验证能力
- [ ] validator / diff checks 通过
- [ ] Codex review PASS

### Trajectory

```yaml
trajectory:
  task_id: TASK-013
  attempt: 1
  date: 2026-07-08
  task_type: docs
  skill_versions:
    agent-plugin-dependency-governance: 1.0.0
    open-ended-research-orchestration: 1.0.0
  score: provisional
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: not-launched
    codex_result: not-launched
    verification:
      commands: []
      logs: []
      diff_scope: "skills/agent-plugin-dependency-governance/, skills/open-ended-research-orchestration/, docs/WHY_HERCULES.md"
    cr_ids: []
    blocker_type: scope
    next_owner: User
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-013"
    review_record: "暂无"
    logs: []
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
