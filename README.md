# LangGraph Workflow Builder Skill

这是一个面向 Codex / Claude Code 的 Skill，帮助你基于 LangGraph 快速完成：

- 工作流与代理图建模（`StateGraph`）
- 条件路由（`add_conditional_edges`）
- 并行 worker 编排（`Send`）
- 动态跳转（`Command`）
- 人在回路与恢复（`interrupt` + checkpointer）

## 项目结构

```text
langgraph-workflow-builder/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

## 安装到 Codex

将 `langgraph-workflow-builder` 目录复制到 `$CODEX_HOME/skills/`（未设置时通常是 `~/.codex/skills/`），然后重启会话。

## 设计说明

本仓库中的 Skill 内容由 OpenCode 全权开发与整理，目标是给出可执行、可测试、可迭代的 LangGraph 工程实践。

