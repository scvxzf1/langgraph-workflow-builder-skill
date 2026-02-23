# LangGraph Workflow Builder Skill

一个用于 **Codex / Claude Code / Claude.ai / API** 的 LangGraph 技能包。
它帮助你快速完成 LangGraph 工作流设计、实现、调试和迭代。

## 能力范围

- `StateGraph` 状态建模
- `add_conditional_edges` 条件路由
- `Send` 并行 worker 编排
- `Command` 动态跳转
- `interrupt` + checkpointer 人在回路与恢复

## 目录结构

```text
langgraph-workflow-builder/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

## 安装方式

### 1) 安装到 Codex

将 `langgraph-workflow-builder` 目录复制到：

- `$CODEX_HOME/skills/`
- 若未设置 `CODEX_HOME`，通常是 `~/.codex/skills/`

然后重启 Codex 会话。

### 2) 安装到 Claude.ai

1. 把 `langgraph-workflow-builder` 文件夹打包为 zip。
2. 打开 `Settings -> Capabilities -> Skills`。
3. 点击上传并选择 zip 文件。

### 3) 安装到 Claude Code

两种常见方式：

1. 通过 Claude Code 的 Skills 管理入口导入该文件夹（或 zip）。
2. 放入你的 Claude Code 本地 skills 目录（按本机配置为准），然后重启会话。

> 如果你使用团队工作区，也可以由管理员统一分发技能。

### 4) 通过 API 使用

用于程序化场景（应用、自动化流程、Agent 系统）：

1. 通过 Skills API 管理技能（`/v1/skills`）。
2. 在 Messages API 请求里通过 `container.skills` 传入技能。

## 快速触发示例

- “帮我用 LangGraph 设计一个带 `add_conditional_edges` 的路由图”
- “把这个 Python 脚本改造成 LangGraph 图编排”
- “给我一个带 `interrupt` 和恢复流程的审批图”

## 开发说明

本仓库中的 Skill 内容由 OpenCode 全权开发与维护。

