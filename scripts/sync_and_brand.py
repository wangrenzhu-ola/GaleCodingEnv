#!/usr/bin/env python3
import argparse
import fnmatch
import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "galeenv.config.json"
TEXT_EXTENSIONS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".sh",
    ".py",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".css",
    ".html",
    ".xml",
    ".svg",
    ".toml",
    ".ini",
    ".env",
    ".sql",
}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def absolute_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (REPO_ROOT / path).resolve()


def path_matches(path: Path, patterns: list[str], base: Path) -> bool:
    rel = path.relative_to(base).as_posix()
    for pattern in patterns:
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True
    return False


def should_treat_as_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        chunk = path.read_bytes()[:2048]
    except OSError:
        return False
    return b"\x00" not in chunk


def copy_tree(source: Path, target: Path, exclude_globs: list[str]) -> tuple[int, int]:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    copied_files = 0
    copied_dirs = 0
    for item in source.rglob("*"):
        if path_matches(item, exclude_globs, source):
            continue
        relative = item.relative_to(source)
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            copied_dirs += 1
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, destination)
        copied_files += 1
    return copied_dirs, copied_files


def apply_rules(text: str, rules: list[dict]) -> tuple[str, int]:
    current = text
    total = 0
    for rule in rules:
        if rule.get("regex"):
            current, count = re.subn(rule["pattern"], rule["replacement"], current)
        else:
            count = current.count(rule["pattern"])
            if count:
                current = current.replace(rule["pattern"], rule["replacement"])
        total += count
    return current, total


def brand_workspace(mode: str) -> tuple[int, int]:
    config = load_config()
    mirror = absolute_path(config["paths"]["upstreamMirror"])
    workspace = absolute_path(config["paths"]["brandedWorkspace"])
    preserve_globs = config.get("preserveGlobs", [])
    rules = config["branding"][mode]
    copied_dirs, copied_files = copy_tree(mirror, workspace, config.get("excludeGlobs", []))
    modified_files = 0
    replacement_count = 0
    for file_path in workspace.rglob("*"):
        if not file_path.is_file():
            continue
        if path_matches(file_path, preserve_globs, workspace):
            continue
        if not should_treat_as_text(file_path):
            continue
        original = file_path.read_text(encoding="utf-8", errors="ignore")
        updated, count = apply_rules(original, rules)
        if count:
            file_path.write_text(updated, encoding="utf-8")
            modified_files += 1
            replacement_count += count
    return copied_files + copied_dirs, modified_files + replacement_count


def sync_upstream() -> tuple[int, int]:
    config = load_config()
    source = absolute_path(config["paths"]["upstreamRepo"])
    target = absolute_path(config["paths"]["upstreamMirror"])
    if not source.exists():
        raise FileNotFoundError(f"Upstream repo not found: {source}")
    return copy_tree(source, target, config.get("excludeGlobs", []))


def verify_paths() -> dict:
    config = load_config()
    source = absolute_path(config["paths"]["upstreamRepo"])
    mirror = absolute_path(config["paths"]["upstreamMirror"])
    workspace = absolute_path(config["paths"]["brandedWorkspace"])
    return {
        "upstream_exists": source.exists(),
        "mirror_exists": mirror.exists(),
        "workspace_exists": workspace.exists(),
        "hkt_memory_exists": absolute_path(config["paths"]["hktMemoryRepo"]).exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="sync_and_brand")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync")
    sync_parser.set_defaults(command_name="sync")

    brand_parser = subparsers.add_parser("brand")
    brand_parser.add_argument("--mode", choices=["safe", "aggressive"], default="safe")
    brand_parser.set_defaults(command_name="brand")

    refresh_parser = subparsers.add_parser("refresh")
    refresh_parser.add_argument("--mode", choices=["safe", "aggressive"], default="safe")
    refresh_parser.set_defaults(command_name="refresh")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.set_defaults(command_name="verify")

    args = parser.parse_args()

    if args.command_name == "sync":
        dirs, files = sync_upstream()
        print(json.dumps({"synced_dirs": dirs, "synced_files": files}, ensure_ascii=False, indent=2))
        return

    if args.command_name == "brand":
        copied, changed = brand_workspace(args.mode)
        print(
            json.dumps(
                {"copied_entries": copied, "brand_updates": changed, "mode": args.mode},
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command_name == "refresh":
        dirs, files = sync_upstream()
        copied, changed = brand_workspace(args.mode)
        print(
            json.dumps(
                {
                    "synced_dirs": dirs,
                    "synced_files": files,
                    "copied_entries": copied,
                    "brand_updates": changed,
                    "mode": args.mode,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print(json.dumps(verify_paths(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
