#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
from importlib import metadata
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Python and LangGraph runtime requirements."
    )
    parser.add_argument(
        "--min-python",
        default="3.10",
        help="Minimum Python version. Default: 3.10",
    )
    parser.add_argument(
        "--write-json",
        default="",
        help="Optional output path for JSON report.",
    )
    return parser.parse_args()


def version_tuple(value: str) -> tuple[int, int]:
    major, minor = value.split(".", 1)
    return int(major), int(minor)


def main() -> int:
    args = parse_args()
    py_req = version_tuple(args.min_python)
    py_now = (sys.version_info.major, sys.version_info.minor)
    py_ok = py_now >= py_req

    has_langgraph = importlib.util.find_spec("langgraph") is not None
    langgraph_version = ""
    if has_langgraph:
        try:
            langgraph_version = metadata.version("langgraph")
        except metadata.PackageNotFoundError:
            langgraph_version = ""

    report = {
        "python_version": platform.python_version(),
        "python_required": args.min_python,
        "python_ok": py_ok,
        "langgraph_installed": has_langgraph,
        "langgraph_version": langgraph_version,
        "ok": py_ok and has_langgraph,
    }

    if args.write_json:
        out_path = Path(args.write_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
