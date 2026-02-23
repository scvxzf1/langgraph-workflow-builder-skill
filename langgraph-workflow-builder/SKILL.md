---
name: langgraph-workflow-builder
description: 设计、实现、重构和调试基于 Python LangGraph 的工作流与代理，覆盖 StateGraph 状态建模、add_conditional_edges 路由、Send 并行 worker、Command 动态跳转、interrupt 人在回路与 checkpointer 持久化，并输出可运行代码与测试。Use when user asks for LangGraph, StateGraph, add_conditional_edges, Send, Command, interrupt, MemorySaver, SqliteSaver, workflows and agents, LangGraph agent, LangGraph 调优，或把普通脚本改造成图编排。
---

# LangGraph Workflow Builder

## 目标

将需求转成可运行、可测试、可迭代的 LangGraph Python 实现。
优先使用官方 Graph API 习惯用法，并保持最小可运行闭环。

## 执行流程

1. 先明确任务类型，再选图模式。
2. 先给出状态与节点设计，再落代码。
3. 先做最小可运行图，再逐步加能力。
4. 每轮都提供测试结果和下一步改进点。

## 模式决策树

- 任务路径固定、步骤可预测: 选 Prompt Chaining 风格线性图。
- 需要按输入分类到不同处理链路: 选 Routing + `add_conditional_edges`。
- 子任务数量动态且可并发: 选 Orchestrator-worker + `Send`。
- 需要人审或外部批准: 选 `interrupt` + checkpointer。
- 需要节点内同时改状态并跳转: 选 `Command`。

## 第 1 步：收集实现输入

始终先拿到以下信息，不足则补全最小默认值：

- 业务目标: 最终要产出什么。
- 输入输出: 输入结构、输出结构、是否流式输出。
- 工具能力: LLM、工具调用、外部 API、数据库。
- 运行约束: 延迟、成本、容错、是否需要持久化。
- 人工节点: 哪一步必须人工确认或编辑。

## 第 2 步：定义状态与节点契约

- 使用 `TypedDict` 明确状态。
- 对并发写入键使用 reducer，例如 `Annotated[list[T], operator.add]`。
- 为每个节点写清输入键、输出键、副作用、失败策略。
- 路由函数返回值要严格映射到存在的节点名或 `END`。

## 第 3 步：实现图骨架

优先生成可直接运行的最小骨架：

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    task: str
    result: str

def run_task(state: State) -> dict:
    return {"result": f"done: {state['task']}"}

builder = StateGraph(State)
builder.add_node("run_task", run_task)
builder.add_edge(START, "run_task")
builder.add_edge("run_task", END)
graph = builder.compile()
```

如果需要持久化或中断恢复，编译时显式传入 checkpointer。

## 第 4 步：实现高级编排能力

- 路由: `add_conditional_edges`，仅做分流判断。
- 并行 worker: 在条件边中返回 `Send(...)` 列表，聚合到共享 reducer 键。
- 动态跳转: 在节点中返回 `Command(goto=...)`，同时可附带状态更新。
- 人在回路: 在节点中调用 `interrupt(...)`，恢复时用 `graph.invoke(Command(resume=...), config=...)`。

## 第 5 步：测试与迭代

执行三类测试，并保持单次后台测试命令在 60 秒内：

1. 路由测试：验证应触发和不应触发的分支。
2. 功能测试：节点状态更新、工具调用、错误处理。
3. 性能对比：改造前后步骤数、失败率、token 或调用次数。

优先产出 `pytest` 用例，至少覆盖：

- 正常路径
- 路由边界
- 异常路径
- interrupt 恢复路径

## 调试规则

- 不要在裸 `try/except` 中包裹 `interrupt`。
- 不要在同一节点内改变多个 `interrupt` 的顺序。
- `interrupt` 只传可序列化数据。
- 在 `interrupt` 之前的副作用必须幂等，或拆到后续节点。
- 并行写同一状态键时必须定义 reducer。

## 输出要求

每次执行任务时都输出：

1. 选用模式及理由。
2. 状态定义与节点职责表述。
3. 可运行代码或补丁。
4. 测试命令与结果结论。
5. 下一轮可迭代项。

## 资源导航

- 环境检查：`scripts/check_langgraph_env.py`
- 项目脚手架：`scripts/scaffold_langgraph_project.py`
- 官方能力速查：`references/langgraph-core-reference.md`
- 模式映射与验收：`references/langgraph-pattern-mapping.md`
