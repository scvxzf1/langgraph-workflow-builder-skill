#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a minimal LangGraph Python project scaffold."
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for the scaffold project.",
    )
    parser.add_argument(
        "--package",
        default="agent_app",
        help="Python package name under src/. Default: agent_app",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    return parser.parse_args()


def validate_package_name(name: str) -> str:
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", name):
        raise ValueError(
            "Invalid package name. Use letters, numbers, and underscores only."
        )
    return name


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_files(package: str) -> dict[str, str]:
    pyproject = textwrap.dedent(
        f"""\
        [project]
        name = "{package}-langgraph-app"
        version = "0.1.0"
        requires-python = ">=3.10"
        dependencies = [
          "langgraph>=1.0.0",
          "typing-extensions>=4.0.0"
        ]
        """
    )

    init_py = ""

    graph_py = textwrap.dedent(
        """\
        from typing import Literal
        from typing_extensions import TypedDict
        from langgraph.graph import StateGraph, START, END


        class State(TypedDict):
            user_input: str
            intent: str
            result: str


        def classify(state: State) -> dict:
            text = state["user_input"].lower()
            intent = "summarize" if any(k in text for k in ["summary", "summarize"]) else "answer"
            return {"intent": intent}


        def summarize(state: State) -> dict:
            return {"result": f"[summary] {state['user_input']}"}


        def answer(state: State) -> dict:
            return {"result": f"[answer] {state['user_input']}"}


        def route(state: State) -> Literal["summarize", "answer"]:
            return "summarize" if state["intent"] == "summarize" else "answer"


        builder = StateGraph(State)
        builder.add_node("classify", classify)
        builder.add_node("summarize", summarize)
        builder.add_node("answer", answer)
        builder.add_edge(START, "classify")
        builder.add_conditional_edges("classify", route, {
            "summarize": "summarize",
            "answer": "answer",
        })
        builder.add_edge("summarize", END)
        builder.add_edge("answer", END)

        graph = builder.compile()


        if __name__ == "__main__":
            print(graph.invoke({"user_input": "please summarize this", "intent": "", "result": ""}))
        """
    )

    test_py = textwrap.dedent(
        f"""\
        import pathlib
        import sys

        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

        from {package}.graph import graph


        def test_answer_path() -> None:
            out = graph.invoke({{"user_input": "hello", "intent": "", "result": ""}})
            assert out["result"].startswith("[answer]")


        def test_summary_path() -> None:
            out = graph.invoke({{"user_input": "can you summarize this", "intent": "", "result": ""}})
            assert out["result"].startswith("[summary]")
        """
    )

    readme = textwrap.dedent(
        """\
        # LangGraph Scaffold

        ## Quick start

        ```bash
        python -m pip install -e .
        python -m pytest -q
        python src/agent_app/graph.py
        ```
        """
    )

    return {
        "pyproject.toml": pyproject,
        f"src/{package}/__init__.py": init_py,
        f"src/{package}/graph.py": graph_py,
        "tests/test_graph.py": test_py,
        "README.md": readme.replace("agent_app", package),
    }


def main() -> int:
    args = parse_args()
    package = validate_package_name(args.package)
    out_dir = Path(args.out).resolve()
    files = build_files(package)
    created: list[Path] = []

    for rel_path, content in files.items():
        file_path = out_dir / rel_path
        write_file(file_path, content, args.force)
        created.append(file_path)

    print("Scaffold created:")
    for path in created:
        print(f"- {path}")
    print("")
    print("Next:")
    print(f"- cd {out_dir}")
    print("- python -m pip install -e .")
    print("- python -m pytest -q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
