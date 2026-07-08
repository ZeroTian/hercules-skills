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

## Archive

Completed tasks TASK-001 through TASK-009 have been archived to keep this ledger compact. See `docs/ai-collaboration/tasks/archive-2026-07.md`. The archive preserves full task records, trajectory blocks, source pointers, and review-record links. This live ledger keeps recently closed tasks (TASK-010, TASK-011), active/backlog tasks (TASK-012, TASK-013), and the template/policy sections.

## [x] TASK-010：P1 productized entry + README landing

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；Codex recheck PASS，按用户授权自动 commit，不 push
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（codex-plugin-cc 对比：入口简单、可执行命令面）
- 关联任务：TASK-008
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-08-task010-productized-entry.md`
- 验证证据：Hermes 已暂存 intended TASK-010 package；`bash -n scripts/hercules` 通过；`scripts/hercules help` 通过；`scripts/hercules validate` 通过；`scripts/hercules bootstrap --check` 通过（audit-only，未安装 optional plugin）；`scripts/hercules status` 通过；`scripts/hercules package` 通过；`scripts/hercules doctor` 通过；`python3 scripts/validate-skill-pack.py` 0 errors / 0 warnings / 3 reflection signals；`git diff --check` 与 `git diff --cached --check` 通过；staged privacy scan 通过。中途 `scripts/hercules package` 初版 privacy scan 误扫自身 secret regex 已修复。Codex 初审发现 `CR-T010-001` executable bit 未暂存、`CR-T010-002` secret hits 写固定 `/tmp`；Hermes 已改为暂存 executable bit 并用内存变量保留前 20 条 hit，不写固定 temp 文件，Codex recheck PASS。
- 阻塞原因：无；用户已授权 TASK-010~013 自动执行、Codex PASS 后自动 commit、不 push

### 目标

降低外部用户的上手成本：提供 `scripts/hercules` 命令入口和 reader-facing README landing，让用户不用先理解全部治理文档也能跑通 validate/bootstrap/status/package/doctor。

### 执行项

- [x] 设计 `scripts/hercules` 子命令：`validate`, `bootstrap --check`, `status`, `package`, `doctor`
- [x] 实现 shell wrapper 并保持无外部依赖
- [x] README 第一屏改为价值主张 + 三步 quickstart + 典型 Hermes→Claude→Codex→verification 流程
- [x] 运行 shell syntax、validator、wrapper 子命令 smoke tests
- [x] Codex 复核 CLI/README 是否降低入口门槛且不削弱治理边界

### 验收标准

- [x] `scripts/hercules validate` 运行 validator、diff check、bootstrap script syntax check，并返回正确 exit code
- [x] `scripts/hercules bootstrap --check` 运行 audit-only bootstrap，不安装 optional plugin
- [x] README 保持 reader-facing，不复制长规则
- [x] validator / diff checks / shell syntax 通过
- [x] Codex review PASS

### Hermes 执行记录

- 授权边界：用户已授权 TASK-010~013 自动执行；每个任务 Codex PASS 后自动 commit；不 push
- Claude 尝试：Claude Code `--effort high --max-turns 30` 超时且无落地改动；Hermes 直接实现并继续独立验证
- 修改文件：`scripts/hercules`, `README.md`, `docs/ai-collaboration/TASKS.md`, `docs/ai-collaboration/OPTIMIZATION_ROADMAP.md`
- wrapper 子命令：`validate`, `bootstrap --check`, `status`, `package`, `doctor`, `help`
- 验证结果：wrapper smoke tests、validator、diff checks、bootstrap audit-only、staged privacy scan 均通过；Codex 初审 FAIL：`CR-T010-001`/`CR-T010-002`；Hermes 已修复；Codex narrow recheck PASS
- 遗留风险：fresh-clone smoke 不在 TASK-010 范围内，已留给 TASK-011

### Codex 复核记录

- 复核日期：2026-07-08
- 初审结果：FAIL / highest P1
- Findings：`CR-T010-001` executable bit 未暂存；`CR-T010-002` privacy scan 将 secret hits 写入固定 `/tmp` 路径
- 修复：Hermes staged executable mode `100755`；privacy scan 改用内存变量 `hits`，不再写固定 temp path
- Recheck：PASS，无剩余 findings
- Review record：`docs/ai-collaboration/codex-reviews/2026-07-08-task010-productized-entry.md`

### Trajectory

```yaml
trajectory:
  task_id: TASK-010
  attempt: 1
  date: 2026-07-08
  task_type: implementation
  skill_versions:
    writing-plans: 1.1.0
  score: 0.8
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: timeout-no-edits-then-Hermes-direct-implementation
    codex_result: PASS-after-CR-T010-001-CR-T010-002
    verification:
      commands: ["bash -n scripts/hercules", "scripts/hercules help", "scripts/hercules validate", "scripts/hercules bootstrap --check", "scripts/hercules status", "scripts/hercules package", "scripts/hercules doctor", "python3 scripts/validate-skill-pack.py", "git diff --check"]
      logs: ["/tmp/task010_productized_entry_prompt.md"]
      diff_scope: "scripts/hercules, README.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/OPTIMIZATION_ROADMAP.md"
    cr_ids: ["CR-T010-001", "CR-T010-002"]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-010"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-08-task010-productized-entry.md"
    logs: []
```

## [x] TASK-011：P1/P2 validator release gate + fresh-clone smoke

- 当前状态：已完成
- 优先级：P1
- 当前负责人：无
- 下一负责人：无
- 下一步：无；TASK-011 release gate 已完成并经 Codex PASS，按用户授权自动进入 TASK-012
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（发布门禁与可迁移证明）
- 关联任务：TASK-010
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-08-task011-validator-release-gate.md`（初审 FAIL；CR-T011-001~005 已修复；最终 Codex recheck PASS）
- 验证证据：TDD red run observed expected failures before implementation；CR fix RED observed for inline linked-file and staged-only smoke tests；final verification passed after CR fixes: `python3 tests/test_validate_skill_pack_cli.py -v` OK (6 tests); `python3 scripts/validate-skill-pack.py` 0 errors / 0 warnings / 3 signals; `python3 scripts/validate-skill-pack.py --json` machine-parseable via `python3 -m json.tool`; `python3 scripts/validate-skill-pack.py --strict` exit 0; `scripts/smoke-fresh-clone.sh` passed in temp clone using staged-only default; `scripts/hercules validate` passed; `scripts/hercules package` passed; `git diff --check` 与 `git diff --cached --check` passed; staged privacy scan passed
- 阻塞原因：无；用户已授权 TASK-010~013 自动执行、Codex PASS 后自动 commit、不 push

### 目标

把 `scripts/validate-skill-pack.py` 从结构检查升级为可供 Hermes/Codex/CI 消费的 release gate，并增加 fresh-clone smoke proof。

### 执行项

- [x] 增加 `--json` 输出
- [x] 增加 `--strict` 模式
- [x] 增加 untracked candidate disposition 检查（沿用 visible-vs-tracked warning，并由 `--strict` release gate 阻断）
- [x] 增加 `references/` / `templates/` / `scripts/` / `assets/` 深度链接检查
- [x] 新增 `scripts/smoke-fresh-clone.sh` repo-level smoke script
- [x] 为 validator/smoke 增加可运行验证；Codex review PASS

### 验收标准

- [x] JSON 输出可机器解析
- [x] strict mode 对 release-blocking warning 失败
- [x] fresh-clone smoke 使用临时目录，不修改源 repo
- [x] 当前 repo normal validation 与 strict validation 通过；无 strict 例外
- [x] Codex review PASS

### Hermes 执行记录

- 授权边界：用户已授权 TASK-010~013 自动执行；每个任务 Codex PASS 后自动 commit；不 push
- TDD RED：`python3 tests/test_validate_skill_pack_cli.py -v` 初次失败，缺少 `--json`、`--strict` 与 smoke script
- 实现：validator 增加 `--json`、`--strict`、skill-local linked-file deep check；新增 `scripts/smoke-fresh-clone.sh`；新增 unittest smoke tests；补齐 `workflow-skill-pack-audit/references/round2-reconciliation-pattern.md` 使 linked-file deep check 零 warning
- 修改文件：`scripts/validate-skill-pack.py`, `scripts/smoke-fresh-clone.sh`, `tests/test_validate_skill_pack_cli.py`, `README.md`, `docs/ai-collaboration/TASKS.md`, `docs/ai-collaboration/OPTIMIZATION_ROADMAP.md`, `skills/workflow-skill-pack-audit/references/round2-reconciliation-pattern.md`
- Codex 初审：FAIL，CR-T011-001 P2 linked-file validation too narrow；CR-T011-002 P2 smoke included unstaged tracked diffs；CR-T011-003 P3 README strict-mode wording imprecise
- Hermes 修复：linked-file classifier now validates normal inline same-skill references while skipping downstream `scripts/run_tests.sh` examples；fresh-clone smoke defaults to staged-only and requires `HERCULES_SMOKE_INCLUDE_UNSTAGED=1` opt-in for unstaged tracked diffs；README states default vs `--strict` exit semantics
- Codex recheck 1：CR-T011-001~003 fixed；新增 CR-T011-004 P2 review record path did not exist / trajectory pointer stale
- Hermes 修复 CR-T011-004：新增并暂存 `docs/ai-collaboration/codex-reviews/2026-07-08-task011-validator-release-gate.md`，同步 trajectory `source_pointers.review_record`
- Codex recheck 2：CR-T011-004 fixed；新增 CR-T011-005 P2 CR IDs were accidentally attached to TASK-001 instead of TASK-011
- Hermes 修复 CR-T011-005：TASK-001 `cr_ids` restored to `[]`；TASK-011 trajectory now carries `CR-T011-001`~`CR-T011-005`
- Codex recheck 3：CR-T011-005 fixed；最终 PASS，highest_severity none
- 遗留风险：signals 仍包含 TASK-007 max-turns 和 TASK-012/TASK-013 backlog blocked，这是反射提示不是 release-blocking warning；TASK-012/TASK-013 将在后续任务中解除 backlog blocker

### Trajectory

```yaml
trajectory:
  task_id: TASK-011
  attempt: 1
  date: 2026-07-08
  task_type: implementation
  skill_versions:
    skill-pack-governance-validation: 1.0.0
  score: 1.0
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: skipped-after-previous-timeout-Hermes-direct-TDD-implementation
    codex_result: PASS
    verification:
      commands: ["python3 tests/test_validate_skill_pack_cli.py -v", "python3 scripts/validate-skill-pack.py", "python3 scripts/validate-skill-pack.py --json", "python3 -m json.tool /tmp/hercules_task011_after_cr_fixes.json", "python3 scripts/validate-skill-pack.py --strict", "scripts/smoke-fresh-clone.sh", "scripts/hercules validate", "scripts/hercules package", "git diff --check", "git diff --cached --check"]
      logs: []
      diff_scope: "scripts/validate-skill-pack.py, scripts/smoke-fresh-clone.sh, tests/test_validate_skill_pack_cli.py, README.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/OPTIMIZATION_ROADMAP.md, skills/workflow-skill-pack-audit/references/round2-reconciliation-pattern.md"
    cr_ids: [CR-T011-001, CR-T011-002, CR-T011-003, CR-T011-004, CR-T011-005]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-011"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-08-task011-validator-release-gate.md"
    logs: []
```

## [x] TASK-012：P2 skill information architecture + TASKS scaling

- 当前状态：已完成
- 优先级：P2
- 当前负责人：无
- 下一负责人：无
- 下一步：无；Codex recheck PASS，按用户授权自动 commit，不 push，并自动进入 TASK-013
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（core skill pack 导航与 ledger 可维护性）
- 关联任务：TASK-011
- 关联审阅：`docs/ai-collaboration/codex-reviews/2026-07-08-task012-information-architecture.md`（初审 FAIL；CR-T012-001~003 已修复；最终 Codex recheck PASS）
- 验证证据：Hermes/Claude 已实现 `docs/ai-collaboration/SKILL_NAVIGATION.md`、`docs/ai-collaboration/tasks/archive-2026-07.md`、live TASKS compact split、validator navigation/archive checks；`python3 tests/test_validate_skill_pack_cli.py -v` OK (6 tests)；`python3 scripts/validate-skill-pack.py` 0 errors / 0 warnings / 2 reflection signals；`python3 scripts/validate-skill-pack.py --json` 可由 `python3 -m json.tool` 解析；`python3 scripts/validate-skill-pack.py --strict` exit 0；`scripts/hercules validate` pass；`scripts/hercules package` pass（staged privacy scan ok）；`git diff --check` 与 `git diff --cached --check` pass。当前 2 个 reflection signals 为 TASK-012 Claude max-turns/brief pressure 与 evidence-package recommendation，非 release-blocking warning；Codex recheck PASS
- 阻塞原因：无；用户已授权 TASK-010~013 自动执行、Codex PASS 后自动 commit、不 push

### 目标

让当前核心 skill pack 更易导航，并降低 `TASKS.md` 长期膨胀带来的上下文成本。

### 执行项

- [x] 定义 role/maturity metadata：entry / atom / specialized / archived 等
- [x] 更新组合图和 skill 分类说明
- [x] 设计并实施 TASKS active/archive split：`docs/ai-collaboration/tasks/archive-2026-07.md` 保存 TASK-001~TASK-009，live `TASKS.md` 保留 archive pointer、recent TASK-010~011、active/backlog TASK-012~013 与模板
- [x] 更新 validator 可检查的分类一致性与 archive link / duplicate task-id checks
- [x] Codex 复核 ledger truth 未丢失

### 验收标准

- [x] 新用户能区分 entry skills 与 atoms
- [x] 主 TASKS 只保留 active/recently closed，历史任务可回溯
- [x] archive 链接和 review records 不断链（validator 检查 archive target 与 live/archive task-id 重复）
- [x] validator 通过
- [x] Codex review PASS

### Hermes 执行记录

- 授权边界：用户已授权 TASK-010~013 自动执行；每个任务 Codex PASS 后自动 commit；不 push
- Claude 尝试：Claude Code `--effort high --max-turns 30` 达到 max turns 后留下部分文档改动；Hermes 接管完成 validator checks、ledger truth、验证与 Codex review loop
- 修改文件：`docs/ai-collaboration/SKILL_NAVIGATION.md`, `docs/ai-collaboration/tasks/archive-2026-07.md`, `docs/ai-collaboration/TASKS.md`, `scripts/validate-skill-pack.py`, `README.md`, `docs/ai-collaboration/README.md`, `docs/ai-collaboration/ARCHITECTURE.md`, `docs/ai-collaboration/SKILL_GROUP_AUDIT.md`, `docs/ai-collaboration/SKILL_GROUP_DEEP_RESEARCH_2026-07-05.md`, `docs/ai-collaboration/OPTIMIZATION_ROADMAP.md`
- Codex 初审：FAIL；`CR-T012-001` stale evidence, `CR-T012-002` duplicate navigation rows not detected, `CR-T012-003` missing required archive-link assertion
- Hermes 修复：同步 TASK-012 evidence/trajectory；validator now detects duplicate `SKILL_NAVIGATION.md` rows；validator now warns for non-empty unlinked task archive files, including malformed archives without parseable task headings
- Codex recheck：CR-T012-001/002 fixed；CR-T012-003 first recheck still found malformed archive edge case；second recheck PASS / highest severity none

### Codex 复核记录

- Review record：`docs/ai-collaboration/codex-reviews/2026-07-08-task012-information-architecture.md`
- 最终结果：PASS；无剩余 findings
- 遗留风险：reflection signals 仍提示 TASK-012 max-turns/brief pressure 与 evidence-package recommendation，作为后续 meta-skill evidence signal，不阻塞 release

### Trajectory

```yaml
trajectory:
  task_id: TASK-012
  attempt: 1
  date: 2026-07-08
  task_type: docs
  skill_versions:
    workflow-skill-pack-audit: 1.1.0
  score: 1.0
  actor_path: "User decision -> Hermes plan -> Claude implement -> Hermes verify -> Codex"
  phi:
    capability_preflight: cached
    relevant_capabilities: []
    effort: high
    claude_result: max-turns-after-partial-edits-Hermes-finished
    codex_result: PASS-after-CR-T012-001-CR-T012-002-CR-T012-003
    verification:
      commands: ["python3 tests/test_validate_skill_pack_cli.py -v", "python3 scripts/validate-skill-pack.py", "python3 scripts/validate-skill-pack.py --json", "python3 -m json.tool /tmp/hercules_task012_validator.json", "python3 scripts/validate-skill-pack.py --strict", "scripts/hercules validate", "scripts/hercules package", "git diff --check", "git diff --cached --check"]
      logs: ["/tmp/task012_information_architecture_prompt.md"]
      diff_scope: "README.md, docs/ai-collaboration/README.md, docs/ai-collaboration/ARCHITECTURE.md, docs/ai-collaboration/SKILL_GROUP_AUDIT.md, docs/ai-collaboration/SKILL_GROUP_DEEP_RESEARCH_2026-07-05.md, docs/ai-collaboration/SKILL_NAVIGATION.md, docs/ai-collaboration/TASKS.md, docs/ai-collaboration/tasks/archive-2026-07.md, docs/ai-collaboration/OPTIMIZATION_ROADMAP.md, scripts/validate-skill-pack.py"
    cr_ids: ["CR-T012-001", "CR-T012-002", "CR-T012-003"]
    blocker_type: none
    next_owner: none
  source_pointers:
    task_record: "docs/ai-collaboration/TASKS.md#task-012"
    review_record: "docs/ai-collaboration/codex-reviews/2026-07-08-task012-information-architecture.md"
    logs: []
```

## [ ] TASK-013：P2/P3 external absorption workflow + WHY_HERCULES outreach package

- 当前状态：待处理
- 优先级：P2
- 当前负责人：Hermes
- 下一负责人：Hermes
- 下一步：TASK-012 Codex PASS 并自动提交后，Hermes/Claude 将 `codex-plugin-cc` 研究吸收流程产品化，并产出对外说明
- 是否需要 Codex 复核：是
- 创建日期：2026-07-08
- 最后更新：2026-07-08
- 来源：优化路线图（让“研究某 repo 能否吸收到技能组”可复用；对外传播）
- 关联任务：TASK-007, TASK-008
- 关联审阅：暂无
- 验证证据：待补充
- 阻塞原因：无；用户已授权 TASK-010~013 自动执行、Codex PASS 后自动 commit、不 push

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
    blocker_type: none
    next_owner: Hermes
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
