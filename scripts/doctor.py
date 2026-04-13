#!/usr/bin/env python3
import json
from pathlib import Path

from hkt_memory_bridge import hkt_repo, hkt_script
from sync_and_brand import load_config, absolute_path, verify_paths


REPO_ROOT = Path(__file__).resolve().parent.parent


def collect_payload() -> dict:
    config = load_config()
    upstream = absolute_path(config["paths"]["upstreamRepo"])
    mirror = absolute_path(config["paths"]["upstreamMirror"])
    workspace = absolute_path(config["paths"]["brandedWorkspace"])
    openspec_changes = REPO_ROOT / "openspec" / "changes"
    return {
        "paths": verify_paths(),
        "git": {
            "gale_repo": (REPO_ROOT / ".git").exists(),
            "upstream_repo": (upstream / ".git").exists(),
        },
        "skeleton": {
            "openspec_changes_dir": openspec_changes.exists(),
            "workspace_generated": workspace.exists(),
            "upstream_mirror_generated": mirror.exists(),
            "hkt_memory_repo": hkt_repo().exists(),
            "hkt_memory_script": hkt_script().exists(),
        },
    }


def main() -> int:
    payload = collect_payload()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    checks = [
        payload["paths"]["upstream_exists"],
        payload["git"]["gale_repo"],
        payload["git"]["upstream_repo"],
        payload["skeleton"]["openspec_changes_dir"],
        payload["skeleton"]["hkt_memory_repo"],
        payload["skeleton"]["hkt_memory_script"],
    ]
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
