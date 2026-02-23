# LangGraph 官方能力速查

本文件用于提供可快速引用的官方事实和 API 要点。
信息来源：
- https://github.com/langchain-ai/langgraph
- https://github.com/langchain-ai/langgraph/blob/main/README.md
- https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/pyproject.toml
- https://docs.langchain.com/oss/python/langgraph/quickstart
- https://docs.langchain.com/oss/python/langgraph/workflows-agents
- https://docs.langchain.com/oss/python/langgraph/interrupts

## 1. 基础事实

- 安装：`pip install -U langgraph`
- 当前仓库版本：`1.0.9`
- Python 要求：`>=3.10`
- 核心定位：面向长生命周期、有状态工作流与代理的低层图编排框架

## 2. Graph API 最小闭环

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str

def a(state: State) -> dict:
    return {"text": state["text"] + "a"}

builder = StateGraph(State)
builder.add_node("a", a)
builder.add_edge(START, "a")
builder.add_edge("a", END)
graph = builder.compile()
```

## 3. 常用控制流

- 线性：`add_edge("node1", "node2")`
- 条件路由：`add_conditional_edges("router", route_fn, {...})`
- 动态跳转：节点返回 `Command(goto="next_node")`
- 并行 fan-out：在条件边或路由中返回 `Send(...)` 列表

## 4. 人在回路与恢复

- 在节点中调用 `interrupt(payload)` 暂停执行
- 恢复时调用 `graph.invoke(Command(resume=...), config=...)`
- 使用 checkpointer 才能跨步骤持久化和恢复

## 5. 实战建议

- 先做最小闭环，再引入工具调用和持久化
- 并行写同一键时先定义 reducer，再做 fan-out
- 将外部副作用放到可重试、可幂等节点
- 每个节点只做一件事，避免节点职责过宽
