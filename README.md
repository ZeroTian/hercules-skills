# Hercules

[English](#english) | [中文](#中文)

## English

Hercules is an adaptive Hermes skill group. It discovers the capabilities already installed on your machine and composes them for the current task. It does not install, configure, authenticate, or require Claude, Codex, MCP servers, or plugins.

### Quickstart

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
/skill hercules
```

Hercules starts from the task, inspects only relevant local capabilities, uses confirmed plugins when helpful, and falls back without changing your environment.

## 中文

Hercules 是一组自适应的 Hermes Skills。它会发现机器上已有的能力，并根据当前任务进行组合。它不会安装、配置或执行认证，也不要求预先具备 Claude、Codex、MCP Server 或插件。

### 快速开始

```bash
curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/init.sh | bash
hermes --tui
/skill hercules
```

Hercules 从任务出发，只检查相关的本地能力；确认插件有帮助时才使用，并在不可用时回退，全程不改变你的环境。

## Internal Skills / 内部 Skills

| Skill | Purpose / 用途 |
|---|---|
| `hercules` | Single public entry and task router / 唯一公开入口与任务路由 |
| `hercules-capability-discovery` | Demand-led local capability discovery / 按需发现本地能力 |
| `hercules-collaborative-workflow` | Compose confirmed capabilities for execution / 组合已确认能力执行任务 |
| `hercules-review-workflow` | Select an appropriate review path / 选择合适的复核路径 |
| `hercules-project-init` | Initialize project-scoped guidance / 初始化项目级指引 |

## License

MIT. See [LICENSE](LICENSE).

## Contributing

Contributor workflows and maintainer commands live in [`.maintain/README.md`](.maintain/README.md).
