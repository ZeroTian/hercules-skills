# Hercules

[English](#english) | [中文](#中文)

## English

Hercules is a single adaptive Hermes Skill. It discovers the capabilities already installed on your machine and composes them for the current task. It does not install, configure, authenticate, or require Claude, Codex, MCP servers, or plugins.

### Quickstart

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
```

Inside Hermes:

```text
/hercules <your task>
```

If Hermes was already running during an update, use `/reload-skills` or restart it first.

Hercules starts from the task, inspects only relevant local capabilities, uses confirmed plugins when helpful, and falls back without changing your environment.

Hermes owns routing. Once it selects Claude Code, Codex CLI, or another facility, that facility executes the bounded brief directly without re-entering Hercules.

## 中文

Hercules 是一个自适应的 Hermes Skill。它会发现机器上已有的能力，并根据当前任务进行组合。它不会安装、配置或执行认证，也不要求预先具备 Claude、Codex、MCP Server 或插件。

### 快速开始

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
```

进入 Hermes 后：

```text
/hercules <你的任务>
```

如果更新时 Hermes 已在运行，请先执行 `/reload-skills` 或重启 Hermes。

Hercules 从任务出发，只检查相关的本地能力；确认插件有帮助时才使用，并在不可用时回退，全程不改变你的环境。

路由只由 Hermes 负责。Claude Code、Codex CLI 或其他设施一旦被选中，就直接执行限定任务，不再进入 Hercules。

## Public Skill / 公开 Skill

| Skill | Purpose / 用途 |
|---|---|
| `hercules` | Single public entry and task router / 唯一公开入口与任务路由 |

## Internal references / 内部流程

| Reference | Purpose / 用途 |
|---|---|
| `capability-discovery.md` | Demand-led local capability discovery / 按需发现本地能力 |
| `collaborative-workflow.md` | Compose confirmed capabilities for execution / 组合已确认能力执行任务 |
| `invocation-lifecycle.md` | Foreground/background and PTY lifecycle for facility invocation / 设施调用的前台/后台与 PTY 生命周期 |
| `review-workflow.md` | Select an appropriate review path / 选择合适的复核路径 |
| `project-init.md` | Initialize project-scoped guidance / 初始化项目级指引 |

## License

MIT. See [LICENSE](LICENSE).

## Contributing

Contributor workflows and maintainer commands live in [`.maintain/README.md`](.maintain/README.md).
