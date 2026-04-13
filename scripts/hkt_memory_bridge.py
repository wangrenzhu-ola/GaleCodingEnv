#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "galeenv.config.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (REPO_ROOT / path).resolve()


def hkt_repo() -> Path:
    return resolve_path(load_config()["paths"]["hktMemoryRepo"])


def hkt_script() -> Path:
    return hkt_repo() / "scripts" / "hkt_memory_v5.py"


def base_command() -> list[str]:
    script = hkt_script()
    if not script.exists():
        raise FileNotFoundError(f"HKT-memory script not found: {script}")
    if shutil_which("uv"):
        return ["uv", "run", str(script)]
    return [sys.executable, str(script)]


def shutil_which(name: str) -> str | None:
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / name
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def run_hkt(arguments: list[str]) -> int:
    command = base_command() + arguments
    completed = subprocess.run(command, cwd=hkt_repo())
    return completed.returncode


def verify() -> int:
    payload = {
        "repo_exists": hkt_repo().exists(),
        "script_exists": hkt_script().exists(),
        "uv_available": bool(shutil_which("uv")),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["repo_exists"] and payload["script_exists"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="hkt_memory_bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.set_defaults(handler=lambda _: verify())

    retrieve_parser = subparsers.add_parser("retrieve")
    retrieve_parser.add_argument("--query", required=True)
    retrieve_parser.add_argument("--limit", type=int, default=5)
    retrieve_parser.set_defaults(
        handler=lambda args: run_hkt(
            ["retrieve", "--query", args.query, "--layer", "all", "--limit", str(args.limit)]
        )
    )

    store_parser = subparsers.add_parser("store")
    store_parser.add_argument("--title", required=True)
    store_parser.add_argument("--content", required=True)
    store_parser.add_argument("--topic", default="galeenv")
    store_parser.set_defaults(
        handler=lambda args: run_hkt(
            [
                "store",
                "--title",
                args.title,
                "--content",
                args.content,
                "--topic",
                args.topic,
                "--layer",
                "all",
            ]
        )
    )

    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
